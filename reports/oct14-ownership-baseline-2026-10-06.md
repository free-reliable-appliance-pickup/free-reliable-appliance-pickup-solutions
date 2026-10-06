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
