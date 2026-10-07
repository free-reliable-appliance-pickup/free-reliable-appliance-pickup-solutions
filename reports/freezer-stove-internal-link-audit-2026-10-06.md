# Freezer + Stove/Oven Internal-Link Audit — 2026-10-06

## Decision

No customer-facing ranking edit is justified before the current experiment gates.

The audit was added to the existing internal-link monitor and completed successfully on current `main`.

## Technical status

- Active freezer specialty pages: **12**
- Active stove/oven specialty pages: **13**
- Broken internal targets: **0**
- Unreachable sitemap URLs: **0**
- True zero-inlink sitemap pages after excluding self-links: **0**

## Missing direct city-owner handoffs

### Freezer
- `/los-angeles-freezer-pickup/`
  - direct `/los-angeles-appliance-pickup/` handoff: **missing**
  - meaningful active inlinks: **4**
  - crawl depth: **2**
  - current sources: freezer hub + LA refrigerator/stove/washer-dryer specialty pages
  - effective gate: **2026-10-14**

### Stove / oven
- `/los-angeles-stove-oven-pickup/`
  - direct `/los-angeles-appliance-pickup/` handoff: **missing**
  - meaningful active inlinks: **5**
  - crawl depth: **2**
  - current sources: stove/oven hub + Southern California stove/oven + LA refrigerator/freezer/washer-dryer specialty pages
  - effective gate: **2026-10-14**

These are architecture observations, not verified defects. The Los Angeles general owner is protected, so do not add the direct handoffs before its gate.

## Low-link specialty pages that already have the city handoff

- `/aurora-freezer-pickup/` — 1 meaningful inlink, depth 2, gate **2026-10-16**
- `/denver-freezer-pickup/` — 1 meaningful inlink, depth 2, gate **2026-10-16**
- `/aurora-stove-oven-pickup/` — 1 meaningful inlink, depth 2, gate **2026-10-16**
- `/denver-stove-oven-pickup/` — 1 meaningful inlink, depth 2, gate **2026-10-16**
- `/phoenix-stove-oven-pickup/` — 1 meaningful inlink, depth 2, gate **2026-10-16**

These pages remain reachable and are not technical orphans.

## Finalized GSC baseline through 2026-10-04

Window: **2026-09-07 through 2026-10-04**.

- `/los-angeles-freezer-pickup/` — **11 impressions, 0 clicks, avg position 17.0**
- `/los-angeles-stove-oven-pickup/` — **2 impressions, 0 clicks, avg position 5.0**
- `/aurora-freezer-pickup/` — no finalized GSC row yet
- `/denver-freezer-pickup/` — no finalized GSC row yet
- `/aurora-stove-oven-pickup/` — no finalized GSC row yet
- `/denver-stove-oven-pickup/` — no finalized GSC row yet
- `/phoenix-stove-oven-pickup/` — **1 impression, 0 clicks, avg position 5.0**

## Interpretation

- The Los Angeles stove/oven page already has a small page-one signal. Protect it; do not normalize internal links merely for consistency.
- The Los Angeles freezer page has more volume but is still below page one on average. Recheck finalized query/page ownership at the October 14 gate.
- Aurora and Denver specialty pages do not yet have enough finalized evidence for a link-strengthening change.
- Phoenix stove/oven has only one impression; protect the existing page-one signal and wait for more data.

## Review rule

At each applicable gate:
1. Pull finalized GSC first.
2. Check the exact city + appliance query ownership.
3. Protect page-one or improving signals.
4. Only add a general-city → specialty handoff when it strengthens intended ownership without cannibalizing a working general owner.
5. Make one minimal change, validate, and restart the observation window.

## Monitoring change

Commit `69cba605257ae55e3339a3fff54485ca8d03d343` expanded the internal-link workflow to audit active freezer and stove/oven city handoffs with experiment-gate awareness.
