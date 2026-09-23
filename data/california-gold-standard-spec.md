# California SEO Gold Standard

California is the source-of-truth model for future state, regional, county, city, and washer/dryer service pages.

## Core rule

Do not mass-copy a thin city template. New state rollouts must inherit the strongest California structure while keeping the main content genuinely useful and specific to the real market, appliance intent, access conditions, and route model.

## Technical SEO requirements

- Indexable pages use `index, follow, max-image-preview:large`.
- Exactly one self-referencing canonical URL.
- Exactly one H1 on priority gold-standard city pages.
- Page must be present in `sitemap.xml` with a current `lastmod` after meaningful edits.
- Unique title, meta description, H1, and useful H2 structure.
- Keep priority-city meta descriptions concise enough to avoid unnecessary truncation; the audit warns above 165 characters.
- No repeated exact H2 headings on the same page.
- WebPage, Service, FAQPage, and BreadcrumbList structured data on priority gold-standard city pages.
- Internal links connect city -> regional/county -> state and appliance-specific guides.
- Every priority gold-standard city page links to the refrigerator, washer/dryer, freezer, and stove/oven authority guides.
- Priority gold-standard city pages maintain at least 20 useful internal links so they are integrated into the site rather than isolated doorway pages.
- Priority gold-standard city pages include at least one legitimate external local/official reference.
- The request form and customer routing must remain functional.
- Do not create separate indexable pages that only swap a city name while leaving the useful body substantially the same.

## Full major-appliance breadth

General appliance-pickup pages in the California gold-standard model must visibly support the five core appliance groups: **washers, dryers, refrigerators, freezers, and stoves/ranges/ovens**. Do not let a general city or regional page drift into washer/dryer-only content.

- Keep the full appliance breadth visible near the top of priority general pickup pages.
- Link general pages to the washer/dryer, refrigerator, freezer, and stove/range authority guides.
- Link those appliance authority guides back to the strongest regional California hubs so authority flows both directions.
- Use appliance-specific city pages only when they add genuinely distinct testing, access, routing, or demand information; do not mass-create thin city × appliance doorway pages.
- Protect a general city page as the primary destination for broad appliance-pickup/removal intent while specialized laundry pages serve washer/dryer-specific intent.

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

Priority city heroes use a real local appliance photo, `fetchpriority="high"`, meaningful alt text, and the real intrinsic `width` and `height` of the source image to protect layout stability. Preserve the original full-resolution file rather than creating a blurry replacement.

Use the best-looking image that matches the page intent: nicest stove/range for stove pages, nicest refrigerator for refrigerator pages, nicest matching washer/dryer set for laundry pages, and strongest mixed-appliance group photos for general appliance-pickup pages. Avoid repeatedly using the same weak photo across priority pages when better approved originals are available.

Use real appliance photos where appropriate and keep the previously approved city/region photo assignment unless there is a documented reason to change it.

## Conversion standard

- Clear qualification language: free pickup is reviewed, not automatically guaranteed.
- Strong CTA near the top.
- Call/text options where assigned.
- Request form stays on the local page.
- Request asks for condition, exact address/ZIP, floor/stairs/access, and appliance details.
- Photos/testing guidance is visible before submission.
- Do not promise service outside actual qualification and route rules.
- Do not copy competitor claims such as "same day," "any condition," "all appliances," or "100% free" unless they are actually true under the site's published qualification and route rules.

## Quality gate before copying to another state

A California page can be used as a rollout model only after it passes the repository gold-standard audits.

General appliance benchmark:
`data/california-seo-model-pages.txt`

Priority California city model:
`data/california-priority-gold-city-pages.txt`

The priority list is the stricter source model for future nationwide city rollouts. These pages must pass the extra category-authority, official-reference, internal-link-depth, schema, H1, and hero-image checks in the California audit.

Laundry benchmark:
`data/california-laundry-gold-standard-pages.txt`

Automated audits:
`.github/workflows/audit-california-seo-model.yml`
`.github/workflows/audit-california-laundry-gold-standard.yml`

If an older page conflicts with this document, use the strongest currently audited California page as the model rather than the older page.
