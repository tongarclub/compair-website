# Shopee Affiliate Link Guide
**Partner ID: 15358640421**
Updated: 2026-06-26

---

## URL Format ที่ถูกต้อง

### Short Link (จาก Portal)
```
https://s.shopee.co.th/XXXXX
```
→ redirect ไปยัง full URL พร้อม affiliate parameters ครบ

### Full Affiliate URL
```
https://shopee.co.th/product/{shopid}/{itemid}
  ?mmp_pid=an_15358640421
  &utm_source=an_15358640421
  &utm_medium=affiliates
  &utm_content=----
  &gads_t_sig={encrypted}         ← auto-generated โดย Shopee
  &uls_trackid={unique_per_link}  ← auto-generated โดย Shopee
  &utm_campaign=id_{campaign}     ← auto-generated โดย Shopee
  &utm_term={term}                ← auto-generated โดย Shopee
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

## วิธีสร้าง Affiliate Link

### วิธีที่ 1 — Portal (Manual, Full Tracking)
1. ไปที่ [https://affiliate.shopee.co.th](https://affiliate.shopee.co.th)
2. คลิก **"Create Link"** หรือ **"Link Generator"**
3. วาง product URL → ได้ `https://s.shopee.co.th/XXXXX`
4. ลิงก์มี `utm_campaign`, `uls_trackid`, `utm_term` ครบ

### วิธีที่ 2 — เพิ่ม Partner ID กับ Product URL (Basic, ใช้กับ JSON data)
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

# ตัวอย่าง
url = "https://shopee.co.th/product/153078644/40303177573"
affiliate = make_affiliate_link(url)
# → https://shopee.co.th/product/153078644/40303177573
#   ?mmp_pid=an_15358640421&utm_source=an_15358640421&utm_medium=affiliates&utm_content=----
```
✅ ได้รับ commission attribution  
⚠️ ไม่มี link-level tracking (`utm_campaign`, `uls_trackid`)

### วิธีที่ 3 — Shopee Affiliate API (Batch, Full Tracking)
```
POST https://open.shopee.com/api/v2/affiliate/link
Authorization: Bearer {access_token}
Body: { "origin_url": "https://shopee.co.th/product/..." }
```
→ ได้ `https://s.shopee.co.th/XXXXX` พร้อม full tracking  
⚠️ ต้องมี API credentials จาก Open Platform

---

## ปัญหาของ `affiliate_link` ใน CSV ที่ download มา

```
https://shope.ee/an_redir?origin_link=https%3A%2F%2Fshopee.co.th%2Fproduct%2F...
```

❌ **ไม่มี `mmp_pid`** → ไม่ track กลับมาที่บัญชีของคุณ  
❌ ไม่ควรใช้ตรง ๆ โดยไม่เพิ่ม affiliate parameters

**วิธีแก้:** ใช้ `product_link` จาก JSON แล้วเพิ่ม affiliate parameters แทน (วิธีที่ 2)

---

## ไฟล์ข้อมูลสินค้าที่เตรียมไว้

| ไฟล์ | Domain | สินค้า |
|---|---|---|
| `data/affiliate/gpu.json` | A+F: GPU/Image Gen | การ์ดจอ RTX, thermal accessories |
| `data/affiliate/mac.json` | C: MacBook | เคส MacBook M1–M5, USB-C Hub |
| `data/affiliate/mac_accessories.json` | C: MacBook | Thunderbolt cable, 4K monitor |
| `data/affiliate/solar_panel.json` | B: Solar | อุปกรณ์ติดตั้ง solar, สายไฟ |
| `data/affiliate/solar_inverter.json` | B: Solar | MPPT controller, MC4 connector |
| `data/affiliate/ev_charger.json` | D: EV | BYD accessories, EV charger storage |
| `data/affiliate/gold_invest.json` | E: Gold | แหวนทองคำแท้ 96.5%, ทอง 1 กรัม |

แต่ละ item มี field `product_link` → ใช้กับ `make_affiliate_link()` ได้เลย

---

## ตัวอย่าง Affiliate Link สมบูรณ์

จาก `data/affiliate/mac.json` item แรก (UGREEN USB-C to HDMI):
```
product_link: https://shopee.co.th/product/153078644/40303177573

affiliate_link (วิธีที่ 2):
https://shopee.co.th/product/153078644/40303177573?mmp_pid=an_15358640421&utm_source=an_15358640421&utm_medium=affiliates&utm_content=----
```

---

## Links อ้างอิง

- Shopee Affiliate Portal: [https://affiliate.shopee.co.th](https://affiliate.shopee.co.th)
- Shopee Open Platform: [https://open.shopee.com](https://open.shopee.com)
