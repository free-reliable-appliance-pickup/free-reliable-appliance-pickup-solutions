# TTG FastTrack: Territory Quality & Partner Retention Intelligence
Updated 2026-11-10 | Free Reliable Appliance Pickup

## Business goal
Create a sustainable **monthly partner value proposition**, not one-off territory sales. A territory earns an upgraded rating only if real lead flow translates into working, reusable appliances, completed pickups, profitable resale, and renewals.

**Separate two questions.** (a) Is a market worth investigating? Demographics and competitive supply answer this tentatively. (b) Can the business support a paid partner territory? Only recorded pickups, accurate net resale margins, service capacity, and actual partner retention can answer that.

## Research shortlist, not for sale
The following seven states are research priorities in \`data/market-routing.json\` with \`lead_priority=2\`, while their \`status=request-only\` remains unchanged. Specific cities and county income anchors are in \`data/ttg-markets/national-premium-territory-candidates.json\`.
VA — Northern Virginia; NJ — Somerset/Morris/Bergen; MA — Middlesex/Boston; CT — Fairfield/Southwest; NC — Raleigh-Cary and Charlotte north; GA — North Atlanta; MN — Twin Cities suburbs. Maryland remains a special priority. Existing AZ/CA/CO/FL/ID/NV/OR/TX/UT/WA priorities are unchanged.

Income estimates are 2020–2024 ACS (2024 dollars). Higher-income homes are a **source-location hypothesis**, not evidence of working appliances, quality or buyer profits. Never extrapolate county income to every city or ZIP.

## Per-item data collected privately
Use one record per appliance, with a shared lead ID for multi-item requests. Separate \`working_status=reported_working\` (customer claim) from \`working_status=verified_working\` (an actual test). Log photo evidence, model and condition during intake; add A/B quality grade only when justified by inspection or other reliable confirmation.

For each month + operator territory, count unique leads, appliances, claimed working, verified working, grade A/B, partner-accepted requests, completed pickups, sold units with **realized** resale proceeds and complete costs, and measured net contribution. Record decline and cancellation causes. Always report counts alongside rates: 4 good appliances out of 5 leads is not comparable to 80 good appliances out of 100 leads in business value.

For repeat business, maintain a complete partner-month ledger separately; compute observed next-month renewal rate among partners with **known** renewal outcomes. Partner tenure and satisfaction matter as much as volume; low quality or insufficient earnings should trigger an immediate territory review before the next subscription renewal.

## Territory value framework
1. **Prospecting:** candidate from independent demographics, housing/upgrade activity, university/density indicators and buyer presence; no volume claims.
2. **Lead observation:** unique requests, clear appliance categories, photos, reported working, ZIPs and source attribution.
3. **Fulfillment validation:** true working tests, pickup acceptance, completed visits, travel/access costs, partner feedback.
4. **Economic validation:** realized partner net unit profit, 30/60/90-day trends, repeat demand, churn/refunds and observed renewals.
5. **Commercial review:** only then consider an optional recurring territory agreement with explicit no-guarantee terms and written owner approval. Pricing must account for partner profitability, not just business lead revenue.

### Suggested monthly partner-facing scorecard
- Qualified appliance items and accepted leads (not raw form spam)
- Verified working / A-B reusable items (counts and %; evidence-based)
- Completed pickups and estimated vs **realized** net partner value, separately
- Rejected/expired leads, common defects, and travel losses
- Actual renewal satisfaction or issues; value improvement commitments next month

## Privacy and implementation
Use \`data/territory-quality-schema.json\` to map private consented exports. Do **not** commit raw Formspree submissions, customer names, phones, addresses, photos, full ZIP-level small-cell records, or partner personal contact details to GitHub. The analysis script reads a local private CSV and produces aggregated city-group/territory statistics without IDs. Cohorts below the privacy minimum are suppressed. Internal reports are not intended as public proof of lead volume.

No ongoing automation, live Formspree integration, billing, territory purchase or operator agreement is enabled by this change.

## Phase 2: additional county-anchored research corridors (2026-11-10)
The candidate file now contains **17 corridors** across the first and second research batches. The ten newly added corridors below are hypotheses only. Each income figure is a U.S. Census QuickFacts **2020–2024 median household income** estimate, in 2024 dollars, for the named county—not for each listed city, ZIP, household or appliance.

| Research area (county anchor) | County median income | Initial operating hypothesis |
| --- | ---: | --- |
| Denver south / Douglas County, CO | $149,594 | Premium condition may justify costlier longer routes if verified |
| Nashville south / Williamson County, TN | $135,594 | Test nearby repeat buyers and apartment versus house logistics |
| Columbus north / Delaware County, OH | $133,540 | Potential quality stock; measure completed working units, not clicks |
| Philadelphia west / Chester County, PA | $127,208 | Test appliance reuse and reliable pickups across clustered suburbs |
| Seattle Eastside / King County, WA | $124,746 | Higher travel/labor/building-access expenses may offset quality |
| Dallas north / Collin County, TX | $121,600 | Compare partner-accepted appliances with established Texas volume areas |
| Orange County, CA | $116,289 | Existing California operating benchmark for realized margins |
| North Austin / Williamson County, TX | $111,340 | Fast growth might raise turnover; verify working condition independently |
| Milwaukee west / Waukesha County, WI | $106,076 | Examine dense practical routes, buyer competition and winter handling |
| Boise-Meridian / Ada County, ID | $91,502 | **Growth/volume** hypothesis, not automatically a premium-income territory |

Links to the original Census county tables and a short city-level focus shortlist for **each** corridor are stored in `national-premium-territory-candidates.json`; do not infer that every city shares its anchor county's income. The Ohio, Pennsylvania, Tennessee and Wisconsin state-level **research lead priority** is raised from 3 to 2, but their coverage status remains `request-only`. California, Colorado, Idaho, Texas and Washington priorities were already 2; no status or release changes were made.

### Real-world validation before recurring partner subscriptions
1. **Month 0: map operator and reseller capacity** (who actually buys which major appliance types, ability to serve ZIPs, access constraints, rate of declinations). Candidate businesses are *prospects*, not approved partners.
2. **30-day intake audit:** log every actual incoming lead/item, reliable photos, source, reported working versus unknown, and missing information. Keep incomplete/no-coverage requests in the denominator.
3. **60-day fulfillment audit:** independently verify working units, A/B readiness, partner acceptance, completed pickups, damage/cancellation and full per-item costs.
4. **90-day economics review:** compare medians and totals of observed realized net resale contribution, verified working items, service time, and explicit customer/buyer feedback. Compare territory to matched low-income and mid-income controls; no income-based claims without measurement.
5. **Renewal review:** observed partner renewals and partner feedback only after a genuine renewal decision. If leads are low quality or travel costs erase profit, revise or withhold territory offering rather than charge for an unproven territory.

**Non-negotiable:** No public demand forecast, exclusive sales territory, published partner profit, guaranteed free pickup, auto billing or indexability comes from demographic research. Explicit owner approval plus proven operational coverage and form receipt remains mandatory.
