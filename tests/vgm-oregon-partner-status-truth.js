#!/usr/bin/env node
// Source-only regression guard: no customers, network, or browser forms.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const source = fs.readFileSync('assets/partner-routing.js', 'utf8');
const routing = JSON.parse(fs.readFileSync('data/market-routing.json', 'utf8'));
const cityData = JSON.parse(fs.readFileSync('data/cities.json', 'utf8'));

function reviewer(js) {
  const sandbox = { document: { addEventListener() {} }, window: {} };
  vm.runInNewContext(js, sandbox, { filename: 'assets/partner-routing.js', timeout: 1000 });
  return sandbox.window.FreeReliablePartnerRouting;
}
const labels = reviewer(source);
assert.equal(typeof labels.label, 'function');
assert.equal(typeof labels.decision, 'function');

const metro = (city, region) => {
  assert(cityData.cities.some(c => c.city === city && c.state_code === 'OR' && c.region === region), city + ' absent from approved catalog');
  const regionRecord = routing.markets.find(m => m.state_code === 'OR' && m.region === region && !m.city);
  assert(regionRecord, region + ' missing from routing');
  return { ...regionRecord, resolution_level: 'regional' };
};

let tested = 0;
for (const [city, region] of [
  ['Woodburn', 'Salem Metro'], ['Monmouth', 'Salem Metro'],
  ['McMinnville', 'Salem Metro'], ['Keizer', 'Salem Metro'],
  ['Beaverton', 'Portland Metro'], ['Hillsboro', 'Portland Metro'],
  ['Oregon City', 'Portland Metro'], ['Wilsonville', 'Portland Metro'],
]) {
  const info = metro(city, region);
  assert.equal(labels.decision(info).decision, 'DIRECT_OVERFLOW_CANDIDATE');
  const publicText = labels.label(info);
  assert.match(publicText, /confirm local pickup route/);
  assert.doesNotMatch(publicText, /Established operation/);
  tested++;
}
for (const city of ['Salem', 'Portland']) {
  const info = routing.markets.find(x => x.state_code === 'OR' && x.city === city);
  assert(info, city + ' missing exact market record');
  assert.match(labels.label({ ...info, resolution_level: 'exact-city' }), /Established operation/);
  tested++;
}
const nonOregon = {
  status: 'direct', territory_status: 'protected', state_code: 'CO',
  region: 'Denver Metro', resolution_level: 'regional'
};
assert.match(labels.label(nonOregon), /Established operation/);
tested++;
const coast = metro('Astoria', 'Oregon Coast');
assert.match(labels.label(coast), /Partner recruiting/);
tested++;

// Negative fixture: deleting the Oregon regional exception must make a test fail.
const mutated = source.replace("info.state_code==='OR'", "info.state_code==='ZZ'");
assert.notEqual(mutated, source, 'negative fixture did not mutate code');
assert.match(labels.label(metro('Woodburn', 'Salem Metro')), /confirm local pickup route/);
assert.match(reviewer(mutated).label(metro('Woodburn', 'Salem Metro')), /Established operation/);
tested++;

console.log('PASS VGM Oregon partner status accuracy; cases=' + tested + '; negative fixture=1');
