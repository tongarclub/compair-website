# Affiliate Manual Guide
> คู่มือเพิ่มสินค้า Affiliate — ใช้ Excel เป็น Source of Truth

## สรุปในรอบเดียว

| ไฟล์ | หน้าที่ |
|------|--------|
| `data/affiliate/picks.xlsx` | ✏️ **แก้สินค้าที่นี่** (Excel หลัก) |
| `scripts/import_picks.py` | รัน import Excel → JSON (รองรับ .xlsx และ .csv) |
| `scripts/create_picks_xlsx.py` | สร้าง template ใหม่ (ถ้า Excel เสีย) |
| `data/affiliate/manual-picks.json` | 🔄 generated — อย่าแก้มือ |

### Script Options

```bash
python3 scripts/import_picks.py               # import ทั้งหมด (xlsx > csv)
python3 scripts/import_picks.py --dry-run     # preview ไม่บันทึก
python3 scripts/import_picks.py --section ev  # import เฉพาะ section
python3 scripts/create_picks_xlsx.py          # reset Excel template
```

### Excel มีอะไรบ้าง

- **Sheet "Picks"** — ข้อมูลสินค้าทั้งหมด พร้อม:
  - Dropdown validation: `type`, `source`, `badge`
  - Row ระบายสีแยกตาม section (เขียว=mac, ฟ้า=AI, ชมพู=CPU, …)
  - Frozen header row
- **Sheet "Ref"** — ตาราง reference ครบ: section keys, cpu ids, mac guide rows, image_gen rows

---

## ภาพรวม

```
data/affiliate/picks.xlsx   ← ✏️  แก้ที่นี่ (Excel / Numbers)
         ↓
python3 scripts/import_picks.py
         ↓
data/affiliate/manual-picks.json  ← 🔄 auto-generated จาก Excel
         ↓
หน้าเว็บโหลด JSON → แสดงสินค้า
```

> **ไม่ต้องแก้ manual-picks.json โดยตรง** — แก้ Excel แล้วรัน script เท่านั้น

---

## ไฟล์ที่เกี่ยวข้อง

| ไฟล์ | หน้าที่ |
|------|--------|
| `data/affiliate/picks.xlsx` | ✏️ แก้ไขสินค้าที่นี่ (Excel หลัก) |
| `data/affiliate/manual-picks.json` | 🔄 generated — อย่าแก้มือ |
| `scripts/import_picks.py` | Script import Excel/CSV → JSON |
| `scripts/create_picks_xlsx.py` | สร้าง picks.xlsx ใหม่ (reset template) |
| `js/aff-render.js` | Renderer (อย่าแก้ถ้าไม่จำเป็น) |
| `css/shared.css` | Style ของ card และ guide column |

---

## วิธีใช้ทุกวัน (Quick Start)

```bash
# 1. เปิด Excel แก้ไขสินค้า (sheet "Picks")
open data/affiliate/picks.xlsx

# 2. บันทึกและปิด Excel แล้วรัน import
python3 scripts/import_picks.py

# 3. ตรวจ preview ก่อน (optional)
python3 scripts/import_picks.py --dry-run

# 4. import เฉพาะ section เดียว (optional)
python3 scripts/import_picks.py --section mac_llm

# 5. reset Excel template (ถ้าไฟล์เสีย หรือต้องการเริ่มใหม่)
python3 scripts/create_picks_xlsx.py
```

---

## รูปแบบ Excel (sheet "Picks")

### Columns (row แรก = header — อย่าเปลี่ยนชื่อ)

```
section | type | ids | title | price | original_price | link | image | source | badge | row | hint
```

### Column คำอธิบาย

| Column | Required | หมายเหตุ |
|--------|----------|---------|
| `section` | ✅ | key ใน JSON (ดู Section Reference) |
| `type` | ✅ | `item` หรือ `guide` |
| `ids` | - | id คั่นด้วย `\|` เช่น `r9_7950x\|r9_7900x` (items + filterId เท่านั้น) |
| `title` | ✅ | ชื่อสินค้า (items) / ชื่อสินค้าใน guide column (guides) |
| `price` | ✅ | ราคา (ตัวเลขล้วน ไม่ใส่ ฿) |
| `original_price` | - | ราคาก่อนลด — แสดง strikethrough (items เท่านั้น) |
| `link` | ✅ | Affiliate URL |
| `image` | - | URL รูปสินค้า (items เท่านั้น) |
| `source` | - | ชื่อแพลตฟอร์ม: Shopee / Lazada / ฯลฯ |
| `badge` | - | ป้าย: ขายดี / แนะนำ / ราคาดี (items เท่านั้น) |
| `row` | ✅ guide | row index 0-based (guides เท่านั้น) |
| `hint` | - | คำอธิบายสั้นใต้ชื่อ (guides เท่านั้น) |

### Excel Features

| Feature | รายละเอียด |
|---------|-----------|
| **Dropdown validation** | `type` (item/guide), `source` (Shopee/Lazada/…), `badge` (ขายดี/แนะนำ/…) |
| **Color by section** | แถวสีตาม section อัตโนมัติ (เขียว=mac_llm, ฟ้า=ai_calculator, …) |
| **Sheet "Ref"** | ตาราง reference: section keys, cpu ids, row index ทั้งหมด |
| **Frozen header** | row 1 = header ติดอยู่เสมอขณะ scroll |

### เพิ่มแถวใหม่

เพิ่มแถวต่อท้ายข้อมูลเดิมได้เลย สคริปต์จะ replace ตาม section ที่ระบุ

---

## ตัวอย่าง

```
section          | type  | ids              | title                     | price | original_price | link                           | image | source | badge  | row | hint
ai_calculator    | item  |                  | ASUS DUAL RTX 5060 8GB    | 14990 | 16500          | https://s.shopee.co.th/xxx     |       | Shopee | ขายดี  |     |
ai_calculator_cpu| item  | r9_7950x|r9_7900x| AMD Ryzen 9 7950X         | 18990 |                | https://s.shopee.co.th/xxx     |       | Shopee | แนะนำ  |     |
mac_llm          | guide |                  | เคส MacBook Air M4         | 590   |                | https://s.shopee.co.th/xxx     |       |        |        | 0   | ป้องกันรอย
```

---

## Section Reference

### Section → หน้าเว็บ

| section | หน้า | type ที่รองรับ |
|---------|------|--------------|
| `ai_calculator` | AI Calculator (GPU strip) | `item` |
| `ai_calculator_cpu` | AI Calculator (CPU strip + filterId) | `item` + `ids` |
| `mac_llm` | Mac LLM Calculator | `item`, `guide` (row 0–6) |
| `solar` | Solar Calculator | `item` |
| `ev` | EV Calculator | `item` |
| `gold` | Gold Calculator | `item` |
| `image_gen` | Image Gen Calculator | `item`, `guide` (row 0–2) |

### `ids` Reference — CPU id

ใช้กับ `section=ai_calculator_cpu` เท่านั้น (id มาจาก `data/ai-models/cpus.json`):

| ids value | CPU |
|-----------|-----|
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

### Mac Buying Guide rows (mac_llm.guide)

| row | Mac tier |
|-----|---------|
| 0 | MacBook Air M4 16 GB |
| 1 | MacBook Air M4 32 GB |
| 2 | MacBook Pro M4 Pro 24 GB |
| 3 | MacBook Pro M4 Pro 48 GB |
| 4 | MacBook Pro M4 Max 36 GB |
| 5 | MacBook Pro M4 Max 128 GB |
| 6 | Mac Studio |

### Image Gen GPU Guide rows (image_gen.guide)

| row | GPU tier |
|-----|---------|
| 0 | RTX 5060 8 GB (เริ่มต้น) |
| 1 | RTX 5060 Ti 16 GB (จริงจัง) |
| 2 | RTX 5070 Ti / 5080 (Pro) |

---

## การซ่อน Strip

ถ้าต้องการซ่อน strip ของ section ใด ให้ลบแถวทั้งหมดของ section นั้นออกจาก CSV
แล้วรัน script — items จะเป็น `[]` และ strip จะซ่อนตัวเองอัตโนมัติ

---

## filterId — ผูกสินค้ากับ Dropdown ID

สำหรับ section ที่ต้องแสดงสินค้าต่างกันตาม dropdown ที่เลือก (เช่น CPU):

```csv
# items ที่ไม่มี ids → แสดงทุกครั้ง (fallback)
ai_calculator_cpu,item,,Cooler Master Hyper 212 (Universal),690,,https://...,,,,,

# items ที่มี ids → แสดงเฉพาะเมื่อ dropdown เลือก id นั้น
ai_calculator_cpu,item,r9_7950x|r9_7900x,AMD Ryzen 9 7950X,18990,,https://...,,Shopee,แนะนำ,,
ai_calculator_cpu,item,i9_14900k,Intel i9-14900K,17500,,https://...,,Shopee,,,
```

---

## หา Affiliate Link

| แพลตฟอร์ม | วิธีหา link |
|-----------|------------|
| Shopee | [affiliate.shopee.co.th](https://affiliate.shopee.co.th/offer/custom_link) → ค้นสินค้า → Copy short link |
| Lazada | [affiliate.lazada.co.th](https://affiliate.lazada.co.th) → เปิดสินค้า → Get link |
| อื่นๆ | ใส่ URL ตรงได้เลย |

---

## ตรวจสอบ JSON หลัง Import

```bash
# รัน import + ตรวจ JSON syntax
python3 scripts/import_picks.py
python3 -m json.tool data/affiliate/manual-picks.json > /dev/null && echo "OK"
```

---

## Reset Template Excel

ถ้า picks.xlsx เสียหาย หรือต้องการเริ่มใหม่:

```bash
python3 scripts/create_picks_xlsx.py
```

จะสร้าง picks.xlsx ใหม่พร้อมตัวอย่างข้อมูลทุก section ครับ
