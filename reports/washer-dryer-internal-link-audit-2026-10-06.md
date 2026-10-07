# Washer/Dryer Internal-Link Audit — 2026-10-06

## Decision

The active washer/dryer network is structurally healthy. Do not make customer-facing link changes before the applicable experiment gates.

## Technical status

Validated on current `main`:

- Active washer/dryer pages in sitemap: **274**
- Missing direct matching city-owner handoffs: **2**
- Washer/dryer pages with one or fewer meaningful inlinks: **1**
- Unreachable sitemap URLs: **0**
- Broken internal targets: **0**
- True zero-inlink sitemap pages after excluding self-links: **0**

## Missing direct city-owner handoffs

### South Pasadena
- `/south-pasadena-washer-dryer-pickup/`
- direct `/south-pasadena-appliance-pickup/` handoff: **missing**
- meaningful active inlinks: **1**
- crawl depth: **4**
- current source: `/alhambra-washer-dryer-pickup/`
- effective gate: **2026-10-15**

Finalized GSC through 2026-10-04:
- washer/dryer page: no finalized row yet
- general city owner: **5 impressions, 0 clicks, avg position 22.2**
- observed query: `free appliance pickup pasadena` — 3 impressions, avg position 33

Interpretation: this is the weakest structural laundry handoff in the active network, but the owner page is frozen. Review first at the October 15 gate; do not force an edit now.

### Central Valley
- `/central-valley-washer-dryer-pickup/`
- direct `/central-valley-appliance-pickup/` handoff: **missing**
- meaningful active inlinks: **13**
- crawl depth: **2**
- effective gate: **2026-10-14**

Finalized GSC through 2026-10-04:
- washer/dryer page: **3 impressions, 0 clicks, avg position 13.67**
- general regional owner: **1 impression, 0 clicks, avg position 13**

Interpretation: this is not an orphan or crawl-depth problem. It already has strong network support. Do not add a direct handoff simply for symmetry; review ownership at the October 14 gate.

## Review rule

At the effective gate:
1. Pull finalized GSC first.
2. Check exact city/region + washer/dryer query ownership.
3. Protect improving/page-one signals.
4. Only add a direct owner → laundry handoff if it strengthens intended ownership without cannibalizing a working page.
5. Make one minimal change, validate it, and restart the observation window.

## Monitoring change

Commit `936fa03eba004cd4509ec1fd8840971fc3cda2a5` expanded the internal-link workflow to audit active washer/dryer city handoffs with experiment-gate awareness.
