import { getSecret } from "astro:env/server";

export const ADMIN_COOKIE = "frap_admin_session";

async function sha256(value: string) {
  const bytes = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

export async function expectedAdminSession() {
  const password = getSecret("ADMIN_DASHBOARD_PASSWORD");
  if (!password) return "";
  return sha256(`frap-admin-v1:${password}`);
}

export async function isValidAdminPassword(candidate: string) {
  const configured = getSecret("ADMIN_DASHBOARD_PASSWORD");
  if (!configured || !candidate) return false;

  const [a, b] = await Promise.all([
    sha256(`candidate:${candidate}`),
    sha256(`candidate:${configured}`)
  ]);

  if (a.length !== b.length) return false;

  let diff = 0;
  for (let i = 0; i < a.length; i++) {
    diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return diff === 0;
}
