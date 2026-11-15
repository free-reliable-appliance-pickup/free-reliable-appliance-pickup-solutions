# Rancho Cucamonga laundry request link loop — technical fix
Date: 2026-11-14
Source page: /rancho-cucamonga-appliance-pickup/
Intended laundry guide: /rancho-cucamonga-washer-dryer-pickup/
Actual shared city request form: /rancho-cucamonga-appliance-pickup/#request

Confirmed defect: After the verified laundry request architecture repair (PR #1314), the two links on the city general page using /rancho-cucamonga-washer-dryer-pickup/#request sent users to an intermediate laundry section that itself directs users back to the city request form, adding an avoidable loop.

Narrow correction: Keep the hero's Free Washer & Dryer Pickup link pointing to the laundry guide itself (drop only #request); point the note promising "submit directly" to #request on the same city page instead. Preserves the distinct laundry information page, existing full city form, all page titles, H1, canonicals, images, service claims, phone numbers and routes. No edits to protected washer/dryer experiment page. No speculative SEO rewrite.

Verify via browser smoke and CI before merging; deployment and successful customer form delivery are separate checks.
