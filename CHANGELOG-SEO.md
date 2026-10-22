# SEO change and decision register

Use `SEO-CHANGE-CONTROL.md` for process rules. This public record contains no customer details. Existing experiment histories remain in `data/seo-experiments.json`; do **not** duplicate or overwrite them.

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
