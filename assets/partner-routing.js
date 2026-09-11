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
    if (!routing || !Array.isArray(routing.markets)) return { ...DEFAULT };
    const stateCode = String(state || '').trim().toUpperCase();
    const cityName = normalize(city);

    const exact = routing.markets.find(m =>
      String(m.state_code || '').toUpperCase() === stateCode &&
      m.city && normalize(m.city) === cityName
    );
    if (exact) return exact;

    let region = null;
    if (cityCatalog && Array.isArray(cityCatalog.cities)) {
      const catalogCity = cityCatalog.cities.find(c =>
        String(c.state_code || '').toUpperCase() === stateCode &&
        normalize(c.city) === cityName
      );
      if (catalogCity && catalogCity.region) region = catalogCity.region;
    }

    if (region) {
      const regional = routing.markets.find(m =>
        String(m.state_code || '').toUpperCase() === stateCode &&
        !m.city && normalize(m.region) === normalize(region)
      );
      if (regional) return regional;
    }

    if (Array.isArray(routing.state_defaults)) {
      const statewide = routing.state_defaults.find(s =>
        String(s.state_code || '').toUpperCase() === stateCode
      );
      if (statewide) return statewide;
    }

    return { ...DEFAULT, state_code: stateCode, city };
  }

  function publicLabel(info) {
    if (info.status === 'direct' || info.territory_status === 'protected') {
      return 'Established operation — backup or overflow applications may be reviewed';
    }
    if (info.status === 'partner-supported' || info.territory_status === 'assigned') {
      return 'Partner-supported market — applications reviewed for future availability';
    }
    if (info.status === 'partner-recruiting') {
      return 'Partner recruiting — applications welcome';
    }
    if (info.territory_status === 'waitlist') {
      return 'Waitlist market — application may be held for future review';
    }
    return 'Future market — application can be reviewed';
  }

  function ensureHidden(form, name, id) {
    let input = form.querySelector('#' + id);
    if (!input) {
      input = document.createElement('input');
      input.type = 'hidden';
      input.name = name;
      input.id = id;
      form.appendChild(input);
    }
    return input;
  }

  function classifySelection() {
    const form = document.getElementById('partnerForm');
    const selectedInput = document.getElementById('selectedCitiesInput');
    if (!form || !selectedInput) return;

    const raw = String(selectedInput.value || '').split(';').map(v => v.trim()).filter(Boolean);
    const classified = raw.map(item => {
      const comma = item.lastIndexOf(',');
      const city = comma >= 0 ? item.slice(0, comma).trim() : item;
      const state = comma >= 0 ? item.slice(comma + 1).trim() : '';
      const info = marketFor(city, state);
      return {
        city,
        state,
        region: info.region || 'Unassigned market',
        status: info.status || DEFAULT.status,
        territory_status: info.territory_status || DEFAULT.territory_status,
        lead_priority: info.lead_priority || DEFAULT.lead_priority
      };
    });

    ensureHidden(form, 'Selected Market Routing', 'selectedMarketRouting').value = classified
      .map(x => `${x.city}, ${x.state} | ${x.region} | ${x.status} | ${x.territory_status} | priority ${x.lead_priority}`)
      .join('; ');
    ensureHidden(form, 'Application Source', 'applicationSource').value = 'Nationwide Partner Page';
    ensureHidden(form, 'Routing Policy', 'routingPolicy').value = 'Application review only; selection does not establish coverage or create an SEO page';

    const homeCity = document.getElementById('homeCity');
    const homeState = document.getElementById('homeState');
    if (homeCity && homeState) {
      const primary = marketFor(homeCity.value, homeState.value);
      ensureHidden(form, 'Primary Market Status', 'primaryMarketStatus').value = primary.status || DEFAULT.status;
      ensureHidden(form, 'Primary Territory Status', 'primaryTerritoryStatus').value = primary.territory_status || DEFAULT.territory_status;
      ensureHidden(form, 'Primary Market Region', 'primaryMarketRegion').value = primary.region || DEFAULT.region;
    }
  }

  function syncCanonicalCityPicker() {
    if (!cityCatalog || !Array.isArray(cityCatalog.cities)) return;
    const search = document.getElementById('citySearch');
    const filter = document.getElementById('stateFilter');
    const results = document.getElementById('cityResults');
    if (!search || !filter || !results) return;

    const catalog = cityCatalog.cities
      .map(c => ({
        city: String(c.city || '').trim(),
        state: String(c.state_code || '').trim().toUpperCase(),
        stateName: String(c.state || c.state_code || '').trim(),
        region: String(c.region || '').trim()
      }))
      .filter(c => c.city && c.state)
      .sort((a, b) => a.city.localeCompare(b.city) || a.state.localeCompare(b.state));

    function selectedKeys() {
      const input = document.getElementById('selectedCitiesInput');
      return new Set(String(input && input.value || '')
        .split(';').map(v => v.trim()).filter(Boolean)
        .map(v => {
          const i = v.lastIndexOf(',');
          return normalize(i >= 0 ? v.slice(0, i) : v) + '|' + String(i >= 0 ? v.slice(i + 1) : '').trim().toUpperCase();
        }));
    }

    function renderCanonical() {
      const q = normalize(search.value);
      const st = String(filter.value || '').toUpperCase();
      const chosen = selectedKeys();
      const rows = catalog.filter(c =>
        (!q || normalize(c.city).includes(q) || normalize(c.state).includes(q) || normalize(c.stateName).includes(q) || normalize(c.region).includes(q)) &&
        (!st || c.state === st) &&
        (!activeLetter || c.city.toUpperCase().startsWith(activeLetter))
      );

      results.innerHTML = '';
      if (!rows.length) {
        results.innerHTML = '<div class="city">No matching catalog city. Use manual city entry below.</div>';
        return;
      }

      rows.forEach(c => {
        const row = document.createElement('div');
        row.className = 'city';
        const info = document.createElement('div');
        const strong = document.createElement('strong');
        strong.textContent = c.city;
        const small = document.createElement('small');
        small.textContent = (c.stateName || c.state) + ' (' + c.state + ')' + (c.region ? ' · ' + c.region : '');
        info.append(strong, small);

        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'add';
        const exists = chosen.has(normalize(c.city) + '|' + c.state);
        button.textContent = exists ? 'Selected' : 'Add City';
        button.disabled = exists;
        if (!exists) button.onclick = function () {
          if (typeof window.add === 'function') window.add(c.city, c.state);
          setTimeout(renderCanonical, 0);
        };
        row.append(info, button);
        results.appendChild(row);
      });
    }

    search.oninput = renderCanonical;
    filter.onchange = renderCanonical;
    document.querySelectorAll('#letters .letter').forEach(button => {
      button.onclick = function () {
        activeLetter = button.textContent === 'All' ? '' : button.textContent;
        document.querySelectorAll('#letters .letter').forEach(x => x.classList.remove('active'));
        button.classList.add('active');
        renderCanonical();
      };
    });

    renderCanonical();
  }

  async function loadRouting() {
    try {
      const [routingResponse, cityResponse] = await Promise.all([
        fetch('../data/market-routing.json', { cache: 'no-store' }),
        fetch('../data/cities.json', { cache: 'no-store' })
      ]);
      if (routingResponse.ok) routing = await routingResponse.json();
      if (cityResponse.ok) cityCatalog = await cityResponse.json();
    } catch (_) {
      // Safe fallback remains request-only/available.
    }
    syncCanonicalCityPicker();
    document.dispatchEvent(new CustomEvent('partner-routing-ready'));
  }

  document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('partnerForm');
    if (form) form.addEventListener('submit', classifySelection, true);
    loadRouting();
  });

  window.FreeReliablePartnerRouting = {
    classify: marketFor,
    label: publicLabel,
    refresh: classifySelection,
    syncCityPicker: syncCanonicalCityPicker
  };
})();
