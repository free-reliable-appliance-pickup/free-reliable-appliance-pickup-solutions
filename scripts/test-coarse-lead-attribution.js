// Offline regression test for coarse attribution. Never posts a form or uses live customer data.
'use strict';
const fs=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const js=fs.readFileSync('assets/lead-source-evidence.js','utf8');
const routing=fs.readFileSync('assets/customer-routing.js','utf8');
const begin=js.indexOf("const COARSE_SOURCE_KEY='frap_coarse_lead_source_v1';");
const end=js.indexOf('function putLeadSourceField(form,name,value){',begin);
assert.ok(begin>=0 && end>begin,'coarse attribution helpers must exist');
const section=js.slice(begin,end);
assert.ok(section.includes('function coarseTrafficSource()'));
function run({query='',referrer='',store={},now=Date.now(),elapsed=0,hostname='freereliableappliancepickup.com'}={}){
  let clock=now;
  const context={
    location:{search:query,hostname},
    document:{referrer},
    URL,URLSearchParams,JSON,String,Number,
    Date:{now:()=>clock,advance:()=>{clock+=elapsed}},
    sessionStorage:{
      getItem:k=>store[k]??null,
      setItem:(k,v)=>{store[k]=v}
    }
  };
  return vm.runInNewContext(section+'\nDate.advance();coarseTrafficSource();',context,{timeout:1500});
}
for(const [query,referrer,channel,basis] of [
  ['', '', 'unknown', 'no_external_source_signal'],
  ['?utm_source=facebook','','facebook_tagged','utm_source'],
  ['?utm_source=instagram','','instagram_tagged','utm_source'],
  ['?fbclid=opaque','','facebook_link_tagged','fbclid'],
  ['?gclid=opaque','','google_paid_tagged','paid_click_tag'],
  ['?utm_source=google&utm_medium=cpc','','google_paid_tagged','paid_click_tag'],
  ['?utm_source=google','','google_tagged_unverified','utm_source'],
  ['?utm_source=somepartner','','other_tagged','utm_source'],
  ['', 'https://l.facebook.com/some-path?secret=ignored','facebook_referral','referrer_host'],
  ['', 'https://www.google.com/search?q=secret','google_referral_unverified','referrer_host'],
  ['', 'https://www.google.co.uk/search?q=secret','google_referral_unverified','referrer_host'],
  ['', 'https://www.bing.com/search?q=secret','bing_referral','referrer_host'],
  ['', 'https://google.com.evil.example/','other_referral','referrer_host'],
  ['', 'https://freereliableappliancepickup.com/fontana-washer-dryer-pickup/','unknown','no_external_source_signal']
]){
  const out=run({query,referrer});
  assert.equal(out.channel,channel,query||referrer||'direct');
  assert.equal(out.basis,basis,query||referrer||'direct');
  assert.equal(JSON.stringify(out).includes('secret'),false,'never return raw referrer or query');
  assert.equal(JSON.stringify(out).includes('opaque'),false,'never return click IDs');
}
const store={};
assert.equal(run({referrer:'https://facebook.com/',store,now:5000000}).channel,'facebook_referral');
assert.equal(run({referrer:'https://freereliableappliancepickup.com/other/',store,now:5000001}).channel,'facebook_referral');
assert.equal(run({store,now:5000000+1800001}).channel,'unknown','session evidence expires after 30 minutes');
assert.equal(run({store:{},now:5000000}).channel,'unknown','private/no-referrer visit remains unknown');

assert.equal(run({query:'?gclid=opaque',now:5000000,elapsed:1800001}).channel,'unknown','unchanged landing query must expire after 30 minutes');
const legacy={frap_observed_traffic_source:'UTM: facebook',frap_observed_source_at:'5000000'};
const carried=run({referrer:'https://freereliableappliancepickup.com/rancho-cucamonga-appliance-pickup/',store:legacy,now:5000001});
assert.equal(carried.channel,'facebook_tagged','early routing evidence survives a delayed helper load on the previous page');
assert.equal(carried.basis,'routing_entry_evidence');
assert.equal(run({store:{frap_observed_traffic_source:'Google referrer',frap_observed_source_at:'5000000'},now:5000001}).channel,'google_referral_unverified');
assert.equal(run({store:{frap_observed_traffic_source:'UTM: facebook',frap_observed_source_at:'5000000'},now:5000000+1800001}).channel,'unknown','early routing source expires');
assert.match(routing,/sessionStorage\.setItem\('frap_observed_source_at',String\(Date\.now\(\)\)\)/,'early routing source timestamp is captured');
assert.match(js,/putLeadSourceField\(form,'traffic_source_channel',source\.channel\)/);
assert.match(js,/putLeadSourceField\(form,'traffic_source_basis',source\.basis\)/);
assert.match(routing,/hidden\(form,'Traffic Source \(Observed\)'/,'existing attribution remains');
assert.match(routing,/recordObservedTrafficSource\(form\)/,'existing submit hook remains');
assert.match(routing,/function initLeadAnalytics\(\)/,'GA4 preserved');
assert.match(routing,/function wireForm\(form\)/,'routing preserved');
assert.match(routing,/siteUrl\('assets\/lead-source-evidence\.js'\)/,'shared loader preserved');
assert.ok(Buffer.byteLength(routing,'utf8')<=40000,'shared routing remains within performance budget');
console.log('PASS: coarse Google/Facebook/Bing/tag/unknown classification, privacy, 30-minute cache and existing hooks.');
