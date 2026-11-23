'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

// Execute the actual homepage ZIP routing function without submitting forms or
// changing the DOM. This test is intentionally independent of any SEO copy.
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const match = html.match(/function routeForZip\(zip\)\{([\s\S]*?)\n  \}\n\n  homepageZipForm\.addEventListener/);
assert.ok(match, 'Homepage routeForZip function must be present');
const routeForZip = new Function('zip', match[1]);

const exactCityCases = [
  ['90620', 'Buena Park, CA', '/buena-park-appliance-pickup/'],
  ['90621', 'Buena Park, CA', '/buena-park-appliance-pickup/'],
  ['90631', 'La Habra, CA', '/la-habra-appliance-pickup/'],
  ['90680', 'Stanton, CA', '/stanton-appliance-pickup/'],
  ['90630', 'Cypress, CA', '/cypress-appliance-pickup/'],
  ['90623', 'La Palma, CA', '/la-palma-appliance-pickup/'],
  ['90720', 'Los Alamitos, CA', '/los-alamitos-appliance-pickup/'],
  ['90740', 'Seal Beach, CA', '/seal-beach-appliance-pickup/'],
  ['92220', 'Banning, CA', '/banning-appliance-pickup/'],
  ['92223', 'Beaumont, CA', '/beaumont-appliance-pickup/']
];
for (const [zip, city, href] of exactCityCases) {
  const route = routeForZip(zip);
  assert.ok(route.region.includes(city), zip + ' should show its city');
  assert.equal(route.href, href, zip + ' should link to existing city intake');
  assert.equal(route.phone, '909-375-6685', zip + ' should show approved 909 phone');
  assert.equal(route.tel, '+19093756685', zip + ' should use approved tel/sms link');
}

// Controls ensure exact ZIP exceptions do not incorrectly remap nearby LA,
// Coachella Valley, or other states/regions.
const controls = [
  ['90012', '/los-angeles-county-appliance-pickup/', '310-774-4304'],
  ['90601', '/los-angeles-county-appliance-pickup/', '310-774-4304'],
  ['90731', '/los-angeles-county-appliance-pickup/', '310-774-4304'],
  ['90802', '/los-angeles-county-appliance-pickup/', '310-774-4304'],
  ['91301', '/los-angeles-county-appliance-pickup/', '310-774-4304'],
  ['91321', '/los-angeles-county-appliance-pickup/', '310-774-4304'],
  ['92601', '/orange-county-appliance-pickup/', '909-375-6685'],
  ['92801', '/orange-county-appliance-pickup/', '909-375-6685'],
  ['92234', '/coachella-valley-appliance-pickup/', '909-375-6685'],
  ['92240', '/coachella-valley-appliance-pickup/', '909-375-6685'],
  ['92501', '/riverside-county-appliance-pickup/', '909-375-6685'],
  ['92335', '/fontana-appliance-pickup/', '909-375-6685'],
  ['93001', '/central-coast-appliance-pickup/', '310-774-4304'],
  ['93003', '/central-coast-appliance-pickup/', '310-774-4304'],
  ['85004', '/phoenix-appliance-pickup/', '602-726-7552'],
  ['97201', '/portland-appliance-pickup/', '503-868-4455'],
  ['93701', '/fresno-appliance-pickup/', '310-774-4304']
];
for (const [zip, href, phone] of controls) {
  const route = routeForZip(zip);
  assert.ok(route, zip + ' must still have a route');
  assert.equal(route.href, href, zip + ' regional control');
  assert.equal(route.phone, phone, zip + ' phone control');
  assert.equal(route.tel, '+1' + phone.replace(/\D/g, ''), zip + ' tel/sms control');
}
assert.equal(routeForZip('abc'), null, 'invalid ZIP should not map');
assert.equal(routeForZip(''), null, 'blank ZIP should not map');
console.log('Homepage ZIP regression: 10 exact city routes, 17 regional controls, 2 invalid-input cases PASS');


// Guard the homepage's high-intent regional laundry handoffs. The ZIP lookup
// must continue offering general appliance pickup and a direct laundry form.
const laundryMapMatch = html.match(/var laundryLinks=\{([\s\S]*?)\n        \};/);
assert.ok(laundryMapMatch, 'Homepage laundryLinks map must be present');
const regionalLaundryLinks = new Function('return ({' + laundryMapMatch[1] + '});')();
const regionalLaundryCases = [
  ['90012', '/los-angeles-county-washer-dryer-pickup/#request'],
  ['91790', '/san-gabriel-valley-washer-dryer-pickup/#request'],
  ['92399', '/inland-empire-washer-dryer-pickup/#request'],
  ['92501', '/riverside-county-washer-dryer-pickup/#request'],
  ['92601', '/orange-county-washer-dryer-pickup/#request'],
  ['92234', '/coachella-valley-washer-dryer-pickup/#request']
];
for (const [zip, laundryHref] of regionalLaundryCases) {
  const route = routeForZip(zip);
  assert.ok(route, zip + ' must resolve to a regional intake route');
  assert.equal(regionalLaundryLinks[route.href], laundryHref, zip + ' must offer the dedicated laundry request');
  const localPath = laundryHref.split('#')[0].replace(/^\//, '');
  const pageHtml = fs.readFileSync(path.join(__dirname, '..', localPath, 'index.html'), 'utf8');
  assert.match(pageHtml, /id=["']request["']/, zip + ' laundry destination must have a request anchor');
  assert.match(pageHtml, /<form\b[^>]*action=["']https:\/\/formspree\.io\//i, zip + ' laundry destination must keep its request form');
}
console.log('Homepage regional laundry handoffs: 6 ZIP paths to existing request forms PASS');

// California laundry photo-handoff contract: check the two corrected city
// forms without sending a Formspree request or requiring any network access.
for (const city of ['diamond-bar', 'temple-city']) {
  const cityHtml = fs.readFileSync(path.join(__dirname, '..', city + '-washer-dryer-pickup', 'index.html'), 'utf8');
  const form = cityHtml.match(/<form\b[^>]*action="https:\/\/formspree\.io\/f\/mvzeapzd"[^>]*>[\s\S]*?<\/form>/i)?.[0];
  assert.ok(form, city + ' must retain its real Formspree intake form');
  assert.match(form, /<select\b(?=[^>]*\bname="photos_available")(?=[^>]*\brequired\b)[^>]*>/i,
    city + ' must ask for a required photo-sharing method');
  assert.match(form, /<input\b(?=[^>]*\bname="photo_link")(?=[^>]*\btype="url")[^>]*>/i,
    city + ' must allow an optional photo URL');
  assert.match(form, /This form does not upload photos directly/i,
    city + ' must avoid promising unsupported photo upload');
  assert.match(form, /sms:\+19093756685/, city + ' must retain the local SMS photo handoff');
}
console.log('Diamond Bar and Temple City required photo-handoff regression PASS');


// Photo sharing is required for Eastvale and Jurupa Valley washer/dryer requests.
// Keep the existing local phone and Formspree endpoint, with no fake submissions.
for (const city of ['eastvale', 'jurupa-valley']) {
  const cityHtml = fs.readFileSync(path.join(__dirname, '..', city + '-washer-dryer-pickup', 'index.html'), 'utf8');
  const form = cityHtml.match(/<form\b[^>]*action="https:\/\/formspree\.io\/f\/mvzeapzd"[^>]*>[\s\S]*?<\/form>/i)?.[0];
  assert.ok(form, city + ' must retain the original Formspree request');
  assert.match(form, /<select\b(?=[^>]*\bname="photos_available")(?=[^>]*\brequired\b)[^>]*>/i,
    city + ' must require a photo-sharing choice');
  assert.match(form, /<input\b(?=[^>]*\bname="photo_link")(?=[^>]*\btype="url")[^>]*>/i,
    city + ' must allow an optional photo link');
  assert.match(form, /This form does not upload photos directly/i,
    city + ' must not claim unsupported file upload');
  assert.match(form, /sms:\+19093756685/, city + ' must retain the local SMS photo handoff');
  assert.match(form, /name="paid_removal_preference"/, city + ' must preserve the optional paid quote choice');
}
console.log('Eastvale and Jurupa Valley photo-sharing form contract PASS');
