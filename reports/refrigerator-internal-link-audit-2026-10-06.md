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

## Finalized GSC baseline through 2026-10-04

Measurement window: **2026-09-07 through 2026-10-04**.

### Dedicated refrigerator pages

- `/baldwin-park-refrigerator-pickup/` — no finalized GSC row yet.
- `/costa-mesa-refrigerator-pickup/` — no finalized GSC row yet.
- `/huntington-beach-refrigerator-pickup/` — no finalized GSC row yet.
- `/los-angeles-refrigerator-pickup/` — **13 impressions, 0 clicks, avg position 33.77**.
  - observed queries include `free refrigerator pick up los angeles` (~42) and `refrigerator removal los angeles` (~55).
- `/aurora-refrigerator-pickup/` — no finalized GSC row yet.
- `/bellflower-refrigerator-pickup/` — no finalized GSC row yet.

### Matching general city owners

- `/baldwin-park-appliance-pickup/` — **11 impressions, 0 clicks, avg position 11.73**.
- `/costa-mesa-appliance-pickup/` — **36 impressions, 0 clicks, avg position 17.39**.
  - refrigerator-intent signals already exist on the general page: `refrigerator pickup free` ~position 5, `pick up old fridge for free near me` ~7, `broken refrigerator pick up` ~8.
- `/huntington-beach-appliance-pickup/` — **47 impressions, 0 clicks, avg position 12.06**.
  - refrigerator-intent signals already exist on the general page: `refrigerator disposal near me` ~position 1 and `free refrigerator pick up near me` ~7.
- `/los-angeles-appliance-pickup/` — **141 impressions, 4 clicks, 2.84% CTR, avg position 16.38**.
  - includes a `free fridge haul away` click at position 1 and broader Los Angeles appliance visibility.

### Interpretation

The missing city-owner handoff is **not automatically a defect**. Costa Mesa, Huntington Beach and Los Angeles already show refrigerator-intent visibility on the general owner, while the dedicated refrigerator pages are either immature or weaker. At the effective gate, compare finalized query/page ownership before deciding whether to add a direct handoff. Do not move refrigerator intent away from a working general owner just to normalize architecture.

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
