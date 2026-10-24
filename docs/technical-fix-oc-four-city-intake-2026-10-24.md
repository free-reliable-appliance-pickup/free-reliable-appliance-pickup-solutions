# VGM verified technical exception: four Orange County customer-intake forms (2026-10-24)

## Baseline and observed defect

Inspected `main` at `77fbcac0f3340f333a38665baa12745b31caee49` and the existing general appliance request forms. Santa Ana and Lake Forest had the approved Formspree POST, required telephone and ZIP, and correct city-specific attribution, but **no static optional paid-removal quote preference**. Neither page loaded the paid-choice fallback script. Fullerton and Lake Forest had required `type="tel"` fields with `autocomplete="tel"` but no `inputmode="tel"`; Irvine's ZIP field had `inputmode="numeric"` but no `autocomplete="postal-code"`.

The source omissions are confirmed; they do not prove failed Formspree delivery, a mobile conversion change, or organic ranking loss. The approved optional quote preference asks only whether a customer might consider a **separate quote if free pickup is unavailable**. It does not promise a pickup, authorize payment, or book service.

## Bounded change and preserved behavior

- Santa Ana and Lake Forest: add one existing-standard, blank-default optional `paid_removal_preference` selector with `free_only` and `quote_ok` values inside the existing POST form, available without JavaScript.
- Fullerton and Lake Forest: add the missing telephone keypad hint.
- Irvine: add the missing ZIP autofill hint.
- Extend the existing static paid-quote and priority intake regression source audits to cover these exact pages.

Preserved without modification: all telephone numbers and `tel:` links, Formspree action, method, mandatory fields, city/state and service attribution, appliance eligibility and access policies, images, title/meta, canonical, robots, schema, ranking copy, internal links, sitemap, and routing files. **Westminster's existing page is Colorado, not an Orange County page; it is explicitly outside this scope.**

## Search experiment coordination

The authoritative `data/seo-experiments.json` records running experiments for Santa Ana (evaluate no earlier than Oct 14), Lake Forest and Fullerton (Oct 15), and Irvine through California anti-template work (Oct 14). This change is a logged customer-intake/mobile technical exception only, not a ranking test or a reset of any SEO gate. Daily SEO Ranking Countermove retains exclusive ranking experiment decisions; Website Technical Repair retains emergency breakage ownership. No experiment registry values are changed.

The available three-day finalized GSC page baseline (Oct 19–21) showed Santa Ana 3 impressions/0 clicks, Lake Forest 1/0, Fullerton 2/1, and no page-level row for Irvine. These are very small samples and are **not** an SEO performance verdict.

## Validation and rollback

Require the existing GitHub PR checks (especially SEO Experiment Guard, static paid-quote, priority intake, customer routing, and browser checks) to pass. After merge, independently confirm the resulting main source, GitHub Pages deployment, and fresh public HTML. Do not claim Formspree email receipt without an authorized end-to-end test. Revert the isolated PR if form behavior regresses. No live test submission or paid action is authorized.
