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

// Ventura County exceptions preserve the existing Central Coast/310 intake line.
const venturaCases = ['91320', '91360', '91362', '91377'];
for (const zip of venturaCases) {
  const route = routeForZip(zip);
  assert.ok(route.region.includes('Ventura County'), zip + ' should show Ventura County');
  assert.equal(route.href, '/central-coast-appliance-pickup/', zip + ' should use existing Ventura hub');
  assert.equal(route.phone, '310-774-4304', zip + ' should retain existing 310 phone');
  assert.equal(route.tel, '+13107744304', zip + ' should retain existing tel/sms link');
}

// Controls ensure exact ZIP exceptions do not incorrectly remap nearby LA,
// Coachella Valley, or other states/regions.
const controls = [
  ['90012', '/los-angeles-county-appliance-pickup/', '310-774-4304'],
  ['90601', '/los-angeles-county-appliance-pickup/', '310-774-4304'],
  ['90731', '/los-angeles-county-appliance-pickup/', '310-774-4304'],
  ['90802', '/los-angeles-county-appliance-pickup/', '310-774-4304'],
  ['91301', '/los-angeles-county-appliance-pickup/', '310-774-4304'],
  // 91361 crosses a county boundary: require a full address, do not auto-override.
  ['91361', '/los-angeles-county-appliance-pickup/', '310-774-4304'],
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
console.log('Homepage ZIP regression: 10 corrected city routes, 4 Ventura exceptions, 18 regional controls, 2 invalid-input cases PASS');
