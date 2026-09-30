import type { APIRoute } from "astro";
import { ADMIN_COOKIE } from "../../../lib/adminAuth";

export const prerender = false;

export const POST: APIRoute = async ({ cookies, redirect }) => {
  cookies.delete(ADMIN_COOKIE, { path: "/" });
  return redirect("/admin/login/", 303);
};
