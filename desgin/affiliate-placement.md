# ComPair — Affiliate Placement Strategy

> จุดวางลิงก์ affiliate ที่ดึงดูด click ได้มากที่สุด  
> อัปเดต: 27 มิถุนายน 2026 (rev 2)

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

**สถานะปัจจุบัน:** ❌ ยังไม่มีในทุกหน้า (มีแค่หลัง dropdown change)  
**ควรเพิ่มใน:** `onGPUChange()` + `render()`, `onMacChange()` + `render(mac)`, Solar/EV/Gold result

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

**สถานะปัจจุบัน:** ❌ ยังไม่มีในทุกหน้า

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

**สถานะปัจจุบัน:** ✅ มีแล้วใน `ai-calculator.html` และ `mac-llm-calculator.html`  
**ขาดใน:** `solar-calculator.html`, `ev-calculator.html`, `gold-calculator.html`

---

### 5. หน้า Shopee Deals แยก

หน้า `/html/shopee-deals.html` สำหรับ user ที่มาจาก keyword ซื้อสินค้าโดยตรง

**สถานะปัจจุบัน:** ✅ มีแล้ว — 350+ สินค้า, search, filter, sort  
**Intent:** กลาง (ยังไม่รู้ว่าจะซื้ออะไร)

---

## สรุป Priority Matrix

| จุด | Intent | Conversion | สถานะ | Effort |
|---|---|---|---|---|
| หลัง Result แสดง | ⭐⭐⭐⭐⭐ | สูงสุด | ❌ | กลาง |
| ใน Spec Card | ⭐⭐⭐⭐⭐ | สูงมาก | ❌ | ต่ำ |
| Buying Guide Table | ⭐⭐⭐⭐ | สูง | ✅ Mac + Image Gen | — |
| หลัง Dropdown | ⭐⭐⭐⭐ | สูง | ✅ GPU + Mac | — |
| Solar/EV/Gold Dropdown | ⭐⭐⭐⭐ | สูง | ❌ | ต่ำ |
| หน้า Shopee Deals | ⭐⭐⭐ | กลาง | ✅ | — |

---

## Roadmap การ Implement

### Phase 1 — ง่าย + Impact สูง (ทำก่อนเลย)
- [x] เพิ่ม affiliate link column ใน Buying Guide Table ทุกหน้า
- [ ] เพิ่ม CTA button ใน Spec Card (`ai-calculator`, `mac-llm-calculator`)
- [ ] เพิ่ม affiliate strip หลัง `render()` function (ไม่ใช่แค่ dropdown)

### Phase 2 — ขยาย Coverage
- [ ] เพิ่ม affiliate strip ใน `solar-calculator.html` (แผงโซล่า + อินเวอร์เตอร์)
- [ ] เพิ่ม affiliate strip ใน `ev-calculator.html` (EV Charger)
- [ ] เพิ่ม affiliate strip ใน `gold-calculator.html` (ทองคำ)

### Phase 3 — Optimize
- [ ] A/B test: strip 3 cards vs inline button
- [ ] เพิ่ม UTM tracking ต่างกันแต่ละ placement เพื่อวัด click rate

---

## Affiliate Data Mapping

| หน้า Calculator | Affiliate JSON | Keywords จาก JSON |
|---|---|---|
| ai-calculator (GPU) | `gpu.json` | RTX series numbers |
| mac-llm-calculator | `mac.json` + `mac_accessories.json` | M1/M2/M3/M4 |
| solar-calculator | `solar_panel.json` + `solar_inverter.json` | วัตต์, แผง, อินเวอร์เตอร์ |
| ev-calculator | `ev_charger.json` | Type 2, 7kW, 22kW |
| gold-calculator | `gold_invest.json` | ทองคำ, แหวน, ทองแท่ง |
| image-gen-calculator | `gpu.json` | RTX series numbers |
