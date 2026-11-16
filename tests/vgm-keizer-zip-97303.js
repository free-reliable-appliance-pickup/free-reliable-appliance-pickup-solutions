#!/usr/bin/env node
// Validate ZIP 97303 Keizer/North Salem route without opening browser, submitting leads, or fetching network content.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const home = fs.readFileSync('index.html','utf8');
const keizer = fs.readFileSync('keizer-appliance-pickup/index.html','utf8');
function route(source){
  const start = source.indexOf('function routeForZip(zip){');
  const end = source.indexOf("homepageZipForm.addEventListener('submit'",start);
  assert(start>=0 && end>start, 'homepage routing function intact');
  return vm.runInNewContext(source.slice(start,end)+'\nrouteForZip',{}, { timeout:1000 });
}
const zip = route(home);
for(const z of ['97303','97303-1234']){
  const x=zip(z);
  assert.equal(x.href,'/keizer-appliance-pickup/',z+' must resolve to local Keizer review');
  assert.equal(x.phone,'503-868-4455');
  assert.equal(x.tel,'+15038684455');
  assert.match(x.region,/Keizer \/ North Salem/);
}
for(const z of ['97301','97302','97304','97305','97306','97317']){
  assert.equal(zip(z).href,'/salem-appliance-pickup/',z+' must preserve Salem route');
}
for(const z of ['97201','97214']){
  assert.equal(zip(z).href,'/portland-appliance-pickup/',z+' must preserve Portland route');
}
assert.equal(zip('97701').href,'/oregon-appliance-pickup/','Bend remains statewide review');
assert.equal(zip('invalid'),null,'malformed input stays unrouted');
assert.match(home, /A ZIP match identifies the intake page; it never guarantees pickup/);
assert.match(keizer, /<link rel="canonical" href="https:\/\/freereliableappliancepickup.com\/keizer-appliance-pickup\/">/);
assert.match(keizer, /https:\/\/formspree.io\/f\/mvzeapzd/);
assert.equal(route(home.replace("zip:['97303']","zip:['97307']")).call(null,'97303').href, '/oregon-appliance-pickup/','negative fixture must show missing ZIP yields statewide fallback');
console.log('PASS: Keizer/North Salem ZIP 97303 local routing and preservation of Salem, Portland, Oregon fallback');
