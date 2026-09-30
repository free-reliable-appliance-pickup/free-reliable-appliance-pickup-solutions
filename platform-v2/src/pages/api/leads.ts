import type { APIRoute } from "astro";
import { getSecret } from "astro:env/server";
import { createClient } from "@supabase/supabase-js";
import { routeLeadToMarketplace } from "../../lib/marketplaceMatching";

export const prerender = false;

function textValue(form: FormData, key: string, max = 500) {
  const value = form.get(key);
  if (typeof value !== "string") return "";
  return value.trim().slice(0, max);
}

function parseJson(value: string) {
  if (!value) return {};
  try {
    const parsed = JSON.parse(value);
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

function boundedCount(value: string) {
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed)) return 1;
  return Math.min(20, Math.max(1, parsed));
}

export const POST: APIRoute = async ({ request, redirect }) => {
  const form = await request.formData();

  // Honeypot: bots that fill hidden fields are silently discarded.
  if (textValue(form, "website", 200)) {
    return redirect("/thank-you/", 303);
  }

  const customerName = textValue(form, "customer_name", 120);
  const customerPhone = textValue(form, "customer_phone", 40);
  const city = textValue(form, "city", 120);
  const state = textValue(form, "state", 80);
  const applianceType = textValue(form, "appliance_type", 120);
  const applianceCondition = textValue(form, "appliance_condition", 120);

  if (!customerName || !customerPhone || !city || !state || !applianceType || !applianceCondition) {
    return new Response("Please complete the required fields.", { status: 400 });
  }

  const supabaseUrl = getSecret("SUPABASE_URL");
  const serviceRoleKey = getSecret("SUPABASE_SERVICE_ROLE_KEY");

  if (!supabaseUrl || !serviceRoleKey) {
    console.error("Lead intake is not configured: missing server-side Supabase secrets.");
    return new Response("Pickup request service is temporarily unavailable.", { status: 503 });
  }

  // The service-role key is read only on the server and must never be exposed to browser code.
  const supabase = createClient(supabaseUrl, serviceRoleKey, {
    auth: { persistSession: false, autoRefreshToken: false }
  });

  const sourcePage = textValue(form, "source_page", 500);
  const sourceChannel = textValue(form, "source_channel", 100);
  const market = textValue(form, "market", 160);
  const requestedIntent = textValue(form, "service_intent", 40);
  const serviceIntent =
    requestedIntent === "washer-dryer" ? "washer-dryer" : "appliance";
  const priorityMarkets = new Set([
    "Inland Empire",
    "San Gabriel Valley",
    "SGV–Inland Empire Corridor"
  ]);
  const marketPriority = priorityMarkets.has(market) ? "PRIORITY" : "NEW_MARKET";

  const trackingData = {
    first_touch: parseJson(textValue(form, "first_touch_json", 6000)),
    current_touch: parseJson(textValue(form, "current_touch_json", 6000)),
    service_intent: serviceIntent,
    market: market || null
  };

  const leadRecord = {
    customer_name: customerName,
    customer_phone: customerPhone,
    customer_email: textValue(form, "customer_email", 180) || null,
    city,
    state,
    zip_code: textValue(form, "zip_code", 20) || null,
    appliance_type: applianceType,
    appliance_condition: applianceCondition,
    message: textValue(form, "message", 2000) || null,
    access_summary: textValue(form, "access_summary", 1000) || null,
    appliance_count: boundedCount(textValue(form, "appliance_count", 3)),
    market_priority: marketPriority,
    source_page: sourcePage || null,
    source_channel: sourceChannel || "unknown",
    landing_page: textValue(form, "landing_page", 1000) || null,
    referrer_url: textValue(form, "referrer_url", 1000) || null,
    utm_source: textValue(form, "utm_source", 200) || null,
    utm_medium: textValue(form, "utm_medium", 200) || null,
    utm_campaign: textValue(form, "utm_campaign", 300) || null,
    utm_term: textValue(form, "utm_term", 300) || null,
    utm_content: textValue(form, "utm_content", 300) || null,
    gclid: textValue(form, "gclid", 300) || null,
    msclkid: textValue(form, "msclkid", 300) || null,
    fbclid: textValue(form, "fbclid", 300) || null,
    session_id: textValue(form, "session_id", 100) || null,
    tracking_data: trackingData,
    status: "new"
  };

  const { data, error } = await supabase
    .from("appliance_leads")
    .insert(leadRecord)
    .select("id")
    .single();

  if (error || !data) {
    console.error("Lead insert failed", error);
    return new Response("We could not save the pickup request. Please call or text us instead.", {
      status: 500
    });
  }

  const { error: eventError } = await supabase.from("lead_events").insert({
    lead_id: data.id,
    event_type: "submitted",
    event_data: {
      source_page: sourcePage || null,
      source_channel: sourceChannel || "unknown",
      service_intent: serviceIntent,
      market: market || null,
      market_priority: marketPriority,
      appliance_type: applianceType,
      appliance_condition: applianceCondition
    }
  });

  if (eventError) {
    // The lead itself is already safely stored, so do not make the customer resubmit.
    console.error("Lead event insert failed", eventError);
  }

  const routing = await routeLeadToMarketplace(supabase, {
    id: data.id,
    city,
    state,
    zipCode: textValue(form, "zip_code", 20) || null,
    applianceType,
    applianceCondition,
    applianceCount: boundedCount(textValue(form, "appliance_count", 3)),
    accessSummary: textValue(form, "access_summary", 1000) || null,
    serviceIntent
  });

  const { error: routingEventError } = await supabase.from("lead_events").insert({
    lead_id: data.id,
    event_type: routing.routed ? "marketplace_routed" : "marketplace_held",
    event_data: {
      reason: routing.reason,
      opportunity_id: routing.opportunityId || null,
      offer_count: routing.offerCount || 0,
      customer_private_locked: true
    }
  });

  if (routingEventError) {
    console.error("Marketplace routing lead event insert failed", routingEventError);
  }

  return redirect("/thank-you/", 303);
};
