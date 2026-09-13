const SUPABASE_URL = 'https://hutsrafyktcxpgilogdj.supabase.co';
const SUPABASE_PUBLISHABLE_KEY = 'sb_publishable_eSxdhKuBxrC-Sw7FwmYxGA_oBYCTCgg';

function setStatus(message, ok = true) {
  const el = document.getElementById('marketplaceStatus');
  if (!el) return;
  el.textContent = message;
  el.className = ok ? 'status-ok' : 'status-error';
}

async function loadOpportunityFeed() {
  try {
    const sessionRaw = localStorage.getItem('sb-hutsrafyktcxpgilogdj-auth-token');
    if (!sessionRaw) {
      setStatus('Marketplace database connection is ready. Buyer sign-in is required before live opportunities can be displayed.');
      return;
    }
    const session = JSON.parse(sessionRaw);
    const accessToken = session?.access_token || session?.currentSession?.access_token;
    if (!accessToken) {
      setStatus('Buyer session not found. Sign in before viewing live opportunities.', false);
      return;
    }

    const response = await fetch(`${SUPABASE_URL}/rest/v1/marketplace_opportunity_feed?select=*&order=created_at.desc&limit=20`, {
      headers: {
        apikey: SUPABASE_PUBLISHABLE_KEY,
        Authorization: `Bearer ${accessToken}`,
        Accept: 'application/json'
      }
    });

    if (!response.ok) {
      setStatus('Marketplace database setup is not complete yet. The public website remains safe while setup is finished.', false);
      return;
    }

    const rows = await response.json();
    const container = document.getElementById('liveOpportunities');
    if (!container) return;
    container.innerHTML = '';

    if (!rows.length) {
      container.innerHTML = '<div class="card"><h3>No live opportunities right now</h3><p>New matching appliance opportunities will appear here after qualification.</p></div>';
      setStatus('Live marketplace connection is working.');
      return;
    }

    rows.forEach(row => {
      const card = document.createElement('article');
      card.className = 'card';
      const price = row.opportunity_price == null ? 'Individually priced' : `$${Number(row.opportunity_price).toFixed(0)}`;
      card.innerHTML = `<h3>${row.appliance_count || 1}-appliance opportunity</h3>
        <p><strong>Area:</strong> ${escapeHtml(row.approximate_area || [row.city, row.state].filter(Boolean).join(', ') || 'Local area')}</p>
        <p><strong>Owner report:</strong> ${escapeHtml(row.owner_reported_summary || 'Details available after review')}</p>
        <p><strong>Access:</strong> ${escapeHtml(row.access_summary || 'Not specified')}</p>
        <p><strong>Photos:</strong> ${row.photo_count || 0}</p>
        <p class="price">${price}</p>
        <div class="locked"><strong>Private until verified purchase/assignment:</strong> homeowner name, phone, email and exact address.</div>`;
      container.appendChild(card);
    });
    setStatus(`Live marketplace connection is working. ${rows.length} opportunity${rows.length === 1 ? '' : 'ies'} loaded.`);
  } catch (error) {
    setStatus('Marketplace preview is available, but the live database connection is still being configured.', false);
  }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]));
}

document.addEventListener('DOMContentLoaded', loadOpportunityFeed);
