# VGM California regional mobile request correction — 2026-10-24

## Verified issue and scope
The already-published San Gabriel Valley regional request form required an extended access-details message, although phone, city, ZIP, appliance and condition are already required. This added unnecessary text entry on mobile before a request could be submitted. The published Inland Empire regional request form omitted the telephone keypad hint and ZIP autofill hint despite those fields being mandatory.

## Correction (existing pages only)
- San Gabriel Valley: make only the long access-details textarea optional, with an honest optional label; retain required phone, city, ZIP, appliance, condition, consent and attribution. Staff can confirm access after initial contact.
- Inland Empire: add only telephone keypad, ZIP autofill and city autofill attributes. Do not change their mandatory nature.
- Extend the existing priority intake regression to include both existing regional hubs; check mobile hints, original Formspree endpoint and source/service fields, and ensure SGV textarea remains optional with positive/negative fixtures.

## SEO experiment control and rollback
This is a usability/accessibility customer-intake correction only; no ranking content experiment and no changes to titles, H1, canonicals, robots, schema, images, phone links, descriptions or city directories. Relevant regional owner experiments have review gates ending 2026-10-14; no speculative content modifications here. Revert the PR if a form regression appears.

## Required gates and limitations
Review diff; require all applicable GitHub PR checks including priority intake, SEO Experiment Guard, phone routing, image and schema validations before merge. After merge, verify main source, GitHub Pages build and published form HTML separately. Neither deployment nor test success proves real Formspree delivery, improved conversion or better search rankings.