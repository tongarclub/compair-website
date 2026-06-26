# Shopee Affiliate Link Guide
**Partner ID: 15358640421**  
Updated: 2026-06-26

---

## URL Format ที่ถูกต้อง

### Short Link (จาก Portal) — แนะนำ
```
https://s.shopee.co.th/XXXXX
```
→ redirect ไปยัง full URL พร้อม affiliate parameters ครบ

### Full Affiliate URL (Method 2)
```
https://shopee.co.th/product/{shopid}/{itemid}
  ?mmp_pid=an_15358640421
  &utm_source=an_15358640421
  &utm_medium=affiliates
  &utm_content=----
```

---

## Parameters อธิบาย

| Parameter | ค่า | คงที่? | หน้าที่ |
|---|---|---|---|
| `mmp_pid` | `an_15358640421` | ✅ คงที่ | ระบุ affiliate account |
| `utm_source` | `an_15358640421` | ✅ คงที่ | แหล่งที่มา (affiliate ID) |
| `utm_medium` | `affiliates` | ✅ คงที่ | ช่องทาง |
| `utm_content` | `----` | ✅ คงที่ | content label |
| `gads_t_sig` | encrypted string | ❌ ต่างกันทุก link | signature ความปลอดภัย |
| `uls_trackid` | เช่น `5604fchn00m1` | ❌ ต่างกันทุก link | click-level tracking |
| `utm_campaign` | เช่น `id_Ag6NkqX3Yx` | ❌ ต่างกันทุก link | campaign per link |
| `utm_term` | เช่น `f4topjuar4wy` | ❌ ต่างกันทุก link | keyword tracking |

---

## วิธีสร้าง Short Link (Manual Workflow — วิธีที่ใช้อยู่)

### ขั้นตอน

**1. เปิดไฟล์ URL list**
```
data/affiliate/shopee-urls-to-shorten.txt
```

**2. Copy 5 URLs ต่อ batch (ตาม `--- Batch N ---`)**

**3. ไปที่ Portal → สร้าง short links**
- URL: https://affiliate.shopee.co.th/offer/custom_link
- Paste 5 URLs ใน textarea → กด **รับลิงก์**
- Copy short links ที่ได้ (5 อัน)

**4. Paste short links กลับใน txt file** ใต้ original URLs ของ batch นั้น
```
--- Batch 1/10 ---
https://shopee.co.th/product/AAA/111
https://shopee.co.th/product/BBB/222
...

https://s.shopee.co.th/SHORT1   ← paste ที่นี่
https://s.shopee.co.th/SHORT2
...
```

**5. รัน script เพื่ออัปเดต JSON**
```bash
python3 scripts/apply_short_links.py
```

Script จะ:
- จับคู่ original URL → short link ตามลำดับ
- อัปเดต `shopee_short_link` และ `affiliate_link` ใน JSON files
- ข้าม item ที่มี short link แล้ว (safe to rerun)

---

## ไฟล์ข้อมูลสินค้าที่เตรียมไว้

| ไฟล์ | Domain | สินค้า | Items |
|---|---|---|---|
| `data/affiliate/gpu.json` | A+F: GPU/Image Gen | การ์ดจอ RTX, thermal accessories | 50 |
| `data/affiliate/mac.json` | C: MacBook | เคส MacBook M1–M5, USB-C Hub | 50 |
| `data/affiliate/mac_accessories.json` | C: MacBook | Thunderbolt cable, 4K monitor | 50 |
| `data/affiliate/solar_panel.json` | B: Solar | อุปกรณ์ติดตั้ง solar, สายไฟ | 50 |
| `data/affiliate/solar_inverter.json` | B: Solar | MPPT controller, MC4 connector | 50 |
| `data/affiliate/ev_charger.json` | D: EV | BYD accessories, EV charger storage | 50 |
| `data/affiliate/gold_invest.json` | E: Gold | แหวนทองคำแท้ 96.5%, ทอง 1 กรัม | 50 |

**รวม: 350 URLs / 70 batches**

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

- `affiliate_link` — link ที่ใช้แสดงบนเว็บ (short link เมื่อมี, Method 2 ถ้ายังไม่มี)
- `shopee_short_link` — short link จาก portal (ว่าง = ยังไม่ได้ generate)

---

## สถานะ Progress

```
Step 1 ✅ Method 2 — เพิ่ม mmp_pid ใน JSON (เสร็จแล้ว)
           affiliate_link = product_link + ?mmp_pid=an_15358640421&...

Step 2 🔄 Manual Short Links — copy-paste ผ่าน Portal
           URL List: data/affiliate/shopee-urls-to-shorten.txt  (70 batches)
           Script:   python3 scripts/apply_short_links.py
           Progress: batch 1/70 เสร็จแล้ว (5 items จาก gpu.json)

Step 3 🔜 Add Shopee section ในหน้า calculator
           → แสดง product card grid โหลดจาก data/affiliate/*.json
```

---

## Method 2 — Python Helper (Basic Tracking)

```python
PARTNER_ID = "15358640421"

def make_affiliate_link(product_url: str) -> str:
    return (
        f"{product_url}"
        f"?mmp_pid=an_{PARTNER_ID}"
        f"&utm_source=an_{PARTNER_ID}"
        f"&utm_medium=affiliates"
        f"&utm_content=----"
    )
```

✅ ได้รับ commission attribution  
⚠️ ไม่มี link-level tracking (`utm_campaign`, `uls_trackid`)

---

## ปัญหาของ `affiliate_link` ใน CSV ที่ download มา

```
https://shope.ee/an_redir?origin_link=https%3A%2F%2Fshopee.co.th%2Fproduct%2F...
```

❌ **ไม่มี `mmp_pid`** → ไม่ track กลับมาที่บัญชีของคุณ  
**วิธีแก้:** ใช้ `product_link` จาก JSON แล้วเพิ่ม affiliate parameters แทน

---

## Links อ้างอิง

- Shopee Affiliate Portal: https://affiliate.shopee.co.th
- Custom Link Generator: https://affiliate.shopee.co.th/offer/custom_link
- Shopee Open Platform: https://open.shopee.com
