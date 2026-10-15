# Finalized Google Search Console city-intent baseline — October 15, 2026

## Source, period and limits
- Source: **direct connected Google Search Console via Windsor.ai**, authorized `searchconsole` account `sc-domain:freereliableappliancepickup.com` (read-only).
- Pulled October 15, 2026, with `include_fresh_data=false`. Exact-city query/page/device comparison: **September 25–October 12, 2026**. Sitewide daily comparison: **September 11–October 12, 2026**.
- The performance API returns query/page impressions and Google's **average position across those impressions**. It does not establish present-day, location-independent SERP rank; rows are withheld/aggregated for low-volume searches. Different pages in the same query report are **not** proven to have appeared simultaneously.
- No `URL Inspection` / Google-selected canonical / Manual Actions API finding was obtained. Missing rows do not prove deindexing.
- **All website/photo changes committed October 15 occurred *after* this finalized-data window. Do not attribute any change in these numbers to those commits.**

## Sitewide organic visibility by period

| Window | Days | Impressions | Clicks | CTR | Avg position (impression-weighted) |
|---|---:|---:|---:|---:|---:|
| Sep 11–17 | 7 | 169 | 7 | 4.14% | 24.88 |
| Sep 18–24 | 7 | 526 | 4 | 0.76% | 22.29 |
| Sep 25–Oct 1 | 7 | 752 | 22 | 2.93% | 17.38 |
| Oct 2–8 | 7 | 1,530 | 12 | 0.78% | 17.36 |
| Oct 9–12 | 4 | 678 | 7 | 1.03% | 19.78 |
| **Total Sep 11–Oct 12** | **32** | **3,655** | **52** | **1.42%** | — |

Impressions grew markedly, but the Oct 2–8 click-through rate was weak. The Oct 9–12 entry is only four days; do not compare its raw totals as though it were a full week.

## Verified exact-query / actual URL ownership

Source: Windsor.ai GSC Search Analytics, filtered on the city name in `query`, grouped by `query` and `page` and weighted by reported impressions (2026-09-25 through 2026-10-12).

### `free appliance pickup upland`

| Google-selected impression recipient | Impressions | Clicks | Avg position |
|---|---:|---:|---:|
| `/upland-washer-dryer-pickup/` | 15 | 0 | 12.40 |
| `/san-bernardino-county-appliance-pickup/` | 12 | 0 | 11.25 |
| `/highland-appliance-pickup/` | 8 | 0 | 37.88 |
| `/san-bernardino-appliance-pickup/` | 6 | 0 | 13.83 |
| **`/upland-appliance-pickup/` intended broad owner** | **No returned row** | — | — |

The general Upland city page exists, is internally linked from the county/regional hub, and has a self-canonical. Do not interpret absence of its exact-query GSC row as a noindex result. Its general-page hero/preview was corrected on Oct 15 (commit `a2dba93a71ad215d15128cbbbc6e0fda369c6815`); this is *not* yet a ranking fix proven by GSC.

### `free appliance pickup fontana`

| Google-selected impression recipient | Impressions | Clicks | Avg position |
|---|---:|---:|---:|
| `/fontana-stove-oven-pickup/` | 13 | 0 | 18.69 |
| `/fontana-appliance-pickup/` intended broad owner | 11 | 0 | 21.64 |
| `/southern-california-appliance-pickup/` | 11 | 0 | 6.18 |
| `/rialto-washer-dryer-pickup/` | 5 | 0 | 5.60 |

The **Oct 6–12** subset returned five impressions for Fontana general at avg position 21.80, and none for Fontana stove or Southern California general in the filtered exact-query rows. Treat this as a small, *potentially favorable owner-matching signal*, not proof of lasting improvement. Protect existing stove/laundry pages from blanket redirects or noindex.

The Fontana general page already has a five-appliance garage hero; its Open Graph, Twitter and primaryImageOfPage schema were aligned on Oct 15 (commit `072aa1136192860b7d44e5555511f684346bf0b0`). This affects metadata accuracy, not Google ranks already finalized.

### `free appliance pickup rancho cucamonga`

| Google-selected impression recipient | Impressions | Clicks | Avg position |
|---|---:|---:|---:|
| `/rancho-cucamonga-refrigerator-pickup/` | 8 | 0 | 35.13 |
| `/southern-california-refrigerator-pickup/` | 8 | 0 | 14.88 |
| `/rancho-cucamonga-appliance-pickup/` intended broad owner | 7 | 0 | 28.00 |
| `/san-bernardino-appliance-pickup/` | 5 | 0 | 4.80 |

The **Oct 6–12** subset returned six impressions for the intended Rancho general owner at position 28.83 on average, so it is being surfaced for the exact city query but is far from a top-three claim. Its authentic truck-liftgate pickup photo was inspected and preserved.

## Technical verification

- The priority URLs inspected in `main` have index/follow source directives, self-canonicals and Formspree intake. This does **not** replace Google URL Inspection.
- The San Bernardino County hub, San Bernardino city page, and Southern California hub already contain links to `/upland-appliance-pickup/`, `/rancho-cucamonga-appliance-pickup/`, and `/fontana-appliance-pickup/`. Blindly adding another round of these links is not justified.
- Highland's local page had no literal `Upland` mention or Upland link in its inspected source despite showing in GSC for the Upland query. Therefore no factual basis to 'remove Upland keywords' from Highland.
- GSC Sitemaps connector returned `sitemap.xml`: **699 submitted URLs** as last downloaded **Oct 13, 2026 19:32 UTC**, **0 warnings, 0 errors**. The deprecated `indexed` field returned 0; **do not interpret it as zero indexed URLs**. Site changes after that download may not yet be reflected.

## Controlled actions and measurement gates

1. **Do not create more city pages** as a remedy for these three exact phrases. Do not delete working specialty/neighbor pages based on these low-volume overlapping query rows.
2. **Upland:** preserve city-general vs washer/dryer-specific intent; measure post-Oct-15 finalized GSC exact-query owner split by mobile and desktop after enough search impressions accumulate. Avoid further title/H1/canonical rewrites without clearer evidence.
3. **Fontana:** allow the recent owner-matching signal to develop; protect the main city page, legitimate stove clicks, phone and local request form.
4. **Rancho Cucamonga:** prioritize legitimate local citations/reuse listings and service trust, and measure whether the main city owner grows from its weak 7-impression / avg-pos-28 exact query baseline. Preserve real pickup image.
5. Track **qualified phone requests, completed forms and confirmed pickups**, not just ranking positions.
6. Retain comparison methods (`query`, `page`, `device`, `clicks`, `impressions`, `position`) and finalized date windows; rerun after changes are old enough to appear in finalized GSC.

The goal is genuine local intent ownership with reliable customer conversion, not maximal page or keyword counts.
