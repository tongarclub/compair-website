/**
 * aff-render.js — Manual Affiliate Renderer
 * ข้อมูลสินค้ามาจาก data/affiliate/manual-picks.json เท่านั้น
 *
 * API:
 *   loadAffiliate(key, opts)        — render strip ของสินค้า
 *   loadAffiliateGuide(key, opts)   — render คอลัมน์ใน Buying Guide table
 */

const AFF_DATA_URL = '../data/affiliate/manual-picks.json';
let _affCache = null;

async function _getAffData() {
  if (_affCache) return _affCache;
  try {
    _affCache = await fetch(AFF_DATA_URL).then(r => r.json());
  } catch (_) {
    _affCache = {};
  }
  return _affCache;
}

function _cardHTML(item) {
  const img    = item.image
    ? `<img class="aff-card-img" src="${item.image}" alt="${item.title}" loading="lazy">`
    : `<div class="aff-card-img aff-card-img-placeholder"></div>`;
  const badge  = item.badge
    ? `<span class="aff-badge-manual">${item.badge}</span>`
    : '';
  const orig   = (item.original_price && item.original_price > item.price)
    ? `<span class="aff-orig">฿${Number(item.original_price).toLocaleString()}</span>`
    : '';

  // Mall badge — แสดงถ้าชื่อร้านมีคำว่า "official" (case-insensitive)
  const isOfficial = item.shop_name && /official/i.test(item.shop_name);
  const mallBadge  = isOfficial
    ? `<span class="aff-mall-badge">Mall</span>`
    : '';

  // Footer: source · shop name · sold
  const sourcePart = item.source
    ? `<span class="aff-card-source">${item.source}</span>`
    : '';
  const shopPart = item.shop_name
    ? `<span class="aff-card-shop" title="${item.shop_name}">${item.shop_name}</span>`
    : '';
  const sold = Number(item.item_sold) || 0;
  const soldPart = sold > 0
    ? `<span class="aff-sold${sold >= 10 ? ' aff-sold-hot' : ''}">${sold >= 10 ? '🔥' : '⚡'} ขายได้ ${sold} ชิ้น</span>`
    : '';
  const footer = (sourcePart || shopPart || soldPart)
    ? `<div class="aff-card-footer">${sourcePart}${shopPart}${soldPart}</div>`
    : '';

  return `<a class="aff-card" href="${item.link}" target="_blank" rel="noopener sponsored">
    ${mallBadge}
    ${img}
    <div class="aff-card-body">
      ${badge}
      <div class="aff-card-title">${item.title}</div>
      <div class="aff-card-price">
        <span class="aff-price">฿${Number(item.price).toLocaleString()}</span>
        ${orig}
      </div>
      ${footer}
    </div>
    <span class="aff-card-arrow">→</span>
  </a>`;
}

/**
 * loadAffiliate — แสดง affiliate strip
 * @param {string} key      — key ใน manual-picks.json (เช่น "ai_calculator")
 * @param {object} opts
 *   stripId  {string} — id ของ .aff-strip container
 *   cardsId  {string} — id ของ .aff-strip-cards container
 *   labelId  {string} — id ของ label element (optional)
 *   filterId {string} — กรองเฉพาะ item ที่มี ids[] ครอบคลุม id นี้ (optional)
 *                       item ที่ไม่มี field "ids" จะแสดงเสมอ (fallback)
 */
async function loadAffiliate(key, opts = {}) {
  const data    = await _getAffData();
  const section = data[key];
  if (!section || !Array.isArray(section.items)) return;

  const strip = opts.stripId ? document.getElementById(opts.stripId) : null;
  const cards = opts.cardsId ? document.getElementById(opts.cardsId) : null;
  if (!cards) return;

  // กรอง items ตาม filterId (ถ้ามี)
  let items = section.items;
  if (opts.filterId) {
    items = items.filter(i =>
      !Array.isArray(i.ids) || i.ids.includes(opts.filterId)
    );
  }

  // ถ้าไม่มีสินค้าหลังกรอง → ซ่อน strip แล้วหยุด
  if (!items.length) {
    if (strip) strip.style.display = 'none';
    return;
  }

  if (opts.labelId && section.label) {
    const lbl = document.getElementById(opts.labelId);
    if (lbl) lbl.textContent = section.label;
  }

  cards.innerHTML = items.map(_cardHTML).join('');
  if (strip) strip.style.display = '';
}

/**
 * loadAffiliateGuide — เติมคอลัมน์ "ซื้อ" ใน Buying Guide table
 * @param {string} key      — key ใน manual-picks.json
 * @param {string} selector — CSS selector ของ <td> cells (เช่น ".gt-buy-cell[data-pick]")
 */
async function loadAffiliateGuide(key, selector) {
  const data    = await _getAffData();
  const section = data[key];
  if (!section || !Array.isArray(section.guide)) return;

  const ARROW = `<svg width="10" height="10" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 8h10M9 4l4 4-4 4"/></svg>`;

  document.querySelectorAll(selector).forEach(cell => {
    const pick = section.guide.find(g => g.row === +cell.dataset.pick);
    if (!pick || !pick.link) return;

    const priceHtml = pick.price != null
      ? `<div class="gt-buy-price">฿${Number(pick.price).toLocaleString()}</div>`
      : '';
    const hintHtml  = pick.hint
      ? `<div class="gt-buy-hint">${pick.hint}</div>`
      : '';

    cell.innerHTML = `<div class="gt-buy-pick">
      <div class="gt-buy-name">${pick.name}</div>
      ${hintHtml}
      ${priceHtml}
      <a class="gt-buy-cta" href="${pick.link}" target="_blank" rel="noopener sponsored">
        ดูสินค้า ${ARROW}
      </a>
    </div>`;
  });
}
