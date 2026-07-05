/**
 * aff-render.js — Manual Affiliate Renderer
 * ข้อมูลสินค้ามาจาก data/affiliate/manual-picks.json เท่านั้น
 *
 * API:
 *   loadAffiliate(key, opts)        — render strip (preview 3 รายการ + modal ทั้งหมด)
 *   loadAffiliateGuide(key, opts)   — render คอลัมน์ใน Buying Guide table
 */

const AFF_DATA_URL = '../data/affiliate/manual-picks.json';
const AFF_PREVIEW  = 3;   // จำนวนสินค้าที่แสดงใน strip
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

// ─── Card HTML (ใช้ใน strip และ modal) ──────────────────────────────────────

function _cardHTML(item) {
  const img = item.image
    ? `<img class="aff-card-img" src="${item.image}" alt="${item.title}" loading="lazy">`
    : `<div class="aff-card-img aff-card-img-placeholder"></div>`;

  const badge = item.badge
    ? `<span class="aff-badge-manual">${item.badge}</span>`
    : '';

  const orig = (item.original_price && item.original_price > item.price)
    ? `<span class="aff-orig">฿${Number(item.original_price).toLocaleString()}</span>`
    : '';

  const isOfficial = item.shop_name && /official/i.test(item.shop_name);
  const mallBadge  = isOfficial ? `<span class="aff-mall-badge">Mall</span>` : '';

  const sourcePart = item.source
    ? `<span class="aff-card-source">${item.source}</span>` : '';
  const shopPart = item.shop_name
    ? `<span class="aff-card-shop" title="${item.shop_name}">${item.shop_name}</span>` : '';
  const sold = Number(item.item_sold) || 0;
  const soldPart = sold > 0
    ? `<span class="aff-sold${sold >= 10 ? ' aff-sold-hot' : ''}">${sold >= 10 ? '🔥' : '⚡'} ขายได้ ${sold} ชิ้น</span>`
    : '';
  const footer = (sourcePart || shopPart || soldPart)
    ? `<div class="aff-card-footer">${sourcePart}${shopPart}${soldPart}</div>` : '';

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

// ─── Modal ───────────────────────────────────────────────────────────────────

function _openModal(key, items, label) {
  // ลบ modal เดิม (ถ้ามี) เพื่อ refresh เมื่อ filterId เปลี่ยน
  const old = document.getElementById(`aff-modal-${key}`);
  if (old) old.remove();

  const modal = document.createElement('div');
  modal.id        = `aff-modal-${key}`;
  modal.className = 'aff-modal';
  modal.setAttribute('role', 'dialog');
  modal.setAttribute('aria-modal', 'true');
  modal.setAttribute('aria-label', label);

  modal.innerHTML = `
    <div class="aff-modal-backdrop"></div>
    <div class="aff-modal-panel">
      <div class="aff-modal-header">
        <span class="aff-modal-title">${label}</span>
        <span class="aff-modal-count">${items.length} รายการ</span>
        <button class="aff-modal-close" aria-label="ปิด">✕</button>
      </div>
      <div class="aff-modal-body">
        <div class="aff-modal-grid">
          ${items.map(_cardHTML).join('')}
        </div>
      </div>
    </div>`;

  document.body.appendChild(modal);

  const close = () => {
    modal.classList.remove('is-open');
    document.body.style.overflow = '';
    modal.addEventListener('transitionend', () => modal.remove(), { once: true });
  };

  modal.querySelector('.aff-modal-backdrop').addEventListener('click', close);
  modal.querySelector('.aff-modal-close').addEventListener('click', close);
  document.addEventListener('keydown', function onKey(e) {
    if (e.key === 'Escape') { close(); document.removeEventListener('keydown', onKey); }
  });

  // trigger animation
  requestAnimationFrame(() => {
    requestAnimationFrame(() => modal.classList.add('is-open'));
  });
  document.body.style.overflow = 'hidden';
}

// ─── loadAffiliate ───────────────────────────────────────────────────────────

/**
 * loadAffiliate — แสดง affiliate strip (preview 3 รายการ)
 * @param {string} key      — key ใน manual-picks.json (เช่น "ai_calculator")
 * @param {object} opts
 *   stripId  {string} — id ของ .aff-strip container
 *   cardsId  {string} — id ของ .aff-strip-cards container
 *   labelId  {string} — id ของ label element (optional)
 *   filterId {string} — กรองเฉพาะ item ที่มี ids[] ครอบคลุม id นี้ (optional)
 *   preview  {number} — จำนวนสินค้าที่แสดงใน strip (default: 3)
 */
async function loadAffiliate(key, opts = {}) {
  const data    = await _getAffData();
  const section = data[key];
  if (!section || !Array.isArray(section.items)) return;

  const strip = opts.stripId ? document.getElementById(opts.stripId) : null;
  const cards = opts.cardsId ? document.getElementById(opts.cardsId) : null;
  if (!cards) return;

  const allItems = section.items;                 // ทั้งหมดใน section ไม่กรอง
  const label    = section.label || key;

  // กรอง items ตาม filterId (ถ้ามี)
  let items = allItems;
  if (opts.filterId) {
    items = allItems.filter(i =>
      !Array.isArray(i.ids) || i.ids.includes(opts.filterId)
    );
  }

  // ลบปุ่ม "ดูทั้งหมด" / "fallback" เดิม (กรณี filterId เปลี่ยน)
  const oldBtn = strip ? strip.querySelector('.aff-see-more') : null;
  if (oldBtn) oldBtn.remove();

  // ── ไม่มีสินค้าที่ตรงกับ filterId ──────────────────────────────────
  if (!items.length) {
    if (opts.filterId && allItems.length > 0 && strip) {
      // มีสินค้าในหมวดอยู่ แต่ไม่มีสำหรับ GPU/CPU นี้โดยเฉพาะ
      // → แสดง strip ว่าง + ปุ่ม fallback "ดูสินค้าหมวดนี้ทั้งหมด"
      cards.innerHTML = '';
      strip.style.display = '';
      if (opts.labelId && section.label) {
        const lbl = document.getElementById(opts.labelId);
        if (lbl) lbl.textContent = section.label;
      }
      const btn = document.createElement('button');
      btn.className = 'aff-see-more aff-see-more--fallback';
      btn.innerHTML = `ดูสินค้าในหมวดนี้ <strong>${allItems.length}</strong> รายการ <span class="aff-see-more-arrow">→</span>`;
      btn.addEventListener('click', () => _openModal(key, allItems, label));
      strip.appendChild(btn);
    } else {
      if (strip) strip.style.display = 'none';
    }
    return;
  }

  // ── มีสินค้า → แสดงปกติ ────────────────────────────────────────────
  if (opts.labelId && section.label) {
    const lbl = document.getElementById(opts.labelId);
    if (lbl) lbl.textContent = section.label;
  }

  const previewN = opts.preview ?? AFF_PREVIEW;
  cards.innerHTML = items.slice(0, previewN).map(_cardHTML).join('');
  if (strip) strip.style.display = '';

  // ปุ่ม "ดูทั้งหมด" เปิด modal แสดง allItems ทั้ง section
  if (allItems.length > previewN && strip) {
    const btn = document.createElement('button');
    btn.className = 'aff-see-more';
    btn.innerHTML = `ดูสินค้าทั้งหมด <strong>${allItems.length}</strong> รายการ <span class="aff-see-more-arrow">→</span>`;
    btn.addEventListener('click', () => _openModal(key, allItems, label));
    strip.appendChild(btn);
  }
}

// ─── loadAffiliateGuide ──────────────────────────────────────────────────────

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
