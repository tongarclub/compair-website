---
name: css-architecture
description: >-
  Guides CSS edits for the ComPair website. Enforces the 5-file CSS
  architecture (theme-*.css, shared.css, ai-specific.css, solar-specific.css).
  Use when the user asks to change colors, typography, component styles, add a
  new page, or edit any .css file in this project.
  For SEO/AEO changes (JSON-LD, meta tags, sitemap), use the seo-aeo skill instead.
disable-model-invocation: true
---

# ComPair CSS Architecture

## File Map — แก้ที่เดียวได้ทุกที่

```
css/
├── theme-ai.css       ← สีและตัวแปร :root ของหน้า AI (gold palette)
├── theme-solar.css    ← สีและตัวแปร :root ของหน้า Solar (green palette)
├── shared.css         ← ทุกอย่างที่ใช้ร่วมกัน (nav, hero, forms, tips, footer)
├── ai-specific.css    ← เฉพาะหน้า AI (GPU card, model cards, quant table, score bar)
└── solar-specific.css ← เฉพาะหน้า Solar (summary cards, ROI table, panel compare)
```

## Rule: แก้ที่ไหน?

| ต้องการแก้ | ไฟล์ |
|---|---|
| สี accent ของหน้า AI (gold) | `css/theme-ai.css` → `--primary`, `--primary2`, `--primary3` |
| สี accent ของหน้า Solar (green) | `css/theme-solar.css` → `--primary`, `--primary2`, `--primary3` |
| สีพื้นหลัง / border / text ของหน้า AI | `css/theme-ai.css` → `--bg`, `--border`, `--text*` |
| สีพื้นหลัง / border / text ของหน้า Solar | `css/theme-solar.css` |
| Status colors (ok/warn/err/info) | เหมือนกันทั้งสอง theme — แก้ทั้ง `theme-ai.css` และ `theme-solar.css` |
| Typography, font size | `css/shared.css` |
| Navigation bar | `css/shared.css` → section `NAVIGATION` |
| Hero section | `css/shared.css` → section `HERO` |
| Form elements (select, chips, inputs) | `css/shared.css` → section `FORM SECTION` |
| Tips section | `css/shared.css` → section `TIPS SECTION` |
| Footer | `css/shared.css` → section `FOOTER` |
| GPU card, model cards, quant table, score bar | `css/ai-specific.css` |
| Summary cards, rec section, ROI table, panel compare | `css/solar-specific.css` |

## CSS Variable System

### Semantic accent variables (defined differently per theme)

```css
--primary   /* main accent color */
--primary2  /* medium variant */
--primary3  /* light variant (borders, decorative) */
```

### Backward-compatible aliases (ใช้ใน inline styles ใน HTML)

```css
/* theme-ai.css aliases */
--gold  → var(--primary)
--gold3 → var(--primary3)

/* theme-solar.css aliases */
--green  → var(--primary)
--green3 → var(--primary3)

/* both themes */
--amber → var(--warn)   --amber-bg → var(--warn-bg)
--green → var(--ok)     --green-bg → var(--ok-bg)    (AI only)
--blue  → var(--info)   --blue-bg  → var(--info-bg)
--red   → var(--err)    --red-bg   → var(--err-bg)
```

> **สำคัญ**: อย่าใช้ `--gold` หรือ `--green` ใน CSS ไฟล์ใหม่ — ใช้ `--primary` แทน
> aliases มีไว้เพื่อความเข้ากันได้กับ inline styles ที่มีอยู่แล้วเท่านั้น

## HTML Page → CSS Files

| HTML file | โหลด CSS |
|---|---|
| `index.html` | `theme-ai.css` + `shared.css` + inline overrides |
| `html/ai-calculator.html` | `theme-ai.css` + `shared.css` + `ai-specific.css` |
| `html/solar-calculator.html` | `theme-solar.css` + `shared.css` + `solar-specific.css` |

## เพิ่มหน้าใหม่

1. ถ้าใช้ gold palette → `<link rel="stylesheet" href="/css/theme-ai.css">`
2. ถ้าใช้ green palette → `<link rel="stylesheet" href="/css/theme-solar.css">`
3. โหลด `shared.css` เสมอ
4. สร้าง `css/<page>-specific.css` สำหรับ component เฉพาะหน้า
5. ใช้ `var(--primary)` สำหรับ accent color — ไม่ใช้ hard-coded hex

## Fonts (Google Fonts)

```
'Cormorant Garamond' — heading, display, decorative numbers
'DM Sans'            — body text
'DM Mono'            — labels, mono tags, code, metadata
```
