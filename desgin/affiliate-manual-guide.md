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
  "ai_calculator": {
    "label": "GPU · เปรียบราคา",
    "items": [ ...สินค้า... ]
  },
  "mac_llm": {
    "label": "Mac · เปรียบราคา",
    "items": [ ...สินค้า... ],
    "guide": [ ...guide picks... ]
  },
  "solar":      { "label": "...", "items": [] },
  "ev":         { "label": "...", "items": [] },
  "gold":       { "label": "...", "items": [] },
  "image_gen":  { "label": "...", "items": [], "guide": [] }
}
```

### Key → หน้า

| key | หน้า | มี guide? |
|-----|------|----------|
| `ai_calculator` | AI Calculator (GPU) | ไม่ |
| `mac_llm` | Mac LLM Calculator | ✅ 7 แถว (row 0–6) |
| `solar` | Solar Calculator | ไม่ |
| `ev` | EV Calculator | ไม่ |
| `gold` | Gold Calculator | ไม่ |
| `image_gen` | Image Gen Calculator | ✅ 3 แถว (row 0–2) |

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
