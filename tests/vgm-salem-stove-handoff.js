#!/usr/bin/env node
// VGM Salem stove hub customer-path check, no network or submissions.
const fs=require('node:fs'), assert=require('node:assert/strict');
const hub=fs.readFileSync('stove-oven-pickup/index.html','utf8');
const local=fs.readFileSync('salem-stove-pickup/index.html','utf8');
const key='<h2>Oregon and Colorado Stove Pickup Pages</h2>';
function validate(page){
 const a=page.indexOf(key),b=page.indexOf('</section>',a);
 assert.ok(a>=0&&b>a,'National stove local city links found');
 const block=page.slice(a,b);
 assert.equal(block.split('<a href="/salem-stove-pickup/">Salem stove &amp; range pickup</a>').length-1,1,'Exactly one Salem stove handoff');
 assert.ok(!block.includes('<a href="/salem-appliance-pickup/">Salem Appliance Pickup &amp; Removal</a>'),'Do not send stove customer to generic Salem page');
 for(const url of ['/portland-appliance-pickup/','/keizer-appliance-pickup/','/denver-appliance-pickup/','/service-areas/'])
   assert.ok(block.includes('href="'+url+'"'),'Existing local option preserved: '+url);
}
validate(hub);
assert.ok(local.includes('<link rel="canonical" href="https://freereliableappliancepickup.com/salem-stove-pickup/">'),'Self-canonical local stove URL');
assert.match(local,/<meta name="robots" content="index,follow/);
assert.ok(local.includes('https://formspree.io/f/mvzeapzd'),'Same customer Formspree route');
assert.ok(local.includes('503-868-4455'),'Same verified Oregon phone');
assert.throws(()=>validate(hub.replace('href="/salem-stove-pickup/"','href="/missing-stove-url/"')),'Broken local URL detected');
console.log('PASS: Salem stove hub target, neighbor links, canonical, phone/form and negative fixture');
