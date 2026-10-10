# Free Reliable Appliance Pickup — California SEO Gold Model
**Evidence and operating standard as of October 10, 2026.** This is an internal, non-indexed repository document, not a new consumer service page.

## Verified search baseline (do not extrapolate beyond the data)
GSC property `sc-domain:freereliableappliancepickup.com`; finalized data September 10–October 7, 2026. These are impressions/average positions, not guaranteed individual-city search-result placements.

- **Rancho Cucamonga main page:** 60 impressions, 2 clicks, 3.33% CTR, avg position 17.23 across its queries. Exact city query: 1 impression, avg position 23.
- **Fontana main page:** 30 impressions, 0 clicks, avg position 11.6 across queries; exact city query: 7 impressions, avg position 21.57.
- **Fontana stove/oven page:** 13 impressions for the *general* Fontana query (avg 18.69), indicating broad/specific page overlap.
- **Southern California region page:** 11 impressions for the general Fontana query (avg 6.18); it outranked the Fontana main page for this sample.
- **Upland main page:** No data rows returned by page insights for the period (not proof of nonindexing).
- **Upland washer/dryer page:** 14 impressions for the general Upland pickup query (avg position 10.93).
- **San Bernardino County page:** 11 impressions for the general Upland query (avg position 12.09).
- **San Bernardino city page:** 5 impressions for the general Rancho Cucamonga query (avg position 4.8).
- GSC flagged *free appliance pickup fontana* and *free appliance pickup upland* as query/page overlap opportunities. Small samples can produce cross-city matches; this is evidence to investigate, **not** a confirmed Google penalty.

Keyword.com project ID 3846568 tracked 100 desktop/mobile keywords on October 10:
- 8 Top 3, 22 Top 10, 29 Top 20, 41 Top 100; 59 outside the tracker range.
- On October 2 the project had 17 Top 3, 22 Top 10, 33 Top 20, 43 Top 100.
- Rancho Cucamonga mobile and desktop: not detected on October 10. The earlier #2 appearance on October 2 was the **San Bernardino city URL**, not the Rancho URL. Later Rancho URL appeared at positions 22–39.
- Fontana mobile: position 20 on October 10; desktop not detected. Earlier desktop #3 was the **Southern California region URL**, not the Fontana URL.

Competitor sampled: `takemyappliance.com`, matching city pages for Rancho Cucamonga, Fontana, Upland, Ontario, Montclair, Claremont, La Verne, San Dimas, Pomona, Chino, Chino Hills, and San Bernardino. Their pages generally use a shorter 3-step intake flow and leaner visible copy; length alone has no demonstrated causal SEO effect. Ubersuggest backlink snapshot: Free Reliable DA 5, 26 backlinks, 20 referring domains; TakeMyAppliance DA 7, 58 backlinks, 31 referring domains. Tool estimates are not Google's own ranking signals.

## Page ownership / intent mapping
1. One primary *general* service page per confirmed pickup city, such as `/fontana-appliance-pickup/`, `/upland-appliance-pickup/`, `/rancho-cucamonga-appliance-pickup/`. Cover washers, dryers, refrigerators, freezers, ranges/stoves/ovens, and mixed loads. Use exact city context, real pickup coverage, photos, clear lead path.
2. Narrow appliance pages (e.g., `/fontana-stove-oven-pickup/`, `/upland-washer-dryer-pickup/`) answer that category only. For general/mixed requests, link visibly and naturally to the city's main page. Keep the narrow page self-canonical if it has genuinely distinct useful service content.
3. County, corridor and Southern California hubs exist to help visitors find the correct city; they must not claim to be a local business in every city. Use a focused city directory, not repetitive SEO-only location lists.
4. The homepage helps visitors choose the correct market; do not make it pretend to be a city landing page.
5. Use natural descriptive internal anchors. Avoid "for broad searches", "search intent", "primary SEO owner", "rank", or other internal SEO instructions in customer-facing copy.
6. **Do not** canonicalize a real laundry/stove city page to the general page solely because both got impressions. A canonical/redirect is for truly duplicative pages after checking actual index state and user intent. Do not bulk-noindex or delete valuable service pages without a URL-by-URL decision.

## Gold-model city-page customer experience
- Accurate title/H1 and short, clear meta description (city + free-pickup qualification + actual response path).
- In the first viewport: what is accepted; that free pickup is *conditional*; city and service availability; prominent call/text/request options that work on mobile.
- Qualification stated once clearly: working appliances preferred, mixed loads considered when roughly 80% of major appliances work; single fully nonworking items generally not free; dishwasher only with at least two major working appliances; microwaves not accepted alone. Do not claim every request or appointment is guaranteed.
- Helpful details: specific tested functions (cooling, spin/drain, heat, burners/oven), safe disconnection, floor, stairs, gates, driveway/parking, elevator, photo sharing and exact ZIP. Avoid repeated notices.
- Legitimate local information: verified city recycling/bulky-item alternatives and correct public source link; specific access considerations without claiming fictitious local crews or offices.
- Real business or owner-supplied appliance photos, relevant to service type, with truthful captions and sensible image sizes. Never label inventory photos as a specific local pickup event unless proven.
- City-specific photos and practical customer questions rather than mass-repeated blocks of neighborhoods, cities, and keywords.
- Source-separated snippets: property-manager/recurring/commercial requests may be relevant but should not displace the residential pickup flow.
- Phone numbers and routing from the approved market map. Do not invent locations, fake GBP profiles, storefronts or unverified reviews.

## Golden mobile form specification
The initial request should require only: name, callback phone, city, ZIP, appliance type, condition (unless a narrower form pre-fills city/type). Optional first-stage inputs: street address, floor/stairs, gates, model, notes, photo link, preferred window. Clear wording that exact address/access will be needed before a pickup can be confirmed.
- Keep the existing Formspree endpoint and `assets/customer-routing.js` workflow. Do not remove country/state/city fields required by the routing script.
- Include hidden `source_page` for attribution; the route script should continue to add routing/qualification metadata.
- Validate Android/mobile usability and click-to-call/text. Test form delivery with an explicitly labeled test submission before claiming a verified live delivery.

## Technical publishing and QA gates
Every changed URL must pass:
- HTTP 200 on the deployed custom domain, exact final URL, correct self-canonical (unless purposefully consolidated), robots/index directive appropriate to content.
- One relevant H1, unique helpful title/description, stable breadcrumbs and clear main content.
- Valid parseable JSON-LD, correct `areaServed` and Organization references without fabricated addresses or reviews.
- Images load; descriptive alt text; priority hero and mobile layout functional.
- Call/text numbers and Formspree request workflow unchanged; source attribution present.
- No accidental dead or cross-market navigation links, no content replaced by broad region boilerplate.
- Sitemaps include each important canonical URL. Inclusion is **not** equivalent to indexing.
- Check GSC finalized query/page/mobile data and Keyword.com mobile/desktop trends, with exact city URL and detected Google-selected URL. Compare conversion rates (qualified calls/forms), not only rankings.

## Nationwide rollout gate
Do **not** mass-publish another templated wave of location pages based on this model. First confirm service availability and partner routing; then ship genuinely distinct, validated pages in prioritized markets. Evaluate changes on Rancho Cucamonga, Fontana, Upland, Montclair, Ontario, and nearby corridors over the next settled-data windows.
- Target primary local general keyword; measure *which* URL Google picks; diagnose query overlap.
- Preserve genuine unique appliance-category content and user navigation.
- Get legitimate mentions/citations, real reviews from actual customers, and truthful GBP for eligible verified business presence. Avoid paid links or fabricated local signals.
- A ranking improvement cannot be promised on the deployment day. Only the underlying issues and code can be fixed immediately.

## Changes committed October 10, 2026
- Reduced duplicated eligibility notices and internal SEO-jargon on Rancho Cucamonga, Fontana, Upland, Ontario, Montclair, Claremont, La Verne, San Dimas, Pomona, Chino, Chino Hills, and San Bernardino pages.
- Clarified on-page scope/navigation in Southern California, San Bernardino County and San Bernardino city pages.
- Aligned Fontana and Upland general titles/meta with appliance pickup and removal intent; kept category-specific pages distinct.
- Improved Ontario and Montclair quick request forms from 9 to 6 required fields, preserving the original field names and Formspree endpoint.
- Added `source_page` attribution to Fontana stove/oven requests; made the Upland washer/dryer street address optional (6 required initial fields).
- Confirmed canonical references, forms, phone details and JSON-LD parsing on the priority edited files by inspecting GitHub main branch. **Live GitHub Pages propagation and Google re-crawling remain separate checks.**

## What would constitute success
Primary page begins receiving impressions for its exact city generic query; competing region/service pages decrease as the main city URL becomes the preferred result, while category pages retain their specific queries. Observe 7/14/28-day trends once data is settled, and require rising qualified contacts plus no false promises. Do not confuse a keyword-tracker rank of `0` with Google's explicit "not indexed" status.

## October 10 follow-on audit — 18 city similarity test and local rewrite
- Inspected text-shingle overlap across 18 priority city general-appliance pages, normalizing the city name. Approximate shared-shingle ratios (relative to the smaller page): **West Covina/Pasadena 64% before editing**, Pomona/Covina 38%, Montclair/Chino Hills 32%, Chino/Covina 30%, La Verne/San Dimas 27%. This is a homegrown repeat-text signal, not Google's duplicate-content metric or a confirmed spam action.
- Rewrote **nine West Covina paragraphs + hero** to center on real appliance condition and photo intake, garage/apartment/driveway access, and the distinct Athens Services city disposal alternative. Official West Covina city environmental-service source: https://www.westcovina.gov/259/Environmental-Services ; Athens West Covina bulky-item information: https://athensservices.com/commercial-services/west-covina/ . The program details and Athens phone must be periodically verified.
- Rewrote **eight Pasadena paragraphs + hero** to explain apartment/hillside exit details, the City refuse-customer bulky item process, and its exclusion of refrigerators/air conditioners from the specific bulky program. Official source: https://www.cityofpasadena.net/public-works/waste-management-recycling/residential-refuse-service-recycling/ . Verify city conditions as rules change.
- After these commits the West Covina/Pasadena comparable overlap measured **36.7%** using the same text-shingle method (down from the initial ~64%). This is a quality audit measurement, **not proof that rankings have risen**.
- Updated Montclair's title, meta/OG description and hero to clarify conditional free pickup, photo-first request and actual callback number; Montclair already had a city-specific Burrtec alternative linked.
- Keyword.com October 10 mobile SERP top-25 sampling showed TakeMyAppliance #1 for Rancho Cucamonga, Fontana, Upland, Ontario, Montclair, San Bernardino and Chino Hills; our Montclair URL #6 and Fontana around #20; several other city URLs not detected. Pomona showed **neighboring-city TakeMyAppliance URLs** in positions #1 and #2, a reminder not to mistake all cross-city ranking for a Google penalty.
- GSC Wizard's trial-blocked URL Inspection and on-page audit are **not** evidence of pages being unindexed. SMEPost GSC data is usable with a lag; its last settled endpoint was October 7, 2026. Use it as the measurement standard.
- A GSC page-insights sample: West Covina/Pasadena upgrades were made to lower template repetition, not in response to a demonstrated manual action. Validate future exact-city query impressions and chosen URLs after settled data.
- Next rewrite candidates in quality-first order: Pomona/Covina; Montclair/Chino Hills; Chino/Covina. Do not reduce useful text merely to lower an overlap percentage; replace generic repetitions with verified distinct local utility. Preserve intake, phone, source tracking, service acceptance, all H1/canonical/structured-data links.
