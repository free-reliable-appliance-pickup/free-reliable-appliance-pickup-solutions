# Verified Gold Model — SGV specialty request quote-consent consistency (2026-10-24)

## Verified current-source issue
At the connected GitHub `main` baseline on October 24, four existing specialty pickup request pages had approved POST forms, required telephone numbers, and source-page attribution but lacked the static optional paid-removal quote selection already offered on the corresponding general city pages:

- `/pasadena-refrigerator-pickup/`
- `/claremont-washer-dryer-pickup/`
- `/san-dimas-washer-dryer-pickup/`
- `/la-verne-washer-dryer-pickup/`

This is an intake-consistency defect. It is not evidence that customers were unable to submit forms or that search performance changed.

## Narrow technical exception
On each original form, append **one optional blank-default** `paid_removal_preference` selector immediately before the submit button. Values: `""` (no choice), `free_only` (no paid quote), and `quote_ok` (quote consideration only). Make clear that requesting a quote is not a booking, guaranteed service, payment, or authorization to charge. Do not alter previously required fields, endpoint, attribution, phone, qualification, canonical, metadata, copy, photos, schema, internal links, or indexing.

Expand the no-JavaScript static-consent audit to cover these four pages, including its positive/negative fixtures. The current SEO experiment protections continue. This is not a new ranking experiment; do not rewrite ranking copy while experiments remain running.

## Release checks and proof requirements
- Run `python3 scripts/audit-sfv-paid-quote-static.py`, applicable forms/phones CI, SEO Experiment Guard, and other required checks against the **exact** PR head.
- Merge only with passing required checks and no concurrent conflict; independently verify GitHub Pages deployment and the fresh public HTML of all four pages.
- An HTML/CI pass does not prove actual Formspree inbox delivery, a customer inquiry, link acquisition, or better organic ranking. Keep those measures separate.

Rollback: revert this narrow PR if a verified customer-intake regression arises.
