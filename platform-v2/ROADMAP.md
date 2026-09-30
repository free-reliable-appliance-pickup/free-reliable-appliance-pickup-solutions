# Platform V2 — Safe Build Roadmap

## Current state discovered
An existing Supabase project named `free-reliable-appliance-pickup-partners` is active and already contains the beginnings of the marketplace:
- partner applications
- partner territories
- appliance leads
- marketplace buyers
- marketplace territories
- marketplace opportunities
- offers
- events
- wallets and wallet transactions
- payments
- pickup confirmations
- subscriptions
- auto-buy rules
- disputes

This means we do **not** rebuild the database from zero. We preserve the useful work and improve it carefully.

## Safety findings before public connection
Supabase advisory checks currently report:
- several RLS-enabled tables with no policies yet
- some foreign keys without covering indexes
- some RLS policies that can be optimized
- pg_net installed in the public schema

These are not reasons to delete anything. They are a checklist to resolve before exposing marketplace functions publicly.

## Rules for all future work
1. No deleting live pages just to simplify architecture.
2. No changing the public domain during development.
3. No changing existing high-value URL slugs unless a redirect is planned and tested.
4. No production database destructive migrations without an explicit review.
5. No new tool/platform unless it fills a documented gap in the locked stack.
6. New marketplace work goes into isolated development/staging first.
7. Ranking work continues independently on the current live website.

## Build order
### 1. Foundation audit
- inventory current live URLs
- identify duplicates/canonical conflicts
- map current forms and phone-number rules
- document existing Supabase tables and relationships
- review RLS policies before connecting buyer/customer dashboards

### 2. Astro SEO shell
- global layout
- header/footer
- metadata/canonical component
- schema component
- city-page template
- washer/dryer template
- commercial template
- partner template
- sitemap generation
- robots generation

### 3. Data-driven location system
Create one structured location dataset with fields for:
- city
- state
- metro/cluster
- county
- ZIPs
- unique local introduction
- service qualification rules
- phone number
- nearby locations
- images
- FAQs
- commercial notes
- partner coverage status

### 4. Marketplace MVP
- homeowner request
- photos
- lead creation
- territory matching
- partner login
- opportunity list
- claim/pass
- contact release after authorized claim
- admin visibility
- event audit trail

### 5. Protection and scale
- RLS policies
- rate limiting
- validation
- indexes
- abuse controls
- logging
- backups
- payment webhook verification

### 6. Staging SEO parity
Before launch, compare a priority sample of current vs V2:
- status code
- URL
- canonical
- title
- description
- H1
- schema
- internal links
- image alt text
- form behavior
- phone
- sitemap presence

### 7. Cutover only after pass
No DNS change until the parity checklist passes and rollback is ready.
