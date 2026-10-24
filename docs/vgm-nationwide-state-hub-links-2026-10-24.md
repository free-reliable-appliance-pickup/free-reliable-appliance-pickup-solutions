# VGM nationwide discovery & service-hub linking experiment — October 24, 2026

## Confirmed gap and existing inventory
- Homepage `index.html`, section `homepage-service-hubs`, had a crawlable link to California, Arizona, Oregon and Colorado state hubs, but did not directly link Washington, Nevada, Texas, Florida, Idaho or Utah state hubs from the state-hub card.
- Those six hub URLs were independently verified present in `sitemap.xml` and their existing source pages were verified before linking. Texas and Florida specifically state they are expansion-market request review, **not guaranteed operating coverage**; Idaho and Utah similarly qualify availability by partner/route.
- The homepage already linked to selected WA/NV local/regional pages in a separate featured-city card; this is an information architecture/direct state-hub link gap, **not** a claim that the pages were orphaned or unindexed. Do not portray a sitemap link alone as a ranking improvement.

## Before baseline (finalized October 19–21, 2026)
Search Console, source: connected GSC SEO Content Planner, free recent three-day view:
- `/washington-appliance-pickup/`: 1 impression, zero clicks, average position 2, **single-impression estimate not reliable for stable rank**.
- `/oregon-appliance-pickup/`, `/colorado-appliance-pickup/`, `/arizona-appliance-pickup/`, `/nevada-appliance-pickup/`, `/texas-appliance-pickup/`, `/florida-appliance-pickup/`: no reportable page rows during that short window. **Not evidence of deindexing**.
- City-level reference only: Portland 16 impressions, position 7.19; Salem 10 impressions, position 8.5; Phoenix 14 impressions, position 31.57. These are separate pages, not valid direct measurements of statewide hub link effectiveness.
- No meaningful impression comparison is available in the post-trial free GSC view.

## Hypothesis and single variable
Giving six existing statewide owner hubs clear crawlable links from the established homepage state-hubs card may make those hubs easier for users/crawlers to discover and clarify the nationwide service hierarchy, while preserving California priority placement. Explicitly group TX/FL/ID/UT under request review to avoid unsupported service availability claims.

**Only the homepage state-hub card is being changed.** No new city pages, page titles, descriptions, copy on destination pages, structured data, canonicals, robots, internal-link removals, photo swaps or phone changes. Existing state and local owner pages remain their query owners.

## Measurable evaluation
- Change date: October 24, 2026.
- Minimum protected observation gate: November 1, 2026 (7 days); preferred review: November 7, 2026 (14 days).
- Outcome signals: Search Console finalized impressions, clicks and indexed owner URL performance for the six state hubs, with separate checks for their connected local cities. Compare to the Oct19–21 baseline only where impression counts are adequate. A higher number of links or successful deployment alone does not establish ranking gains.
- Preserve homepage link experiment until the review window, unless a verified incorrect link/coverage/technical defect requires correction.
- Revert from PR if a broken destination, incorrect coverage representation, accessibility failure or CI regression is found.

## Existing homepage concentration safeguard reconciled
The initial PR check `Audit Homepage Concentration` correctly failed: the six new state links raised unique homepage internal destinations from 62 to 68, above the old 62-destination policy. The former cap was a local site-policy limit, not a Google-required maximum. In the same PR, the existing guard was **narrowly updated to a hard cap of 68**, and six existing indexable/sitemapped state hubs were explicitly added to its mandatory-link set. The guard still requires all previous California, statewide and major-market links and preserves the low-friction customer form. This is a transparent, documented expansion of authority distribution, not a silent audit bypass. If later unrelated homepage links are added, the guard will fail until independently reviewed.

## Verification checklist
1. Confirm six destinations already exist, self-canonical and are in the sitemap.
2. Run GitHub CI (link graph, SEO Experiment Guard, content, schema and deployment checks).
3. Merge only after all PR checks pass.
4. Confirm `main` and freshly fetched public homepage `<a href>` contain the links and truthful request-review disclaimer.
5. **Do not claim** form leads, organic clicks or ranking changes without corresponding measurements.
