# SEO + Lead Reporting

## Connected data
Google Search Console is connected through the authorized GSC Content Planner organization for Free Reliable Appliance Pickup.

The first finalized U.S. snapshot imported into Supabase covers:
- 2026-08-31 through 2026-09-27
- 889 impressions
- 10 clicks
- 1.12% CTR
- average position 20.58

The import stores:
- site totals
- query metrics
- page metrics
- query/page relationships

## Internal funnel report
Supabase view: `public.reporting_page_funnel`

It compares the latest imported Google page metrics with lead submissions from the same period:
- organic impressions
- organic clicks
- CTR
- average position
- leads
- progressed leads
- leads per organic click

The view is not accessible to anonymous or normal authenticated browser users. It is reserved for trusted server-side reporting.

## Attribution caveat
Organic Google does not provide a reliable exact search-query-to-individual-customer identity. We compare organic query/page performance with page-level lead production over the same time window. Paid click IDs and UTM-tagged campaigns can be attributed more directly.

## Current baseline examples
The first snapshot already shows useful differences:
- some pages have first-page average positions but little/no click activity
- Imperial Beach and Irvine have recorded organic clicks
- Rancho Cucamonga has impressions but still needs stronger visibility overall
- the data can now be compared with future tracked V2 leads instead of judging success by rank alone

## Next reporting layer
When staging is deployed, add an authenticated owner dashboard that reads this internal view and the lead event history.
