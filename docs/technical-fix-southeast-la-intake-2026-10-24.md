# VGM technical customer-intake correction — Southeast Los Angeles County (2026-10-24)

## Source-verified gaps before the change
At main `2a3b2dbd866ef2668219c68f09ad0f79ac8e0d13`, existing Long Beach, Bellflower, Compton and South Gate general appliance pickup forms each had a required phone, ZIP, and the approved Formspree POST endpoint but lacked a **static** optional paid-removal quote choice. The global customer-routing script can inject a quote selector with JavaScript, but a static selector ensures that customers can choose free-only or quote-interest even without JavaScript. A blank selection is **not** consent.

All four pages lacked complete ZIP autofill hints. Long Beach and Bellflower also lacked telephone autofill/keypad hints. Bellflower, Compton and South Gate lacked the hidden `service` attribution field, which can complicate identifying the requested service in the form submission.

## Narrow change
- Add one optional, blank-default `paid_removal_preference` selector to the existing form on each of the four pages, with `free_only` and `quote_ok` values. No charge, booking or price is authorized.
- Add missing `autocomplete=tel`, `inputmode=tel`, `autocomplete=postal-code`, and `inputmode=numeric` hints as applicable.
- Add `service=General major appliance pickup` hidden attribution to Bellflower, Compton and South Gate.
- Extend source-level regression checks for static quote choice, form endpoint/source/service, and phone/ZIP input hints.

## Guardrails and experiment ownership
The registry `data/seo-experiments.json` has running experiments on Long Beach (review gate 2026-10-16), Bellflower (2026-10-16) and Compton (2026-10-14). These edits are documented technical/customer-intake exceptions only, not speculative ranking/content experiments. They do **not** change titles, metadata, canonical, robots, H1, search copy, internal links, photographs, phone routing, qualification rules, Formspree endpoint or the other existing form fields. Daily SEO Ranking Countermove owns future ranking hypotheses; Website Technical Repair owns emergency breakage.

## Verification boundaries
A passing source audit or GitHub workflow does not establish that the production HTML is current, that Formspree delivered a message, that Google indexed the change, or that rankings improved. Verify the merged commit and GitHub Pages deployment separately. Do not submit a real lead to test delivery without authorization.
