# Next Features Roadmap — ComPair

> อัปเดต: มิถุนายน 2026

---

## สถานะปัจจุบัน

| หน้า | สถานะ |
|---|---|
| AI Hardware VRAM Calculator | ✅ Live |
| Solar ROI Calculator | ✅ Live |
| Mac / Apple Silicon LLM | ✅ Live |
| GPU Pages (Level 1 SEO) — 10 รุ่น | ✅ Live |
| Model Pages (Level 2 SEO) — 5 model | ✅ Live |
| Sitemap — 19 URLs | ✅ Live |
| Google Analytics (G-J3C1X16FZ5) | ✅ Live |

---

## ตัวเลือกฟีเจอร์ถัดไป

### 🔥 Option A: RTX 5000 Series Pages
**Blackwell: RTX 5090, 5080, 5070, 5060 Ti, 5060**

**Keywords ที่จับได้:**
- "RTX 5090 รัน LLM ได้ไหม"
- "5090 vs 4090 AI performance"
- "RTX 5070 VRAM เท่าไหร่"
- "Blackwell สำหรับ local AI"

**Effort:** ต่ำมาก — ใช้ `scripts/gen_gpu_pages.py` เดิม แค่เพิ่ม data ใน `data/ai-models/gpus.json`

**ทำไมทำก่อน:**
- RTX 5000 ออกตั้งแต่ต้นปี 2026 — คนค้นหาเยอะแต่ content ภาษาไทยยังน้อย
- Competition ต่ำ — first-mover advantage
- ROI สูงสุดเมื่อเทียบกับ effort

**ขั้นตอน:**
1. เพิ่ม RTX 5090/5080/5070/5060Ti/5060 ใน `data/ai-models/gpus.json`
2. รัน `python3 scripts/gen_gpu_pages.py`
3. อัปเดต `sitemap.xml`
4. เพิ่ม card ใน GPU section ของ `ai-calculator.html`

---

### 🔥 Option B: AI Image Generation Calculator
**"การ์ดจอรุ่นไหนรัน Stable Diffusion / FLUX ได้?"**

**Keywords ที่จับได้:**
- "Stable Diffusion VRAM เท่าไหร่"
- "FLUX 1 Dev GPU ที่ต้องการ"
- "RTX 4060 รัน SD ได้ไหม"
- "AI art GPU แนะนำ"
- "ComfyUI ต้องการ VRAM เท่าไหร่"

**Effort:** กลาง — ต้องสร้าง data set ใหม่สำหรับ image models

**ต่างจาก LLM Calculator:**
- VRAM requirements ต่างกัน (SD 1.5 ใช้ 4 GB, FLUX Dev ใช้ 12–24 GB)
- Resolution มีผลต่อ VRAM (512px vs 1024px vs 2048px)
- Tools ต่างกัน: ComfyUI, A1111, Forge, InvokeAI

**Data ที่ต้องสร้าง:**
```
- SD 1.5 / SD 2.1
- SDXL
- FLUX.1 Schnell (8 step)
- FLUX.1 Dev
- Stable Diffusion 3.5
```

---

### ⚡ Option C: Cloud vs Local AI Cost Calculator
**"รัน LLM ใน Cloud คุ้มไหม vs ซื้อ GPU เอง?"**

**Keywords ที่จับได้:**
- "RunPod ราคา GPU"
- "cloud GPU ถูกที่สุด 2026"
- "ซื้อ RTX 4090 vs cloud คุ้มกว่ากัน"
- "ค่าไฟ GPU server ต่อเดือน"

**สูตรคำนวณ:**
```
Break-even = ราคา GPU / (ค่า cloud/ชั่วโมง - ค่าไฟ/ชั่วโมง)
```

**Effort:** สูง — ต้องดึงราคา cloud providers และ maintain ให้ up-to-date

**Providers ที่น่าเปรียบเทียบ:**
- RunPod
- Vast.ai
- AWS (p3/p4/p5 instances)
- Google Cloud (A100/T4)
- Lambda Labs

---

### 🌱 Option D: AI PC / NPU Calculator
**"Intel Core Ultra / AMD Ryzen AI รัน LLM ได้ไหม?"**

**Keywords ที่จับได้:**
- "Core Ultra NPU LLM performance"
- "AI PC ซื้อคุ้มไหม"
- "NPU vs GPU สำหรับ AI"
- "Copilot+ PC local LLM"
- "Snapdragon X Elite LLM"

**Chips ที่น่าครอบคลุม:**
- Intel Core Ultra 200H/200U (NPU 48 TOPS)
- AMD Ryzen AI 300 (NPU 50 TOPS)
- Qualcomm Snapdragon X Elite (NPU 45 TOPS)

**ต่อยอดจาก:** Mac calculator ที่มีอยู่แล้ว

**Effort:** กลาง — ต้องรวบรวมข้อมูล benchmark NPU + LLM performance

---

## สรุปการจัดลำดับ

| ลำดับ | Option | Effort | SEO Impact | Timing |
|---|---|---|---|---|
| **1** | RTX 5000 Series Pages | ต่ำมาก | ⭐⭐⭐⭐⭐ | ทำเดี๋ยวนี้เลย |
| **2** | AI Image Gen Calculator | กลาง | ⭐⭐⭐⭐⭐ | ก่อน Q3 2026 |
| **3** | Cloud vs Local Calculator | สูง | ⭐⭐⭐⭐ | Q3 2026 |
| **4** | AI PC / NPU Calculator | กลาง | ⭐⭐⭐ | Q4 2026 |

---

## หมายเหตุเพิ่มเติม

- **RTX 5000 data specs** (ประมาณการ มิ.ย. 2026):
  - RTX 5090: 32 GB GDDR7, ~1.8 TB/s bandwidth
  - RTX 5080: 16 GB GDDR7, ~960 GB/s
  - RTX 5070 Ti: 16 GB GDDR7, ~896 GB/s
  - RTX 5070: 12 GB GDDR7, ~672 GB/s
  - RTX 5060 Ti: 16 GB GDDR7, ~448 GB/s

- **FLUX image gen VRAM guide** (reference):
  - FLUX.1 Schnell Q4: ~6 GB
  - FLUX.1 Dev FP8: ~12 GB
  - FLUX.1 Dev BF16: ~24 GB
  - SDXL: ~6 GB (1024px)
  - SD 1.5: ~4 GB (512px)
