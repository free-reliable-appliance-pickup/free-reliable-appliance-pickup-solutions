# Los Angeles Customer Conversion Checkpoint — 2026-10-08

## Confirmed business feedback
The operator reports that Los Angeles is producing the most incoming telephone calls and several real customers; other regions have generated a smaller number of inquiries. This is firsthand qualitative business feedback, **not** an independently verified call count or a claim that every call originated from Google organic search. No customer identities or contact details are recorded here.

## Finalized Google Search Console baseline
Connected Search Console property: `sc-domain:freereliableappliancepickup.com`
Observation: **2026-09-08 through 2026-10-05**, finalized GSC data.

| Landing page | Clicks | Impressions | CTR | Average position |
| --- | ---: | ---: | ---: | ---: |
| /los-angeles-appliance-pickup/ | 4 | 148 | 2.70% | 16.45 |
| /los-angeles-county-appliance-pickup/ | 0 | 4 | 0% | 4.75 |
| /los-angeles-refrigerator-pickup/ | 0 | 16 | 0% | 31.13 |
| /los-angeles-washer-dryer-pickup/ | no returned page row | — | — | — |

Site-wide over same date range: 39 clicks, 2,417 impressions, 1.61% CTR, average position 18.59.

Selected geotargeted query rows (all have zero clicks):
- `free appliance pick up los angeles`: 5 impressions; average position 15.
- `appliance removal los angeles`: 2 impressions; position 58.5.
- `refrigerator removal los angeles`: 3 impressions; position 41.33.
- `washer and dryer removal los angeles`: 2 impressions; position 18.

The query breakdown can omit low-volume/anonymized searches and **must not** be added up to reconcile page totals. A strong page-wide average is not evidence of a strong rank for an exact Los Angeles city modifier.

## Live-site and source confirmation (2026-10-08)
Reviewed deployed page: https://freereliableappliancepickup.com/los-angeles-appliance-pickup/
Source: `los-angeles-appliance-pickup/index.html` on GitHub `main`.

- Displayed Los Angeles number: **310-774-4304**, consistent in hero, call/text strip, footer/mobile CTA, metadata and structured service contact.
- Clickable `tel:+13107744304` and `sms:+13107744304` links are present, including a sticky mobile CTA.
- City request form is present; HTML method POST points to the established Formspree form endpoint.
- Form includes source attribution fields: `_subject=Los Angeles California Appliance Pickup Request`, `city=Los Angeles`, `state=California`, `source_page=Los Angeles city page`. The pickup form also asks for phone, location, appliance, condition and removal access.
- Robots directive `index, follow`; self-referencing canonical and structured WebPage are present.
- This verifies the **markup and configured endpoint**, not successful submission or delivery; do not send a fake customer request to test.
- No GA4/Tag Manager phone-click event was apparent in the inspected Los Angeles page HTML. Actual phone-call attribution cannot be computed from the Google Search Console report alone.

## SEO experiment protections
Current `data/seo-experiments.json` on `main`:
- `/los-angeles-appliance-pickup/`: protected under `2026-10-04-california-anti-template-cleanup`, evaluate not before **2026-10-14**.
- `/los-angeles-refrigerator-pickup/`: protected under `2026-10-06-los-angeles-refrigerator-concentration`, evaluate not before **2026-10-16**.
- `/los-angeles-county-appliance-pickup/`: protected under `2026-10-07-los-angeles-county-winner-protection`, evaluate not before **2026-10-17**.
- `/` homepage: current meta CTR experiment protected through **2026-10-14**.
- Determine the latest gate for every overlapping target **and support-page** experiment before any edit.

## Decision and next checks
**PROTECT AND MEASURE.** Los Angeles is already generating meaningful calls/customers according to the operator. Do not rewrite the LA city page, title, snippets, URL, canonical or internal-link ownership before Oct 14 based on only a few days of GSC observations.

1. Keep the 310 number and the working lead intake path; treat LA as highest-priority *customer-confirmed* market, without claiming it is highest by tracked revenue.
2. On/after **Oct 14**, compare finalized post-change GSC against the recorded baseline. Look specifically at the true Los Angeles queries, which page receives them, and whether qualified inquiries continue.
3. After their respective gates, examine Los Angeles refrigerator and county support pages; do not redirect/consolidate them just because GSC displays multiple URLs.
4. Plan free/low-cost source attribution for phone taps, forms and completed pickups. It will require an actual measurement destination or integration, and should not falsely count `tel:` clicks as connected calls or completed jobs.
5. Keep a simple aggregate operational tally: market, date, channel if known (Google, Facebook, repeat/referral, unknown), phone/form, qualified yes/no, booked yes/no, completed yes/no. Never log private homeowner details in this public repository.
6. Check the forms with genuine user submissions or a separate controlled test that does not pollute production inbox; an HTML review cannot prove delivery.

## Change status
**Documentation-only.** No customer-facing page, schema, call number, form, sitemap, experiment variable or deployment file changed as part of this checkpoint.
