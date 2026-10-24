# VGM technical exception: coastal Orange County customer-intake controls (2026-10-24)

## Verified baseline and scope
On `main` at `109abe1f7f85d7b292572e8e8f893124a116232d`, the existing general pickup forms for Huntington Beach, Costa Mesa, Newport Beach, and Laguna Niguel have an approved POST action (`https://formspree.io/f/mvzeapzd`), required phone, and city-specific `source_page` and `service` attribution, but no static `paid_removal_preference` selector. Laguna Niguel's phone and ZIP inputs also lack mobile keyboard/autofill hints. This is a verified intake-consistency and usability gap, **not** evidence of failed lead delivery, missing partners, or ranking loss.

## Minimal authorized repair
Add the previously approved optional blank-default free-only / paid-quote-interest selector immediately before the existing submit button on these four forms. It is available without JavaScript and does not book, charge, or promise service. Add `autocomplete=tel` and `inputmode=tel` on Laguna Niguel's required phone input, and `autocomplete=postal-code` and `inputmode=numeric` on its required ZIP input. Extend the existing static-quote and priority-intake regression audits.

## Scope and freeze protection
No changes to eligibility, service coverage, partner claims, phone numbers, Formspree action, required-field semantics, photos, titles, visible SEO sections, canonicals, structured data, sitemap, or internal linking. This is a customer-intake technical exception under `data/seo-experiments.json`; do not modify or bypass ranking freeze gates. Daily SEO Ranking Countermove owns speculative SEO experiments and Website Technical Repair owns emergency breakage.

## Verification gate
Require all applicable GitHub PR checks including SEO Experiment Guard, static quote audit, and priority intake audit on the latest PR head before merging. Verify merged source and GitHub Pages deployment separately; do not claim live HTML or Formspree receipt without independent evidence.

## Rollback
Revert the isolated PR if the form, quote consent, phone/ZIP input or attribution behavior regresses. No test customer request or paid action is authorized by this change.
