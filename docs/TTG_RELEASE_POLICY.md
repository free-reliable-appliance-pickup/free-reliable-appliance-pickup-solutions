# TTG release policy — effective FastTrack 2.1

**Owner-directed policy update, 2026-11-09.** Replaces the former policy that required two successful OpenRouter free-model reports on every exact PR head. The owner requested a release process that is not blocked by temporary external API quota errors; the following retains enforceable QA and truthful-service gates. Free-model review remains available on demand as an **advisory**, not a recurring production prerequisite.

## Mandatory pre-merge checks for every ordinary state/page change

1. Use one coherent state release PR with inventory/manifest and an explicit target market, not dozens of near-duplicate PRs. Avoid content duplication and doorway-style city pages.
2. On the exact PR commit, **all relevant ordinary GitHub Actions checks must pass**. Run the quota-free TTG state batch QA (and its unit tests), page/link/image and SEO checks, and market routing checks. A state manifest must explicitly list the staged pages. A success with zero manifested pages is never proof of a state batch.
3. **GitHub CodeQL JavaScript/Python `security-extended`** must complete successfully for workflow, JS/Python, routing and form code changes. Investigate any actual high/critical findings before approval. A successful scan is not proof of no vulnerabilities; findings and coverage must be inspected.
4. **Independent quality review:** address CodeRabbit findings when available; for material form, customer data, shared routing, payment, release workflow or security logic changes, obtain an independent review (CodeRabbit or qualified reviewer), analyze consequential findings, and document the outcome. For unchanged page-template batches, validated templates, negative unit tests, and maintainer source review are required; repeated paid/free LLM calls are not.
5. The accountable maintainer must inspect the exact code and tests, confirm no unaddressed high/critical defects, and explicitly approve the merge. Never treat a bot comment, a failed call, or a green scan as a human signoff.

## Separate operational eligibility from code release

- Unverified markets can only collect **conditional requests** and must remain `request-only` and `noindex, follow` without fake local operators, booking promises, or guaranteed free pickup. **A request-only page is not an active service page.**
- Do not switch an Illinois (or any other) city to indexable service claims until a real accepting operator, agreed pickup terms, actual ZIP coverage and customer intake flow are verified.
- After an approved merge, verify live URLs, mobile layout, one real category-correct photo, links, and actual Formspree receipt using a legitimate owner-controlled test before marking deployed/operational. Check Google Search Console only when a page is genuinely index-eligible.
- A blocked operator/onboarding confirmation must not block drafting, staging or QA of the next state; it **does** block service activation or ranking claims in unserved markets.

## External model review

The historical free-model workflow is retained as a **manually triggered advisory**. OpenRouter 429, invalid JSON or unavailable model yields no report; it is never counted as success. Do not auto-trigger per city PR. Use only explicit reviewer requests, with no paid fallback or unverified response acceptance. This keeps optional AI review from wasting daily quota or producing misleading red PR checks.

## Evidence per release

Record PR, exact SHA, test and CodeQL run links, review findings resolution, responsible maintainer, market status, live URL, browser/form receipt test and deployment/indexing eligibility. No silent override of GitHub branch protection or rulesets (currently none configured on `main`, verified 2026-11-09). If branch protections are added later, update required checks transparently.

## Rollout order

First merge/review infrastructure changes (CodeQL and deterministic batch QA). Next stage all 17 Illinois request-only pages as **one coherent package**, checking that the integrated branch includes the latest statewide/Chicago form fixes. Only publish after project QA and explicit maintainer review. Then apply the exact same tested workflow to the next state.

No automatic deployment, false coverage, fake approvals or Google ranking guarantee is authorized by this document.
