# VGM — four San Gabriel Valley laundry customer-intake corrections (2026-10-24)

## Verified source defects and scope
At main `3e784d000f60beddf2d5b9b70f8d39725c988c4c`, the existing Rosemead, Temple City, Monterey Park and El Monte washer/dryer Formspree request forms each had a required phone field and `source_page` attribution, but no static optional `paid_removal_preference` choice. Phone inputs lacked mobile keyboard/autofill hints; ZIP inputs lacked postal-code autofill. These are **customer-intake consistency issues**, not proven submission failures or organic-ranking causes. All four pages have a pre-existing approved Formspree POST action.

## Exact reversible change
On each original form only, add one optional blank-default selector (`free_only` / `quote_ok`) with explicit no-booking/no-charge text, and add `inputmode="tel"`, `autocomplete="tel"`, and ZIP mobile/autofill hints. Extend the existing static-quote regression audit to these four pages. Preserve the existing Formspree endpoint, required phone/address/ZIP/condition and appliance fields, source attribution, existing city/phone routing, current eligibility, images, schema, title/meta, canonical, internal links and visible SEO sections. No new city URL, ranking experiment, backlink or paid action.

## Experiment and ownership protection
`2026-10-06-sgv-zero-visibility-laundry-cleanup-wave2` protects Rosemead and Monterey Park, with `evaluateNotBefore=2026-10-16` but `status=running`; do not change its settings or protected ranking copy. This is a documented **factual/technical intake exception** under `data/seo-experiments.json`. Daily SEO Ranking Countermove owns ranking experiments, and Website Technical Repair owns emergency breakage. No operational partner or completed pickup is inferred.

## Verification gates
1. Inspect exact PR diff and ensure only four existing forms, this evidence record and the static quote audit changed.
2. Run `python3 scripts/audit-sfv-paid-quote-static.py` and applicable phone/form, HTML, and SEO Experiment Guard checks on the exact PR head. Do not merge while required checks fail.
3. Verify merge commit, Pages deployment, and each fresh public HTML separately; a successful deployment is not proof of Formspree email delivery.
4. Roll back by reverting the PR if an actual intake regression is verified.

## Search evidence
Connected GSC SEO & Content Planner has only the settled three-day window (Oct 20–22) without comparison. Rosemead laundry returned no page row in that sample, which is **not** proof of deindexing or no demand. No ranking effect is claimed.
