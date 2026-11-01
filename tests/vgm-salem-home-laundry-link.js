#!/usr/bin/env node
// Read-only source validation for one Salem laundry homepage link experiment.
const fs = require('node:fs');
const assert = require('node:assert/strict');
const home = fs.readFileSync('index.html','utf8');
const salem = fs.readFileSync('salem-washer-dryer-pickup/index.html','utf8');
function verify(s) {
  const section = s.match(/<div class="card"><h3>Priority Laundry Markets<\/h3>([\s\S]*?)<\/div>/)?.[1];
  assert(section, 'homepage laundry market section missing');
  const direct = [...section.matchAll(/<a href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/g)]
    .filter(m=>m[1]==='/salem-washer-dryer-pickup/');
  assert.equal(direct.length,1,'one Salem direct laundry link in relevant section');
  assert.match(direct[0][2],/Salem washer &amp; dryer pickup page/);
  assert.doesNotMatch(section,/For Portland, Salem, Vancouver WA, Denver/,'old non-specific Salem instruction remains');
}
verify(home);
assert.match(salem, /<link rel="canonical" href="https:\/\/freereliableappliancepickup.com\/salem-washer-dryer-pickup\/">/);
assert.match(salem,/<form action="https:\/\/formspree.io\/f\/mvzeapzd" method="POST">/);
assert.throws(()=>verify(home.replace('href="/salem-washer-dryer-pickup/"','href="/salem-appliance-pickup/"')),/one Salem direct laundry link/);
console.log('PASS: homepage links Salem laundry intent directly to its existing indexable live page; negative fixture passed');
