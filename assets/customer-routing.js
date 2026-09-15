/* Customer request routing helper for Free Reliable Appliance Pickup.
   Operational metadata only. Never creates city URLs or indexable pages. */
(function(){
'use strict';

const FALLBACK={status:'request-only',territory_status:'available',region:'Unassigned market',lead_priority:3,partner_id:null,backup_partner_id:null,phone:null};
const PRIORITY_909_PHONE='909-375-6685';
let routing=null,cities=null,loadPromise=null;
const n=v=>String(v||'').trim().toLowerCase();

/* Priority Southern California intake override.
   This keeps customer routing consistent with the public 909 priority network even
   when a community is missing from, or grouped differently inside, cities.json. */
const CA_909_PRIORITY={
  'montrose':'San Gabriel Valley','la crescenta':'San Gabriel Valley','la cañada flintridge':'San Gabriel Valley','la canada flintridge':'San Gabriel Valley','altadena':'San Gabriel Valley','pasadena':'San Gabriel Valley','south pasadena':'San Gabriel Valley','san marino':'San Gabriel Valley','san gabriel':'San Gabriel Valley','sierra madre':'San Gabriel Valley','arcadia':'San Gabriel Valley','monrovia':'San Gabriel Valley','duarte':'San Gabriel Valley','azusa':'San Gabriel Valley','glendora':'San Gabriel Valley','covina':'San Gabriel Valley','west covina':'San Gabriel Valley','san dimas':'San Gabriel Valley','la verne':'San Gabriel Valley','claremont':'San Gabriel Valley','pomona':'San Gabriel Valley','el monte':'San Gabriel Valley','south el monte':'San Gabriel Valley','baldwin park':'San Gabriel Valley','montebello':'San Gabriel Valley','la puente':'San Gabriel Valley','whittier':'San Gabriel Valley','norwalk':'San Gabriel Valley','downey':'San Gabriel Valley','rowland heights':'San Gabriel Valley','diamond bar':'San Gabriel Valley',
  'montclair':'Inland Empire','ontario':'Inland Empire','upland':'Inland Empire','rancho cucamonga':'Inland Empire','fontana':'Inland Empire','san bernardino':'Inland Empire','highland':'Inland Empire','loma linda':'Inland Empire','yucaipa':'Inland Empire','oak glen':'Inland Empire','grand terrace':'Inland Empire','bloomington':'Inland Empire','rialto':'Inland Empire','colton':'Inland Empire','redlands':'Inland Empire','muscoy':'Inland Empire','arrowhead farms':'Inland Empire','north san bernardino':'Inland Empire',
  'riverside':'Riverside County','eastvale':'Riverside County','norco':'Riverside County','moreno valley':'Riverside County','corona':'Riverside County','jurupa valley':'Riverside County','calimesa':'Riverside County','cherry valley':'Riverside County','beaumont':'Riverside County','banning':'Riverside County','temecula':'Riverside County','murrieta':'Riverside County','menifee':'Riverside County',
  'brea':'Orange County','yorba linda':'Orange County','anaheim hills':'Orange County'
};

function siteBase(){
  const host=(location.hostname||'').toLowerCase();
  if(host.endsWith('.github.io')){
    const first=(location.pathname||'/').split('/').filter(Boolean)[0];
    return first ? '/'+first+'/' : '/';
  }
  return '/';
}
function siteUrl(path){return siteBase()+String(path||'').replace(/^\/+/, '');}

function stateCode(value){
  const raw=String(value||'').trim();
  if(raw.length===2)return raw.toUpperCase();
  const map={alabama:'AL',alaska:'AK',arizona:'AZ',arkansas:'AR',california:'CA',colorado:'CO',connecticut:'CT',delaware:'DE',florida:'FL',georgia:'GA',hawaii:'HI',idaho:'ID',illinois:'IL',indiana:'IN',iowa:'IA',kansas:'KS',kentucky:'KY',louisiana:'LA',maine:'ME',maryland:'MD',massachusetts:'MA',michigan:'MI',minnesota:'MN',mississippi:'MS',missouri:'MO',montana:'MT',nebraska:'NE',nevada:'NV','new hampshire':'NH','new jersey':'NJ','new mexico':'NM','new york':'NY','north carolina':'NC','north dakota':'ND',ohio:'OH',oklahoma:'OK',oregon:'OR',pennsylvania:'PA','rhode island':'RI','south carolina':'SC','south dakota':'SD',tennessee:'TN',texas:'TX',utah:'UT',vermont:'VT',virginia:'VA',washington:'WA','west virginia':'WV',wisconsin:'WI',wyoming:'WY'};
  return map[n(raw)]||raw.toUpperCase();
}

function priority909(city,state){
  const sc=stateCode(state),cn=n(city),region=CA_909_PRIORITY[cn];
  if(sc!=='CA'||!region)return null;
  return {state:'California',state_code:'CA',city:String(city||'').trim(),region,status:'partner-recruiting',territory_status:'available',lead_priority:1,partner_id:null,backup_partner_id:null,phone:PRIORITY_909_PHONE,pricing_status:'collect_data',monthly_price_cents:null,resolution_level:'priority-909-city'};
}

function classify(city,state){
  const sc=stateCode(state),cn=n(city);
  const priority=priority909(city,state);
  if(priority)return priority;
  if(!routing||!Array.isArray(routing.markets))return {...FALLBACK,state_code:sc,city,resolution_level:'fallback'};
  const exact=routing.markets.find(m=>stateCode(m.state_code||m.state)===sc&&m.city&&n(m.city)===cn);
  if(exact)return {...exact,resolution_level:'exact-city'};
  const namedRegion=routing.markets.find(m=>stateCode(m.state_code||m.state)===sc&&!m.city&&n(m.region)===cn);
  if(namedRegion)return {...namedRegion,resolution_level:'regional'};
  let region=null;
  if(cities&&Array.isArray(cities.cities)){
    const c=cities.cities.find(x=>stateCode(x.state_code||x.state)===sc&&n(x.city)===cn);
    if(c)region=c.region||null;
  }
  if(region){
    const m=routing.markets.find(x=>stateCode(x.state_code||x.state)===sc&&!x.city&&n(x.region)===n(region));
    if(m)return {...m,resolution_level:'regional'};
  }
  if(Array.isArray(routing.state_defaults)){
    const s=routing.state_defaults.find(x=>stateCode(x.state_code||x.state)===sc);
    if(s)return {...s,city,region:s.region||((s.state||sc)+' statewide intake'),resolution_level:'statewide'};
  }
  return {...FALLBACK,state_code:sc,city,resolution_level:'fallback'};
}

function routingDecision(info){
  const status=String(info&&info.status||FALLBACK.status);
  const territory=String(info&&info.territory_status||FALLBACK.territory_status);
  if(status==='direct')return {decision:'DIRECT_OPERATION',tier:'direct-operations',action:'Review qualification and dispatch through the established company market.'};
  if(status==='partner-supported'||territory==='assigned')return {decision:'PARTNER_NETWORK',tier:'assigned-partner',action:'Review qualification and route to the assigned approved partner.'};
  if(status==='partner-recruiting')return {decision:'RECRUITING_QUEUE',tier:'partner-recruiting',action:'Keep as an intake lead while local partner coverage is being recruited; do not promise pickup.'};
  return {decision:'NATIONAL_INTAKE',tier:'request-only',action:'Accept for review only; confirm local coverage before offering or scheduling pickup.'};
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
  if(!el){el=document.createElement('input');el.type='hidden';el.name=name;form.appendChild(el);}
  el.value=value==null?'':String(value);
  return el;
}

function qualify(form){
  const city=findField(form,['city','City','pickup_city','Primary City']);
  const state=findField(form,['state','State','pickup_state','Primary State']);
  if(!city||!state)return;
  const info=classify(city.value,state.value);
  const route=routingDecision(info);
  hidden(form,'Routing City',city.value.trim());
  hidden(form,'Routing State Code',stateCode(state.value));
  hidden(form,'Routing Region',info.region||FALLBACK.region);
  hidden(form,'Routing Resolution Level',info.resolution_level||'fallback');
  hidden(form,'Routing Market Status',info.status||FALLBACK.status);
  hidden(form,'Routing Territory Status',info.territory_status||FALLBACK.territory_status);
  hidden(form,'Routing Priority',info.lead_priority||FALLBACK.lead_priority);
  hidden(form,'Routing Phone',info.phone||'');
  hidden(form,'Routing Partner ID',info.partner_id||'');
  hidden(form,'Routing Backup Partner ID',info.backup_partner_id||'');
  hidden(form,'Routing Decision',route.decision);
  hidden(form,'Routing Network Tier',route.tier);
  hidden(form,'Routing Next Action',route.action);
  hidden(form,'Coverage Promise','None until qualification and local coverage are confirmed');
  hidden(form,'Routing Source',info.resolution_level==='priority-909-city'?'Priority 909 customer-routing override':'Canonical market-routing.json');
  hidden(form,'SEO Page Creation','Disabled');
  const condition=findField(form,['condition','Condition','Appliance Condition']);
  const appliance=findField(form,['appliance','Appliance','Appliance Type']);
  const stairs=findField(form,['stairs','Stairs']);
  const access=findField(form,['access','Access','Access Notes']);
  hidden(form,'Qualification Snapshot',[appliance&&appliance.value,condition&&condition.value,stairs&&stairs.value,access&&access.value].filter(Boolean).join(' | '));
}

function load(){
  if(loadPromise)return loadPromise;
  loadPromise=Promise.all([fetch(siteUrl('data/market-routing.json'),{cache:'no-store'}),fetch(siteUrl('data/cities.json'),{cache:'no-store'})]).then(async([r,c])=>{if(r.ok)routing=await r.json();if(c.ok)cities=await c.json();}).catch(()=>{});
  return loadPromise;
}

function wireForm(form){
  if(form.dataset.customerRoutingWired==='1')return;
  form.dataset.customerRoutingWired='1';
  form.addEventListener('submit',async function routeBeforeSubmit(event){
    if(form.dataset.customerRoutingQualified==='1')return;
    event.preventDefault();
    await load();
    qualify(form);
    form.dataset.customerRoutingQualified='1';
    if(typeof form.requestSubmit==='function')form.requestSubmit(event.submitter||undefined);else form.submit();
  },true);
}

function isCustomerPickupForm(form){return !!(findField(form,['city','City','pickup_city'])&&findField(form,['state','State','pickup_state'])&&findField(form,['appliance','Appliance','Appliance Type']));}

function pagePath(){
  let p=location.pathname||'/';
  const base=siteBase();
  if(base!=='/'&&p.startsWith(base.slice(0,-1)))p=p.slice(base.length-1)||'/';
  if(!p.startsWith('/'))p='/'+p;
  if(!p.endsWith('/'))p+='/';
  return p;
}

const WASHER_DRYER_PHOTOS={
  '/california-washer-dryer-pickup/':{hero:'front-load-laundry-set.jpg',alt:'Real washer and dryer set for pickup in California'},
  '/southern-california-washer-dryer-pickup/':{hero:'washer-dryer-set.jpg',alt:'Real washer and dryer set for pickup in Southern California'},
  '/san-gabriel-inland-empire-washer-dryer-pickup/':{hero:'stacked-laundry-center.jpg',alt:'Real washer and dryer set for San Gabriel Valley and Inland Empire pickup'},
  '/los-angeles-county-washer-dryer-pickup/':{hero:'front-load-laundry-set.jpg',alt:'Real washer and dryer set for pickup in Los Angeles County'},
  '/orange-county-washer-dryer-pickup/':{hero:'laundry-pair.jpg',alt:'Real washer and dryer set for pickup in Orange County'},
  '/riverside-county-washer-dryer-pickup/':{hero:'washer-dryer-set.jpg',alt:'Real washer and dryer set for pickup in Riverside County'},
  '/san-bernardino-county-washer-dryer-pickup/':{hero:'stacked-laundry-center.jpg',alt:'Real washer and dryer set for pickup in San Bernardino County'}
};

const CA_WASHER_DRYER_PAGES=new Set(Object.keys(WASHER_DRYER_PHOTOS));
const LAUNDRY_GALLERY=[['front-load-laundry-set.jpg','Front-load washer and dryer set from our appliance work'],['laundry-pair.jpg','Washer and dryer pair from our appliance work'],['washer-dryer-set.jpg','Washer and dryer set available for pickup review'],['stacked-laundry-center.jpg','Stacked laundry center from our appliance work'],['top-load-washer.jpg','Top-load washer from our appliance work'],['front-load-dryer.jpg','Front-load dryer from our appliance work']];

function ensureRegionalState(form){if(findField(form,['state','State','pickup_state','Primary State']))return;if(CA_WASHER_DRYER_PAGES.has(pagePath()))hidden(form,'state','CA');}

function preferLocalRequestForm(){
  const forms=Array.from(document.querySelectorAll('form[action*="formspree.io"]'));
  forms.forEach(ensureRegionalState);
  const form=forms.find(isCustomerPickupForm);
  if(!form)return;
  let target=form.closest('section');if(!target)target=form;if(!target.id)target.id='request';
  const localHref='#'+target.id;
  const selectors=['a[href="/#request"]','a[href="../#request"]','a[href="./#request"]','a[href="https://freereliableappliancepickup.com/#request"]'];
  document.querySelectorAll(selectors.join(',')).forEach(link=>link.setAttribute('href',localHref));
}

function buildLaundryGallery(path){
  if(document.querySelector('.site-laundry-photo-showcase'))return;
  const main=document.querySelector('main');if(!main)return;
  const pageIndex=Math.max(0,Object.keys(WASHER_DRYER_PHOTOS).indexOf(path));
  const picks=[LAUNDRY_GALLERY[pageIndex%LAUNDRY_GALLERY.length],LAUNDRY_GALLERY[(pageIndex+2)%LAUNDRY_GALLERY.length],LAUNDRY_GALLERY[(pageIndex+4)%LAUNDRY_GALLERY.length]];
  const section=document.createElement('section');section.className='site-laundry-photo-showcase';
  const h2=document.createElement('h2');h2.textContent='Real Washer & Dryer Photos';
  const p=document.createElement('p');p.textContent='Real appliance photos from our pickup work and inventory. Send clear photos of your own washer or dryer so we can review condition, access and local route availability.';
  const grid=document.createElement('div');grid.style.display='grid';grid.style.gridTemplateColumns='repeat(auto-fit,minmax(210px,1fr))';grid.style.gap='14px';
  picks.forEach(([file,alt])=>{const figure=document.createElement('figure');figure.style.margin='0';const img=document.createElement('img');img.src=siteUrl('assets/laundry/'+file);img.alt=alt;img.loading='lazy';img.decoding='async';img.style.width='100%';img.style.height='250px';img.style.objectFit='cover';img.style.borderRadius='12px';img.style.boxShadow='0 8px 22px rgba(0,0,0,.12)';figure.appendChild(img);grid.appendChild(figure);});
  section.append(h2,p,grid);main.insertBefore(section,main.firstChild);
}

function enhanceWasherDryerPhotos(){
  const path=pagePath();const config=WASHER_DRYER_PHOTOS[path];if(!config)return;
  const src=siteUrl('assets/laundry/'+config.hero);const hero=document.querySelector('.site-hero-art img');
  if(hero){hero.src=src;hero.alt=config.alt;hero.removeAttribute('width');hero.removeAttribute('height');hero.decoding='async';hero.style.width='100%';hero.style.height='auto';hero.style.maxHeight='420px';hero.style.objectFit='cover';hero.style.borderRadius='16px';hero.style.boxShadow='0 12px 28px rgba(0,0,0,.18)';}
  buildLaundryGallery(path);
}

load();
document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('form[action*="formspree.io"]').forEach(ensureRegionalState);
  preferLocalRequestForm();enhanceWasherDryerPhotos();
  document.querySelectorAll('form[action*="formspree.io"]').forEach(form=>{if(isCustomerPickupForm(form))wireForm(form);});
});

window.FreeReliableCustomerRouting={classify,qualify,load,siteBase,routingDecision,preferLocalRequestForm,enhanceWasherDryerPhotos,priority909};
})();
