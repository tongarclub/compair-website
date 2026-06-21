# ComPair — Comparison Engine & Calculator

Static AEO-Optimized comparison engine สำหรับ AI Hardware VRAM และ Solar Cell ROI

---

## วิธีรันเว็บ (Local Development)

> **จำเป็น**: เว็บใช้ ES Modules (`import/export`) และ `fetch()` จึงต้องรันผ่าน HTTP Server เท่านั้น  
> ห้ามเปิดด้วยการดับเบิลคลิกไฟล์ HTML โดยตรง (จะเกิด CORS error)

### วิธีที่ 1 — Python (แนะนำ · ไม่ต้องติดตั้งอะไรเพิ่ม)

```bash
cd /path/to/compair-website
python3 -m http.server 8080
```

เปิดเบราว์เซอร์ที่ → **http://localhost:8080**

### วิธีที่ 2 — VS Code Live Server Extension

1. ติดตั้ง Extension **"Live Server"** โดย Ritwick Dey
2. คลิกขวาที่ `index.html` → **"Open with Live Server"**
3. เว็บจะเปิดที่ `http://127.0.0.1:5500` อัตโนมัติ

### วิธีที่ 3 — Node.js `serve`

```bash
npx serve .
```

---

## โครงสร้างโปรเจกต์

```
compair-website/
├── index.html                      ← หน้าหลัก (Domain selector)
├── robots.txt                      ← Crawler guidance
├── sitemap.xml                     ← Sitemap สำหรับ Search Engines
│
├── html/
│   ├── ai-calculator.html          ← Domain A: AI Hardware VRAM Calculator
│   └── solar-calculator.html       ← Domain B: Solar Cell ROI & Sizing Calculator
│
├── css/                            ← CSS Architecture (แก้ที่เดียวได้ทุกที่)
│   ├── theme-ai.css                ← สีและตัวแปร :root สำหรับ AI page (gold palette)
│   ├── theme-solar.css             ← สีและตัวแปร :root สำหรับ Solar page (green palette)
│   ├── shared.css                  ← Nav, Hero, Forms, Tips, Footer (ใช้ร่วมกันทุกหน้า)
│   ├── ai-specific.css             ← GPU card, Model cards, Quant table, Score bar
│   └── solar-specific.css          ← Summary cards, ROI table, Panel compare
│
├── data/                           ← Flat-file JSON (ไม่มี Database)
│   ├── ai-models/
│   │   ├── gpus.json               ← GPU catalog: NVIDIA / AMD / Apple Silicon (50+ รุ่น)
│   │   ├── cpus.json               ← CPU catalog
│   │   ├── models.json             ← LLM catalog: Llama / Mistral / Phi / Gemma
│   │   └── llama3-8b.json          ← ตัวอย่าง AI Model schema
│   └── solar/
│       ├── panels.json             ← Solar panel catalog: Jinko / LONGi / Canadian / SunPower
│       └── inverters.json          ← Inverter catalog: GoodWe / Sungrow / Huawei / SolarEdge
│
├── js/                             ← Domain-Driven JavaScript (Pure Functions)
│   ├── ai/
│   │   └── calculator.js           ← VRAM compatibility & GPU scoring functions
│   ├── solar/
│   │   └── calculator.js           ← ROI, sizing & CO₂ savings functions
│   └── shared/
│       └── utils.js                ← JSON-LD injector, data fetcher, formatters
│
├── design/
│   └── specs-light.html            ← Design reference (original spec)
│
├── .cursor/skills/
│   └── css-architecture/SKILL.md   ← Cursor AI skill: CSS architecture guide
│
└── prompt.md                       ← Project context & requirements
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Pure HTML + CSS + Vanilla JavaScript |
| Database | ไม่มี — ใช้ Flat-file JSON |
| Build Tool | ไม่มี — รันได้ทันทีจาก Static files |
| Testing | Jest / Vitest (สำหรับ Pure Functions ใน `js/`) |
| SEO/AEO | Static JSON-LD Schema.org ใน `<head>` + `sitemap.xml` + `robots.txt` |

---

## Domain A — AI Hardware VRAM Calculator

**ไฟล์:** `html/ai-calculator.html`

**ฟีเจอร์:**
- เลือก GPU / CPU / RAM → ประเมิน LLM Compatibility ทันที
- แสดง Quantization ทุกระดับ (FP16 → Q2_K) พร้อมสถานะ ok/warn/split/no
- ประมาณ Tokens/sec จาก Memory Bandwidth
- Compatibility Score 0–100 ต่อ GPU
- ตาราง Quantization Reference ครบถ้วน

**Pure Functions ที่ Test ได้ (`js/ai/calculator.js`):**
```js
getQuantCompatibility(gpuVramGB, modelVramGB, systemRamGB) // → 'ok'|'warn'|'split'|'no'
evaluateModelQuants(model, gpuVramGB, systemRamGB, quantKeys)
scoreGPU(perfScore, vramGB)                                // → 0–100
estimateTokPerSec(baseSpeed, bandwidthGBs)
recommendQuant(quantResults)
```

---

## Domain B — Solar Cell ROI & Sizing Calculator

**ไฟล์:** `html/solar-calculator.html`

**ฟีเจอร์:**
- ป้อนค่าไฟ (หน่วย/เดือน) + เลือกภูมิภาค → คำนวณขนาดระบบที่แนะนำทันที
- เปรียบเทียบแผง 10+ รุ่น และอินเวอร์เตอร์หลายยี่ห้อ
- ตาราง ROI แบบรายปีตลอด 25 ปี
- แสดงผลลด CO₂ (kg/ปี) และ lifetime savings (บาท)

**Pure Functions ที่ Test ได้ (`js/solar/calculator.js`):**
```js
calcDailyEnergy(systemKW, peakSunHours, lossFactor)
calcAnnualEnergy(systemKW, year, ...)          // คำนึง degradation ตามอายุปี
calcSystemSize(dailyDemandKWh, ...)            // → kW ที่แนะนำ
calcPanelCount(systemKW, panelWattage)         // → จำนวนแผง
calcROI({ systemKW, totalCostTHB, ... })       // → paybackYears, ROI%, lifetime savings
calcCO2Savings(annualEnergyKWh)                // → kg CO₂/year
```

---

## CSS Architecture — แก้ที่เดียวได้ทุกที่

| ต้องการแก้ | ไฟล์ |
|---|---|
| สี accent ของหน้า AI (gold) | `css/theme-ai.css` → `--primary` |
| สี accent ของหน้า Solar (green) | `css/theme-solar.css` → `--primary` |
| Typography, font size | `css/shared.css` |
| Navigation / Hero / Footer | `css/shared.css` |
| GPU card, model cards | `css/ai-specific.css` |
| ROI table, panel compare | `css/solar-specific.css` |

**เพิ่มหน้าใหม่:**
```html
<link rel="stylesheet" href="/css/theme-ai.css">   <!-- หรือ theme-solar.css -->
<link rel="stylesheet" href="/css/shared.css">
<link rel="stylesheet" href="/css/my-page-specific.css">
```

---

## AEO / SEO Implementation

### Static JSON-LD (ใน `<head>` ทุกหน้า)

แต่ละหน้ามี Schema.org JSON-LD แบบ static ที่ AI crawlers อ่านได้โดยไม่ต้องรัน JavaScript:

| หน้า | Schema types |
|---|---|
| `index.html` | `WebSite` + `FAQPage` |
| `ai-calculator.html` | `WebPage` + `FAQPage` + `HowTo` |
| `solar-calculator.html` | `WebPage` + `FAQPage` + `HowTo` |

### Dynamic JSON-LD (inject ผ่าน JS หลัง data load)

`utils.js` มีฟังก์ชัน helper สำหรับ inject schema ที่มีข้อมูล dynamic (จาก JSON files):

```js
import { injectJsonLd, buildFaqSchema, buildHowToSchema } from '/js/shared/utils.js';

// FAQ schema พร้อมข้อมูลจริงจาก data
injectJsonLd(buildFaqSchema([
  { question: 'RTX 4070 12GB รัน Llama 3 8B ได้ไหม?',
    answer: 'ได้ ด้วย Q4_K_M ใช้ VRAM 4.1 GB จากทั้งหมด 12 GB' }
]), 'jsonld-faq-dynamic');
```

### ไฟล์ SEO อื่นๆ

| ไฟล์ | หน้าที่ |
|---|---|
| `robots.txt` | อนุญาต crawlers ทุก bot + ชี้ sitemap |
| `sitemap.xml` | บอก Search Engines ว่ามีหน้าไหนบ้าง |
| `<link rel="canonical">` | ป้องกัน duplicate content |
| `<meta property="og:*">` | Social sharing + บาง AI crawlers |

---

## เพิ่มข้อมูล GPU / Model / Panel

แก้ไขไฟล์ JSON ใน `/data/` ตามโครงสร้าง schema ที่กำหนด:

```bash
# เพิ่ม GPU ใหม่
vim data/ai-models/gpus.json

# เพิ่ม Solar panel ใหม่
vim data/solar/panels.json
```

---

## Unit Testing

```bash
npm init -y
npm install -D vitest

# เพิ่มใน package.json:
# "scripts": { "test": "vitest" }

npx vitest
```

Pure Functions ทุกตัวใน `js/` รับ input → return output โดยไม่มี side effects  
ครอบ test ได้โดยตรงโดยไม่ต้อง mock browser APIs
