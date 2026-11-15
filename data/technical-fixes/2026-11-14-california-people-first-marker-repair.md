# California people-first template marker repair — 2026-11-14

Verified failure: "Audit California People-First SEO Standard" on main, run 43674824731 and later 436770283xx.
Exact faults:
- San Gabriel Valley appliance pickup: dated SEO class marker on one priority laundry link.
- Orange County appliance pickup: same marker.
- Riverside appliance pickup: same marker and visible copy 2,201 words against the audit's 2,200-word guard.
- Los Angeles appliance pickup: same marker.

Correction:
- Replace unstyled `class="priority-laundry-local-link-20261114"` with timeless `class="priority-laundry-local-link"` on exactly one element per file. Confirmed no CSS or customer-routing JavaScript references the old class.
- Preserve all four links and their customer-facing anchor text, title, H1, canonicals, images, phone links, forms, ZIP/locality statements and intent ownership.
- In Riverside, shorten only one redundant form note sentence without changing its promise: from "A submission starts a review; it does not guarantee acceptance or a specific pickup time." to "Submitting starts a review; it does not guarantee acceptance or a pickup time." Visible word count: 2,199 by audit parser's counting method.
- No new pages, no change to accepted appliance types, no customer form submission, no claims of rankings.

All affected older experiments had earliest review dates in October 2026; no future protected window was overridden. This is a minimal verified source-quality repair; validate in CI before merge.
