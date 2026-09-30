# Cloudflare Staging Activation

The code is prepared for Cloudflare Workers staging. The live domain is not changed by this setup.

## Current staging Worker name
`free-reliable-appliance-pickup-v2-staging`

## Search protection
All public V2 pages are intentionally marked:
`noindex, nofollow`

Do not remove this protection until the production cutover checklist is complete.

## Permanent Cloudflare setup
Cloudflare Workers can deploy this existing Astro project directly. The project already includes:
- Astro Cloudflare adapter
- Wrangler configuration
- Node.js compatibility flag
- static asset binding
- observability
- a manual GitHub deployment workflow

## Required Cloudflare/GitHub deployment credentials
For the manual GitHub deployment workflow:
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_API_TOKEN`

These belong in GitHub Actions secrets, never in repository files.

## Required Worker application secrets
The deployed Worker also needs:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `ADMIN_DASHBOARD_PASSWORD`

These must be configured as Cloudflare Worker secrets. They must never be committed to GitHub.

## First staging acceptance test
1. Open the workers.dev staging URL.
2. Confirm every public response remains noindex.
3. Open the Rancho Cucamonga V2 page.
4. Submit one controlled test request.
5. Confirm the lead is written to Supabase.
6. Confirm source page and acquisition attribution are present.
7. Open the private owner dashboard.
8. Confirm the test lead appears.
9. Confirm Google reporting data is visible next to lead metrics.
10. Confirm the existing production website and its forms remain unchanged.

## Production rule
Do not attach `freereliableappliancepickup.com` to V2 until:
- SEO URL parity passes
- forms pass end-to-end testing
- admin dashboard works
- security review passes
- sitemap/canonical/robots/schema audits pass
- redirect map is ready
- rollback is ready
