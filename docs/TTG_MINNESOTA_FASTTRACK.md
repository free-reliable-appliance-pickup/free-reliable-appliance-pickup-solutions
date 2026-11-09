# Minnesota TTG FastTrack — State batch 01 (request-only)

## Plan and release safeguards
- One state branch, one PR, 40 manifest-listed HTML pages (one statewide hub, 15 city guides, 24 category guides covering six high-priority markets).
- Build only useful request-only information. Noindex/follow with correct self canonicals and **no Minnesota service partner claims**, no fake local photos, no unverified free routes.
- Reuse the existing Formspree endpoint and `/assets/customer-routing.js`, one real existing appliance photo per page, actual photos required for approval but photo link optional for initial inquiry, full stairs/access/condition fields, paid quote only by opt-in.
- The city request list is Minneapolis, Saint Paul, Bloomington, Brooklyn Park, Maple Grove, Blaine, Woodbury, Lakeville, Rosemount, Plymouth, Eden Prairie, Burnsville, Rochester, St. Cloud and Duluth.
- Dedicated four categories only for Minneapolis, Saint Paul, Bloomington, Brooklyn Park, Maple Grove and Rochester. Avoid broad low-value category clones for other cities without confirmed demand.
- State-level routing is already request-only in `data/market-routing.json`; do not change it or index pages without actual accepting operators and owner approval.

## Market signals (checked 2026-11-09)
- Minnesota State Demographic Center: 2025 population 5,891,109 and 2,375,248 households: https://mn.gov/admin/demography/data-by-topic/population-data/our-estimates/
- Metropolitan Council: Twin Cities households increased 6.6% between 2020 and 2025: https://metc1new.metctest.state.mn.us/Data-and-Maps/Community-Development-Research/Forecasts-and-Estimates/Population-and-Household-Estimates.aspx
- Minnesota MPCA refrigerant guidance: https://www.pca.state.mn.us/business-with-us/working-with-refrigerants
- Saint Paul city bulky item collection, revised July 2026: https://www.stpaul.gov/departments/public-works/garbage-and-recycling/residential-collection/bulky-item-collection
- Local market alternatives include appliance resale stores, junk removal firms, public recycling programs, and programs operating under separate rules. Do not claim exclusivity or #1 ranking.

## Staging, testing, activation
1. `python scripts/ttg_state_batch_qa.py` and `python -m unittest discover -s tests -p 'test_ttg_minnesota_pages.py' -v`.
2. All relevant GitHub CI, tests, link/image/SEO audits and CodeQL must pass on the exact PR head; inspect substantive review notes.
3. Merge once, monitor GitHub Pages build, then read-only smoke-check live hub, sample city/category pages and form attributes; don't POST fake requests.
4. Independently confirm an accepting operator for each city and supported ZIP, eligibility, safe access, free/paid terms, plus actual owner-controlled Formspree inbox receipt before any launch PR.
5. Request a separate reviewed city-level SEO/indexing activation; monitor GSC impressions and real inquiries. No bulk activation based on passing code checks.

**Release progress:** staged pages are distinct from active service, proven Formspree receipt or indexable city service.
