# TTG FastTrack 2.1 — one state, one testable batch

## Why our releases kept blocking
The current repository policy requires two successful independent free-model reviews on every exact PR head. Free model quota errors (HTTP 429), unavailable providers, invalid responses and large patches can prevent approval even when normal CI passes. Never describe a quota failure as a failed page test. A later code commit invalidates approval based only on an earlier SHA.

## What is implemented in this change
- Offline Python QA, regression tests and a GitHub Actions job that do not use paid services, OpenRouter tokens or third-party AI quotas.
- A batch manifest format for the next state and every subsequent state. Each manifest explicitly lists existing proposed page paths, so missing pages are failures rather than silently skipped.
- The checker verifies one H1, self-canonical, noindex for unverified coverage, Illinois-style form safety fields, one valid local image, state restriction, page source tags and customer routing.
- The checker reads market-routing.json and rejects premature automatic promotion of a request-only batch.
- If no manifest exists, the workflow clearly says **NO PAGES APPROVED**. Green unit tests for the checker are never a release approval.

## How to use with the next state
1. Start exactly one branch for the state, with one state hub, useful unique city pages and only justified appliance-category pages. Use real category-correct images, correct alt text and truthful operator descriptions.
2. Add a file at data/ttg-state-batches/XX.json. Example (paths must exist on the branch and correspond to the correct state):

    {
      "state_code": "IL",
      "mode": "request-only",
      "pages": [
        "illinois-appliance-pickup/index.html",
        "chicago-il-appliance-pickup/index.html",
        "aurora-il-appliance-pickup/index.html"
      ]
    }

3. Run: python -m unittest discover -s tests -p test_ttg_state_batch_qa.py -v
4. Run: python scripts/ttg_state_batch_qa.py
5. Open **one batch PR** rather than dozens of repetitive page PRs. This offline check runs on changes to pages, manifests or routing. CodeQL and the normal site CI remain independent jobs.
6. Keep requests conditional and noindex until actual market coverage is established. Before enabling indexing, verify operators, supported neighborhoods/ZIPs, terms, live Formspree receipt, mobile rendering, links, and accurate scope. Then verify merged GitHub Pages URLs and Search Console.

The manifest describes only staging pages; the absence of a route and a live operator means the site must not promise free pickup or booking. No blanket city radius or #1 ranking is promised.

## Release governance adopted for FastTrack 2.1
The owner requested a quota-independent release process; the operative requirements are documented in [TTG_RELEASE_POLICY.md](TTG_RELEASE_POLICY.md). Deterministic exact-head QA, CodeQL where applicable, substantive independent review for consequential changes, and accountable maintainer approval replace an unconditional requirement for two limited free-model responses. A free model call remains a manually requested advisory only. No project policy grants false operator activation or bypasses an actual GitHub branch protection rule.

The project does **not** mark Illinois published merely because the new testing engine passes. Publish only reviewed code, test owner-controlled Formspree delivery and live mobile rendering, and retain request-only/noindex until confirmed fulfillment supports other claims.

## Status ledger
Keep separate evidence for: drafted, staged, structural QA passed, security reviewed, release approved, merged, deployed, form receipt verified and index eligible. Record commit SHA, operator evidence, reviewer, actual deployed URL and GSC results. A passing preflight is only one step of the state pipeline.

## Existing Illinois dependency
Illinois hub #988 and Chicago guide #989 remain open, and category drafts #993–#996 are not live. CodeQL is staged in #997; the new policy in this PR supersedes the quota-dependent rule. Open reviewer-hardening PR #960 needs separate reconsideration so it does not reintroduce automatic rate-limited failures.