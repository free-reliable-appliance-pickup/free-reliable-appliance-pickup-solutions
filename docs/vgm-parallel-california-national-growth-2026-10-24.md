# VGM: parallel California authority + nationwide discovery — 2026-10-24

## Decision
Do not hold nationwide photo/market rollout until California ranks in positions 1–3. Run both workstreams in parallel, but launch only genuinely distinct local pages with confirmed actual service/contact or honestly labeled request-first coverage. Avoid thin doorway city variants and unverified city-specific completion claims.

## Confirmed issue
Prior to this change, the homepage "State & National Coverage" card linked California, Arizona, Oregon and Colorado, but omitted direct homepage links to the already-published Washington, Nevada, Texas, Florida, Idaho and Columbus, Ohio hubs. Texas and Florida request-first state pages showed only a corporate logo in the main hero instead of actual appliance type examples. Their existing qualification and expansion-market notices were accurate and must remain.

## Baseline and testable hypotheses
- Finalized Google Search Console (2026-10-19 through 2026-10-21) returned one Washington state-hub impression, zero clicks, page average position 2 (not meaningful evidence of a stable #2 rank). Nevada, Texas, Florida, Idaho, Arizona, Oregon and Colorado **state hub URLs** returned no page rows during that short 3-day period (not proof of deindexing).
- Nationwide/priority California keyword tracker last reported 13/100 tracked queries in top 10 and 30/100 in top 20; this is a cross-market metric, not a state hub KPI.
- Homepage link hypothesis: direct editorial links to existing, qualified state hubs will improve their discoverability and navigation from the homepage; inspect finalized GSC impressions and query/page ownership after the observation window. Merely adding a link does not prove or guarantee higher ranks.
- Texas and Florida photo hypotheses (independent pages): relevant and correctly described appliance photographs can improve user comprehension relative to corporate-logo-only content. Measure actual customer lead counts and navigation; photos alone are not a Google ranking guarantee.

## Controlled changes
1. Existing homepage state-hub card: add Washington, Nevada, Texas request-intake, Florida request-intake, Idaho request-intake and Columbus/Ohio links. All destinations existed before this PR. Distinguish request-only coverage and repeat the requirement for local confirmation.
2. Texas request-intake page: replace logo-only hero with a visually inspected repository-backed group appliance image. The alt explicitly describes a representative example and **does not falsely claim a Texas pickup**.
3. Florida request-intake page: replace logo-only hero with a different preexisting garage group appliance photo and similarly honest alt text. Do not change local coverage claims or qualifications.
4. Extend the existing active-image audit with regression checks for the homepage's six national links and two visually approved image URLs/representative alt text.

## Preserve the original SEO experiment
No changes to titles, H1 text, description, robots, canonicals, structured data, phone numbers, Formspree endpoint or city pages. The current homepage snippet experiment had an evaluate-not-before date of 2026-10-14, which has already passed. Monitor the homepage link change separately and avoid simultaneous home metadata rewrites. No change to protected California city hero experiments.

## Operational expansion guidance
Build original/meaningfully localized general appliance pages and specialty pages only where coverage, actual appliance types, partner capacity, local contact and original photo content support a useful page. Existing form-first state hubs can collect honest requests while local partners are being recruited. Prioritize California ranking repair and, in parallel, WA/OR, AZ, NV, CO and existing Texas/Florida request intake; no need to pause nationwide photo preparation.

## Verification and rollback
Merge only if applicable GitHub audits pass. Then verify the merged source, successful GitHub Pages deployment and public website homepage links and both updated photographs. Check linked destinations. Revert the three HTML changes as a unit if links or images are broken, coverage is misstated or conversion regressions are discovered. Neither green CI nor published changes demonstrate improved organic rankings or incoming leads.