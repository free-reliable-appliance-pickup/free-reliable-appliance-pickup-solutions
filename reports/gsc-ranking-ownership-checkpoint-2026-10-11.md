# California Gold Standard — finalized GSC query ownership checkpoint
**Retrieved:** October 11, 2026 (America/Mazatlan). **Finalized data:** October 7–9, 2026 (three days only). **Property:** `sc-domain:freereliableappliancepickup.com` (verified siteOwner through connected Google Search Console SEO & Content Planner).

**Purpose:** Establish a ranking/CTR/landing-page baseline without changing SEO test variables. This is an operational observation, not proof of ranking progress. Free account access is `free_recent_three_days`, without prior-period comparisons; query and page insight endpoints may return different subsets. Source: GSC `get_gsc_opportunities` (minImpressions=1, all devices / MOBILE / DESKTOP) and `get_gsc_page_insights` (named pages). Google explanation: https://support.google.com/webmasters/answer/7042828 — average position is not a fixed local SERP rank.

## Exact observations — all devices
| Source type and target | Clicks | Impressions | Avg position | Interpretation |
|---|---:|---:|---:|---|
| Query opportunity: `free appliance pickup rowland heights` | 0 | 20 | 12.80 | Promising near-page-one exact-city query; do not claim live position #13 |
| Page insight: `/rowland-heights-appliance-pickup/` | 0 | 9 | 8.56 | Different endpoint/grouping and returned rows; **do not add it to or equate with the query row** |
| Page insight: `/fresno-county-appliance-pickup/` | 0 | 119 | 23.03 | Major low-CTR / mixed-service landing page with protection through Oct 17 |
| Page insight: `/fresno-stove-oven-pickup/` | 0 | 9 | 39.44 | Intended exact appliance page underperforms sibling URLs |
| `free stove pickup fresno` on Fresno stove page (page insight) | 0 | 8 | 43.00 | Current intended owner is weaker than some sibling city pages |
| Page insight: `/fresno-refrigerator-pickup/` | 0 | 7 | 40.71 | Specialty URL visible, not necessarily excluded from index |
| Page insight: `/sanger-appliance-pickup/` | 0 | 20 | 8.80 | Do not sacrifice sibling city visibility |
| Page insight: `/rancho-cucamonga-appliance-pickup/` | 0 | 9 | 17.78 | Overall page; exact-city query subset differed |
| Exact query `free appliance pickup rancho cucamonga` on intended owner | 0 | 3 | 34.33 | Page insight; distinguish from overall page average |
| Page insight: `/salem-appliance-pickup/` | 1 | 10 | 7.70 | Preserve actual click and no unnecessary changes |

### Fresno — potential search-intent leakage, not proven same-SERP duplication
All-device opportunity returned `washer dryer pickup fresno` with 22 impressions, average 26.91; related **Clovis general page** 7 impressions / avg pos 4.29; **Sanger laundry** 6 / 10.67; Fresno County general 13 / 38.85. The Fresno laundry owner was not among returned rows. Preserve Clovis and Sanger until longer evidence justifies a targeted change.

For `stove pickup fresno`, all-device opportunity shows 25 impressions / average 20.68, and related Fresno County 17 / 26, Clovis general 6 / 2.17, Sanger general 6 / 7.50. This relatedPage reporting is not a list of results simultaneously shown on a single SERP.

For `free freezer pickup fresno`, opportunity shows 23 impressions / avg 23.87, Fresno County 13 / avg 16.92, dedicated Fresno freezer page 6 / avg 44.33, Sanger general 3 / avg 4.67. Do not canonicalize/deindex any sibling based on three days.

The dedicated `/fresno-washer-dryer-pickup/` returned **no page-insight row** in this window. Lack of a row does **not** demonstrate `noindex`, non-indexation, or no traffic over a longer period.

### Device-specific snapshot
- **MOBILE, Oct 7–9:** `/rancho-cucamonga-appliance-pickup/` 1 impression / avg position 23 for exact city phrase; `/fontana-appliance-pickup/` 2 / 22 for exact city phrase; `/pasadena-appliance-pickup/` 4 / 26 for exact city phrase. `/ontario-appliance-pickup/`, `/upland-appliance-pickup/`, `/victorville-appliance-pickup/` and `/hesperia-appliance-pickup/` returned no page-insight rows in this tiny mobile sample.
- **MOBILE query opportunity:** Rowland Heights exact city 14 impressions / avg position 12.21. All-device query opportunity 20 / 12.80, not a statistically meaningful comparison.
- **DESKTOP opportunity:** `washer dryer pickup fresno` 17 impressions / average 28.24; the Clovis and Sanger ranking overlap is also observable on desktop. `free washer and dryer pickup fresno` 8 / 19.75.
- The separately requested all-device Rancho page insights returned 9 total page impressions / 17.78 avg, exact city 3 / 34.33. Do not treat MOBILE position 23 as a trend relative to all-device.

## Live/source technical review (no substantive page edits)
Read current `main` sources for Rowland Heights general, Fresno County general, Fresno laundry, Fresno stove, Fresno freezer, Sanger general and Salem general. All sampled pages have one self-canonical URL in source, `robots=index,follow`, a Formspree customer intake form with explicit source, the shared routing script and their current regional 909/310/503 phone number. This checks **source HTML**, not Google-selected canonical, live lead delivery, or service capacity. Live public Rowland Heights page and Fresno laundry page were accessible in web retrieval on Oct 11; Rancho page accessible. Could not reliably retrieve Fresno County page through the web tool; the GitHub source was inspected instead. Do not infer its live HTTP status from that one retrieval failure.

## Specific ranking-first decisions and protected gates
1. **Now (Oct 11):** No SEO-title, heading, internal-link, index/noindex or canonical changes to active tests. Record the above baseline, protect Rowland Heights (exact query near page one), Salem (actual click) and Sanger/Clovis (stronger positions for Fresno-related queries). Recheck phone/form after any technical change.
2. **Oct 13–14:** Re-evaluate Pasadena after its last overlapping gate (the California anti-template experiment extends it to Oct 14); Rancho, Fontana, Ontario, Upland and Rowland Heights after Oct 14. Pull new finalized same-query, same-device results. Improve only the intended owner when enough evidence; one reversible variable at a time.
3. **Oct 14+ for Fresno specialty pages:** Carefully evaluate city/service wording on Fresno stove, freezer, refrigerator and laundry owners with longer finalized evidence. Avoid stealing impressions from genuinely useful Clovis/Sanger results through blanket redirects or mass changes.
4. **Oct 17+ for Fresno County hub:** Protected by `2026-10-07-fresno-county-winner-protection` until **2026-10-17**. Retain its working county route and impressions while evaluating whether it needs clearer human-useful city versus appliance task navigation.
5. **Oct 14–17 for Oregon/High Desert:** Preserve Salem clicks; after each page's **effective latest overlapping** test gate, review settled city+device GSC. Review High Desert Victorville/Hesperia/Adelanto (Oct 15) and Phelan/regional hub (Oct 17) separately.
6. **Indexing/coverage blockers:** GSC planner does not expose actual Page Indexing, Manual Actions, Security Issues or Google-selected canonical inspection here. Do not claim those are cleared. Independently confirm approved California operator/partner pickup capacity; current configuration marks priority CA cities partner-recruiting.
7. **Measurement of success:** qualified phone calls and Formspree leads first, then completed pickups; measure finalized GSC clicks/CTR/query owner and manual matched-location Google organic results. No promised #1 ranking.

**No claim:** a three-day GSC sample, a green CI run, and a self-canonical in source HTML do not by themselves show Google has indexed, ranked or recommended the page. No new indexable URL, fabricated review, partner, backlink or service-area promise is authorized by this checkpoint.
