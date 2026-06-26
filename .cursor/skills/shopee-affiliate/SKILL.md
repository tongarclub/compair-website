# Shopee Affiliate Short Link Workflow

## Overview
สร้าง short links (`https://s.shopee.co.th/XXXXX`) สำหรับ affiliate products แล้วอัปเดตลงใน JSON files

---

## File Structure

```
data/affiliate/
├── shopee-urls-to-shorten.txt   ← working file (paste short links ที่นี่)
├── gpu.json
├── mac.json
├── mac_accessories.json
├── solar_panel.json
├── solar_inverter.json
├── ev_charger.json
└── gold_invest.json

scripts/
└── apply_short_links.py         ← script อัปเดต JSON จาก txt
```

---

## Format ของ shopee-urls-to-shorten.txt

```
--- Batch 1/10 ---
https://shopee.co.th/product/AAA/111
https://shopee.co.th/product/BBB/222
https://shopee.co.th/product/CCC/333
https://shopee.co.th/product/DDD/444
https://shopee.co.th/product/EEE/555

https://s.shopee.co.th/SHORT1       ← paste short links ใต้ original URLs
https://s.shopee.co.th/SHORT2
https://s.shopee.co.th/SHORT3
https://s.shopee.co.th/SHORT4
https://s.shopee.co.th/SHORT5

--- Batch 2/10 ---
...
```

**กฎ:**
- Short links ต้องอยู่ **ใต้ original URLs** ของ batch เดียวกัน คั่นด้วยบรรทัดว่าง
- ลำดับต้องตรงกัน: URL ที่ 1 → short link ที่ 1
- Batch ที่ยังไม่ได้ทำ ไม่ต้องใส่ short links (script จะข้ามให้)

---

## Step-by-Step Workflow

### ขั้นตอนที่ 1: เปิด txt file
```
data/affiliate/shopee-urls-to-shorten.txt
```

### ขั้นตอนที่ 2: Copy original URLs (5 URLs/batch)
เปิดไฟล์แล้ว copy URLs ใน `--- Batch N ---` ที่ยังไม่ได้ทำ

### ขั้นตอนที่ 3: สร้าง short links บน Shopee Portal
1. ไปที่ https://affiliate.shopee.co.th/offer/custom_link
2. Paste 5 URLs ใน textarea
3. กด **รับลิงก์**
4. Copy short links ที่ได้ทั้ง 5

### ขั้นตอนที่ 4: Paste short links กลับใน txt file
วาง short links ใต้ original URLs ของ batch นั้น (คั่นด้วยบรรทัดว่าง 1 บรรทัด)

### ขั้นตอนที่ 5: รัน script เพื่ออัปเดต JSON
```bash
python3 scripts/apply_short_links.py
```

Script จะ:
- อ่าน txt file หาคู่ (original URL → short link)
- อัปเดต `shopee_short_link` และ `affiliate_link` ใน JSON files
- บันทึกเฉพาะไฟล์ที่มีการเปลี่ยนแปลง
- แสดง summary: Updated / Already / Not found

---

## JSON Item Schema

```json
{
  "title": "ชื่อสินค้า",
  "price": 1990,
  "rating": 4.8,
  "sold": 500,
  "product_link": "https://shopee.co.th/product/...",
  "affiliate_link": "https://s.shopee.co.th/XXXXX",
  "shopee_short_link": "https://s.shopee.co.th/XXXXX"
}
```

- `affiliate_link` — link ที่ใช้แสดงบนเว็บ (ใช้ short link เมื่อมี)
- `shopee_short_link` — short link จาก portal (ถ้าว่าง = ยังไม่ได้ generate)

---

## เมื่อต้องการสร้าง txt file ใหม่ (เช่น เพิ่ม products)

```bash
node -e "
const fs = require('fs');
const categories = [
  { file: 'gpu', label: 'GPU / การ์ดจอ' },
  // ... เพิ่มตามต้องการ
];
// ... (ดู logic ใน gen script เดิม)
"
```

---

## Partner ID
```
15358640421
```

URL Portal: https://affiliate.shopee.co.th/offer/custom_link
