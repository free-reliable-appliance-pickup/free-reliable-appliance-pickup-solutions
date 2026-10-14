# Colorado form attribution — October 14, 2026

## Completed

Added one static hidden source_page field to each existing customer Formspree form:

- Centennial: cbbd55f020938c76d8681b4f0ed4e1d0cd9d800b
- Thornton: fec53381bdaae65b9a4b66d9ddbaceb4c51f1349
- Westminster, Colorado: 51eb261c8a6a8dedfa52dbc42d194b94a405a33f
- Parker: f310dd444af24b4c202daaa1bedb7c197bd1041b

The shared customer-routing.js already inserts attribution when JavaScript loads. This change adds progressive enhancement resilience: the source page remains available if JavaScript fails or is disabled. It does not establish that normal JavaScript-enabled submissions were previously losing attribution.

## Technical exception log

This is a technical-only change under the repository experiment policy. No visible copy, titles, descriptions, canonical, schema, phone numbers, links, qualification rules, form endpoints or ranking experiment variables changed. Each commit uses the technical-fix prefix and records the reason. In particular, the Thornton observation window is not being used as an opportunity for a speculative ranking rewrite.

## Validation

- Fresh pull of all four remote commits succeeded.
- Priority intake audit: 61 forms checked, zero errors; its supplementary Foothill, High Desert and Oregon checks passed.
- Customer routing test suite: 23 regression cases, 10 appliance-condition labels, attribution and existing-field behavior passed.
- Experiment guard exited successfully for the latest technical-fix commit.
- Live HTTP checks: Denver, Aurora, Centennial, Thornton, Westminster and Parker all returned 200 and retained tel:+17206047498.
- At first live check after committing, the four new static fields were not yet visible; deployment is pending/unverified. Denver and Aurora already had static attribution.
- No real customer forms were submitted.

## Follow-up

Verify the four new fields on the public pages after deployment. Broader source attribution audit reported 260 issues across 621 active forms before these changes; this is a static audit, not evidence of 260 broken live forms. Many missing-city results are regional/state pages, and JavaScript can provide source_page dynamically. Review each result before any further edits.

No rankings, new outreach, published backlinks, or Search Console performance gains were verified in this batch. Prior backlink submissions were not repeated.
