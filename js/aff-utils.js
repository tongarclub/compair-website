/**
 * aff-utils.js — Shared affiliate strip utilities
 *
 * Provides:
 *   affVariant()        → 'A' | 'B'  (persistent 50/50 A/B split)
 *   affMerge(...lists)  → merged + sorted array (backward compat)
 *   affRenderSplit(cfg) → render Shopee section + Lazada section separately
 *   affCardHTML(item, page, placement) → HTML string for one product card
 *   affTrackClick(el, page, placement)
 *   affTrackImpression(page, placement, count, sources)
 *
 * Loaded as a plain <script> (not a module) — all functions are global.
 */

/* ── A/B Variant ─────────────────────────────────────────────── */
function affVariant() {
  let v = localStorage.getItem('aff_v');
  if (!v) {
    v = Math.random() < 0.5 ? 'A' : 'B';
    localStorage.setItem('aff_v', v);
  }
  return v;
}

/* ── Merge helper (backward compat, used when split not needed) ─ */
function affMerge(...lists) {
  const seen   = new Set();
  const merged = [];
  for (const list of lists) {
    if (!Array.isArray(list)) continue;
    for (const item of list) {
      if (!item.source) item.source = 'shopee';
      const key = (item.title || '').toLowerCase()
        .replace(/[^a-z0-9\u0e00-\u0e7f]/g, '').slice(0, 20);
      if (!key || seen.has(key)) continue;
      seen.add(key);
      merged.push(item);
    }
  }
  return merged.sort((a, b) => {
    const score = x =>
      (parseInt(x.item_sold || 0) + 1) *
      (parseFloat(x.item_rating || 4)) *
      (1 + parseInt(x.discount_percentage || 0) / 100);
    return score(b) - score(a);
  });
}

/* ── Sort a single source array by score ─────────────────────── */
function _affSort(items) {
  return [...items].sort((a, b) => {
    const score = x =>
      (parseInt(x.item_sold || 0) + 1) *
      (parseFloat(x.item_rating || 4)) *
      (1 + parseInt(x.discount_percentage || 0) / 100);
    return score(b) - score(a);
  });
}

/**
 * affRenderSplit — render Shopee section + Lazada section separately
 *
 * @param {object} cfg
 *   shopeeItems    {Array}       — pre-filtered Shopee items
 *   lazadaItems    {Array}       — pre-filtered Lazada items
 *   shopeeCardsId  {string}      — id of Shopee cards container
 *   lazadaCardsId  {string}      — id of Lazada cards container
 *   shopeeSectionId{string}      — id of Shopee section wrapper (for hide/show)
 *   lazadaSectionId{string}      — id of Lazada section wrapper
 *   stripEl        {HTMLElement} — main .aff-strip element
 *   page           {string}
 *   placement      {string}
 */
function affRenderSplit(cfg) {
  const v     = affVariant();
  const limit = v === 'B' ? 1 : 3;

  const shopee = _affSort(cfg.shopeeItems || []).slice(0, limit);
  const lazada = _affSort(cfg.lazadaItems || []).slice(0, limit);

  // Render Shopee
  const shopeeCards   = document.getElementById(cfg.shopeeCardsId);
  const shopeeSection = document.getElementById(cfg.shopeeSectionId);
  if (shopeeCards)
    shopeeCards.innerHTML = shopee.map(i => affCardHTML(i, cfg.page, cfg.placement)).join('');
  if (shopeeSection)
    shopeeSection.style.display = shopee.length ? '' : 'none';

  // Render Lazada
  const lazadaCards   = document.getElementById(cfg.lazadaCardsId);
  const lazadaSection = document.getElementById(cfg.lazadaSectionId);
  if (lazadaCards)
    lazadaCards.innerHTML = lazada.map(i => affCardHTML(i, cfg.page, cfg.placement)).join('');
  if (lazadaSection)
    lazadaSection.style.display = lazada.length ? '' : 'none';

  // Show/hide strip + slide-in animation
  const strip = cfg.stripEl;
  if (strip && (shopee.length || lazada.length)) {
    strip.classList.toggle('variant-b', v === 'B');
    strip.style.display = 'none';
    void strip.offsetWidth;
    strip.style.display = '';
  }

  // Track
  const total   = shopee.length + lazada.length;
  const sources = [shopee.length && 'shopee', lazada.length && 'lazada']
    .filter(Boolean).join(',');
  affTrackImpression(cfg.page, cfg.placement, total, sources);
}

/* ── Card HTML ───────────────────────────────────────────────── */
function affCardHTML(item, page, placement) {
  page      = page      || 'unknown';
  placement = placement || 'strip';

  const disc    = parseInt(item.discount_percentage || 0);
  const link    = item.affiliate_link || item.product_link || '#';
  const saleP   = parseInt(item.sale_price || 0).toLocaleString('th-TH');
  const origRaw = disc > 0
    ? parseInt(item.price || item.original_price || 0)
    : parseInt(item.original_price || 0);
  const origP   = origRaw > parseInt(item.sale_price || 0)
    ? origRaw.toLocaleString('th-TH') : null;
  const rating  = parseFloat(item.item_rating || 0).toFixed(1);
  const sold    = parseInt(item.item_sold || 0);
  const sFmt    = sold >= 1000
    ? (sold / 1000).toFixed(1).replace('.0', '') + 'K' : sold || '';
  const title   = (item.title || item.name || 'สินค้าแนะนำ')
    .replace(/^[^\w\u0E00-\u0E7F\u0020]+/, '').trim();
  const img     = item.image_link || item.image_url || item.img || '';
  const src     = item.source || 'shopee';

  return `<a class="aff-card" href="${link}" target="_blank" rel="noopener sponsored"
     data-aff-page="${page}" data-aff-placement="${placement}" data-aff-source="${src}"
     onclick="affTrackClick(this,'${page}','${placement}')">
    ${img
      ? `<img class="aff-card-img" src="${img}" alt="${title}" loading="lazy"
           onerror="this.style.background='var(--surface2)';this.style.display='block'">`
      : `<div class="aff-card-img"></div>`}
    <div class="aff-card-body">
      <div class="aff-card-title">${title}</div>
      <div class="aff-card-price">
        <span class="aff-price">฿${saleP}</span>
        ${origP ? `<span class="aff-orig">฿${origP}</span>` : ''}
        ${disc > 0 ? `<span class="aff-disc">-${disc}%</span>` : ''}
      </div>
      <div class="aff-card-meta">${rating > 0 ? `★${rating} · ` : ''}${sFmt ? `ขาย ${sFmt}` : ''}</div>
    </div>
    <span class="aff-card-arrow">→</span>
  </a>`;
}

/* ── GA4 Click Tracking ──────────────────────────────────────── */
function affTrackClick(el, page, placement) {
  if (typeof gtag !== 'function') return;
  gtag('event', 'affiliate_click', {
    page,
    placement,
    variant:   affVariant(),
    source:    el.dataset.affSource || 'shopee',
    link:      el.href,
    title:     el.querySelector('.aff-card-title')?.textContent?.trim().slice(0, 60) || '',
  });
}

/* ── GA4 Impression Tracking ─────────────────────────────────── */
function affTrackImpression(page, placement, count, sources) {
  if (typeof gtag !== 'function') return;
  gtag('event', 'affiliate_impression', {
    page,
    placement,
    variant: affVariant(),
    count,
    sources: sources || 'shopee',
  });
}
