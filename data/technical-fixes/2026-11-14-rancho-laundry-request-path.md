# Verified technical repair — Rancho Cucamonga laundry intake
Date: 2026-11-14 (America/Mazatlan calendar date)
Affected page: /rancho-cucamonga-washer-dryer-pickup/
Existing shared intake: /rancho-cucamonga-appliance-pickup/#request
Active protected experiment: 2026-11-12-rancho-laundry-exact-city-title; review not before 2026-11-29.

## Confirmed defects
- Main-branch GitHub Actions Audit Approved Request Actions (run 43674825013) failed because the laundry page had its own duplicate Formspree endpoint, instead of linking to the existing shared city request form.
- Audit California Laundry Gold Standard (run 43674824843) failed the expected request target and form architecture.
- Audit California City Gold Model (run 43674824929) failed for missing city-parent request path.
- Validate Google Search Appearance (run 43674824881) failed WebPage JSON-LD description versus HTML meta description mismatch.
- Existing city intake was inspected: it has Washer, Dryer and Washer and Dryer options plus washer tests, dryer tests, dryer gas/electric choice, floor/stairs/access and photo availability. Thus this change retains functional customer intake.

## Narrow correction and preservation
- Replaced only the dedicated page's duplicate inline Formspree form with a prominent link to the existing shared city form, call/text photo link and helpful washer-specific instructions.
- Aligned the WebPage structured-data description exactly with the existing HTML meta description.
- Preserved the active experiment's HTML title, H1, canonical URL, original washer/dryer hero image, regional linking intent and all accepted-appliance boundaries.
- Did not change the shared city form, lead destination, Formspree account, phone routing, robots or sitemap.
- No claim of actual customer form delivery, Google indexing changes or search ranking improvement.
- Qualifies for the documented [technical-fix] exception (verified broken intake architecture and machine-readable metadata mismatch); not an SEO copy experiment.

## Verification
- Read actual repository source and latest main-branch GitHub Actions failures before changing code.
- Confirmed the duplicate form endpoint is absent and the city request path is present in the revised source.
- Confirmed the protected page title and image URL remain unchanged.
- PR CI must pass before merge and deployed URL must be checked separately.
