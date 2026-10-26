# VGM California organic query → landing-page ownership checkpoint

Collected: **2026-10-26**. Read-only measurement; no site page, image, canonical, routing, or form edits.

## Source and methodology

- First-party **Google Search Console** data returned by the connected **Windsor.ai `searchconsole`** connector for `sc-domain:freereliableappliancepickup.com`.
- Requested period: **2026-09-25 through 2026-10-23 inclusive**, Google Web query/page/date/device rows. Exact query match (`query eq`) for each named keyword. Retrieved results are the rows the connector returned; they are **not exhaustive Search Console property totals**, local rank checks, or leads.
- Positions below are **impression-weighted means of returned rows per exact query × landing page**, not today's SERP positions. A Google impression may be attributed to multiple pages; do not sum the per-page impressions as a property-wide total. Zero clicks on sampled rows does not establish zero business leads.
- Lack of a row **does not prove no indexing**. Windsor may omit/withhold some queries or days; no live URL Inspection data in this report.

## Exact-query landing-page findings

| Exact user query | Returned landing page | Impressions | Clicks | Weighted avg position |
| --- | --- | ---: | ---: | ---: |
| free appliance pickup rancho cucamonga | /rancho-cucamonga-appliance-pickup/ | 14 | 0 | 22.57 |
| same | /san-bernardino-appliance-pickup/ | 5 | 0 | 4.80 |
| same | /southern-california-refrigerator-pickup/ | 8 | 0 | 14.88 |
| free appliance pickup upland | /upland-appliance-pickup/ | **no returned row** | — | — |
| same | /upland-washer-dryer-pickup/ | 18 | 0 | 14.89 |
| same | /san-bernardino-county-appliance-pickup/ | 12 | 0 | 11.25 |
| same | /san-bernardino-appliance-pickup/ | 6 | 0 | 13.83 |
| free appliance pickup fontana | /fontana-appliance-pickup/ | 12 | 0 | 21.08 |
| same | /fontana-stove-oven-pickup/ | 13 | 0 | 18.69 |
| same | /southern-california-appliance-pickup/ | 11 | 0 | 6.18 |
| free appliance pickup claremont | /claremont-appliance-pickup/ | 16 | 0 | 13.06 |
| same | /claremont-washer-dryer-pickup/ | 20 | 0 | 12.40 |
| free appliance pickup pasadena | /pasadena-appliance-pickup/ | 13 | 0 | 29.00 |
| same | /south-pasadena-appliance-pickup/ | 16 | 0 | 37.38 |
| free appliance pickup san dimas | /san-dimas-appliance-pickup/ | 14 | 0 | 12.71 |
| same | /san-gabriel-valley-appliance-pickup/ | 6 | 0 | 2.83 |
| free appliance pickup pomona | /pomona-appliance-pickup/ | 15 | 0 | 18.47 |
| same | /pomona-stove-oven-pickup/ | 3 | 0 | 11.33 |

**Interpretation:** Especially for Upland, there is measurable query-to-page ownership ambiguity: the general city's intended owner did not appear in the *returned exact-query rows*, while unrelated regional/specialty pages did. There is also cross-page appearance for Rancho, Fontana, Claremont, Pasadena and San Dimas. This is evidence for further investigation, **not proof** of Google cannibalization, a penalty or the reason every query ranks poorly. In particular, the reported average position for an alternate page does not imply it always displaced the main page.

## Latest independent page-level check

A second connected source, **GSC SEO & Content Planner**, owner property, **2026-10-21 to 2026-10-23** (free three-day mode; **no comparison allowed**), reports all-query page performance:

| Page | Impressions | Clicks | Avg position |
| --- | ---: | ---: | ---: |
| Rancho Cucamonga general | 46 | 0 | 15.09 |
| Claremont general | 1 | 0 | 6.00 |
| Fontana general | 1 | 0 | 1.00 |
| Los Angeles general | 4 | 0 | 9.75 |
| Upland, Ontario, Pasadena general | No page-level row returned | — | — |

For Rancho exact `free appliance pickup rancho cucamonga`, this *three-day* source returned **3 impressions / 0 clicks / average position 12** on the intended general page. This does not contradict the longer exact-query sample because periods differ.

## Proposed next action (NOT implemented by this evidence-only PR)

1. **Priority 1 Upland**: inspect its actual Google-selected canonical (Search Console URL Inspection), sitemap membership, internal incoming anchors and current ownership from service-area and regional hubs. Compare against laundry and San Bernardino County pages. Distinguish indexation vs no query exposure.
2. **Priority 2 Rancho/Fontana/Claremont**: inspect the landing-page overlap for their *exact general-pickup searches*, while preserving good specialty search intents. Avoid redirecting/deindexing a page just because it also appeared.
3. Pull a consistent, **country=USA, device=MOBILE, 28-day** export using available free first-party access and a stable after-change date before editing SEO titles, headers, canonicals or intent-bearing links.
4. Maintain the VGM **one-variable-at-a-time** discipline and existing protected experiments, including the SFV image experiment through 2026-11-06. Review `data/seo-experiments.json` before changes.
5. Check contact-form delivery and real service coverage separately; do not equate SEO impressions with qualified leads or verified local pickup capacity.
6. Link building: prioritize legitimate free, geographically relevant resource listings; only count a backlink after publication. No bought backlinks or fabricated local profiles.

## Technical context

On `main` at **3cbc7b42** (2026-10-26), GitHub Pages deployment, active page image, internal link, phone routing, pickup form and search-intent audit workflows reported **success**. Successful CI indicates the tested contracts passed, not that Google ranks the pages favorably.

Related tracking: [#453](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/issues/453), [#278](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/issues/278), [#311](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/issues/311).
