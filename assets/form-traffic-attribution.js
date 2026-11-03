(function(){
'use strict';
/* VGM lead-source diagnosis: source page != acquisition source.
   Capture only coarse external referral evidence; never send raw referrer URLs,
   query strings, click IDs or cross-visit identifiers to Formspree. */
const TRAFFIC_SOURCE_SESSION_KEY='freeReliableSourceEvidenceV1';
function observeTrafficSource(){
  const params=new URLSearchParams(location.search||'');
  const utm=String(params.get('utm_source')||'').trim().toLowerCase();
  const medium=String(params.get('utm_medium')||'').trim().toLowerCase();
  if(params.has('gclid')||params.has('gbraid')||params.has('wbraid')||
     ((utm==='google'||utm==='googleads')&&/^(cpc|ppc|paid|paid_search)$/.test(medium)))
    return {channel:'google_paid_tagged',basis:'paid_click_tag'};
  if(params.has('fbclid'))return {channel:'facebook_link_tagged',basis:'fbclid'};
  if(utm==='facebook'||utm==='fb'||utm==='meta')
    return {channel:'facebook_tagged',basis:'utm_source'};
  if(utm==='instagram'||utm==='ig')
    return {channel:'instagram_tagged',basis:'utm_source'};
  if(utm==='google')return {channel:'google_tagged_unverified',basis:'utm_source'};
  let host='';
  try{host=new URL(document.referrer||'').hostname.toLowerCase().replace(/^www\./,'');}catch(_){}
  const own=String(location.hostname||'').toLowerCase().replace(/^www\./,'');
  if(host===own||host==='free-reliable-appliance-pickup.github.io')return null;
  if(host==='facebook.com'||host.endsWith('.facebook.com')||host==='fb.com'||host.endsWith('.fb.com'))
    return {channel:'facebook_referral',basis:'referrer_host'};
  if(host==='instagram.com'||host.endsWith('.instagram.com'))
    return {channel:'instagram_referral',basis:'referrer_host'};
  if(host==='google.com'||host.endsWith('.google.com')||/^google\.[a-z]{2,3}(?:\.[a-z]{2})?$/.test(host))
    return {channel:'google_referral_unverified',basis:'referrer_host'};
  if(host)return {channel:'other_referral',basis:'referrer_host'};
  return null;
}
function getTrafficSourceEvidence(){
  const now=Date.now(),observed=observeTrafficSource();
  let cached=null;
  try{cached=JSON.parse(sessionStorage.getItem(TRAFFIC_SOURCE_SESSION_KEY)||'null');}catch(_){}
  if(observed){
    const current={channel:observed.channel,basis:observed.basis,observed_at:now};
    try{sessionStorage.setItem(TRAFFIC_SOURCE_SESSION_KEY,JSON.stringify(current));}catch(_){}
    return current;
  }
  if(cached&&typeof cached.channel==='string'&&typeof cached.basis==='string'&&
     Number.isFinite(cached.observed_at)&&now>=cached.observed_at&&now-cached.observed_at<=1800000)
    return cached;
  return {channel:'unknown',basis:'no_external_source_signal',observed_at:now};
}
getTrafficSourceEvidence();
function putHidden(form,name,value){
  let input=form.querySelector('input[type="hidden"][name="'+name+'"]');
  if(!input){input=document.createElement('input');input.type='hidden';input.name=name;form.appendChild(input);}
  input.value=value;
}
document.addEventListener('submit',function(event){
  const form=event.target;
  if(!form||!form.matches||!form.matches('form[action*="formspree.io"]'))return;
  if(!form.querySelector('[name="city"]')||(!form.querySelector('[name="appliance"]')&&!form.querySelector('[name="appliances"]')))return;
  const source=getTrafficSourceEvidence();
  putHidden(form,'traffic_source_channel',source.channel);
  putHidden(form,'traffic_source_basis',source.basis);
},true);
})();
