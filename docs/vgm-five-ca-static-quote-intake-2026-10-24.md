# VGM technical exception: five California customer forms — 2026-10-24

## Verified defects on main before changes
- San Marino and Sierra Madre general pickup forms lacked an HTML paid-removal quote preference and standard phone/ZIP mobile keypad/autofill hints.
- Buena Park, Yorba Linda and Mission Viejo general pickup forms lacked an HTML paid-removal quote preference. They already had the relevant phone/ZIP mobile hints.
- All five forms already posted to the approved Formspree endpoint, carried source_page/service attribution, and used required phone and appliance/condition fields. Those contracts are preserved.
- Existing JavaScript can supply a quote choice; static HTML now preserves the **same optional preference when JavaScript is off**. The selector is blank by default, is not required, and does not book, charge or guarantee paid removal.
- No change to telephone routing, qualification rules, images, title/meta, canonical, structured data, page content, or links. No customer form submission was made.

## Overlapping SEO experiment gates
- San Marino CTR snippet, Sierra Madre foothill, Buena Park structure, Yorba Linda structure: prior review dates Oct 14–15; status still marked running. Mission Viejo belongs to the California anti-template test, with Oct 14 minimum gate. These are **technical customer-intake exceptions only**, not new speculative SEO experiments.
- Preserve search snippet and ranking variables. Daily SEO Ranking Countermove retains ranking experimentation; Website Technical Repair retains emergency breakage.

## Baseline and observation
- Connected GSC/SMEPost free settled window Oct 19–21, 2026 returned no page-level rows for these five URLs. This does **not** imply deindexing or zero ranking visibility outside the three-day window.
- Verify one static optional select with empty/free_only/quote_ok choices, one required phone, one approved POST form and preserved hidden attribution in source and CI.
- After merge, verify GitHub main SHA, GitHub Pages deployment and fresh public HTML separately. Do not claim actual Formspree inbox delivery without a consented end-to-end test.

## Rollback
Revert the narrow page markup and audit changes together if any affected form loses required inputs, duplicates the quote selector, or changes submission destination. Do not roll back unrelated work.
