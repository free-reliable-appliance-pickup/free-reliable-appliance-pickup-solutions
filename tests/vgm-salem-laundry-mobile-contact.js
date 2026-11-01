#!/usr/bin/env node
// Salem laundry mobile Call/Text/Request quick-contact source regression. No network traffic or form submission.
const fs = require('node:fs');
const assert = require('node:assert/strict');
const page = fs.readFileSync('salem-washer-dryer-pickup/index.html', 'utf8');
const sharedCss = fs.readFileSync('assets/site-brand.css', 'utf8');
function verify(html) {
  assert.equal((html.match(/class="priority-mobile-cta"/g) || []).length, 1, 'one persistent mobile bar');
  const nav = html.match(/<nav class="priority-mobile-cta"[^>]*>([\s\S]*?)<\/nav>/)?.[1];
  assert(nav, 'navigation exists and closes');
  const links = [...nav.matchAll(/<a\s+href="([^"]+)"[^>]*>([^<]+)<\/a>/g)].map(m => [m[1],m[2]]);
  assert.equal(links.length, 3);
  assert.equal(links[0][0], 'tel:+15038684455');
  assert.equal(links[1][0], 'sms:+15038684455');
  assert.equal(links[2][0], '#request');
  assert.match(links[0][1], /Call 503-868-4455/);
  assert.match(links[1][1], /Text Photos/);
  assert.match(links[2][1], /Request Pickup/);
  assert.match(html, /<section[^>]*id="request"/);
  assert.match(html, /<form action="https:\/\/formspree\.io\/f\/mvzeapzd" method="POST"/);
  for(const field of ['name','phone','address','city','zip','appliance','condition','location','stairs']) {
    assert(new RegExp('name="' + field + '"[^>]*required').test(html), field + ' remains required');
  }
  assert.equal((html.match(/<img\b/g)||[]).length, 2, 'logo and one real laundry photo remain unchanged');
  assert.match(html, /assets\/laundry\/original-user-heroes\/1000274683\(5\)\.jpg/);
  assert.match(html, /<link rel="canonical" href="https:\/\/freereliableappliancepickup.com\/salem-washer-dryer-pickup\/">/);
}
verify(page);
assert.match(sharedCss, /\.priority-mobile-cta\{display:none\}/, 'bar hidden on desktop');
assert.match(sharedCss, /@media\(max-width:760px\)/, 'bar enabled at mobile breakpoint');
assert.match(sharedCss, /\.priority-mobile-cta a\{display:flex/, 'touch targets styled in existing shared CSS');
assert.match(sharedCss, /min-height:58px/, 'usable touch target size');
assert.match(sharedCss, /safe-area-inset-bottom/, 'safe area bottom support');
assert.throws(() => verify(page.replace('class="priority-mobile-cta"','class="missing-mobile-cta"')), /one persistent mobile bar/, 'negative fixture confirms missing bar fails');
console.log('PASS: Salem laundry mobile contact bar, phone/text/form and existing photo; negative fixture passes');
