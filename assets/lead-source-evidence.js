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
const DOCUMENT_SOURCE=observedCoarseTrafficSource();
const DOCUMENT_SOURCE_TIME=Date.now();
function isRecentSource(at,now){return Number.isFinite(at)&&at>0&&now>=at&&now-at<=1800000;}
function earlyRoutingSource(now){
  // The already-loaded routing script records early entry evidence before this helper downloads.
  try{
    const at=Number(sessionStorage.getItem('frap_observed_source_at')||0);
    if(!isRecentSource(at,now))return null;
    const raw=String(sessionStorage.getItem('frap_observed_traffic_source')||'').trim().toLowerCase();
    let channel='';
    if(raw==='google referrer')channel='google_referral_unverified';
    else if(raw==='facebook referrer')channel='facebook_referral';
    else if(raw==='instagram referrer')channel='instagram_referral';
    else if(raw==='bing referrer')channel='bing_referral';
    else if(raw==='yahoo referrer')channel='other_referral';
    else if(raw.startsWith('other referral: '))channel='other_referral';
    else if(raw.startsWith('utm: ')){
      const tag=raw.slice(5);
      if(tag==='facebook'||tag==='fb'||tag==='meta')channel='facebook_tagged';
      else if(tag==='instagram'||tag==='ig')channel='instagram_tagged';
      else if(tag==='google')channel='google_tagged_unverified';
      else channel='other_tagged';
    }
    if(!channel)return null;
    return {channel,basis:'routing_entry_evidence',at};
  }catch(_){return null;}
}
function coarseTrafficSource(){
  const now=Date.now();
  if(DOCUMENT_SOURCE&&isRecentSource(DOCUMENT_SOURCE_TIME,now)){
    // Use original entry time, not submit time; never renew evidence on a long-open page.
    const entry={...DOCUMENT_SOURCE,at:DOCUMENT_SOURCE_TIME};
    try{sessionStorage.setItem(COARSE_SOURCE_KEY,JSON.stringify(entry));}catch(_){}
    return {channel:entry.channel,basis:entry.basis};
  }
  try{
    const cached=JSON.parse(sessionStorage.getItem(COARSE_SOURCE_KEY)||'null');
    if(cached&&typeof cached.channel==='string'&&typeof cached.basis==='string'&&isRecentSource(cached.at,now))
      return {channel:cached.channel,basis:cached.basis};
  }catch(_){}
  const prior=earlyRoutingSource(now);
  if(prior){
    try{sessionStorage.setItem(COARSE_SOURCE_KEY,JSON.stringify(prior));}catch(_){}
    return {channel:prior.channel,basis:prior.basis};
  }
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
