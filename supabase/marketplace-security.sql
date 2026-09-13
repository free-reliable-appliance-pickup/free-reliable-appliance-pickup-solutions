-- Marketplace security hardening for authenticated buyer accounts.
-- Apply AFTER marketplace-schema.sql in Supabase SQL Editor.

alter table public.marketplace_buyers
  add column if not exists user_id uuid unique references auth.users(id) on delete set null;

create index if not exists idx_marketplace_buyers_user_id
  on public.marketplace_buyers(user_id);

-- Buyers may only read their own buyer profile.
create policy "buyers_read_own_profile"
on public.marketplace_buyers
for select
to authenticated
using (auth.uid() = user_id);

-- Buyers may only update their own non-admin profile row.
create policy "buyers_update_own_profile"
on public.marketplace_buyers
for update
to authenticated
using (auth.uid() = user_id)
with check (auth.uid() = user_id);

-- Buyers may read only offers assigned to them.
create policy "buyers_read_own_offers"
on public.marketplace_offers
for select
to authenticated
using (
  exists (
    select 1 from public.marketplace_buyers b
    where b.id = marketplace_offers.buyer_id
      and b.user_id = auth.uid()
  )
);

-- Buyers may read only opportunities attached to their own offers.
-- Sensitive customer fields should still be excluded from client queries until
-- a server-side payment/assignment function marks an opportunity purchased.
create policy "buyers_read_offered_opportunities"
on public.marketplace_opportunities
for select
to authenticated
using (
  exists (
    select 1
    from public.marketplace_offers o
    join public.marketplace_buyers b on b.id = o.buyer_id
    where o.opportunity_id = marketplace_opportunities.id
      and b.user_id = auth.uid()
  )
);

-- Territories remain private by default. No public policies are added.
-- Marketplace events remain private by default. No public policies are added.

-- Safe buyer-facing view that excludes customer PII entirely.
create or replace view public.marketplace_buyer_feed
with (security_invoker = true) as
select
  o.id,
  o.created_at,
  o.status,
  o.territory_id,
  o.city,
  o.state,
  o.zip_code,
  o.approximate_area,
  o.residential_or_commercial,
  o.appliance_count,
  o.appliances,
  o.photo_urls,
  o.photo_count,
  o.visual_quality_score,
  o.completeness_score,
  o.demand_score,
  o.opportunity_class,
  o.hot_opportunity,
  o.owner_reported_summary,
  o.access_summary,
  o.urgency,
  o.opportunity_price,
  o.accepted_at,
  o.purchased_at,
  o.purchased_by,
  o.expires_at
from public.marketplace_opportunities o;

grant select on public.marketplace_buyer_feed to authenticated;

-- IMPORTANT: customer_name, customer_phone, customer_email and exact_address
-- are intentionally omitted from marketplace_buyer_feed.
-- They should only be returned by a future server-side function after verified
-- payment and assignment checks. Do not expose them directly to browser code.
