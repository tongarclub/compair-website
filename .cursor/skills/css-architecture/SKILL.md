---
name: css-architecture
description: >-
  Guides CSS edits for the ComPair website. Enforces the CSS architecture
  (theme-*.css → shared.css → page-specific.css). Use when the user asks to
  change colors, typography, component styles, or add a new page.
  For SEO/AEO changes (JSON-LD, meta tags, sitemap), use the seo-aeo skill instead.
disable-model-invocation: true
---

# ComPair CSS Architecture

## ⚠️ Critical: CSS Loading Order

**ทุกหน้าต้องโหลด CSS ในลำดับนี้เสมอ — มิฉะนั้น CSS variables จะไม่มีค่า:**

```html
<!-- 1. Theme ก่อน — defines --primary, --bg, --border, --text* ฯลฯ -->
<link rel="stylesheet" href="../css/theme-ev.css">
<!-- 2. Shared — ใช้ var() ที่ theme กำหนด -->
<link rel="stylesheet" href="../css/shared.css">
<!-- 3. Page-specific — override หรือเพิ่มเติมจาก shared -->
<link rel="stylesheet" href="../css/ev-specific.css">
```

## File Map

```
css/
├── theme-ai.css       ← :root variables — Gold/Warm Brown palette (AI pages)
├── theme-solar.css    ← :root variables — Forest Green palette (Solar page)
├── theme-ev.css       ← :root variables — Warm Beige/Gold palette (EV page)
├── shared.css         ← ทุกอย่างที่ใช้ร่วมกัน (nav, hero, forms, tips, footer)
├── ai-specific.css    ← GPU card, model cards, quant table, score bar
├── solar-specific.css ← summary cards, ROI table, panel compare
├── ev-specific.css    ← preset cards, bar chart, TCO table, solar CTA
└── gpu-page.css       ← GPU/Model detail pages (html/gpu/, html/model/)
```

## Rule: แก้ที่ไหน?

| ต้องการแก้ | ไฟล์ |
|---|---|
| สี accent ของหน้า AI | `css/theme-ai.css` → `--primary`, `--primary2`, `--primary3` |
| สี accent ของหน้า Solar | `css/theme-solar.css` → `--primary`, `--primary2`, `--primary3` |
| สี accent ของหน้า EV | `css/theme-ev.css` → `--primary`, `--primary2`, `--primary3` |
| Typography, font size | `css/shared.css` |
| Navigation bar | `css/shared.css` → section `NAVIGATION` |
| Hero section | `css/shared.css` → section `HERO` |
| Form elements (inputs, labels, buttons) | `css/shared.css` → section `FORM SECTION` |
| Tips section | `css/shared.css` → section `TIPS SECTION` |
| Footer | `css/shared.css` → section `FOOTER` |
| GPU card, model cards, quant table | `css/ai-specific.css` |
| Solar ROI table, panel compare | `css/solar-specific.css` |
| EV preset cards, bar chart, TCO table | `css/ev-specific.css` |

## HTML Page → CSS Files

| HTML file | โหลด CSS (ตามลำดับ) |
|---|---|
| `index.html` | `theme-ai.css` → `shared.css` |
| `html/ai-calculator.html` | `theme-ai.css` → `shared.css` → `ai-specific.css` |
| `html/solar-calculator.html` | `theme-solar.css` → `shared.css` → `solar-specific.css` |
| `html/ev-calculator.html` | `theme-ev.css` → `shared.css` → `ev-specific.css` |
| `html/mac-llm-calculator.html` | `theme-ai.css` → `shared.css` |
| `html/gpu/*.html` | `gpu-page.css` (standalone, no shared.css) |
| `html/model/*.html` | `gpu-page.css` (standalone, no shared.css) |

## ⚠️ Class Names — ใช้ให้ถูกต้อง (shared.css)

นี่คือ class names ที่มีใน `shared.css` — **ห้ามสร้าง class ซ้ำในชื่อที่ไม่มีอยู่จริง**

### Navigation
```html
<nav>
  <div class="wrap">
    <div class="nav-inner">
      <a href="../index.html" class="logo">
        <div class="logo-mark">C</div>
        <div>
          <div class="logo-text">ComPair</div>
          <div class="logo-sub">Comparison Engine</div>
        </div>
      </a>
      <div class="nav-right">
        <a href="..." class="nav-link">Link</a>
        <span class="nav-badge">Current Page</span>  <!-- active indicator -->
      </div>
    </div>
  </div>
</nav>
```

> **ห้ามใช้**: `.top-nav`, `.logo-link`, `.nav-links`, `.nav-link-active` — ไม่มีใน shared.css

### Hero
```html
<div class="hero">
  <div class="wrap">
    <div class="hero-label">Domain X · Category</div>
    <h1>Title<br><em>Subtitle</em></h1>  <!-- h1 มี global style ใน shared.css -->
    <p class="hero-desc">Description</p>
    <!-- hero-card (optional sidebar card) -->
  </div>
</div>
```

> **ห้ามใช้**: `.hero-inner`, `.hero-title`, `.hero-chips`, `.hero-chip`
> **ทางเลือก**: ถ้าต้องการ chips/tags ให้เพิ่มใน page-specific CSS แทน (เช่น `.ev-chips`, `.ev-chip`)

### Form Sections
```html
<div class="form-section">
  <div class="form-header">
    <div class="form-title">Section Title</div>
    <div class="form-subtitle">Subtitle / step info</div>
  </div>
  <div class="form-body" style="grid-template-columns:repeat(3,1fr)">
    <div class="form-col">
      <label class="field-label">Label</label>
      <div class="num-input-wrap">
        <input class="num-input" type="number">
        <span class="num-unit">unit</span>
      </div>
      <div class="field-hint">Hint text</div>
    </div>
  </div>
  <div style="padding:0 32px 28px">
    <button class="calc-btn">คำนวณ</button>
  </div>
</div>
```

> **ห้ามใช้**: `.calc-wrap`, `.calc-section`, `.section-hd`, `.section-label`, `.section-title`, `.section-sub`, `.field-grid`, `.field-group`, `.field-input`, `.input-row`, `.field-unit`
> **ใช้แทน**: `.form-section`, `.form-header`, `.form-title`, `.form-subtitle`, `.form-body`, `.form-col`, `.num-input-wrap`, `.num-input`, `.num-unit`, `.field-hint`, `.field-label`

### Tips Section
```html
<div class="tips-section">
  <div class="tips-title">Tips Title <em>highlight</em></div>
  <div class="tips-grid">  <!-- 3-col by default, override with style="" -->
    <div class="tip-item">
      <div class="ti-num">01</div>
      <div class="ti-title">Tip Title</div>
      <div class="ti-text">Tip content <code>code snippet</code></div>
    </div>
  </div>
</div>
```

### Footer
```html
<footer>
  <div class="wrap">
    <div class="footer-inner">
      <div class="footer-logo">ComPair · Page Name</div>
      <div class="footer-meta">source attribution</div>
      <div class="footer-links">
        <a href="../index.html">← หน้าหลัก</a>
        <a href="other-page.html">Other →</a>
      </div>
    </div>
  </div>
</footer>
```

> **ห้ามใช้**: `.site-footer` — ใช้แค่ `footer` (element selector)

### Section Divider
```html
<div class="section-divider">
  <div class="sd-line"></div>
  <div class="sd-label">Label Text</div>
  <div class="sd-line"></div>
</div>
```

### Utilities
```html
.wrap          <!-- max-width container, centered -->
.fade-up       <!-- fade-in animation -->
.placeholder   <!-- empty state box -->
.info-block    <!-- bordered info text block -->
.ram-chips / .ram-chip  <!-- chip selector (AI page) -->
.select-wrap   <!-- custom select dropdown -->
```

## เพิ่มหน้าใหม่ — Checklist

1. **สร้าง `css/theme-<page>.css`** กำหนด `:root { --primary, --bg, --surface, --border, --text* }`
2. **โหลด CSS ถูกลำดับ**: `theme-<page>.css` → `shared.css` → `<page>-specific.css`
3. **ใช้ class จาก shared.css** ตามตัวอย่างข้างบน — ห้ามสร้าง class ชื่อซ้ำที่ไม่มีใน shared.css
4. **เพิ่มใน page-specific.css** เฉพาะ component ใหม่ที่ shared.css ไม่มี
5. **ใช้ `var(--primary)`** แทน hard-coded hex สำหรับ accent color
6. **Relative path**: จาก `html/*.html` ใช้ `href="../css/..."` เสมอ

## CSS Variable System

### Core variables (defined in theme-*.css)
```css
--bg          /* page background */
--bg2         /* secondary background */
--surface     /* card/box background */
--surface2    /* alternate surface (form headers) */
--border      /* default border color */
--border2     /* stronger border */
--text        /* primary text */
--text2       /* secondary text */
--text3       /* tertiary / muted text */
--primary     /* main accent color */
--primary2    /* dark variant */
--primary3    /* light variant */
--ok / --ok-bg        /* success state */
--warn / --warn-bg    /* warning state */
--err / --err-bg      /* error state */
--info / --info-bg    /* info state */
```

## Path Rules — GitHub Pages Compatible

```html
<!-- index.html (root) -->
<link rel="stylesheet" href="css/theme-ai.css">

<!-- html/*.html -->
<link rel="stylesheet" href="../css/theme-ev.css">

<!-- navigation links from html/ back to root -->
<a href="../index.html">หน้าหลัก</a>

<!-- between pages in html/ -->
<a href="solar-calculator.html">Solar</a>
```

## Typography Scale (Readable — อัปเดต มิ.ย. 2026)

| Role | Size | ไฟล์ | หมายเหตุ |
|---|---|---|---|
| Body text | **16px** | `shared.css` body | |
| Body line-height | **1.75** | `shared.css` body | |
| Hero description | **16px** | `shared.css` `.hero-desc` | |
| h1 | `clamp(48px, 6vw, 80px)` | `shared.css` `h1` | |
| Tips body text | **14px** | `shared.css` `.ti-text` | |
| Tips title | **16px** | `shared.css` `.ti-title` | |
| Field hints | **14px** | `shared.css` `.field-hint` | |
| Footer links | **14px** | `shared.css` `.footer-links a` | |
| Mono labels | **11px** | `shared.css` `.field-label` | |
| Caption / meta | **12px** | ทุกไฟล์ | |

> **กฎ**: อย่าใช้ font-size ต่ำกว่า **11px** สำหรับ text ที่คนต้องอ่าน

## Fonts (Google Fonts)

```
'Cormorant Garamond' — heading, display, decorative numbers
'DM Sans'            — body text
'DM Mono'            — labels, mono tags, code, metadata
```

โหลด font ใน `<head>` ก่อน CSS:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
```
