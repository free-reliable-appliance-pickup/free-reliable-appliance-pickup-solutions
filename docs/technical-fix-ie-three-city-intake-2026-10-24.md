# VGM technical intake correction — Corona, Moreno Valley, San Bernardino (2026-10-24)

## Verified source evidence
On main `b057c8438800b1dc3b1a71738d90bdc7e81f1e9a`, each existing general appliance pickup page has exactly one approved Formspree POST, required phone and ZIP fields, and correct source/service attribution, but lacks a **static** optional paid-removal quote selector. The shared JavaScript may inject a selector, but a no-JavaScript visitor has no equivalent choice. Corona and Moreno Valley lack phone autofill/keypad hints and ZIP autofill; San Bernardino lacks phone keypad and ZIP keypad hints.

## Narrow, reversible technical exception
- Add one blank-default, optional `paid_removal_preference` select to each existing form with only `free_only` and `quote_ok` affirmative values. Blank is not consent. A quote is not a booking, payment or charge.
- Add missing telephone and ZIP mobile keyboard/autofill hints without changing field requirements, options or form validation.
- Extend the existing static quote audit and priority intake regression checks. Include Corona and Moreno Valley in the latter's inspected city set.
- Preserve current telephone links, approved Formspree action, hidden source/service fields, appliance acceptance rules, all photos, canonical, metadata, schema, page copy, and internal links.

## Ownership and freeze gates
The `data/seo-experiments.json` California anti-template experiment includes Corona and San Bernardino, is marked running and has an `evaluateNotBefore` date of 2026-10-14. Moreno Valley laundry has a separate protected experiment (2026-10-16) and is **not** edited. This PR is a documented factual customer-intake technical exception, not a speculative ranking/content experiment. Daily SEO Ranking Countermove owns ranking tests; Website Technical Repair owns emergency breakage.

## Validation and rollback
Run both regression audits, all repository CI including the SEO Experiment Guard, verify the merged commit and GitHub Pages deployment, and independently retrieve production HTML when possible. Formspree delivery, rankings, indexing, and real customer lead receipt are **not** established by CI. Roll back only these three form controls and related audit fixtures if necessary; do not revert unrelated ranking experiments.
