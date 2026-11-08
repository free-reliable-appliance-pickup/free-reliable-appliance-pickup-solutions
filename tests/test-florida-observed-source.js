"use strict";
/**
 * Regression tests using the actual browser source-capture and Formspree
 * attribution functions, including across-page session storage.
 */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const source = fs.readFileSync("assets/customer-routing.js", "utf8");
const start = source.indexOf("function observedVisitSource(){");
const end = source.indexOf("\nfunction qualify(form)", start);
assert.ok(start >= 0 && end > start, "production capture and form source functions must exist");
const attributionScript = source.slice(start, end);
const observedField = "Traffic Source (Observed)";
const methodField = "Traffic Source Method";
const storageKey = "frap_observed_traffic_source";

/**
 * Simulate one real page visit using the production URL/referrer capture code.
 * Reusing the same Map across calls models same-tab navigation/sessionStorage.
 */
function visit({
  state = "FL",
  page = "/florida-appliance-pickup/",
  search = "",
  referrer = "",
  storage = new Map()
} = {}) {
  const form = { state, submitted: {} };
  const context = {
    URL,
    URLSearchParams,
    location: {
      hostname: "freereliableappliancepickup.com",
      pathname: page,
      search
    },
    document: { referrer },
    sessionStorage: {
      getItem(key) {
        assert.equal(key, storageKey);
        return storage.get(key) ?? null;
      },
      setItem(key, value) {
        assert.equal(key, storageKey);
        storage.set(key, value);
      }
    },
    stateCode(value) {
      const v = String(value || "").toUpperCase();
      return v === "FLORIDA" ? "FL" : v === "TEXAS" ? "TX" : v;
    },
    pagePath: () => page,
    findField(target, names) {
      return target.state && names.includes("state")
        ? { value: target.state }
        : null;
    },
    hidden(target, name, value) {
      target.submitted[name] = value;
    }
  };
  vm.runInNewContext(attributionScript, context, { filename: "customer-routing-attribution.js" });
  context.recordObservedTrafficSource(form);
  return form.submitted;
}

// The initial tagged visit must capture and remember the actual query string.
const taggedStorage = new Map();
const taggedLanding = visit({
  search: "?utm_source=facebook&utm_campaign=appliance",
  storage: taggedStorage
});
assert.equal(taggedLanding[observedField], "UTM: facebook");
assert.equal(taggedLanding[methodField], "UTM tag or website referrer");
assert.equal(taggedStorage.get(storageKey), "UTM: facebook");

// On a second city guide, same-site referrer must not override the recorded tag.
const taggedCity = visit({
  state: "Florida",
  page: "/orlando-fl-refrigerator-pickup/",
  referrer: "https://freereliableappliancepickup.com/florida-appliance-pickup/",
  storage: taggedStorage
});
assert.equal(taggedCity[observedField], "UTM: facebook");
assert.equal(taggedCity[methodField], "UTM tag or website referrer");

// An external referrer must be captured on the landing page and persisted.
const referrerStorage = new Map();
const externalLanding = visit({
  page: "/miami-fl-appliance-pickup/",
  referrer: "https://www.google.com/search?q=appliance+pickup+miami",
  storage: referrerStorage
});
assert.equal(externalLanding[observedField], "Google referrer");
assert.equal(referrerStorage.get(storageKey), "Google referrer");
const externalCity = visit({
  page: "/miami-fl-washer-dryer-pickup/",
  referrer: "https://freereliableappliancepickup.com/miami-fl-appliance-pickup/",
  storage: referrerStorage
});
assert.equal(externalCity[observedField], "Google referrer");

// Do not claim a source when the browser provided neither UTM nor referrer.
const direct = visit();
assert.equal(direct[observedField], "Direct / unknown");
assert.equal(direct[methodField], "No UTM or external referrer available");
assert.equal(visit({ referrer: "https://www.bing.com/search?q=washer" })[observedField],
  "Bing referrer");
assert.equal(visit({ referrer: "https://example.org/story" })[observedField],
  "Other referral: example.org");

// Preserve the existing Texas and Salem source-attribution behavior.
assert.equal(visit({ state: "TX", search: "?utm_source=google" })[observedField],
  "UTM: google");
assert.equal(visit({ state: "OR", page: "/salem-appliance-pickup/",
  referrer: "https://www.facebook.com/" })[observedField], "Facebook referrer");

// Do not add observed-source fields to other markets or missing-state forms.
assert.deepEqual(Object.keys(visit({ state: "CA", search: "?utm_source=google" })), []);
assert.deepEqual(Object.keys(visit({ state: null, search: "?utm_source=google" })), []);
console.log("PASS: actual Florida URL/referrer capture, session navigation, and legacy markets");
