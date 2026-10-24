# VGM technical/photo exception — Upland hero (2026-10-24)

## Verified presentation defect
Issue #360 documents Upland general pickup using `/seattle-group-appliances.webp`, which is also the live Seattle general-pickup hero. The current main branch and public Upland page were inspected. This is a duplicate-photo/rotation issue, **not** evidence of a Google penalty or changed search rankings.

## Replacement provenance and limits
Reused the existing repository asset `/home-six-appliance-garage.webp` (Git blob `146d92114e2adbba83f34de8159fcd9f10b0ddb2`), visually inspected on 2026-10-24. It shows six major household appliances lined up in a garage: two laundry machines, a range, a refrigerator, a stacked laundry center, and another refrigerator. Actual WebP dimensions: 1400 × 1120. It already appears on the homepage; it is not represented as a photograph taken in Upland. It was not used as the hero of the 15 priority city pages inspected in this audit. No new, synthetic, stock, collage or upscaled photograph was introduced.

## Narrow source change
In `upland-appliance-pickup/index.html`, replace all five references to the Seattle hero with the garage asset: image preload, Open Graph image, Twitter image, WebPage primaryImageOfPage and displayed hero image. Update neutral hero/OG alt text to describe what is actually visible, and correct displayed intrinsic dimensions. Preserve all other text, customer qualification and claims, contact number 909-375-6685, form endpoint/fields, canonical, robots, schema intent, navigation and links.

## SEO experiment separation
`data/seo-experiments.json` includes Upland in two running experiments with latest overlapping `evaluateNotBefore` 2026-10-14. This is a bounded visual truthfulness/rotation correction permitted as a documented technical exception; it is not a speculative ranking experiment. No claim is made about ranking, partner presence, conversion or email receipt. Daily SEO Ranking Countermove owns content/ranking experiments; Website Technical Repair owns emergency breakage.

## Verification and rollback
Review the exact five source references and intrinsic dimensions; run existing image audit, priority intake, routing, browser/mobile and SEO experiment checks before merge. After merge, verify main-branch source, Pages workflow and production HTML independently. The existing image audit may continue warning on *other* cross-city duplicates; do not suppress those warnings. Rollback by reverting this narrow PR if image loading, display, or test coverage regresses. The remaining photo mappings in issue #360 remain open for individually inspected replacements.
