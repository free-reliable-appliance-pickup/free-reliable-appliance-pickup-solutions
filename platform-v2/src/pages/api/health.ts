import type { APIRoute } from "astro";
import { getSecret } from "astro:env/server";

export const prerender = false;

export const GET: APIRoute = async () => {
  const supabaseUrl = getSecret("SUPABASE_URL");
  const serviceRoleKey = getSecret("SUPABASE_SERVICE_ROLE_KEY");
  const adminPassword = getSecret("ADMIN_DASHBOARD_PASSWORD");

  const body = {
    ok: true,
    service: "free-reliable-appliance-pickup-v2-staging",
    configuration: {
      supabase_url_configured: Boolean(supabaseUrl),
      supabase_service_role_configured: Boolean(serviceRoleKey),
      admin_dashboard_password_configured: Boolean(adminPassword)
    }
  };

  return new Response(JSON.stringify(body), {
    status: 200,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "x-robots-tag": "noindex, nofollow, noarchive"
    }
  });
};
