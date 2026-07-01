# ComPair — Affiliate Placement Strategy

> จุดวางลิงก์ affiliate ที่ดึงดูด click ได้มากที่สุด  
> อัปเดต: 1 กรกฎาคม 2026 (rev 5 — Lazada integration)

---

## หลักการ: Intent ซื้อสูงสุด = หลังผลคำนวณออก

ยิ่ง user ใกล้ "ตัดสินใจ" มากเท่าไหร่ โอกาส click affiliate สูงขึ้นเท่านั้น  
**ลำดับ Intent: หลัง result > ใน spec card > หลัง dropdown > buying guide > หน้า deals แยก**

---

## จุดที่แนะนำ (เรียงตาม Conversion Rate)

### 🥇 1. หลัง Result / ผลคำนวณปรากฏ ← สำคัญที่สุด

ตอนที่ user เห็นผล เช่น:
- "RTX 4090 รัน Llama 3 70B ได้ ✓"
- "Solar คืนทุน 6 ปี ROI 220%"
- "EV ประหยัดกว่า ฿31,000/ปี"

นี่คือ **High Purchase Intent Moment** — user confirmed แล้วว่าต้องการอะไร  
→ แสดง affiliate strip ทันทีใต้ result grid

```
[ผลคำนวณ: ✓ รัน 70B ได้]
─────────────────────────────
สินค้าที่เกี่ยวข้อง · Shopee
[RTX 4090 card] [RTX 4090 card] [RTX 4090 card]
                                  ดูทั้งหมด →
```

**สถานะปัจจุบัน:** ✅ ทำแล้วทุกหน้า — `render()`/`calculate()` ใน `ai-calculator`, `mac-llm-calculator`, `solar-calculator`, `ev-calculator`, `gold-calculator`

---

### 🥈 2. ใน Spec Card / Result Summary Card

แต่ละหน้ามี spec card แสดงข้อมูลหลัก — เพิ่มปุ่ม CTA ติดใน card เลย

| หน้า | Spec Card | ปุ่มที่ควรเพิ่ม | Affiliate Category |
|---|---|---|---|
| `ai-calculator.html` | GPU Spec Card | "ซื้อ [GPU รุ่น] บน Shopee →" | `gpu.json` |
| `mac-llm-calculator.html` | Mac Spec Card | "อุปกรณ์เสริม [chip] →" | `mac.json` + `mac_accessories.json` |
| `solar-calculator.html` | ผลสรุประบบ kW | "ดูแผงโซล่า Shopee →" | `solar_panel.json` + `solar_inverter.json` |
| `ev-calculator.html` | ผลเปรียบเทียบ EV | "ซื้อ EV Charger Shopee →" | `ev_charger.json` |
| `gold-calculator.html` | กราฟผลตอบแทน | "ทองคำลงทุน บน Shopee →" | `gold_invest.json` |

**สถานะปัจจุบัน:** ✅ ทำแล้ว — `gscCtaRow` ใน GPU spec card, `scCtaRow` ใน Mac spec card

---

### 🥉 3. Buying Guide Table — เพิ่ม Column ลิงก์

ทุกหน้ามีตารางแนะนำซื้อตามงบอยู่แล้ว แค่เพิ่ม column affiliate link

```markdown
| งบประมาณ | รุ่นแนะนำ | Shopee |
|---|---|---|
| ฿65,000–85,000 | MacBook Pro M4 Pro 24 GB | [ดูราคา →](affiliate_link) |
| ฿35,000–55,000 | MacBook Air M4 16 GB | [ดูราคา →](affiliate_link) |
```

**สถานะปัจจุบัน:** ✅ ทำแล้ว — `mac-llm-calculator.html` (7 rows × Mac accessories) + `image-gen-calculator.html` (GPU buying guide table ใหม่ 3 rows)  
**ง่ายที่สุดในการ implement** — แค่แก้ HTML table เพิ่ม column

---

### 4. หลัง Dropdown Change (ปัจจุบัน)

affiliate strip แสดงใต้ info box ทันทีที่เลือก GPU หรือ Mac

**สถานะปัจจุบัน:** ✅ มีทุกหน้า — ผ่าน `render()`/`calculate()` ใน 5 calculator ทั้งหมด

---

### 5. หน้า Shopee Deals แยก

หน้า `/html/shopee-deals.html` สำหรับ user ที่มาจาก keyword ซื้อสินค้าโดยตรง

**สถานะปัจจุบัน:** ✅ มีแล้ว — 350+ สินค้า, search, filter, sort  
**Intent:** กลาง (ยังไม่รู้ว่าจะซื้ออะไร)

---

## สรุป Priority Matrix

| จุด | Intent | Conversion | สถานะ | Effort |
|---|---|---|---|---|
| หลัง Result แสดง | ⭐⭐⭐⭐⭐ | สูงสุด | ✅ ครบทุกหน้า (5/5) | — |
| ใน Spec Card | ⭐⭐⭐⭐⭐ | สูงมาก | ✅ GPU + Mac | — |
| Buying Guide Table | ⭐⭐⭐⭐ | สูง | ✅ Mac + Image Gen | — |
| Solar/EV/Gold Strip | ⭐⭐⭐⭐ | สูง | ✅ Phase 2 เสร็จ | — |
| GA4 Click Tracking | ⭐⭐⭐⭐ | วัดผล | ✅ ทุก placement (Phase 3) | — |
| A/B Test (3 cards vs 1) | ⭐⭐⭐ | ทดสอบ | ✅ ทุกหน้า (Phase 3) | — |
| หน้า Shopee Deals | ⭐⭐⭐ | กลาง | ✅ | — |

---

## Roadmap การ Implement

### Phase 1 — ง่าย + Impact สูง ✅ เสร็จทั้งหมด
- [x] เพิ่ม affiliate link column ใน Buying Guide Table ทุกหน้า
- [x] เพิ่ม CTA button ใน Spec Card (`ai-calculator`, `mac-llm-calculator`)
- [x] เพิ่ม affiliate strip หลัง `render()` function (ไม่ใช่แค่ dropdown)

### Phase 2 — ขยาย Coverage ✅ เสร็จทั้งหมด
- [x] เพิ่ม affiliate strip ใน `solar-calculator.html` (แผงโซล่า + อินเวอร์เตอร์) — แสดงหลัง `calculate()`
- [x] เพิ่ม affiliate strip ใน `ev-calculator.html` (EV Charger) — แสดงหลัง `calculate()`
- [x] เพิ่ม affiliate strip ใน `gold-calculator.html` (ทองคำ) — แสดงหลัง `render()`

### Phase 3 — Optimize ✅ เสร็จทั้งหมด
- [x] A/B test: strip 3 cards (Variant A) vs 1 card (Variant B) — persistent via `localStorage`, class `variant-b`
- [x] GA4 event tracking ทุก placement — `affiliate_click` + `affiliate_impression` events  
  → ดูใน GA4: **Events → affiliate_click** (filter by `placement`: `strip`, `spec_card`, `guide_table`)  
  → `affTrackImpression` บันทึก variant + จำนวน card ที่แสดง  
  → ทุกหน้า (ai, mac-llm, image-gen, solar, ev, gold) ผ่าน `js/aff-utils.js` shared script

### Phase 4 — Lazada Integration ✅ เสร็จ 1 กรกฎาคม 2026
- [x] ติดตั้ง Lazada Affiliate API (official Python SDK + `.env`)
- [x] สร้าง `scripts/pull_lazada_products.py` ดึงสินค้า 11 categories → JSON
- [x] อัปเดต `affMerge()` ใน `aff-utils.js` — merge Shopee + Lazada, dedupe, sort by score
- [x] เพิ่ม source badge บน card: `SP` (Shopee) / `Laz` (Lazada)
- [x] Map Lazada JSON เข้า: `ai-calculator`, `mac-llm-calculator`, `solar-calculator`, `ev-calculator`
- [x] GA4 tracking เพิ่ม param `source` (shopee/lazada) + `sources` ใน impression

---

## Affiliate Data Mapping (Shopee + Lazada)

| หน้า Calculator | Shopee JSON | Lazada JSON | merge via |
|---|---|---|---|
| `ai-calculator` | `gpu.json` | `lazada_gpu.json` | `affMerge()` |
| `mac-llm-calculator` | `mac.json` + `mac_accessories.json` | `lazada_laptop.json` | `affMerge()` |
| `solar-calculator` | `solar_panel.json` + `solar_inverter.json` | `lazada_solar_panel.json` | `affMerge()` |
| `ev-calculator` | `ev_charger.json` | `lazada_ev_charger.json` | `affMerge()` |
| `gold-calculator` | `gold_invest.json` | — | — |
| `image-gen-calculator` | `gpu.json` (guide table) | — | — |

**Refresh Lazada data:**
```bash
python3 scripts/pull_lazada_products.py --all --limit 50
```
