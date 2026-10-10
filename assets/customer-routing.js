/* Customer request routing + premium washer/dryer presentation helper.
   Operational metadata only. Never creates city URLs or indexable pages. */
(function(){
'use strict';

const FALLBACK={status:'request-only',territory_status:'available',region:'Unassigned market',lead_priority:3,partner_id:null,backup_partner_id:null,phone:null};
const PRIORITY_909_PHONE='909-375-6685';
const PRIORITY_310_PHONE='310-774-4304';
let routing=null,cities=null,loadPromise=null;
const n=v=>String(v||'').trim().toLowerCase();

const CA_909_PRIORITY={
'montrose':'San Gabriel Valley','la crescenta':'San Gabriel Valley','la cañada flintridge':'San Gabriel Valley','la canada flintridge':'San Gabriel Valley','altadena':'San Gabriel Valley','pasadena':'San Gabriel Valley','south pasadena':'San Gabriel Valley','san marino':'San Gabriel Valley','san gabriel':'San Gabriel Valley','sierra madre':'San Gabriel Valley','arcadia':'San Gabriel Valley','monrovia':'San Gabriel Valley','duarte':'San Gabriel Valley','azusa':'San Gabriel Valley','glendora':'San Gabriel Valley','covina':'San Gabriel Valley','west covina':'San Gabriel Valley','san dimas':'San Gabriel Valley','la verne':'San Gabriel Valley','claremont':'San Gabriel Valley','pomona':'San Gabriel Valley','el monte':'San Gabriel Valley','south el monte':'San Gabriel Valley','baldwin park':'San Gabriel Valley','montebello':'San Gabriel Valley','la puente':'San Gabriel Valley','whittier':'San Gabriel Valley','norwalk':'San Gabriel Valley','downey':'San Gabriel Valley','rowland heights':'San Gabriel Valley','diamond bar':'San Gabriel Valley',
'montclair':'Inland Empire','ontario':'Inland Empire','upland':'Inland Empire','rancho cucamonga':'Inland Empire','fontana':'Inland Empire','san bernardino':'Inland Empire','highland':'Inland Empire','loma linda':'Inland Empire','yucaipa':'Inland Empire','oak glen':'Inland Empire','grand terrace':'Inland Empire','bloomington':'Inland Empire','rialto':'Inland Empire','colton':'Inland Empire','redlands':'Inland Empire','muscoy':'Inland Empire','arrowhead farms':'Inland Empire','north san bernardino':'Inland Empire',
'riverside':'Riverside County','eastvale':'Riverside County','norco':'Riverside County','moreno valley':'Riverside County','corona':'Riverside County','jurupa valley':'Riverside County','calimesa':'Riverside County','cherry valley':'Riverside County','beaumont':'Riverside County','banning':'Riverside County','temecula':'Riverside County','murrieta':'Riverside County','menifee':'Riverside County',
'brea':'Orange County','yorba linda':'Orange County','anaheim hills':'Orange County','anaheim':'Orange County','santa ana':'Orange County','fullerton':'Orange County','orange':'Orange County','garden grove':'Orange County','tustin':'Orange County','fountain valley':'Orange County','westminster':'Orange County','la habra':'Orange County','buena park':'Orange County','cypress':'Orange County','seal beach':'Orange County','los alamitos':'Orange County','placentia':'Orange County','villa park':'Orange County','la palma':'Orange County','irvine':'Orange County','newport beach':'Orange County','mission viejo':'Orange County','lake forest':'Orange County','laguna niguel':'Orange County','rancho santa margarita':'Orange County','san juan capistrano':'Orange County','san clemente':'Orange County','laguna hills':'Orange County','aliso viejo':'Orange County','trabuco canyon':'Orange County','ladera ranch':'Orange County','coto de caza':'Orange County','laguna woods':'Orange County','laguna beach':'Orange County','dana point':'Orange County','costa mesa':'Orange County','huntington beach':'Orange County',
'alhambra':'San Gabriel Valley','monterey park':'San Gabriel Valley','rosemead':'San Gabriel Valley','temple city':'San Gabriel Valley','hacienda heights':'San Gabriel Valley','walnut':'San Gabriel Valley','irwindale':'San Gabriel Valley','south san jose hills':'San Gabriel Valley','avocado heights':'San Gabriel Valley',
'chino':'Inland Empire','chino hills':'Inland Empire',
'perris':'Riverside County','hemet':'Riverside County','lake elsinore':'Riverside County','wildomar':'Riverside County',
'palm springs':'Coachella Valley','palm desert':'Coachella Valley','rancho mirage':'Coachella Valley','indian wells':'Coachella Valley','la quinta':'Coachella Valley','cathedral city':'Coachella Valley','indio':'Coachella Valley','coachella':'Coachella Valley','desert hot springs':'Coachella Valley','bermuda dunes':'Coachella Valley','pga west':'Coachella Valley',
'victorville':'Victorville Valley','hesperia':'Victorville Valley','adelanto':'Victorville Valley','apple valley':'Victorville Valley','phelan':'Victorville Valley','el mirage':'Victorville Valley','oak hills':'Victorville Valley','helendale':'Victorville Valley','silver lakes':'Victorville Valley','spring valley lake':'Victorville Valley','pinon hills':'Victorville Valley','wrightwood':'Victorville Valley'};

const CA_310_PRIORITY={
'los angeles':'Los Angeles County','long beach':'Los Angeles County','la mirada':'Los Angeles County','cerritos':'Los Angeles County','bellflower':'Los Angeles County','pico rivera':'Los Angeles County','carson':'Los Angeles County','compton':'Los Angeles County','culver city':'Los Angeles County','gardena':'Los Angeles County','hawthorne':'Los Angeles County','inglewood':'Los Angeles County','lawndale':'Los Angeles County','lynwood':'Los Angeles County','south gate':'Los Angeles County','huntington park':'Los Angeles County','maywood':'Los Angeles County','bell':'Los Angeles County','bell gardens':'Los Angeles County','commerce':'Los Angeles County','cudahy':'Los Angeles County','vernon':'Los Angeles County','torrance':'Los Angeles County','redondo beach':'Los Angeles County','manhattan beach':'Los Angeles County','hermosa beach':'Los Angeles County','el segundo':'Los Angeles County','beverly hills':'Los Angeles County','west hollywood':'Los Angeles County','santa monica':'Los Angeles County','malibu':'Los Angeles County','burbank':'Los Angeles County','glendale':'Los Angeles County','santa clarita':'Los Angeles County','san fernando':'Los Angeles County','calabasas':'Los Angeles County',
'palmdale':'Antelope Valley','lancaster':'Antelope Valley','acton':'Antelope Valley','leona valley':'Antelope Valley','littlerock':'Antelope Valley','lake los angeles':'Antelope Valley','quartz hill':'Antelope Valley','pearblossom':'Antelope Valley','llano':'Antelope Valley','sun village':'Antelope Valley','antelope acres':'Antelope Valley','juniper hills':'Antelope Valley','crystalaire':'Antelope Valley','desert view highlands':'Antelope Valley','largo vista':'Antelope Valley','lakeview':'Antelope Valley',
'san diego':'San Diego County','chula vista':'San Diego County','oceanside':'San Diego County','carlsbad':'San Diego County','escondido':'San Diego County','el cajon':'San Diego County','la mesa':'San Diego County','national city':'San Diego County','encinitas':'San Diego County','san marcos':'San Diego County','santee':'San Diego County','imperial beach':'San Diego County','lemon grove':'San Diego County','poway':'San Diego County','coronado':'San Diego County','del mar':'San Diego County','solana beach':'San Diego County',
'san francisco':'San Francisco Bay Area','san jose':'San Francisco Bay Area','oakland':'San Francisco Bay Area','berkeley':'San Francisco Bay Area','fremont':'San Francisco Bay Area','hayward':'San Francisco Bay Area','richmond':'San Francisco Bay Area','concord':'San Francisco Bay Area','palo alto':'San Francisco Bay Area','santa clara':'San Francisco Bay Area','sunnyvale':'San Francisco Bay Area','walnut creek':'San Francisco Bay Area',
'sacramento':'Central Valley','fresno':'Central Valley','stockton':'Central Valley','modesto':'Central Valley','bakersfield':'Central Valley','visalia':'Central Valley',
'oxnard':'Central Coast','ventura':'Central Coast','santa barbara':'Central Coast','san luis obispo':'Central Coast','santa maria':'Central Coast'};

function siteBase(){const host=(location.hostname||'').toLowerCase();if(host.endsWith('.github.io')){const first=(location.pathname||'/').split('/').filter(Boolean)[0];return first?'/'+first+'/':'/';}return '/';}
function siteUrl(path){return siteBase()+String(path||'').replace(/^\/+/, '');}
function stateCode(value){const raw=String(value||'').trim();if(raw.length===2)return raw.toUpperCase();const map={alabama:'AL',alaska:'AK',arizona:'AZ',arkansas:'AR',california:'CA',colorado:'CO',connecticut:'CT',delaware:'DE',florida:'FL',georgia:'GA',hawaii:'HI',idaho:'ID',illinois:'IL',indiana:'IN',iowa:'IA',kansas:'KS',kentucky:'KY',louisiana:'LA',maine:'ME',maryland:'MD',massachusetts:'MA',michigan:'MI',minnesota:'MN',mississippi:'MS',missouri:'MO',montana:'MT',nebraska:'NE',nevada:'NV','new hampshire':'NH','new jersey':'NJ','new mexico':'NM','new york':'NY','north carolina':'NC','north dakota':'ND',ohio:'OH',oklahoma:'OK',oregon:'OR',pennsylvania:'PA','rhode island':'RI','south carolina':'SC','south dakota':'SD',tennessee:'TN',texas:'TX',utah:'UT',vermont:'VT',virginia:'VA',washington:'WA','west virginia':'WV',wisconsin:'WI',wyoming:'WY'};return map[n(raw)]||raw.toUpperCase();}
function priorityCalifornia(city,state){const sc=stateCode(state),cn=n(city);if(sc!=='CA')return null;const region909=CA_909_PRIORITY[cn];if(region909)return {state:'California',state_code:'CA',city:String(city||'').trim(),region:region909,status:'partner-recruiting',territory_status:'available',lead_priority:1,partner_id:null,backup_partner_id:null,phone:PRIORITY_909_PHONE,pricing_status:'collect_data',monthly_price_cents:null,resolution_level:'priority-california-city'};const region310=CA_310_PRIORITY[cn];if(region310)return {state:'California',state_code:'CA',city:String(city||'').trim(),region:region310,status:'partner-recruiting',territory_status:'available',lead_priority:1,partner_id:null,backup_partner_id:null,phone:PRIORITY_310_PHONE,pricing_status:'collect_data',monthly_price_cents:null,resolution_level:'priority-california-city'};return null;}
function priority909(city,state){const info=priorityCalifornia(city,state);return info&&info.phone===PRIORITY_909_PHONE?info:null;}
function classify(city,state){const sc=stateCode(state),cn=n(city),priority=priorityCalifornia(city,state);if(priority)return priority;if(!routing||!Array.isArray(routing.markets))return {...FALLBACK,state_code:sc,city,resolution_level:'fallback'};const exact=routing.markets.find(m=>stateCode(m.state_code||m.state)===sc&&m.city&&n(m.city)===cn);if(exact)return {...exact,resolution_level:'exact-city'};const namedRegion=routing.markets.find(m=>stateCode(m.state_code||m.state)===sc&&!m.city&&n(m.region)===cn);if(namedRegion)return {...namedRegion,resolution_level:'regional'};let region=null;if(cities&&Array.isArray(cities.cities)){const c=cities.cities.find(x=>stateCode(x.state_code||x.state)===sc&&n(x.city)===cn);if(c)region=c.region||null;}if(region){const m=routing.markets.find(x=>stateCode(x.state_code||x.state)===sc&&!x.city&&n(x.region)===n(region));if(m)return {...m,resolution_level:'regional'};}if(Array.isArray(routing.state_defaults)){const s=routing.state_defaults.find(x=>stateCode(x.state_code||x.state)===sc);if(s)return {...s,city,region:s.region||((s.state||sc)+' statewide intake'),resolution_level:'statewide'};}return {...FALLBACK,state_code:sc,city,resolution_level:'fallback'};}
function routingDecision(info){const status=String(info&&info.status||FALLBACK.status),territory=String(info&&info.territory_status||FALLBACK.territory_status);if(status==='direct')return {decision:'DIRECT_OPERATION',tier:'direct-operations',action:'Review qualification and dispatch through the established company market.'};if(status==='partner-supported'||territory==='assigned')return {decision:'PARTNER_NETWORK',tier:'assigned-partner',action:'Review qualification and route to the assigned approved partner.'};if(status==='partner-recruiting')return {decision:'RECRUITING_QUEUE',tier:'partner-recruiting',action:'Keep as an intake lead while local partner coverage is being recruited; do not promise pickup.'};return {decision:'NATIONAL_INTAKE',tier:'request-only',action:'Accept for review only; confirm local coverage before offering or scheduling pickup.'};}
function findField(form,names){for(const name of names){const el=form.querySelector(`[name="${name}"]`)||form.querySelector('#'+name);if(el)return el;}return null;}
function hidden(form,name,value){let el=form.querySelector(`input[type="hidden"][name="${name}"]`);if(!el){el=document.createElement('input');el.type='hidden';el.name=name;form.appendChild(el);}el.value=value==null?'':String(value);return el;}
function qualify(form){const city=findField(form,['city','City','pickup_city','Primary City']),state=findField(form,['state','State','pickup_state','Primary State']);if(!city||!state)return;const info=classify(city.value,state.value),route=routingDecision(info);hidden(form,'Routing City',city.value.trim());hidden(form,'Routing State Code',stateCode(state.value));hidden(form,'Routing Region',info.region||FALLBACK.region);hidden(form,'Routing Resolution Level',info.resolution_level||'fallback');hidden(form,'Routing Market Status',info.status||FALLBACK.status);hidden(form,'Routing Territory Status',info.territory_status||FALLBACK.territory_status);hidden(form,'Routing Priority',info.lead_priority||FALLBACK.lead_priority);hidden(form,'Routing Phone',info.phone||'');hidden(form,'Routing Partner ID',info.partner_id||'');hidden(form,'Routing Backup Partner ID',info.backup_partner_id||'');hidden(form,'Routing Decision',route.decision);hidden(form,'Routing Network Tier',route.tier);hidden(form,'Routing Next Action',route.action);hidden(form,'Coverage Promise','None until qualification and local coverage are confirmed');hidden(form,'Routing Source',info.resolution_level==='priority-california-city'?'Priority California customer-routing override':'Canonical market-routing.json');hidden(form,'SEO Page Creation','Disabled');const condition=findField(form,['condition','Condition','Appliance Condition']),appliance=findField(form,['appliance','Appliance','Appliance Type']),stairs=findField(form,['stairs','Stairs']),access=findField(form,['access','Access','Access Notes']);hidden(form,'Qualification Snapshot',[appliance&&appliance.value,condition&&condition.value,stairs&&stairs.value,access&&access.value].filter(Boolean).join(' | '));const cycleTest=findField(form,['laundry_cycle_test']),unusualNoise=findField(form,['laundry_unusual_noise']),faultDetails=findField(form,['condition_details']);const conditionValue=String(condition&&condition.value||''),cycleValue=String(cycleTest&&cycleTest.value||''),noiseValue=String(unusualNoise&&unusualNoise.value||'');const mechanicalRisk=['Working With Issues','Needs Repair','Not Working','Unknown','Mixed Load - Mixed Conditions'].includes(conditionValue)||['Cycle has problems','Failed cycle','Power only','Not tested'].includes(cycleValue)||['Loud unusual noise','Not tested'].includes(noiseValue);hidden(form,'Customer Laundry Cycle Test',cycleValue);hidden(form,'Customer Reported Unusual Noise',noiseValue);hidden(form,'Customer Defect Explanation',faultDetails&&faultDetails.value||'');hidden(form,'Dispatch Condition Gate',mechanicalRisk?'HOLD FOR MANUAL CONDITION REVIEW - do not send a partner without verifying faults, photos/testing and explicit partner acceptance':'MANUAL VERIFY BEFORE DISPATCH - customer selection alone does not confirm fully working');}
function load(){if(loadPromise)return loadPromise;loadPromise=Promise.all([fetch(siteUrl('data/market-routing.json'),{cache:'no-store'}),fetch(siteUrl('data/cities.json'),{cache:'no-store'})]).then(async([r,c])=>{if(r.ok)routing=await r.json();if(c.ok)cities=await c.json();}).catch(()=>{});return loadPromise;}
function wireForm(form){if(form.dataset.customerRoutingWired==='1')return;form.dataset.customerRoutingWired='1';form.addEventListener('submit',async function(event){if(form.dataset.customerRoutingQualified==='1'){qualify(form);return;}event.preventDefault();await load();qualify(form);form.dataset.customerRoutingQualified='1';if(typeof form.requestSubmit==='function')form.requestSubmit(event.submitter||undefined);else form.submit();},true);}
function isCustomerPickupForm(form){return !!(findField(form,['city','City','pickup_city'])&&findField(form,['state','State','pickup_state'])&&findField(form,['appliance','Appliance','Appliance Type']));}
function pagePath(){let p=location.pathname||'/',base=siteBase();if(base!=='/'&&p.startsWith(base.slice(0,-1)))p=p.slice(base.length-1)||'/';if(!p.startsWith('/'))p='/'+p;if(!p.endsWith('/'))p+='/';return p;}

/* IMPORTANT: every hero in this rotation is a complete washer + dryer set. */
const COMPLETE_SET_HEROES=[
'front-load-laundry-set.jpg',
'laundry-pair.jpg',
'washer-dryer-set.jpg',
'washer-dryer-set-sharp.jpg',
'heroes/la-canada-premium-set.webp',
'heroes/pasadena-premium-set.webp',
'heroes/ontario-premium-set.webp',
'heroes/rancho-cucamonga-premium-set.webp',
'heroes/san-bernardino-premium-set.webp'
];

const PREMIUM_WD_SLUGS=[
'california','southern-california','san-gabriel-inland-empire','los-angeles-county','orange-county','south-orange-county','riverside-county','san-bernardino-county',
'montrose','la-crescenta','la-canada-flintridge','altadena','pasadena','south-pasadena','san-marino','san-gabriel','sierra-madre','arcadia','monrovia','duarte','azusa','glendora','covina','west-covina','san-dimas','la-verne','claremont','pomona','montclair','ontario','upland','rancho-cucamonga','fontana','san-bernardino','chino-hills','highland','loma-linda','yucaipa','oak-glen',
'anaheim-hills','brea','yorba-linda','irvine','newport-beach','mission-viejo','lake-forest','laguna-niguel','rancho-santa-margarita','san-juan-capistrano','san-clemente','laguna-hills','aliso-viejo','trabuco-canyon','ladera-ranch','coto-de-caza','laguna-woods','laguna-beach','dana-point','costa-mesa','huntington-beach','calimesa','cherry-valley','beaumont','banning'
];

const CITY_LABEL_OVERRIDES={
'la-crescenta':'La Crescenta','la-canada-flintridge':'La Cañada Flintridge','san-gabriel-inland-empire':'San Gabriel Valley & Inland Empire','los-angeles-county':'Los Angeles County','orange-county':'Orange County','south-orange-county':'South Orange County','riverside-county':'Riverside County','san-bernardino-county':'San Bernardino County','rancho-cucamonga':'Rancho Cucamonga','rancho-santa-margarita':'Rancho Santa Margarita','san-juan-capistrano':'San Juan Capistrano','san-clemente':'San Clemente','newport-beach':'Newport Beach','mission-viejo':'Mission Viejo','lake-forest':'Lake Forest','laguna-niguel':'Laguna Niguel','laguna-hills':'Laguna Hills','aliso-viejo':'Aliso Viejo','trabuco-canyon':'Trabuco Canyon','ladera-ranch':'Ladera Ranch','coto-de-caza':'Coto de Caza','laguna-woods':'Laguna Woods','laguna-beach':'Laguna Beach','dana-point':'Dana Point','costa-mesa':'Costa Mesa','huntington-beach':'Huntington Beach','chino-hills':'Chino Hills','anaheim-hills':'Anaheim Hills','cherry-valley':'Cherry Valley','south-pasadena':'South Pasadena','san-marino':'San Marino','san-gabriel':'San Gabriel','sierra-madre':'Sierra Madre','west-covina':'West Covina','san-dimas':'San Dimas','la-verne':'La Verne','loma-linda':'Loma Linda','oak-glen':'Oak Glen'
};
function slugLabel(slug){if(CITY_LABEL_OVERRIDES[slug])return CITY_LABEL_OVERRIDES[slug];return slug.split('-').map(w=>w.charAt(0).toUpperCase()+w.slice(1)).join(' ');}
const WASHER_DRYER_PHOTOS={};
PREMIUM_WD_SLUGS.forEach((slug,i)=>{const label=slugLabel(slug);WASHER_DRYER_PHOTOS['/'+slug+'-washer-dryer-pickup/']={hero:COMPLETE_SET_HEROES[i%COMPLETE_SET_HEROES.length],alt:'Real washer and dryer set for pickup in '+label};});
/* Keep La Crescenta on a confirmed side-by-side/front-load pair. */
WASHER_DRYER_PHOTOS['/la-crescenta-washer-dryer-pickup/']={hero:'front-load-laundry-set.jpg',alt:'Real matching washer and dryer set for pickup in La Crescenta'};

const CA_WASHER_DRYER_PAGES=new Set(Object.keys(WASHER_DRYER_PHOTOS));
const LAUNDRY_GALLERY=COMPLETE_SET_HEROES.map((file,i)=>[file,'Real washer and dryer set '+(i+1)+' from our appliance work']);
const COMPRESSED_LAUNDRY_REPLACEMENTS={'washer-dryer-pickup-frontload-set.jpg':'front-load-laundry-set.jpg','washer-dryer-pickup-gray-topload-set.jpg':'laundry-pair.jpg','washer-dryer-pickup-modern-topload-set.jpg':'washer-dryer-set.jpg','washer-dryer-pickup-stacked-set.jpg':'washer-dryer-set-sharp.jpg'};

function replaceCompressedLaundryPhotos(){document.querySelectorAll('img[src*="/assets/washer-dryer-photos/"]').forEach(img=>{const raw=String(img.getAttribute('src')||''),file=raw.split('?')[0].split('/').pop(),replacement=COMPRESSED_LAUNDRY_REPLACEMENTS[file];if(!replacement)return;img.src=siteUrl('assets/laundry/'+replacement);img.removeAttribute('width');img.removeAttribute('height');img.decoding='async';});}
function ensureRegionalState(form){if(findField(form,['state','State','pickup_state','Primary State']))return;if(CA_WASHER_DRYER_PAGES.has(pagePath()))hidden(form,'state','CA');}
function preferLocalRequestForm(){const forms=Array.from(document.querySelectorAll('form[action*="formspree.io"]'));forms.forEach(ensureRegionalState);const form=forms.find(isCustomerPickupForm);if(!form)return;let target=form.closest('section');if(!target)target=form;if(!target.id)target.id='request';const localHref='#'+target.id,selectors=['a[href="/#request"]','a[href="../#request"]','a[href="./#request"]','a[href="https://freereliableappliancepickup.com/#request"]'];document.querySelectorAll(selectors.join(',')).forEach(link=>link.setAttribute('href',localHref));}
function buildLaundryGallery(path){if(document.querySelector('.site-laundry-photo-showcase'))return;const main=document.querySelector('main');if(!main)return;const pageIndex=Math.max(0,Object.keys(WASHER_DRYER_PHOTOS).indexOf(path)),picks=[LAUNDRY_GALLERY[pageIndex%LAUNDRY_GALLERY.length],LAUNDRY_GALLERY[(pageIndex+3)%LAUNDRY_GALLERY.length],LAUNDRY_GALLERY[(pageIndex+6)%LAUNDRY_GALLERY.length]],section=document.createElement('section');section.className='site-laundry-photo-showcase';const h2=document.createElement('h2');h2.textContent='Real Washer & Dryer Set Photos';const p=document.createElement('p');p.textContent='Real washer and dryer set photos from our appliance work and inventory. Send clear photos of your own machines so we can review condition, access and local route availability.';const grid=document.createElement('div');picks.forEach(([file,alt])=>{const figure=document.createElement('figure'),img=document.createElement('img');figure.style.margin='0';img.src=siteUrl('assets/laundry/'+file);img.alt=alt;img.loading='lazy';img.decoding='async';figure.appendChild(img);grid.appendChild(figure);});section.append(h2,p,grid);main.insertBefore(section,main.firstChild);}
function enhanceWasherDryerPhotos(){const path=pagePath(),config=WASHER_DRYER_PHOTOS[path];if(!config)return;const src=siteUrl('assets/laundry/'+config.hero),hero=document.querySelector('.site-hero-art img');if(hero){hero.src=src+(src.includes('?')?'&':'?')+'premium-set=20260916';hero.alt=config.alt;hero.removeAttribute('width');hero.removeAttribute('height');hero.decoding='async';hero.style.width='100%';hero.style.height='auto';hero.style.maxHeight='520px';hero.style.objectFit='contain';hero.style.background='#f5f7f6';hero.style.borderRadius='16px';hero.style.boxShadow='0 12px 28px rgba(0,0,0,.18)';}buildLaundryGallery(path);}
function enhanceCityLaundrySearchTerms(){if(document.querySelector('.site-city-laundry-search'))return;const path=pagePath(),config=WASHER_DRYER_PHOTOS[path];if(!config)return;const slug=path.replace(/^\//,'').replace(/-washer-dryer-pickup\/$/,'');if(['california','southern-california','san-gabriel-inland-empire','los-angeles-county','orange-county','south-orange-county','riverside-county','san-bernardino-county'].includes(slug))return;const city=slugLabel(slug),main=document.querySelector('main');if(!main)return;const section=document.createElement('section');section.className='site-city-laundry-search';const h2=document.createElement('h2');h2.textContent='Free Washer, Dryer & Laundry Set Pickup in '+city;const lead=document.createElement('p');lead.textContent='Customers in '+city+' can submit washers, dryers and complete laundry sets for pickup review. Qualification depends on appliance condition, safe access and current route availability.';const grid=document.createElement('div');grid.className='grid';[['Free Washer Pickup in '+city,'Send clear photos and describe whether the washer fills, washes, drains and spins.'],['Free Dryer Pickup in '+city,'Identify gas or electric service and whether the drum turns and produces heat.'],['Free Washer & Dryer Pickup in '+city,'Complete working washer and dryer sets receive especially strong consideration because both machines can often be routed together for reuse.']].forEach(([title,text])=>{const card=document.createElement('div'),h3=document.createElement('h3'),p=document.createElement('p');card.className='card';h3.textContent=title;p.textContent=text;card.append(h3,p);grid.appendChild(card);});const note=document.createElement('div');note.className='note';note.innerHTML='<strong>Best chance for free pickup:</strong> fully working machines and complete working sets receive the strongest consideration. Send clear appliance and access photos for review.';section.append(h2,lead,grid,note);const first=main.querySelector('section');if(first&&first.nextSibling)main.insertBefore(section,first.nextSibling);else main.appendChild(section);}


function pagePhone(){
  const tel=document.querySelector('a[href^="tel:"]');
  if(tel){
    const digits=String(tel.getAttribute('href')||'').replace(/\D/g,'');
    if(digits.length>=10)return {digits:digits.slice(-10),display:digits.slice(-10,-7)+'-'+digits.slice(-7,-4)+'-'+digits.slice(-4)};
  }
  return null;
}
function ensurePriorityMobileCta(){
  // Pages with a pre-rendered sticky bar also need bottom clearance on small screens.
  if(document.querySelector('.priority-mobile-cta')){
    document.body.classList.add('has-priority-mobile-cta');
    return;
  }
  const request=document.querySelector('#request, form[action*="formspree.io"]');
  const phone=pagePhone();
  if(!request||!phone)return;
  document.body.classList.add('has-priority-mobile-cta');
  const bar=document.createElement('nav');
  bar.className='priority-mobile-cta';
  bar.setAttribute('aria-label','Quick pickup actions');
  const call=document.createElement('a');call.href='tel:+1'+phone.digits;call.textContent='Call';
  const textLink=document.createElement('a');textLink.href='sms:+1'+phone.digits;textLink.textContent='Text Photos';
  const requestLink=document.createElement('a');requestLink.href='#request';requestLink.textContent='Request Pickup';
  bar.append(call,textLink,requestLink);
  document.body.appendChild(bar);
}
function enhancePhotoFirstIntake(){
  const phone=pagePhone();
  document.querySelectorAll('form[action*="formspree.io"]').forEach(form=>{
    if(form.dataset.photoFirstEnhanced==='1')return;
    form.dataset.photoFirstEnhanced='1';
    const box=document.createElement('div');
    box.className='site-photo-first-intake';
    const title=document.createElement('strong');
    title.textContent='Photos help us review your pickup faster.';
    const copy=document.createElement('p');
    copy.textContent='Send clear appliance and access photos by text, or paste a share link below. Include inside photos for refrigerators/freezers and tested condition when known.';
    box.append(title,copy);
    if(phone){
      const sms=document.createElement('a');
      sms.href='sms:+1'+phone.digits;
      sms.textContent='Text photos to '+phone.display;
      sms.className='site-photo-text-button';
      box.appendChild(sms);
    }
    form.insertBefore(box,form.firstChild);
    if(!form.querySelector('[name="Photo Link"]')){
      const wrap=document.createElement('label');
      wrap.className='site-photo-link-field';
      wrap.textContent='Optional photo share link (Google Photos, iCloud, Dropbox, etc.)';
      const input=document.createElement('input');
      input.type='url';
      input.name='Photo Link';
      input.inputMode='url';
      input.placeholder='https://';
      input.autocomplete='url';
      wrap.appendChild(input);
      const submit=form.querySelector('button[type="submit"],input[type="submit"]');
      if(submit&&submit.parentNode)submit.parentNode.insertBefore(wrap,submit);else form.appendChild(wrap);
    }
  });
}

/* Keep condition intake consistent on Formspree pickup pages that load this shared file.
   Existing HTML fields remain useful when JavaScript is unavailable. */
function enhanceApplianceConditionIntake(){
  const choices=[
    ['','Select actual condition'],
    ['Fully Working','Fully working — all functions tested, no known problems'],
    ['Working With Issues','Works, but has problems (explain below)'],
    ['Needs Repair','Needs repair — not fully working'],
    ['Not Working','Not working'],
    ['Unknown','Unknown / not tested'],
    ['Mixed Load - Mixed Conditions','Multiple appliances — describe each condition']
  ];
  document.querySelectorAll('form[action*="formspree.io"]').forEach(form=>{
    const select=form.querySelector('select[name="condition"]');
    if(!select)return;
    const alreadyClear=Array.from(select.options).some(option=>option.value==='Working With Issues');
    const oldValue=String(select.value||'').trim();
    if(!alreadyClear){
      while(select.firstChild)select.removeChild(select.firstChild);
      choices.forEach(([value,label])=>{
        const option=document.createElement('option');
        option.value=value;
        option.textContent=label;
        select.appendChild(option);
      });
      const aliases={'fully working':'Fully Working','needs minor repair':'Needs Repair','needs repair':'Needs Repair','not working':'Not Working','unknown':'Unknown','mixed load - majority working':'Mixed Load - Mixed Conditions'};
      select.value=choices.some(([value])=>value===oldValue)?oldValue:(aliases[oldValue.toLowerCase()]||'');
    }
    if(form.querySelector('[name="condition_details"]'))return;
    const label=document.createElement('label');
    label.className='site-condition-details';
    label.style.cssText='display:block;margin:12px 0;font-weight:600';
    label.textContent='What works and what does not? (please explain any issues)';
    const details=document.createElement('textarea');
    details.name='condition_details';
    details.rows=3;
    details.placeholder='Example: washer spins but leaks; dryer runs but no heat; refrigerator powers on but does not cool. For several appliances, list each condition.';
    details.style.cssText='display:block;width:100%;box-sizing:border-box;margin-top:6px;font-weight:400';
    label.appendChild(details);
    const holder=select.closest('label')||select.closest('.field')||select;
    holder.insertAdjacentElement('afterend',label);
  });
}


/* Pre-dispatch laundry screening: a noisy washer is NOT fully working merely
   because the motor starts. Customer reports are never a dispatch guarantee. */
function enhanceLaundryConditionCheck(){
  document.querySelectorAll('form[action*="formspree.io"]').forEach(form=>{
    const appliance=form.querySelector('select[name="appliance"]');
    const condition=form.querySelector('select[name="condition"]');
    if(!appliance||!condition||form.querySelector('[name="laundry_cycle_test"]'))return;

    const fieldset=document.createElement('fieldset');
    fieldset.className='site-laundry-condition-screen';
    fieldset.style.cssText='border:1px solid #b8d4c1;border-radius:9px;padding:12px 14px;margin:12px 0';
    const legend=document.createElement('legend');
    legend.textContent='Washer / dryer condition check';
    legend.style.cssText='font-weight:700;color:#075c34';
    fieldset.appendChild(legend);

    const note=document.createElement('p');
    note.style.cssText='margin:4px 0 12px';
    note.textContent='Powering on or spinning does not mean fully working. Loud rumbling, grinding, banging, heavy shaking, leaking or a failed cycle can mean it needs repair. Please answer accurately so no pickup partner makes a wasted trip.';
    fieldset.appendChild(note);

    function question(name,prompt,choices){
      const label=document.createElement('label');
      label.style.cssText='display:block;margin:10px 0;font-weight:600';
      label.textContent=prompt;
      const select=document.createElement('select');
      select.name=name;
      select.style.cssText='display:block;width:100%;max-width:100%;margin-top:6px';
      const empty=document.createElement('option');
      empty.value='';
      empty.textContent='Choose one';
      select.appendChild(empty);
      choices.forEach(([value,text])=>{
        const option=document.createElement('option');
        option.value=value;
        option.textContent=text;
        select.appendChild(option);
      });
      label.appendChild(select);
      fieldset.appendChild(label);
      return select;
    }
    const cycle=question('laundry_cycle_test','Was a full wash/spin or dry/heat cycle tested?',[
      ['Full cycle passed','Yes — full cycle finished normally'],
      ['Cycle has problems','Runs, but cycle has problems'],
      ['Power only','Only turned on / did not test full cycle'],
      ['Failed cycle','Will not finish or fails the cycle'],
      ['Not tested','Not tested / unsure']
    ]);
    const noise=question('laundry_unusual_noise','Does it grind, rumble, bang, squeal or shake unusually during use?',[
      ['No unusual noise','No — tested, sounds normal'],
      ['Loud unusual noise','Yes — loud / grinding / rumbling / banging / shaking'],
      ['Not tested','Not tested / unsure']
    ]);

    const honestyLabel=document.createElement('label');
    honestyLabel.style.cssText='display:block;margin:12px 0;font-weight:600';
    const attestation=document.createElement('input');
    attestation.type='checkbox';
    attestation.name='laundry_condition_attestation';
    attestation.value='Confirmed all known condition and noise issues disclosed';
    attestation.style.cssText='width:auto;display:inline-block;margin-right:8px';
    honestyLabel.appendChild(attestation);
    honestyLabel.appendChild(document.createTextNode('I have reported any unusual noise, heavy shaking, leaks, cycle problems or other known faults to the best of my knowledge.'));
    fieldset.appendChild(honestyLabel);
    const videoNote=document.createElement('p');
    videoNote.style.cssText='font-size:13px;margin:6px 0';
    videoNote.textContent='Before a partner makes a long trip, we may request a short video of the washer spinning or the dryer running, plus appliance photos. Do not run an appliance that seems unsafe.';
    fieldset.appendChild(videoNote);

    const warning=document.createElement('p');
    warning.setAttribute('role','status');
    warning.style.cssText='font-size:14px;margin:10px 0 0;color:#784200';
    fieldset.appendChild(warning);

    const conditionDetails=form.querySelector('[name="condition_details"]');
    const anchor=(conditionDetails&&conditionDetails.closest('label'))||condition.closest('label')||condition.closest('.field')||condition;
    anchor.insertAdjacentElement('afterend',fieldset);

    function refresh(){
      const isLaundry=/washer|dryer|laundry/i.test(appliance.value||'');
      fieldset.hidden=!isLaundry;
      cycle.disabled=!isLaundry;
      noise.disabled=!isLaundry;
      cycle.required=isLaundry;
      noise.required=isLaundry;
      attestation.required=isLaundry;
      attestation.disabled=!isLaundry;
      if(!isLaundry){cycle.value='';noise.value='';attestation.checked=false;}

      const isIssue=['Working With Issues','Needs Repair','Not Working','Mixed Load - Mixed Conditions'].includes(condition.value);
      if(conditionDetails)conditionDetails.required=isIssue;
      if(conditionDetails)conditionDetails.setAttribute('aria-required',String(isIssue));

      const full=condition.value==='Fully Working';
      const conflict=isLaundry&&full&&
        ((cycle.value&&cycle.value!=='Full cycle passed')||
         (noise.value&&noise.value!=='No unusual noise'));
      condition.setCustomValidity(conflict?'This washer/dryer cannot be marked fully working when its full cycle was not tested successfully or it makes unusual noise. Select Works, but has problems, Needs repair, or Unknown.':'');
      if(!isLaundry)warning.textContent='';
      else if(noise.value==='Loud unusual noise'||cycle.value==='Cycle has problems'||cycle.value==='Failed cycle')
        warning.textContent='Mechanical problem reported. Free pickup is not confirmed. We must review details and obtain partner acceptance before any trip.';
      else if(cycle.value==='Power only'||cycle.value==='Not tested'||noise.value==='Not tested')
        warning.textContent='Not fully verified. Please do not select Fully working. The request requires condition review before any trip.';
      else warning.textContent='Even if tested, pickup and partner dispatch require confirmation after reviewing condition, photos and access.';
    }
    [appliance,condition,cycle,noise].forEach(input=>input.addEventListener('change',refresh));
    refresh();
  });
}

function enhanceRequestNextSteps(){
  document.querySelectorAll('form[action*="formspree.io"]').forEach(form=>{
    const host=form.closest('section')||form.parentElement;
    if(!host||host.querySelector('.site-request-next-steps'))return;
    const text=(host.textContent||'').toLowerCase();
    if(text.includes('what happens after you submit'))return;
    const box=document.createElement('div');
    box.className='site-request-next-steps';
    box.innerHTML='<h3>What happens after you submit?</h3><div class="site-request-next-grid"><div><strong>1. We review the appliance</strong><span>Condition, photos and appliance type are checked.</span></div><div><strong>2. We review the address & access</strong><span>Stairs, gates, parking and route availability are considered.</span></div><div><strong>3. We confirm the pickup</strong><span>If the request qualifies, pickup details are confirmed by call or text.</span></div></div>';
    host.insertBefore(box,form);
  });
}

/* GA4 lead-action tracking 20261002 */
const GA4_MEASUREMENT_ID='G-X9VMB6GQMF';

function analyticsPageLabel(){
  const p=(location.pathname||'/').replace(/^\/+|\/+$/g,'');
  return p || 'home';
}
function gaEvent(name,params){
  if(typeof window.gtag!=='function')return;
  window.gtag('event',name,Object.assign({
    page_path:location.pathname||'/',
    page_title:document.title||'',
    page_label:analyticsPageLabel()
  },params||{}));
}
function initLeadAnalytics(){
  if(typeof window==='undefined'||typeof document==='undefined'||window.__freeReliableGa4Loaded)return;
  window.__freeReliableGa4Loaded=true;
  window.dataLayer=window.dataLayer||[];
  window.gtag=window.gtag||function(){window.dataLayer.push(arguments);};
  window.gtag('js',new Date());
  window.gtag('config',GA4_MEASUREMENT_ID,{send_page_view:true});

  function loadGa4Library(){
    if(document.querySelector('script[data-free-reliable-ga4]'))return;
    const tag=document.createElement('script');
    tag.async=true;
    tag.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(GA4_MEASUREMENT_ID);
    tag.dataset.freeReliableGa4='1';
    document.head.appendChild(tag);
  }
  function scheduleGa4Library(){
    if(typeof window.addEventListener!=='function')return;
    const afterLoad=function(){
      if('requestIdleCallback' in window)window.requestIdleCallback(loadGa4Library,{timeout:2000});
      else window.setTimeout(loadGa4Library,0);
    };
    if(document.readyState==='complete')afterLoad();
    else window.addEventListener('load',afterLoad,{once:true});
    window.addEventListener('pointerdown',loadGa4Library,{once:true,passive:true});
    window.addEventListener('keydown',loadGa4Library,{once:true});
  }
  scheduleGa4Library();

  document.addEventListener('click',function(event){
    const link=event.target&&event.target.closest?event.target.closest('a[href]'):null;
    if(!link)return;
    const href=String(link.getAttribute('href')||'').trim().toLowerCase();
    let eventName=null;
    if(href.startsWith('tel:'))eventName='click_call';
    else if(href.startsWith('sms:'))eventName='click_text';
    if(!eventName)return;
    gaEvent(eventName,{
      link_text:String(link.textContent||'').trim().slice(0,100),
      button_location:link.closest('.priority-mobile-cta')?'mobile_sticky':'page',
      transport_type:'beacon'
    });
  },true);

  document.addEventListener('submit',function(event){
    const form=event.target;
    if(!form||!form.matches||!form.matches('form[action*="formspree.io"]'))return;
    // Routing intercepts and replays the first valid submit. Count only the routed replay.
    if(form.dataset.customerRoutingWired==='1'&&form.dataset.customerRoutingQualified!=='1')return;
    gaEvent('pickup_form_submit',{
      form_id:form.id||'pickup_form',
      transport_type:'beacon'
    });
  },true);
}

initLeadAnalytics();
load();
document.addEventListener('DOMContentLoaded',()=>{ensurePriorityMobileCta();enhancePhotoFirstIntake();enhanceApplianceConditionIntake();enhanceLaundryConditionCheck();enhanceRequestNextSteps();replaceCompressedLaundryPhotos();document.querySelectorAll('form[action*="formspree.io"]').forEach(ensureRegionalState);preferLocalRequestForm();enhanceWasherDryerPhotos();/* Avoid injecting identical keyword-heavy sections across city laundry pages; preserve the original useful page content. */document.querySelectorAll('form[action*="formspree.io"]').forEach(form=>{if(isCustomerPickupForm(form))wireForm(form);});});
/* Some premium city files include an older inline hero lock. Re-apply the verified complete-set rotation after those load handlers finish so each city keeps its assigned washer/dryer set. */
if(typeof window!=='undefined'&&typeof window.addEventListener==='function'){window.addEventListener('load',()=>{enhanceWasherDryerPhotos();});}
/* Load the final sharp individual-photo override on every premium washer/dryer page. */
if(typeof document!=='undefined'&&!document.querySelector('script[data-premium-sharp-hero]')){const sharp=document.createElement('script');sharp.src=siteUrl('assets/premium-sharp-hero-fix.js')+'?v=20260916h2';sharp.async=true;sharp.dataset.premiumSharpHero='1';document.head.appendChild(sharp);}
window.FreeReliableCustomerRouting={classify,qualify,load,siteBase,routingDecision,preferLocalRequestForm,enhanceWasherDryerPhotos,enhanceCityLaundrySearchTerms,replaceCompressedLaundryPhotos,priority909};
})();