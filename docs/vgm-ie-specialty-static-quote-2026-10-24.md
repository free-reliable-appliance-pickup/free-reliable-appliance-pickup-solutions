# VGM Inland Empire specialty-form intake audit — 2026-10-24

Source baseline: `main` f79b985551c4e3b54b25a9ba1c3258ae8203e18c. Changes limited to four existing customer forms:
- `/upland-washer-dryer-pickup/`
- `/upland-refrigerator-pickup/`
- `/ontario-washer-dryer-pickup/`
- `/montclair-washer-dryer-pickup/`

## Confirmed before change
Each existing form POSTs to the approved `https://formspree.io/f/mvzeapzd` and requires a telephone number. None had a static `paid_removal_preference` field, so no-JavaScript customers could not explicitly select free-only versus consideration of a paid quote. Montclair washer/dryer had no static `source_page` hidden input. Upland, Ontario and Montclair laundry forms lacked `inputmode="tel"` hints. All facts were checked in main source, not inferred from ranking data.

## Narrow fix
Insert one optional blank-default selector per form: free-only or may be offered a separate paid-removal quote. Selecting quote consideration does not authorize a charge, guarantee service, or create a booking. Add Montclair static source attribution; improve mobile phone input hints. Existing qualification, Formspree endpoint, phone CTA, metadata, image, links and protected ranking content remain unchanged.

## Freeze, tests and limits
The three relevant laundry experiment IDs in the changelog remain running with historical review dates. This is a verified customer-intake technical exception, not a speculative ranking edit. Regression guard `scripts/audit-sfv-paid-quote-static.py` covers exactly one static selector, its optional blank default, allowed values, required phone, endpoint and source attribution. CI must pass on the PR SHA before merge. Independently confirm Pages deployment and actual public form HTML after merge. No live Formspree email receipt or GSC ranking gain is claimed. Rollback: revert this PR if an intake regression is observed.
