---
name: seo-aeo
description: >-
  Guides SEO and AEO (Answer Engine Optimization) work for the ComPair website.
  Covers static JSON-LD schemas, meta tags, Open Graph, sitemap.xml, robots.txt,
  and canonical URLs. Use when the user asks to improve search visibility, add
  structured data, update FAQ content, add a new page to sitemap, or edit
  SEO-related tags in any HTML file.
disable-model-invocation: true
---

# ComPair SEO / AEO Architecture

## ไฟล์ที่เกี่ยวข้อง

| ไฟล์ | หน้าที่ |
|---|---|
| `robots.txt` | อนุญาต crawlers ทุก bot + ชี้ `sitemap.xml` |
| `sitemap.xml` | ลิสต์ทุก URL ที่ต้องการ index |
| `index.html` `<head>` | `WebSite` + `FAQPage` schema |
| `html/ai-calculator.html` `<head>` | `WebPage` + `FAQPage` + `HowTo` schema |
| `html/solar-calculator.html` `<head>` | `WebPage` + `FAQPage` + `HowTo` schema |
| `js/shared/utils.js` | `injectJsonLd()`, `buildFaqSchema()`, `buildHowToSchema()` |

---

## หลักการ: Static ก่อน Dynamic

```
Static JSON-LD (<head> ใน HTML)  ← AI crawlers อ่านได้ทันที ไม่ต้องรัน JS
Dynamic JSON-LD (inject ผ่าน JS) ← Google อ่านได้ แต่ Perplexity/ChatGPT อาจพลาด
```

**กฎ**: FAQ และ HowTo ที่สำคัญต้องอยู่ใน static `<head>` เสมอ  
JS `injectJsonLd()` ใช้เสริมเท่านั้น (เช่น ข้อมูลที่ดึงจาก JSON file แบบ real-time)

---

## โครงสร้าง `<head>` มาตรฐานของทุกหน้า

```html
<!-- 1. Basic meta -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[หน้า] — ComPair</title>
<meta name="description" content="[150–160 ตัวอักษร ภาษาไทย]">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://compair.app/[path]">

<!-- 2. Open Graph -->
<meta property="og:type"        content="website">
<meta property="og:url"         content="https://compair.app/[path]">
<meta property="og:title"       content="[title]">
<meta property="og:description" content="[description]">
<meta property="og:locale"      content="th_TH">

<!-- 3. Static JSON-LD (อย่างน้อย WebPage + FAQPage) -->
<script type="application/ld+json">{ ... }</script>
```

---

## Schema ที่ใช้ในแต่ละหน้า

### `index.html`
- `WebSite` — ชื่อ, URL, hasPart ชี้ไปยัง calculator pages
- `FAQPage` — 4 คำถามทั่วไปเกี่ยวกับ ComPair, GPU, Solar

### `html/ai-calculator.html`
- `WebPage` — isPartOf WebSite
- `FAQPage` — คำถาม GPU+LLM เช่น "RTX 4060 รัน 8B ได้ไหม?", "Q4_K_M คืออะไร?"
- `HowTo` — 3 ขั้นตอนใช้ calculator

### `html/solar-calculator.html`
- `WebPage` — isPartOf WebSite
- `FAQPage` — คำถาม Solar เช่น "คืนทุนกี่ปี?", "Mono vs Poly ต่างกันยังไง?"
- `HowTo` — 3 ขั้นตอนใช้ calculator

---

## เพิ่มหน้าใหม่ — Checklist

```
- [ ] เพิ่ม URL ใน sitemap.xml
- [ ] เพิ่ม <meta name="description"> (150–160 ตัวอักษร)
- [ ] เพิ่ม <link rel="canonical">
- [ ] เพิ่ม Open Graph tags ครบ 5 ตัว
- [ ] เพิ่ม static JSON-LD: WebPage + FAQPage (อย่างน้อย 3 คำถาม)
- [ ] เพิ่ม HowTo schema (ถ้าหน้ามี calculator/form)
```

---

## เพิ่ม/แก้ FAQ

แก้ static JSON-LD ใน `<head>` ของไฟล์ HTML โดยตรง:

```json
{
  "@type": "Question",
  "name": "[คำถามที่ผู้ใช้จะค้นหา — ควรตรงกับ search intent]",
  "acceptedAnswer": {
    "@type": "Answer",
    "text": "[คำตอบตรงประเด็น ข้อมูลครบ ไม่ต้องยาวเกินไป]"
  }
}
```

**แนวทางเขียน FAQ ที่ดี:**
- คำถามควรตรงกับสิ่งที่คนจะพิมพ์ใน Google / AI
- คำตอบควรมีตัวเลขจริง (เช่น "4.1 GB", "6–8 ปี", "~97%")
- ไม่ต้องเกิน 3–4 ประโยคต่อคำตอบ

---

## Dynamic JSON-LD (JS utils)

```js
import { injectJsonLd, buildFaqSchema, buildHowToSchema } from '/js/shared/utils.js';

// เรียกหลัง data load เสร็จ
injectJsonLd(buildFaqSchema([
  { question: '...', answer: '...' }
]), 'jsonld-dynamic-faq');   // ← ใส่ unique id เพื่อกัน duplicate
```

ใช้สำหรับ FAQ ที่ต้องการข้อมูล real-time จาก JSON files (เช่น ชื่อ GPU ที่ score สูงสุด)  
**อย่าใส่ id เดียวกับ static script** เพราะ `injectJsonLd()` จะ overwrite

---

## Base URL

```
Production: https://compair.app
```

อัปเดตทุกที่ถ้า domain เปลี่ยน: `sitemap.xml`, `robots.txt`, `<link rel="canonical">`, `og:url`, JSON-LD `url` fields
