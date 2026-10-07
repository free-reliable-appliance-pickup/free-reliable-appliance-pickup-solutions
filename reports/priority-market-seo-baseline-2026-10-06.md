# Priority Market SEO Baseline — 2026-10-06

## Scope

Read-only continuation of the active SEO program. This report records finalized Google Search Console evidence through 2026-10-04, current competitor structure, and technical validation for priority markets without changing protected ranking experiments.

Primary pages:
- /rancho-cucamonga-appliance-pickup/
- /fresno-appliance-pickup/
- /phoenix-appliance-pickup/
- /denver-appliance-pickup/
- /imperial-beach-appliance-pickup/

## Finalized GSC evidence through 2026-10-04

### Rancho Cucamonga
Page: /rancho-cucamonga-appliance-pickup/
- 56 impressions
- 2 clicks
- CTR 3.57%
- average position 17.21

Notable query signals:
- "free appliance recycling" — avg position 7
- "free fridge pick up near me" — avg position 6.5
- "free appliance pickup" — avg position 11

Decision:
- PROTECT.
- Current city owner is under active experiments through 2026-10-14.
- No speculative title/body/internal-link/schema/intent edit before the gate.

### Fresno
Page: /fresno-appliance-pickup/
- 21 impressions
- 0 clicks
- average position 20.14

Notable query signals:
- "appliance recycling fresno" — avg position 4
- "appliance removal fresno" — avg position 19
- "free washer and dryer pickup fresno" — avg position 38.5

Decision:
- PROTECT existing Fresno general/laundry intent boundaries through 2026-10-14.
- Do not fold laundry intent back into the general page during the current test.

### Phoenix
Page: /phoenix-appliance-pickup/
- 48 impressions
- 1 click
- CTR 2.08%
- average position 27.98

Notable query signals:
- "free appliance removal" — avg position 10
- "free appliance removal phoenix" — avg position 17
- "free appliance removal phoenix az" — avg position 19

Decision:
- Existing Phoenix city/metro separation experiment evaluates no earlier than 2026-10-09, preferred review 2026-10-16.
- Preserve the city owner, regional hub separation, phone 602-726-7552, and qualification language.

### Denver
Page: /denver-appliance-pickup/
- 18 impressions
- 0 clicks
- average position 39.83

Notable query signals:
- "appliance pick up free near me" — avg position 8
- "free refrigerator pick up" — avg position 9
- city-modified "appliance removal denver" remains weak at avg position 75.83

Decision:
- Denver intent-separation experiment evaluates no earlier than 2026-10-09, preferred review 2026-10-16.
- Do not rewrite during the observation window.
- After the gate, prioritize Denver city-modified removal intent if finalized data still shows the same split.

### Imperial Beach
Page: /imperial-beach-appliance-pickup/
- latest safe-state scan recorded 8 impressions, 2 clicks, avg position 14.63
- "free refrigerator pick up near me" recorded 2 clicks at avg position 4.5

Decision:
- PROTECT the page-one click signal.
- Do not create a speculative rewrite merely because the page is not currently in a ranking experiment.

## Current GSC opportunity scan

The 2026-09-07 through 2026-10-04 opportunity pull returned:
- homepage low-CTR opportunity — protected by homepage metadata experiment through 2026-10-14
- Upland cannibalization candidate — protected by Upland/Rancho laundry boundary experiment through 2026-10-14
- Pasadena striking-distance candidate — protected through 2026-10-13 / California cleanup through 2026-10-14
- Clovis low-CTR candidate — protected by Fresno sibling-intent experiment through 2026-10-14
- About page low-CTR candidate — protected through 2026-10-14
- Fontana cannibalization candidate — protected through 2026-10-14
- Santa Clarita removal-intent candidate — protected through 2026-10-15
- Los Angeles refrigerator-intent candidate — protected by California cleanup through 2026-10-14

Conclusion:
There is no current evidence-backed customer-facing ranking rewrite in this opportunity set that can be made without contaminating an active experiment.

## Competitor structure check

### TakeMyAppliance
Observed current pages:
- Rancho Cucamonga: https://www.takemyappliance.com/locations/southern-california/rancho-cucamonga
- Fresno: https://www.takemyappliance.com/locations/northern-california/fresno
- Phoenix: https://www.takemyappliance.com/locations/arizona/phoenix
- Denver: https://www.takemyappliance.com/locations/colorado/denver

Recurring structure:
1. exact-city owner
2. short request flow
3. local/neighborhood/ZIP coverage
4. appliance-category links
5. official/local disposal alternatives
6. FAQs
7. commercial/partner routing
8. city × appliance child pages

### AppliancePickupNow
Observed current pages:
- Fresno: https://appliancepickupnow.com/fresno/
- Phoenix: https://appliancepickupnow.com/phoenix/

Recurring structure:
1. exact-city page
2. short qualification form
3. appliance categories
4. photo-first / condition-first intake
5. local public disposal alternatives where available

## What the comparison means

The priority Free Reliable Appliance Pickup pages already contain most of the visible on-page components that competitors use: exact-city ownership, appliance categories, ZIP/neighborhood coverage, photo/condition intake, commercial/property-manager paths, local alternatives, FAQs, and exact contact routing.

Therefore:
- do not keep adding generic copy simply to match competitor word count;
- preserve city ownership and appliance-intent boundaries;
- focus post-freeze tests on queries where finalized GSC proves a gap;
- continue authority/referral/citation growth separately from on-page experiments;
- keep real operating rules even when competitors make broader free/condition claims.

## Technical source validation — 2026-10-06

Validated on main branch:
- Rancho Cucamonga: self-canonical, indexable, valid JSON-LD, one WebPage definition, title/schema aligned
- Fresno: self-canonical, indexable, valid JSON-LD, one WebPage definition, title/schema aligned
- Phoenix: self-canonical, indexable, valid JSON-LD, one WebPage definition, title/schema aligned
- Denver: self-canonical, indexable, valid JSON-LD, one WebPage definition, title/schema aligned
- Imperial Beach: self-canonical, indexable, valid JSON-LD, one WebPage definition, title/schema aligned

No verified technical defect was found that would justify breaking an active experiment freeze.

## Next gates

- Phoenix / Denver: review no earlier than 2026-10-09; preferred review 2026-10-16
- Pasadena: no earlier than 2026-10-13
- Rancho / Fresno / Upland / Clovis / Fontana / homepage / About / California cleanup: no earlier than 2026-10-14
- Santa Clarita: no earlier than 2026-10-15
- Oregon state hub / I-5 corridor: no earlier than 2026-10-16

Until each gate:
- continue read-only GSC observation;
- fix only verified technical/factual/contact/indexability/safety defects;
- do not reset title/body/internal-link/schema-intent experiments.
