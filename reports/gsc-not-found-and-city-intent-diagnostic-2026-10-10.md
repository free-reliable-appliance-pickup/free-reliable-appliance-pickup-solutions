# Why so many tracked keywords show “not found” — verified GSC diagnostic (2026-10-10)

**Owner:** Free Reliable Appliance Pickup • **Sources:** Google's Search Console property `sc-domain:freereliableappliancepickup.com`, source range **September 11–October 8, 2026**; connected Keyword.com project **3846568**, snapshot **October 10, 2026**.

## Executive decision: do not equate “not found” with “not indexed”

- Keyword.com has **100 keyword records**; **59** had rank=0 (“not found”) in the checked location/device SERP snapshot. Of those, **52** separately show **positive GSC impressions** from the tracker’s connected Google Search Console integration. Different dates/search surfaces mean this is not a contradiction: rank=0 is not a deindexing diagnosis.
- **38 distinct recorded ranking URLs** were verified in GitHub main: all 38 have a self-referencing canonical, none has a `noindex` directive, and all 38 occur in `sitemap.xml`.
- `robots.txt` contains `User-agent: *`, `Allow: /` and the sitemap reference. These checks verify *code configuration*, not Google's final per-URL index-coverage decision. No bulk reindex, deleting/suppressing city pages, or changing canonical targets is justified from “not found” alone.
- A static internal-link existence check on 15 high-priority pages found no broken **local href target paths** in that sample; it does not test URLs outside the sample or guarantee Google's crawl/index eligibility.

## Actual Google Search Console page data

**Important:** Page positions average *all queries surfaced for that URL*. The last two columns represent only the specifically matched **“free appliance pickup [city]”** query where that query appeared in the page's GSC breakdown. Do not claim the average page position equals the exact keyword's rank. Source request: `get_gsc_page_insights`; data through 2026-10-08.

| Page | Impressions (all queries) | Clicks | Average page position | Exact-city query impressions | Exact-city query average position |
|---|---:|---:|---:|---:|---:|
| Rancho Cucamonga | 67 | 2 | 17 | 3 | 28.7 |
| Ontario | 31 | 0 | 9.9 | 2 | 31 |
| Upland (general) | no data | no data | no data | no data | no data |
| Upland (laundry) | 39 | 0 | 8.5 | 14 | 10.9 |
| Claremont | 15 | 1 | 10.3 | 3 | 20 |
| Pomona | 22 | 0 | 11.7 | 9 | 18.4 |
| Fontana | 31 | 0 | 11.5 | 7 | 21.6 |
| Montclair | 28 | 0 | 6.9 | 12 | 8.5 |
| San Dimas | 16 | 0 | 6.9 | 5 | 13.8 |
| Fresno (general) | 29 | 0 | 25.9 | no data | no data |
| Clovis | 99 | 0 | 7.8 | no data | no data |
| Sanger | 82 | 0 | 10.7 | no data | no data |
| Pasadena | 27 | 0 | 12.3 | 9 | 26.2 |
| Covina | 21 | 0 | 12.9 | 8 | 22.9 |
| La Verne | 7 | 0 | 5.6 | no data | no data |
| West Covina | 5 | 0 | 6.2 | no data | no data |
| San Marino | 11 | 0 | 5.8 | no data | no data |
| Sierra Madre | 6 | 0 | 4.5 | no data | no data |
| Temple City | 1 | 0 | 3 | no data | no data |

Upland general appliance owner had **no page performance record** in this GSC date-range response; this does **not** establish deindexing. The Upland washer/dryer page received 39 impressions and 14 were from the broader “free appliance pickup upland” query, indicating misaligned page targeting.

## Confirmed competing URL appearances on identical exact-city queries

Google Search Console's opportunity service identifies multiple *distinct URLs* receiving impressions for the same query, a warning of possible organic intent ambiguity. It is **not** proof of an algorithmic penalty or that all listed URLs concurrently rank on one SERP.

### “free appliance pickup upland” — 11 URLs, 53 total reported page-query impressions

| URL owner | Impressions | Average query position |
|---|---:|---:|
| Upland washer/dryer | 14 | 10.93 |
| San Bernardino County general | 12 | 11.25 |
| San Bernardino city general | 6 | 13.83 |
| Highland general | 4 | 36 |
| Hermosa Beach general | 3 | 45.67 |
| La Mesa general | 3 | 48.67 |
| Pico Rivera general | 3 | 44.33 |
| San Gabriel–Inland Empire regional | 3 | 11.33 |
| Southern California regional | 3 | 41.67 |
| Hawaiian Gardens general | 1 | 44 |
| Rancho Cucamonga general | 1 | 35 |

**Preferred owner** once verified: `/upland-appliance-pickup/` for general appliance-intent, with `/upland-washer-dryer-pickup/` kept for laundry-specific requests.

### “free appliance pickup fontana” — 6 URLs, 40 total reported page-query impressions

| URL owner | Impressions | Average query position |
|---|---:|---:|
| Fontana stove/oven | 13 | 18.69 |
| Southern California general | 11 | 6.18 |
| Fontana general | 7 | 21.57 |
| Rialto washer/dryer | 5 | 5.60 |
| Southern California refrigerator | 3 | 24.67 |
| Homepage | 1 | 8.00 |

**Preferred owner:** `/fontana-appliance-pickup/` for general appliance pickup; `/fontana-stove-oven-pickup/` for stove/range/oven service intent.

### “free dryer pickup fresno” — 9 URLs, 41 total page-query impressions

Sanger general 9, Clovis general 7, Visalia general 6, Fowler laundry 5, Fresno County general 5, Sanger laundry 4, Fresno refrigerator 2, Selma general 2, Selma laundry 1. Neither a distant neighboring city nor a refrigerator page should be deliberately optimized to replace the proper Fresno laundry service owner.

## Exact fix order, without violating protected experiment baselines

1. **Do now:** preserve valid sitemap, index/canonical/robots declarations; fix only verified hard errors (broken links, wrong city routing, false form defaults, 404, facts). These do not improve rankings instantly.
2. **Before editing:** check `data/seo-experiments.json` for `evaluateNotBefore`. The high-value Upland, Fontana, Fresno and wider California owner pages are in active SEO experiments around October 14–16. Prematurely resetting a changed title/body/anchor may prevent measuring whether earlier experiments worked.
3. **On observation gate:** collect finalized GSC query->page and Keyword.com city/device snapshots, then choose **one clear owner per query**, reduce generic-city language/links on inappropriate category or neighboring-city pages, and sharpen the category-specific pages to their actual intent. Test bounded changes, record before/after.
4. **Keep true local utility:** accurate photos, appliance condition/testing, 80% working multi-load rule, actual routing, municipal alternatives, accessibility/stairs and partner expectations. No keyword stuffing, paid backlinks, blind noindex, fake GBPs or doorway pages.
5. **Track business outcome:** lead forms completed, valid pickup requests, confirmed pickups and call taps per service area. A rank increase without qualified leads is not success.

## What is not yet proved

We did not have GSC per-URL indexing verdicts or verified all mobile/desktop SERPs. GSC data through Oct 8 cannot confirm that code changes on Oct 9–10 improved or worsened ranks. A week of daily tracking plus GSC data is needed; do not promise #1 or report “all fixed” from successful site deployments alone.

See also `reports/keyword-com-corridor-baseline-2026-10-10.md`; read the preceding report's “not found” cells as tracker rank not found, **not as broken pages**.
