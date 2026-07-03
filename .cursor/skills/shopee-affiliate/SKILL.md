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

## การเพิ่มสินค้า

### ขั้นตอนสั้น ๆ

1. เปิด `data/affiliate/manual-picks.json`
2. หา key ที่ต้องการ (เช่น `"ai_calculator"`)
3. เพิ่ม object ใน `"items"` array
4. ตรวจ JSON: `cat data/affiliate/manual-picks.json | python3 -m json.tool`
5. Push

### Item schema

```json
{
  "title":          "ชื่อสินค้า",
  "price":          15990,
  "original_price": 18000,
  "link":           "https://s.shopee.co.th/xxx",
  "image":          "https://...",
  "source":         "Shopee",
  "badge":          "ขายดี"
}
```

| Field | Required | หมายเหตุ |
|-------|----------|---------|
| `title` | ✅ | ≤60 ตัวอักษรสวยที่สุด |
| `price` | ✅ | ตัวเลขล้วน |
| `link` | ✅ | Affiliate URL ของแพลตฟอร์มนั้น ๆ |
| `original_price` | optional | ถ้าใส่ จะแสดง strikethrough |
| `image` | optional | URL รูป (ไม่มีก็ text-only card) |
| `source` | optional | "Shopee" / "Lazada" / อื่น ๆ |
| `badge` | optional | "ขายดี" / "แนะนำ" / "ราคาดี" |

### Guide schema (สำหรับ Buying Guide table)

```json
{
  "row": 0,
  "name": "ชื่อสินค้า",
  "hint": "คำอธิบายสั้น",
  "price": 14990,
  "link": "https://..."
}
```

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
