# Marketplace Phase 2 Checklist

## Completed in code

- Owner Control Center preview for opportunities, buyers, territories and revenue.
- Buyer dashboard preview from Phase 1.
- Supabase marketplace schema for buyers, territories, opportunities, offers and events.
- Row-level security hardening for authenticated buyers.
- Buyer-safe feed view that excludes customer name, phone, email and exact address.
- Protected/Open/Territory Available routing model documented.
- Payment-before-private-data-unlock rule preserved.

## Required before real transactions

1. Run `supabase/marketplace-schema.sql` in the Supabase SQL Editor.
2. Run `supabase/marketplace-security.sql` after the schema completes successfully.
3. Enable buyer authentication in Supabase and link each approved marketplace buyer to an `auth.users` account.
4. Select and connect a payment provider.
5. Implement a server-side claim/payment function that atomically verifies availability, records payment, assigns the buyer and only then releases customer contact information.
6. Add payment webhook verification so a browser cannot mark its own opportunity as paid.
7. Test with sample records before using real homeowner information.

## Security rule

Do not place Supabase secret keys, payment secret keys or raw homeowner private data in browser JavaScript or public GitHub files. Browser clients may use only safe public credentials and sanitized buyer-facing data.
