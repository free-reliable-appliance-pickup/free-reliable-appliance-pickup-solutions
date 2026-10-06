# Fresh GSC Early-Warning Snapshot — 2026-10-06

## Scope

Source: Windsor.ai Search Console connector for `sc-domain:freereliableappliancepickup.com`.

Window requested: **2026-10-04 through 2026-10-06** with `include_fresh_data=true`.

This data is **not finalized**. It is directional only and must not be used to trigger ranking/content edits before the active experiment gates. Finalized GSC remains the decision source.

## Rancho Cucamonga

Fresh signal:
- `free appliance pickup rancho cucamonga`
  - `/rancho-cucamonga-appliance-pickup/` — 1 impression, position 23
  - `/san-bernardino-appliance-pickup/` — 1 impression, position 5
  - `/southern-california-appliance-pickup/` — 1 impression, position 10

Interpretation:
- The intended Rancho owner has begun appearing in the exact-query set.
- Wrong-page ownership still exists.
- Do not alter the experiment before finalized post-change data reaches the October 14+ gate.

## Fontana

Fresh signals:
- `free appliance pickup fontana`
  - `/fontana-appliance-pickup/` — 3 impressions on Oct 5, avg position 24.33
  - `/southern-california-appliance-pickup/` — 2 impressions on Oct 5, avg position 3.5
  - `/southern-california-refrigerator-pickup/` — 2 impressions on Oct 5, avg position 24.5
  - Oct 4 also showed `/rialto-washer-dryer-pickup/` at position 2 and `/fontana-stove-oven-pickup/` at position 9 on one impression each.

Interpretation:
- The intended Fontana page is appearing more often, but the regional owner remains substantially stronger in fresh data.
- Rialto is under its own Oct 16 experiment gate, so do not counter-edit it early.

## Upland

Fresh signals:
- `free appliance pickup upland`
  - `/san-bernardino-county-appliance-pickup/` — 3 impressions, position 6
  - `/upland-washer-dryer-pickup/` — 3 impressions, position 8.67
  - intended `/upland-appliance-pickup/` did not appear in the returned fresh exact-query rows.

Interpretation:
- Early wrong-page ownership remains strong.
- Hold until finalized data reaches the Oct 14 gate.

## Fresno

Fresh data continues to show broad sibling/specialty leakage.

Examples:
- `washer dryer pickup fresno`
  - `/clovis-appliance-pickup/` — 5 impressions on Oct 6, position 5
  - `/sanger-washer-dryer-pickup/` — 3 impressions on Oct 6, position 12
  - `/clovis-appliance-pickup/` — 4 impressions on Oct 4, position 3.75
  - `/sanger-washer-dryer-pickup/` — 4 impressions on Oct 4, position 9.75
- `free appliance pickup fresno`
  - `/fresno-freezer-pickup/` — 2 impressions on Oct 5, position 1.5
  - `/fresno-refrigerator-pickup/` — 2 impressions on Oct 5, position 11.5
  - `/clovis-appliance-pickup/` — 1 impression on Oct 4, position 2
- `free washer and dryer pickup fresno`
  - `/fresno-appliance-pickup/` — 2 impressions on Oct 4, position 38.5
  - `/clovis-washer-dryer-pickup/` — 1 impression on Oct 4, position 2

Interpretation:
- Fresh data does **not** yet show clean Fresno general/laundry ownership.
- Several wrong pages have strong positions.
- Because these are incomplete/fresh rows and the pages are frozen, no change is authorized.
- This is a high-priority finalized-data review for Oct 14.

## Phoenix

Fresh exact-city rows continue to route to the intended city owner:
- `appliance recycling phoenix` → `/phoenix-appliance-pickup/` — 1 impression, position 69
- `appliance removal phoenix` → same page — 1 impression, position 92
- `appliance removal phoenix az` → same page — 1 impression, position 78
- `appliance removal phoenix, az` → same page — 1 impression, position 81

Interpretation:
- City-vs-metro ownership remains directionally clean.
- Exact-city ranking strength remains weak.
- Do not restructure ownership from fresh data.

## Denver

Fresh returned signal:
- `washer and dryer removal denver` → `/denver-washer-dryer-pickup/` — 1 impression, position 8

Interpretation:
- Dedicated laundry ownership is directionally correct.
- No fresh broad Denver exact-query row was returned in this small window.
- Denver/Lakewood broad ownership remains governed by the Oct 14 Lakewood boundary experiment.

## Sacramento / Stockton / Coachella

No exact-city rows were returned in this fresh filtered pull.

Interpretation:
- Absence is not failure.
- Continue to use finalized page/query evidence at the appropriate gates.

## Rule

This snapshot is an early-warning layer only:
1. Do not edit from fresh data.
2. Compare these patterns with finalized GSC when the experiment gates open.
3. Protect improvements that persist.
4. Treat wrong-page signals as hypotheses until finalized data confirms them.
