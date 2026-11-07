"use strict";
/* Regression tests for what Formspree actually receives as an observed source. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const source = fs.readFileSync("assets/customer-routing.js", "utf8");
const start = source.indexOf("function recordObservedTrafficSource(form){");
const end = source.indexOf("\nfunction qualify(form)", start);
assert.ok(start >= 0 && end > start, "customer-source function must exist");
const functionBody = source.slice(start, end);

function submit({state, page="/florida-appliance-pickup/", observed="", remembered=""}) {
  const form = {state, submitted: {}};
  const runtime = {
    CURRENT_OBSERVED_SOURCE: observed,
    stateCode: value => {
      const v = String(value || "").toUpperCase();
      return v === "FLORIDA" ? "FL" : v === "TEXAS" ? "TX" : v;
    },
    pagePath: () => page,
    findField: (target, names) => target.state && names.includes("state")
      ? {value: target.state} : null,
    hidden: (target, name, value) => {target.submitted[name] = value;},
    sessionStorage: {getItem: name => {
      assert.equal(name, "frap_observed_traffic_source");
      return remembered;
    }}
  };
  vm.runInNewContext(functionBody, runtime);
  runtime.recordObservedTrafficSource(form);
  return form.submitted;
}

const observed = "Traffic Source (Observed)";
const method = "Traffic Source Method";
assert.equal(submit({state:"FL", observed:"UTM: facebook"})[observed], "UTM: facebook",
  "Florida hub submissions preserve observed tagged traffic");
assert.equal(submit({state:"Florida", observed:"Google referrer"})[observed], "Google referrer",
  "Florida state name forms are tracked");
assert.equal(submit({state:"FL", page:"/orlando-fl-refrigerator-pickup/", observed:"Bing referrer"})[observed],
  "Bing referrer", "dedicated Florida city forms keep referrer labels");
assert.equal(submit({state:"FL", remembered:"Facebook referrer"})[observed],
  "Facebook referrer", "same-session referrer survives internal navigation");
const direct = submit({state:"FL"});
assert.equal(direct[observed], "Direct / unknown", "unknown source is not invented");
assert.equal(direct[method], "No UTM or external referrer available");
assert.equal(submit({state:"TX", observed:"UTM: google"})[observed], "UTM: google",
  "existing Texas source tracking remains in place");
assert.equal(submit({state:"OR", page:"/salem-appliance-pickup/", observed:"Other referral: example.org"})[observed],
  "Other referral: example.org", "existing Salem source tracking remains in place");
assert.deepEqual(Object.keys(submit({state:"CA", observed:"Google referrer"})), [],
  "unrelated states are unchanged");
assert.deepEqual(Object.keys(submit({state:null, observed:"Google referrer"})), [],
  "forms without state field are unchanged");
console.log("PASS: 9 Florida/Texas/Salem observed-source regression checks");
