# SEO change and decision register

Use `SEO-CHANGE-CONTROL.md` for process rules. This public record contains no customer details. Existing experiment histories remain in `data/seo-experiments.json`; do **not** duplicate or overwrite them.

## 2026-10-23 — Enforce existing priority intake contract in CI
- **Verified gap:** The existing `scripts/audit-priority-intake-contract.py` was expanded to 38 pages, but the `Audit Priority Pickup Forms` workflow only ran `scripts/audit-priority-pickup-forms.py`. Its green 61-form audit did not independently demonstrate the 38-page guard or negative fixtures executed.
- **Change:** Add the existing contract script to both workflow path triggers and run its positive/negative fixture self-test and full source contract check as separate CI steps. No public page, form destination, routing, content, indexability or SEO experiment changed.
- **Verification/rollback:** PR must show both new steps succeeded and `PRIORITY_INTAKE_PAGES_INSPECTED 38`, `PRIORITY_INTAKE_FAILURES 0`, plus fixture results before merge. Revert this workflow-only change if it creates false positives. CI source checks do not prove live form receipt.
- **Status:** Branch proposal pending exact-head CI and merge at time of entry.

## 2026-10-23 — Southeast California Formspree service-attribution corrections (operational exception)
- **Classification:** Verified source-level customer intake metadata inconsistency, not a ranking experiment or reported delivery failure.
- **Pages:** `/la-mirada-appliance-pickup/`, `/cerritos-appliance-pickup/`, `/pico-rivera-appliance-pickup/`, `/downey-appliance-pickup/`.
- **Evidence:** Current main source had exactly one Formspree POST customer form on each page, with required telephone input and source-page attribution, but no static hidden `service` field. Each retains the established `https://formspree.io/f/mvzeapzd` destination. This does **not** prove any submission was lost.
- **Technical exception:** `data/seo-experiments.json` contains running Downey and Pico Rivera SEO tests (evaluate-not-before Oct 14). This change does not touch title, meta, body copy, schema, canonical, navigation, imagery, indexability or ranking variables; it only supplies the existing service classification consistently with PR #400. No ranking experiment was initiated.
- **Change:** Add exactly one hidden `service=General major appliance pickup` field after each existing `source_page` field; extend `scripts/audit-priority-intake-contract.py` by four existing pages (38 total including homepage).
- **Preserved:** Form action/method, mandatory contact fields, phone numbers and routing, optional customer fields, appliance eligibility, pickup claims, partner status, quote preferences and current SEO experiments.
- **Risk/rollback:** Medium-risk customer-form metadata update; review CI and branch diff before merge, revert the bounded PR on regression. No paid action, fake test lead, or end-to-end submission is authorized. Source assertions alone cannot verify actual receipt.
- **GSC context:** Connected SMEPost finalized Oct 18–20 only (three days, no comparisons). Too little for an SEO impact claim; operational field correction does not require a ranking hypothesis.
- **Status:** Feature-branch commits pending PR CI and merge; production deployment and real Formspree receipt unverified at time of entry.

## 2026-10-23 — Four California intake source and mobile input repairs (operational exception)
- **Classification:** Verified source-level customer-form attribution/mobile usability defects, not an SEO experiment or an emergency incident.
- **Pages:** `/palm-springs-appliance-pickup/`, `/la-canada-flintridge-appliance-pickup/`, `/altadena-appliance-pickup/`, `/san-marino-appliance-pickup/`.
- **Evidence:** Current `main` source on Oct 23 had one Formspree POST form on each page with required contact fields and `source_page` but no static hidden `service`. La Cañada Flintridge, Altadena and San Marino also had a required `phone` field without `type="tel"`. Shared `assets/customer-routing.js` does not automatically supply missing `service` fields. **No form-delivery failure is established.**
- **Existing controls:** Related merged PR #393 fixed the same class on other cities. The authoritative `data/seo-experiments.json` lists protected Coachella, Altadena, La Cañada Flintridge and San Marino experiments (evaluate-not-before dates Oct 9–15). This is a documented **technical exception**, not a ranking/content change. No registry values or experiment variables were changed.
- **Change:** Add exactly one static `service=General major appliance pickup` field to each existing form; add `type="tel"` to the three required phone inputs; extend `scripts/audit-priority-intake-contract.py` to include all four pages.
- **Unchanged:** Formspree action/method, customer field requiredness, customer text, pickup eligibility, paid-quote preference, telephone numbers, market/partner routing, images, SEO title/meta/body, canonical, robots, sitemap and internal links.
- **Risk and rollback:** Medium-risk customer-form source change; revert the bounded PR if validation finds a regression. No paid action or live test submission authorized.
- **Baseline:** Connected GSC free finalized Oct 18–20, 2026 window; Palm Springs page insight returned no page-level data. GSC is not a prerequisite for verified operational input corrections and no ranking effect is claimed.
- **Tests and deployment:** Branch source assertions passed for changed fields; expanded regression guard pending CI. PR merge, GitHub Pages deployment, public form rendering and actual Formspree receipt must be verified separately.
- **Status:** Committed to feature branch; **not yet merged/live verified** at time of entry. Review after CI/PR inspection; no speculative ranking experiment launched.

## 2026-10-22 — Process audit: quality checks were not triggered for ordinary HTML PRs
- **Finding:** `audit-content-uniqueness-fast.yml` only ran on sitemap/workflow changes; `audit-page-concentration.yml` ran on push but not PR. The quality reports therefore did not reliably appear **before merging city-page content edits**.
- **Evidence:** workflow trigger definitions read in GitHub on 2026-10-22.
- **Change:** PR [#385](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/pull/385); merged as `bc7674ce84974838f437b47c9142bd3519ff2818`.
- **Scope:** Two GitHub Actions workflow trigger files. No customer HTML, copy, images, phones, forms, redirects or canonical tags changed.
- **Verification:** All 13 available PR workflow runs completed successfully on head SHA `47504e0f6e689f67d0a79206913b3f9eb0a345ce`; the two intended diagnostics appeared in that run.
- **Status:** **Merged to main; CI execution verified.** This does not demonstrate that quality-score thresholds block a poor page or that a deliberate negative fixture was detected. No organic-impact claim.
- **Follow-up:** Test nonzero audit coverage and deliberate fail fixtures before claiming a complete preventive quality gate. Verify branch protection separately (GitHub integration returned 403 to a branch-protection read).

## 2026-10-22 — California lead classification normalization
- **Change:** PR [#384](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/pull/384); merged as `9b72927ee66767b1e038d3b76515f4592af46bb4`.
- **Scope:** Added missing hidden `service` attribution field to 26 existing California general pickup forms, leaving their existing source-page field intact.
- **Verification currently recorded:** GitHub merge; source-level change. **No independent live form receipt or organic ranking improvement is documented in this record.**
- **Status:** **Merged to main; live receipt and business effect unverified in this register.**
- **Follow-up:** Check a controlled form receipt for representative affected pages without exposing customer data.

## 2026-10-22 — Open limitations, not confirmed SEO defects
- **Google indexing:** Sitewide Page Indexing counts and per-priority-page Google-selected canonicals were not available from connected GSC Wizard (subscription required); the limited connected GSC performance window is not an indexing inventory. **Status: unverified**.
- **Production governance:** GitHub branch-protection read returned a 403 from the integration. **Status: governance configuration unverified**, not proof of protection or lack thereof.
- **Organic search:** Keyword.com and Ubersuggest metrics have different scopes and freshness. The 100-keyword tracking snapshot and estimated monthly domain traffic must not be conflated with each other or treated as proof of any single edit's impact.
- **Pending decision:** Avoid mass rewriting/deleting/redirecting pages until indexing inventory, real business coverage, search intent, and measurement are established.

## Template for subsequent changes
```text
Change ID / date:
Type / severity:
Issue and verified evidence:
Existing experiment ID / prior related PRs:
URL(s) / shared components affected:
Owner-approved business facts checked:
Hypothesis (for SEO experiments) or defect description:
Finalized baseline, last data date and source (or operational exception):
One variable / scope and exclusions:
Risk / approvals / rollback path:
PR and commit SHA:
Test scope, actual execution, results:
Live URL and receipt verification (or reason unavailable):
Status (proposed/branch/checks/merged/live/indexed/measured):
Observation window and review date:
Verdict (pending/improved/unchanged/regressed/inconclusive):
Next action / no-revisit-before:
```

## 2026-10-22 — Phoenix general form service classification
- **Type:** Verified operational attribution inconsistency; not a ranking experiment.
- **URL:** https://freereliableappliancepickup.com/phoenix-appliance-pickup/
- **Evidence:** Live HTML and main source lack a static service field; customer-routing.js does not add one. Existing city, state and source_page fields remain present. This does not establish failed delivery.
- **Change:** Add one hidden service=General major appliance pickup field on branch fix/phoenix-form-service-20261022. Base main: 9c8a791181d55a0f21ead95454e4e995f0311abe.
- **Prior work:** PR #384 applied the same classification to 26 California forms; all 26 live pages were checked on October 22 and contain the expected service and source fields and required phone input.
- **Risk/verification:** One additive hidden input; existing endpoint, visible fields, phones, content and indexability unchanged. Exact removal of the new line restores the original file. Review PR checks before merge; verify public HTML after deployment. No test submission or inbox receipt has been verified.
- **Baseline exception:** Operational field consistency does not require a search-ranking baseline; no SEO experiment variables changed.
- **Status:** Committed to branch; deployment and business impact pending. Rollback: remove the single added input. Review after deployment.


## 2026-10-22 — VGM homepage static form attribution
- **Type:** Verified operational intake attribution inconsistency; not an SEO experiment.
- **URL:** https://freereliableappliancepickup.com/#request
- **Evidence:** The homepage Formspree form in main contained no static `source_page` or `service` input. Shared customer-routing.js supplies `source_page` only when its submission handler runs, and does not supply `service`. Other priority city forms have both inputs. This does not prove failed delivery or missing leads.
- **Prior work / experiment check:** PRs #384 and #387 standardized the same inputs on city pages. `data/seo-experiments.json` includes an ongoing homepage title/meta CTR test with an evaluation gate of 2026-10-14; no title/meta, internal links, canonical, or indexability settings are changed here.
- **Change:** Add two static hidden homepage pickup-form fields: `source_page=home` and `service=General major appliance pickup`. Preserve the existing Formspree endpoint, visible inputs, required phone, ZIP, state, city, qualification, routing JavaScript and all customer-facing content.
- **Pre-merge source tests:** Exact-one-form-anchor check; positive assertions for both fields; baseline negative fixture without both fields; exact diff reconstruction confirms no other homepage changes. Tests passed locally in the connected GitHub read/write session, not an end-to-end submission.
- **Risk / rollback:** Narrow medium-risk operational attribution fix. Rollback is removal of the two added hidden input elements.
- **Status:** Committed to review branch `fix/vgm-homepage-intake-attribution-20261022`. PR/CI, merge, actual public HTML, Google effects and Formspree inbox receipt are not yet verified at the time of this record.
- **Follow-up:** Review PR checks; verify deployed public HTML and complete an authorized controlled inbox receipt test. Do not treat missing lead attribution as proof of lost leads.


## 2026-10-22 — VGM organic ranking and competitor scoreboard codified
- **Type:** Documentation and repeatable verification method; no live page, form, phone, schema, canonical, link or routing modification.
- **Evidence:** The existing `SEO-GOLD-MODEL.md` already advised SERP and competitor analysis but had no single mandatory per-market/per-query scoreboard defining comparability, missing-rank notation and decision gates. Owner requested that organic search and competitor rankings become mandatory parts of "Use VGM."
- **Change:** Defined VGM command, baseline fields, competitor SERP comparison, GSC query/page/device measures, qualified-lead outcome, experiment gate and reporting standard; connected it to `SEO-CHANGE-CONTROL.md`. No ranking performance improvement is claimed.
- **Safety:** Preserves `data/seo-experiments.json` as the only experiment calendar and `data/market-routing.json` as operational market truth; prevents changes based on missing evidence.
- **Review:** [PR #389](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/pull/389). This is a documentation-only change; verify its current merge state in GitHub. No CI check was triggered on the documentation-only PR at initial inspection.


## 2026-10-22 — VGM priority customer form regression gate
- **Type / evidence:** Verified missing CI assertion, not a confirmed form-delivery failure. The existing `Audit Approved Request Actions` workflow checked for a Formspree endpoint and same-page request links, but did not assert a required customer phone or consistent `source_page` and `service` tracking fields on the homepage/priority city forms. The homepage source/service omission was repaired in PR #388; this check is designed to prevent recurrence.
- **Scope:** Add `scripts/audit-priority-intake-contract.py` (root home and 23 existing priority general city pages) and invoke its one positive plus seven negative fixtures and read-only source audit in the existing approved-actions PR workflow. Preserve original customer HTML, scripts, business routing, images, titles, metadata, and experiment registry.
- **Baseline observations:** The reviewed priority forms contain static source/service fields and required phone inputs. Phoenix has the existing label `Phoenix city page` and Columbus has lowercase `general appliance pickup`; this audit respects those established values rather than altering customer-facing forms as part of a CI change.
- **Acceptance:** CI must report 24 inspected HTML pages with zero failures; test fixtures must demonstrate that a missing/wrong attribution, unrequired phone, wrong method/endpoint and duplicate customer form are rejected. Record actual PR checks, not just test presence.
- **Scope limits:** The test checks repository HTML; it is not evidence of GitHub Pages deployment, Google indexing, organic positions, call tracking, or successful receipt by Formspree.
- **Vancouver routing:** Existing issue #378 already records a distinct unresolved mismatch between the public partner-supported description and `data/market-routing.json` recruiting status. Do not infer approved partner forwarding or override market truth in this CI change.
- **Rollback:** Revert the added script and workflow step; no production content to undo.
- **Status:** Review branch `ci/vgm-priority-intake-regression-20261022`; merge and check outcomes are separate verification steps.
