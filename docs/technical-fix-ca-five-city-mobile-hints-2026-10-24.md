# VGM California mobile intake hints — 2026-10-24

## Verified source gap
At main commit `657cb9a6825a6e904f0ab6356d80f2687297c458`, five existing general-appliance request forms use the approved Formspree POST, required telephone/ZIP, source/service attribution and optional paid-removal quote preference. Riverside and Anaheim ZIP inputs omit `autocomplete="postal-code"`. Ontario, Rancho Cucamonga and Fontana telephone inputs omit `inputmode="tel"`. These are browser usability inconsistencies, not proven lead-delivery failures.

## Bounded technical correction
Add only the missing HTML autofill/keypad hints on those five existing forms; extend `scripts/audit-priority-intake-contract.py` with these five protected pages and two positive/two negative fixture checks. Preserve all Formspree actions, required fields, values, hidden provenance, existing local telephone links, appliance eligibility, quote consent, photographs, metadata, canonical, schema, internal links and ranking copy.

## Freeze and responsibility
`data/seo-experiments.json` marks the Inland Empire owner stabilization, California anti-template cleanup and Anaheim people-first experiments as running, with `evaluateNotBefore: 2026-10-14`. Passing that date is not permission for this task to change speculative ranking variables. This documented mobile usability correction is a narrow technical exception. Daily SEO Ranking Countermove owns ranking/content experiments and Website Technical Repair owns emergency breakage.

## Validation and rollback
Run the intake regression self-test and source checks plus GitHub PR checks, especially the SEO Experiment Guard. Confirm merge and Pages publishing independently. Actual browser autofill behavior, Formspree receipt, indexing and ranking improvement cannot be inferred from passing source tests. Roll back this isolated PR if the fields regress.
