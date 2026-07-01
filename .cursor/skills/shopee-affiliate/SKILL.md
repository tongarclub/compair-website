# ComPair — Multi-Source Affiliate System (Shopee + Lazada)

> ระบบ affiliate ครบวงจรสำหรับ ComPair — รองรับ Shopee และ Lazada พร้อม GA4 tracking + A/B test

---

## Architecture Overview

```
data/affiliate/
├── guide-picks.json          ← ✨ Buying Guide curated picks (แก้ที่นี่ที่เดียว)
│
├── [SHOPEE — csv datafeed]
│   ├── gpu.json              ← GPU / การ์ดจอ
│   ├── mac.json              ← Mac / อุปกรณ์เสริม Mac
│   ├── mac_accessories.json  ← Mac accessories เพิ่มเติม
│   ├── solar_panel.json      ← แผงโซล่าเซลล์
│   ├── solar_inverter.json   ← อินเวอร์เตอร์ / MPPT Controller
│   ├── ev_charger.json       ← EV Charger
│   ├── gold_invest.json      ← ทองคำ / เครื่องประดับ
│   └── shopee-urls-to-shorten.txt  ← working file สำหรับ short link
│
├── [LAZADA — API datafeed]
│   ├── lazada_gpu.json       ← Computers & Components (L1: 3834)
│   ├── lazada_laptop.json    ← Computers & Components (L1: 3834)
│   ├── lazada_headphone.json ← Audio (L1: 10100387)
│   ├── lazada_smartwatch.json← Smart Devices (L1: 10100412)
│   ├── lazada_gaming.json    ← Gaming Devices (L1: 10100871)
│   ├── lazada_air_conditioner.json  ← Home Appliances (L1: 3833)
│   ├── lazada_washing_machine.json  ← Home Appliances (L1: 3833)
│   ├── lazada_water_filter.json     ← Home Appliances (L1: 3833)
│   ├── lazada_air_purifier.json     ← Home Appliances (L1: 3833)
│   ├── lazada_solar_panel.json      ← Home Appliances (L1: 3833)
│   └── lazada_ev_charger.json       ← Home Appliances (L1: 3833)
│
js/
└── aff-utils.js              ← ✨ affVariant, affMerge, affCardHTML, affTrackClick

css/
└── shared.css                ← .aff-strip + .aff-badge--shopee/lazada CSS

scripts/
├── pull_lazada_products.py   ← ดึง Lazada products → JSON (รัน manual หรือ cron)
├── apply_short_links.py      ← อัปเดต Shopee short links
├── test_lazada_api.py        ← ทดสอบ Lazada API credentials
└── lazop/                    ← Official Lazada Python SDK
```

---

## Placement Map — สินค้าแสดงที่ไหนบ้าง

| หน้า | Shopee | Lazada | Strip | Spec CTA | Guide Table |
|---|---|---|---|---|---|
| `ai-calculator.html` | `gpu.json` → `_isGpu()` filter | ❌ disabled (Lazada feed ไม่มี GPU) | ✅ Shopee only (hidden ถ้าไม่มี match) | ✅ | — |
| `mac-llm-calculator.html` | `mac.json` + `mac_accessories.json` → `_isMacProduct()` | `lazada_laptop.json` (44 items, exclusion-only filter) | ✅ chip match | ✅ | ✅ 7 rows |
| `image-gen-calculator.html` | — | — | — | — | ✅ 3 rows |
| `solar-calculator.html` | `solar_panel.json` + `solar_inverter.json` → `_isSolarProduct()` | ❌ disabled (L1=3833 คืน washing machine) | ✅ Shopee only | — | — |
| `ev-calculator.html` | `ev_charger.json` → `_isEvCharger()` | ❌ disabled (L1=3833 คืน washing machine) | ✅ Shopee only | — | — |
| `gold-calculator.html` | `gold_invest.json` | — | ✅ | — | — |

**Display:** แยก 2 section (Shopee / Lazada) ต่าง header — ใช้ `affRenderSplit()` ใน `aff-utils.js`  
**Section ซ่อนตัวเองถ้า:** filtered array ว่างเปล่า (เช่น series ไม่มีสต็อก Shopee → Shopee section hidden)  
**⚠ Lazada API Limitations (ค้นพบจากการทดสอบ Jul 2026):**
- `/marketing/product/feed` รองรับแค่ `categoryL1` ระดับ L1 เท่านั้น — L2/L3/categoryId ไม่ทำงาน
- `keyword` parameter ถูก ignore ทั้งหมด — คืน random feed เหมือนกัน
- L1=3834 (Computers) คืน laptops เป็นส่วนใหญ่ — ไม่มี GPU card เลย
- L1=3833 (Home Appliances) คืน washing machine / dehumidifier — ไม่มี EV/Solar
- **GPU section disabled:** ใช้ Shopee only สำหรับ ai-calculator
- **EV/Solar disabled:** ใช้ Shopee only พร้อม keyword filter

---

## Part 1: Refresh Lazada Data

### รัน Script

```bash
# ดึงทุก category (แนะนำ: รัน weekly)
python3 scripts/pull_lazada_products.py --all --limit 50

# ดึงเฉพาะ category เดียว
python3 scripts/pull_lazada_products.py --category gpu

# ดู categories ทั้งหมด
python3 scripts/pull_lazada_products.py --list-categories
```

### Categories ที่รองรับ

| slug | L1 Category | ไฟล์ output |
|---|---|---|
| `gpu` | ❌ ไม่มี GPU ในฟีด | ไม่ใช้ (Lazada feed คืน laptop เท่านั้น) |
| `laptop` | Computers & Components (3834) | `lazada_laptop.json` — 44 unique laptops |
| `headphone` | Audio (10100387) | `lazada_headphone.json` |
| `smartwatch` | Smart Devices (10100412) | `lazada_smartwatch.json` |
| `gaming` | Gaming (10100871) | `lazada_gaming.json` |
| `air_conditioner` | Home Appliances (3833) | `lazada_air_conditioner.json` |
| `washing_machine` | Home Appliances (3833) | `lazada_washing_machine.json` |
| `water_filter` | Home Appliances (3833) | `lazada_water_filter.json` |
| `air_purifier` | Home Appliances (3833) | `lazada_air_purifier.json` |
| `solar_panel` | Home Appliances (3833) | `lazada_solar_panel.json` |
| `ev_charger` | Home Appliances (3833) | `lazada_ev_charger.json` |

### .env ที่ต้องมี

```
LAZADA_APP_KEY=105827
LAZADA_APP_SECRET=xxxx
LAZADA_USER_TOKEN=xxxx    ← จาก Lazada Affiliate Dashboard
```

### ทดสอบ credentials

```bash
python3 scripts/test_lazada_api.py
```

ต้องเห็น `✅ ได้ X สินค้า` ใน Test 1

---

## Part 2: แก้ไข Buying Guide Picks (Shopee)

ไฟล์: `data/affiliate/guide-picks.json` — แก้ที่นี่ที่เดียว หน้าเว็บ fetch อัตโนมัติ

```json
{
  "mac-llm": [
    {
      "row": 0,
      "label": "...",
      "name": "...",
      "hint": "...",
      "price": 323,
      "link": "https://s.shopee.co.th/XXXXX"
    }
  ],
  "image-gen-gpu": [...]
}
```

---

## Part 3: Generate Shopee Short Links

```
Portal:     https://affiliate.shopee.co.th/offer/custom_link
Partner ID: 15358640421
```

### ขั้นตอน

1. เปิด `data/affiliate/shopee-urls-to-shorten.txt`
2. Copy original URLs (batch ที่ยังไม่มี short link)
3. Portal → Paste → **รับลิงก์** → Copy short links
4. Paste กลับใต้ original URLs (คั่นบรรทัดว่าง 1 บรรทัด)
5. รัน: `python3 scripts/apply_short_links.py`

---

## Part 4: Shared JS — aff-utils.js

| Function | หน้าที่ |
|---|---|
| `affVariant()` | Return `'A'`\|`'B'` — 50/50 A/B, persistent via `localStorage` |
| `affMerge(...lists)` | Merge Shopee + Lazada arrays, dedupe by title, sort by score |
| `affCardHTML(item, page, placement)` | HTML string สำหรับ product card + source badge |
| `affTrackClick(el, page, placement)` | GA4 `affiliate_click` event |
| `affTrackImpression(page, placement, count, sources)` | GA4 `affiliate_impression` event |

### Multi-source card HTML

`affCardHTML()` ดู `item.source` อัตโนมัติ:
- `source: 'shopee'` → badge `SP` สีส้ม
- `source: 'lazada'` → badge `Laz` สีน้ำเงิน

### เพิ่ม Strip หน้าใหม่ (multi-source template)

```javascript
// 1. Fetch + merge
let _xxxAffCache = null;
async function getXxxAffData() {
  if (_xxxAffCache) return _xxxAffCache;
  try {
    const [r1, r2] = await Promise.allSettled([
      fetch('../data/affiliate/xxx.json').then(r => r.json()),
      fetch('../data/affiliate/lazada_xxx.json').then(r => r.json()),
    ]);
    const shopee = r1.status === 'fulfilled' ? (r1.value.items || []) : [];
    const lazada = r2.status === 'fulfilled' ? (r2.value.items || []) : [];
    _xxxAffCache = affMerge(shopee, lazada);
  } catch(e) { _xxxAffCache = []; }
  return _xxxAffCache;
}

// 2. Render
async function renderXxxAffiliate() {
  const box = document.getElementById('xxxAffBox');
  const cardsEl = document.getElementById('xxxAffCards');
  const items = await getXxxAffData();
  if (!items.length) return;

  const v = affVariant();
  const picks = items.slice(0, v === 'B' ? 1 : 3);
  box.classList.toggle('variant-b', v === 'B');
  cardsEl.innerHTML = picks.map(i => affCardHTML(i, 'xxx_page', 'strip')).join('');
  box.style.display = 'none'; void box.offsetWidth; box.style.display = '';
  const srcs = [...new Set(picks.map(i => i.source || 'shopee'))].join(',');
  affTrackImpression('xxx_page', 'strip', picks.length, srcs);
}
```

```html
<!-- HTML placeholder -->
<div class="aff-strip" id="xxxAffBox" style="display:none" data-aff-placement="xxx_strip">
  <div class="aff-strip-header">
    <span class="aff-strip-label">สินค้าแนะนำ</span>
  </div>
  <div class="aff-strip-cards" id="xxxAffCards"></div>
</div>

<!-- โหลด script ก่อน </body> -->
<script src="../js/aff-utils.js"></script>
```

---

## Part 5: GA4 Tracking

| Event | Parameters |
|---|---|
| `affiliate_click` | `page`, `placement`, `variant`, `source` (shopee/lazada), `link`, `title` |
| `affiliate_impression` | `page`, `placement`, `variant`, `count`, `sources` (shopee/lazada/shopee,lazada) |

**ดูผล A/B Test:**
```
CTR = affiliate_click / affiliate_impression (per variant, per source)
```

**ดูใน GA4:** Reports → Engagement → Events → `affiliate_click` → filter by `source`

---

## Quick Reference

| Task | คำสั่ง |
|---|---|
| Refresh Lazada data | `python3 scripts/pull_lazada_products.py --all` |
| Test Lazada API | `python3 scripts/test_lazada_api.py` |
| Apply Shopee short links | `python3 scripts/apply_short_links.py` |
| Reset A/B variant | `localStorage.removeItem('aff_v')` ใน DevTools |
| ดู Lazada categories | `python3 scripts/pull_lazada_products.py --list-categories` |

```
Shopee Partner ID: 15358640421
Shopee Portal:     https://affiliate.shopee.co.th/offer/custom_link
Lazada Portal:     https://open.lazada.com/apps/myapp
Lazada Dashboard:  https://affiliate.lazada.co.th
GA4 ID:            G-J3C1X16FZ5
```
