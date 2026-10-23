# Verified Gold Model (VGM) organic-search checkpoint — 2026-10-22

**Scope:** Free Reliable Appliance Pickup, `sc-domain:freereliableappliancepickup.com`, customer-facing city/service pages. This is an evidence snapshot and decision gate, **not** an SEO page rewrite, a Google URL Inspection result, a new ranking experiment, or a qualified-lead report.

## Sources and comparability

1. Connected Google Search Console SEO & Content Planner page insights and opportunities retrieved October 22, 2026; the plan allows only **October 18–20, 2026** (three *finalized* days), all devices together. No prior-period comparison and no query × device export in this tool's current free tier. Google may suppress low-volume queries.
2. Previously preserved [28-day first-party GSC baseline](../data/gsc-city-ownership-review-2026-10-10.md) covers September 11–October 8, 2026: **2,977 impressions, 45 clicks, 1.51% CTR, sitewide average position 18.66**. Do not compare these differently sized periods as trend or growth.
3. Connected GitHub `main` inspected at commit `65a35a3697932ea2ccdd09faf79b2c0962087791`. Selected public pages were also fetched on October 22. Repository HTML and a live response establish accessibility/content, not whether Google indexed a given URL.
4. GSC Wizard trial and Keyword.com SERP subscription refused data requests as subscription-expired; Ahrefs project request refused as insufficient plan. Do **not** treat expired plugins as a failure of the free, official Google Search Console account.
5. Search results for competitor pages found public content, but no reproducible rank positions using the same exact city/query, device, search location, and date. Therefore competitor positions are **not measured** in this checkpoint.

## Recent page-level Google organic observations

Page-level figures mix **all search queries** for that page. The displayed average position **is not** the live rank for any one exact-city query. A dash below means **no returned GSC row** during this three-day sample; it does not mean deindexed or permanent zero visibility.

| Existing page path | Clicks | Impressions | Average position | Decision |
| --- | ---: | ---: | ---: | --- |
| `/rancho-cucamonga-appliance-pickup/` | 1 | 37 | 15.51 | Protect current intent experiment; collect exact-query/device history |
| `/corona-appliance-pickup/` | 0 | 9 | 12.56 | Query `appliance removal corona`: 7 impressions, avg pos 13.29; review intent, not speculative copy |
| `/portland-appliance-pickup/` | 0 | 14 | 5.71 | Page-level zero clicks too small to establish a low-CTR defect |
| `/salem-appliance-pickup/` | 0 | 9 | 8.44 | Review exact Salem queries in longer window |
| `/vancouver-appliance-pickup/` | 0 | 2 | 2.00 | Extremely small, query unspecified; no rank claim |
| `/phoenix-appliance-pickup/` | 0 | 8 | 27.63 | Query `free appliance removal phoenix`: 3 impressions, avg pos 11; overall page mixes very weak and stronger phrases |
| `/san-dimas-appliance-pickup/` | 0 | 1 | 11.00 | Inconclusive |
| `/los-angeles-appliance-pickup/` | 0 | 1 | 5.00 | Inconclusive |
| `/stockton-appliance-pickup/` | 0 | 2 | 5.50 | Inconclusive |
| `/anaheim-appliance-pickup/` | 1 | 2 | 1.00 | Two impressions only, do not call this stable rank #1 |
| `/service-areas/` | 0 | 15 | 3.73 | Mixed queries not returned; insufficient evidence for another title rewrite |
| `/upland-appliance-pickup/` | — | — | — | No returned page row |
| `/claremont-appliance-pickup/` | — | — | — | No returned page row |
| `/la-verne-appliance-pickup/` | — | — | — | No returned page row |
| `/pomona-appliance-pickup/` | — | — | — | No returned page row |
| `/fontana-appliance-pickup/` | — | — | — | No returned page row |
| `/denver-appliance-pickup/` | — | — | — | No returned page row |
| `/aurora-appliance-pickup/` | — | — | — | No returned page row |
| `/columbus-appliance-pickup/` | — | — | — | No returned page row |
| `/fresno-appliance-pickup/` | — | — | — | No returned page row |
| `/sacramento-appliance-pickup/` | — | — | — | No returned page row |
| `/orange-county-appliance-pickup/` | — | — | — | No returned page row |
| `/pasadena-appliance-pickup/` | — | — | — | No returned page row |

The page insights on `/rancho-cucamonga-appliance-pickup/` also returned `free appliance pickup rancho cucamonga` at **2 impressions, 0 clicks, avg position 12.00**—different from the page's overall 15.51. Low-volume search positions are unstable. The earlier 28-day GSC baseline independently identified more significant exact-city page-ownership problems for **Fontana, Upland, Rancho, Pasadena, and Fresno**; review those before authoring another experiment.

## Existing indexing architecture and operational truth

- Main `sitemap.xml` currently lists **713 distinct URLs** in GitHub; the checked repository tree has **840 directory `index.html` files**, of which 128 do not occur in the *main* sitemap. This is **not** a count of unindexed pages: alternate sitemaps exist and many directory URLs intentionally have `noindex`. The existing approved-sitemap validation is the authoritative inventory test.
- `/seattle-appliance-pickup/` and `/tacoma-appliance-pickup/` currently specify `noindex, follow`; `/spokane-appliance-pickup/` specifies `noindex, follow` and canonicalizes to `/service-areas/`. This explains why simply adding these URLs to a sitemap would not make them indexable. Before any index-status/market-claim change, verify current approved partner operations, service quality, unique local usefulness, URL-level impact, and owner approval.
- `/vancouver-appliance-pickup/` is currently indexable, self-canonical and in the main sitemap. `data/market-routing.json` nevertheless records Vancouver as `partner-recruiting`, whereas the public page refers to a supported local partner. **Existing issue #378 already tracks this mismatch.** Do not create a duplicate ticket, claim dispatch has been tested, or alter coverage status without reconciliation.
- `/corona-appliance-pickup/`, `/rancho-cucamonga-appliance-pickup/`, `/salem-appliance-pickup/`, `/portland-appliance-pickup/`, `/phoenix-appliance-pickup/`, and `/denver-appliance-pickup/` have inspected self-canonical HTML, qualifying call/form CTAs, and no `noindex` instruction in the source. This does not establish Google-selected canonical or indexing.

## Competitor context (not measured ranks)

- Corona: [909 Junk Removal — appliance removal Corona](https://909junkremoval.com/services/appliance-removal-corona) shows a paid, quoted hauling offer; the site's qualification-based *free* reuse service is distinct. We should not imitate same-day, insurance or price claims without first-party proof.
- Portland: [AppliancePickupNow Portland](https://appliancepickupnow.com/portland/) shows a brief partner-matching three-step request flow and broader appliance examples; compare ease of request and documented coverage, not word counts alone.
- Phoenix: [AppliancePickupNow Phoenix](https://appliancepickupnow.com/phoenix/) offers an alternative partner-matching flow; the [City of Phoenix appliance recycling page](https://www.phoenix.gov/administration/departments/publicworks/residential-trash-recycling/residential-recycling/appliance-recycling.html) is a municipal alternative, **not** necessarily an organic pickup competitor.

## Decision gate / work queue

1. **No speculative page rewrite from three days of data.** Preserve the existing `data/seo-experiments.json` periods; page changes, merges, deployment, indexing, rankings and leads are distinct states.
2. **Highest-value original-owner diagnostic:** Rancho Cucamonga → Upland → Claremont → La Verne → San Dimas → Pomona → Fontana, then other supported California cities. Revisit `data/gsc-query-device-ownership-snapshot-2026-10-16.csv` and retrieve fresh **28–90 finalized days** of exact query × page × device history in the official free GSC account.
3. **Active operating markets:** Portland → Salem → Vancouver WA → Denver/Aurora and other verified partner markets. Confirm page ownership, mobile call/text and form *receipt* (not merely DOM presence), real image, local customer value and actual operational capacity. Do not unlock Seattle/Tacoma/Spokane indexing solely to boost URL count.
4. For each exact market query, record competitor **organic** URL/rank only from a repeatable location- and device-controlled capture, separately from Map Pack, images, paid, AI and GSC impression-weighted average positions.
5. One change per proven defect or well-evidenced experiment, branch/PR and relevant tests, then independent public verification. Revisit after at least 7–14 days of **finalized** observations and record qualified organic forms/calls where attributable.

**Status on 2026-10-22:** Data and repository reviewed; **no customer-page content, title, meta, canonical, robots, phone, image, service eligibility, or sitemap change is authorized by these sparse observations**. This checkpoint is documentation only. Organic improvement and lead impact remain **unverified**.
