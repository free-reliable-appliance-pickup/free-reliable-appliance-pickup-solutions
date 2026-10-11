# Technical intake fix — SGV pickup forms (2026-10-10)

## Verified defect

The following live-page source forms used `required` selects whose first option was a real value: `location = First Floor` and `stairs = No Stairs`. A customer could submit the request without selecting either one, and the form would report incorrect property access details. This is a verified lead-quality / dispatch-accuracy bug, not a search-intent optimization.

Affected general appliance pages:
- `/san-marino-appliance-pickup/` — CTR-snippet experiment protected until 2026-10-15.
- `/sierra-madre-appliance-pickup/` — foothill parity experiment protected until 2026-10-14.
- `/la-canada-flintridge-appliance-pickup/` — foothill parity experiment protected until 2026-10-14.

## Correction and safeguards

Each required select now begins with a disabled, selected, empty-value prompt: `Select appliance location` or `Select stair access`. Users must explicitly disclose their floor/location and stair conditions. The existing form field names, allowed choices, phone numbers, Formspree endpoint, title/description, canonical, schema, city links, and service qualification promises are unchanged. The page experiments are otherwise frozen.

## Verification

Source checked before the update: each page had exactly one affected `location` select and one `stairs` select. PR CI should verify that standard routing/form audits remain green. After merge, test the live mobile form with unanswered access selectors to confirm native form validation blocks submission, then submit a deliberate test with accurate values to confirm intake delivery if permitted. No Formspree submission has been sent by this change.

## Reason for technical override

Partners must not receive default, possibly false `First Floor` / `No Stairs` claims; these affect carrying labor and safety. This narrow bug repair is justified during the protected ranking observation window and does not change measured SEO experiment variables.
