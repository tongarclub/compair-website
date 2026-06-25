# ComPair — สิ่งที่ช่วยทำให้เว็บดึงดูดได้อีก
> อัปเดต: มิ.ย. 2026

---

## 🎯 Level 1 — Quick Wins (Effort ต่ำ, Impact สูง)

### 1. Share Result Feature
หลังจากกด "คำนวณ" แล้ว มี URL ที่ share ได้ทันที:
```
/ev-calculator.html?ev=byd-seal&gas=honda-crv&km=20000&rate=2.6
```
- ผลคำนวณ restore จาก query string อัตโนมัติ
- ผู้ใช้แชร์ให้เพื่อนได้เลยไม่ต้องกรอกใหม่
- **ทำไมสำคัญ**: Organic spread ทาง LINE / Facebook = backlink ฟรี + returning traffic

### 2. Print / Export ผลเป็น PNG / PDF
ปุ่ม "บันทึกผลการคำนวณ" → capture ด้วย `html2canvas` หรือ `window.print()` พร้อม print CSS

### 3. "อัปเดตล่าสุด" Badge บน Homepage
Badge เล็กๆ เช่น "RTX 5000 ใหม่" หรือ "อัปเดต มิ.ย. 2026"
→ สร้างความรู้สึกว่าข้อมูลสดและเว็บยัง active

### 4. ปุ่ม Reset / Compare Another
บน calculator pages เพิ่มปุ่ม "ล้างข้อมูล" หรือ "เปรียบเทียบรุ่นอื่น"
→ ลด friction ให้คนอยู่ในเว็บนานขึ้น

---

## 🚀 Level 2 — Medium Impact Features

### 5. Multi-item Comparison Mode
เปรียบเทียบ **3 รุ่นพร้อมกัน** แทน 1 vs 1:
- GPU: RTX 5090 vs RTX 4090 vs RTX 3090 เทียบ token speed เต็มตาราง
- EV: BYD Seal vs Tesla Model 3 vs Honda HR-V side-by-side

นี่คือ feature ที่ผู้ใช้มักต้องการมากที่สุดบน comparison sites

### 6. ทองคำ vs กองทุน ROI Calculator
จาก roadmap — **effort ต่ำที่สุด** ใน non-AI options เพราะ data static ไม่ต้อง maintain บ่อย

**Keywords เป้าหมาย:**
- "ซื้อทอง 1 บาทวันนี้ กี่ปีคืนทุน"
- "ทองคำ 10 ปี ผลตอบแทนเท่าไหร่"
- "กองทุนทองคำ vs ทองแท่ง vs หุ้น"

### 7. AI Image Gen Calculator
จาก roadmap — FLUX, Stable Diffusion, Midjourney API

**Keywords เป้าหมาย:**
- "FLUX รันบน RTX 4060 ได้ไหม"
- "VRAM สำหรับ Stable Diffusion"
- "Midjourney vs Self-hosted ราคา"

SEO impact ⭐⭐⭐⭐⭐ — กระแส AI image ยังร้อนแรงในไทย

### 8. "Popular Searches" Section บน Homepage
Trending keywords static หรือ dynamic เช่น:
> 🔥 BYD Seal ค่าชาร์จ · RTX 5090 LLM · Llama 3 70B ต้องการ VRAM เท่าไหร่

---

## 💡 Level 3 — Differentiation Features (เว็บอื่นไม่มี)

### 9. "แพ็กเกจสมบูรณ์" Cross-calculator Flow
Journey แบบ connected ข้ามหน้า:
```
Solar ROI → ชาร์จ EV → ประหยัดรวม Solar + EV ต่อปี
GPU VRAM → AI Image Gen → ราคา Midjourney vs Self-hosted
```
ทำ flow เชื่อมหน้าเข้าหากัน คำนวณทีเดียวได้ผลหลายมิติ

### 10. Embeddable Widget
ให้เว็บอื่น embed calculator ผ่าน `<iframe>` หรือ script
→ เพิ่ม backlink quality สูงมาก

### 11. Dark Mode
Toggle dark/light — เหมาะมากกับ target audience (tech users ชอบ dark mode)
GPU/AI audience โดยเฉพาะ

### 12. LINE OA / Notification
ผู้ใช้ลงทะเบียน → รับ alert เมื่อราคา GPU เปลี่ยน หรือ RTX 5060 วางขาย
→ สร้าง returning users และ engaged community

---

## 📊 Priority Matrix

| Feature | Effort | Impact | ทำเมื่อไหร่ |
|---|---|---|---|
| Share URL result | ต่ำ | ⭐⭐⭐⭐⭐ | ทำก่อนเลย |
| ทองคำ vs กองทุน Calculator | ต่ำ | ⭐⭐⭐⭐ | ทำก่อนเลย |
| "อัปเดตล่าสุด" Badge | ต่ำมาก | ⭐⭐⭐ | ทำก่อนเลย |
| AI Image Gen Calculator | กลาง | ⭐⭐⭐⭐⭐ | Q3 2026 |
| Multi-compare Mode | กลาง–สูง | ⭐⭐⭐⭐⭐ | Q3 2026 |
| Condo ROI Calculator | กลาง | ⭐⭐⭐⭐ | Q3 2026 |
| Print / Export | ต่ำ | ⭐⭐⭐ | Q3 2026 |
| Dark Mode | กลาง | ⭐⭐⭐ | Q4 2026 |
| Cross-calculator Flow | สูง | ⭐⭐⭐⭐⭐ | Q4 2026 |
| Embeddable Widget | สูง | ⭐⭐⭐⭐ | Q4 2026 |
| LINE OA / Notification | สูง | ⭐⭐⭐ | Q4 2026 |

---

## ข้อเสนอแนะ ถ้าจะทำตอนนี้

**ลำดับที่แนะนำ:**
1. **Share URL** — ต่ำ effort, สูง impact สุด สร้าง virality ได้ทันที
2. **ทองคำ vs กองทุน** — data static, SEO keyword ดี, ขยาย audience ออกนอก tech
3. **AI Image Gen Calculator** — ต่อยอดจาก GPU pages ที่มีอยู่แล้ว, SEO สูงมาก
