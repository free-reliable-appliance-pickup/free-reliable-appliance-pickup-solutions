# Organic ranking / city-page ownership review — October 10, 2026

## Source, period and interpretation
**Source:** connected Google Search Console for the verified domain property `sc-domain:freereliableappliancepickup.com` (GSC SEO & Content Planner read-only integration).

**Finalized period:** September 11–October 8, 2026; all devices unless explicitly noted. Search Console can withhold or aggregate low-volume queries, and opportunity and page-insight outputs can contain slightly different subsets. Values below are **average positions over impressions**, *not* a current, universal local/mobile SERP rank, and impressions across URLs do not prove they appeared together in a single search. No competitor ranking was directly verified by these GSC data.

**Sitewide baseline:** **2,977 impressions, 45 Google organic clicks, 1.51% CTR, average position 18.66**. This is not the volume of submitted forms, verified calls or actual pickups.

## Five urgent page-ownership gaps (evidence first)

| Search/query or page | Pages surfaced / GSC evidence | Intended query owner | Evidence-driven priority |
|---|---|---|---|
| `free appliance pickup fontana` | Regional `/southern-california-appliance-pickup/`: **11 impressions / avg pos 6.18**; `/fontana-stove-oven-pickup/`: **13 / 18.69**; exact `/fontana-appliance-pickup/`: **7 / 21.57** | `/fontana-appliance-pickup/` | **Highest:** Google is often showing the regional / stove page for general Fontana intent. Preserve stove's **4 organic clicks overall** and avoid blanket redirects |
| `free appliance pickup upland` | `/upland-washer-dryer-pickup/`: **14 / 10.93**; `/san-bernardino-county-appliance-pickup/`: **12 / 11.25**; no page-level results returned for `/upland-appliance-pickup/` in this range | `/upland-appliance-pickup/` | **Highest:** investigate why the general city owner does not surface in returned finalized sample. Missing performance rows do **not** establish `noindex` or non-indexation |
| `free appliance pickup rancho cucamonga` | Main `/rancho-cucamonga-appliance-pickup/` has 64 total page impressions, 2 clicks and avg pos 16.86 overall; page insights returned **2 exact-city query impressions / pos 23**. Query-page overview exposes additional nearby/specialty landing pages | `/rancho-cucamonga-appliance-pickup/` | **High:** maintain city intent; distinguish refrigerator/laundry-specific pages and other-city pages. Do not conflate mixed query-position averages with exact rank |
| `free appliance pickup pasadena` | Main `/pasadena-appliance-pickup/`: **5 exact-query impressions / pos 26.4**, despite overall page avg pos **9.87** on 23 impressions; GSC query-page overview also shows `/south-pasadena-appliance-pickup/` | `/pasadena-appliance-pickup/` | **High:** exact city query is far weaker than broad generic phrases; inspect matching Pasadena vs South Pasadena URLs and mobile SERPs |
| Fresno appliance-specific requests | `/clovis-appliance-pickup/` showed for `stove pickup fresno` (**14 / 2.64**), `washer dryer pickup fresno` (**25 / 4.76**), `refrigerator pickup fresno` (**5 / 4.6**), while `/fresno-appliance-pickup/` received **29 total impressions, 0 clicks, avg pos 25.93** | Fresno general page or the relevant Fresno laundry, stove, refrigerator and freezer specialty page | **High:** city/service ownership; **protect Clovis and other sibling-city visibility while moving intended traffic toward Fresno URLs** |

## Protect wins rather than blindly altering all pages

- `/fontana-stove-oven-pickup/`: **23 impressions, 4 clicks (17.4% CTR)** overall in GSC page insights; broad Fontana-query appearances are not evidence to remove a useful specialty page.
- `/rancho-cucamonga-appliance-pickup/`: **2 clicks** and **64 page impressions** from page insights. There is some organic traffic even though exact-city visibility is still weak.
- `/los-angeles-appliance-pickup/`: **4 clicks** from 151 sitewide summary page impressions.
- `/service-areas/`: **3 clicks** and 98 impressions; `/salem-appliance-pickup/`: **3 clicks**, 78 impressions. Don't deindex hubs or remove city links indiscriminately.
- `/clovis-appliance-pickup/`: 87 page-insight impressions, **0 clicks** (sitewide summary may return 99). High positions for Fresno terms do not yet translate to demonstrated qualified conversions.
- Homepage: **161 impressions and 0 clicks**, avg pos 6.03 for *mixed* searches. **Do not** describe this as rank #6 for the specific query `free appliance pickup near me` without a query-level breakdown.

## What competitor comparison tells us (separate evidence)
The same-city structure comparisons against TakeMyAppliance in `data/competitor-parity-2026-10-10-rialto-redlands-sgv.md` identify repeated and overlapping city sections in Rialto, Redlands, Highland, Moreno Valley, Jurupa Valley and Corona. This is **a content-quality hypothesis, not proof that H2 count causes poor rankings**. Verify results using Search Console and actual SERPs before rewriting.

## Specific next actions by protected experiment dates

**October 13 (Pasadena / some SGV tests)**
1. Retrieve the finalized query/page/device breakdown for `free appliance pickup pasadena` and comparable broader phrases, plus South Pasadena appearances.
2. Confirm the city page is self-canonical and indexable (source already shows a self-canonical, robots index and one H1); verify actual Google-selected canonical / indexing when a URL inspection is available.
3. Only with post-test evidence, change one substantive variable: clarify exact city-owner intent and distinct local pickup access. Keep original working CTA/phone and appointment qualification; measure at least 7–14 days after change.

**October 14 (Fontana, Rancho Cucamonga, Upland, Fresno)**
1. Re-read finalized exact query/page impressions, CTR and positions, split mobile/desktop.
2. Review broad anchor text on county/region pages and specialty pages, and whether they direct general city intent to the intended city page. Prefer useful human-readable city-specific links; avoid keyword-stuffed links or repetitive SEO blocks.
3. One isolated, reversible change per test group only when results warrant it. **Do not** redirect, noindex, or canonicalize a working specialty or sibling-city page merely because it ranks for an overlapping term.
4. Verify that critical city/service content and partner-qualified request workflow stay accurate. Preserve all local phone mappings and real appliance photos.
5. Keep/revise/revert from finalized GSC and *qualified* calls/forms; do not claim the goal of top 1–3 was reached without exact-query external checks.

**October 15 (Rialto, Redlands, Grand Terrace)**
- Review long, overlapping main-content sections against the 5-city matched competitor evidence. Where unique local facts are preserved, test one concise content simplification; do not treat fewer sections as a ranking factor.

## Practical constraints
- The connected third-party GSC trial response reports access through **2026-10-11T21:02:17Z**; native Google Search Console is free and should remain the system of record. A connected-plugin trial ending does not mean the website or Google's own console stops.
- No live form POST was sent, no paid backlinks/citations were bought, and no Google rank improvements are yet attributable to the current technical changes.
- The SEO experiment registry in `data/seo-experiments.json` contains the recorded 2026-10-10 observations while existing content freeze dates remain unchanged.
