# VGM Independent Multi-AI Review — Free-First Setup

## Purpose
Create TWO genuinely independent AI second-opinion checks on proposed Free Reliable Appliance Pickup website changes. ChatGPT remains the coordinator; AI results are suggestions only. Never replace static CI, manual/operational verification, customer-form checks, partner confirmation, or actual Search Console evidence.

**Current stage: source code proposed in PR; reviewers do not run until this PR is merged and the user connects an OpenRouter API key. No DeepSeek, Perplexity or Kimi accounts are connected by this code.**

## Architecture
1. Existing GitHub pull request raised for a future website improvement.
2. `.github/workflows/vgm-independent-multi-ai.yml` runs on each new or updated same-repository PR AFTER this change merges.
3. The job checks out the trusted default branch ONLY. It reads public PR *patch text as data* from GitHub's API; does not checkout/run contributor code, and makes no website/API mutations.
4. Two currently free, distinct third-party AI models on the OpenRouter free plan independently inspect the same limited public diff:
   - Cohere North Mini Code `cohere/north-mini-code:free` — technical regressions
   - Qwen3.8 27B `qwen/qwen3.8-27b:free` — SEO, customer forms, business truthfulness
5. A report and JSON artifact are available in the GitHub Actions run. Each model's separate findings and exact model IDs are recorded.
6. Incomplete model responses, missing secret, unreviewed/large files, or API quota errors are explicitly **INCOMPLETE**, never approved. High/critical findings demand human review.
7. Separate existing safety audits, branch/PR checks and live deployment verification still apply. **No automatic merge or deployment is authorized by this review.**

## One-time connection — the only user action needed
1. Sign up for OpenRouter's Free plan at https://openrouter.ai/ (no paid subscription or credits required for the free-model routes, subject to current rate limits).
2. In OpenRouter, create a personal API key. Keep it private; **never paste it in chat or commit it**.
3. In GitHub repository `free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions`, visit **Settings > Secrets and variables > Actions > New repository secret**. Set its name to exactly `OPENROUTER_API_KEY`, and paste the key as the value.
4. Review and merge this PR once existing checks pass. For every following same-repo pull request, GitHub Actions will automatically request two independent reviews.
5. To review an existing PR, use **Actions > VGM Independent Multi-AI Review (Free Models) > Run workflow** and enter its PR number.

The free OpenRouter plan currently limits free models to about 50 requests/day; two requests are used for every reviewed PR. When quotas are exhausted, results will say INCOMPLETE. We send only selected *public GitHub diff text* to the model provider. Avoid pushing private homeowner information, private partner rosters, or API tokens to a public repo.

## Later agents: independent research and comparison
- Perplexity: research/source verification, if separately authenticated and API use authorized.
- DeepSeek: optional additional code-review model when a truly no-cost endpoint is available.
- Kimi/Moonshot: second-opinion review of strategy when a no-cost authorized endpoint is available.
- Activepieces: Gmail outreach reply classification, registration status, follow-ups, directory link verification — must be connected by the account owner. No paid plan required to start.

Do not quietly substitute paid API routes for free services. If a user wants the exact named AI products instead of the current free Cohere+Qwen reviewers, verify their available **free API** access before activation.

## Operating guardrails
- Apply Verified Gold Model: inspect -> evidence -> minimum fix -> tests -> live verification -> report.
- The AI model's claim is never independent evidence that a website change is correct or that rankings moved.
- No paid links, fabricated street addresses/partners/reviews, invented phone numbers or guaranteed free pickup.
- Exclude private/customer lead paths, credentials and binary/image data from outbound prompts.
- No write GitHub permission; no autonomous commits, merges, outreach messages, account registration or purchase in this workflow.
- Appliance Deal Flow USA is a separate project and must not be included.
- Provider models and free-tier availability can change; the strict allowlist fails visibly, never auto-switches to a paid model.
