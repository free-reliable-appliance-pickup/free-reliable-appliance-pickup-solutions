# Owner Dashboard

## Route
- `/admin/` — ranking + lead dashboard
- `/admin/login/` — private login

## Security
The dashboard is server-rendered and marked noindex/nofollow.
It requires `ADMIN_DASHBOARD_PASSWORD`, stored only as a Cloudflare/server secret.
The login cookie stores a SHA-256 session fingerprint, not the plain password.
Supabase's service-role key remains server-only.

## Dashboard data
The current owner view shows:
- Google impressions
- Google clicks
- tracked leads for the same reporting period
- all stored leads
- page-by-page average Google position
- CTR
- leads and progressed leads
- lead-per-click ratio
- latest pickup requests and their acquisition source

## Activation
When the staging Cloudflare Worker is created, configure these server secrets:
- SUPABASE_URL
- SUPABASE_SERVICE_ROLE_KEY
- ADMIN_DASHBOARD_PASSWORD

Do not put the service-role key or dashboard password into browser JavaScript, public GitHub files, or client-side environment variables.
