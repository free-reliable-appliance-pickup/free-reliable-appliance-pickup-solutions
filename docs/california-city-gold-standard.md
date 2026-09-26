# California City Gold Standard

Rancho Cucamonga is the reference implementation for the city-level California SEO model.

## Required city architecture

Each gold-standard city should have one primary city hub plus distinct appliance-intent pages where demand justifies them:

- `{city}-appliance-pickup/` — primary city hub for free appliance pickup, removal, haul-away, recycling/disposal choices, qualification, local access, property/commercial requests and conversion.
- `{city}-washer-dryer-pickup/` — laundry-specific testing, gas/electric details, sets, stacked installations and access.
- `{city}-refrigerator-pickup/` — cooling condition, refrigerator/fridge terminology, dimensions, interior/model photos and door/access issues.
- `{city}-freezer-pickup/` — chest/upright terminology, freezing condition, dimensions and garage/shed/basement access.
- `{city}-stove-oven-pickup/` — stove/range/oven terminology, fuel type, tested functions, disconnection and heavy-unit access.

Do not create a separate page for every synonym. The main city hub should naturally cover related intent such as appliance removal, old appliance removal, haul-away, recycling, disposal, junk-appliance alternatives and near-me wording. Appliance-specific child pages own the deeper category details.

## Local proof and usefulness

Every city hub must contain facts that are genuinely local to that city rather than swapped city names. Use the actual neighborhoods, physical ZIP codes, access conditions, local property patterns and an official municipal or waste-resource link when relevant. Do not copy a competitor's factual claim without checking the official source.

Where a ZIP is mailing-only or otherwise unsuitable for physical routing, say so rather than copying it into a service list.

The page should explain the difference between:
- qualification-based free pickup for working/reusable major appliances;
- paid junk/appliance removal when guaranteed paid hauling is the better fit; and
- the city's own bulky-item, waste or recycling option when applicable.

## Search-intent ownership

The city hub should prominently and naturally cover the phrases customers actually use, without keyword stuffing:
- free appliance pickup;
- appliance pickup;
- appliance removal;
- old appliance removal;
- appliance haul-away;
- appliance recycling and disposal;
- working/reusable appliance pickup;
- washer, dryer, refrigerator/fridge, freezer, stove/range/oven pickup;
- garage, driveway, inside-home, apartment and condo access;
- landlords, property managers, senior/55+ communities and recurring/commercial replacement work.

When discussing donation or give-away intent, be explicit that Free Reliable Appliance Pickup is not a charity and does not issue tax-deductible donation receipts.

## Images

Use real appliance photos. The preferred hero image must:
- be high quality and relevant to the page;
- use an HTML `<img>` element;
- have useful alt text;
- declare width and height;
- use `fetchpriority="high"` for the hero;
- have a descriptive, city/category-specific file URL where practical;
- match `og:image`, Twitter image metadata and `WebPage.primaryImageOfPage`;
- be discoverable through `sitemap-images.xml`.

Do not repeat the exact same non-logo image twice on the same specialty page merely to increase image count.

## Structured data and locality

Use accurate Service, WebPage, BreadcrumbList and FAQPage JSON-LD that matches visible page content. Keep title, meta description and WebPage name/description synchronized.

City service-area pages must not invent a storefront, office, staff location or per-city LocalBusiness entity. The network model should stay explicit: requests are reviewed through independent local pickup professionals where coverage is available.

Do not add AggregateRating or review markup without verified, page-visible review data that meets Google's policies.

Do not publish claims such as “serving since YYYY,” “X years in business,” founding dates, certifications, review counts or ratings unless the claim is documented and can be kept current.

## Internal linking

The main city hub must link to each city appliance-intent child page. Each child must link back to the city hub and use the city hub in its breadcrumb hierarchy.

Regional hubs should link into the city hub, and category/regional pages should link to important city specialty pages when contextually useful. Anchor text should describe the destination rather than use generic "click here" wording.

As a minimum crawl-safety baseline, a configured gold city hub should have at least 8 active internal inlinks and remain within 2 clicks of the homepage. Each configured appliance-intent child should have at least 3 active internal inlinks and remain within 3 clicks of the homepage. These are site architecture safeguards, not claims that a specific link count causes rankings.

## Long-page navigation

Gold city hubs are intentionally comprehensive, but they should not force mobile users to scroll blindly. Place a compact, crawlable in-page navigation near the top using normal `<a href="#section">` links and stable section IDs. At minimum, expose shortcuts to qualification, appliance types, local areas, access, real photos, property/commercial information, FAQ and the request form.

Use descriptive anchor text rather than generic “click here” wording. This is primarily a usability standard; it also keeps important sections easy for crawlers and users to understand.

## Conversion

The city hub should provide a direct local request form plus call/text actions. Near the top of the page, clearly state that a request is free to submit and does not require an account or credit card when that is true for the live request flow. Specialty pages may route to the city hub request form when that keeps one clean conversion endpoint.

The request path should ask for appliance type, brand/model when known, true working condition, whether the appliance is testable, photos/photo availability, exact address/ZIP, property type, floor/stairs, access details and a preferred pickup window. Never guarantee same-day pickup or free acceptance before qualification and route review.

Keep a direct Text Photos action visible when the form backend does not support native file uploads. Only enable native photo-upload fields after confirming the live form backend/account supports them; do not publish a file input that silently fails.

Place a concise request-contact disclosure beside the submission action and link the site's Privacy Information and Service Terms so customers can understand how their request information and local-provider routing are handled.

## Anti-duplication rule

A gold-standard city page must not become a clone of another city page. The reusable structure is the model; the local facts, access conditions, official resources, examples and wording must be specific to the market.

The automated workflow `Audit California City Gold Model` enforces the structural baseline for cities listed in `data/california-city-gold-standard-clusters.json`.
