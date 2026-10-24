# VGM California phone keypad hints — 2026-10-24

## Verified defect and scope
At main commit `3d0f188c713881363becb1f5815ae23aabc53d0b`, the five existing general-appliance pickup forms for Chino, Chino Hills, Pomona, Claremont and Redlands each had exactly one required `type="tel"` phone input with `autocomplete="tel"`, but no `inputmode="tel"`. Each already had one approved Formspree POST, required ZIP with postal-code autofill and numeric keypad, source/service attribution and optional paid-removal quote preference. This is a minor browser-usability inconsistency, not a verified lead-delivery outage.

## Bounded technical exception
Add only `inputmode="tel"` to each existing required phone input. Expand `scripts/audit-priority-intake-contract.py` mobile-hint guard for exactly these five pages and add a passing and failing Chino fixture. Do not change form endpoints, phone links, required fields, eligibility, paid-quote choice, local service promises, images, metadata, schema, canonicals, internal links or ranking content.

## Experiment and responsibility gates
Read `data/seo-experiments.json` on main. Chino, Pomona, Claremont and Redlands remain associated with running SEO experiments whose review gates were Oct 13–15. The anti-template cleanup also lists Chino Hills. Their ranking hypotheses and all content variables remain untouched. This is a documented technical browser-hint exception, not a new experiment. Daily SEO Ranking Countermove retains speculative ranking/content experiments; Website Technical Repair retains emergency breakage. The protected San Fernando Valley hero experiment through Nov 6 is untouched.

## Validation, deployment and rollback
Check the exact HTML one-field diff and existing intake contract, run `python3 scripts/audit-priority-intake-contract.py --self-test` and the full source audit, and require green GitHub checks including SEO Experiment Guard and phone routing before merge. Verify the main commit, Pages workflow and fresh production HTML separately. Neither CI nor publishing proves actual Formspree receipt or improved rankings. Roll back by reverting this isolated PR if a regression is found.
