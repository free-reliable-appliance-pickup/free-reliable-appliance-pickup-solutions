# VGM California telephone keypad hints — 2026-10-24

## Source-confirmed defect
On main `a2ae8f97c5f78d22ec5e60cb68084ff7d9c754ce`, the Upland, Montclair and Huntington Beach existing general-appliance pickup forms each had exactly one required `type="tel" name="phone"` input with `autocomplete="tel"`, but no `inputmode="tel"`. Their existing ZIP inputs already had `autocomplete="postal-code" inputmode="numeric"`. Each form already had the approved Formspree POST endpoint, `source_page` and `service` hidden fields and optional static paid-removal quote preference. This is a small mobile keyboard hint inconsistency, not proof of a lead outage.

## Narrow technical exception
Add only `inputmode="tel"` to the three existing telephone inputs; expand the existing mobile-input regression guard for exactly these pages and add passing/failing Upland fixtures. Do not modify page copy, SEO intent, phones/tel links, photos, Formspree routing, field requiredness, paid-quote consent, pickup eligibility, canonical, schema, metadata, or navigation.

## Freeze ownership
Read `data/seo-experiments.json` updated October 17: Upland and Montclair are listed in the California anti-template cleanup (review gate Oct 14), Upland in IE owner stabilization (Oct 14), and Huntington Beach in anti-template cleanup (Oct 14). These observations remain marked running; this change touches no ranking variables. The San Fernando Valley hero experiment with November 6 protection is untouched. Daily SEO Ranking Countermove owns speculative experiments; Website Technical Repair owns emergency breakage.

## Test and deployment gates
Require `python3 scripts/audit-priority-intake-contract.py --self-test` and its full source audit, plus all relevant GitHub PR checks including SEO Experiment Guard and phone-routing checks. Inspect the exact diff, confirm merge SHA and GitHub Pages publishing, then independently retrieve public form HTML. Passing CI or Pages does not prove actual Formspree email delivery, indexing or rankings. Roll back by reverting the isolated PR if a regression is found.
