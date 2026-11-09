# Turbo Track Gold — FastTrack 2.0 (Illinois-first)

## Goal
Finish each state in one cohesive batch while ensuring any published page is safe, genuinely useful, and backed by real pickup capacity. No synthetic addresses, fake local jobs, unverified partner routes, or guaranteed free pickups. Illinois stays first until its release checklist is complete.

## Separate work from approval
1. **Research**: competitor strengths, municipal disposal/donation options, appliance resale/buyer evidence, most practical metro clusters.
2. **Inventory**: one state owner guide, unique major-city guides and only genuinely distinct appliance-category guides. Each is a planning record, staged page, approved PR, live page, or index-eligible page; never conflate those states.
3. **Operations truth**: inspect data/market-routing.json and record confirmed actual accepting operator + supported ZIP/terms. Unconfirmed Illinois remains request-only with noindex.
4. **Assets & intake**: one existing real category-correct photo per page, accurate alt/disclosure, truthful phone/service claims; Formspree, actual address, city, ZIP, phone, appliance/condition, stairs/floor, exit path, optional paid quote explicitly separate.
5. **Fast QA independent of external AI**: existing GitHub checks, single-page HTML form/canonical/photo smoke checks, CodeQL JavaScript/Python security-extended scans, source QA, no duplicate submission, and manual independent review of serious findings.
6. **Independent review provider**: use available free AI reviewers sparingly; cache exact-commit reports, back off on HTTP 429, never invent approval. CodeRabbit is a useful extra independent reviewer but not automatically equivalent to two approved model reports.
7. **Release governance**: the repository currently requires two distinct complete independent free-model reviews on exact head; CodeQL alone does NOT satisfy that policy. A separately reviewed explicit policy update is required before any substitution with CodeQL + CodeRabbit + maintainer sign-off. Never bypass GitHub branch protections or force merge.
8. **Release sequence**: Illinois statewide #988 then Chicago #989 then one-file staged cities/categories; real live link and mobile/browser form checks after each approved merge.
9. **Activate rankings only after real fulfillment**: remove noindex solely on verified service city owner pages with distinct value; update state-city-category crosslinks and sitemap, confirm GSC indexing eligibility. No blanket state radius or ranking guarantee.
10. **Scale**: reuse the validator and staging factory for Texas, Florida, Georgia, then the next state based on actual accepted leads and operator availability.

## Findings on 2026-11-09
- Chicago #989 failed the old independent workflow's 18k diff budget (18,719 characters), NOT just model quota. Reduced to approx. 17.5k in commit 926dc936adb20ddaecdfeb67d3e48a99ea05e5cf, retaining safety and form details; live CI/review still pending.
- Illinois #988 latest independent review completed using both existing models, but reported HIGH findings requiring actual code-based triage; complete AI responses are not automatic approval.
- Workflow #960 is open. Free OpenRouter endpoints have quota/capacity limits and proposed replacement models may share the same account allowance.
- GitHub Models inference API was retired July 30, 2026 and is not a viable fallback.
- CodeQL is a different, GitHub-native no-OpenRouter-quota security scan, staged in .github/workflows/ttg-fasttrack-codeql.yml. It cannot independently decide fulfillment truth, SEO quality or form receipt.

## Release checklist (per target page)
- [ ] Unique city/appliance intent, correct indexability and actual routing
- [ ] Correct photo/alt/canonical/link targets; no fake coverage
- [ ] Complete customer and access details; safe form; live Formspree receipt verified
- [ ] Existing ordinary CI success on exact SHA
- [ ] Independent security scan and findings triaged
- [ ] Required release approvals genuinely completed, or later authorized governance replacement in place
- [ ] Merged then verified actual GitHub Pages URL, mobile, form, noindex/canonical and sitemap
- [ ] Actual Google Search Console and accepted-lead measurement

Nothing in this plan authorizes a paid service, a reviewer-gate bypass, or publication of an unverified local free pickup offer.
