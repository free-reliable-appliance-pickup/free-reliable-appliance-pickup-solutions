/* Customer request routing helper for Free Reliable Appliance Pickup.
   Operational metadata only. Never creates city URLs or indexable pages. */
(function(){
'use strict';

const FALLBACK={status:'request-only',territory_status:'available',region:'Unassigned market',lead_priority:3,partner_id:null,backup_partner_id:null,phone:null};
let routing=null,cities=null,loadPromise=null;
const n=v=>String(v||'').trim().toLowerCase();

/* Support both the primary custom domain and the legacy GitHub Pages project URL. */
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

function classify(city,state){
  const sc=stateCode(state),cn=n(city);
  if(!routing||!Array.isArray(routing.markets))return {...FALLBACK,state_code:sc,city,resolution_level:'fallback'};

  /* Exact city routes always win. */
  const exact=routing.markets.find(m=>stateCode(m.state_code||m.state)===sc&&m.city&&n(m.city)===cn);
  if(exact)return {...exact,resolution_level:'exact-city'};

  /* Regional landing-page forms sometimes submit a region/county label in the city field.
     Match that label directly to the canonical regional route before falling back statewide. */
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
    fetch(siteUrl('data/market-routing.json'),{cache:'no-store'}),
    fetch(siteUrl('data/cities.json'),{cache:'no-store'})
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

function isCustomerPickupForm(form){
  return !!(findField(form,['city','City','pickup_city'])&&findField(form,['state','State','pickup_state'])&&findField(form,['appliance','Appliance','Appliance Type']));
}

/* Keep request buttons on the current market page whenever that page already has
   a real customer pickup form. Older pages may use #pickup while newer pages use
   #request, so resolve the actual form section instead of assuming one anchor. */
function preferLocalRequestForm(){
  const forms=Array.from(document.querySelectorAll('form[action*="formspree.io"]'));
  const form=forms.find(isCustomerPickupForm);
  if(!form)return;

  let target=form.closest('section');
  if(!target)target=form;
  if(!target.id)target.id='request';
  const localHref='#'+target.id;

  const selectors=[
    'a[href="/#request"]',
    'a[href="../#request"]',
    'a[href="./#request"]',
    'a[href="https://freereliableappliancepickup.com/#request"]'
  ];
  document.querySelectorAll(selectors.join(',')).forEach(link=>link.setAttribute('href',localHref));
}

/* Real washer/dryer photography for priority laundry pages.
   Uses only business-owned photos supplied for this website and does not create
   new location pages or change pickup qualification rules. */
function pagePath(){
  let p=location.pathname||'/';
  const base=siteBase();
  if(base!=='/'&&p.startsWith(base.slice(0,-1)))p=p.slice(base.length-1)||'/';
  if(!p.startsWith('/'))p='/'+p;
  if(!p.endsWith('/'))p+='/';
  return p;
}

const WASHER_DRYER_PHOTOS={
  '/washer-dryer-pickup/':{
    src:'assets/washer-dryer-photos/washer-dryer-pickup-frontload-set.jpg',
    alt:'Real washer and dryer set submitted for appliance pickup'
  },
  '/california-washer-dryer-pickup/':{
    src:'assets/washer-dryer-photos/washer-dryer-pickup-modern-topload-set.jpg',
    alt:'Real washer and dryer set for pickup in California'
  },
  '/southern-california-washer-dryer-pickup/':{
    src:'assets/washer-dryer-photos/washer-dryer-pickup-gray-topload-set.jpg',
    alt:'Real washer and dryer set for pickup in Southern California'
  },
  '/san-gabriel-inland-empire-washer-dryer-pickup/':{
    src:'assets/washer-dryer-photos/washer-dryer-pickup-stacked-set.jpg',
    alt:'Real washer and dryer set for San Gabriel Valley and Inland Empire pickup'
  },
  '/los-angeles-county-washer-dryer-pickup/':{
    src:'assets/washer-dryer-photos/washer-dryer-pickup-frontload-set.jpg',
    alt:'Real washer and dryer set for pickup in Los Angeles County'
  },
  '/orange-county-washer-dryer-pickup/':{
    src:'assets/washer-dryer-photos/washer-dryer-pickup-modern-topload-set.jpg',
    alt:'Real washer and dryer set for pickup in Orange County'
  },
  '/riverside-county-washer-dryer-pickup/':{
    src:'assets/washer-dryer-photos/washer-dryer-pickup-gray-topload-set.jpg',
    alt:'Real washer and dryer set for pickup in Riverside County'
  },
  '/san-bernardino-county-washer-dryer-pickup/':{
    src:'assets/washer-dryer-photos/washer-dryer-pickup-stacked-set.jpg',
    alt:'Real washer and dryer set for pickup in San Bernardino County'
  }
};

function enhanceWasherDryerPhotos(){
  const path=pagePath();
  const config=WASHER_DRYER_PHOTOS[path];
  if(!config)return;

  const hero=document.querySelector('.site-hero-art img');
  if(hero){
    hero.src=siteUrl(config.src);
    hero.alt=config.alt;
    hero.removeAttribute('width');
    hero.removeAttribute('height');
    hero.decoding='async';
    hero.style.width='100%';
    hero.style.height='auto';
    hero.style.maxHeight='420px';
    hero.style.objectFit='cover';
    hero.style.borderRadius='16px';
    hero.style.boxShadow='0 12px 28px rgba(0,0,0,.18)';
  }

  /* Replace the older generic proof image on the nationwide laundry hub with
     a small gallery of real washer/dryer examples. */
  if(path==='/washer-dryer-pickup/'){
    const proof=document.querySelector('.real-appliance-proof');
    if(proof){
      const photos=[
        ['washer-dryer-pickup-frontload-set.jpg','Real front-load washer and dryer set from appliance pickup inventory'],
        ['washer-dryer-pickup-modern-topload-set.jpg','Real modern top-load washer and dryer set from appliance pickup inventory'],
        ['washer-dryer-pickup-gray-topload-set.jpg','Real gray washer and dryer set from appliance pickup inventory'],
        ['washer-dryer-pickup-stacked-set.jpg','Real stacked washer and dryer set from appliance pickup inventory']
      ];
      proof.innerHTML='<h2>Real Washer & Dryer Pickup Photos</h2><p>Examples of real washers and dryers handled through our appliance pickup work. Each customer request is reviewed separately for condition, location, access and current local coverage.</p><div class="washer-dryer-photo-grid"></div>';
      const grid=proof.querySelector('.washer-dryer-photo-grid');
      if(grid){
        grid.style.display='grid';
        grid.style.gridTemplateColumns='repeat(auto-fit,minmax(220px,1fr))';
        grid.style.gap='14px';
        photos.forEach(([file,alt])=>{
          const figure=document.createElement('figure');
          figure.style.margin='0';
          const img=document.createElement('img');
          img.src=siteUrl('assets/washer-dryer-photos/'+file);
          img.alt=alt;
          img.loading='lazy';
          img.decoding='async';
          img.style.width='100%';
          img.style.height='260px';
          img.style.objectFit='cover';
          img.style.borderRadius='10px';
          figure.appendChild(img);
          grid.appendChild(figure);
        });
      }
    }
  }
}

load();

document.addEventListener('DOMContentLoaded',()=>{
  preferLocalRequestForm();
  enhanceWasherDryerPhotos();
  document.querySelectorAll('form[action*="formspree.io"]').forEach(form=>{
    if(isCustomerPickupForm(form))wireForm(form);
  });
});

window.FreeReliableCustomerRouting={classify,qualify,load,siteBase,routingDecision,preferLocalRequestForm,enhanceWasherDryerPhotos};
})();
