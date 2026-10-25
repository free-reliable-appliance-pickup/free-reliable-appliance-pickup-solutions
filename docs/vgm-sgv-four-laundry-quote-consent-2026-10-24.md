# VGM — SGV laundry no-JavaScript quote consent (2026-10-24)

## Verified source defects
Current main branch lacked a native `paid_removal_preference` selector in the existing washer/dryer forms for Pasadena, Alhambra, La Puente and Baldwin Park. Without JavaScript, customers could not choose free-only versus permission to consider a separate paid-removal quote. These four forms already submit to the approved Formspree endpoint and require a telephone number; do not infer email receipt from HTML inspection.

## Narrow technical exception to overlapping SEO experiments
The running `2026-10-06-zero-visibility-laundry-structure-simplification`, `2026-10-06-alhambra-laundry-concentration`, and `2026-10-06-sgv-zero-visibility-laundry-simplification` experiments have passed their earliest evaluation dates (Oct 16), but remain running pending finalized GSC evidence. This change is a factual/customer-intake technical correction, not a ranking experiment: no SEO title, meta description, canonical, schema, internal links, ranking body copy, photo, eligibility or owner URL changes.

Each existing HTML form receives a blank-default optional `paid_removal_preference` with `free_only` and `quote_ok` values, a plain-language no-charge/no-booking explanation, and a hidden `service` attribution value. Existing `source_page`, Formspree action, phone routing and required fields remain unchanged. Missing phone and ZIP mobile input hints are added only where absent. Extend `scripts/audit-sfv-paid-quote-static.py` for the four pages.

## Verification and rollback
Run `python3 scripts/audit-sfv-paid-quote-static.py`, relevant California intake/phone tests and the SEO Experiment Guard on the exact PR head. Review the diff to ensure no experiment variables changed. Merge only after passing CI, then separately verify the deployed production HTML and GitHub Pages workflow. Actual Formspree receipt requires a separately authorized end-to-end test. Rollback: revert the narrow HTML/script/doc commits. No rankings, partner coverage or paid service availability is asserted.
