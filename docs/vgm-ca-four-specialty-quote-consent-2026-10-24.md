# VGM California specialty customer-intake consistency — 2026-10-24

Source baseline: `main` `0bc5c15f223065e37023ad085118cbbc996ad791`. Scope is four **existing** California specialty pickup forms:
- `/riverside-washer-dryer-pickup/`
- `/riverside-refrigerator-pickup/`
- `/anaheim-washer-dryer-pickup/`
- `/pomona-washer-dryer-pickup/`

## Source-confirmed defect
Each had exactly one approved `https://formspree.io/f/mvzeapzd` POST form with a required telephone field and static source-page attribution. Each lacked the optional static `paid_removal_preference` choice used by the approved general and specialty intake forms, so a no-JavaScript customer could not indicate free-only vs willingness to review a separate paid-removal quote. Three laundry forms also lacked `inputmode=tel` and ZIP autofill hints. This is a verified intake-consistency defect, not evidence of failed submissions or a ranking problem.

## Bounded repair and consent
One blank-default optional selector on each existing form, with `free_only` and `quote_ok` values, before the existing submit button; mobile keyboard/autofill hints on the three laundry forms. A quote request is not a booking, authorization to charge, guaranteed service, or a promise of free pickup. No changes to fee policy, Formspree destination, existing phone routing, acceptance criteria, image, canonical, robots, schema, page title, internal links or ranking copy.

## Experiment separation
Registry experiments still running: `2026-10-06-ie-laundry-template-concentration`, `2026-10-04-ontario-pomona-riverside-refrigerator-localization`, `2026-10-06-anaheim-laundry-structure-simplification`, and `2026-10-06-pomona-laundry-concentration`. Their speculative ranking changes remain exclusively with Daily SEO Ranking Countermove. This change uses the documented narrow customer-intake technical exception; no SEO experiment variable is edited. Emergency Website Technical Repair remains separate.

## Acceptance and limits
Run `python3 scripts/audit-sfv-paid-quote-static.py`, relevant phone/intake and SEO Experiment Guard workflows on the exact PR SHA. The static quote guard includes all four pages and checks one approved endpoint, required phone, source attribution, optional blank default, and explicit free-only/quote-consideration values; its positive/negative fixtures protect consent. Confirm merge, successful GitHub Pages deployment, and uncached public HTML independently. Actual Formspree email receipt requires a controlled end-to-end test and is **not** established by source checks. No rankings or lead improvement claimed.

Rollback: revert the scoped PR if a verified intake regression is observed.
