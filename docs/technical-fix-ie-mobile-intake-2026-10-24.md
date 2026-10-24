# VGM technical exception — IE mobile intake hints (2026-10-24)

## Verified defect and scope
Source inspection on main found Bloomington, Colton and Highland general-appliance pickup forms each use a required telephone input without `autocomplete="tel"` or `inputmode="tel"`, and a required ZIP input without `autocomplete="postal-code"` or `inputmode="numeric"`. This is a mobile keyboard/autofill usability inconsistency, not evidence that a lead was lost or delivery failed.

## Narrow reversible correction
Add only those four standard browser hints to the existing telephone and ZIP fields on those three pages. Preserve field names, required states, Formspree action, hidden city/source/service attribution, phone call/text routing, eligibility, paid quote consent, image references, page metadata and content. No live form submission or payment is authorized. Extend `scripts/audit-priority-intake-contract.py` to cover Colton and Highland and guard the three IE forms' mobile hints, with positive and negative fixtures.

## SEO and emergency ownership
`data/seo-experiments.json` contains running experiments for Bloomington (people-first simplification), Colton (people-first simplification) and Highland (California anti-template cleanup), each with `evaluateNotBefore: 2026-10-14`. The date passing does not authorize speculative ranking/content changes; Daily SEO Ranking Countermove retains ownership of experiment decisions. This is a documented bounded technical exception for verified mobile markup only. Website Technical Repair retains exclusive responsibility for emergency breakage.

## Verification and rollback
Require the applicable pull-request checks, especially priority intake, mobile/browser, phone routing and SEO experiment guard. Verify main-branch files and GitHub Pages deployment separately after merge. Neither source checks nor a successful deployment prove customer email receipt or improved Google rankings. Roll back by reverting the isolated PR if browser behavior or lead intake regresses. No photos were changed; duplicate-photo issue #360 remains open for visual inspection.
