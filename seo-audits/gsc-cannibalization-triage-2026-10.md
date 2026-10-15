# Search Console cannibalization triage — October 2026

Source: Windsor.ai connected Google Search Console property sc-domain:freereliableappliancepickup.com; September 11–October 11, 2026. Query+page export returned 766 rows. Counts below are URLs with impressions for a query, **not** confirmed duplicate-content or cannibalization penalties. Small sample sizes make positions volatile.

## Provisional owner URLs — do not redirect without deeper review

| Intent | Preferred owner | Other observed URLs | Action |
| --- | --- | --- | --- |
| free appliance pickup Rancho Cucamonga | /rancho-cucamonga-appliance-pickup/ | refrigerator, freezer, San Bernardino, Southern California and other regional pages (11 URLs total) | Strengthen city-specific contextual links and separate refrigerator/freezer intent |
| free appliance pickup Fontana | /fontana-appliance-pickup/ | homepage, stove, Rialto W&D, Southern California pages (6 URLs) | Link to city owner from regional pages; keep stove page focused on stoves |
| free appliance pickup Fresno | /fresno-appliance-pickup/ | Clovis, Fowler, Fresno County, freezer, refrigerator, Sanger, Selma, Visalia, recycling (9 URLs) | Reinforce Fresno owner; inspect Fresno County vs city intent before any consolidation |
| free appliance pickup Upland | /upland-appliance-pickup/ | Upland W&D and other city/regional pages (13 URLs) | Ensure general pickup links go to owner; W&D page targets laundry intent |
| free appliance pickup Claremont | /claremont-appliance-pickup/ | /claremont-washer-dryer-pickup/ (2 URLs) | General vs laundry differentiation |

## Verified repository checks

- /fresno-appliance-pickup/ has self-referencing canonical and city-specific H1; 14 matching appliance-pickup links in raw HTML.
- /upland-appliance-pickup/ has self-referencing canonical and city-specific H1; 15 matching appliance-pickup links.
- /claremont-washer-dryer-pickup/ has self-referencing canonical and laundry-specific H1; 12 matching appliance-pickup links.
- /southern-california-appliance-pickup/ has self-referencing canonical and about 90 matching appliance-pickup links. Review link relevance and navigation layout; raw counts alone do not establish a problem.
- Rancho Cucamonga, Fontana, and Denver general pickup pages have self-referencing canonicals and city-specific metadata.

## Safe implementation order

1. Freeze mass-generated city pages pending content-quality review; do not disable existing routes.
2. Inventory sitemap URLs, titles, H1, canonical, robots/indexability and inbound internal links.
3. For each priority query, compare page-level impressions, clicks, positions and intent, then pick one general-city owner.
4. Adjust *contextual links* and anchor text from regional and service pages to relevant owner pages without removing useful navigation.
5. Differentiate service-specific pages by actual service and locally verified facts; never invent route days, reviews, ZIP coverage or pickup guarantees.
6. Test links, forms, canonicals and mobile rendering before merging.
7. Compare subsequent 28-day GSC periods; no 301 redirect without evidence of redundancy, replacement fit, and backlink/traffic review.

## Important limitations

Search Console shows impressions, not proof of indexation of every sitemap URL. Zero rows in this export do not prove a URL is unindexed. Ranking averages are not live SERP ranks. No redirect, deletion, canonical change or claimed Google ranking improvement is authorized by this report.
