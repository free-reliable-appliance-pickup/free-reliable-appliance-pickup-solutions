/* Nationwide partner application routing helper.
   Operational only: this script never creates URLs or SEO pages. */
(function () {
  'use strict';

  const DEFAULT = {
    status: 'request-only',
    territory_status: 'available',
    region: 'Unassigned market',
    lead_priority: 3
  };

  let routing = null;
  let cityCatalog = null;
  let activeLetter = '';

  const normalize = value => String(value || '').trim().toLowerCase();

  function marketFor(city, state) {
    if (!routing || !Array.isArray(routing.markets)) return { ...DEFAULT, resolution_level: 'fallback' };
    const stateCode = String(state || '').trim().toUpperCase();
    const cityName = normalize(city);
    const exact = routing.markets.find(m => String(m.state_code || '').toUpperCase() === stateCode && m.city && normalize(m.city) === cityName);
    if (exact) return { ...exact, resolution_level: 'exact-city' };
    let region = null;
    if (cityCatalog && Array.isArray(cityCatalog.cities)) {
      const catalogCity = cityCatalog.cities.find(c => String(c.state_code || '').toUpperCase() === stateCode && normalize(c.city) === cityName);
      if (catalogCity && catalogCity.region) region = catalogCity.region;
    }
    if (region) {
      const regional = routing.markets.find(m => String(m.state_code || '').toUpperCase() === stateCode && !m.city && normalize(m.region) === normalize(region));
      if (regional) return { ...regional, resolution_level: 'regional' };
    }
    if (Array.isArray(routing.state_defaults)) {
      const statewide = routing.state_defaults.find(s => String(s.state_code || '').toUpperCase() === stateCode);
      if (statewide) return { ...statewide, resolution_level: 'statewide' };
    }
    return { ...DEFAULT, state_code: stateCode, city, resolution_level: 'fallback' };
  }

  function applicationDecision(info) {
    const status = String(info && info.status || DEFAULT.status);
    const territory = String(info && info.territory_status || DEFAULT.territory_status);
    if (status === 'direct' || territory === 'protected') return { decision: 'DIRECT_OVERFLOW_CANDIDATE', action: 'Review only for backup, overflow, or future territory needs; do not replace established direct operations automatically.' };
    if (status === 'partner-supported' || territory === 'assigned') return { decision: 'ASSIGNED_MARKET_WAITLIST', action: 'Review for backup or future availability while preserving the currently assigned partner territory.' };
    if (status === 'partner-recruiting') return { decision: 'RECRUITING_PRIORITY', action: 'Prioritize partner qualification for this recruiting market; approval is required before any territory assignment.' };
    return { decision: 'FUTURE_MARKET', action: 'Keep as a future-market application; no service coverage or territory is promised by submission.' };
  }

  function preferenceProfile() {
    const leadModel = String((document.getElementById('leadModel') || {}).value || '').trim();
    const responseTime = String((document.getElementById('responseTime') || {}).value || '').trim();
    const radius = String((document.getElementById('radius') || {}).value || '').trim();
    const capacity = String((document.getElementById('capacity') || {}).value || '').trim();
    const inside = String((document.getElementById('insidePickup') || {}).value || '').trim();
    const availability = String((document.getElementById('availability') || {}).value || '').trim();

    const shared = /shared|both/i.test(leadModel);
    const exclusive = /exclusive|priority|both/i.test(leadModel);
    const fastResponse = /15 minutes|1 hour/i.test(responseTime);
    const sameDay = /same day|24 hours/i.test(availability);
    const highCapacity = /4–5|6\+/i.test(capacity);
    const broadRadius = /40 miles|50 miles|More than 50 miles/i.test(radius);
    const insideReady = /Inside pickup/i.test(inside);

    let tier = 'STANDARD_REVIEW';
    if (exclusive && fastResponse && (highCapacity || broadRadius)) tier = 'PRIMARY_TERRITORY_CANDIDATE';
    else if (shared && fastResponse) tier = 'FAST_SHARED_LEAD_CANDIDATE';
    else if (exclusive) tier = 'TERRITORY_INTEREST';
    else if (shared) tier = 'SHARED_LEAD_INTEREST';

    let score = 0;
    if (fastResponse) score += 3;
    else if (/4 hours|Same day/i.test(responseTime)) score += 2;
    else if (responseTime) score += 1;
    if (sameDay) score += 2;
    if (highCapacity) score += 2;
    if (broadRadius) score += 1;
    if (insideReady) score += 1;
    if (shared && exclusive) score += 1;

    return { leadModel, responseTime, radius, capacity, inside, availability, shared, exclusive, tier, score };
  }

  function publicLabel(info) {
    const decision = applicationDecision(info).decision;
    if (decision === 'DIRECT_OVERFLOW_CANDIDATE') return 'Established operation — backup or overflow applications may be reviewed';
    if (decision === 'ASSIGNED_MARKET_WAITLIST') return 'Partner-supported market — applications reviewed for future availability';
    if (decision === 'RECRUITING_PRIORITY') return 'Partner recruiting — applications welcome';
    if (info.territory_status === 'waitlist') return 'Waitlist market — application may be held for future review';
    return 'Future market — application can be reviewed';
  }

  function ensureHidden(form, name, id) {
    let input = form.querySelector('#' + id);
    if (!input) {
      input = document.createElement('input'); input.type = 'hidden'; input.name = name; input.id = id; form.appendChild(input);
    }
    return input;
  }

  function classifySelection() {
    const form = document.getElementById('partnerForm');
    const selectedInput = document.getElementById('selectedCitiesInput');
    if (!form || !selectedInput) return;
    const raw = String(selectedInput.value || '').split(';').map(v => v.trim()).filter(Boolean);
    const profile = preferenceProfile();
    const classified = raw.map(item => {
      const comma = item.lastIndexOf(',');
      const city = comma >= 0 ? item.slice(0, comma).trim() : item;
      const state = comma >= 0 ? item.slice(comma + 1).trim() : '';
      const info = marketFor(city, state);
      const app = applicationDecision(info);
      return { city, state, region: info.region || 'Unassigned market', status: info.status || DEFAULT.status, territory_status: info.territory_status || DEFAULT.territory_status, lead_priority: info.lead_priority || DEFAULT.lead_priority, resolution_level: info.resolution_level || 'fallback', application_decision: app.decision, application_action: app.action };
    });
    ensureHidden(form, 'Selected Market Routing', 'selectedMarketRouting').value = classified.map(x => `${x.city}, ${x.state} | ${x.region} | ${x.status} | ${x.territory_status} | ${x.resolution_level} | ${x.application_decision} | priority ${x.lead_priority}`).join('; ');
    ensureHidden(form, 'Partner Application Decisions', 'partnerApplicationDecisions').value = classified.map(x => `${x.city}, ${x.state}: ${x.application_decision}`).join('; ');
    ensureHidden(form, 'Partner Preference Tier', 'partnerPreferenceTier').value = profile.tier;
    ensureHidden(form, 'Partner Routing Score', 'partnerRoutingScore').value = String(profile.score);
    ensureHidden(form, 'Shared Lead Interest', 'sharedLeadInterest').value = profile.shared ? 'yes' : 'no';
    ensureHidden(form, 'Exclusive Territory Interest', 'exclusiveTerritoryInterest').value = profile.exclusive ? 'yes' : 'no';
    ensureHidden(form, 'Partner Routing Summary', 'partnerRoutingSummary').value = `lead=${profile.leadModel || 'unspecified'} | response=${profile.responseTime || 'unspecified'} | radius=${profile.radius || 'unspecified'} | capacity=${profile.capacity || 'unspecified'} | inside=${profile.inside || 'unspecified'} | availability=${profile.availability || 'unspecified'} | tier=${profile.tier} | score=${profile.score}`;
    ensureHidden(form, 'Application Source', 'applicationSource').value = 'Nationwide Partner Page';
    ensureHidden(form, 'Routing Policy', 'routingPolicy').value = 'Application review only; selection does not establish coverage or create an SEO page';
    const summary = document.getElementById('territorySummary');
    if (summary) {
      summary.innerHTML = '';
      classified.forEach(x => { const row = document.createElement('div'); row.className = 'territory-row'; const title = document.createElement('strong'); title.textContent = x.city + ', ' + x.state; const detail = document.createElement('div'); detail.textContent = (x.region ? x.region + ' · ' : '') + publicLabel(x); row.append(title, detail); summary.appendChild(row); });
    }
    const homeCity = document.getElementById('homeCity');
    const homeState = document.getElementById('homeState');
    if (homeCity && homeState) {
      const primary = marketFor(homeCity.value, homeState.value);
      const primaryDecision = applicationDecision(primary);
      ensureHidden(form, 'Primary Market Status', 'primaryMarketStatus').value = primary.status || DEFAULT.status;
      ensureHidden(form, 'Primary Territory Status', 'primaryTerritoryStatus').value = primary.territory_status || DEFAULT.territory_status;
      ensureHidden(form, 'Primary Market Region', 'primaryMarketRegion').value = primary.region || DEFAULT.region;
      ensureHidden(form, 'Primary Market Resolution Level', 'primaryMarketResolutionLevel').value = primary.resolution_level || 'fallback';
      ensureHidden(form, 'Partner Application Decision', 'partnerApplicationDecision').value = primaryDecision.decision;
      ensureHidden(form, 'Partner Application Next Action', 'partnerApplicationNextAction').value = primaryDecision.action;
    }
  }

  function syncCanonicalCityPicker() {
    if (!cityCatalog || !Array.isArray(cityCatalog.cities)) return;
    const search = document.getElementById('citySearch'), filter = document.getElementById('stateFilter'), results = document.getElementById('cityResults');
    if (!search || !filter || !results) return;
    const catalog = cityCatalog.cities.map(c => ({ city: String(c.city || '').trim(), state: String(c.state_code || '').trim().toUpperCase(), stateName: String(c.state || c.state_code || '').trim(), region: String(c.region || '').trim() })).filter(c => c.city && c.state).sort((a,b) => a.city.localeCompare(b.city) || a.state.localeCompare(b.state));
    function selectedKeys() { const input = document.getElementById('selectedCitiesInput'); return new Set(String(input && input.value || '').split(';').map(v=>v.trim()).filter(Boolean).map(v=>{ const i=v.lastIndexOf(','); return normalize(i>=0?v.slice(0,i):v)+'|'+String(i>=0?v.slice(i+1):'').trim().toUpperCase(); })); }
    function renderCanonical() {
      const q=normalize(search.value), st=String(filter.value||'').toUpperCase(), chosen=selectedKeys();
      const rows=catalog.filter(c=>(!q||normalize(c.city).includes(q)||normalize(c.state).includes(q)||normalize(c.stateName).includes(q)||normalize(c.region).includes(q))&&(!st||c.state===st)&&(!activeLetter||c.city.toUpperCase().startsWith(activeLetter)));
      results.innerHTML='';
      if(!rows.length){results.innerHTML='<div class="city">No matching catalog city. Use manual city entry below.</div>';return;}
      rows.forEach(c=>{const row=document.createElement('div');row.className='city';const info=document.createElement('div');const strong=document.createElement('strong');strong.textContent=c.city;const small=document.createElement('small');const market=marketFor(c.city,c.state);small.textContent=(c.stateName||c.state)+' ('+c.state+')'+(c.region?' · '+c.region:'')+' · '+publicLabel(market);info.append(strong,small);const button=document.createElement('button');button.type='button';button.className='add';const exists=chosen.has(normalize(c.city)+'|'+c.state);button.textContent=exists?'Selected':'Add City';button.disabled=exists;if(!exists)button.onclick=function(){if(typeof window.add==='function')window.add(c.city,c.state);setTimeout(renderCanonical,0);};row.append(info,button);results.appendChild(row);});
    }
    search.oninput=renderCanonical;filter.onchange=renderCanonical;
    document.querySelectorAll('#letters .letter').forEach(button=>{button.onclick=function(){activeLetter=button.textContent==='All'?'':button.textContent;document.querySelectorAll('#letters .letter').forEach(x=>x.classList.remove('active'));button.classList.add('active');renderCanonical();};});
    window.render = renderCanonical;
    renderCanonical();
  }

  async function loadRouting() {
    try { const [routingResponse,cityResponse]=await Promise.all([fetch('../data/market-routing.json',{cache:'no-store'}),fetch('../data/cities.json',{cache:'no-store'})]); if(routingResponse.ok)routing=await routingResponse.json(); if(cityResponse.ok)cityCatalog=await cityResponse.json(); } catch (_) {}
    syncCanonicalCityPicker(); classifySelection(); document.dispatchEvent(new CustomEvent('partner-routing-ready'));
  }
  document.addEventListener('DOMContentLoaded',function(){const form=document.getElementById('partnerForm');if(form)form.addEventListener('submit',classifySelection,true);['leadModel','responseTime','radius','capacity','insidePickup','availability'].forEach(id=>{const el=document.getElementById(id);if(el)el.addEventListener('change',classifySelection);});loadRouting();});
  window.FreeReliablePartnerRouting={classify:marketFor,label:publicLabel,decision:applicationDecision,preference:preferenceProfile,refresh:classifySelection,syncCityPicker:syncCanonicalCityPicker};
})();
