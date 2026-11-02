// VGM: offline attribution regression checks; no real customer submissions.
const fs=require('fs');
const vm=require('vm');
const assert=require('assert').strict;
const src=fs.readFileSync('assets/form-traffic-attribution.js','utf8');
const key='freeReliableSourceEvidenceV1';

function buildBrowser(options={}){
  const values={...(options.storage||{})};
  const listeners={};
  const location={hostname:'freereliableappliancepickup.com',search:options.search||''};
  const document={
    referrer:options.referrer||'',
    addEventListener:(name,fn,capture)=>{
      assert.equal(name,'submit','Attribution only observes form submit events');
      assert.equal(capture,true,'Attribution must attach before form routing');
      listeners[name]=fn;
    },
    createElement:tag=>({tagName:tag,name:'',value:'',type:''})
  };
  const sessionStorage={
    getItem:k=>values[k]??null,
    setItem:(k,v)=>{values[k]=v;}
  };
  const context={document,location,sessionStorage,URL,URLSearchParams,Date,JSON,Number,String};
  vm.runInNewContext(src,context,{filename:'form-traffic-attribution.js'});
  assert.equal(typeof listeners.submit,'function','Must install a submit listener');
  const submit=(options={})=>{
    const fields={};
    if(options.preexisting) for(const [name,value] of Object.entries(options.preexisting))
      fields[name]={type:'hidden',name,value};
    const form={
      matches:q=>options.nonFormspree?false:q==='form[action*="formspree.io"]',
      querySelector:q=>{
        if(q==='[name="city"]')return options.noCity?null:{name:'city'};
        if(q==='[name="appliance"]')return options.noAppliance||options.pluralAppliance?null:{name:'appliance'};
        if(q==='[name="appliances"]')return options.noAppliance?null:(options.pluralAppliance?{name:'appliances'}:null);
        const m=q.match(/\[name="([^"]+)"\]/);
        return m?fields[m[1]]||null:null;
      },
      appendChild:node=>{fields[node.name]=node;return node;}
    };
    listeners.submit({target:form});
    return Object.fromEntries(Object.entries(fields).map(([k,v])=>[k,v.value]));
  };
  return {submit,values,location,document};
}
function expect(label,options,channel,basis){
  const state=buildBrowser(options);
  const fields=state.submit();
  assert.equal(fields.traffic_source_channel,channel,label+' channel');
  assert.equal(fields.traffic_source_basis,basis,label+' evidence');
  assert.equal(Object.keys(fields).sort().join(','),'traffic_source_basis,traffic_source_channel',
    label+' emits no raw URL, click IDs or other browsing data');
  console.log('PASS: '+label);
}
expect('explicit Facebook UTM',{search:'?utm_source=facebook&utm_medium=social&utm_campaign=salem_pickup'},'facebook_tagged','utm_source');
expect('Facebook click ID',{search:'?fbclid=untrusted-click-token'},'facebook_link_tagged','fbclid');
expect('Facebook referrer',{referrer:'https://l.facebook.com/l.php?u=https://freereliableappliancepickup.com/'},'facebook_referral','referrer_host');
expect('Instagram referrer',{referrer:'https://l.instagram.com/'},'instagram_referral','referrer_host');
expect('Google search page referrer is NOT proof of organic',{referrer:'https://www.google.com/search?q=salem'},'google_referral_unverified','referrer_host');
expect('Google CPC tag not miscounted as organic',{search:'?gclid=private-token'},'google_paid_tagged','paid_click_tag');
expect('Paid Google UTM not miscounted as organic',{search:'?utm_source=google&utm_medium=cpc'},'google_paid_tagged','paid_click_tag');
expect('Google UTM ambiguous',{search:'?utm_source=google&utm_medium=referral'},'google_tagged_unverified','utm_source');
expect('Unknown direct visitor',{referrer:'',search:''},'unknown','no_external_source_signal');
expect('Other external referral',{referrer:'https://example.org/article'},'other_referral','referrer_host');
expect('Fake google.example.com is NOT Google',{referrer:'https://google.com.evil.example/'},'other_referral','referrer_host');

const fb=buildBrowser({referrer:'https://l.facebook.com/'});
fb.document.referrer='https://freereliableappliancepickup.com/salem-appliance-pickup/';
const retained=fb.submit();
assert.equal(retained.traffic_source_channel,'facebook_referral','A same-site next page retains first external source');
assert.equal(retained.traffic_source_basis,'referrer_host','First external source evidence remains coarse');
console.log('PASS: Same-tab internal navigation retains observed Facebook referral');

const expired=buildBrowser({storage:{[key]:JSON.stringify({
  channel:'facebook_referral',basis:'referrer_host',observed_at:Date.now()-1800001
})}});
assert.equal(expired.submit().traffic_source_channel,'unknown','Expired 30-minute session evidence must not be reused');
console.log('PASS: Expired session evidence becomes unknown');

const unknown=buildBrowser({});
assert.equal(Object.keys(unknown.submit({nonFormspree:true})).length,0,'Never alter non-Formspree forms');
assert.equal(Object.keys(unknown.submit({noCity:true})).length,0,'Never alter forms without city');
assert.equal(Object.keys(unknown.submit({noAppliance:true})).length,0,'Never alter forms without appliance');
const plural=buildBrowser({search:'?utm_source=facebook'}).submit({pluralAppliance:true});
assert.equal(plural.traffic_source_channel,'facebook_tagged','Legacy plural appliances field still gets Facebook attribution');
assert.equal(plural.traffic_source_basis,'utm_source','Legacy plural label preserves evidence');
console.log('PASS: Legacy plural appliances form captures source evidence');
const overwrite=unknown.submit({preexisting:{traffic_source_channel:'stale',traffic_source_basis:'stale'}});
assert.equal(overwrite.traffic_source_channel,'unknown','Existing hidden source fields are updated, not duplicated');
assert.equal(Object.keys(overwrite).length,2,'Do not append duplicate attribution fields');
console.log('PASS: Invalid forms ignored and existing hidden fields updated safely');

console.log('PASS: VGM Formspree source-evidence offline tests completed; this does NOT verify live inbox delivery.');
