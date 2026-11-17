# California laundry integrated release — November 16, 2026

**Draft, not deployed.** Source base `main` commit `09c13d7348361b44d0f73d0228b8d1df22185599`. This is one combined review candidate from #1384, #1389, #1390, #1391. It does not add new city pages.

## Exact inventory

- 36 pre-existing California laundry service pages / county pages.
- #1384: 9 existing washer/dryer forms; customer-selected floor/location and stairs, truthful city/service/source attribution and Pico Rivera blank-first appliance selection.
- #1389: 15 existing pages with invisible FAQPage JSON-LD that failed to correspond to displayed Q&A; remove invalid FAQ nodes, retain one verified visible Chino pair and original Service/BreadcrumbList.
- #1390: 8 Inland Empire forms with required blank-first location and stairs, plus missing city/service static attribution.
- #1391: 6 California pages with observed search traffic, with required blank-first location/stairs and missing attribution.
- Overlap of #1384 and #1389 on Chino and Chino Hills: exact #1384 pickup forms injected into #1389 page bodies. All #1389 non-form bytes preserved.
- Existing `CHANGELOG-SEO.md` entry from #1384 and seven source-only test/workflow files are included.

### Existing page list (36)

- `baldwin-park-washer-dryer-pickup/index.html`
- `banning-washer-dryer-pickup/index.html`
- `beaumont-washer-dryer-pickup/index.html`
- `bloomington-washer-dryer-pickup/index.html`
- `chino-hills-washer-dryer-pickup/index.html`
- `chino-washer-dryer-pickup/index.html`
- `claremont-washer-dryer-pickup/index.html`
- `corona-washer-dryer-pickup/index.html`
- `eastvale-washer-dryer-pickup/index.html`
- `el-monte-washer-dryer-pickup/index.html`
- `fontana-washer-dryer-pickup/index.html`
- `glendora-washer-dryer-pickup/index.html`
- `hesperia-washer-dryer-pickup/index.html`
- `jurupa-valley-washer-dryer-pickup/index.html`
- `los-angeles-county-washer-dryer-pickup/index.html`
- `menifee-washer-dryer-pickup/index.html`
- `montebello-washer-dryer-pickup/index.html`
- `moreno-valley-washer-dryer-pickup/index.html`
- `murrieta-washer-dryer-pickup/index.html`
- `ontario-washer-dryer-pickup/index.html`
- `orange-county-washer-dryer-pickup/index.html`
- `perris-washer-dryer-pickup/index.html`
- `pico-rivera-washer-dryer-pickup/index.html`
- `pomona-washer-dryer-pickup/index.html`
- `redlands-washer-dryer-pickup/index.html`
- `riverside-washer-dryer-pickup/index.html`
- `sacramento-metro-washer-dryer-pickup/index.html`
- `san-bernardino-washer-dryer-pickup/index.html`
- `san-francisco-washer-dryer-pickup/index.html`
- `san-luis-obispo-washer-dryer-pickup/index.html`
- `san-marcos-washer-dryer-pickup/index.html`
- `south-el-monte-washer-dryer-pickup/index.html`
- `temple-city-washer-dryer-pickup/index.html`
- `upland-washer-dryer-pickup/index.html`
- `visalia-washer-dryer-pickup/index.html`
- `west-covina-washer-dryer-pickup/index.html`

## Verification and release criteria

No customer data submitted. No verified live Formspree receipt or deployment claim. Do not change page titles, H1, canonical tags, robots tags, public hero images, regional phone routing, service availability assertions, search experiments or visible marketing text outside the targeted forms. No guarantee of SEO ranking changes.

Before merging: all applicable exact-integrated-head Actions and CodeQL green; independent review of the consolidated validators, forms and structured data; address unresolved defects; explicit accountable maintainer approval per `docs/TTG_RELEASE_POLICY.md`. Individual source-branch green checks are NOT sufficient to authorize this batch. After approved merge: verify the exact deployed content, genuine owner-controlled Formspree receipts, mobile layout, and Search Console query/page impressions and clicks. Roll back on regression.

Until this candidate is independently reviewed and approved, do not merge predecessors #1384, #1389, #1390 or #1391 separately. No merge approval is implied by preparation of this draft.
