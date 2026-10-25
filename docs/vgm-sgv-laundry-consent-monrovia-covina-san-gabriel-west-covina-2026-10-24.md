# VGM — SGV laundry optional quote consent (2026-10-24)

## Verified source gap
At main commit c3c8048cb30a2dad313f8d16f7c2c1662371904a, existing washer/dryer request forms for Monrovia, Covina, San Gabriel and West Covina had approved Formspree POST actions, required telephone fields and source-page attribution, but lacked the static optional paid-removal quote preference already approved on nearby California forms. The four ZIP inputs lacked postal-code autofill; West Covina's phone field lacked tel autofill and keypad hints. This is customer-intake consistency work, **not** evidence of failed delivery or search-ranking weakness.

## Reversible, limited change
Add a blank-default optional `paid_removal_preference` selector with `free_only` and `quote_ok` values and a clear notice that a quote is not a booking or charge. Add `autocomplete="postal-code"` to four ZIP fields and `autocomplete="tel" inputmode="tel"` to West Covina's required telephone input. Extend the existing static quote audit to the four pages. Do not change the Formspree endpoint, required fields, phone links, service eligibility, city claims, page images, titles, canonicals, internal links, structured data or SEO body copy.

## Experiment and ownership protection
The running `2026-10-06-zero-visibility-laundry-structure-simplification` (Covina), `2026-10-06-west-covina-laundry-concentration`, `2026-10-06-san-gabriel-laundry-concentration` and `2026-10-06-monrovia-laundry-title-intent` experiments all have `evaluateNotBefore=2026-10-16`; no hypothesis, content, title, schema, ownership or freeze gate is modified. This is a documented technical customer-intake exception under `data/seo-experiments.json`. Daily SEO Ranking Countermove owns ranking experiments; Website Technical Repair owns emergency breakage.

## Validation and release
1. Confirm the PR diff is limited to the four existing forms, this record and the static quote audit.
2. Run `python3 scripts/audit-sfv-paid-quote-static.py`, phone/form and SEO Experiment Guard checks at exact PR head. Do not merge while required checks fail.
3. After merge, separately confirm Pages deployment and retrieve public HTML for each form. Formspree email delivery requires separate end-to-end testing; never infer receipt from HTML or CI.
4. Revert this PR if a real intake regression is observed.

GSC Wizard was subscription-blocked on 2026-10-24; no fresh ranking, indexing or conversion claim is made.
