# October 14 Ownership Review Baseline — captured 2026-10-06

## Purpose

Evidence-only baseline for the October ownership experiments. This file does **not** authorize a page edit before the experiment gates.

Primary source for this capture: connected Windsor.ai `searchconsole` account `sc-domain:freereliableappliancepickup.com`, verified by a successful 186-row query/page pull for **2026-10-01 through 2026-10-03**.

Important: this is pre-change / early-change evidence for experiments changed October 3–4. It must be compared with later finalized GSC data; it is not a reason to rewrite protected pages now.

## Fresno ownership baseline

Desired owners:
- broad Fresno appliance intent → `/fresno-appliance-pickup/`
- Fresno laundry-only intent → `/fresno-washer-dryer-pickup/`

Observed October 1–3 wrong-page signals:
- `washer dryer pickup fresno` → `/clovis-washer-dryer-pickup/`: 4 impressions, avg position 3.25
- `washer dryer pickup fresno` → `/clovis-appliance-pickup/`: 4 impressions, avg position 6.75
- `free appliance pickup fresno` → `/visalia-appliance-pickup/`: 3 impressions, avg position 30
- `free appliance pickup fresno` → `/clovis-appliance-pickup/`: 2 impressions, avg position 21
- `free appliance pickup fresno` → `/sanger-appliance-pickup/`: 2 impressions, avg position 27.5
- `free appliance pickup fresno` → `/fresno-freezer-pickup/`: 1 impression, avg position 6
- `free appliance pickup fresno` → `/fresno-refrigerator-pickup/`: 1 impression, avg position 10
- `appliance recycling fresno` → `/fowler-appliance-pickup/`: 1 impression, position 19
- `appliance removal fresno` → `/fowler-appliance-pickup/`: 1 impression, position 19

Decision: **wrong-page ownership is confirmed in the baseline, but do not edit before 2026-10-14**. Success means later finalized rows migrate toward the Fresno general/laundry owner pages without losing useful visibility.

## Rancho Cucamonga ownership baseline

Desired broad owner: `/rancho-cucamonga-appliance-pickup/`

Observed `free appliance pickup rancho cucamonga` rows:
- `/san-bernardino-appliance-pickup/`: 4 impressions, avg position 4.75
- `/southern-california-refrigerator-pickup/`: 6 impressions, avg position 11.33
- `/rancho-cucamonga-refrigerator-pickup/`: 6 impressions, avg position 35.33
- `/fontana-appliance-pickup/`: 1 impression, position 11
- `/rancho-cucamonga-freezer-pickup/`: 1 impression, position 17
- `/san-gabriel-inland-empire-appliance-pickup/`: 1 impression, position 12
- `/southern-california-freezer-pickup/`: 1 impression, position 14
- `/upland-washer-dryer-pickup/`: 1 impression, position 28

The intended Rancho general page does not appear in this October 1–3 exact-query slice.

Decision: **baseline confirms strong wrong-page ownership, but the stabilization experiment changed after most/all of this evidence. Freeze through 2026-10-14.**

## Fontana ownership baseline

Desired broad owner: `/fontana-appliance-pickup/`

Observed `free appliance pickup fontana` rows:
- `/fontana-stove-oven-pickup/`: 12 impressions, avg position 19.5
- `/southern-california-appliance-pickup/`: 8 impressions, avg position 5.625
- `/rialto-washer-dryer-pickup/`: 4 impressions, avg position 6.5
- `/fontana-appliance-pickup/`: 3 impressions, avg position 18.67
- homepage: 1 impression, position 8

Decision: wrong-page ranking is clearly visible in the baseline, including strong regional/Rialto results. **Do not counter-edit until 2026-10-14 and later finalized data shows whether ownership is migrating.**

## Upland ownership baseline

Desired broad owner: `/upland-appliance-pickup/`

Observed `free appliance pickup upland` rows:
- `/upland-washer-dryer-pickup/`: 11 impressions, avg position 11.55
- `/san-bernardino-county-appliance-pickup/`: 7 impressions, avg position 16
- `/san-bernardino-appliance-pickup/`: 2 impressions, avg position 10.5
- `/san-gabriel-inland-empire-appliance-pickup/`: 2 impressions, avg position 11
- several unrelated city pages also received low-volume impressions

The intended Upland general page does not appear in this October 1–3 exact-query slice.

Decision: **baseline confirms laundry/regional leakage. Freeze through 2026-10-14.**

## Ontario ownership baseline

No Ontario-specific rows were returned in the October 1–3 filtered pull.

Decision: treat Ontario as **DISCOVERY / insufficient evidence**, not a failure.

## October 14 evaluation rule

When the gate opens:
1. Pull finalized GSC rows that include a meaningful post-change window after October 3–4.
2. Compare exact-city broad queries against this file.
3. Success = more impressions on the intended city general owner, fewer wrong-page impressions, and no material loss of useful page-one visibility.
4. If a wrong page still wins, identify the exact source of overlap before changing anything.
5. Make at most one minimal ownership/authority adjustment per experiment, then reset the observation window.


## Dependency matrix — added 2026-10-06

The wrong-page URLs in this baseline are themselves part of active experiments. The October 14 review must respect those dependency gates rather than treating every wrong page as immediately editable.

### Fresno

Most known competing Fresno-owner pages are eligible for first review on **2026-10-14**:
- `/clovis-appliance-pickup/`
- `/clovis-washer-dryer-pickup/`
- `/sanger-appliance-pickup/`
- `/fowler-appliance-pickup/`
- `/visalia-appliance-pickup/`
- `/fresno-freezer-pickup/`
- `/fresno-refrigerator-pickup/`

These are covered by the Fresno sibling/Visalia/specialty ownership experiments. If later finalized GSC shows migration to the intended Fresno owner pages, **protect the result and do not edit again**.

### Rancho Cucamonga

Known wrong/support pages and gates:
- `/san-bernardino-appliance-pickup/` — first combined safe review **2026-10-14**
- `/southern-california-refrigerator-pickup/` — **2026-10-14**
- `/rancho-cucamonga-refrigerator-pickup/` — **2026-10-14**
- `/rancho-cucamonga-freezer-pickup/` — **2026-10-14**
- `/san-gabriel-inland-empire-appliance-pickup/` — **2026-10-14**
- `/upland-washer-dryer-pickup/` — **2026-10-14**
- `/southern-california-freezer-pickup/` — **2026-10-15**

Important: if the Southern California freezer page is still materially winning the broad Rancho query, defer that part of the ownership decision until **October 15** rather than changing around a still-running support-page experiment.

### Fontana

Known wrong/support pages and gates:
- `/fontana-stove-oven-pickup/` — **2026-10-14**
- `/southern-california-appliance-pickup/` — **2026-10-14**
- `/fontana-appliance-pickup/` — **2026-10-14**
- `/rialto-washer-dryer-pickup/` — **2026-10-16**

The Rialto laundry page is part of experiment `2026-10-06-rialto-laundry-intent-concentration`. Because it currently has strong historic Fontana-query leakage, **do not declare Fontana ownership fully resolved or fully failed on October 14 if Rialto is still involved**. Re-evaluate that overlap on or after October 16 with finalized post-change data.

### Upland

Known wrong/support pages and gates:
- `/upland-washer-dryer-pickup/` — **2026-10-14**
- `/san-bernardino-county-appliance-pickup/` — **2026-10-14**
- `/san-bernardino-appliance-pickup/` — **2026-10-14**
- `/san-gabriel-inland-empire-appliance-pickup/` — **2026-10-14**

The October 14 review can evaluate Upland ownership as a group if finalized GSC includes a fair post-change window.

### Ontario

No exact-query ownership evidence was returned in the baseline. Keep Ontario **DISCOVERY** unless later finalized data produces a clear owner/wrong-page pattern.

## Review sequencing rule

The correct sequence is now:

1. **Oct 14:** Fresno, Upland and the mature portion of Rancho/Fontana ownership.
2. **Oct 15:** Rancho support overlap involving Southern California freezer intent, if still present.
3. **Oct 16:** Fontana/Rialto laundry overlap, if still present.
4. At every step, compare finalized GSC against the baseline before any edit.
5. Never modify a sibling/support page merely because it appears for the wrong query while its own experiment is still frozen.

This sequencing prevents one optimization from invalidating another active measurement.


## Finalized GSC update — through 2026-10-04

The official GSC planner now reports finalized data through **2026-10-04**.

### Rancho Cucamonga intended owner
`/rancho-cucamonga-appliance-pickup/`
- **2 clicks**
- **56 impressions**
- **3.57% CTR**
- **avg position 17.21**

Useful query signals on the intended owner include:
- `free appliance pickup` — 2 impressions, avg position 11
- `free appliance recycling` — 2 impressions, avg position 7
- `free fridge pick up near me` — 2 impressions, avg position 6.5
- `free refrigerator pickup near me` — 1 impression, position 10

Interpretation:
- The Rancho general owner now has meaningful page-level visibility and clicks.
- This is a **PROTECT** signal at the page level even though exact Rancho city ownership still needs later finalized query/page comparison.
- Do not broad-rewrite the owner page on Oct 14 merely because a wrong page still appears for one city-modified query.

### Fontana intended owner
`/fontana-appliance-pickup/`
- 0 clicks
- **24 impressions**
- **avg position 9.17**
- `free appliance pickup fontana` — 3 impressions, avg position 18.67

Interpretation:
- The Fontana owner page now has a page-one average overall.
- Treat the page-level signal as **PROTECT**.
- Exact city-modifier ownership is still weak and must be compared against Southern California / Rialto / specialty pages after their effective gates.
- Do not broad-rewrite the Fontana page if its overall page-one signal holds.

### Upland intended owner
`/upland-appliance-pickup/` still has no page-level row in the official GSC planner through Oct 4.

Interpretation: remain DISCOVERY / ownership-review mode; absence is not proof of failure.

### Fresno intended owner
`/fresno-appliance-pickup/`
- 0 clicks
- **21 impressions**
- **avg position 20.14**
- `appliance recycling fresno` — 1 impression, position 4
- `appliance removal fresno` — 1 impression, position 19
- `free washer and dryer pickup fresno` — 2 impressions, avg position 38.5

Interpretation:
- Fresno general visibility increased from 18 to 21 impressions, but ownership remains mixed.
- The general page has at least one strong exact-city recycling signal.
- Laundry intent is still not cleanly owned by the intended laundry page in the broader evidence.
- Hold all ownership changes until Oct 14+ finalized comparison.
