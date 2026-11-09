# TTG Minnesota batch — 2026-11-09

## Release classification

**Staged for review only.** Each of 31 pages is request-only, noindex/follow with one existing real appliance photo, a complete Formspree request, and separate optional paid quote; local Minnesota partners and pickup zones are **not** independently confirmed. Do not add to the sitemap or promote service claims until actual operator acceptance, QA, review, and live-test checks are done. This is not active partner recruiting.

## Market grounds

- Minnesota State Demographic Center: approximately 5.89 million population and 2.375 million households (2025 estimates, released July 2026). https://mn.gov/admin/demography/data-by-topic/population-data/our-estimates/
- Census Bureau: Minnesota 2025 housing units 2.62 million and 2025 authorized building permits 20,947 (different methodology/date from the state demographic estimates). https://www.census.gov/quickfacts/fact/table/MN/POP715224
- Metro Council residential development identifies Twin Cities suburban housing activity; this informs city priority, not pickup proof. https://metc2new.metctest.state.mn.us/Data-and-Maps/Community-Development-Research/Housing/Residential-Development.aspx
- TakeMyAppliance has statewide, Minneapolis, St. Paul, and category-specific Minnesota pages; compete on truthful conditions, real photos, useful access details and verified fulfillment rather than mass near-duplicate city pages. https://www.takemyappliance.com/locations/minnesota
- Hennepin County publishes a working-appliance reuse path and legal recycling options. https://www.hennepincounty.gov/green-disposal-guide/items/appliances
- Xcel Energy has its own restricted refrigerator/freezer recycling program; do not present its rebate or pickup as ours. https://xcelenergymn.clearesult.com/indoor-pickup

## Prioritization

First cluster: Minneapolis, St. Paul, Bloomington, Woodbury. Independent urban markets: Rochester and Duluth. Later candidates (requires actual lead/partner evidence): Plymouth, Maple Grove, Lakeville, Eagan, Eden Prairie, Burnsville, St. Cloud, Blaine, Brooklyn Park, Coon Rapids, Edina, Minnetonka, Shakopee, Roseville.

## Pre-merge checklist

- Run `python scripts/ttg_state_batch_qa.py` and ordinary CI on exact head. Treat CodeQL and other scans as evidence, not a stand-in for required release review.
- Verify all 31 self canonicals, one photo per page, category-appropriate real photos and mobile form behavior.
- Formspree and routing script must accept an MN form without giving a false receipt or assigning an unverified partner.
- Get actual operator name, geography, terms, dates/ability to accept and fees before claiming service or enabling indexing.
- Obtain all actual required reviewer approvals; do not bypass old 2-independent-model requirement or equate HTTP 429 with success. Then merge/deploy and smoke-test the actual live form before any indexation.
