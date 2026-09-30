type JsonRecord = Record<string, unknown>;

type Territory = {
  id: number;
  state: string;
  city: string | null;
  zip_codes: unknown;
  territory_status: string;
  coverage_level: string;
  protected_buyer_id: number | null;
  opportunity_window_minutes: number;
};

type Buyer = {
  id: number;
  status: string;
  verified: boolean;
  service_areas: unknown;
  appliance_preferences: unknown;
  condition_preferences: unknown;
  reliability_score: number | null;
};

export type MarketplaceLead = {
  id: number | string;
  city: string;
  state: string;
  zipCode?: string | null;
  applianceType: string;
  applianceCondition: string;
  applianceCount: number;
  accessSummary?: string | null;
  serviceIntent: "appliance" | "washer-dryer";
};

export type MarketplaceRouteResult = {
  routed: boolean;
  reason:
    | "matched"
    | "no_active_territory"
    | "no_eligible_buyer"
    | "already_routed"
    | "routing_error";
  opportunityId?: number;
  offerCount?: number;
};

const ACTIVE_BUYER_STATUSES = new Set(["active", "approved"]);
const ROUTABLE_TERRITORY_STATUSES = new Set(["active", "open", "protected"]);
const NON_COVERAGE_LEVELS = new Set(["", "none", "inactive", "unavailable"]);

function normalize(value: unknown) {
  return String(value ?? "").trim().toLowerCase();
}

function normalizeCityState(value: unknown) {
  return normalize(value)
    .replace(/\s+/g, " ")
    .replace(/,\s*/g, ", ");
}

function jsonArray(value: unknown): unknown[] {
  return Array.isArray(value) ? value : [];
}

function includesAnyPreference(value: unknown, needles: string[]) {
  const prefs = jsonArray(value).map(normalize).filter(Boolean);
  if (prefs.length === 0 || prefs.includes("any") || prefs.includes("all")) return true;

  return prefs.some((pref) =>
    needles.some((needle) => pref === needle || pref.includes(needle) || needle.includes(pref))
  );
}

function serviceAreaMatches(value: unknown, city: string, state: string, zipCode?: string | null) {
  const targetCity = normalize(city);
  const targetState = normalize(state);
  const targetZip = normalize(zipCode);
  const targetLabel = normalizeCityState(`${city}, ${state}`);

  for (const area of jsonArray(value)) {
    if (typeof area === "string") {
      const normalized = normalizeCityState(area);
      if (normalized === targetLabel || normalized === targetCity) return true;
      if (targetZip && normalized === targetZip) return true;
      continue;
    }

    if (!area || typeof area !== "object") continue;
    const record = area as JsonRecord;
    const areaCity = normalize(record.city);
    const areaState = normalize(record.state);
    const zips = jsonArray(record.zip_codes ?? record.zips).map(normalize);

    if (areaCity === targetCity && (!areaState || areaState === targetState)) return true;
    if (targetZip && zips.includes(targetZip)) return true;
  }

  return false;
}

function territoryMatches(territory: Territory, city: string, state: string, zipCode?: string | null) {
  if (normalize(territory.state) !== normalize(state)) return false;
  if (!ROUTABLE_TERRITORY_STATUSES.has(normalize(territory.territory_status))) return false;
  if (NON_COVERAGE_LEVELS.has(normalize(territory.coverage_level))) return false;

  const cityMatch = normalize(territory.city) === normalize(city);
  const zips = jsonArray(territory.zip_codes).map(normalize);
  const zipMatch = Boolean(zipCode && zips.includes(normalize(zipCode)));

  return cityMatch || zipMatch;
}

function territoryScore(territory: Territory, city: string, zipCode?: string | null) {
  let score = 0;
  if (normalize(territory.city) === normalize(city)) score += 100;
  if (zipCode && jsonArray(territory.zip_codes).map(normalize).includes(normalize(zipCode))) score += 120;
  if (territory.protected_buyer_id) score += 25;
  return score;
}

function applianceNeedles(applianceType: string, serviceIntent: MarketplaceLead["serviceIntent"]) {
  const type = normalize(applianceType);
  const needles = [type];

  if (serviceIntent === "washer-dryer" || type.includes("washer") || type.includes("dryer")) {
    needles.push("washer", "dryer", "laundry", "washer dryer", "washer and dryer");
  }

  if (type.includes("refrigerator")) needles.push("fridge");
  if (type.includes("stove") || type.includes("range")) needles.push("stove", "range", "oven");
  return Array.from(new Set(needles.filter(Boolean)));
}

function conditionNeedles(condition: string) {
  const normalized = normalize(condition);
  const needles = [normalized];
  if (normalized === "fully working") needles.push("working");
  if (normalized === "needs repair") needles.push("repairable", "repair");
  if (normalized === "not working") needles.push("nonworking", "not working", "broken");
  return Array.from(new Set(needles.filter(Boolean)));
}

function eligibleBuyers(
  buyers: Buyer[],
  territory: Territory,
  lead: MarketplaceLead
) {
  return buyers
    .filter((buyer) => {
      if (!buyer.verified) return false;
      if (!ACTIVE_BUYER_STATUSES.has(normalize(buyer.status))) return false;

      if (territory.protected_buyer_id) {
        if (Number(buyer.id) !== Number(territory.protected_buyer_id)) return false;
      } else if (!serviceAreaMatches(buyer.service_areas, lead.city, lead.state, lead.zipCode)) {
        return false;
      }

      if (!includesAnyPreference(
        buyer.appliance_preferences,
        applianceNeedles(lead.applianceType, lead.serviceIntent)
      )) return false;

      if (!includesAnyPreference(
        buyer.condition_preferences,
        conditionNeedles(lead.applianceCondition)
      )) return false;

      return true;
    })
    .sort((a, b) => {
      const protectedA = territory.protected_buyer_id === a.id ? 1 : 0;
      const protectedB = territory.protected_buyer_id === b.id ? 1 : 0;
      if (protectedA !== protectedB) return protectedB - protectedA;
      return Number(b.reliability_score || 0) - Number(a.reliability_score || 0);
    })
    .slice(0, territory.protected_buyer_id ? 1 : 3);
}

function isHotLaundryLead(lead: MarketplaceLead) {
  const type = normalize(lead.applianceType);
  const working = normalize(lead.applianceCondition) === "fully working";
  return working && (
    lead.serviceIntent === "washer-dryer" ||
    type.includes("washer") ||
    type.includes("dryer")
  );
}

export async function routeLeadToMarketplace(supabase: any, lead: MarketplaceLead): Promise<MarketplaceRouteResult> {
  try {
    const { data: territories, error: territoryError } = await supabase
      .from("marketplace_territories")
      .select("id,state,city,zip_codes,territory_status,coverage_level,protected_buyer_id,opportunity_window_minutes")
      .eq("state", lead.state);

    if (territoryError) throw territoryError;

    const matchedTerritory = ((territories || []) as Territory[])
      .filter((territory) => territoryMatches(territory, lead.city, lead.state, lead.zipCode))
      .sort((a, b) => territoryScore(b, lead.city, lead.zipCode) - territoryScore(a, lead.city, lead.zipCode))[0];

    if (!matchedTerritory) {
      return { routed: false, reason: "no_active_territory" };
    }

    const { data: buyers, error: buyerError } = await supabase
      .from("marketplace_buyers")
      .select("id,status,verified,service_areas,appliance_preferences,condition_preferences,reliability_score")
      .eq("verified", true)
      .in("status", ["active", "approved"]);

    if (buyerError) throw buyerError;

    const matchedBuyers = eligibleBuyers((buyers || []) as Buyer[], matchedTerritory, lead);
    if (matchedBuyers.length === 0) {
      return { routed: false, reason: "no_eligible_buyer" };
    }

    const { data: existing, error: existingError } = await supabase
      .from("marketplace_opportunities")
      .select("id")
      .eq("source_request_id", String(lead.id))
      .limit(1);

    if (existingError) throw existingError;
    if (existing?.length) {
      return {
        routed: true,
        reason: "already_routed",
        opportunityId: Number(existing[0].id)
      };
    }

    const windowMinutes = Math.min(
      120,
      Math.max(5, Number(matchedTerritory.opportunity_window_minutes || 30))
    );
    const expiresAt = new Date(Date.now() + windowMinutes * 60_000).toISOString();

    const { data: opportunity, error: opportunityError } = await supabase
      .from("marketplace_opportunities")
      .insert({
        status: "offered",
        source_request_id: String(lead.id),
        territory_id: matchedTerritory.id,
        city: lead.city,
        state: lead.state,
        zip_code: lead.zipCode || null,
        approximate_area: [lead.city, lead.state, lead.zipCode].filter(Boolean).join(", "),
        appliance_count: lead.applianceCount,
        appliances: [{
          type: lead.applianceType,
          condition: lead.applianceCondition,
          count: lead.applianceCount,
          service_intent: lead.serviceIntent
        }],
        hot_opportunity: isHotLaundryLead(lead),
        owner_reported_summary: `${lead.applianceType}; condition: ${lead.applianceCondition}; count: ${lead.applianceCount}`,
        access_summary: lead.accessSummary || null,
        customer_private_locked: true,
        expires_at: expiresAt
      })
      .select("id")
      .single();

    if (opportunityError) {
      if (opportunityError.code === "23505") {
        const { data: racedOpportunity, error: racedError } = await supabase
          .from("marketplace_opportunities")
          .select("id")
          .eq("source_request_id", String(lead.id))
          .single();

        if (racedError || !racedOpportunity) throw racedError || opportunityError;

        return {
          routed: true,
          reason: "already_routed",
          opportunityId: Number(racedOpportunity.id)
        };
      }

      throw opportunityError;
    }

    if (!opportunity) throw new Error("Opportunity insert returned no row.");

    const offers = matchedBuyers.map((buyer) => ({
      opportunity_id: opportunity.id,
      buyer_id: buyer.id,
      expires_at: expiresAt,
      status: "offered",
      payment_status: "unpaid"
    }));

    const { error: offerError } = await supabase.from("marketplace_offers").insert(offers);
    if (offerError) {
      // Offer creation is a single Postgres statement. If it fails, remove the
      // unoffered opportunity so a later retry can route the lead cleanly.
      const { error: cleanupError } = await supabase
        .from("marketplace_opportunities")
        .delete()
        .eq("id", opportunity.id)
        .eq("source_request_id", String(lead.id))
        .is("purchased_by", null);

      if (cleanupError) {
        console.error("Marketplace opportunity cleanup failed after offer error", cleanupError);
      }

      throw offerError;
    }

    const events = [
      {
        opportunity_id: opportunity.id,
        event_type: "opportunity_created",
        event_data: {
          territory_id: matchedTerritory.id,
          service_intent: lead.serviceIntent,
          customer_private_locked: true
        }
      },
      ...matchedBuyers.map((buyer) => ({
        opportunity_id: opportunity.id,
        buyer_id: buyer.id,
        event_type: "offer_created",
        event_data: {
          expires_at: expiresAt,
          protected_territory: matchedTerritory.protected_buyer_id === buyer.id
        }
      }))
    ];

    const { error: eventError } = await supabase.from("marketplace_events").insert(events);
    if (eventError) {
      console.error("Marketplace event insert failed", eventError);
    }

    return {
      routed: true,
      reason: "matched",
      opportunityId: Number(opportunity.id),
      offerCount: matchedBuyers.length
    };
  } catch (error) {
    console.error("Marketplace routing failed", error);
    return { routed: false, reason: "routing_error" };
  }
}
