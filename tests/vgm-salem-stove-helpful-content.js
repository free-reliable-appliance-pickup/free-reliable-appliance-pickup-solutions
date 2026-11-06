#!/usr/bin/env node
// Guard the Salem stove one-section content experiment, without submitting a lead.
const fs=require('node:fs'),assert=require('node:assert/strict');
const s=fs.readFileSync('salem-stove-pickup/index.html','utf8');
const reg=JSON.parse(fs.readFileSync('data/seo-experiments.json','utf8'));
const imgs=[...s.matchAll(/<img\b[^>]*>/gi)];
assert.equal(imgs.length,1,'one stove image only');
assert.match(imgs[0][0],/\/1000238723\.jpg/,'existing stove photo retained');
for(const mark of [
 'Salem Stove &amp; Range Pickup: What to Send for Review',
 'Describe what works and what does not',
 'Plan for safe access before removal',
 'qualified professional',
 '/salem-appliance-pickup/',
 'https://formspree.io/f/mvzeapzd',
 'name="source_page" value="salem-stove-pickup"',
 'name="service" value="Salem stove and range pickup"',
 'tel:+15038684455',
 'https://freereliableappliancepickup.com/salem-stove-pickup/'
]) assert.ok(s.includes(mark),'Missing protected content: '+mark);
assert.equal((s.match(/<form\b/gi)||[]).length,1,'exactly one intake form');
assert.ok(reg.experiments.some(x=>x.id==='2026-11-03-salem-stove-useful-information'&&x.status==='running'),'registered measured experiment');
assert.ok(!s.replace(/<script\b[\s\S]*?<\/script>/gi,'').match(/guaranteed pickup|guaranteed free removal/i),'no guaranteed route claim');
const corrupted=s.replace('Describe what works and what does not','');
assert.ok(!corrupted.includes('Describe what works and what does not'),'negative fixture changes content');
console.log('PASS: Salem stove content, one photo, preserved intake, registered SEO experiment');
