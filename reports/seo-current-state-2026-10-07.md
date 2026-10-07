# SEO Current-State Checkpoint — 2026-10-07

## Purpose

Preserve the latest ranking/indexability evidence before any further protected-page edits. This checkpoint is intentionally read-only with respect to active SEO experiment pages.

## Data boundaries

- Google Search Console finalized data currently available through 2026-10-04.
- Keyword.com project snapshot checked on 2026-10-07.
- Active experiment freezes remain authoritative; most priority pages are protected until 2026-10-13 through 2026-10-16.
- Do not interpret pre-2026-10-05 GSC performance as evidence against page changes made on 2026-10-05 or 2026-10-06.

## Keyword.com project snapshot

Project: freereliableappliancepickup.com
Tracked keywords: 100

Compared with 2026-10-04:

- Top 3: 11 (was 9, +2)
- Top 10: 23 (was 17, +6)
- Top 20: 34 (was 21, +13)
- Top 30: 44 (was 30, +14)
- Top 100: 47 (was 32, +15)
- Keywords up: 31

This is a broad improvement in ranking coverage, so protected pages should not be rewritten before their evaluation gates unless a verified technical/factual/contact/indexability/safety issue is found.

## Current notable tracked results

Correct/intended city owner examples:

- free appliance pickup Montclair: around positions 5–6 on /montclair-appliance-pickup/
- free appliance pickup Rowland Heights: around position 5 on /rowland-heights-appliance-pickup/
- free appliance pickup Azusa: around position 8 on /azusa-appliance-pickup/
- free appliance pickup San Dimas: around position 9 on /san-dimas-appliance-pickup/
- free appliance pickup La Puente: around positions 14–15 on /la-puente-appliance-pickup/
- free appliance pickup Rialto: around position 17 on /rialto-appliance-pickup/
- free appliance pickup Claremont: around position 17 on /claremont-appliance-pickup/
- free appliance pickup Chino Hills: around positions 20–21 on /chino-hills-appliance-pickup/
- free appliance pickup Walnut: around position 20 on /walnut-appliance-pickup/
- free appliance pickup Fontana: around position 21 on /fontana-appliance-pickup/
- free appliance pickup Rancho Cucamonga: around position 22 on /rancho-cucamonga-appliance-pickup/
- free appliance pickup Pasadena: around position 29 on /pasadena-appliance-pickup/

Known wrong-owner / unstable examples still under active experiment protection:

- free appliance pickup Upland has historically surfaced /upland-washer-dryer-pickup/ instead of the broad city owner.
- Fresno appliance/refrigerator/washer-dryer terms are still split across Clovis, Sanger, Selma and Fresno County pages.
- Some SGV city terms remain volatile or temporarily outside the tracked top 100.

Do not change these protected pages before their gates just because the current scrape is volatile.

## Search Console finalized evidence through 2026-10-04

- Homepage: 136 impressions, 0 clicks, average position about 4.8. A homepage snippet experiment was changed after this data window, so hold.
- Pasadena appliance page: 18 impressions, average position about 6.6. Protected experiment remains active.
- Clovis appliance page: 47 impressions overall, average position about 9.2. Fresno sibling-intent cleanup was changed after the finalized GSC window; hold.
- Fontana appliance page: 24 impressions, average position about 9.2. Exact Fontana broad-intent ownership work was changed after the finalized GSC window; hold.
- Los Angeles appliance page: 141 impressions, 4 clicks, average position about 16.4. Refrigerator-intent support pages are under current experiment controls.
- GSC also continues to show historical cannibalization for Upland and Fontana, but those relationships predate the latest protected owner changes.

## Current competitor landscape from Keyword.com

Top recurring non-self domains appearing in tracked Top 10 SERPs over the recent window include:

1. facebook.com
2. takemyappliance.com
3. goloadup.com
4. yelp.com
5. instagram.com
6. reddit.com
7. fastfreeapplianceremoval.com

TakeMyAppliance remains the most consistent direct appliance-pickup organic competitor. Facebook's high frequency confirms that off-site/social presence can occupy meaningful SERP space alongside traditional websites.

## Technical fixes completed 2026-10-07

1. Expanded the active sitemap audit to inspect all sitemap*.xml files for noindex aliases, meta-refresh redirects and self-canonical consistency.
2. Corrected an escaping bug in the audit regex so canonical/noindex checks actually match HTML.
3. Found and removed /oak-glen-washer-dryer-pickup/ from sitemap-new.xml because the page is intentionally noindex and canonicalized to /san-bernardino-county-washer-dryer-pickup/.
4. Verified /bellflower-refrigerator-pickup/ is a complete, self-canonical, indexable refrigerator page with request form and Bellflower city handoff; added it to the approved indexable service-page registry.
5. Post-fix checks:
   - Audit Active Sitemap Pages: SUCCESS
   - Validate Approved Sitemap: SUCCESS
   - Final SEO Safety Audit: SUCCESS
   - IndexNow submission workflow: SUCCESS

## Decision rule from this checkpoint

Until the relevant experiment gate opens, continue only with:

- verified technical/indexability corrections,
- factual/contact fixes,
- competitor research,
- rank/ownership monitoring,
- non-destructive QA,
- work on pages not covered by an active experiment.

At each gate, compare finalized GSC and Keyword.com ranking ownership against this checkpoint before deciding keep/revise/revert.
