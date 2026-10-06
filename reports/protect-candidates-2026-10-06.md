# SEO Protect Candidates — 2026-10-06

## Purpose

Analysis guardrail for automatic SEO work. These pages have useful finalized Google Search Console signals in the 2026-09-06 through 2026-10-03 window and should **not** receive broad speculative rewrites while those signals are being observed.

This file does not change live page content and does not create a ranking claim. It records evidence so future batches do not overwrite a working signal just because a different query on the same page is weak.

## Strong protect candidates

### /imperial-beach-appliance-pickup/
- 8 impressions, 2 clicks, 25% observed CTR in the returned query-page rows.
- `free refrigerator pick up near me`: 2 impressions, 2 clicks, avg position 4.5.
- `appliance recycle near me`: 3 impressions, avg position 10.
- Decision: protect. Do not rewrite title/H1/body broadly without a new isolated reason.

### /hillsboro-appliance-pickup/
- 3 impressions, avg position about 4.33.
- `free washer and dryer removal`: position 1.
- `refrigerator pickup free`: position 5.
- `free appliance`: position 7.
- Decision: protect.

### /hayward-appliance-pickup/
- 4 impressions, avg position about 9.75.
- Page-one signals for `appliance pick up free`, `appliance pick up near me`, and `free disposal of appliances`.
- Decision: protect.

### /fremont-appliance-pickup/
- 2 impressions, avg position 9.5.
- `free appliance disposal near me`: position 9.
- `free appliance recycling near me`: position 10.
- Decision: protect.

### /encinitas-appliance-pickup/
- 2 impressions, avg position 7.5.
- `pick up appliances for free near me`: position 5.
- `free appliance recycling`: position 10.
- Decision: protect.

### /visalia-washer-dryer-pickup/
- 2 impressions for `free washer removal`, avg position 8.5.
- Decision: protect laundry intent.

## Partial-protect candidates

### /ladera-ranch-appliance-pickup/
- `refrigerator pickup free`: position 1 on one impression.
- Broad removal intent is much weaker.
- Decision: no full-page rewrite. Any future change must isolate broad-removal intent without disrupting refrigerator/free-pickup relevance.

### /long-beach-appliance-pickup/
- 14 impressions overall in the returned query-page rows.
- Broad `appliance removal long beach` is weak, but `free fridge pickup` is around position 9 and `refrigerator removal free` around position 10.
- Decision: no full-page rewrite. Diagnose broad-removal weakness separately.

## Operating rule

Before changing any page in this file:
1. Re-read finalized GSC data.
2. Identify the exact weak query versus the existing winning query.
3. Avoid changing variables that support the winning query unless there is a verified technical/factual problem.
4. Prefer a minimal isolated experiment over a whole-page rewrite.
