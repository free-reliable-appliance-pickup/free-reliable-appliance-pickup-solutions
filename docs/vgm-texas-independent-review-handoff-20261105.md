# VGM Texas launch — independent review handoff (NOT an approval)

**Snapshot:** PR [#807](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/pull/807) code HEAD `369107186f31cf86f454bddf3b80f58f31b96787` at the time this handoff was prepared (2026-11-05). After any further commit, inspect the new exact head and rerun all checks; this manifest does not authorize deployment.

## Customer and market scope

- **89 requested Texas cities × 5 distinct pages = 445** Texas city/category pickup inquiry pages in repository source (some pre-existing), plus the statewide request hub. These are not 445 independently verified pickup routes.
- Texas city/category pilots are **`noindex, follow`** until independently confirmed pickup coverage and original useful content exist. Texas statewide customer hub stays indexable.
- One existing customer Formspree action (`https://formspree.io/f/mvzeapzd`) per request page. No new paid form, recruitment or fake local office.
- Texas statewide page uses title **Free Appliance Pickup Texas | Request Eligibility Review** and one representative garage appliance photo, not a fabricated completed Texas pickup.
- The 89-city selector prefills the existing customer form. The user explicitly instructed that **partner recruitment is not active**: the public statewide Texas hub has no partner/recruiting text; the shared customer form reports `request-only` / `NATIONAL_INTAKE` for markets with internal recruiting status.
- Existing California and Oregon pages, regional phones, photo types and source-attribution fields must remain intact.

## Why the normal PR patch is incomplete

At snapshot `369107186f31cf86f454bddf3b80f58f31b96787`, the GitHub PR API listed **223 changed files**. Exactly **199** exposed textual `patch` contents; **24** changed paths had no patch text in the API response. A green CI result or an abbreviated patch is **not independent review of these files**. The missing paths are:

- [`huntsville-washer-dryer-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/huntsville-washer-dryer-pickup/index.html)
- [`keller-freezer-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/keller-freezer-pickup/index.html)
- [`keller-refrigerator-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/keller-refrigerator-pickup/index.html)
- [`keller-stove-oven-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/keller-stove-oven-pickup/index.html)
- [`keller-washer-dryer-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/keller-washer-dryer-pickup/index.html)
- [`kyle-freezer-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/kyle-freezer-pickup/index.html)
- [`kyle-refrigerator-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/kyle-refrigerator-pickup/index.html)
- [`kyle-stove-oven-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/kyle-stove-oven-pickup/index.html)
- [`kyle-washer-dryer-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/kyle-washer-dryer-pickup/index.html)
- [`lancaster-tx-freezer-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/lancaster-tx-freezer-pickup/index.html)
- [`lancaster-tx-refrigerator-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/lancaster-tx-refrigerator-pickup/index.html)
- [`temple-stove-oven-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/temple-stove-oven-pickup/index.html)
- [`temple-washer-dryer-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/temple-washer-dryer-pickup/index.html)
- [`texas-appliance-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/texas-appliance-pickup/index.html)
- [`the-colony-freezer-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/the-colony-freezer-pickup/index.html)
- [`the-colony-refrigerator-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/the-colony-refrigerator-pickup/index.html)
- [`the-colony-stove-oven-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/the-colony-stove-oven-pickup/index.html)
- [`the-colony-washer-dryer-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/the-colony-washer-dryer-pickup/index.html)
- [`tyler-freezer-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/tyler-freezer-pickup/index.html)
- [`tyler-refrigerator-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/tyler-refrigerator-pickup/index.html)
- [`tyler-stove-oven-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/tyler-stove-oven-pickup/index.html)
- [`tyler-washer-dryer-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/tyler-washer-dryer-pickup/index.html)
- [`victoria-freezer-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/victoria-freezer-pickup/index.html)
- [`victoria-refrigerator-pickup/index.html`](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/blob/369107186f31cf86f454bddf3b80f58f31b96787/victoria-refrigerator-pickup/index.html)

**Review procedure:** Independent reviewer should open the entire file for each of the 24 paths above, compare it against the `main` counterpart when present, and inspect the 199 other changed files in the PR. Fetch whole contents for any other truncated or minified patch rather than marking it reviewed. The absence of a patch does **not** mean the file was unchanged.

## Mandatory checks for independent reviewer (record actual observations)

1. **Source and security:** inspect `texas-appliance-pickup/index.html`, `assets/customer-routing.js`, `assets/texas-city-shortcut.js`, `data/market-routing.json`, plus form/audit scripts, every changed page and 24 patch-omitted paths. No external payloads or secret values committed; Formspree action and source tracking stable.
2. **Authenticity and image QA:** exactly one real applicable non-brand appliance photograph per page; avoid AI-created proof or made-up Texas service photos, image/category mismatches, duplicated heroes, and broken relative paths.
3. **Customer only:** no recruiting CTA on Texas statewide form; sample Houston, Dallas, Austin, San Antonio, Beaumont, Lancaster, San Marcos, and unlisted-city submissions. California priority phone mapping (909/310), Oregon/WA (503) and CO (720) must remain correct; no recruiting field values in customer submissions.
4. **SEO/index policy:** 445 Texas city/category pages stay `noindex` and are not automatically inserted into the indexable sitemap. Statewide hub has a self-canonical, accurate title/description/schema and no misleading claim of universal free pickup.
5. **Actual use:** review desktop + mobile city-selector behavior, only one form, required fields, stairs and condition review, accessibility, and actual Formspree delivery **only with explicit permission to send a test**; CI mock tests are not inbox receipt.
6. **Deployment verification:** after separate sign-off and authorized merge, verify the public Texas hub no longer shows a partner-recruitment invitation and redirects to the correct customer intake. Verify live robots/canonical, pages, images, and Search Console independently.
7. **Release gating:** see [#705](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/issues/705). The missing `OPENROUTER_API_KEY` means the existing automated independent reviewer is **not configured**. A real independent human review is a proposed no-fee alternative only if the repository owner explicitly authorizes that process. Do not disable/skip review or treat ChatGPT's or CI's own checks as an independent approval.

## Evidence ledger

- Snapshot `369107186f31cf86f454bddf3b80f58f31b96787`: **36/36** GitHub Actions completed successfully, including read-only Playwright browser smoke, customer routing, Texas 89-city coverage, photo/SEO/index audits, metadata and performance checks. **No independent reviewer appeared in the list of 36 checks.**
- [Public Texas hub](https://freereliableappliancepickup.com/texas-appliance-pickup/) still showed the old recruiting invitation on 2026-11-05 because code had **not been merged or deployed**.
- **Independent reviewer, review SHA, timestamp, and decision: PENDING.**
- **Owner release approval and GitHub merge: PENDING.**
- **Post-release form receipt, Google indexing and rankings: NOT VERIFIED.**

*This handoff records evidence and remaining work; it is not a substitute for independent review, approval or actual pickup-coverage verification.*
