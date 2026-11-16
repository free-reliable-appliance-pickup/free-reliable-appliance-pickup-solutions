// Offline regression test for coarse attribution. Never posts a form or uses live customer data.
'use strict';
const fs=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const js=fs.readFileSync('assets/customer-routing.js','utf8');
const begin=js.indexOf("const COARSE_SOURCE_KEY='frap_coarse_lead_source_v1';");
const end=js.indexOf('function recordObservedTrafficSource(form){',begin);
assert.ok(begin>=0 && end>begin,'coarse attribution helpers must exist');
const section=js.slice(begin,end);
assert.ok(section.includes('function coarseTrafficSource()'));
function run({query='',referrer='',store={},now=Date.now(),hostname='freereliableappliancepickup.com'}={}){
  const context={
    location:{search:query,hostname},
    document:{referrer},
    URL,URLSearchParams,JSON,String,Number,
    Date:{now:()=>now},
    sessionStorage:{
      getItem:k=>store[k]??null,
      setItem:(k,v)=>{store[k]=v}
    }
  };
  return vm.runInNewContext(section+'\ncoarseTrafficSource();',context,{timeout:1500});
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
assert.match(js,/hidden\(form,'traffic_source_channel',coarse\.channel\)/);
assert.match(js,/hidden\(form,'traffic_source_basis',coarse\.basis\)/);
assert.match(js,/hidden\(form,'Traffic Source \(Observed\)'/,'existing attribution remains');
assert.match(js,/recordObservedTrafficSource\(form\)/,'existing submit hook remains');
assert.match(js,/function initLeadAnalytics\(\)/,'GA4 preserved');
assert.match(js,/function wireForm\(form\)/,'routing preserved');
console.log('PASS: coarse Google/Facebook/Bing/tag/unknown classification, privacy, 30-minute cache and existing hooks.');
