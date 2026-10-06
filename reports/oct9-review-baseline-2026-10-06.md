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


## Ownership dependency update — 2026-10-06

A broader finalized GSC query/page pull exposed an important dependency that changes how the October 9 review should be handled.

### Denver / Lakewood

Finalized GSC through 2026-10-03 shows:
- `denver appliance pickup` → **/lakewood-appliance-pickup/** — 5 impressions, avg position **10**
- `appliance pick up denver` → **/denver-appliance-pickup/** — 1 impression, avg position **55**
- `appliance removal denver` → **/denver-appliance-pickup/** — 6 impressions, avg position **75.83**

This is a real wrong-page ownership signal, but it is **already under a separate active experiment**:
- experiment: `2026-10-04-lakewood-denver-boundary`
- Lakewood last changed: 2026-10-04
- Lakewood evaluateNotBefore: **2026-10-14**
- change already made: Denver references/links on the Lakewood page were reduced to one explicit address-boundary handoff.

Therefore:
- **Do not make a second Denver/Lakewood ownership change on October 9.**
- On October 9, observe the Denver city experiment only.
- The first fair combined Denver/Lakewood ownership decision is **October 14 or later**, using finalized post-October-4 GSC.
- Do not strengthen the Denver page in a way intended to pull the exact query away from Lakewood while the Lakewood boundary experiment is still measuring that same ownership problem.

### Phoenix

All currently returned Phoenix-modifier rows in the broader finalized GSC pull are owned by **/phoenix-appliance-pickup/**, including:
- `appliance removal phoenix` — 5 impressions, avg position **82.4**
- `appliance removal phoenix, az` — 3 impressions, avg position **81**
- `appliance recycling phoenix` — 2 impressions, avg position **34.5**
- `appliance pick up phoenix` — 1 impression, avg position **64**
- `free appliance removal phoenix` — 1 impression, avg position **17**
- `free appliance removal phoenix az` — 1 impression, avg position **19**

Interpretation:
- Phoenix city-vs-metro ownership is currently **clean in the returned exact-city data**.
- The problem is ranking strength, not wrong-page cannibalization.
- On October 9, do not change city/metro routing unless new finalized evidence shows leakage.
- If exact-city positions remain weak after a mature window, prefer one minimal city-authority/CTR test; do not restructure city-vs-metro ownership again.

### Coachella Valley / Palm Desert

No exact desert-city modifier rows were returned in the broader query filter even though page-level GSC shows Palm Desert and Indio page-one signals.

Interpretation:
- Treat the hub as **discovery/low-data**.
- Protect Palm Desert and Indio.
- Do not use absence of query rows as proof of failure.
- Do not mass-edit Palm Springs, La Quinta, Cathedral City, Rancho Mirage or Indian Wells without page-level evidence.

## Fresh competitor snapshot — checked 2026-10-06

### Denver

TakeMyAppliance currently exposes:
- exact Denver city page
- free-to-submit / no-account request framing
- commercial request path
- Denver neighborhoods and a very large ZIP list
- appliance-specific Denver guides
- FAQ coverage
- official/utility alternatives including Xcel and Denver disposal references

Our Denver page already has:
- direct 720 phone/text
- explicit qualification rules
- mixed-load rule
- direct access/stairs/elevator requirements
- dedicated laundry ownership
- real appliance proof
- official Denver fallback
- commercial/property-manager paths

Decision: the primary measurable gap remains **exact Denver query ownership/strength**, not missing general page features.

### Phoenix

TakeMyAppliance currently exposes:
- exact Phoenix city page
- city neighborhoods and ZIPs
- appliance-specific city guide links
- partner request flow and commercial path

AppliancePickupNow currently exposes:
- Phoenix city page
- photo-first intake
- clear access notes
- city disposal alternative
- request matching and qualification language

Our Phoenix page already has:
- direct 602-726-7552 phone/text
- exact Phoenix city ownership statement
- separate city/metro/laundry routing
- neighborhoods and ZIPs
- official City of Phoenix fallback
- commercial/property/senior/installer paths
- appliance-specific Phoenix child links
- truthful qualification rules

Official City of Phoenix 2026 rates remain:
- up to five non-refrigerant appliances curbside: **$30**
- refrigerant appliance curbside: **$25 each**

Decision: do not add another broad structural block merely for competitor parity. Measure exact-city strength first.

### Palm Desert / Coachella Valley

TakeMyAppliance and AppliancePickupNow both expose Palm Desert-specific pages with broad appliance lists, FAQs and aggressive free/fast language.

The City of Palm Desert currently confirms:
- Burrtec is the contracted waste/recycling provider.
- Residents can schedule bulky-item pickup and place up to **four items** at the curb.
- Large appliances are listed as examples of accepted bulky items.

Our Palm Desert/Coachella content already uses qualification-based language and the official fallback without making blanket same-day/always-free promises.

Decision: protect existing page-one Palm Desert/Indio signals and avoid copying competitor claims that are broader than our operating rules.


## Effective page gates after overlap audit — 2026-10-06

The experiment registry was audited page-by-page across all running experiments. A page is editable only after the **latest evaluateNotBefore date among every running experiment that touches that page**.

### Coachella Valley cluster

All seven pages in `2026-10-01-coachella-v2-cluster` have an effective gate of **2026-10-09**:
- `/coachella-valley-appliance-pickup/`
- `/coachella-valley-washer-dryer-pickup/`
- `/coachella-valley-refrigerator-pickup/`
- `/palm-springs-appliance-pickup/`
- `/palm-desert-appliance-pickup/`
- `/la-quinta-appliance-pickup/`
- `/indio-appliance-pickup/`

This does not mean they should be edited on Oct 9; it only means no overlapping experiment pushes their technical freeze later. Finalized GSC still decides whether any change is warranted.

### Denver

- `/denver-appliance-pickup/` — effective gate **2026-10-09**
- `/denver-washer-dryer-pickup/` — effective gate **2026-10-09**

However, broad Denver-vs-Lakewood ownership cannot be fairly changed until the Lakewood boundary experiment reaches **2026-10-14**. Oct 9 may evaluate Denver-page behavior, but must not make a Denver/Lakewood ownership countermove.

### Phoenix

The Phoenix experiment has mixed effective gates because the city page overlaps another running experiment:

- `/phoenix-appliance-pickup/` — effective gate **2026-10-14**
  - overlapped by `2026-10-01-commercial-authority-links`, last changed 2026-10-04, gate 2026-10-14
- `/phoenix-metro-appliance-pickup/` — effective gate **2026-10-09**
- `/phoenix-washer-dryer-pickup/` — effective gate **2026-10-09**

Therefore:
- **Do not edit the Phoenix city page on Oct 9.**
- Oct 9 may observe city-page data and may evaluate metro/laundry ownership.
- Any Phoenix city-page ranking/CTR/content change must wait until at least Oct 14 and still requires finalized evidence.

## Effective-gate rule

For all future reviews:
1. Determine every running experiment touching the target page.
2. Use the **maximum** `evaluateNotBefore` date as the page's effective gate.
3. If the ranking problem involves a sibling/support page, also respect that sibling page's effective gate.
4. Do not use an earlier experiment's gate to bypass a later overlapping freeze.
