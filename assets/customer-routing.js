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
const COMPRESSED_LAUNDRY_REPLACEMENTS={
  'washer-dryer-pickup-frontload-set.jpg':'front-load-laundry-set.jpg',
  'washer-dryer-pickup-gray-topload-set.jpg':'laundry-pair.jpg',
  'washer-dryer-pickup-modern-topload-set.jpg':'washer-dryer-set.jpg',
  'washer-dryer-pickup-stacked-set.jpg':'stacked-laundry-center.jpg'
};

/* One existing city page targets washer-only, dryer-only and complete-set searches.
   These are presentation enhancements only; no new city URLs are generated here. */
const PREMIUM_CITY_LAUNDRY_SEARCH={
  '/pasadena-washer-dryer-pickup/':{city:'Pasadena',area:'San Gabriel Valley',washer:'For Pasadena washer pickup requests, tell us whether the machine fills, washes, drains and spins. Apartments, garages and multi-unit properties are welcome for review when floor level, stairs and loading access are included.',dryer:'For Pasadena dryer pickup requests, identify gas or electric service and whether the drum turns and produces heat. Clear access and parking details help the local route review.',set:'A working matching washer and dryer set in Pasadena receives strong priority because both machines can often be handled together for reuse.'},
  '/la-canada-flintridge-washer-dryer-pickup/':{city:'La Cañada Flintridge',area:'western San Gabriel Valley',washer:'For La Cañada Flintridge washer pickup, include tested functions plus driveway grade, gates, steps and carrying distance when the laundry room is away from the driveway.',dryer:'For La Cañada Flintridge dryer pickup, identify gas or electric, whether it turns and heats, and any narrow side-yard or interior access that affects removal.',set:'Complete working washer and dryer sets in La Cañada Flintridge receive strong priority, especially when photos show both machines and the full removal path.'},
  '/arcadia-washer-dryer-pickup/':{city:'Arcadia',area:'San Gabriel Valley',washer:'Arcadia washer pickup requests are reviewed faster when photos show the machine, model label and access from the laundry area to the pickup vehicle.',dryer:'For Arcadia dryer pickup, identify gas or electric service, heating performance and any stairs, gates or tight doorways before scheduling.',set:'Working washer and dryer sets in Arcadia receive strong consideration because matching pairs can often be routed together for reuse.'},
  '/monrovia-washer-dryer-pickup/':{city:'Monrovia',area:'San Gabriel Valley',washer:'For Monrovia washer pickup, report whether the machine fills, agitates or tumbles, drains and spins, plus any leaks or error codes.',dryer:'For Monrovia dryer pickup, identify gas or electric, whether the drum turns and whether it produces heat. Include garage, side-yard or interior access details.',set:'A complete working laundry pair in Monrovia can receive priority review when both appliances are submitted in the same request.'},
  '/azusa-washer-dryer-pickup/':{city:'Azusa',area:'San Gabriel Valley',washer:'Azusa washer pickup requests should include clear photos and a short condition check: fill, wash, drain and spin, plus floor level and stairs.',dryer:'Azusa dryer pickup requests should identify gas or electric service and whether the drum turns and heats so the appliance can be reviewed correctly.',set:'Working washer and dryer sets in Azusa receive strong priority when both machines are complete, accessible and ready for route review.'},
  '/covina-washer-dryer-pickup/':{city:'Covina',area:'San Gabriel Valley',washer:'For free washer pickup review in Covina, send photos, tested functions and any access details such as apartments, stairs, garages or narrow gates.',dryer:'For free dryer pickup review in Covina, tell us gas or electric, whether it turns and heats, and where the dryer is located on the property.',set:'Matching working washer and dryer sets in Covina receive especially strong consideration because they can often stay together for reuse.'},
  '/west-covina-washer-dryer-pickup/':{city:'West Covina',area:'San Gabriel Valley',washer:'West Covina washer pickup requests are easiest to review when the working condition, floor level, parking and removal path are clear from the start.',dryer:'West Covina dryer pickup requests should identify gas or electric service, heating status and whether stairs or long carries are involved.',set:'Complete working washer and dryer sets in West Covina receive priority review when both appliances and the access path are shown clearly.'},
  '/pomona-washer-dryer-pickup/':{city:'Pomona',area:'Pomona Valley',washer:'For Pomona washer pickup, include clear appliance photos, whether it completes a cycle and whether the machine is on the ground floor, in a garage or inside the home.',dryer:'For Pomona dryer pickup, identify gas or electric, drum and heat condition, plus stairs, gates and parking access.',set:'Pomona sits on the transition between the San Gabriel Valley and Inland Empire routes, making complete working washer and dryer sets especially useful for coordinated pickup review.'},
  '/ontario-washer-dryer-pickup/':{city:'Ontario',area:'Inland Empire',washer:'Ontario washer pickup requests should include tested washer functions, photos, floor level and loading access so the Inland Empire route can review the request efficiently.',dryer:'Ontario dryer pickup requests should identify gas or electric service and whether the drum turns and heats, along with any apartment or stair access.',set:'Working matching washer and dryer sets in Ontario receive strong priority because both machines can often be routed together.'},
  '/rancho-cucamonga-washer-dryer-pickup/':{city:'Rancho Cucamonga',area:'Inland Empire',washer:'For Rancho Cucamonga washer pickup, include machine condition plus driveway, gate, stair and carrying-distance details when access is not straightforward.',dryer:'For Rancho Cucamonga dryer pickup, identify gas or electric service, heat performance and where the dryer sits relative to vehicle access.',set:'Clean, complete working washer and dryer sets in Rancho Cucamonga receive strong priority for local reuse routing.'},
  '/fontana-washer-dryer-pickup/':{city:'Fontana',area:'Inland Empire',washer:'Fontana washer pickup requests are reviewed using the machine condition, clear photos, floor level, stairs and local route capacity.',dryer:'Fontana dryer pickup requests should identify gas or electric service, drum movement and heat so the correct type of appliance can be routed.',set:'Working washer and dryer sets in Fontana receive especially strong consideration when both machines are submitted together.'},
  '/san-bernardino-washer-dryer-pickup/':{city:'San Bernardino',area:'Inland Empire',washer:'For San Bernardino washer pickup, send clear photos and report whether the machine fills, washes, drains and spins, plus any access limitations.',dryer:'For San Bernardino dryer pickup, identify gas or electric service, whether the drum turns and whether it heats. Include stairs, gates and loading access.',set:'Complete working washer and dryer sets in San Bernardino receive strong priority within the Inland Empire pickup network.'}
};

function replaceCompressedLaundryPhotos(){
  document.querySelectorAll('img[src*="/assets/washer-dryer-photos/"]').forEach(img=>{
    const raw=String(img.getAttribute('src')||'');
    const file=raw.split('?')[0].split('/').pop();
    const replacement=COMPRESSED_LAUNDRY_REPLACEMENTS[file];
    if(!replacement)return;
    img.src=siteUrl('assets/laundry/'+replacement);
    img.removeAttribute('width');
    img.removeAttribute('height');
    img.decoding='async';
  });
}

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

function enhanceCityLaundrySearchTerms(){
  if(document.querySelector('.site-city-laundry-search'))return;
  const config=PREMIUM_CITY_LAUNDRY_SEARCH[pagePath()];if(!config)return;
  const main=document.querySelector('main');if(!main)return;
  const section=document.createElement('section');section.className='site-city-laundry-search';
  const intro=document.createElement('h2');intro.textContent='Free Washer, Dryer & Laundry Set Pickup in '+config.city;
  const lead=document.createElement('p');lead.textContent='This '+config.area+' page is organized around the three searches customers use most: free washer pickup, free dryer pickup, and free washer & dryer pickup in '+config.city+'. Qualification still depends on appliance condition, safe access and current route availability.';
  const grid=document.createElement('div');grid.className='grid';
  const items=[
    ['Free Washer Pickup in '+config.city,config.washer],
    ['Free Dryer Pickup in '+config.city,config.dryer],
    ['Free Washer & Dryer Pickup in '+config.city,config.set]
  ];
  items.forEach(([title,text])=>{const card=document.createElement('div');card.className='card';const h3=document.createElement('h3');h3.textContent=title;const p=document.createElement('p');p.textContent=text;card.append(h3,p);grid.appendChild(card);});
  const note=document.createElement('div');note.className='note';note.innerHTML='<strong>Best chance for free pickup:</strong> fully working machines and complete working sets receive the strongest consideration. Send clear appliance and access photos for review.';
  section.append(intro,lead,grid,note);
  const first=main.querySelector('section');
  if(first&&first.nextSibling)main.insertBefore(section,first.nextSibling);else main.appendChild(section);
}

load();
document.addEventListener('DOMContentLoaded',()=>{
  replaceCompressedLaundryPhotos();
  document.querySelectorAll('form[action*="formspree.io"]').forEach(ensureRegionalState);
  preferLocalRequestForm();enhanceWasherDryerPhotos();enhanceCityLaundrySearchTerms();
  document.querySelectorAll('form[action*="formspree.io"]').forEach(form=>{if(isCustomerPickupForm(form))wireForm(form);});
});

window.FreeReliableCustomerRouting={classify,qualify,load,siteBase,routingDecision,preferLocalRequestForm,enhanceWasherDryerPhotos,enhanceCityLaundrySearchTerms,replaceCompressedLaundryPhotos,priority909};
})();