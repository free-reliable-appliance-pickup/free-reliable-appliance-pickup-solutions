// VGM: offline source attribution regression; never submit actual Formspree data.
const fs=require('node:fs'),vm=require('node:vm'),a=require('node:assert/strict');
const source=fs.readFileSync('assets/form-traffic-attribution.js','utf8');
const key='freeReliableSourceEvidenceV1';
function check({query='',ref='',store={},plural=false,noCity=false,noAppliance=false,otherForm=false}={}){
 const fields={};let listener;
 const document={referrer:ref,createElement:()=>({name:'',type:'',value:''}),
   addEventListener:(event,fn,capture)=>{a.equal(event,'submit');a.equal(capture,true);listener=fn}};
 const form={
   matches:()=>!otherForm,
   querySelector:q=>{
     if(q==='[name="city"]')return noCity?null:{};
     if(q==='[name="appliance"]')return plural||noAppliance?null:{};
     if(q==='[name="appliances"]')return plural&&!noAppliance?{}:null;
     return fields[q.match(/name="([^"]+)"/)?.[1]]||null;
   },
   appendChild:el=>{fields[el.name]=el}
 };
 const sessionStorage={getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v}};
 vm.runInNewContext(source,{document,location:{search:query,hostname:'freereliableappliancepickup.com'},sessionStorage,URL,URLSearchParams,Date,Number,String,JSON},{timeout:1000});
 a.equal(typeof listener,'function');listener({target:form});
 return Object.fromEntries(Object.entries(fields).map(([k,v])=>[k,v.value]));
}
for(const [query,ref,channel,basis] of [
 ['?utm_source=facebook','','facebook_tagged','utm_source'],
 ['?fbclid=masked','','facebook_link_tagged','fbclid'],
 ['','https://l.facebook.com/','facebook_referral','referrer_host'],
 ['','https://instagram.com/','instagram_referral','referrer_host'],
 ['','https://www.google.com/search?q=salem','google_referral_unverified','referrer_host'],
 ['?gclid=masked','','google_paid_tagged','paid_click_tag'],
 ['?utm_source=google&utm_medium=cpc','','google_paid_tagged','paid_click_tag'],
 ['?utm_source=google','','google_tagged_unverified','utm_source'],
 ['','','unknown','no_external_source_signal'],
 ['','https://elsewhere.example/','other_referral','referrer_host'],
 ['','https://google.com.evil.example/','other_referral','referrer_host']
 ]){
 const x=check({query,ref});a.equal(x.traffic_source_channel,channel);
 a.equal(x.traffic_source_basis,basis);a.deepEqual(Object.keys(x).sort(),['traffic_source_basis','traffic_source_channel']);
}
a.equal(check({query:'?utm_source=facebook',plural:true}).traffic_source_channel,'facebook_tagged');
const store={};check({ref:'https://l.facebook.com/',store});
a.equal(check({ref:'https://freereliableappliancepickup.com/other/',store}).traffic_source_channel,'facebook_referral');
a.equal(check({store:{[key]:JSON.stringify({channel:'facebook_referral',basis:'referrer_host',observed_at:Date.now()-1800001})}}).traffic_source_channel,'unknown');
for(const opt of [{otherForm:true},{noCity:true},{noAppliance:true}]){
 a.deepEqual(check(opt),{});
}
for(const city of ['eugene','grants-pass','springfield']){
 for(const kind of ['freezer','refrigerator','washer-dryer']){
 const file=city+'-'+kind+'-pickup/index.html',html=fs.readFileSync(file,'utf8');
 a.equal(html.split('<script src="../assets/form-traffic-attribution.js" defer></script>').length-1,1,file);
 a.ok(html.includes('https://formspree.io/f/mvzeapzd'),file);
 a.match(html,/name="city"/);a.match(html,/name="appliance"/);
 a.ok(!html.includes('src="../assets/customer-routing.js"'),file);
 }
}
console.log('PASS: source types, no leaked URLs, 30-minute evidence, singular/plural forms, negative fixtures, nine Oregon page entry points.');
