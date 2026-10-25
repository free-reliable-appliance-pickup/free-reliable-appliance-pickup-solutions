# VGM — Arcadia and Glendora laundry customer-intake consistency (2026-10-24)

## Evidence from connected GitHub main
At the pre-change source baseline, `/arcadia-washer-dryer-pickup/` and `/glendora-washer-dryer-pickup/` each had one Formspree POST to the approved endpoint, required telephone, condition and access fields, but lacked the optional static `paid_removal_preference` control present on approved nearby pickup pages. Glendora's laundry form also lacked both `source_page` and `service` hidden identifiers, making lead routing attribution less specific. The mobile phone and ZIP fields lacked standard autocomplete hints on both pages. No evidence of a failed real customer submission or Formspree inbox delivery is claimed.

## Minimal documented technical exception
Add one blank-default, non-required paid quote preference with values `free_only` and `quote_ok`, clear statement that a quote is not a booking or charge, and telephone/ZIP input hints. Add correct Glendora source/service hidden fields. Preserve existing form action, method, required fields, phone CTA, city coverage, qualification, hero images, canonical, title/meta, body copy, internal links and schema. No new city page or SEO rewrite.

These specialty URLs remain protected by running registry entries `2026-10-05-arcadia-laundry-intent-cleanup` and `2026-10-06-zero-visibility-laundry-structure-simplification`; this verified intake-only change is the registry policy's documented technical exception, **not** a speculative ranking experiment. Daily SEO Ranking Countermove retains ranking experiments and freeze gates; Website Technical Repair retains emergency breakage. Do not change experiment registry values for this repair.

## Required verification
1. Confirm only these two existing HTML forms and the static-consent audit changed, plus this record.
2. Run `python3 scripts/audit-sfv-paid-quote-static.py`, priority phone/form audits and SEO Experiment Guard on exact PR head; do not merge if required CI fails.
3. After merge verify the exact main commit, successful Pages deployment, and fresh public HTML for both URLs separately.
4. Do not claim actual Formspree inbox delivery, increased leads, ranking gains, or a newly verified partner without independent evidence.

Rollback: revert the PR if a customer-intake regression is independently verified. Preserve all protected SEO variables.
