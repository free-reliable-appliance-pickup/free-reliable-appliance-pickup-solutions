# VGM technical exception: five Orange County mobile request forms (2026-10-24)

## Verified defect and scope

On main at `8f61a4ecd0`, the existing general appliance pickup forms for Orange, Laguna Hills, Mission Viejo, San Clemente, and Placentia have a required `type="tel"` telephone field and a ZIP field, but their markup is missing at least one of the standardized `autocomplete="tel"`, `inputmode="tel"`, `autocomplete="postal-code"`, or `inputmode="numeric"` hints. This is a mobile form usability inconsistency; it is not evidence of broken submissions, improved rankings, or partner coverage.

## Minimal change

Add only the missing phone and ZIP mobile keyboard/autofill attributes inside the existing customer forms. Keep all original required/optional states, input types, field names, Formspree endpoint, source-page and service attribution, consent behavior, telephone call links, eligibility claims, photos, metadata, canonical, schema, and internal links unchanged. No payment or test submission is made. Extend the existing priority intake source regression to cover these five pages and verify the hints.

## Experiment gates and ownership

`data/seo-experiments.json` lists active experiments for all five pages (Orange local uniqueness, Laguna Hills boundary/laundry handoff, Mission Viejo anti-template, San Clemente parity, Placentia concentration); the latest overlapping `evaluateNotBefore` dates are October 14–15, 2026. Although those dates have elapsed, ranking evaluation remains owned by Daily SEO Ranking Countermove and requires finalized GSC. This is a documented narrow technical/mobile exception only. Website Technical Repair owns emergency breakage; no emergency repair is attempted here.

## Verification and rollback

Before merge, require all applicable GitHub PR checks including priority intake, phone routing, mobile/browser checks, and SEO experiment guard to pass. Verify the main-branch source and Pages deployment separately after merge. Source checks do not prove real Formspree delivery or Google rankings. Rollback: revert the isolated PR if mobile fields or customer submissions regress; do not modify the experiment registry.
