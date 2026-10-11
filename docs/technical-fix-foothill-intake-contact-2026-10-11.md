# [technical-fix] Foothill intake access and contact routing — 2026-10-11

## Independently verified technical defects
- La Crescenta form has required `location` and `stairs` selects with nonblank first options, silently submitting First Floor / No Stairs without a customer choice.
- La Crescenta and Montrose display 909-375-6685 in their hero, metadata and primary CTA, but contain 310-774-4304 in explanatory text and the mobile footer tel/sms links.
- Verified against live page content and current main branch source on 2026-10-11. The main form action remains Formspree `mvzeapzd`.

## Experiment freeze exception
`data/seo-experiments.json` has a running `2026-10-04-california-anti-template-cleanup` experiment protecting both pages through `evaluateNotBefore: 2026-10-14` (preferred review 2026-10-20). These are factual customer-contact and intake-access defects; this fix does not change titles, canonical, SEO body strategy, intent ownership, schema, images, routing, qualifications or internal links.

## Reversible batch
- `la-crescenta-appliance-pickup/index.html`: require an explicit floor and stairs choice; unify contact references to the existing 909 market number.
- `montrose-appliance-pickup/index.html`: unify the contradictory 310 footer/text references to the existing 909 market number.
- `scripts/audit-priority-pickup-forms.py`: regression checks for blank required select prompts and 909 call/text consistency on both foothill pages.

## Verification required before deployment claim
Run `python3 scripts/audit-priority-pickup-forms.py` and all existing form, phone-routing, JSON-LD, image, gold-standard, SEO safety and experiment guard workflows. Confirm Pages deployment and both live pages after merge. No change to existing customer submissions or permissions.
