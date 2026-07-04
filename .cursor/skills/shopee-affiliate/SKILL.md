# ComPair — Manual Affiliate System

> ระบบ Affiliate แบบ Manual สำหรับ ComPair — เพิ่มสินค้าเองทั้งหมดจาก `manual-picks.json`
>
> ไม่มี Shopee API / Lazada API — ควบคุมคุณภาพสินค้าได้ 100%

---

## Architecture

```
data/affiliate/
└── manual-picks.json    ← ✨ แก้ที่นี่ที่เดียว — ข้อมูลสินค้าทั้งหมด

js/
└── aff-render.js        ← loadAffiliate() + loadAffiliateGuide()

css/
└── shared.css           ← .aff-strip, .aff-card, .gt-buy-*, .gpu-buy-* styles

desgin/
└── affiliate-manual-guide.md  ← คู่มือฉบับเต็ม
```

---

## Placement Map

| หน้า | key ใน JSON | มี guide? | strip id | cards id |
|------|------------|----------|---------|---------|
| `ai-calculator.html` | `ai_calculator` | — | `gpuAffiliateBox` | `gpuAffCards` |
| `mac-llm-calculator.html` | `mac_llm` | ✅ `.gt-buy-cell[data-pick]` | `macAffiliateBox` | `macAffCards` |
| `solar-calculator.html` | `solar` | — | `solarAffBox` | `solarAffCards` |
| `ev-calculator.html` | `ev` | — | `evAffBox` | `evAffCards` |
| `gold-calculator.html` | `gold` | — | `goldAffBox` | `goldAffCards` |
| `image-gen-calculator.html` | `image_gen` | ✅ `.gpu-buy-cell[data-gpu-pick]` | — | — |

---

## การเพิ่มสินค้า (Excel Workflow)

> **picks.xlsx คือ Source of Truth** — แก้ Excel แล้วรัน script เท่านั้น อย่าแก้ JSON โดยตรง

### ขั้นตอน

```bash
# 1. เปิด Excel แก้ไข (sheet "Picks")
open data/affiliate/picks.xlsx

# 2. preview ก่อน (optional)
python3 scripts/import_picks.py --dry-run

# 3. import จริง
python3 scripts/import_picks.py

# 4. import เฉพาะ section เดียว
python3 scripts/import_picks.py --section mac_llm

# 5. reset template ถ้า Excel เสีย
python3 scripts/create_picks_xlsx.py
```

### Excel Columns (sheet "Picks")

| Column | Required | หมายเหตุ |
|--------|----------|---------|
| `section` | ✅ | key ใน JSON เช่น `ai_calculator` |
| `type` | ✅ | `item` หรือ `guide` (dropdown) |
| `ids` | - | id คั่นด้วย `\|` เช่น `r9_7950x\|r9_7900x` (filterId) |
| `title` | ✅ | ชื่อสินค้า (items) / ชื่อใน guide (guides) |
| `price` | ✅ | ตัวเลขล้วน |
| `original_price` | - | ราคาก่อนลด (items) |
| `link` | ✅ | Affiliate URL |
| `image` | - | URL รูปสินค้า (items) |
| `source` | - | Shopee / Lazada / ฯลฯ (dropdown) |
| `badge` | - | ขายดี / แนะนำ / ราคาดี (dropdown) |
| `row` | ✅ guide | row index 0-based (guides) |
| `hint` | - | คำอธิบายสั้น (guides) |

Sheet **"Ref"** ใน Excel มี reference ครบ: section keys, cpu ids, row index ทุกหน้า

> คู่มือเต็ม → `desgin/affiliate-manual-guide.md`

---

## JS API

### loadAffiliate(key, opts)

แสดง affiliate strip จาก `manual-picks.json`

```javascript
loadAffiliate('ai_calculator', {
  stripId: 'gpuAffiliateBox',  // id ของ .aff-strip container
  cardsId: 'gpuAffCards',      // id ของ .aff-strip-cards
  labelId: 'gpuAffLabel',      // id ของ label element (optional)
});
```

**Behavior:** ถ้า `items` ว่าง → strip ซ่อนตัวเอง (ไม่แสดงกล่องว่าง)

### loadAffiliateGuide(key, selector)

เติม Buying Guide column จาก `manual-picks.json`

```javascript
loadAffiliateGuide('mac_llm', '.gt-buy-cell[data-pick]');
loadAffiliateGuide('image_gen', '.gpu-buy-cell[data-gpu-pick]');
```

---

## เพิ่ม Strip ในหน้าใหม่

### HTML

```html
<!-- เพิ่มสินค้าได้ใน data/affiliate/manual-picks.json → "my_page" -->
<div class="aff-strip" id="myAffBox" style="display:none">
  <div class="aff-strip-header">
    <span class="aff-strip-label" id="myAffLabel">สินค้าแนะนำ</span>
  </div>
  <div class="aff-strip-cards" id="myAffCards"></div>
</div>
```

### JS (ก่อน `</body>`)

```html
<script src="../js/aff-render.js"></script>
<script>
  loadAffiliate('my_page', {
    stripId: 'myAffBox',
    cardsId: 'myAffCards',
    labelId: 'myAffLabel',
  });
</script>
```

### JSON

เพิ่ม key ใน `data/affiliate/manual-picks.json`:

```json
"my_page": {
  "label": "สินค้าแนะนำ",
  "items": []
}
```

---

## Portals

```
Shopee Affiliate:  https://affiliate.shopee.co.th/offer/custom_link
Lazada Affiliate:  https://affiliate.lazada.co.th
```

คู่มือฉบับเต็ม → `desgin/affiliate-manual-guide.md`
