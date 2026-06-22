# ComPair — SEO/AEO Timeline & Custom Domain

> สรุปจากการวิเคราะห์สำหรับ ComPair (`tongarclub.github.io/compair-website/`)  
> อัปเดต: มิถุนายน 2026

---

## 1. SEO/AEO จะขึ้นบน Google หรือ AI ประมาณกี่วัน?

**ไม่มีกำหนดวันที่แน่นอน** — SEO/AEO เป็นกระบวนการที่ใช้เวลา ไม่ใช่เปิดสวิตช์แล้วขึ้นทันที

### Timeline โดยประมาณ

| ช่วง | Google (SEO) | AI (AEO) |
|---|---|---|
| ถูก crawl / รู้จัก | 3–14 วัน | 1–4 สัปดาห์ |
| เริ่มมี impression / ถูกอ้างอิง | 2–8 สัปดาห์ | 2–6 สัปดาห์ (คำถาม niche) |
| ติดอันดับ / ถูก cite สม่ำเสมอ | 3–6 เดือนขึ้นไป | 1–3 เดือน (ถ้า content ตรง intent) |

### Google (SEO)

#### Index — ให้ Google รู้จักหน้า
- **เว็บใหม่ / หน้าใหม่**: ประมาณ **3–14 วัน** หลัง deploy
- Submit sitemap ผ่าน **Google Search Console** อาจเร็วขึ้นเป็น **1–7 วัน**
- ComPair มี `sitemap.xml` + `robots.txt` ครบแล้ว — ช่วยให้ Google หา URL ได้เร็วขึ้น แต่ยังต้องรอ bot มา crawl

#### Ranking — ติดหน้าแรก / อันดับดี
- **คีย์เวิร์ดแข่งน้อย** (เช่น "RTX 4060 รัน 8B ได้ไหม", "คืนทุนโซลาร์เซลล์กี่ปี"): **2–8 สัปดาห์**
- **คีย์เวิร์ดแข่งสูง** ("โซลาร์เซลล์", "GPU AI"): **3–6 เดือนขึ้นไป** หรืออาจไม่ติดเลยถ้า domain authority ต่ำ

#### ปัจจัยที่ทำให้ ComPair ช้ากว่าเว็บทั่วไป
- อยู่บน **GitHub Pages subdomain** (`tongarclub.github.io`) — authority ต่ำกว่า custom domain
- มีแค่ **3 หน้า** — Google มักให้ความสำคัญกับเว็บที่มี content มากและอัปเดตสม่ำเสมอ
- ยังไม่มี backlink / social signal

### AI Search (AEO)

AEO ต่างจาก SEO ตรงที่ AI ไม่ได้ "จัดอันดับ" แต่ **เลือก cite แหล่งที่ตอบคำถามได้ตรงที่สุด**

| Engine | พฤติกรรม | Timeline โดยประมาณ |
|---|---|---|
| Perplexity / Google AI Overview / Bing Copilot | Crawl แบบ real-time หรือ near real-time | 2–6 สัปดาห์ (คำถาม niche) |
| ChatGPT (Browse / Search) | มัก cite เว็บ authority สูงก่อน | ไม่แน่นอน — GitHub Pages + เว็บใหม่ = โอกาสต่ำในช่วงแรก |

#### สิ่งที่ ComPair ทำได้ดีแล้ว
- Static `FAQPage` + `HowTo` schema ใน `<head>` — AI crawler อ่านได้ทันที (ไม่ต้องรัน JS)
- คำถาม FAQ ตรง search intent (เช่น "Q4_K_M คืออะไร?", "Mono vs Poly ต่างกันยังไง?")
- คำตอบมีตัวเลขจริง — AI ชอบ cite ข้อมูล concrete

### Timeline จริงที่ควรคาดหวัง (ComPair)

```
วันที่ 0          → Deploy + submit sitemap ใน GSC
วันที่ 3–7        → Google เริ่ม index หน้า (เช็คด้วย site: URL)
วันที่ 2–4 สัปดาห์ → เริ่มมี impression ใน GSC (คีย์เวิร์ด long-tail)
วันที่ 1–2 เดือน   → AI อาจ cite FAQ บางข้อ (ถ้าไม่มีคู่แข่งตอบดีกว่า)
วันที่ 3–6 เดือน   → Ranking เริ่มนิ่ง (ถ้ามี content + backlink เพิ่ม)
```

### วิธีเช็คว่า "ขึ้นแล้ว" หรือยัง

| ช่องทาง | วิธีเช็ค |
|---|---|
| Google Index | พิมพ์ `site:tongarclub.github.io/compair-website` ใน Google |
| Google Search Console | ดู Coverage, Performance, FAQ rich results |
| Google Analytics (GA4) | ดู Users, Sessions, Page views, Traffic source |
| Perplexity | ถามคำถาม FAQ ตรง ๆ เช่น "RTX 4060 รัน 8B ได้ไหม" |
| Google Rich Results Test | ทด schema ที่ https://search.google.com/test/rich-results |

### สิ่งที่ช่วยให้เร็วขึ้น

#### Must (ทำได้ทันที)
- [ ] ลงทะเบียน **Google Search Console** + submit sitemap
- [ ] ติดตั้ง **Google Analytics (GA4)** ในทุกหน้า HTML (ดู §4)
- [ ] เช็ค index ทุก 3–5 วันด้วย `site:` query

#### Should (ช่วย AEO + SEO)
- [ ] เพิ่ม FAQ ใหม่ตามคำถามที่ user ถามจริง
- [ ] แชร์ลิงก์ใน community ที่เกี่ยวข้อง (Reddit, Pantip, Facebook group GPU/โซลาร์)
- [ ] อัปเดต `lastmod` ใน sitemap เมื่อแก้ content

#### Could (ระยะยาว)
- [ ] ย้ายไป **custom domain** — authority ดีกว่า GitHub subdomain มาก
- [ ] เพิ่ม blog/article หน้าใหม่ — ขยาย long-tail keywords

---

## 2. Custom Domain มีค่าใช้จ่ายไหม?

**มีค่าใช้จ่าย — แต่เฉพาะค่าซื้อ/ต่ออายุโดเมนเท่านั้น**

GitHub Pages รองรับ custom domain **ฟรี** (รวม SSL/HTTPS) — ไม่มีค่า hosting เพิ่ม

| สถานะ | URL | ค่าใช้จ่าย |
|---|---|---|
| ปัจจุบัน | `tongarclub.github.io/compair-website/` | **ฟรี 100%** |
| Custom domain | เช่น `compair.com` | **≈ 300–800 บาท/ปี** |

### ราคาโดเมนโดยประมาณ (2026)

| ประเภท | ราคา/ปี (โดยประมาณ) | เหมาะกับ ComPair? |
|---|---|---|
| `.com` | ~350–800 บาท (~$10–20) | ✅ แนะนำ — สากล น่าเชื่อถือ |
| `.app` / `.dev` | ~400–900 บาท | ✅ ดีถ้าเน้น tech/tool |
| `.in.th` | ~300–500 บาท | ✅ ถูกกว่า .co.th ไม่ต้องมีนิติบุคคล |
| `.co.th` | ~800–2,500+ บาท | ⚠️ ต้องมีหนังสือรับรองบริษัท/เครื่องหมายการค้า |
| `.th` (ระดับบนสุด) | หลักหมื่นบาท+ | ❌ ไม่จำเป็นสำหรับโปรเจกต์นี้ |

> **หมายเหตุ:** ปีแรกมักถูกกว่า (promo 99–299 บาท) แต่ **ต่ออายุแพงกว่า** — ดูราคา renewal ก่อนซื้อเสมอ

### สิ่งที่ฟรี (ไม่ต้องจ่ายเพิ่ม)

| รายการ | ค่าใช้จ่าย |
|---|---|
| GitHub Pages hosting | ฟรี |
| Custom domain บน GitHub Pages | ฟรี |
| SSL/HTTPS (Let's Encrypt) | ฟรี |
| DNS (Cloudflare free tier) | ฟรี |

### ตัวอย่างค่าใช้จ่ายจริง

```
compair.com หรือ compair.app  →  ≈ 400–700 บาท/ปี  (≈ 35–60 บาท/เดือน)
compair.in.th                 →  ≈ 300–500 บาท/ปี
tongarclub.github.io (ปัจจุบัน) →  0 บาท/ปี
```

### คุ้มไหมที่จะจ่าย?

| ข้อดี custom domain | ข้อเสีย |
|---|---|
| SEO authority ดีกว่า subdomain มาก | จ่ายต่อปี |
| URL สั้น จำง่าย (`compair.com`) | ต้องตั้ง DNS + อัปเดต canonical/sitemap |
| ดูเป็น brand จริง | ถ้าไม่ต่ออายุ โดเมนหาย |

**สำหรับ ComPair ที่ต้องการ SEO/AEO จริงจัง — คุ้ม** เพราะ GitHub subdomain มี authority ต่ำกว่ามาก

### Registrar ที่แนะนำ

1. **Cloudflare Registrar** — ราคา cost price ไม่ mark up (ต้องใช้ Cloudflare DNS)
2. **Namecheap** — ราคาดี ใช้ง่าย
3. **Ninet / Z.com (ไทย)** — ถ้าต้องการ `.in.th`

---

## 3. Checklist ย้าย Custom Domain (เมื่อพร้อม)

เมื่อได้ domain แล้ว ต้องอัปเดต URL ในทุกไฟล์เหล่านี้พร้อมกัน:

| ไฟล์ | สิ่งที่ต้องแก้ |
|---|---|
| `robots.txt` | `Sitemap:` URL |
| `sitemap.xml` | ทุก `<loc>` |
| `index.html` | `canonical`, `og:url`, JSON-LD `url` |
| `html/ai-calculator.html` | `canonical`, `og:url`, JSON-LD `url`, `isPartOf.url` |
| `html/solar-calculator.html` | `canonical`, `og:url`, JSON-LD `url`, `isPartOf.url` |
| GitHub Pages Settings | Custom domain + Enforce HTTPS |

> **Tip:** ใช้ Find & Replace ใน editor แทนที่ URL เก่าทีเดียวทุกไฟล์

---

## 4. Google Analytics — เช็คจำนวนผู้เข้าเว็บ

### GA4 vs Search Console — ต่างกันยังไง?

| | Google Analytics 4 (GA4) | Google Search Console (GSC) |
|---|---|---|
| **วัดอะไร** | ผู้เข้าเว็บจริงทุกช่องทาง | การแสดงผล/คลิกจาก Google Search เท่านั้น |
| **ตัวเลขหลัก** | Users, Sessions, Page views | Impressions, Clicks, CTR, Average position |
| **รู้ได้ว่า** | คนเข้ากี่คน มาจากไหน ดูหน้าไหน อยู่นานแค่ไหน | คนค้นหาคำไหนแล้วเจอเว็บเรา ติดอันดับเท่าไหร่ |
| **ค่าใช้จ่าย** | ฟรี | ฟรี |
| **ComPair สถานะ** | ❌ ยังไม่ได้ติดตั้ง | ❓ ยังไม่แน่ใจ |

> **ใช้คู่กัน** — GSC บอกว่า SEO ทำงานไหม GA4 บอกว่าคนเข้าเว็บจริงกี่คนและทำอะไรบ้าง

### ลิงก์ที่ใช้

| เครื่องมือ | URL |
|---|---|
| สร้างบัญชี GA4 | https://analytics.google.com |
| คู่มือติดตั้ง gtag | https://support.google.com/analytics/answer/9304153 |
| Search Console | https://search.google.com/search-console |
| Realtime report (ดู live traffic) | GA4 → Reports → Realtime |

---

### ขั้นตอนติดตั้ง GA4 สำหรับ ComPair

#### Step 1 — สร้าง Property
1. ไปที่ https://analytics.google.com → **Admin** (ไอคอนเฟือง)
2. **Create Property** → ตั้งชื่อ `ComPair`
3. เลือก timezone `Asia/Bangkok`, currency `THB`
4. สร้าง **Web Data Stream** → URL: `https://tongarclub.github.io/compair-website/`
5. คัดลอก **Measurement ID** (รูปแบบ `G-XXXXXXXXXX`)

#### Step 2 — ใส่ tracking code ในทุกหน้า HTML

วางใน `<head>` ของทุกไฟล์ (ก่อน `</head>`):

```html
<!-- Google Analytics (GA4) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

ไฟล์ที่ต้องใส่:

| ไฟล์ | หมายเหตุ |
|---|---|
| `index.html` | หน้าแรก |
| `html/ai-calculator.html` | AI Calculator |
| `html/solar-calculator.html` | Solar Calculator |

> แทนที่ `G-XXXXXXXXXX` ด้วย Measurement ID จริงจาก Step 1

#### Step 3 — ยืนยันว่าทำงาน
1. Deploy ขึ้น GitHub Pages
2. เปิดเว็บจริง 1–2 หน้า
3. ไปที่ GA4 → **Reports → Realtime**
4. ควรเห็น **1 active user** ภายใน 30 วินาที

#### Step 4 — เชื่อม GA4 กับ Search Console (แนะนำ)
1. GA4 → **Admin → Product links → Search Console links**
2. Link property กับ GSC ของ ComPair
3. จะดู search query + landing page ใน GA4 ได้ในที่เดียว

---

### Metrics ที่ควรดู (รายสัปดาห์)

#### GA4 — ผู้เข้าเว็บ

| Metric | อยู่ที่ไหน | ความหมาย |
|---|---|---|
| **Users** | Reports → Acquisition → Traffic acquisition | จำนวนคนที่เข้า (ไม่ซ้ำ) |
| **Sessions** | Reports → Engagement → Overview | จำนวนครั้งที่เข้า (รวมคนกลับมา) |
| **Views** | Reports → Engagement → Pages and screens | หน้าไหนถูกดูบ่อย |
| **Avg. engagement time** | Reports → Engagement → Overview | อยู่บนเว็บนานแค่ไหน |
| **Traffic source** | Reports → Acquisition → Traffic acquisition | มาจาก Google / Direct / Social |

#### GSC — SEO Performance

| Metric | อยู่ที่ไหน | ความหมาย |
|---|---|---|
| **Total clicks** | Performance | คลิกจาก Google Search |
| **Total impressions** | Performance | แสดงผลกี่ครั้ง |
| **Average CTR** | Performance | % ที่คลิกเมื่อเห็น |
| **Average position** | Performance | อันดับเฉลี่ย |
| **Top queries** | Performance → Queries | คำค้นหาที่พา traffic มา |

---

### Benchmark ที่คาดหวัง (ComPair ช่วงแรก)

| ช่วงเวลา | Users/เดือน (ประมาณ) | หมายเหตุ |
|---|---|---|
| เดือน 1 | 10–50 | ส่วนใหญ่ direct / จากที่แชร์เอง |
| เดือน 2–3 | 50–200 | เริ่มมี organic จาก long-tail |
| เดือน 6+ | 200–1,000+ | ถ้า SEO + backlink ทำงาน |

> ตัวเลขเป็น estimate — niche tool ภาษาไทย traffic ต่ำกว่าเว็บทั่วไป แต่ conversion intent สูงกว่า

---

### Checklist ติดตั้ง Analytics

```
- [ ] สร้าง GA4 Property + Web Data Stream
- [ ] ใส่ gtag ใน index.html, ai-calculator.html, solar-calculator.html
- [ ] Deploy + ยืนยัน Realtime report มี active user
- [ ] ลงทะเบียน Google Search Console + submit sitemap
- [ ] Link GA4 ↔ Search Console
- [ ] ตั้ง reminder ดู report ทุกสัปดาห์
```

### ข้อควรระวัง (PDPA / Privacy)

- GA4 เก็บ cookie และ IP ( anonymized ) — ถือเป็นข้อมูลส่วนบุคคลตาม PDPA
- สำหรับเว็บ tool ขนาดเล็ก แนะนำเพิ่ม **Privacy Policy** หน้าเดียว ระบุว่าใช้ Google Analytics
- ถ้าไม่ต้องการ cookie banner ตอนนี้ — ใช้ GA4 แบบ **anonymize IP** (default แล้ว) + ไม่เก็บ User-ID

---

## 5. คำถามที่ยังต้องตัดสินใจ

- [ ] ลง **Google Search Console** แล้วหรือยัง?
- [ ] ติดตั้ง **Google Analytics (GA4)** แล้วหรือยัง?
- [ ] เป้าหมายหลักคือ **traffic จาก Google** หรือ **ถูก AI cite**?
- [ ] มีแผนย้ายไป custom domain ไหม? (งบ ≈ 400–700 บาท/ปี)
- [ ] โดเมนที่สนใจ: `compair.com`, `compair.app`, หรือ `compair.in.th`?
