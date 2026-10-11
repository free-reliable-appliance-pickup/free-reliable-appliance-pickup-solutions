# Appliance condition and partner pickup verification
Updated October 10, 2026 — simplified at the owner's request.

## Customer-facing form: keep it simple
One required **Condition** dropdown:
- Fully working
- Working, but has a problem (explain below)
- Needs repair
- Not working
- Unknown / not sure

One nearby text box: **What works and what does not? (please explain any issues)**.
Example: "Washing machine works but makes a loud noise." When a customer reports a problem or a need for repair, the explanation is required; otherwise it can be left blank. This is intended for **all major appliances**, not just washers. No extra testing questionnaire, checkbox, or mandatory video is part of the form.

The shared `assets/customer-routing.js` provides the simple choices and description field on other Formspree intake pages as well, preserving the existing form action and routing metadata.

## Internal partner process — not extra questions on the website
- Read `condition`, `condition_details`, `Customer Defect Explanation` and `Dispatch Condition Gate` on submitted inquiries. A reported problem is a **manual review flag**; it is not an integrated dispatch blocker.
- A customer describing "works but makes a loud noise" is **not promising a fully working washer**. Disclose the report accurately to the pickup partner before they agree to drive.
- The partner decides whether the appliance and trip make sense. Obtain explicit acceptance before a distant dispatch and confirm appointment access/address.
- Free pickup remains conditional on qualifying appliances and partner/route availability; an individual broken appliance does not qualify automatically. Mixed multi-item loads may be reviewed when roughly 80% of the major appliances work.
- Only follow up about actual testing, photos or video **if needed** for a particular case; do not make customers complete a testing process in the online form or ask them to operate unsafe appliances.
- Record any mismatches at pickup and use them to improve intake quality, without presuming customers are deliberately dishonest.

This documentation replaces the superseded cycle-test, noise-question and attestation checklist from earlier October 10 edits.
