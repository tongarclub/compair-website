# คู่มือระบบ Affiliate — ComPair (Shopee + Lazada)

> คู่มือปฏิบัติการสำหรับจัดการลิงก์ affiliate บนเว็บไซต์ ComPair  
> อัปเดต: 1 กรกฎาคม 2026 — เพิ่ม Lazada integration

---

## สารบัญ

1. [ภาพรวมระบบ](#1-ภาพรวมระบบ)
2. [งานประจำ — เร็วสุด](#2-งานประจำ--เร็วสุด)
3. [Lazada — Refresh ข้อมูลสินค้า](#3-lazada--refresh-ข้อมูลสินค้า)
4. [Shopee — Generate Short Links](#4-shopee--generate-short-links)
5. [อัปเดต Buying Guide Picks](#5-อัปเดต-buying-guide-picks)
6. [ดูผลใน GA4](#6-ดูผลใน-ga4)
7. [ทดสอบ A/B Test](#7-ทดสอบ-ab-test)
8. [เพิ่มหน้า Calculator ใหม่](#8-เพิ่มหน้า-calculator-ใหม่)
9. [ข้อมูลอ้างอิง](#9-ข้อมูลอ้างอิง)

---

## 1. ภาพรวมระบบ

### สินค้าแสดงที่ไหนบ้าง (Shopee + Lazada)

| หน้าเว็บ | Strip (หลัง result) | ปุ่ม Spec Card | Buying Guide | แหล่งข้อมูล |
|---|:---:|:---:|:---:|---|
| ai-calculator | ✅ GPU ตาม RTX series | ✅ | — | Shopee + **Lazada** |
| mac-llm-calculator | ✅ Mac ตาม chip | ✅ | ✅ 7 แถว | Shopee + **Lazada** |
| image-gen-calculator | — | — | ✅ 3 แถว | Shopee |
| solar-calculator | ✅ โซล่า + อินเวอร์เตอร์ | — | — | Shopee + **Lazada** |
| ev-calculator | ✅ EV Charger | — | — | Shopee + **Lazada** |
| gold-calculator | ✅ ทองคำ | — | — | Shopee |

**Source badge บน card:** `SP` (Shopee, สีส้ม) / `Laz` (Lazada, สีน้ำเงิน)
| ev-calculator | ✅ EV Charger | — | — |
| gold-calculator | ✅ ทองคำ | — | — |

### ไฟล์สำคัญ

```
data/affiliate/
├── guide-picks.json       ← แก้ที่นี่ที่เดียวสำหรับ Buying Guide
├── gpu.json               ← สินค้า GPU ~50 รายการ
├── mac.json               ← Mac accessories ~50 รายการ
├── mac_accessories.json   ← Mac accessories เพิ่มเติม
├── solar_panel.json       ← แผงโซล่า ~50 รายการ
├── solar_inverter.json    ← อินเวอร์เตอร์ / MPPT ~50 รายการ
├── ev_charger.json        ← EV Charger ~50 รายการ
├── gold_invest.json       ← ทองคำ ~50 รายการ
├── shopee-urls-to-shorten.txt  ← ไฟล์ทำงาน short links
│
├── lazada_gpu.json        ← Lazada: GPU / Computers
├── lazada_laptop.json     ← Lazada: Laptop
├── lazada_headphone.json  ← Lazada: Audio
├── lazada_smartwatch.json ← Lazada: Smart Devices
├── lazada_air_conditioner.json ← Lazada: Home Appliances
├── lazada_solar_panel.json     ← Lazada: Home Appliances
├── lazada_ev_charger.json      ← Lazada: Home Appliances
└── lazada_*.json          ← Lazada: อื่นๆ

js/
└── aff-utils.js           ← Shared JS: affMerge + A/B + GA4 + source badge

scripts/
├── apply_short_links.py   ← Shopee: จับคู่ URL → short link → JSON
├── pull_lazada_products.py← Lazada: ดึงสินค้าทุก category → JSON
└── test_lazada_api.py     ← Lazada: ทดสอบ API credentials
```

---

## 2. งานประจำ — เร็วสุด

### เปลี่ยน/อัปเดต link ใน Buying Guide Table

```
แก้ไข → data/affiliate/guide-picks.json
```

หน้าเว็บจะ fetch ใหม่อัตโนมัติ ไม่ต้อง rebuild หรือ deploy อะไรเพิ่ม

### Refresh ข้อมูล Lazada (แนะนำ: ทำทุกสัปดาห์)

```bash
python3 scripts/pull_lazada_products.py --all --limit 50
```

### ตรวจสอบสินค้าที่ยังไม่มี short link (Shopee)

```bash
python3 -c "
import json, glob
for f in glob.glob('data/affiliate/*.json'):
    if 'lazada' in f: continue
    d = json.load(open(f))
    empty = sum(1 for i in d.get('items',[]) if not i.get('shopee_short_link'))
    if empty: print(f'{f}: {empty} items ยังไม่มี short link')
"
```

---

## 3. Lazada — Refresh ข้อมูลสินค้า

### ก่อนใช้งานครั้งแรก — ตรวจสอบ credentials

```bash
python3 scripts/test_lazada_api.py
```

ต้องเห็น `✅ ได้ X สินค้า` ใน Test 1 — ถ้าไม่เห็น แสดงว่า `LAZADA_USER_TOKEN` หมดอายุ  
→ Login [affiliate.lazada.co.th](https://affiliate.lazada.co.th) → รับ token ใหม่ → อัปเดต `.env`

### ไฟล์ .env

```
LAZADA_APP_KEY=105827
LAZADA_APP_SECRET=xxxx
LAZADA_USER_TOKEN=xxxx    ← จาก Lazada Affiliate Dashboard → Settings → API Token
```

### รัน Pull

```bash
# ดึงทุก category
python3 scripts/pull_lazada_products.py --all --limit 50

# ดึงเฉพาะ
python3 scripts/pull_lazada_products.py --category gpu
python3 scripts/pull_lazada_products.py --category air_conditioner

# ดู categories ที่รองรับ
python3 scripts/pull_lazada_products.py --list-categories
```

output ไปที่ `data/affiliate/lazada_*.json` — หน้าเว็บ fetch อัตโนมัติ

---

## 4. Shopee — Generate Short Links

**Portal:** https://affiliate.shopee.co.th/offer/custom_link  
**Partner ID:** `15358640421`

### ขั้นตอน

**ขั้นที่ 1 — เปิดไฟล์ URL list**

```
data/affiliate/shopee-urls-to-shorten.txt
```

**ขั้นที่ 2 — หา Batch ที่ยังไม่มี short link**

Batch ที่ *ยังไม่ได้ทำ* จะมีแค่ original URLs ไม่มีบรรทัดว่างและ short links ข้างล่าง:

```
--- Batch 5/70 ---
https://shopee.co.th/product/AAA/111
https://shopee.co.th/product/BBB/222
https://shopee.co.th/product/CCC/333
https://shopee.co.th/product/DDD/444
https://shopee.co.th/product/EEE/555
                              ↑ ไม่มีอะไรข้างล่าง = ยังไม่ได้ทำ
```

**ขั้นที่ 3 — Copy 5 URLs ไปที่ Portal**

1. Copy 5 original URLs ของ batch นั้น
2. ไปที่ https://affiliate.shopee.co.th/offer/custom_link
3. Paste 5 URLs ใน textarea
4. กด **รับลิงก์**
5. Copy short links ที่ได้ทั้ง 5 อัน (`https://s.shopee.co.th/XXXXX`)

**ขั้นที่ 4 — Paste short links กลับในไฟล์**

วางต่อท้าย batch นั้น โดยคั่นด้วยบรรทัดว่าง 1 บรรทัด:

```
--- Batch 5/70 ---
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

--- Batch 6/70 ---
...
```

> ⚠️ **สำคัญ:** ลำดับต้องตรงกัน — URL ที่ 1 ต้องได้ short link ที่ 1

**ขั้นที่ 5 — รัน Script อัปเดต JSON**

```bash
python3 scripts/apply_short_links.py
```

Script จะแสดง:
```
gpu.json       → Updated: 5  Already: 0  Not found: 0
mac.json       → Updated: 0  Already: 5  Not found: 0
```

- **Updated** = อัปเดต short link สำเร็จ
- **Already** = มี short link แล้ว (ข้ามไป)
- **Not found** = URL ไม่ตรงกับ JSON ใดเลย (แจ้งเตือน)

---

## 5. อัปเดต Buying Guide Picks

ไฟล์: `data/affiliate/guide-picks.json`

### โครงสร้าง JSON

```json
{
  "_comment": "Buying Guide affiliate picks — แก้ที่นี่ที่เดียว",
  "_updated": "2026-06-27",

  "mac-llm": [
    {
      "row": 0,
      "label": "MacBook Air M4 16 GB (฿35k–55k)",
      "name": "ชื่อสินค้าที่จะแสดงบนหน้าเว็บ",
      "hint": "คำอธิบายสั้นๆ",
      "price": 323,
      "link": "https://s.shopee.co.th/XXXXX"
    }
  ],

  "image-gen-gpu": [...]
}
```

### ฟิลด์แต่ละอัน

| ฟิลด์ | ความหมาย | หมายเหตุ |
|---|---|---|
| `row` | index แถวใน HTML table | ห้ามเปลี่ยน |
| `label` | ชื่อรุ่น/งบ | แสดงใน tooltip |
| `name` | ชื่อสินค้า | แสดงบนการ์ด |
| `hint` | คำอธิบายสั้น | แสดงใต้ชื่อ |
| `price` | ราคา (บาท) | `null` = ไม่แสดงราคา |
| `link` | Shopee short link | ใช้ `s.shopee.co.th/...` |

### วิธีแก้ไข

1. เปิด `data/affiliate/guide-picks.json`
2. แก้ `name`, `hint`, `price`, `link` ของแถวที่ต้องการ
3. อัปเดต `_updated` เป็นวันที่วันนี้
4. บันทึกไฟล์ — หน้าเว็บจะโหลดข้อมูลใหม่อัตโนมัติ

> ✅ ไม่ต้อง rebuild, deploy, หรือแก้โค้ด HTML

---

## 6. ดูผลใน GA4

**Property ID:** G-J3C1X16FZ5  
**Dashboard:** https://analytics.google.com/

### Events ที่ระบบ Track อัตโนมัติ

| Event | เมื่อไหร่ | ข้อมูลที่ส่ง |
|---|---|---|
| `affiliate_click` | ทุกครั้งที่คลิก affiliate card | page, placement, variant, **source**, link, title |
| `affiliate_impression` | ทุกครั้งที่ strip แสดงผล | page, placement, variant, count, **sources** |

**`source`** = `shopee` หรือ `lazada` — บอกว่าคลิก card จากแพลตฟอร์มไหน  
**`sources`** = `shopee`, `lazada`, หรือ `shopee,lazada` — บอกว่า strip นั้นมีสินค้าจากทั้ง 2 แพลตฟอร์ม

### Placement Values

| ค่า | ตำแหน่ง |
|---|---|
| `strip` | 3 การ์ด affiliate ใต้ผลคำนวณ |
| `spec_card` | ปุ่ม CTA ใน GPU/Mac Spec Card |
| `guide_table` | ลิงก์ในคอลัมน์ Buying Guide Table |

### วิธีดูผล

1. ไป **Reports → Engagement → Events**
2. คลิก `affiliate_click`
3. กด **+ Add filter** → เลือก dimension ที่ต้องการ

**ตัวอย่าง queries ที่มีประโยชน์:**

| ต้องการรู้ | Filter ด้วย |
|---|---|
| placement ไหน click เยอะสุด | `placement` |
| หน้าไหน convert ได้ดีสุด | `page` |
| Shopee vs Lazada click อะไรดีกว่า | `source` |
| สินค้าไหนคลิกเยอะสุด | `title` |
| A/B variant ไหนได้ผลดีกว่า | `variant` |

### สูตร CTR สำหรับ A/B + Source

```
CTR (Shopee) = affiliate_click[source=shopee] ÷ affiliate_impression
CTR (Lazada) = affiliate_click[source=lazada] ÷ affiliate_impression
```

---

## 7. ทดสอบ A/B Test

ระบบแบ่ง user ออกเป็น 2 กลุ่ม 50/50 อัตโนมัติ:

| Variant | พฤติกรรม | CSS Class |
|---|---|---|
| **A** (50%) | แสดง **3 การ์ด** (default) | — |
| **B** (50%) | แสดง **1 การ์ด** เท่านั้น | `.aff-strip.variant-b` |

User จะเห็น variant เดิมทุกครั้งในเบราว์เซอร์นั้น (เก็บใน `localStorage`)

### Force Variant เพื่อ Test เอง

เปิด DevTools (F12) → Console แล้วรัน:

```javascript
// ดู variant ปัจจุบัน
localStorage.getItem('aff_v')

// เปลี่ยนเป็น Variant B
localStorage.setItem('aff_v', 'B'); location.reload();

// เปลี่ยนเป็น Variant A
localStorage.setItem('aff_v', 'A'); location.reload();

// Reset (สุ่มใหม่)
localStorage.removeItem('aff_v'); location.reload();
```

### เมื่อ A/B test มีผลลัพธ์ชัดเจน

ถ้า **Variant B มี CTR สูงกว่าอย่างมีนัยสำคัญ** (เช่น ≥ 2 สัปดาห์, ≥ 100 impressions):

แก้ไข `js/aff-utils.js` บรรทัด:
```javascript
// เปลี่ยน default ให้เป็น Variant B ทุกคน
function affVariant() {
  return 'B'; // ← hard-code ผู้ชนะ
}
```

---

## 8. เพิ่มหน้า Calculator ใหม่

เมื่อมี calculator หน้าใหม่ที่ต้องการ affiliate strip:

### ขั้นที่ 1 — เพิ่ม HTML Placeholder

วางก่อน `</div>` ของ result section:

```html
<div class="aff-strip" id="xxxAffBox" style="display:none" data-aff-placement="xxx_strip">
  <div class="aff-strip-header">
    <span class="aff-strip-label">ชื่อหมวด · Shopee</span>
    <a class="aff-strip-more" href="shopee-deals.html?cat=xxx" target="_blank" rel="noopener">
      ดูทั้งหมด
      <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <path d="M5 12h14M12 5l7 7-7 7"/>
      </svg>
    </a>
  </div>
  <div class="aff-strip-cards" id="xxxAffCards"></div>
</div>
```

### ขั้นที่ 2 — เพิ่ม JS (ก่อน `</script>`)

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
  const box     = document.getElementById('xxxAffBox');
  const cardsEl = document.getElementById('xxxAffCards');
  const items   = await getXxxAffData();
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

### ขั้นที่ 3 — เรียกจาก render()/calculate()

```javascript
function render() {
  // ... โค้ดเดิม ...
  renderXxxAffiliate(); // ← เพิ่มบรรทัดนี้ท้ายสุด
}
```

### ขั้นที่ 4 — โหลด shared script

เพิ่มก่อน `</body>`:

```html
<script src="../js/aff-utils.js"></script>
```

---

## 9. ข้อมูลอ้างอิง

### Links สำคัญ

| ชื่อ | URL |
|---|---|
| Shopee Affiliate Portal | https://affiliate.shopee.co.th |
| Custom Link Generator | https://affiliate.shopee.co.th/offer/custom_link |
| Dashboard รายได้ | https://affiliate.shopee.co.th/dashboard |
| GA4 Dashboard | https://analytics.google.com/ |

### Partner Info

```
Partner ID:  15358640421
GA4 ID:      G-J3C1X16FZ5
```

### Short Link Format

```
https://s.shopee.co.th/XXXXX
```

short link จาก portal จะ redirect ไปยัง full URL พร้อม affiliate parameters ครบ — **ไม่ต้อง** เพิ่ม `?mmp_pid` เอง

### JSON Schema สินค้าใน \*.json

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

| ฟิลด์ | ความหมาย |
|---|---|
| `affiliate_link` | ลิงก์ที่แสดงบนหน้าเว็บ (= short link ถ้ามี, ไม่งั้น = product_link) |
| `shopee_short_link` | short link จาก portal (ว่าง = ยังไม่ได้ generate) |
