#!/usr/bin/env python3
"""Generate static GPU pages for ComPair SEO."""
import os, math

BASE = os.path.join(os.path.dirname(__file__), '..')
OUT  = os.path.join(BASE, 'html', 'gpu')
os.makedirs(OUT, exist_ok=True)

BASE_URL = "https://tongarclub.github.io/compair-website"

GPUS = [
    # NVIDIA RTX 50 Series (Blackwell)
    dict(id="5090",     slug="rtx-5090",          name="RTX 5090",          vram=32, bw=1792, perf=10, price="฿85,000–110,000", arch="Blackwell",     gen="NVIDIA RTX 50 Series"),
    dict(id="5080",     slug="rtx-5080",          name="RTX 5080",          vram=16, bw=960,  perf=9,  price="฿45,000–62,000",  arch="Blackwell",     gen="NVIDIA RTX 50 Series"),
    dict(id="5070ti",   slug="rtx-5070-ti",       name="RTX 5070 Ti",       vram=16, bw=896,  perf=8,  price="฿28,000–38,000",  arch="Blackwell",     gen="NVIDIA RTX 50 Series"),
    dict(id="5070",     slug="rtx-5070",          name="RTX 5070",          vram=12, bw=672,  perf=7,  price="฿20,000–28,000",  arch="Blackwell",     gen="NVIDIA RTX 50 Series"),
    dict(id="5060ti",   slug="rtx-5060-ti-16gb",  name="RTX 5060 Ti 16GB",  vram=16, bw=448,  perf=6,  price="฿18,000–26,000",  arch="Blackwell",     gen="NVIDIA RTX 50 Series"),
    # NVIDIA RTX 40 Series (Ada Lovelace)
    dict(id="4060",     slug="rtx-4060",          name="RTX 4060",          vram=8,  bw=272,  perf=4,  price="฿9,000–13,000",   arch="Ada Lovelace",  gen="NVIDIA RTX 40 Series"),
    dict(id="4070",     slug="rtx-4070",          name="RTX 4070",          vram=12, bw=504,  perf=6,  price="฿16,000–22,000",  arch="Ada Lovelace",  gen="NVIDIA RTX 40 Series"),
    dict(id="4090",     slug="rtx-4090",          name="RTX 4090",          vram=24, bw=1008, perf=10, price="฿55,000–70,000",  arch="Ada Lovelace",  gen="NVIDIA RTX 40 Series"),
    dict(id="4080",     slug="rtx-4080",          name="RTX 4080",          vram=16, bw=717,  perf=8,  price="฿30,000–40,000",  arch="Ada Lovelace",  gen="NVIDIA RTX 40 Series"),
    dict(id="4070s",    slug="rtx-4070-super",    name="RTX 4070 Super",    vram=12, bw=504,  perf=6,  price="฿18,000–24,000",  arch="Ada Lovelace",  gen="NVIDIA RTX 40 Series"),
    dict(id="4060ti16", slug="rtx-4060-ti-16gb",  name="RTX 4060 Ti 16GB",  vram=16, bw=288,  perf=5,  price="฿15,000–20,000",  arch="Ada Lovelace",  gen="NVIDIA RTX 40 Series"),
    # NVIDIA RTX 30 Series (Ampere)
    dict(id="3080",     slug="rtx-3080",          name="RTX 3080 10GB",     vram=10, bw=760,  perf=7,  price="฿12,000–18,000",  arch="Ampere",        gen="NVIDIA RTX 30 Series"),
    dict(id="3060",     slug="rtx-3060-12gb",     name="RTX 3060 12GB",     vram=12, bw=360,  perf=5,  price="฿7,000–11,000",   arch="Ampere",        gen="NVIDIA RTX 30 Series"),
    dict(id="3090",     slug="rtx-3090",          name="RTX 3090",          vram=24, bw=936,  perf=8,  price="฿18,000–26,000",  arch="Ampere",        gen="NVIDIA RTX 30 Series"),
    dict(id="3070",     slug="rtx-3070",          name="RTX 3070",          vram=8,  bw=448,  perf=6,  price="฿9,000–13,000",   arch="Ampere",        gen="NVIDIA RTX 30 Series"),
]

MODELS = [
    dict(id="1b",  name="1–3B",   ex="Phi-3-mini · Gemma-2B · TinyLlama",          q8=2.0, q4=1.5, q3=1.2, q2=0.9, spd=180),
    dict(id="7b",  name="7B",     ex="Llama-3.1-8B · Mistral-7B · Qwen2-7B",       q8=7.2, q4=4.1, q3=3.1, q2=2.4, spd=80),
    dict(id="13b", name="13B",    ex="Llama-2-13B · CodeLlama-13B · Vicuna-13B",   q8=14,  q4=7.9, q3=5.9, q2=4.5, spd=40),
    dict(id="30b", name="30–34B", ex="Yi-34B · CodeLlama-34B · Mixtral-8x7B",      q8=34,  q4=19,  q3=15,  q2=11,  spd=18),
    dict(id="70b", name="70B",    ex="Llama-3.1-70B · Qwen2-72B · DeepSeek-V2",    q8=70,  q4=40,  q3=30,  q2=22,  spd=9),
]

QUANTS = [("q8","Q8.0"), ("q4","Q4_K_M"), ("q3","Q3_K_M"), ("q2","Q2_K")]

def badge(vram, needed):
    ratio = vram / needed
    if ratio >= 1.1:
        return f'<span class="badge badge-ok">✓ {needed} GB</span>'
    elif ratio >= 0.85:
        return f'<span class="badge badge-warn">~ {needed} GB</span>'
    else:
        return f'<span class="badge badge-no">✗ {needed} GB</span>'

def best_quant(vram, model):
    for qk, ql in QUANTS:
        needed = model[qk]
        if vram / needed >= 0.85:
            return ql
    return "ไม่รองรับ"

def tok_str(bw, model_spd):
    spd = max(1, round(model_spd * bw / 600))
    return f"~{spd} tok/s"

def ai_score(gpu):
    return min(100, round((gpu['perf'] / 10) * 60 + min(gpu['vram'], 24) / 24 * 40))

def compat_rows(gpu):
    rows = []
    for m in MODELS:
        bq = best_quant(gpu['vram'], m)
        spd = tok_str(gpu['bw'], m['spd']) if bq != "ไม่รองรับ" else "—"
        recs = '<span class="rec-badge">' + bq + '</span>' if bq != "ไม่รองรับ" else '<span style="color:var(--text3);font-size:12px">ไม่รองรับ</span>'
        cells = "".join(f"<td>{badge(gpu['vram'], m[qk])}</td>" for qk, ql in QUANTS)
        rows.append(f'<tr><td><strong>{m["name"]}</strong><div style="font-family:\'DM Mono\',monospace;font-size:9px;color:var(--text3);margin-top:2px">{m["ex"]}</div></td>{cells}<td>{recs}</td><td style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--text2)">{spd}</td></tr>')
    return "\n".join(rows)

def tier_desc(gpu):
    v = gpu['vram']
    if v <= 8:   return f"{gpu['name']} มี VRAM {v} GB — รัน 7B ได้ดีด้วย Q4_K_M รัน 13B ได้บางส่วน ไม่รองรับ 30B+ แต่เหมาะกับผู้เริ่มต้นและงบประมาณจำกัด"
    elif v <= 12: return f"{gpu['name']} มี VRAM {v} GB — รัน 7B ทุก Quantization ได้ รัน 13B ด้วย Q4_K_M ได้สบาย ถือเป็น Sweet Spot สำหรับ Local LLM"
    elif v <= 16: return f"{gpu['name']} มี VRAM {v} GB — รัน 13B ทุก Quantization ได้ รัน 30B บาง Quantization ได้ เหมาะกับงาน Dev และ Research ระดับกลาง"
    else:        return f"{gpu['name']} มี VRAM {v} GB — รัน 7B/13B/30B ได้ทุก Quantization รัน 70B บาง Quantization ได้ เหมาะกับ Researcher ที่ต้องการ model ขนาดใหญ่"

def faqs(gpu):
    v, name, bw = gpu['vram'], gpu['name'], gpu['bw']
    spd_7b = max(1, round(80 * bw / 600))

    q1 = f"{name} รัน Llama 3 8B ได้ไหม?"
    a1 = f"{'ได้' if v >= 4.1 else 'ไม่ได้'}ครับ {name} มี VRAM {v} GB {'รัน Llama 3 8B ด้วย Q4_K_M ได้ ใช้ VRAM ประมาณ 4.1 GB ความเร็วประมาณ ' + str(spd_7b) + ' tok/s' if v >= 4.1 else 'VRAM ไม่พอสำหรับ 7B แม้ Q4_K_M ต้องการ 4.1 GB'}"

    if v >= 8:
        q2 = f"{name} รัน 13B model ได้ไหม?"
        a2 = f"{'ได้ด้วย Q4_K_M (7.9 GB) ' if v >= 7.9 else 'ได้บางส่วน '}ครับ {name} VRAM {v} GB {'รัน 13B ด้วย Q4_K_M ได้ และ Q3_K_M ด้วย' if v >= 7.9 else 'รัน 13B ได้เฉพาะ Q3_K_M (5.9 GB) และ Q2_K (4.5 GB)'} ไม่รองรับ Q8 (14 GB)"
    else:
        q2 = f"{name} ต้องอัปเกรดไหมสำหรับ LLM?"
        a2 = f"{name} VRAM {v} GB เหมาะกับ 7B model เป็นหลัก ถ้าต้องการรัน 13B+ แนะนำอัปเกรดเป็น RTX 4070 12GB หรือ RTX 3060 12GB เพื่อเพิ่ม headroom"

    if v >= 24:
        q3 = f"{name} รัน 70B model ได้ไหม?"
        a3 = f"ได้บางส่วนครับ {name} VRAM {v} GB รัน 70B ด้วย Q2_K (22 GB) ได้ในโหมด borderline แต่ Q4_K_M (40 GB) ไม่พอ แนะนำใช้ GPU+CPU Offload กับ RAM 128 GB+ สำหรับ 70B แบบ Q4"
    elif v >= 12:
        q3 = f"เทียบ {name} กับ RTX 4090 สำหรับ LLM?"
        a3 = f"RTX 4090 (24 GB, 1008 GB/s) เร็วกว่าและรัน model ขนาดใหญ่กว่าได้ แต่ {name} ({v} GB, {bw} GB/s) ราคาถูกกว่ามากและรัน 7B–13B ได้ดี ถ้างบจำกัดและใช้ model ไม่เกิน 13B {name} คุ้มค่ากว่า"
    else:
        q3 = f"{name} ใช้ Ollama หรือ LM Studio ได้ไหม?"
        a3 = f"ได้ทั้งคู่ครับ Ollama รองรับ CUDA บน {name} ได้เลย ติดตั้งง่ายด้วย 'ollama pull llama3' และ LM Studio มี GUI ที่ใช้งานง่าย แนะนำเลือก model ขนาดไม่เกิน 7B สำหรับ VRAM {v} GB"

    return f"""{{
      "@type": "Question",
      "name": "{q1}",
      "acceptedAnswer": {{ "@type": "Answer", "text": "{a1}" }}
    }},
    {{
      "@type": "Question",
      "name": "{q2}",
      "acceptedAnswer": {{ "@type": "Answer", "text": "{a2}" }}
    }},
    {{
      "@type": "Question",
      "name": "{q3}",
      "acceptedAnswer": {{ "@type": "Answer", "text": "{a3}" }}
    }}"""

def related_cards(current_slug):
    others = [g for g in GPUS if g['slug'] != current_slug][:9]
    cards = []
    for g in others:
        cards.append(f'<a href="{g["slug"]}.html" class="related-card"><div class="rc-name">{g["name"]}</div><div class="rc-vram">{g["vram"]} GB · {g["bw"]} GB/s</div><div class="rc-arrow">ดูรายละเอียด →</div></a>')
    return "\n".join(cards)

def generate(gpu):
    name   = gpu['name']
    slug   = gpu['slug']
    vram   = gpu['vram']
    bw     = gpu['bw']
    price  = gpu['price']
    arch   = gpu['arch']
    score  = ai_score(gpu)
    url    = f"{BASE_URL}/html/gpu/{slug}.html"
    spd_7b = max(1, round(80 * bw / 600))

    desc = f"ตรวจสอบว่า {name} ({vram} GB VRAM) รัน Local LLM ขนาดใดได้บ้าง — ผล Quantization ทุกระดับ Q2–Q8 พร้อมตาราง compatibility และ Token/s โดยประมาณ"

    html = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-J3C1X16FZ5"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-J3C1X16FZ5');
</script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} รัน Local LLM ได้ไหม — VRAM {vram} GB | ComPair</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{name} รัน LLM ได้ไหม — VRAM {vram} GB | ComPair">
<meta property="og:description" content="{desc}">
<meta property="og:locale" content="th_TH">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "{name} รัน Local LLM ได้ไหม",
  "url": "{url}",
  "description": "{desc}",
  "inLanguage": "th",
  "isPartOf": {{ "@type": "WebSite", "url": "{BASE_URL}/" }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {faqs(gpu)}
  ]
}}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../css/gpu-page.css">
</head>
<body>

<nav>
  <div class="wrap nav-inner">
    <a href="../../index.html" class="logo">
      <div class="logo-mark">C</div>
      <div><div class="logo-text">ComPair</div><div class="logo-sub">Comparison Engine</div></div>
    </a>
    <div class="nav-right">
      <a class="nav-link" href="../ai-calculator.html">GPU Calculator</a>
      <a class="nav-link" href="../mac-llm-calculator.html">Mac / Apple Silicon</a>
      <a class="nav-link" href="../../index.html">หน้าแรก</a>
    </div>
  </div>
</nav>

<div class="wrap">
  <div class="hero fade-up">
    <div class="hero-label">NVIDIA · {arch} · {gpu['gen']}</div>
    <h1><em>{name}</em><br>รัน LLM ได้ไหน?</h1>
    <p class="hero-desc">{tier_desc(gpu)}</p>
    <div class="hero-meta">
      <span class="hero-chip gold">{vram} GB VRAM</span>
      <span class="hero-chip">{bw} GB/s Bandwidth</span>
      <span class="hero-chip">{arch}</span>
      <span class="hero-chip">CUDA ✓</span>
      <span class="hero-chip">{price}</span>
      <span class="hero-chip">AI Score {score}/100</span>
    </div>
    <a href="../ai-calculator.html#gpu={gpu['id']}" class="cta-link">เปิด Calculator พร้อม {name} →</a>
  </div>
</div>

<div class="wrap">
  <div class="spec-bar">
    <div class="sb-cell"><div class="sb-lbl">VRAM</div><div class="sb-val gold">{vram} GB</div><div class="sb-sub">Video RAM</div></div>
    <div class="sb-cell"><div class="sb-lbl">Bandwidth</div><div class="sb-val">{bw} <span style="font-size:12px;font-weight:400;color:var(--text3)">GB/s</span></div><div class="sb-sub">Memory Bandwidth</div></div>
    <div class="sb-cell"><div class="sb-lbl">Architecture</div><div class="sb-val" style="font-size:14px">{arch}</div><div class="sb-sub">{gpu['gen']}</div></div>
    <div class="sb-cell"><div class="sb-lbl">7B tok/s (Q4)</div><div class="sb-val" style="color:var(--blue)">~{spd_7b}</div><div class="sb-sub">Token per second</div></div>
    <div class="sb-cell"><div class="sb-lbl">ราคาโดยประมาณ</div><div class="sb-val" style="font-size:13px">{price}</div><div class="sb-sub">ตลาดไทย</div></div>
  </div>
</div>

<div class="wrap">
  <div class="section">
    <div class="section-head">
      <div class="section-title">ตาราง LLM Compatibility — {name}</div>
      <div class="section-sub">VRAM ที่ใช้งานได้จริง: {vram} GB · ✓ รันได้ · ~ รันได้แต่ตึง · ✗ VRAM ไม่พอ</div>
    </div>
    <table class="compat">
      <thead>
        <tr>
          <th>Model Size</th>
          <th>Q8.0</th>
          <th>Q4_K_M ⭐</th>
          <th>Q3_K_M</th>
          <th>Q2_K</th>
          <th>แนะนำ</th>
          <th>ความเร็ว</th>
        </tr>
      </thead>
      <tbody>
        {compat_rows(gpu)}
      </tbody>
    </table>
  </div>
</div>

<div class="wrap">
  <div class="divider"><div class="div-line"></div><div class="div-label">Tips สำหรับ {name}</div><div class="div-line"></div></div>
  <div class="section">
    <div class="tips-grid">
      <div class="tip">
        <div class="tip-num">01</div>
        <div class="tip-title">{'Q4_K_M คือ Sweet Spot' if vram <= 12 else 'Q8.0 ให้คุณภาพดีกว่า'}</div>
        <div class="tip-text">{'สำหรับ ' + name + ' VRAM ' + str(vram) + ' GB แนะนำ Q4_K_M เป็นหลัก — คุณภาพ ~97% ของ FP16 แต่ใช้ VRAM น้อยกว่าครึ่งหนึ่ง' if vram <= 12 else 'VRAM ' + str(vram) + ' GB ของ ' + name + ' เพียงพอรัน 7B และ 13B ด้วย Q8.0 ซึ่งให้คุณภาพ ~99% ของ FP16 ดีกว่า Q4 พอสังเกตได้'}</div>
      </div>
      <div class="tip">
        <div class="tip-num">02</div>
        <div class="tip-title">CUDA Acceleration</div>
        <div class="tip-text">{name} รองรับ CUDA ซึ่ง llama.cpp ใช้งานได้เต็มประสิทธิภาพ ติดตั้ง Ollama หรือ LM Studio แล้วใช้ได้เลย — ระบบ detect GPU อัตโนมัติ</div>
      </div>
      <div class="tip">
        <div class="tip-num">03</div>
        <div class="tip-title">{'GPU+CPU Split สำหรับ model ใหญ่' if vram <= 12 else 'Context Window ควบคุมได้'}</div>
        <div class="tip-text">{'ถ้า VRAM ไม่พอรัน 13B+ ใช้ ' + '<code>--n-gpu-layers 20</code>' + ' ใน llama.cpp เพื่อ Offload บางส่วนไป RAM — ต้องการ RAM 32 GB+' if vram <= 12 else 'Context ใหญ่ขึ้นใช้ VRAM เพิ่ม Context 4K ≈ +0.5 GB, 8K ≈ +1 GB, 32K ≈ +4 GB ถ้า VRAM ตึงให้ลด Context ด้วย ' + '<code>--ctx-size 4096</code>'}</div>
      </div>
    </div>
  </div>
</div>

<div class="wrap">
  <div class="divider"><div class="div-line"></div><div class="div-label">GPU อื่นที่น่าสนใจ</div><div class="div-line"></div></div>
  <div class="related-grid">
    {related_cards(slug)}
  </div>
</div>

<footer>
  <div class="wrap">
    <div class="footer-inner">
      <div class="footer-logo">ComPair — {name} LLM Guide</div>
      <div class="footer-meta">ข้อมูลอ้างอิงจาก llama.cpp · HuggingFace · 2025–2026</div>
      <div class="footer-links">
        <a href="../../index.html">หน้าแรก</a>
        <a href="../ai-calculator.html">GPU Calculator</a>
        <a href="../mac-llm-calculator.html">Mac / Apple Silicon</a>
      </div>
    </div>
  </div>
</footer>

</body>
</html>"""
    out_path = os.path.join(OUT, f"{slug}.html")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Created: html/gpu/{slug}.html ({len(html.splitlines())} lines)")

if __name__ == '__main__':
    print("Generating GPU pages...")
    for gpu in GPUS:
        generate(gpu)
    print(f"\nDone! {len(GPUS)} pages created in html/gpu/")
    slugs = [g['slug'] for g in GPUS]
    print("\nSitemap entries to add:")
    for s in slugs:
        print(f"  {BASE_URL}/html/gpu/{s}.html")
