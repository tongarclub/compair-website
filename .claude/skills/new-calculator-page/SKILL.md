---
name: new-calculator-page
description: Guides creation of new comparison/calculator pages for ComPair website. Use when adding a new calculator, comparison tool, or domain page - such as creating a new calculator page, adding a new domain, or setting up a new comparison feature.
---

# ComPair — สร้าง Calculator หน้าใหม่

## โครงสร้างโปรเจกต์

```
index.html                      ← หน้าแรก (domain cards grid)
html/
  ai-calculator.html            ← Domain A: GPU + LLM VRAM
  solar-calculator.html         ← Domain B: Solar ROI
  mac-llm-calculator.html       ← Domain C: Apple Silicon + LLM
  ev-calculator.html            ← Domain D: EV vs Gasoline TCO
  gold-calculator.html          ← Domain E: ทองคำ vs กองทุน ROI
  image-gen-calculator.html     ← Domain F: AI Image Gen VRAM + Cost
css/
  theme-ai.css                  ← Gold/Warm palette (Domain A, C)
  theme-solar.css               ← Green palette (Domain B)
  theme-ev.css                  ← Beige/Warm palette (Domain D)
  theme-gold.css                ← Deep Gold/Amber palette (Domain E)
  theme-image-gen.css           ← Cool Indigo/Slate palette (Domain F)
  shared.css                    ← All shared components
  ai-specific.css               ← Domain A styles
  solar-specific.css            ← Domain B styles
  ev-specific.css               ← Domain D styles
  gold-specific.css             ← Domain E styles
  image-gen-specific.css        ← Domain F styles
data/
  ai-models/gpus.json           ← GPU data (50+ รุ่น)
  ai-models/models.json         ← LLM model sizes
  ai-models/llm-models.json     ← Specific LLM models for detail pages
  solar/panels.json
  solar/inverters.json
sitemap.xml                     ← ต้องเพิ่ม URL ใหม่ทุกครั้ง
```

**Next Domain Letter**: G (Domain G onward)

---

## Design System

ทุกหน้าใช้ CSS variables ชุดเดียวกัน + fonts เดียวกัน:

```css
/* Fonts */
@import 'Cormorant Garamond' /* headings, serif */
@import 'DM Sans'            /* body */
@import 'DM Mono'            /* labels, code, meta */

/* Key variables */
--bg: #F7F5F1    --surface: #FFFFFF    --border: #E4DDD3
--gold: #8B7355  --gold3: #D4BC96      --text: #1C1916
--green: #3D7A5A --amber: #8B6914      --red: #8B3A3A
--blue: #2D5A8E
```

**Reference design**: `design/specs-light.html` — ใช้เป็น template หน้าใหม่ทุกครั้ง

---

## โครงสร้าง HTML มาตรฐาน

```html
<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-J3C1X16FZ5"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-J3C1X16FZ5');
  </script>
  <!-- SEO meta (canonical, OG, JSON-LD) -->
  <!-- Fonts: Cormorant Garamond + DM Sans + DM Mono -->
  <!-- CSS (copy design system จาก specs-light.html) -->
</head>
<body>
  <!-- NAV: logo "ComPair" + nav links + link กลับ index -->
  <!-- HERO: grid 2-col (text + hero-card) -->
  <!-- FORM SECTION: selector inputs -->
  <!-- RESULTS: spec card + compatibility cards -->
  <!-- COMPARISON TABLE (optional) -->
  <!-- BUYING GUIDE / TIPS -->
  <!-- FOOTER: links ไป index + หน้าอื่น -->
  <!-- SCRIPT: data arrays + init() + render() -->
</body>
```

---

## Checklist เพิ่มหน้าใหม่

```
- [ ] สร้าง html/[name].html (copy structure จาก mac-llm-calculator.html)
- [ ] เพิ่ม Google Analytics tag (G-J3C1X16FZ5)
- [ ] เพิ่ม canonical URL + OG tags + static JSON-LD (WebPage + FAQPage)
- [ ] อัปเดต sitemap.xml เพิ่ม <loc> ใหม่
- [ ] อัปเดต index.html เพิ่ม domain card ใหม่
- [ ] อัปเดต JSON-LD ใน index.html (hasPart array)
- [ ] เพิ่ม footer links ข้ามหน้า
```

---

## อัปเดต `index.html`

### เพิ่ม Domain Card

```html
<a class="domain-card" href="html/[name].html">
  <div class="dc-index">Domain [X] · [Category]</div>
  <div class="dc-icon">[symbol]</div>
  <div class="dc-title">[ชื่อหน้า]</div>
  <div class="dc-desc">[คำอธิบาย 1–2 ประโยค]</div>
  <div class="dc-spotlight">
    <div class="sp-row">
      <span class="sp-name">[example]</span>
      <span class="sp-chip sp-chip-score">[highlight]</span>
    </div>
  </div>
  <div class="dc-cta">เปิดเครื่องมือ <svg ...></svg></div>
</a>
```

### อัปเดต JSON-LD `hasPart`

เพิ่มใน static JSON-LD `WebSite` schema ใน `<head>`:

```json
{
  "@type": "WebPage",
  "name": "[ชื่อหน้า]",
  "url": "https://tongarclub.github.io/compair-website/html/[name].html",
  "description": "[คำอธิบายสั้น]"
}
```

---

## อัปเดต `sitemap.xml`

```xml
<url>
  <loc>https://tongarclub.github.io/compair-website/html/[name].html</loc>
  <changefreq>weekly</changefreq>
  <priority>0.9</priority>
</url>
```

---

## Token Speed Formula (สำหรับ calculator)

```js
// NVIDIA GPU
tokSpeed = Math.round(model.baseTokPerSec * gpu.bandwidthGBs / 600)

// Apple Silicon (Metal ~80% efficient vs CUDA)
tokSpeed = Math.round(model.baseTokPerSec * mac.bw / 500)
```

---

## Base URL

```
https://tongarclub.github.io/compair-website/
```

Path ใน `html/*.html` ต้องใช้ `../` prefix:
- CSS/JS: `../css/`, `../js/`, `../data/`
- Links: `../index.html`, `other-page.html` (same folder)

---

## หน้าที่มีอยู่แล้ว (อย่า duplicate keyword)

| หน้า | Domain | Theme CSS | Keywords หลัก |
|---|---|---|---|
| `ai-calculator.html` | A | theme-ai.css | GPU รัน LLM, VRAM calculator, RTX vs LLM |
| `solar-calculator.html` | B | theme-solar.css | โซล่าเซลล์คืนทุน, ROI 25 ปี |
| `mac-llm-calculator.html` | C | theme-ai.css | MacBook Pro รัน LLM, Apple Silicon vs RTX |
| `ev-calculator.html` | D | theme-ev.css | BYD Seal ค่าชาร์จ, EV vs น้ำมัน, TCO |
| `gold-calculator.html` | E | theme-gold.css | ทองคำ vs กองทุน, ลงทุน Compound interest |
| `image-gen-calculator.html` | F | theme-image-gen.css | FLUX.1 VRAM, SD XL GPU, Midjourney vs self-hosted |

---

## Share URL Pattern (ทุกหน้าต้องมี)

เพิ่ม `syncURL()`, `loadFromURL()`, และปุ่ม Share ทุกหน้าใหม่:

```js
function syncURL() {
  const params = new URLSearchParams({ key1: val1, key2: val2 });
  history.replaceState(null, '', '?' + params.toString());
}
function loadFromURL() {
  const p = new URLSearchParams(location.search);
  if (!p.has('key1')) return;
  document.getElementById('input1').value = p.get('key1');
  // ...restore all inputs
}
function copyURL() {
  navigator.clipboard.writeText(location.href).then(() => {
    const msg = document.getElementById('shareMsg');
    msg.style.opacity = '1';
    setTimeout(() => msg.style.opacity = '0', 2500);
  });
}
```

Share button HTML:
```html
<div class="share-row">
  <button class="share-btn" id="shareBtn" onclick="copyURL()">⎘ แชร์ผลนี้</button>
  <span id="shareMsg">✓ คัดลอก URL แล้ว</span>
</div>
```
