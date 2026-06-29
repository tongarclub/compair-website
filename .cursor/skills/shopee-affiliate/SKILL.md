# ComPair — Shopee Affiliate System

> ระบบ affiliate สมบูรณ์แบบสำหรับ ComPair — ตั้งแต่การ generate short link ไปจนถึง GA4 tracking

---

## Architecture Overview

```
data/affiliate/
├── guide-picks.json          ← ✨ Buying Guide curated picks (แก้ที่นี่ที่เดียว)
├── gpu.json                  ← สินค้า GPU / การ์ดจอ (~900 items)
├── mac.json                  ← Mac accessories (~900 items)
├── mac_accessories.json      ← Mac accessories เพิ่มเติม
├── solar_panel.json          ← แผงโซล่าเซลล์ (~900 items)
├── solar_inverter.json       ← อินเวอร์เตอร์ / MPPT Controller (~900 items)
├── ev_charger.json           ← EV Charger / อุปกรณ์ชาร์จ (~900 items)
├── gold_invest.json          ← ทองคำ / เครื่องประดับ (~900 items)
├── laptop.json               ← Laptop
└── shopee-urls-to-shorten.txt ← Working file สำหรับ generate short links

js/
└── aff-utils.js              ← ✨ Shared JS: affVariant, affCardHTML, affTrackClick

css/
└── shared.css                ← `.aff-strip` CSS (ใช้ร่วมกันทุกหน้า)

scripts/
└── apply_short_links.py      ← อัปเดต JSON จาก short link pairs
```

---

## Placement Map — สินค้าแสดงที่ไหนบ้าง

| หน้า | Strip (หลัง result) | Spec Card CTA | Guide Table |
|---|---|---|---|
| `ai-calculator.html` | ✅ GPU (ตาม RTX series) | ✅ `gscCtaRow` | — |
| `mac-llm-calculator.html` | ✅ Mac accessories (ตาม chip) | ✅ `scCtaRow` | ✅ 7 rows |
| `image-gen-calculator.html` | — | — | ✅ 3 rows (GPU) |
| `solar-calculator.html` | ✅ solar_panel + solar_inverter | — | — |
| `ev-calculator.html` | ✅ ev_charger | — | — |
| `gold-calculator.html` | ✅ gold_invest | — | — |

**Trigger:** Strip แสดงหลังจาก `render()` หรือ `calculate()` ทำงาน (in-sync กับ result เสมอ)

---

## Part 1: แก้ไข Buying Guide Picks

ไฟล์: `data/affiliate/guide-picks.json`

แก้ที่นี่ที่เดียว — ทุกหน้าจะอัปเดตอัตโนมัติ (fetch ทุกครั้งที่โหลดหน้า)

### Schema

```json
{
  "mac-llm": [
    {
      "row": 0,           ← index ตาม <td data-pick="0"> ใน HTML table
      "label": "...",     ← ชื่อรุ่น/งบ (แสดงใน tooltip)
      "name": "...",      ← ชื่อสินค้า (แสดงบนหน้า)
      "hint": "...",      ← คำอธิบายสั้น
      "price": 323,       ← ราคา (บาท) — null = ไม่แสดงราคา
      "link": "https://s.shopee.co.th/XXXXX"
    }
  ],
  "image-gen-gpu": [...]
}
```

### วิธีแก้ไข picks

1. เปิด `data/affiliate/guide-picks.json`
2. แก้ `name`, `hint`, `price`, `link` ตาม row ที่ต้องการ
3. บันทึก — หน้าเว็บจะ fetch ใหม่อัตโนมัติ (no rebuild needed)

---

## Part 2: Generate Shopee Short Links

### Portal
```
URL:        https://affiliate.shopee.co.th/offer/custom_link
Partner ID: 15358640421
```

### Format ของ shopee-urls-to-shorten.txt

```
--- Batch 1/10 ---
https://shopee.co.th/product/AAA/111
https://shopee.co.th/product/BBB/222
https://shopee.co.th/product/CCC/333
https://shopee.co.th/product/DDD/444
https://shopee.co.th/product/EEE/555

https://s.shopee.co.th/SHORT1
https://s.shopee.co.th/SHORT2
https://s.shopee.co.th/SHORT3
https://s.shopee.co.th/SHORT4
https://s.shopee.co.th/SHORT5

--- Batch 2/10 ---
...
```

**กฎ:** short links ต้องอยู่ **ใต้ original URLs** ของ batch เดียวกัน คั่นด้วยบรรทัดว่าง 1 บรรทัด  
Batch ที่ยังไม่ได้ทำ ไม่ต้องใส่ short links — script จะข้ามให้

### ขั้นตอน

1. เปิด `data/affiliate/shopee-urls-to-shorten.txt`
2. Copy original URLs จาก batch ที่ยังไม่มี short link
3. ไปที่ portal → Paste → กด **รับลิงก์** → Copy short links
4. Paste กลับในไฟล์ ใต้ original URLs (คั่นบรรทัดว่าง)
5. รัน script:

```bash
python3 scripts/apply_short_links.py
```

Script จะอัปเดต `affiliate_link` + `shopee_short_link` ใน JSON files  
และแสดง summary: `Updated / Already / Not found`

### JSON Item Schema

```json
{
  "title": "ชื่อสินค้า",
  "sale_price": 1990,
  "price": 2490,
  "discount_percentage": 20,
  "item_rating": 4.8,
  "item_sold": "500",
  "image_link": "https://...",
  "product_link": "https://shopee.co.th/product/...",
  "affiliate_link": "https://s.shopee.co.th/XXXXX",
  "shopee_short_link": "https://s.shopee.co.th/XXXXX"
}
```

- `affiliate_link` — ใช้แสดงบนเว็บ (= short link ถ้ามี, ไม่งั้น = product_link)
- `shopee_short_link` — short link จาก portal (ว่าง = ยังไม่ได้ generate)

---

## Part 3: Shared JS — aff-utils.js

ไฟล์: `js/aff-utils.js` — โหลดในทุกหน้า calculator ด้วย `<script src="../js/aff-utils.js"></script>`

### Functions

| Function | หน้าที่ |
|---|---|
| `affVariant()` | Return `'A'` หรือ `'B'` — 50/50 A/B split, persistent ต่อ browser (localStorage `aff_v`) |
| `affCardHTML(item, page, placement)` | Return HTML string สำหรับ product card 1 ใบ |
| `affTrackClick(el, page, placement)` | Fire GA4 event `affiliate_click` เมื่อคลิก |
| `affTrackImpression(page, placement, count)` | Fire GA4 event `affiliate_impression` เมื่อ strip แสดง |

### A/B Test

- **Variant A** (50%) → แสดง 3 cards (default)
- **Variant B** (50%) → แสดง 1 card เท่านั้น (class `variant-b` ต่อ `.aff-strip`)
- User เห็นแบบเดิมทุกครั้งในเบราว์เซอร์เดิม
- Reset ได้ด้วย: `localStorage.removeItem('aff_v')` ใน DevTools Console

### เพิ่ม Strip ในหน้าใหม่

**1. HTML placeholder:**
```html
<div class="aff-strip" id="xxxAffBox" style="display:none" data-aff-placement="xxx_strip">
  <div class="aff-strip-header">
    <span class="aff-strip-label">ป้ายชื่อ · Shopee</span>
    <a class="aff-strip-more" href="shopee-deals.html?cat=xxx" target="_blank" rel="noopener">
      ดูทั้งหมด
      <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
    </a>
  </div>
  <div class="aff-strip-cards" id="xxxAffCards"></div>
</div>
```

**2. JS render function:**
```javascript
let _xxxAffCache = null;
async function getXxxAffData() {
  if (_xxxAffCache) return _xxxAffCache;
  try {
    const r = await fetch('../data/affiliate/xxx.json');
    const d = await r.json();
    _xxxAffCache = d.items || [];
  } catch(e) { _xxxAffCache = []; }
  return _xxxAffCache;
}

async function renderXxxAffiliate() {
  const box = document.getElementById('xxxAffBox');
  const cardsEl = document.getElementById('xxxAffCards');
  const items = await getXxxAffData();
  if (!items.length) return;

  const sorted = [...items].sort((a,b) =>
    (parseInt(b.item_sold||0) + parseInt(b.discount_percentage||0)*10) -
    (parseInt(a.item_sold||0) + parseInt(a.discount_percentage||0)*10)
  );
  const v = affVariant();
  const picks = sorted.slice(0, v === 'B' ? 1 : 3);
  box.classList.toggle('variant-b', v === 'B');
  cardsEl.innerHTML = picks.map(i => affCardHTML(i, 'xxx_calculator', 'strip')).join('');
  box.style.display = 'none'; void box.offsetWidth; box.style.display = '';
  affTrackImpression('xxx_calculator', 'strip', picks.length);
}
```

**3. เรียกจาก render/calculate:**
```javascript
function render() {
  // ... existing logic ...
  renderXxxAffiliate();
}
```

**4. โหลด script:**
```html
<script src="../js/aff-utils.js"></script>  <!-- ก่อน </body> -->
```

---

## Part 4: GA4 Tracking

### Events ที่ถูก Fire อัตโนมัติ

| Event | เมื่อไหร่ | Parameters |
|---|---|---|
| `affiliate_click` | คลิก card ใดๆ | `page`, `placement`, `variant`, `link`, `title` |
| `affiliate_impression` | strip แสดงผล | `page`, `placement`, `variant`, `count` |

### Placement Values

| ค่า | ใช้ที่ไหน |
|---|---|
| `strip` | Affiliate strip 3 cards หลัง result |
| `spec_card` | CTA button ใน GPU/Mac spec card |
| `guide_table` | ลิงก์ใน Buying Guide Table |

### ดูผลใน GA4

1. ไปที่ [GA4 Dashboard](https://analytics.google.com/) → Property `G-J3C1X16FZ5`
2. **Reports → Engagement → Events**
3. คลิก `affiliate_click` หรือ `affiliate_impression`
4. Filter ด้วย `placement` เพื่อเปรียบเทียบ placement
5. Filter ด้วย `variant` เพื่อดูผล A/B test

### วัดผล A/B Test

```
CTR = affiliate_click / affiliate_impression (per variant)
```

- Variant A (3 cards) vs Variant B (1 card)
- ถ้า B มี CTR สูงกว่า → เปลี่ยน default เป็น B (แก้ `affVariant()` ใน aff-utils.js)

---

## Part 5: CSS — aff-strip

CSS ทั้งหมดอยู่ใน `css/shared.css` block `AFFILIATE STRIP`

| Class | หน้าที่ |
|---|---|
| `.aff-strip` | Container หลัก — border, animation `affSlideIn` |
| `.aff-strip-header` | Row บนสุด — label + "ดูทั้งหมด" link |
| `.aff-strip-label` | ป้ายชื่อ DM Mono uppercase (สี `--primary` ของ theme) |
| `.aff-strip-cards` | Grid 3 columns (1 column บน mobile) |
| `.aff-card` | Card แต่ละอัน — flex row, hover effect |
| `.aff-price` | ราคา Shopee orange `#ee4d2d` |
| `.aff-strip.variant-b .aff-strip-cards` | Override → 1 column สำหรับ Variant B |

---

## Quick Reference

### อัปเดต link ใน Buying Guide Table (เร็วที่สุด)
```
แก้ → data/affiliate/guide-picks.json
ไม่ต้อง rebuild, browser fetch ใหม่อัตโนมัติ
```

### Force reset A/B variant (สำหรับ test)
```javascript
// ใน DevTools Console
localStorage.removeItem('aff_v'); location.reload();
```

### ตรวจสอบ affiliate links ทั้งหมด
```bash
python3 -c "
import json, glob
for f in glob.glob('data/affiliate/*.json'):
    d = json.load(open(f))
    empty = [i['title'][:40] for i in d.get('items',[]) if not i.get('shopee_short_link')]
    if empty: print(f, len(empty), 'items without short link')
"
```

### Partner & Portal
```
Partner ID:  15358640421
Portal URL:  https://affiliate.shopee.co.th/offer/custom_link
Dashboard:   https://affiliate.shopee.co.th/dashboard
GA4 ID:      G-J3C1X16FZ5
```
