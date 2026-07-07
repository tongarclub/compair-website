# add_product_images.py — วิธีการใช้งาน

Script สำหรับเพิ่ม column **`รูปสินค้า`** ลงใน CSV ที่ export มาจาก Shopee Affiliate  
โดยดึง link รูปภาพจากไฟล์ HTML ที่ save มาจากหน้าเว็บ Shopee Affiliate Portal

---

## โครงสร้างไฟล์ที่ต้องมี

```
product-convert/
├── add_product_images.py   ← script หลัก
├── product.html            ← HTML ที่ save จากหน้า Shopee Affiliate (ต้องมีอยู่เสมอ)
└── *.csv                   ← ไฟล์ CSV ที่ export จาก Shopee Affiliate
```

---

## ขั้นตอนการใช้งาน

### ขั้นที่ 1 — Export CSV จาก Shopee Affiliate

1. เข้า [Shopee Affiliate Portal](https://affiliate.shopee.co.th)
2. เลือกสินค้าที่ต้องการ → กด **"สร้างลิงก์หลายรายการ"**
3. กด **Export CSV** แล้วนำไฟล์มาวางไว้ใน folder `product-convert/`

### ขั้นที่ 2 — Save HTML จากหน้า Shopee Affiliate

> ขั้นตอนนี้สำคัญมาก เพราะรูปสินค้าอยู่ใน HTML เท่านั้น ไม่ได้อยู่ใน CSV

1. เปิดหน้าที่แสดงรายการสินค้าบน Shopee Affiliate Portal (หน้าเดียวกับที่เลือกสินค้า)
2. กด **Ctrl+A** (เลือกทั้งหมด) → **Ctrl+C** (copy)
3. เปิดโปรแกรม Text Editor (เช่น VS Code, Notepad)  
   แล้ว paste และ save เป็นชื่อ **`product.html`**  
   วางไว้ใน folder `product-convert/`

   **หรือ** กด `Ctrl+U` ใน Browser เพื่อดู Page Source แล้ว Save As → `product.html`

### ขั้นที่ 3 — รัน Script

เปิด Terminal แล้วรันคำสั่ง:

```bash
cd /path/to/csv-affiliate-shoppe/product-convert
python3 add_product_images.py
```

### ขั้นที่ 4 — ตรวจสอบผลลัพธ์

Script จะแสดงผลดังนี้:

```
Parsing image URLs from: product.html
Found 87 product image(s) in HTML.

Processing CSV: ลิงก์สินค้าหลายลิงก์20260707205443-...csv
Added new column 'รูปสินค้า' to ลิงก์สินค้าหลายลิงก์20260707205443-...csv

Results:
  Total rows   : 85
  Matched      : 85
  Not matched  : 0

Output saved to: ลิงก์สินค้าหลายลิงก์20260707205443-...csv
```

ไฟล์ CSV จะถูก **อัปเดต in-place** โดยเพิ่ม column `รูปสินค้า` ต่อท้าย

---

## ข้อควรระวัง

| สถานการณ์ | ผลลัพธ์ |
|---|---|
| CSV ยังไม่มี column `รูปสินค้า` | เพิ่ม column ให้อัตโนมัติ |
| CSV มี column `รูปสินค้า` อยู่แล้ว | เขียนทับด้วยค่าที่ match ได้ใหม่ |
| สินค้าบางตัว match ไม่ได้ | แสดง Warning พร้อม ID ที่หาไม่พบ ค่าจะเป็นช่องว่าง |
| มี CSV หลายไฟล์ใน folder | จะเลือกไฟล์ที่ **ยังไม่มี** column `รูปสินค้า` ก่อน |

---

## ตัวอย่าง CSV ที่ถูกต้อง

**ก่อนรัน script:**
```
รหัสสินค้า,ชื่อสินค้า,ราคา,ขาย,ชื่อร้านค้า,อัตราค่าคอมมิชชัน,คอมมิชชัน,ลิงก์สินค้า,ลิงก์ข้อเสนอ
48160551599,VGA การ์ดจอ PNY GeForce RTX 5080,...
```

**หลังรัน script:**
```
รหัสสินค้า,ชื่อสินค้า,ราคา,ขาย,ชื่อร้านค้า,อัตราค่าคอมมิชชัน,คอมมิชชัน,ลิงก์สินค้า,ลิงก์ข้อเสนอ,รูปสินค้า
48160551599,VGA การ์ดจอ PNY GeForce RTX 5080,...,https://down-tx-th.img.susercontent.com/th-11134207-81ztk-mo4863r6po1v3b.webp
```

---

## Requirements

- Python 3.6 หรือสูงกว่า (ไม่ต้องติดตั้ง library เพิ่มเติม — ใช้แค่ `csv`, `re`, `os`, `glob`)
