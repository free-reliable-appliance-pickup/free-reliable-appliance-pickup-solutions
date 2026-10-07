# Refrigerator Internal-Link Audit — 2026-10-06

## Decision

Do **not** make customer-facing refrigerator/internal-link changes before the applicable experiment gates.

This audit is measurement/monitoring work only. It excludes self-links from meaningful inlink counts and respects the current experiment registry.

## Sitewide technical status

Validated on current `main` after commit `d9a32e186ddcbaf19221fa7f912ceec08623bf52`:

- Sitemap URLs: **698**
- Unreachable from homepage: **0**
- Broken internal targets: **0**
- Active sitemap pages with zero meaningful inlinks: **0**
- Refrigerator pages in the active sitemap missing a direct link from their matching city appliance owner: **4**

## Active refrigerator pages missing the direct city-owner handoff

| Refrigerator page | Meaningful active inlinks | Crawl depth | Current meaningful sources | Effective gate |
|---|---:|---:|---|---|
| `/baldwin-park-refrigerator-pickup/` | 2 | 2 | `/appliances/`, `/refrigerator-pickup/` | **2026-10-14** |
| `/costa-mesa-refrigerator-pickup/` | 2 | 2 | `/appliances/`, `/how-to-get-rid-of-old-refrigerator/` | **2026-10-14** |
| `/huntington-beach-refrigerator-pickup/` | 2 | 2 | `/appliances/`, `/how-to-get-rid-of-old-refrigerator/` | **2026-10-14** |
| `/los-angeles-refrigerator-pickup/` | 5 | 2 | LA freezer, stove/oven, washer/dryer, national refrigerator hub, Southern California refrigerator page | **2026-10-16** |

The matching city appliance owner pages are currently protected, so adding the missing handoff now would contaminate active experiments.

## Low-link refrigerator pages that already have the city handoff

These are not broken, but deserve evidence review at their gates:

- `/aurora-refrigerator-pickup/` — 1 meaningful active inlink, depth 2, effective gate **2026-10-14**
- `/bellflower-refrigerator-pickup/` — 1 meaningful active inlink, depth 3, effective gate **2026-10-16**

Other active refrigerator pages currently have at least 2 meaningful inlinks, and all active refrigerator URLs remain reachable from the homepage.

## Intentional noindex refrigerator aliases

The following existing source pages are intentionally outside the active sitemap and use `noindex, follow`; do not treat them as sitemap-link defects:

- `/claremont-refrigerator-pickup/`
- `/la-verne-refrigerator-pickup/`
- `/san-dimas-refrigerator-pickup/`
- `/upland-refrigerator-pickup/`

## Review rule

At each effective gate:

1. Pull finalized GSC performance first.
2. Check exact query/page ownership and compare with the recorded baseline.
3. Protect any page-one or improving signal.
4. Only add a city-owner → refrigerator handoff if the evidence supports strengthening the refrigerator owner without creating cannibalization.
5. Make one minimal change, validate it, register/reset the experiment window.
6. Do not reactivate intentional noindex refrigerator aliases without separate evidence.

## Monitoring improvements completed

- Commit `195bcdee6a6bf03c1aa3f481d32d05e71d3193d0`: added refrigerator city-handoff auditing and experiment-gate awareness.
- Commit `85f03695b22a813cd565716e8049acf4c232edee`: added meaningful inlink count, crawl depth and source evidence.
- Commit `d9a32e186ddcbaf19221fa7f912ceec08623bf52`: corrected inlink accounting to exclude self-links.

The updated Audit Internal Link Graph workflow completed successfully after the self-link correction.
