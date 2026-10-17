# First-party query-to-landing-page checkpoint — Oct 17, 2026 UTC

## Provenance and limitations
- Verified site property: `sc-domain:freereliableappliancepickup.com`.
- Tool: connected Google Search Console SEO & Content Planner (SMEPost) read-only opportunities, requested Oct 17 UTC.
- **Finalized report window: Oct 12–14, 2026, three days only.** Free account now exposes a rolling three-day finalized report without comparative period.
- GSC Wizard read access was unavailable because its trial ended. Do not claim GSC URL Inspection / Page Indexing / Manual Actions were checked through that tool.
- The values below are Search Console impression-weighted *average positions*. They are **not fixed local rank**, live phone calls, leads, proof of indexation of other URLs or proof of Google's cause for choosing a given page.
- Opportunity aggregation and related-page subrows come from distinct report views and may not be perfectly additive. Do **not** sum their impressions as a sitewide traffic measure.

## Query evidence

| Query | Three-day impressions | Average position | Clicks | Landing-page ownership observation |
| --- | ---: | ---: | ---: | --- |
| free appliance pickup rowland heights | 19 | 11.37 | 0 | Intended `/rowland-heights-appliance-pickup/` is visible; related-page breakdown reports intended page 14 impressions at avg pos 9, Hacienda Heights 4 / pos 16.25, Los Angeles County 2 / pos 22 and Service Areas 1 / pos 12. |
| free appliance pickup arcadia | 15 | 13.33 | 0 | Wrong service-type page is dominant: `/arcadia-refrigerator-pickup/` 11 impressions / pos 9.09; intended `/arcadia-appliance-pickup/` 2 / pos 24.5; homepage 1 / pos 43; Los Angeles County 1 / pos 8. |
| free appliance pickup azusa | 12 | 12.33 | 0 | Intended `/azusa-appliance-pickup/` reported as a striking-distance candidate; preserve existing SGV snippet experiment until review. |

## Page-level opportunity observations (not query-specific)

| Page | Impressions | Clicks | Average position |
| --- | ---: | ---: | ---: |
| `/fresno-county-appliance-pickup/` | 39 | 0 | 21.49 |
| `/phoenix-appliance-pickup/` | 20 | 0 | 23.60 |
| `/appliance-recycling/` | 21 | 0 | 44.43 |

These three-day page aggregates alone do not justify changing titles or redirecting indexable pages. A zero-click result in a three-day small sample is not evidence of a broken conversion funnel.

## Repository cross-check
- `arcadia-refrigerator-pickup/index.html` is a refrigerator-specific, indexable, self-canonical page, and already links to the main Arcadia general-service page multiple times; **do not add redundant links or suppress this specialty URL blindly**.
- `arcadia-appliance-pickup/index.html` is indexable and self-canonical; its current title/H1 identify general appliance pickup.
- `rowland-heights-appliance-pickup/index.html` is indexable, self-canonical and already links to Hacienda Heights and its own specific appliance guides; observed overlap is not proof of a canonical mistake.
- `data/seo-experiments.json` includes running Arcadia, Azusa, Hacienda Heights and Rowland Heights tests with preferred review around Oct 20, 2026. Preserve those tests while documenting the new source signals.

## Next evidence-first actions
1. At/after the experiment review window, compare finalized GSC query × landing page × device data over a longer period for Arcadia, Rowland Heights and Azusa. Preserve specialty pages that are already receiving impressions or clicks.
2. Prioritize **Arcadia query ownership** if the wrong-service URL remains dominant: test one narrowly scoped, reversible change at a time. First check title/H1/anchors actually present; avoid mass canonical, noindex, redirect and city-keyword insertions.
3. Obtain authoritative GSC URL Inspection for Rancho Cucamonga, Upland, Fontana, Arcadia and Salem when a permitted connected tool is available. Absence in a report is *not* proof of not being indexed.
4. Do not change phone coverage or make pickup promises for partner-recruiting Washington/California markets without confirmed operating capacity.
5. Keep the new city×service page freeze and review the next finalized dataset before launching any scaled SEO copy changes.

## Separate technical-image maintenance (same work session)
- `olympia-appliance-pickup/index.html`: added visually inspected existing garage multi-appliance photo; preserved `noindex`, local-partner notice, form and canonical. Commit `4096b2e5203c4eee4589f578e7e8e7d3935bd131`.
- `everett-appliance-pickup/index.html`: added a different visually inspected existing multi-appliance photo; preserved `noindex`, local-partner notice, form and canonical. Commit `4a6e280a6cd615de2954823b28602d61342e16eb`.
- Images are representative appliance examples, **not** photographs of completed jobs in these Washington cities.
