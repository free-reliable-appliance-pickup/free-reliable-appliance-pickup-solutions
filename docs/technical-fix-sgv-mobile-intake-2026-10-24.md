# VGM technical exception — SGV mobile intake hints (2026-10-24)

## Confirmed source issue
Main-branch inspection identified incomplete mobile keyboard/autofill hints in the general-appliance pickup request forms for Pasadena, Arcadia, San Dimas and La Verne. Each required phone input lacked `inputmode="tel"`; Arcadia additionally lacked `autocomplete="tel"`. All four ZIP inputs lacked `autocomplete="postal-code"`, though they already had `inputmode="numeric"`. This is a usability consistency defect, **not** evidence of lost leads.

## Scope and safeguards
Only add missing standard HTML input hints to the existing phone and ZIP fields on:
- `/pasadena-appliance-pickup/`
- `/arcadia-appliance-pickup/`
- `/san-dimas-appliance-pickup/`
- `/la-verne-appliance-pickup/`

Preserve the Formspree action, hidden service/source attribution, required fields, existing telephone routing, optional paid-removal consent, eligibility rules, photographs, metadata, canonicals, content, and navigation. No customer form is submitted. Extend `scripts/audit-priority-intake-contract.py` to enforce the hints on these pages with positive and negative fixtures.

## Experiment ownership
The registry `data/seo-experiments.json` lists active running experiments involving these pages, including California anti-template cleanup (latest gate at least 2026-10-14). This narrow browser-input fix is documented as a technical exception, not a new ranking/content experiment. Daily SEO Ranking Countermove owns any discretionary ranking changes; Website Technical Repair owns emergencies. The date of a gate passing is not evidence that a ranking experiment is complete.

## Verification and rollback
Require the priority intake contract, experiment guard, phone routing and relevant browser/mobile tests to pass on the PR head. After merge, separately verify the exact main commit, GitHub Pages workflow and production markup if available. Formspree receipt, indexing, organic rankings and lead conversion are **not** proven by source checks or deployment. Revert this isolated PR if the input behavior or lead form is impaired. No photo changes; photo issue #360 remains open.
