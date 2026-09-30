# Free Reliable Appliance Pickup — Platform V2

## Purpose
Build the long-term platform without touching the current live GitHub Pages site until the replacement is fully tested.

## Locked foundation
- Front end / SEO site: Astro
- Hosting / edge runtime: Cloudflare Workers
- Database, authentication, storage: Supabase
- Source control: GitHub
- Payments later: Stripe
- Existing domain and current URLs remain unchanged until cutover is approved.

## Two-track strategy
### Track A — rankings now
Continue improving the existing live site: indexing, canonicals, internal links, unique local content, local authority, business listings, backlinks, reviews, and conversion.

### Track B — future platform
Build the partner marketplace in this isolated folder/branch.

## Non-negotiable migration rules
1. Do not delete or rename live URLs without a documented redirect plan.
2. Preserve canonical URLs, titles, meta descriptions, schema, phone rules, images, forms, and sitemap coverage.
3. Build and test on a staging hostname before changing DNS.
4. Compare old vs new URL-by-URL before launch.
5. No bulk generation of thin or near-duplicate city pages.
6. Every indexable location page must have real unique local value.
7. No live-site replacement until crawl, indexing, forms, mobile, analytics, redirects, and structured data pass checks.
8. Keep a rollback path.

## Initial data model
- customers
- pickup_requests
- appliances
- request_photos
- service_areas
- partners
- partner_service_areas
- lead_offers
- lead_claims
- jobs
- job_events
- subscriptions
- payments
- notifications

## Core workflow
Homeowner submits request → system matches service area → eligible partners receive lead → partner claims/unlocks → contact details released → pickup outcome recorded.

## SEO content model
- state hubs
- metro hubs
- city appliance-pickup pages
- city washer/dryer pages
- appliance-type pages
- commercial pages
- partner recruitment pages
- guides/resources

## Phase 1
1. Inventory existing URLs and identify canonical winners.
2. Define reusable page data schema.
3. Build Astro shell and component system.
4. Reproduce a small test set of existing URLs exactly.
5. Build Supabase schema in a non-production project.
6. Add homeowner request flow.
7. Add partner authentication and basic dashboard.
8. Add territory matching.
9. Test staging before any migration.

## Launch gate
Migration happens only when:
- priority URLs match or redirect correctly
- sitemap is valid
- canonicals are correct
- robots rules are correct
- structured data validates
- mobile performance is acceptable
- forms work
- partner workflow works
- 404/redirect audit passes
- old site remains recoverable
