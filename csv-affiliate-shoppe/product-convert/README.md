# add_product_images.py — วิธีการใช้งาน

Script สำหรับเพิ่ม column **`รูปสินค้า`** ลงใน CSV ที่ export มาจาก Shopee Affiliate  
โดยดึง link รูปภาพจากไฟล์ `.txt` ที่ copy มาจากหน้าเว็บ Shopee Affiliate Portal

---

## โครงสร้างไฟล์

```
product-convert/
├── add_product_images.py   ← script หลัก
├── txt/                    ← วาง .txt files ที่ copy มาจากหน้า Shopee Affiliate
│   ├── product_offer_list.txt
│   ├── product_offer_list (1).txt
│   └── product_offer_list (2).txt
└── csv/                    ← วาง .csv files ที่ export จาก Shopee Affiliate
    ├── 5080.csv
    └── 5090.csv
```

> Script จะอ่าน **ทุก `.txt`** ใน `txt/` และประมวลผล **ทุก `.csv`** ใน `csv/` ในคราวเดียว

---

## ขั้นตอนการใช้งาน

### ขั้นที่ 1 — Export CSV จาก Shopee Affiliate

1. เข้า [Shopee Affiliate Portal](https://affiliate.shopee.co.th)
2. เลือกสินค้าที่ต้องการ → กด **"สร้างลิงก์หลายรายการ"**
3. กด **Export CSV** แล้วนำไฟล์มาวางไว้ใน folder `product-convert/csv/`

### ขั้นที่ 2 — Save HTML จากหน้า Shopee Affiliate เป็น .txt

> ขั้นตอนนี้สำคัญ เพราะรูปสินค้าอยู่ใน HTML เท่านั้น ไม่ได้อยู่ใน CSV

1. เปิดหน้าที่แสดงรายการสินค้าบน Shopee Affiliate Portal (หน้าเดียวกับที่เลือกสินค้า)
2. กด **Ctrl+A** (เลือกทั้งหมด) → **Ctrl+C** (copy)
3. เปิด Text Editor (เช่น VS Code) แล้ว paste แล้ว save เป็นไฟล์ `.txt`  
   วางไว้ใน folder `product-convert/txt/`

   **หรือ** กด `Ctrl+U` ใน Browser เพื่อดู Page Source แล้ว Save As → ตั้งชื่อ `.txt`

> ถ้ามีสินค้าหลายหน้า ให้ save ทีละหน้าเป็นหลายไฟล์ เช่น `page1.txt`, `page2.txt`  
> Script จะ merge image URL จากทุกไฟล์รวมกัน

### ขั้นที่ 3 — รัน Script

```bash
cd /path/to/csv-affiliate-shoppe/product-convert
python3 add_product_images.py
```

### ขั้นที่ 4 — ตรวจสอบผลลัพธ์

```
📂 อ่าน .txt จาก: .../txt
  [product_offer_list.txt]    → 20 images (20 new)
  [product_offer_list (1).txt] → 20 images (20 new)
  [product_offer_list (2).txt] → 4 images (4 new)
✅ รวม 44 image URLs จากทุกไฟล์

📂 พบ 1 CSV file(s) ใน: .../csv

🔄 5070ti.csv
  Added column 'รูปสินค้า'
  Total: 44  Matched: 44  Not matched: 0

✅ เสร็จสิ้น — อัปเดต 1 ไฟล์แล้ว
```

ไฟล์ CSV ใน `csv/` จะถูก **อัปเดต in-place** โดยเพิ่ม column `รูปสินค้า` ต่อท้าย

---

## ข้อควรระวัง

| สถานการณ์ | ผลลัพธ์ |
|---|---|
| CSV ยังไม่มี column `รูปสินค้า` | เพิ่ม column ให้อัตโนมัติ |
| CSV มี column `รูปสินค้า` อยู่แล้ว | เขียนทับด้วยค่าที่ match ได้ใหม่ |
| สินค้าบางตัว match ไม่ได้ | แสดง Warning พร้อม ID ที่หาไม่พบ ค่าจะเป็นช่องว่าง |
| มี .txt หลายไฟล์ | merge image URL ทั้งหมดก่อน แล้วค่อย match กับ CSV |
| มี CSV หลายไฟล์ใน csv/ | ประมวลผลทุกไฟล์ในคราวเดียว |

---

## Requirements

- Python 3.6 หรือสูงกว่า (ไม่ต้องติดตั้ง library เพิ่มเติม — ใช้แค่ `csv`, `re`, `os`, `glob`)
