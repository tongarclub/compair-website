/**
 * aff-utils.js — Shared affiliate strip utilities
 *
 * Provides:
 *   affVariant()                       → 'A' | 'B' (persistent 50/50 A/B split)
 *   affCardHTML(item, page, placement) → HTML string for one product card
 *   affTrackClick(el, page, placement) → GA4 event on click
 *   affTrackImpression(page, placement, count) → GA4 impression event
 *
 * Loaded as a plain <script> (not a module) — functions are global.
 * Phase 3: GA4 event tracking across all placements + A/B test.
 */

/* ── A/B Variant (persistent per browser) ───────────────────── */
function affVariant() {
  let v = localStorage.getItem('aff_v');
  if (!v) {
    v = Math.random() < 0.5 ? 'A' : 'B';
    localStorage.setItem('aff_v', v);
  }
  return v;
}

/* ── Card HTML ───────────────────────────────────────────────── */
function affCardHTML(item, page, placement) {
  page      = page      || 'unknown';
  placement = placement || 'strip';

  const disc   = parseInt(item.discount_percentage || 0);
  const link   = item.affiliate_link || item.product_link || '#';
  const saleP  = parseInt(item.sale_price || 0).toLocaleString('th-TH');
  // Original price: use item.price when discounted, or item.original_price
  const origRaw = disc > 0
    ? parseInt(item.price || item.original_price || 0)
    : parseInt(item.original_price || 0);
  const origP  = origRaw > parseInt(item.sale_price || 0)
    ? origRaw.toLocaleString('th-TH')
    : null;
  const rating = parseFloat(item.item_rating || 0).toFixed(1);
  const sold   = parseInt(item.item_sold || 0);
  const sFmt   = sold >= 1000
    ? (sold / 1000).toFixed(1).replace('.0', '') + 'K'
    : sold || '';
  const title  = (item.title || item.name || 'สินค้าแนะนำ')
    .replace(/^[^\w\u0E00-\u0E7F\u0020]+/, '').trim();
  const img    = item.image_link || item.image_url || item.img || '';

  return `<a class="aff-card" href="${link}" target="_blank" rel="noopener sponsored"
     data-aff-page="${page}" data-aff-placement="${placement}"
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
    page:      page,
    placement: placement,
    variant:   affVariant(),
    link:      el.href,
    title:     el.querySelector('.aff-card-title')?.textContent?.trim().slice(0, 60) || '',
  });
}

/* ── GA4 Impression Tracking ─────────────────────────────────── */
function affTrackImpression(page, placement, count) {
  if (typeof gtag !== 'function') return;
  gtag('event', 'affiliate_impression', {
    page:      page,
    placement: placement,
    variant:   affVariant(),
    count:     count,
  });
}
