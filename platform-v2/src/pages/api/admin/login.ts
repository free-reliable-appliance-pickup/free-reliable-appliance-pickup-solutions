import type { APIRoute } from "astro";
import {
  ADMIN_COOKIE,
  expectedAdminSession,
  isValidAdminPassword
} from "../../../lib/adminAuth";

export const prerender = false;

export const POST: APIRoute = async ({ request, cookies, redirect }) => {
  const form = await request.formData();
  const password = form.get("password");

  if (typeof password !== "string" || !(await isValidAdminPassword(password))) {
    return redirect("/admin/login/?error=1", 303);
  }

  const session = await expectedAdminSession();
  if (!session) {
    return new Response("Owner dashboard is not configured.", { status: 503 });
  }

  cookies.set(ADMIN_COOKIE, session, {
    httpOnly: true,
    secure: true,
    sameSite: "strict",
    path: "/",
    maxAge: 60 * 60 * 12
  });

  return redirect("/admin/", 303);
};
