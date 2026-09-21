# California SEO Gold Standard

California is the source-of-truth model for future state, regional, county, city, and washer/dryer service pages.

## Core rule

Do not mass-copy a thin city template. New state rollouts must inherit the strongest California structure while keeping the main content genuinely useful and specific to the real market, appliance intent, access conditions, and route model.

## Technical SEO requirements

- Indexable pages use `index, follow, max-image-preview:large`.
- Exactly one self-referencing canonical URL.
- Page must be present in `sitemap.xml` with a current `lastmod` after meaningful edits.
- Unique title, meta description, H1, and useful H2 structure.
- No repeated exact H2 headings on the same page.
- WebPage, Service, and BreadcrumbList structured data where appropriate.
- Internal links connect city -> regional/county -> state and appliance-specific guides.
- The request form and customer routing must remain functional.
- Do not create separate indexable pages that only swap a city name while leaving the useful body substantially the same.

## Local usefulness requirements

Each primary location page should explain real differences that can change a pickup decision, such as:

- exact city/ZIP or regional route context;
- apartment, condo, HOA, alley, gate, stairs, elevator, driveway, loading, or parking access where locally relevant;
- appliance condition/testing details;
- refrigerator/freezer cooling status;
- washer fill/wash/drain/spin and dryer tumble/heat;
- property-manager or multi-appliance situations where useful;
- a legitimate municipal/recycling alternative when an authoritative local option exists;
- nearby or parent service-area links that help users choose the correct page.

Regional hubs should organize real route clusters and link to important city pages. Smaller communities should not automatically receive thin standalone pages.

## Search-intent rule

Use finalized Google Search Console data to prioritize improvements. Protect pages already earning impressions/clicks and strengthen the specific intent Google is showing rather than rewriting every title at once.

Examples from the California model include dedicated, useful sections for refrigerator, washer/dryer, appliance-removal, access, or disposal intent only when they add real information.

## Image standard

Washer/dryer benchmark pages use the original full-resolution real photo library under:

`/assets/laundry/original-user-heroes/`

Hero URLs should keep the `original-fullres=` cache marker and the current sharp shared CSS. Do not substitute tiny compressed hero files or sprite crops for these benchmark pages.

Use real appliance photos where appropriate and keep the previously approved city/region photo assignment unless there is a documented reason to change it.

## Conversion standard

- Clear qualification language: free pickup is reviewed, not automatically guaranteed.
- Strong CTA near the top.
- Call/text options where assigned.
- Request form stays on the local page.
- Request asks for condition, exact address/ZIP, floor/stairs/access, and appliance details.
- Photos/testing guidance is visible before submission.
- Do not promise service outside actual qualification and route rules.

## Quality gate before copying to another state

A California page can be used as a rollout model only after it passes the repository gold-standard audits.

General appliance benchmark:
`data/california-seo-model-pages.txt`

Laundry benchmark:
`data/california-laundry-gold-standard-pages.txt`

Automated audits:
`.github/workflows/audit-california-seo-model.yml`
`.github/workflows/audit-california-laundry-gold-standard.yml`

If an older page conflicts with this document, use the strongest currently audited California page as the model rather than the older page.
