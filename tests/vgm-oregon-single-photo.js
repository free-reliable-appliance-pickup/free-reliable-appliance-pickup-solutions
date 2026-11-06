#!/usr/bin/env node
// Source-only check for Oregon hub: one appliance image (business logo excluded).
const fs = require('node:fs'), assert = require('node:assert/strict');
const html = fs.readFileSync('oregon-appliance-pickup/index.html','utf8');
function appliancePhotos(s) {
  return [...s.matchAll(/<img\b[^>]*>/gi)].map(m=>m[0]).filter(tag=>!tag.includes('class="site-brand-logo"'));
}
assert.equal(appliancePhotos(html).length,1,'Oregon hub must show one appliance photograph');
assert.match(appliancePhotos(html)[0],/\/portland-group-appliances\.webp/,'retain original appliance garage hero');
assert.doesNotMatch(html,/<section class="real-appliance-proof">/,'remove the redundant example section');
for (const required of [
  'https://freereliableappliancepickup.com/oregon-appliance-pickup/',
  'https://formspree.io/f/mvzeapzd',
  'href="/salem-appliance-pickup/"',
  'href="/portland-appliance-pickup/"'
]) assert.ok(html.includes(required),required+' is unchanged');
// Negative fixture: the checker detects an accidentally added appliance image.
assert.equal(appliancePhotos(html+'<img src="/extra.jpg">').length,2);
console.log('PASS Oregon one-photo rule; hero, canonical, form and links preserved');
