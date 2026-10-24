# VGM: California regional paid-quote preference — October 24, 2026

## Verified pre-change gap
Source inspection on `main` found one approved Formspree POST each at `/inland-empire-appliance-pickup/` and `/san-gabriel-valley-appliance-pickup/`, but neither form had a pre-rendered optional `paid_removal_preference`. Shared JavaScript injects it only when scripts run. This is a no-JavaScript customer consent and lead-qualification gap, not a ranking or indexing defect.

## Minimal technical correction
- Add the same blank-default, optional `free_only` / `quote_ok` choice used on existing California owner pages.
- Inform customers that free pickup is reviewed first and a paid quote is neither a booking nor an automatic charge.
- SGV: correct the telephone field to `type="tel"` with a mobile keypad hint, add ZIP numeric keypad hint, and include the already-standard hidden `service` attribution.
- Register both pages in `scripts/audit-sfv-paid-quote-static.py`, which checks exact Formspree endpoint, required phone, source-page attribution, and consent default/option values.

## SEO experiment isolation and rollback
The regional anti-template cleanup experiment's `evaluateNotBefore` gate was 2026-10-14. This fix changes no title, H1, canonical, robots, schema, copy, image, city directories, phone number, eligibility rule, or internal link ownership. Ranking experiments remain with Daily SEO Ranking Countermove and urgent technical issues with Website Technical Repair. Revert the PR if intake validation or submitted values regress.

## Verification limits
Required before merge: green repository CI including SEO Experiment Guard and static quote regression, then confirm main and GitHub Pages deployed public HTML. No test submission has been sent to Formspree, and no Google ranking improvement or lead conversion has been measured.