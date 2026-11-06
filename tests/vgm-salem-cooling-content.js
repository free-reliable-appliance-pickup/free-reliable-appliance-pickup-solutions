#!/usr/bin/env node
// Source-only; no customer submission or Google ranking claims.
const fs=require('node:fs'),assert=require('node:assert/strict');
const html=fs.readFileSync('salem-refrigerator-freezer-pickup/index.html','utf8');
const reg=JSON.parse(fs.readFileSync('data/seo-experiments.json','utf8'));
assert.equal((html.match(/<img\b/gi)||[]).length,1,'one existing inventory photo');
assert.match(html,/rancho-cucamonga-refrigerator-real-french-door-20261016\.jpg/);
assert.equal((html.match(/<form\b/gi)||[]).length,1,'one request form');
for(const x of ['Which Salem refrigerators and freezers qualify for pickup review?','Refrigerators: condition details that help','Upright and chest freezers: what to report','Salem pickup access and safe preparation','Never puncture or cut refrigerant lines','https://formspree.io/f/mvzeapzd','name="source_page" value="salem-refrigerator-freezer-pickup"','name="service" value="Refrigerator and freezer pickup"','tel:+15038684455','https://freereliableappliancepickup.com/salem-refrigerator-freezer-pickup/'])assert.ok(html.includes(x),'missing: '+x);
assert.ok(reg.experiments.some(x=>x.id==='2026-11-03-salem-cooling-preparation-intent'&&x.status==='running'),'missing experiment');
const bad=html.replace('Never puncture or cut refrigerant lines','');
assert.ok(!bad.includes('Never puncture or cut refrigerant lines'),'negative fixture');
console.log('PASS Salem refrigerator/freezer guidance, single photo, request form and registry');
