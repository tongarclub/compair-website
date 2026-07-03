# Affiliate Manual Guide
> คู่มือเพิ่มสินค้า Affiliate แบบ Manual

## ภาพรวม

ระบบ Affiliate ของ compair-website ใช้ไฟล์ JSON เดียว **`data/affiliate/manual-picks.json`**
เป็นแหล่งข้อมูลสินค้าทั้งหมด ไม่มีการดึงข้อมูลอัตโนมัติจาก Shopee/Lazada API อีกต่อไป
ทุกสินค้าต้องเพิ่มด้วยตนเอง ทำให้ได้สินค้าที่ตรงและมีคุณภาพจริง

### ไฟล์ที่เกี่ยวข้อง

| ไฟล์ | หน้าที่ |
|------|--------|
| `data/affiliate/manual-picks.json` | ข้อมูลสินค้าทั้งหมด |
| `js/aff-render.js` | Renderer (อย่าแก้ถ้าไม่จำเป็น) |
| `css/shared.css` | Style ของ card และ guide column |

---

## โครงสร้าง manual-picks.json

```json
{
  "ai_calculator":     { "label": "GPU · เปรียบราคา", "items": [ ...สินค้า... ] },
  "ai_calculator_cpu": { "label": "CPU · เปรียบราคา", "items": [ ...สินค้า ที่มี ids[]... ] },
  "mac_llm": {
    "label": "Mac · เปรียบราคา",
    "items": [ ...สินค้า... ],
    "guide": [ ...guide picks... ]
  },
  "solar":     { "label": "...", "items": [] },
  "ev":        { "label": "...", "items": [] },
  "gold":      { "label": "...", "items": [] },
  "image_gen": { "label": "...", "items": [], "guide": [] }
}
```

### Key → หน้า

| key | หน้า | มี guide? | มี filterId? |
|-----|------|----------|-------------|
| `ai_calculator` | AI Calculator (GPU) | ไม่ | ไม่ |
| `ai_calculator_cpu` | AI Calculator (CPU) | ไม่ | ✅ `cpu.id` |
| `mac_llm` | Mac LLM Calculator | ✅ 7 แถว (row 0–6) | ไม่ |
| `solar` | Solar Calculator | ไม่ | ไม่ |
| `ev` | EV Calculator | ไม่ | ไม่ |
| `gold` | Gold Calculator | ไม่ | ไม่ |
| `image_gen` | Image Gen Calculator | ✅ 3 แถว (row 0–2) | ไม่ |

---

## วิธีเพิ่มสินค้า

### 1. หา Affiliate Link

- **Shopee**: เข้า Shopee Affiliate → คัดลอก short link (s.shopee.co.th/...)
- **Lazada**: เข้า Lazada Affiliate → สร้าง link ผ่าน dashboard
- **อื่นๆ**: ใส่ URL ตรงได้เลย

### 2. เพิ่ม item ใน JSON

เปิดไฟล์ `data/affiliate/manual-picks.json` แล้วเพิ่ม object ใน `"items"` ของ key ที่ต้องการ:

```json
{
  "title":          "ASUS DUAL GeForce RTX 5060 8GB GDDR7",
  "price":          15990,
  "original_price": 18000,
  "link":           "https://s.shopee.co.th/xxxxxxxx",
  "image":          "https://down-th.img.susercontent.com/...",
  "source":         "Shopee",
  "badge":          "ขายดี"
}
```

#### Field คำอธิบาย

| Field | Required | คำอธิบาย |
|-------|----------|----------|
| `title` | ✅ | ชื่อสินค้า (ควรกระชับ ≤60 ตัวอักษร) |
| `price` | ✅ | ราคาปัจจุบัน (ตัวเลข ไม่ใส่ ฿) |
| `link` | ✅ | Affiliate URL |
| `original_price` | - | ราคาก่อนลด (แสดง strikethrough) |
| `image` | - | URL รูปสินค้า (ถ้าไม่มี card จะ text-only) |
| `source` | - | "Shopee" / "Lazada" / ชื่อแพลตฟอร์ม |
| `badge` | - | ป้าย: "ขายดี" / "แนะนำ" / "ราคาดี" |

---

## การผูกสินค้ากับ Dropdown ID (`ids` filter)

บางหน้ามี dropdown เลือกรุ่น (เช่น CPU) ที่ต้องการแสดงสินค้าต่างกันตาม ID ที่เลือก
ทำได้โดยเพิ่ม field **`ids`** ใน item เพื่อระบุว่าแสดงกับ dropdown id ไหนบ้าง

### หลักการทำงาน

```
dropdown เลือก "r9_7950x"
   ↓
loadAffiliate('ai_calculator_cpu', { filterId: 'r9_7950x' })
   ↓
กรอง items ที่มี ids: [..., "r9_7950x", ...]
   ↓
render เฉพาะสินค้าที่ตรง
```

- item **มี** `ids` → แสดงเฉพาะเมื่อ `filterId` อยู่ใน array
- item **ไม่มี** `ids` → **แสดงทุกครั้ง** (fallback / สินค้าทั่วไป)

### ตัวอย่าง JSON

```json
"ai_calculator_cpu": {
  "label": "CPU · เปรียบราคา",
  "items": [
    {
      "ids":   ["r9_7950x", "r9_7900x"],
      "title": "AMD Ryzen 9 7950X Box",
      "price": 18990,
      "link":  "https://s.shopee.co.th/...",
      "source": "Shopee",
      "badge": "แนะนำ"
    },
    {
      "ids":   ["r9_7950x", "r9_7900x", "r7_7700x", "r5_7600x"],
      "title": "ASUS PRIME X670-P WiFi Motherboard AM5",
      "price": 8990,
      "link":  "https://s.shopee.co.th/...",
      "source": "Shopee"
    },
    {
      "ids":   ["i9_14900k", "i7_14700k", "i5_14600k"],
      "title": "ASUS PRIME Z790-P WiFi Motherboard LGA1700",
      "price": 7490,
      "link":  "https://s.shopee.co.th/...",
      "source": "Shopee"
    }
  ]
}
```

### ID Reference

ID มาจากไฟล์ `data/ai-models/cpus.json` → field `"id"`:

| id | CPU |
|----|-----|
| `r9_7950x` | AMD Ryzen 9 7950X |
| `r9_7900x` | AMD Ryzen 9 7900X |
| `r7_7700x` | AMD Ryzen 7 7700X |
| `r5_7600x` | AMD Ryzen 5 7600X |
| `r9_5900x` | AMD Ryzen 9 5900X |
| `r7_5800x` | AMD Ryzen 7 5800X |
| `r5_5600x` | AMD Ryzen 5 5600X |
| `i9_14900k` | Intel Core i9-14900K |
| `i7_14700k` | Intel Core i7-14700K |
| `i5_14600k` | Intel Core i5-14600K |
| `i9_13900k` | Intel Core i9-13900K |
| `i7_13700k` | Intel Core i7-13700K |
| `i5_13600k` | Intel Core i5-13600K |
| `i9_12900k` | Intel Core i9-12900K |
| `i7_12700k` | Intel Core i7-12700K |

---

### 3. ตัวอย่างสมบูรณ์

```json
{
  "ai_calculator": {
    "label": "GPU · เปรียบราคา",
    "items": [
      {
        "title": "MSI GeForce RTX 5060 VENTUS 2X 8G",
        "price": 14990,
        "original_price": 16500,
        "link": "https://s.shopee.co.th/abc123",
        "image": "https://down-th.img.susercontent.com/file/xxx.jpg",
        "source": "Shopee",
        "badge": "คุ้มค่า"
      },
      {
        "title": "ASUS DUAL GeForce RTX 5060 Ti 16GB",
        "price": 22990,
        "link": "https://s.shopee.co.th/def456",
        "source": "Shopee"
      }
    ]
  }
}
```

---

## วิธีเพิ่ม Buying Guide Column

สำหรับหน้าที่มี Buying Guide table (`mac_llm` และ `image_gen`) ให้เพิ่มข้อมูลใน `"guide"`:

```json
"guide": [
  {
    "row": 0,
    "name": "ASUS DUAL RTX 5060 8GB",
    "hint": "ราคาประหยัด เหมาะมือใหม่",
    "price": 14990,
    "link": "https://s.shopee.co.th/abc123"
  },
  {
    "row": 1,
    "name": "MSI GeForce RTX 5060 Ti 16GB VENTUS",
    "hint": "VRAM 16 GB ครบ SD/FLUX",
    "price": 19990,
    "link": "https://s.shopee.co.th/def456"
  }
]
```

### Row index ของแต่ละหน้า

**mac_llm** (Mac LLM Calculator — 7 แถว):

| row | Mac รุ่น |
|-----|---------|
| 0 | MacBook Air M4 16 GB |
| 1 | MacBook Air M4 32 GB |
| 2 | MacBook Pro M4 Pro 24 GB |
| 3 | MacBook Pro M4 Pro 48 GB |
| 4 | MacBook Pro M4 Max 36 GB |
| 5 | MacBook Pro M4 Max 128 GB |
| 6 | Mac Studio |

**image_gen** (Image Gen Calculator — 3 แถว):

| row | GPU tier |
|-----|---------|
| 0 | เริ่มต้น (RTX 5060 8 GB) |
| 1 | จริงจัง (RTX 5060 Ti 16 GB) |
| 2 | Pro (RTX 5070 Ti / 5080) |

---

## วิธีหาภาพสินค้า

1. เปิดสินค้าบน Shopee ใน Browser
2. คลิกขวาที่ภาพหลัก → "Copy image address"
3. วางใน field `"image"` ใน JSON
4. (ถ้าภาพโหลดไม่ได้ในอนาคต ลบ field ออก — card จะ fallback เป็น text-only)

---

## ลำดับการแสดงผล

สินค้าแสดงตามลำดับใน JSON array (บนสุด = ซ้ายสุดใน strip)
ใส่สินค้า **คุ้มค่าสุด / แนะนำสุด** ไว้ก่อนเสมอ

---

## การซ่อน/ปิด Strip

ถ้าไม่ต้องการแสดง strip ในหน้าใด ให้เซต `"items": []` — strip จะซ่อนตัวเองอัตโนมัติ

```json
"solar": {
  "label": "Solar · เปรียบราคา",
  "items": []
}
```

---

## ตรวจสอบ JSON ก่อน Push

```bash
cat data/affiliate/manual-picks.json | python3 -m json.tool
```

ถ้า valid จะ print formatted JSON ออกมา ถ้า error จะบอก line ที่ผิด
