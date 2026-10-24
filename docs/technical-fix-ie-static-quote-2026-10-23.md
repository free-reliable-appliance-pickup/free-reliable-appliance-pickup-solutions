# VGM technical exception: Inland Empire optional quote preference (2026-10-23)

## Verified baseline and classification
On main at `332fab4d27b08478ef9df6b5a5aa32f38508ba19`, the existing Colton, Bloomington and Highland general pickup forms have one approved POST action (`https://formspree.io/f/mvzeapzd`), a required telephone input, city-specific `source_page`, and `service=General major appliance pickup`. They do not contain the optional `paid_removal_preference` selector and do not load `assets/paid-removal-choice.js`. Thus the already owner-approved free-first / optional paid-removal quote choice is unavailable in these three forms. This is a verified customer-intake omission, **not** evidence of search-ranking harm or broken Formspree delivery.

## Narrow repair
Add a static, optional, blank-default `paid_removal_preference` selector with `free_only` and `quote_ok` values immediately before the existing submit button on these three forms. Extend `scripts/audit-sfv-paid-quote-static.py` to cover all three. No automatic quote, charge, booking or permission to offer paid service when `free_only` is chosen. Do not change required fields, phone numbers, service coverage or acceptance, Formspree action, images, title/body SEO copy, canonical, schema, links, sitemap or experiment registry.

## Freeze gates and ownership
`data/seo-experiments.json` marks Colton's and Bloomington's 2026-10-04 people-first simplifications and Highland's California anti-template cleanup as `running`, with `evaluateNotBefore=2026-10-14`. This customer-intake technical exception leaves their protected ranking variables untouched. Daily SEO Ranking Countermove retains ownership of search experiments; Website Technical Repair retains emergency repairs.

## Validation and deployment
Require the static-quote audit, priority form/intake audits, SEO experiment guard and all applicable PR checks on the latest head SHA before merge. Verify source after merge and Pages workflow status; independently verify exact live HTML before claiming live behavior. Actual Formspree receipt requires a separately authorized controlled end-to-end test; no test lead should be submitted during this change.

## Rollback
Revert the isolated PR if form display, submission, consent semantics or route attribution regress. Do not modify the ranking experiment registry to force this exception.
