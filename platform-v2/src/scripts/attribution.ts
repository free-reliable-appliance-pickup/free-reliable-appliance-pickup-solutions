type Touch = {
  page: string;
  referrer: string;
  source_channel: string;
  utm_source: string;
  utm_medium: string;
  utm_campaign: string;
  utm_term: string;
  utm_content: string;
  gclid: string;
  msclkid: string;
  fbclid: string;
  captured_at: string;
};

const STORAGE_KEY = "frap_first_touch_v1";
const SESSION_KEY = "frap_session_id_v1";

function safeHost(value: string) {
  if (!value) return "";
  try {
    return new URL(value).hostname.toLowerCase();
  } catch {
    return "";
  }
}

function classify(params: URLSearchParams, referrer: string) {
  const utmSource = (params.get("utm_source") || "").toLowerCase();
  const utmMedium = (params.get("utm_medium") || "").toLowerCase();

  if (params.get("gclid")) return "google_ads";
  if (params.get("msclkid")) return "microsoft_ads";
  if (params.get("fbclid")) return "facebook";

  if (utmSource) {
    if (utmSource.includes("google")) {
      return /cpc|ppc|paid/.test(utmMedium) ? "google_ads" : "google";
    }
    if (utmSource.includes("bing") || utmSource.includes("microsoft")) {
      return /cpc|ppc|paid/.test(utmMedium) ? "microsoft_ads" : "bing";
    }
    if (utmSource.includes("facebook") || utmSource === "fb") return "facebook";
    if (utmSource.includes("instagram")) return "instagram";
    return utmSource.replace(/[^a-z0-9_-]+/g, "_").slice(0, 80);
  }

  const host = safeHost(referrer);
  if (!host) return "direct";
  if (/(^|\.)google\./.test(host)) return "google_organic";
  if (/(^|\.)bing\.com$/.test(host)) return "bing_organic";
  if (/(^|\.)search\.yahoo\.com$/.test(host) || /(^|\.)yahoo\./.test(host)) return "yahoo_organic";
  if (/(^|\.)duckduckgo\.com$/.test(host)) return "duckduckgo_organic";
  if (/(^|\.)facebook\.com$/.test(host)) return "facebook";
  if (/(^|\.)instagram\.com$/.test(host)) return "instagram";
  return "referral";
}

function captureTouch(referrer: string): Touch {
  const params = new URLSearchParams(window.location.search);
  return {
    page: window.location.href,
    referrer,
    source_channel: classify(params, referrer),
    utm_source: params.get("utm_source") || "",
    utm_medium: params.get("utm_medium") || "",
    utm_campaign: params.get("utm_campaign") || "",
    utm_term: params.get("utm_term") || "",
    utm_content: params.get("utm_content") || "",
    gclid: params.get("gclid") || "",
    msclkid: params.get("msclkid") || "",
    fbclid: params.get("fbclid") || "",
    captured_at: new Date().toISOString()
  };
}

function getSessionId() {
  try {
    let value = sessionStorage.getItem(SESSION_KEY);
    if (!value) {
      value = crypto.randomUUID();
      sessionStorage.setItem(SESSION_KEY, value);
    }
    return value;
  } catch {
    return "";
  }
}

function getFirstTouch(current: Touch) {
  try {
    const stored = sessionStorage.getItem(STORAGE_KEY);
    if (stored) return JSON.parse(stored) as Touch;
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(current));
  } catch {
    // Storage can be unavailable in privacy modes. Current touch still works.
  }
  return current;
}

function setHidden(form: HTMLFormElement, name: string, value: string) {
  const input = form.elements.namedItem(name);
  if (input instanceof HTMLInputElement) input.value = value;
}

const currentTouch = captureTouch(document.referrer);
const firstTouch = getFirstTouch(currentTouch);
const sessionId = getSessionId();

document.querySelectorAll<HTMLFormElement>("form[data-track-lead]").forEach((form) => {
  setHidden(form, "source_channel", firstTouch.source_channel || currentTouch.source_channel);
  setHidden(form, "landing_page", firstTouch.page);
  setHidden(form, "referrer_url", firstTouch.referrer);
  setHidden(form, "utm_source", firstTouch.utm_source);
  setHidden(form, "utm_medium", firstTouch.utm_medium);
  setHidden(form, "utm_campaign", firstTouch.utm_campaign);
  setHidden(form, "utm_term", firstTouch.utm_term);
  setHidden(form, "utm_content", firstTouch.utm_content);
  setHidden(form, "gclid", firstTouch.gclid);
  setHidden(form, "msclkid", firstTouch.msclkid);
  setHidden(form, "fbclid", firstTouch.fbclid);
  setHidden(form, "session_id", sessionId);
  setHidden(form, "first_touch_json", JSON.stringify(firstTouch));
  setHidden(form, "current_touch_json", JSON.stringify(currentTouch));
});
