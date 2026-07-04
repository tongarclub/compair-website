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

## การเพิ่มสินค้า (2 วิธี)

> **picks.xlsx คือ Source of Truth** — อย่าแก้ JSON โดยตรง

### วิธี A — แก้ Excel โดยตรง

```bash
open data/affiliate/picks.xlsx        # แก้ sheet "Picks"
python3 scripts/import_picks.py       # sync → JSON
python3 scripts/import_picks.py --dry-run          # preview ก่อน
python3 scripts/import_picks.py --section mac_llm  # เฉพาะ section
python3 scripts/create_picks_xlsx.py               # reset template
```

### วิธี B — นำเข้าจาก Shopee "ลิงก์สินค้าหลายรายการ" (ใหม่)

CSV จาก Shopee Affiliate Portal → "สร้างลิงก์หลายรายการ" → Export

```bash
# Step 1: append สินค้าเข้า picks.xlsx
python3 scripts/import_shopee_links.py "csv-affiliate-shoppe/links.csv" \
  --section ai_calculator \
  --ids "5090|5080"     \   # ผูกกับ GPU id (optional)
  --source Shopee        \   # platform label
  --badge ขายดี         \   # badge (optional)
  --dry-run                  # preview ก่อน

# Step 2: sync picks.xlsx → JSON
python3 scripts/import_picks.py --section ai_calculator
```

#### Options ครบของ import_shopee_links.py

| Option | ค่าตัวอย่าง | อธิบาย |
|--------|------------|--------|
| `--section` | `ai_calculator` | **required** section key |
| `--source` | `Shopee` | platform: Shopee / Lazada / Amazon / JD |
| `--badge` | `ขายดี` | ป้าย: ขายดี / แนะนำ / ราคาดี / ใหม่ / HOT |
| `--ids` | `5090\|5080` | GPU/CPU id filter คั่น `\|` |
| `--hint` | `VRAM 32GB` | คำอธิบาย ใส่ทุกแถว |
| `--type` | `item` | item (default) / guide |
| `--limit` | `10` | จำกัดจำนวนแถว |
| `--feed-csv` | `csv-affiliate-shoppe/feed.csv` | ดึงรูปอัตโนมัติจาก Product Feed |
| `--replace` | — | แทนที่แถวเดิมของ section (default: append) |
| `--dry-run` | — | preview ไม่บันทึก |

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

---

## JS API

### loadAffiliate(key, opts)

แสดง affiliate strip จาก `manual-picks.json`

```javascript
// แสดงสินค้าทั้งหมดใน section
loadAffiliate('ai_calculator', {
  stripId: 'gpuAffiliateBox',
  cardsId: 'gpuAffCards',
  labelId: 'gpuAffLabel',
});

// กรองด้วย filterId — ผูกกับ dropdown (ai_calculator, ai_calculator_cpu)
loadAffiliate('ai_calculator', {
  stripId: 'gpuAffiliateBox',
  cardsId: 'gpuAffCards',
  filterId: gpu.id,   // เช่น "5090", "3070"
});
```

**Behavior:**
- `items` ที่มี `ids[]` → แสดงเมื่อ `filterId` อยู่ใน array
- `items` ที่ไม่มี `ids` → แสดงเสมอ (fallback)
- ไม่มี items หลังกรอง → strip ซ่อนตัวเอง

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

## ids Reference (ai_calculator)

GPU ids มาจาก `data/ai-models/gpus.json` field `id`:

```
5090 / 5080 / 5070ti / 5070 / 5060ti / 5060
4090 / 4080s / 4080 / 4070tis / 4070ti / 4070s / 4070
4060ti16 / 4060ti / 4060
3090ti / 3090 / 3080ti / 3080_12 / 3080 / 3070ti / 3070 / 3060ti / 3060 / 3050
```

CPU ids อยู่ใน sheet "Ref" ของ `picks.xlsx` และใน `desgin/affiliate-manual-guide.md`

---

## Portals

```
Shopee Affiliate:  https://affiliate.shopee.co.th/offer/custom_link
Lazada Affiliate:  https://affiliate.lazada.co.th
```

คู่มือฉบับเต็ม → `desgin/affiliate-manual-guide.md`
