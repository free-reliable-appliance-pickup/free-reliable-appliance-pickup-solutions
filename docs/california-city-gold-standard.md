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

## Specialty-page parity

A gold-standard city cluster is only as strong as its appliance-specific child pages. Washer/dryer, refrigerator, freezer and stove/range/oven pages should all inherit the same local trust layer as the city hub while keeping category-specific preparation details.

Each specialty page should include:
- the city and county context when useful for local disambiguation;
- the verified official local disposal/bulky-item reference when one exists;
- a direct near-me style answer written naturally for that appliance category;
- preparation guidance specific to that appliance, such as gas/electric or water connections for laundry, refrigerant-system safety for refrigerators/freezers, and safe gas/hardwired disconnection for cooking appliances;
- a link back to the city hub and the appropriate regional/category authority pages;
- no self-link to the page the customer is already viewing.

Do not duplicate the same generic paragraph across all four child pages. The structure should match; the appliance details should differ.

## Local proof and usefulness

Every city hub must contain facts that are genuinely local to that city rather than swapped city names. Use the actual neighborhoods, physical ZIP codes, access conditions, local property patterns and an official municipal or waste-resource link when relevant. Do not copy a competitor's factual claim without checking the official source.

Where a ZIP is mailing-only or otherwise unsuitable for physical routing, say so rather than copying it into a service list.

The page should explain the difference between:
- qualification-based free pickup for working/reusable major appliances;
- paid junk/appliance removal when guaranteed paid hauling is the better fit; and
- the city's own bulky-item, waste or recycling option when applicable.

## Customer decision path

Every gold-standard city hub should make the removal choice understandable in one scan. Use a compact three-path module:

- **Working or reusable appliance:** send it through the qualification-based free-pickup review. State the pickup charge clearly when the request qualifies, but never promise acceptance before review.
- **End-of-life appliance with an official local option:** link the verified city/hauler program, state only the eligibility and limits confirmed by the official source, and keep that public-program contact clearly separate from our own number.
- **Broken appliance or guaranteed timing needed:** explain that a paid removal company may be a better fit when the customer needs guaranteed hauling or the appliance does not qualify for reuse-focused pickup. Do not invent third-party prices or timing.

Add practical preparation guidance to protect reuse value and safety. Do not tell customers to move a good appliance to the curb before pickup is confirmed. For refrigerators/freezers, do not advise cutting refrigerant lines or removing compressors. For gas appliances, do not imply that an untrained customer should disconnect a gas line.

The city FAQ should answer two preparation questions directly: whether the appliance must be placed at the curb, and whether it must be disconnected before pickup. Keep the visible answers and FAQPage schema synchronized. The answer should reflect the actual service model: inside/garage/driveway requests may be reviewed when safe, and final disconnection/preparation depends on appliance type and access.

This module should answer the customer's real decision rather than simply repeat keyword variants. It is part of the reusable structure, while the official program, eligibility rules, local access issues and wording must be verified separately for each city.

When an official city or county source identifies a separate destination for special items—such as microwaves, e-waste or household hazardous waste—add that guidance only when it prevents a realistic customer mistake. State clearly which items the facility accepts and which major appliances it does not handle. Do not turn a city page into a generic disposal directory, and do not copy competitor disposal facts without checking the primary local source.

## Search Console feedback loop

Use finalized Search Console query/page evidence to refine titles, descriptions, internal links and child-page emphasis. Treat very small impression samples as directional evidence, not a stable ranking. Do not claim a fixed Google position from one or two impressions, and do not stuff a city page with every query variant. When Google is already testing a page for a relevant intent, strengthen the most useful existing page before creating another URL.

## Acceptance boundaries

The gold model should be explicit about what the free program does **not** cover. Do not add an appliance category merely because a competitor ranks for it. If dishwashers, microwaves, water heaters or other items have stricter rules or are outside the free program, say so clearly in visible content and keep the request form wording consistent.

Use negative/qualification language to reduce bad leads, not to manufacture extra keyword pages. A truthful “not accepted alone” or “not part of this free program” answer is more useful than implying broad acceptance and disappointing the customer later.

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

## Recurring and property-program lead quality

For apartments, senior/55+ communities, property managers, installers, retailers and recurring replacement programs, the city hub should ask for enough information to judge the batch before anyone plans a route. At minimum, request appliance count by category, working/testable status, sample photos or model labels when practical, replacement cadence, staging/loading details, appointment rules and an onsite contact.

Make the business intent explicit on the city hub rather than hiding it behind a generic commercial page. A gold city should naturally cover one-time and recurring appliance replacement loads, apartment/rental unit turns, senior/55+ community upgrades, retailer/installer swaps and facility replacement work when those are real service opportunities.

Where the city has a franchised or otherwise regulated solid-waste system, distinguish appliance-reuse pickup from general commercial trash hauling. Link the verified municipal source and do not imply that the appliance network is a substitute for regulated trash, hazardous-waste or non-qualifying disposal service.

Do not treat recurring work as a generic household pickup with a larger appliance count. The brief should make it possible to distinguish a high-quality reusable batch from a mixed cleanout or end-of-life load.

## Network transparency placement

If the city is served through independent local pickup professionals, explain that next to the pickup process—not only in a footer or deep-page disclaimer. The customer should understand before submitting that the page represents a service-area network rather than a company-owned local branch, and that pickup is confirmed only after an available local provider accepts the qualified request.

Keep this disclosure concise and avoid repeating the same network paragraph again near the bottom of the page. Transparency belongs close to the decision flow; duplicated boilerplate does not add local value.

## Conversion

The city hub should provide a direct local request form plus call/text actions. Near the top of the page, clearly state that a request is free to submit and does not require an account or credit card when that is true for the live request flow. Specialty pages may route to the city hub request form when that keeps one clean conversion endpoint. For a configured single-intake city cluster, every appliance-specific child page should use the city hub as the one customer submission endpoint rather than maintaining separate duplicate forms. This prevents qualification fields, privacy text, contact disclosures and routing rules from drifting apart across the local cluster.

The request path should collect appliance type, brand/model when known, true working condition, whether the appliance is testable, photos/photo availability, exact address/ZIP, property type, floor/stairs, access details and a preferred pickup window. Never guarantee same-day pickup or free acceptance before qualification and route review. Keep “free to submit” separate from “free pickup”: the request can be free to submit while the $0 pickup applies only after the appliance/load qualifies and pickup is confirmed.

Keep the first submission low-friction. For a city-specific household form, require only the essentials needed to identify and respond to the request: name, phone, city, ZIP, appliance type and condition. Street address, brand/model, floor/location, stairs, property type, testability, photo status, preferred window and access notes can remain optional and be confirmed by call/text after the first review. The visible “quick request” promise must match the actual HTML required fields.

Keep a direct Text Photos action visible when the form backend does not support native file uploads. Only enable native photo-upload fields after confirming the live form backend/account supports them; do not publish a file input that silently fails.

Place a concise request-contact disclosure beside the submission action and link the site's Privacy Information and Service Terms so customers can understand how their request information and local-provider routing are handled.

## Content discipline and anti-duplication

A gold-standard city page must not become a clone of another city page. The reusable structure is the model; the local facts, access conditions, official resources, examples and wording must be specific to the market.

Comprehensive does not mean repetitive. Consolidate overlapping sections when they answer the same customer question. For example, do not keep separate “what we accept” and “appliance types” sections if one well-structured section can cover qualification plus category breadth. Keep one stable section ID per topic, one jump link per destination, and no duplicate HTML IDs.

Do not add city history, demographics, neighborhood names or local facts merely to increase word count. A local fact should help with service qualification, routing, access, disposal alternatives, audience fit or customer decision-making.

The automated workflow `Audit California City Gold Model` enforces the structural baseline for cities listed in `data/california-city-gold-standard-clusters.json`.
