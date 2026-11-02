#!/usr/bin/env node
// VGM narrow customer-navigation regression. No network calls or customer submissions.
const fs=require('node:fs');
const assert=require('node:assert/strict');
const hub=fs.readFileSync('refrigerator-pickup/index.html','utf8');
const local=fs.readFileSync('salem-refrigerator-freezer-pickup/index.html','utf8');
const key='<section class="refrigerator-location-choices">';
function validate(source){
  const start=source.indexOf(key);
  const end=source.indexOf('</section>',start);
  assert.ok(start>=0&&end>start,'Refrigerator city-chooser section remains present');
  const section=source.slice(start,end);
  const target='<a href="/salem-refrigerator-freezer-pickup/">Salem refrigerator &amp; freezer pickup</a>';
  assert.equal(section.split(target).length-1,1,'Exactly one matching Salem refrigerator anchor');
  assert.equal(section.includes('<a href="/salem-appliance-pickup/">Salem</a>'),false,'Do not send fridge request to generic city page');
  for(const [href,label] of [
    ['/portland-appliance-pickup/','Portland'],
    ['/denver-refrigerator-pickup/','Denver'],
    ['/phoenix-refrigerator-pickup/','Phoenix'],
    ['/fresno-refrigerator-pickup/','Fresno']
  ])assert.ok(section.includes('href="'+href+'"'),label+' existing guide preserved');
}
validate(hub);
assert.match(local,/<link rel="canonical" href="https:\/\/freereliableappliancepickup.com\/salem-refrigerator-freezer-pickup\/">/);
assert.match(local,/<meta name="robots" content="index,follow/);
assert.ok(local.includes('https://formspree.io/f/mvzeapzd'),'Existing target still accepts Formspree requests');
assert.ok(local.includes('503-868-4455'),'Existing local contact remains accessible');
assert.throws(()=>validate(hub.replace('href="/salem-refrigerator-freezer-pickup/"','href="/salem-fridge-404/"')),'Broken Salem link must fail');
console.log('PASS: Salem refrigerator hub handoff, unchanged neighbors, target canonical, contact and negative fixture');
