(function(){
'use strict';
const COARSE_SOURCE_KEY='frap_coarse_lead_source_v1';
function observedCoarseTrafficSource(){
  try{
    const params=new URLSearchParams(location.search||'');
    const utm=String(params.get('utm_source')||'').trim().toLowerCase();
    const medium=String(params.get('utm_medium')||'').trim().toLowerCase();
    if(params.has('gclid')||params.has('gbraid')||params.has('wbraid')||
      ((utm==='google'||utm==='googleads')&&/^(cpc|ppc|paid|paid_search)$/.test(medium)))
      return {channel:'google_paid_tagged',basis:'paid_click_tag'};
    if(params.has('fbclid'))return {channel:'facebook_link_tagged',basis:'fbclid'};
    if(utm==='facebook'||utm==='fb'||utm==='meta')return {channel:'facebook_tagged',basis:'utm_source'};
    if(utm==='instagram'||utm==='ig')return {channel:'instagram_tagged',basis:'utm_source'};
    if(utm==='google')return {channel:'google_tagged_unverified',basis:'utm_source'};
    if(utm)return {channel:'other_tagged',basis:'utm_source'};
    const host=new URL(document.referrer||'').hostname.toLowerCase().replace(/^www\./,'');
    const own=String(location.hostname||'').toLowerCase().replace(/^www\./,'');
    if(!host||host===own||host==='free-reliable-appliance-pickup.github.io')return null;
    if(host==='facebook.com'||host.endsWith('.facebook.com')||host==='fb.com'||host.endsWith('.fb.com'))
      return {channel:'facebook_referral',basis:'referrer_host'};
    if(host==='instagram.com'||host.endsWith('.instagram.com'))
      return {channel:'instagram_referral',basis:'referrer_host'};
    if(host==='google.com'||host.endsWith('.google.com')||/^google\.[a-z]{2,3}(?:\.[a-z]{2})?$/.test(host))
      return {channel:'google_referral_unverified',basis:'referrer_host'};
    if(host==='bing.com'||host.endsWith('.bing.com'))return {channel:'bing_referral',basis:'referrer_host'};
    return {channel:'other_referral',basis:'referrer_host'};
  }catch(_){return null;}
}
function coarseTrafficSource(){
  const observed=observedCoarseTrafficSource(),now=Date.now();
  if(observed){
    try{sessionStorage.setItem(COARSE_SOURCE_KEY,JSON.stringify({...observed,at:now}));}catch(_){}
    return observed;
  }
  try{
    const cached=JSON.parse(sessionStorage.getItem(COARSE_SOURCE_KEY)||'null');
    if(cached&&typeof cached.channel==='string'&&typeof cached.basis==='string'&&
      Number.isFinite(cached.at)&&now>=cached.at&&now-cached.at<=1800000)
      return {channel:cached.channel,basis:cached.basis};
  }catch(_){}
  return {channel:'unknown',basis:'no_external_source_signal'};
}
coarseTrafficSource();

function putLeadSourceField(form,name,value){
  let field=form.querySelector('input[type="hidden"][name="'+name+'"]');
  if(!field){field=document.createElement('input');field.type='hidden';field.name=name;form.appendChild(field);}
  field.value=value;
}
document.addEventListener('submit',function(event){
  const form=event.target;
  if(!form||!form.matches||!form.matches('form[action*="formspree.io"]'))return;
  if(!form.querySelector('[name="state"]')||
     (!form.querySelector('[name="appliance"]')&&!form.querySelector('[name="appliances"]')))return;
  const source=coarseTrafficSource();
  putLeadSourceField(form,'traffic_source_channel',source.channel);
  putLeadSourceField(form,'traffic_source_basis',source.basis);
},true);
})();
