# Finalized Search Console: city-and-service page ownership checkpoint

**Retrieved:** October 16, 2026. **Source:** authorized Windsor.ai `searchconsole` connector, property `sc-domain:freereliableappliancepickup.com`. **Data range:** September 16–October 12, 2026; `include_fresh_data=false`. **Scope:** Google Search Console web performance query×page×device rows; 27-day reporting window. **Site:** Free Reliable Appliance Pickup.

## Interpretation constraints

- Values are Google Search Console **impressions attributed to pages**, not unique searches or unique users. The same query may display multiple URLs across searches or surfaces; dividing owner page impressions by all matching page impressions is a **descriptive proportion**, not the probability that Google will rank that URL.
- Average position is impression-weighted and may combine locations, devices, result types and positions; **not** a manual, fixed local SERP rank. A missing owner row means no matching row was returned in this slice; **not** proof the URL is unindexed.
- No query edits, no emergency canonical or noindex changes, no Google penalty claims. Query data can be anonymized/filtered and differs from aggregate page totals.
- This is a **baseline before** October 16 image and form fixes. It cannot prove an effect from those deployments and should not be presented as post-fix rankings.

## Exact query → intended owner evidence

| Exact search query | Intended owner | GSC page impressions: owner / all | Owner's share | Owner avg position | Most visible alternative(s) | Latest overlapping review gate |
|---|---|---:|---:|---:|---|---|
| free appliance pickup rancho cucamonga | `rancho-cucamonga-appliance-pickup/` | 7 / 37 | 19% | 28 | `rancho-cucamonga-refrigerator-pickup/` (8); `southern-california-refrigerator-pickup/` (8) | none |
| appliance pickup rancho cucamonga | `rancho-cucamonga-appliance-pickup/` | 2 / 3 | 67% | 34 | `southern-california-refrigerator-pickup/` (1) | none |
| free appliance pickup upland | `upland-appliance-pickup/` | 0 / 60 | 0% | not returned | `upland-washer-dryer-pickup/` (15); `san-bernardino-county-appliance-pickup/` (12) | none |
| free appliance pickup fontana | `fontana-appliance-pickup/` | 11 / 44 | 25% | 21.6 | `fontana-stove-oven-pickup/` (13); `southern-california-appliance-pickup/` (11) | none |
| free appliance pickup claremont | `claremont-appliance-pickup/` | 8 / 26 | 31% | 16 | `claremont-washer-dryer-pickup/` (18) | none |
| free appliance pickup arcadia | `arcadia-appliance-pickup/` | 8 / 37 | 22% | 20.4 | `arcadia-refrigerator-pickup/` (15); `baldwin-park-appliance-pickup/` (8) | none |
| free appliance pickup pasadena | `pasadena-appliance-pickup/` | 11 / 27 | 41% | 27.2 | `south-pasadena-appliance-pickup/` (14); `(homepage)` (2) | none |
| free appliance pickup rowland heights | `rowland-heights-appliance-pickup/` | 21 / 55 | 38% | 8 | `hacienda-heights-appliance-pickup/` (13); `service-areas/` (11) | none |
| free appliance pickup chino | `chino-appliance-pickup/` | 18 / 34 | 53% | 20.6 | `chino-hills-appliance-pickup/` (10); `diamond-bar-appliance-pickup/` (5) | none |
| free appliance pickup chino hills | `chino-hills-appliance-pickup/` | 16 / 30 | 53% | 23.3 | `chino-appliance-pickup/` (14) | none |
| free appliance pickup san dimas | `san-dimas-appliance-pickup/` | 9 / 24 | 38% | 13.2 | `san-gabriel-valley-appliance-pickup/` (6); `san-gabriel-inland-empire-appliance-pickup/` (5) | none |
| free appliance pickup montclair | `montclair-appliance-pickup/` | 24 / 24 | 100% | 8.4 | none | none |
| washer dryer pickup fresno | `fresno-washer-dryer-pickup/` | 0 / 76 | 0% | not returned | `clovis-appliance-pickup/` (25); `sanger-washer-dryer-pickup/` (18) | none |
| free washer and dryer pickup fresno | `fresno-washer-dryer-pickup/` | 0 / 35 | 0% | not returned | `fresno-county-appliance-pickup/` (15); `fresno-appliance-pickup/` (7) | none |
| stove pickup fresno | `fresno-stove-oven-pickup/` | 0 / 59 | 0% | not returned | `fresno-county-appliance-pickup/` (25); `clovis-appliance-pickup/` (14) | none |
| free stove pickup fresno | `fresno-stove-oven-pickup/` | 12 / 32 | 38% | 38.8 | `fresno-county-appliance-pickup/` (11); `fresno-freezer-pickup/` (5) | none |
| free freezer pickup fresno | `fresno-freezer-pickup/` | 14 / 59 | 24% | 43 | `fresno-county-appliance-pickup/` (22); `sanger-appliance-pickup/` (9) | none |
| free refrigerator pickup fresno | `fresno-refrigerator-pickup/` | 5 / 27 | 19% | 36.4 | `fresno-county-appliance-pickup/` (12); `fresno-freezer-pickup/` (6) | none |
| free appliance pickup fresno | `fresno-appliance-pickup/` | 0 / 37 | 0% | not returned | `fresno-county-appliance-pickup/` (7); `fresno-freezer-pickup/` (7) | none |
| free appliance pickup whittier | `whittier-appliance-pickup/` | 13 / 22 | 59% | 25.2 | `whittier-washer-dryer-pickup/` (6); `pico-rivera-appliance-pickup/` (3) | none |
| free appliance pickup el monte | `el-monte-appliance-pickup/` | 9 / 20 | 45% | 25.2 | `south-el-monte-appliance-pickup/` (7); `san-gabriel-valley-appliance-pickup/` (3) | none |

## High-priority verified observations

1. **Upland general:** zero intended general-page impressions for `free appliance pickup upland` in this 60-page-impression slice; 15 were assigned to the Upland washer/dryer page and 12 to the San Bernardino County page. Do not equate this with deindexation; compare Google-selected canonical and indexability through authorized URL Inspection before any ownership action.
2. **Rancho Cucamonga general:** 7 of 37 page impressions for `free appliance pickup rancho cucamonga` were attributed to its general page; the Rancho refrigerator and Southern California refrigerator pages each appeared with 8. Strong targeted ownership/intent review candidate, but low volume means no inferred causal ranking mechanism.
3. **Fontana general:** 11 of 44 page impressions for `free appliance pickup fontana` landed on its owner; the Fontana stove page and Southern California general page also appeared. Preserve legitimate Fontana stove search traffic.
4. **Fresno laundry:** `washer dryer pickup fresno` had 76 page impressions and **zero** recorded on `fresno-washer-dryer-pickup/`; Clovis general, Sanger laundry and Fresno County general pages dominate. `free washer and dryer pickup fresno` likewise had no owner row (35 page impressions). **Fresno County** has its own experiment protected until October 17; do not make broad Fresno copy/canonical changes before the latest effective gate.
5. **Claremont:** 18/26 impressions of the general `free appliance pickup claremont` term landed on laundry, versus 8 on general. Contrast with **Montclair**, where 24/24 of the same-form exact-city general query impressions landed on its correct city owner: do not assume every city needs changes.
6. **Rowland Heights:** correct general owner has 21 of 55 impressions for `free appliance pickup rowland heights` with its owner average position about 8.0; avoid changing a page already appearing on page one for some impressions merely because siblings also appear.

## Aggregate page context (not the same grouping as exact queries)

| Google-selected landing page | Impressions | Clicks | Average position |
|---|---:|---:|---:|
| `fresno-county-appliance-pickup/` | 188 | 0 | 21.5 |
| `salem-appliance-pickup/` | 90 | 2 | 9.0 |
| `rancho-cucamonga-appliance-pickup/` | 70 | 2 | 15.5 |
| `fresno-appliance-pickup/` | 36 | 1 | 27.9 |
| `fontana-appliance-pickup/` | 35 | 0 | 12.6 |
| `rowland-heights-appliance-pickup/` | 28 | 1 | 6.8 |
| `aurora-appliance-pickup/` | 9 | 0 | 13.6 |
| `denver-appliance-pickup/` | 6 | 0 | 40.3 |
| `portland-appliance-pickup/` | 6 | 0 | 21.3 |

## Prioritized next actions (no ranking edits in this checkpoint)

1. Compare exact query×page×device slices for Upland, Rancho, Fontana, Claremont and Fresno. Verify current source indexability and canonical owner. Use Google URL Inspection for Google-selected canonical/indexing only when access is granted; never infer from an absent GSC query row.
2. **Do not touch:** Fresno County owner until at least its `2026-10-17` effective evaluation gate, or any page with a later overlapping running experiment. Consider all `pagesChanged`, `protectedOwner`, `protectedOwners`, sibling and dependency pages before a proposed code change. Preserve issue #194 as deferred.
3. Review user-visible SEO jargon and repetitive content only **after** the gates and settled trend evidence; use distinct local operational facts and credible coverage rather than keyword variants, fake proof or doorway page expansion.
4. Operational coverage: `data/market-routing.json` currently records California priority markets as `partner-recruiting`; this is not proof pickups cannot occur, but actual partner capacity must be verified before promising pickup or scaling independent indexed city pages.
5. Free backlink outreach remains tracked in issue #311 (draft ≠ sent or acquired). Focus real local editorial sources; track published URL and approval, not claimed backlink wins.
6. Keep observing qualified form completions, calls and confirmed pickups, which Search Console impressions alone cannot measure. No claim of ranking improvement is made here.

## Sitemaps and limitations

- Current repository `sitemap.xml` (Oct 16) contains 704 `<loc>` entries. Windsor.ai last-known Google Search Console sitemap record, downloaded Oct 13, lists 699 submitted, 0 reported errors and 0 warnings. These are different as-of dates: the discrepancy **does not establish** a current sitemap fault.
- This report is read-only analytics. GSC Wizard trial is inactive, while Windsor.ai searchconsole is connected for free-first performance analysis. Google-selected canonical, Manual Actions report and current complete Page Indexing totals remain unverified.

Related tracking: [issue #278](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/issues/278) (sitewide SEO root cause), [issue #297](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/issues/297) (High Desert), [issue #311](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/issues/311) (free authority links).
