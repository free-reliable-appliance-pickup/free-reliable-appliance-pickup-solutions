# VGM technical exception: Orange County optional quote consent (2026-10-23)

Baseline main: `878264cac1379b5dcf0f695f84feba6fdad96c27`. Existing Anaheim and Irvine general appliance pickup forms have the approved Formspree action, required phone, city-specific `source_page`, and `service`, but no static `paid_removal_preference` control. Neither page loads `assets/paid-removal-choice.js`, so the approved free-first / optional paid quote preference is unavailable to these customers. This is a verified customer-intake omission, not a ranking hypothesis.

Minimal correction: insert one optional blank-default choice with `free_only` and `quote_ok` on each existing form; add both pages to the static paid-quote regression guard. No form action, phone, policy, imagery, canonical, indexability, SEO copy, or ranking variables change. No payment or booking is performed.

SEO gate: `data/seo-experiments.json` still marks Anaheim's 2026-10-04 people-first simplification and California anti-template cleanup as running, with earliest review 2026-10-14. This narrow factual customer-intake exception does not change the protected title, body content outside the form, internal links, schema, canonical or images. Daily SEO Ranking Countermove owns evaluation; Website Technical Repair owns emergency failures.

Validation: run `python3 scripts/audit-sfv-paid-quote-static.py`, `python3 scripts/audit-priority-pickup-forms.py`, and `python3 scripts/audit-priority-intake-contract.py`; require green GitHub checks before merge, then confirm deployed HTML independently. Actual Formspree delivery requires a separately authorized live test.

Rollback: revert the isolated PR; do not change the experiment registry's ranking decisions.
