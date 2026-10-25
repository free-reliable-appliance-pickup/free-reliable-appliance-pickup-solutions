# VGM: Fontana specialty pickup forms — static optional paid quote (2026-10-24)

## Source-proven defect
All four existing Fontana appliance-category forms used `POST https://formspree.io/f/mvzeapzd` with required phone and service-specific source attribution, but had **no static `paid_removal_preference` selector**:
- `fontana-stove-oven-pickup/index.html`
- `fontana-refrigerator-pickup/index.html`
- `fontana-freezer-pickup/index.html`
- `fontana-washer-dryer-pickup/index.html`

Existing Fontana general-owner page already exposes the approved optional free-only versus paid-removal quote choice, creating an inconsistent experience for customers starting directly on a specialty page.

## Exact repair
Insert one non-required static select in each of those four existing forms, with ordered values `""`, `free_only`, `quote_ok`. The blank default does not opt the customer into paid quoting; choosing `free_only` expressly declines a quote. The message explains that a quote is neither a booking nor a charge; price approval is required. Add all four files to the already established static consent audit `scripts/audit-sfv-paid-quote-static.py`.

No new route or page. Preserve four Formspree actions/methods, source_page, city, state, appliance/service, existing required contact/condition/address details, local 909-375-6685 phone, accepted-appliance criteria, original images, headers, meta descriptions, canonical, robots and structured data. This is customer-consent and conversion hygiene, **not evidence of improved organic ranking**.

## Verification gate
1. All automated tests including static paid quote guard, priority forms/phones, SEO experiment guard, schema and image audit must pass.
2. Merge reviewable branch PR.
3. Verify GitHub Pages deployment completed successfully; if superseded by a later main commit, verify the newer build contains the fix.
4. Independently fetch each public Formspree form and verify its optional values, single selector, required phone, submission endpoint, the unchanged canonical and customer-visible consent language.
5. Do not submit actual test personal information through Formspree or claim receipt unless an authorized end-to-end test is executed.

## Rollback
If contract checks fail or paid consent becomes preselected, revert the four selector insertions and audit mapping, leaving all original source values in place.

## Outcome attribution
Measure specialty-page form submissions and qualified leads separately; no inference of rank or new customers from CI alone.
