# Evidence-first change control — Free Reliable Appliance Pickup

Effective: 2026-10-22. Scope: changes to `freereliableappliancepickup.com`, its GitHub Pages source, and customer lead routing. **This is a written policy, not proof that GitHub branch protection or deployment tests are configured.**

## Governing principle
Do not substitute work activity for business results. A code commit, passing CI, GitHub merge, live deployment, Google indexing, improved Google search performance, and qualified customer leads are **different verified states**.

**No discretionary bulk SEO rewrites or new location pages** until indexing and search performance baselines, market capacity, and page intent have been reviewed. Fix verified customer-harm, security, false business claims, broken lead routing and critical indexability defects promptly using their own scoped incident procedure.

## VGM organic and competitor measurement requirement

For discretionary rankings or search-intent changes, follow the mandatory market/query scoreboard in `SEO-GOLD-MODEL.md` under **Verified Gold Model (VGM)**. Document contemporaneous *organic* competitor ranking URLs/positions with exact query, location and device when observable; use finalized Search Console query × page × device performance for the site's own baseline; separately identify Maps, images, AI, paid placements, tracker data and qualified organic leads. Missing or inconclusive ranking data is an explicit **blocker for speculative rewrites**, never a reason to guess. Operational and lead-delivery corrections may proceed with the documented exception. Do not overwrite `data/seo-experiments.json` or invent a second experiment registry.

## Before proposing a change
1. Read the current target HTML, `SEO-GOLD-MODEL.md`, related previous PRs, `CHANGELOG-SEO.md`, `data/seo-experiments.json`, and `data/market-routing.json`. Do not repeat previous work or disturb a running experiment.
2. Identify affected URLs, shared components and dependencies, current main commit, and what will **not** change.
3. Classify as **urgent operational/factual defect**, **verified technical defect**, **approved business update**, or **SEO experiment**. Record observed evidence and uncertainty; do not describe a hypothesis as confirmed.
4. For an SEO experiment, save the latest available finalized GSC query/page/device baseline (at least 28 complete days if available, preferably 90 for low-volume pages), its end date, the target query intent and one primary outcome measure. If unavailable, **do not launch a discretionary ranking experiment**. For an urgent factual or lead-routing correction, explain why ranking data is not a prerequisite.
5. Verify owner-approved pickup coverage, phone/tel target, form endpoint and actual lead receipt procedure, appliance acceptance rules, pictures and license, prices/fees and local statements. Never invent pickup examples, addresses, local crews, reviews or guaranteed free pickup.
6. Define one bounded objective, a test plan, risk classification, observation window, and rollback decision. Compare competing URLs and relevant SERPs before making SEO intent changes.

## Scope and approvals
- One objective per PR, typically one variable family and a small number of pages. A shared template requires an explicit sitewide affected-URL assessment; no blind bulk updates.
- **High risk**: index/noindex, robots, canonical, redirects, URL inventory, service coverage, many pages, and fee or route promises. Before merge, require an independent review, explicit owner approval, URL-level impact list and tested rollback plan. Lack of approval means **not merged**.
- **Medium risk**: priority content, homepage links, lead forms or numbers. Verify affected paths and customer journeys.
- **Low risk**: narrow, non-customer-facing diagnostics, documentation and audits. These may be merged after review of scope and passing applicable checks.
- Follow `data/seo-experiments.json` for frozen experiments; the registry is authoritative. Do not create a second experiment calendar. Avoid editing experiment variables during their observation period.

## Required evidence for an affected customer page
**Before merge:** inspect actual rendered output where feasible, confirm changed pages and assets, sitemap/robots/indexability and canonical behavior, correct local facts, phone/tel routing, lead fields, image suitability, mobile access, and all relevant GitHub checks. A green diagnostic report does **not** mean it enforces a quality threshold. Confirm tests actually inspected a nonzero relevant page set. For lead delivery, a successful browser message is not proof the request reached the business inbox; record a controlled end-to-end receipt test.

**Deploy:** use a reviewable PR from a feature branch, not direct production writes. Confirm the expected SHA and review applicable GitHub Pages deployment status; do not claim branch protection where permissions prevent verification.

**After deploy:** check the exact public page and changed behavior against the expected SHA/content. If public verification is unavailable, report **merged, live unverified**. Google indexing must be separately established using GSC URL Inspection; rankings require GSC or consistent tracking with date/device/location; lead increases require credible call/form attribution.

**Follow-up:** respect the observation window and finalized GSC reporting delay. Compare against the recorded baseline and an unchanged comparison cohort when practical. Record verdict `improved`, `unchanged`, `regressed`, or `inconclusive`. Low-volume samples are often inconclusive; do not rewrite or roll back automatically based on a tiny sample. An urgent customer-impact regression can be rolled back without waiting for the SEO window.

## Status language (do not collapse these)
1. **Proposed** — evidence/hypothesis written, no edit.
2. **Committed to branch** — source changed, not merged.
3. **Checks verified** — specified checks completed on latest PR SHA; audit scope recorded.
4. **Merged to main** — GitHub confirms commit; deployment not automatically verified.
5. **Live verified** — live public page behavior inspected; no indexing or rank claim.
6. **Google indexing verified** — inspection provides actual Google coverage and selected canonical.
7. **Search impact measured** — sufficient finalized performance evidence and uncertainty reported.
8. **Business impact measured** — qualified organic requests or completed pickups attributed credibly.

Avoid unqualified words such as "fixed", "done", "ranking", "live", or "indexed" without the corresponding evidence.

## Permanent record and exception handling
- Log each material change and unresolved issue in `CHANGELOG-SEO.md`, citing issue/PR/commit, impact URLs, reason, baseline reference, risk, tests, deployment proof, status, review date and outcomes. Do not include customer names, exact addresses, lead contents or other sensitive information in this public repository.
- Keep experiments in `data/seo-experiments.json` and link their IDs in change entries.
- If required verification is impossible, state the precise limitation and leave discretionary work proposed or blocked; do not guess. Urgent operational defects may proceed with a documented exception, narrow blast radius, before/after tests and follow-up.
- A quality safeguard is not proven until representative positive and negative fixtures demonstrate it runs, detects an introduced defect, and reports inspected URL counts. Repository branch protections/required checks must be separately verified by an authorized administrator.
