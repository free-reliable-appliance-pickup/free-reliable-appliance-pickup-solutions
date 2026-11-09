# Illinois TTG FastTrack — operational readiness ledger

## Published staging (9 November 2026)

- Illinois site: 61 staged request-only pages, including a statewide hub and 12 city guides, each with four appliance-specific request pages (48 categories).
- Relevant releases: #1002 (intake routing and production checks), #1003 (category batch), #1004 (gas/electric stove intake), #1005 (photo review clarity).
- All 61 staged pages must remain noindex/follow until verified city-level fulfillment supports indexability. No Illinois local operator, coverage guarantee or inbox receipt is claimed here.

## Repeatable release steps

1. Stage a state manifest at `data/ttg-state-batches/XX.json`, with truthful, local pickup content and a separate request form.
2. Run existing offline form/SEO QA and read-only public smoke tests. They establish website structure, not live pickup availability.
3. Create a separate operational record at `data/ttg-release-readiness/XX.json`. Do not store operator/customer PII in this public repository. Include only a reference to a restricted evidence record.
4. Test the Formspree endpoint using the owner's real, consented, clearly labeled test request; confirm actual receipt in the owner's inbox. The automated gate must **never** submit fake leads.
5. Verify accepting operators, exact served city/ZIP areas, price/free criteria, appliances accepted, access/stairs rules, safety, and written pickup terms. Record only actually verified cities.
6. Confirm owner/maintainer operational activation approval. Run `python -m scripts.ttg_release_readiness --state IL --city chicago --require-evidence` for an individual target city.
7. Only after **independent review** open a separate city-scoped activation PR to update truthful coverage, routing, metadata, indexability, sitemap, and local links; verify the production URL and Search Console afterward. A green evidence report is **not** permission to auto-index.

## Deterministic no-quota check

`python -m scripts.ttg_release_readiness --state IL --report ttg-illinois-readiness.json`

This command reports the requested city list, existing structural QA, recorded operational prerequisites and separate blockers. It succeeds for a safe request-only staging configuration even when business coverage is not verified; `--require-evidence` exits nonzero when any selected city prerequisite is absent. GitHub Actions stores a report artifact daily and for relevant PRs. It never changes HTML or customer records.

If the GitHub Actions platform reports an **internal server error before any job starts**, do not treat it as a failed website test or a successful approval. Start a new properly reviewed run; never bypass actual failed tests or CodeQL findings. This is distinct from a local operator-coverage blocker.
