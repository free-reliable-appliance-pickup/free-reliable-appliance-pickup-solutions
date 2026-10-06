# October 9 SEO Review Baseline — captured 2026-10-06

## Purpose

This is an evidence snapshot for the three experiments first eligible for review on **2026-10-09**. It is analysis-only. It does **not** authorize a ranking/content edit before the experiment gate or before finalized post-change GSC data is mature enough.

Search Console data available in this capture is finalized through **2026-10-03**.

## Experiment gates

| Experiment | Earliest gate | Preferred review | Decision today |
|---|---:|---:|---|
| 2026-10-01-coachella-v2-cluster | 2026-10-09 | 2026-10-16 | OBSERVE |
| 2026-10-01-denver-intent-separation | 2026-10-09 | 2026-10-16 | OBSERVE |
| 2026-10-01-phoenix-city-metro-separation | 2026-10-09 | 2026-10-16 | OBSERVE |

## Finalized GSC snapshot through 2026-10-03

### Coachella Valley

| Page | Clicks | Impressions | CTR | Avg position |
|---|---:|---:|---:|---:|
| /coachella-valley-appliance-pickup/ | 0 | 5 | 0% | 18.4 |
| /palm-springs-appliance-pickup/ | no row | no row | — | — |
| /palm-desert-appliance-pickup/ | 0 | 12 | 0% | 9.92 |
| /la-quinta-appliance-pickup/ | no row | no row | — | — |
| /indio-appliance-pickup/ | 1 | 3 | 33.3% | 7.0 |

Interpretation: **Palm Desert is a PROTECT candidate**, not a rewrite candidate. Indio retains the same page-one signal as the experiment baseline. Other desert pages remain discovery/low-data and should not be mass-edited.

### Denver

| Page | Clicks | Impressions | CTR | Avg position |
|---|---:|---:|---:|---:|
| /denver-appliance-pickup/ | 0 | 18 | 0% | 39.83 |
| /denver-washer-dryer-pickup/ | 0 | 6 | 0% | 17.33 |

Observed city-page queries include:
- appliance pick up denver — 1 impression, position 55
- appliance removal denver — 6 impressions, position 75.83
- appliance pick up free near me — 2 impressions, position 8
- free refrigerator pick up — 1 impression, position 9

Interpretation: exact Denver-modifier performance is still weak, but the experiment has not had a mature finalized post-change window yet. **No rewrite today.**

### Phoenix

| Page | Clicks | Impressions | CTR | Avg position |
|---|---:|---:|---:|---:|
| /phoenix-appliance-pickup/ | 1 | 47 | 2.13% | 28.45 |
| /phoenix-metro-appliance-pickup/ | no row | no row | — | — |
| /phoenix-washer-dryer-pickup/ | 0 | 3 | 0% | 59.0 |

Observed Phoenix city-page queries include:
- appliance pick up phoenix — 1 impression, position 64
- appliance recycling phoenix — 2 impressions, position 34.5
- appliance removal phoenix — 5 impressions, position 82.4
- free appliance removal phoenix — 1 impression, position 17
- free appliance removal — 2 impressions, position 10

Interpretation: Phoenix city discovery is broader than the original query-only baseline, but exact Phoenix modifiers are not yet strong. The city/metro/laundry separation must remain unchanged until the gate and a fair finalized GSC window.

## Current competitor benchmark

### Palm Desert / Coachella Valley
- AppliancePickupNow exposes explicit appliance categories, city FAQs and ZIP/service-area text.
- TakeMyAppliance exposes city/county hierarchy, appliance-category links, FAQs and partner/request flow.
- Weakness observed on AppliancePickupNow: repeated/misaligned city lists and blanket same-day / always-free style promises.
- Our defensible advantages: direct 909 call/text path, explicit qualification rules, mixed-load rule, truthful route confirmation, access/gate details, and verified City of Palm Desert / Burrtec alternative.

### Denver
- TakeMyAppliance has very deep ZIP coverage and appliance-category links.
- AppliancePickupNow has broad appliance subtype/brand coverage and aggressive free/speed language.
- Local Denver Metro Appliance Recycling has a simple direct phone route and transparent item pricing.
- Our defensible advantages: direct Denver number, qualification transparency, separate laundry ownership, access-first review, commercial/property-manager support and official alternatives.
- Exact Denver modifier strength remains the primary measurable gap.

### Phoenix
- TakeMyAppliance and AppliancePickupNow both have city-specific request flows, broad appliance categories and local-alternative sections.
- City of Phoenix currently documents separate transfer-station rules and scheduled curbside appliance pickup fees; our Phoenix page reflects the current $30 non-refrigerant pickup charge (up to five appliances) and $25 per refrigerant appliance.
- Our defensible advantages: direct 602-726-7552 call/text path, qualification transparency, city-vs-metro routing, working/reusable focus, access review and official fallback detail.
- Exact Phoenix modifiers remain the primary measurable gap.

## Decision rule for October 9+

1. Read finalized GSC first; do not use same-day rank volatility as the trigger.
2. Protect Palm Desert and Indio if page-one signals hold.
3. For Denver/Phoenix, require evidence that the post-change window includes enough finalized days after the October 1 changes.
4. If exact-city modifiers remain weak, prefer one minimal authority/ownership improvement over another full-page rewrite.
5. Do not copy blanket competitor promises, create thin city×appliance pages, or weaken qualification truthfulness.
