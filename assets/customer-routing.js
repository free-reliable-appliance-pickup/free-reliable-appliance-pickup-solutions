/* Customer request routing helper for Free Reliable Appliance Pickup.
   Operational metadata only. Never creates city URLs or indexable pages. */
(function(){
'use strict';

const FALLBACK={status:'request-only',territory_status:'available',region:'Unassigned market',lead_priority:3,partner_id:null,backup_partner_id:null};
let routing=null,cities=null,loadPromise=null;
const n=v=>String(v||'').trim().toLowerCase();

function stateCode(value){
  const raw=String(value||'').trim();
  if(raw.length===2)return raw.toUpperCase();
  const map={alabama:'AL',alaska:'AK',arizona:'AZ',arkansas:'AR',california:'CA',colorado:'CO',connecticut:'CT',delaware:'DE',florida:'FL',georgia:'GA',hawaii:'HI',idaho:'ID',illinois:'IL',indiana:'IN',iowa:'IA',kansas:'KS',kentucky:'KY',louisiana:'LA',maine:'ME',maryland:'MD',massachusetts:'MA',michigan:'MI',minnesota:'MN',mississippi:'MS',missouri:'MO',montana:'MT',nebraska:'NE',nevada:'NV','new hampshire':'NH','new jersey':'NJ','new mexico':'NM','new york':'NY','north carolina':'NC','north dakota':'ND',ohio:'OH',oklahoma:'OK',oregon:'OR',pennsylvania:'PA','rhode island':'RI','south carolina':'SC','south dakota':'SD',tennessee:'TN',texas:'TX',utah:'UT',vermont:'VT',virginia:'VA',washington:'WA','west virginia':'WV',wisconsin:'WI',wyoming:'WY'};
  return map[n(raw)]||raw.toUpperCase();
}

function classify(city,state){
  if(!routing||!Array.isArray(routing.markets))return {...FALLBACK,state_code:stateCode(state),city};
  const sc=stateCode(state),cn=n(city);
  let region=null;
  if(cities&&Array.isArray(cities.cities)){
    const c=cities.cities.find(x=>stateCode(x.state_code||x.state)===sc&&n(x.city)===cn);
    if(c)region=c.region||null;
  }
  const exact=routing.markets.find(m=>stateCode(m.state_code||m.state)===sc&&m.city&&n(m.city)===cn);
  if(exact)return exact;
  if(region){
    const m=routing.markets.find(x=>stateCode(x.state_code||x.state)===sc&&!x.city&&n(x.region)===n(region));
    if(m)return m;
  }
  return {...FALLBACK,state_code:sc,city};
}

function findField(form,names){
  for(const name of names){
    const el=form.querySelector(`[name="${name}"]`)||form.querySelector('#'+name);
    if(el)return el;
  }
  return null;
}

function hidden(form,name,value){
  let el=form.querySelector(`input[type="hidden"][name="${name}"]`);
  if(!el){
    el=document.createElement('input');
    el.type='hidden';
    el.name=name;
    form.appendChild(el);
  }
  el.value=value==null?'':String(value);
}

function qualify(form){
  const city=findField(form,['city','City','pickup_city','Primary City']);
  const state=findField(form,['state','State','pickup_state','Primary State']);
  if(!city||!state)return;
  const info=classify(city.value,state.value);
  hidden(form,'Routing Region',info.region||FALLBACK.region);
  hidden(form,'Routing Market Status',info.status||FALLBACK.status);
  hidden(form,'Routing Territory Status',info.territory_status||FALLBACK.territory_status);
  hidden(form,'Routing Priority',info.lead_priority||FALLBACK.lead_priority);
  hidden(form,'Routing Partner ID',info.partner_id||'');
  hidden(form,'Routing Backup Partner ID',info.backup_partner_id||'');
  hidden(form,'Routing Source','Canonical market-routing.json');
  hidden(form,'SEO Page Creation','Disabled');
  const condition=findField(form,['condition','Condition','Appliance Condition']);
  const appliance=findField(form,['appliance','Appliance','Appliance Type']);
  const stairs=findField(form,['stairs','Stairs']);
  const access=findField(form,['access','Access','Access Notes']);
  hidden(form,'Qualification Snapshot',[appliance&&appliance.value,condition&&condition.value,stairs&&stairs.value,access&&access.value].filter(Boolean).join(' | '));
}

function load(){
  if(loadPromise)return loadPromise;
  loadPromise=Promise.all([
    fetch('/data/market-routing.json',{cache:'no-store'}),
    fetch('/data/cities.json',{cache:'no-store'})
  ]).then(async([r,c])=>{
    if(r.ok)routing=await r.json();
    if(c.ok)cities=await c.json();
  }).catch(()=>{});
  return loadPromise;
}

function wireForm(form){
  form.addEventListener('submit',async function routeBeforeSubmit(event){
    if(form.dataset.customerRoutingQualified==='1')return;
    event.preventDefault();
    await load();
    qualify(form);
    form.dataset.customerRoutingQualified='1';
    if(typeof form.requestSubmit==='function')form.requestSubmit(event.submitter||undefined);
    else form.submit();
  },true);
}

/* Start loading immediately so routing data is normally ready before a customer submits. */
load();

document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('form[action*="formspree.io"]').forEach(form=>{
    const hasCustomerFields=findField(form,['city','City','pickup_city'])&&findField(form,['state','State','pickup_state'])&&findField(form,['appliance','Appliance','Appliance Type']);
    if(hasCustomerFields)wireForm(form);
  });
});

window.FreeReliableCustomerRouting={classify,qualify,load};
})();
