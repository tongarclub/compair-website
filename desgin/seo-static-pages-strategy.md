# SEO Strategy — Static Pages สำหรับ ComPair

> แนวทางเพิ่มโอกาสในการค้นหาผ่านการสร้างหน้า HTML แบบ Static  
> อัปเดต: มิถุนายน 2026

---

## ข้อสรุปสำคัญ: Query String ≠ SEO

| วิธี | ผล SEO | เหตุผล |
|---|---|---|
| `?gpu=rtx4060&model=7b` | ❌ ไม่ช่วย | Google มองเป็นหน้าเดิม ไม่ index แยก |
| `#gpu=rtx4060` hash | ❌ ไม่ช่วย | Google มองไม่เห็น hash fragment เลย |
| `/html/gpu/rtx-4060.html` | ✅ ดีมาก | URL ใหม่ = index entry ใหม่ = keyword ใหม่ |

---

## แนวทางที่แนะนำ: 3 ระดับ

### ระดับ 1: หน้าแยกต่อ GPU (Priority: Must)

สร้างหน้า HTML 1 ไฟล์ต่อ GPU แต่ละรุ่น โดยมี content เฉพาะ GPU นั้น

**URL Pattern:**
```
/html/gpu/rtx-4090.html
/html/gpu/rtx-4080-super.html
/html/gpu/rtx-4070.html
/html/gpu/rtx-4060.html
/html/gpu/rtx-3090.html
/html/gpu/rtx-3080.html
... (GPU ทั้งหมดใน gpus.json)
```

**Keywords ที่จับได้ (ตัวอย่าง RTX 4060):**
- "RTX 4060 รัน Llama 3 ได้ไหม"
- "RTX 4060 8GB รัน LLM"
- "RTX 4060 VRAM พอไหม"
- "RTX 4060 AI calculator"

**Content ที่แต่ละหน้าควรมี:**
- Title: `[GPU name] รัน Local LLM ได้ไหม — ตรวจสอบ VRAM | ComPair`
- H1 + บทนำเฉพาะ GPU นั้น (VRAM, bandwidth, ราคา)
- ตาราง compatibility กับทุก model (1B–70B, ทุก quantization)
- Calculator embed pre-loaded ด้วย GPU นั้น
- FAQ เฉพาะ GPU: "RTX 4060 รัน 7B ได้ไหม?" "รัน 13B ต้องทำอะไรเพิ่ม?"
- JSON-LD FAQPage schema

**GPU ที่มีใน gpus.json (50 รุ่น):**

| Brand | รุ่น | VRAM |
|---|---|---|
| NVIDIA RTX 40 | 4090, 4080S, 4080, 4070TiS, 4070Ti, 4070S, 4070, 4060Ti-16, 4060Ti-8, 4060 | 8–24 GB |
| NVIDIA RTX 30 | 3090Ti, 3090, 3080Ti, 3080-12, 3080-10, 3070Ti, 3070, 3060Ti, 3060, 3050 | 8–24 GB |
| NVIDIA RTX 20 | 2080Ti, 2080S, 2070S | 8–11 GB |
| NVIDIA GTX | 1080Ti, 1080 | 8–11 GB |
| NVIDIA DC | A100-80, A100-40, A6000 | 40–80 GB |
| AMD RX 7000 | 7900XTX, 7900XT, 7900GRE, 7800XT, 7700XT | 12–24 GB |
| AMD RX 6000 | 6950XT, 6900XT, 6800XT, 6700XT | 12–16 GB |
| Apple M1 | M1, M1 Pro, M1 Max, M1 Ultra | 8–64 GB |
| Apple M2 | M2, M2 Pro, M2 Max, M2 Ultra | 8–96 GB |
| Apple M3 | M3, M3 Pro, M3 Max | 8–128 GB |
| Apple M4 | M4, M4 Pro, M4 Max | 16–128 GB |

---

### ระดับ 2: หน้าแยกต่อ Model (Priority: Should)

**URL Pattern:**
```
/html/model/llama-3-8b.html
/html/model/llama-3-70b.html
/html/model/mistral-7b.html
/html/model/phi-3-mini.html
/html/model/gemma-7b.html
```

**Keywords ที่จับได้ (ตัวอย่าง Llama 3 8B):**
- "Llama 3 8B ต้องการ GPU อะไร"
- "Llama 3 8B VRAM เท่าไหร่"
- "รัน Llama 3 8B บน PC ได้ไหม"
- "Llama 3 8B quantization แนะนำ"

**Content ที่แต่ละหน้าควรมี:**
- ตาราง GPU ทั้งหมดที่รัน model นั้นได้ (เรียงตาม VRAM)
- แนะนำ quantization ที่ดีที่สุดสำหรับแต่ละ GPU tier
- เปรียบเทียบ performance (tok/s) ในแต่ละ GPU

---

### ระดับ 3: Combination Pages (Priority: Could)

**URL Pattern:**
```
/html/rtx-4060-llama-8b.html
/html/rtx-3080-llama-70b.html
/html/m2-pro-mistral-7b.html
```

**Keywords ที่จับได้:**
- "RTX 4060 รัน Llama 3 8B ผล เป็นอย่างไร"
- "RTX 3080 70B model ทำได้ไหม"

**⚠️ ข้อควรระวัง:** ถ้า content ซ้ำกันมากเกินไป (GPU × Model = หลายร้อยหน้า) Google อาจมองเป็น thin content ให้เพิ่มเฉพาะ combination ที่มีคนค้นหาจริงๆ

---

## การ Implement

### วิธีที่แนะนำ: Script-based Generation

เนื่องจากมีข้อมูลครบใน `gpus.json` และ `models.json` สามารถเขียน script เพื่อ generate ได้:

```
data/ai-models/gpus.json    → 50 GPU pages
data/ai-models/models.json  → 5 Model pages
```

**สิ่งที่ต้องทำหลัง generate:**
1. เพิ่ม URL ทั้งหมดใน `sitemap.xml`
2. เพิ่ม link ไปยังหน้าเหล่านี้จาก `index.html` และ `ai-calculator.html`
3. ตรวจสอบ canonical URL ทุกหน้า
4. Submit sitemap ใหม่ใน Google Search Console

---

## ประเมิน Impact vs Effort

| วิธี | จำนวนหน้าใหม่ | Effort | SEO Impact |
|---|---|---|---|
| หน้าต่อ GPU | ~50 หน้า | กลาง (script) | ⭐⭐⭐⭐⭐ |
| หน้าต่อ Model | ~5 หน้า | ต่ำ | ⭐⭐⭐⭐ |
| Combination | หลายร้อยหน้า | สูง | ⭐⭐⭐ (risk thin content) |

**แนะนำให้เริ่มจาก:**
1. หน้าต่อ GPU ก่อน (ROI สูงสุด)
2. ตาม GPU ยอดนิยมก่อน: RTX 4060, RTX 4090, RTX 3080, M1 Max, M2 Pro

---

## Internal Linking Strategy

หลังสร้างหน้า GPU แล้ว ต้องเพิ่ม internal link ด้วย:

```
index.html → link ไป /html/gpu/[id].html ทุกรุ่น
ai-calculator.html → เมื่อ user เลือก GPU → แสดง "ดูรายละเอียด [GPU name]"
```

Internal linking ช่วยให้ Google crawl หน้าใหม่เร็วขึ้น และเพิ่ม PageRank flow

---

## Checklist ก่อน Launch หน้า GPU

- [ ] Title tag unique ต่อหน้า (ไม่ซ้ำกัน)
- [ ] Meta description unique และมี keyword
- [ ] H1 มีชื่อ GPU
- [ ] Canonical URL ชี้ไปตัวเอง
- [ ] JSON-LD FAQPage มี 3–5 คำถามเฉพาะ GPU
- [ ] ลิงก์กลับหน้าหลัก (internal link)
- [ ] เพิ่มใน sitemap.xml
