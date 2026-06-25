#!/usr/bin/env python3
"""Generate Level-2 Model pages for ComPair SEO."""
import os, json, math

BASE    = os.path.join(os.path.dirname(__file__), '..')
OUT     = os.path.join(BASE, 'html', 'model')
os.makedirs(OUT, exist_ok=True)

BASE_URL = "https://tongarclub.github.io/compair-website"

data     = json.load(open(os.path.join(BASE, 'data/ai-models/llm-models.json')))
MODELS   = data['models']
GPUS_RAW = json.load(open(os.path.join(BASE, 'data/ai-models/gpus.json')))

# ── GPU data: flatten list or dict ──────────────────────────────────────────
if isinstance(GPUS_RAW, list):
    GPUS_RAW_LIST = GPUS_RAW
elif isinstance(GPUS_RAW, dict):
    GPUS_RAW_LIST = GPUS_RAW.get('gpus', [])
    if not GPUS_RAW_LIST:
        for v in GPUS_RAW.values():
            if isinstance(v, list):
                GPUS_RAW_LIST = v; break

# Normalise field names (vramGB → vram, bandwidthGBs → bandwidth)
GPUS = []
for g in GPUS_RAW_LIST:
    if not isinstance(g, dict):
        continue
    norm = dict(g)
    if 'vramGB' in norm and 'vram' not in norm:
        norm['vram'] = norm['vramGB']
    if 'bandwidthGBs' in norm and 'bandwidth' not in norm:
        norm['bandwidth'] = norm['bandwidthGBs']
    if 'priceTHB' in norm and 'price' not in norm:
        p = norm['priceTHB']
        norm['price'] = f"฿{p}" if p else "—"
    if norm.get('vram') and norm.get('name'):
        GPUS.append(norm)

# ── POPULAR GPU SUBSET shown in comparison table (ordered by VRAM) ────────
POPULAR_GPU_IDS = [
    "4060", "3060", "4070", "4070s", "3080", "4080", "3090", "4090",
    "m2pro", "m3max",
]

def get_popular_gpus():
    found = []
    for gid in POPULAR_GPU_IDS:
        for g in GPUS:
            if str(g.get('id','')) == gid or g.get('slug','') == gid:
                found.append(g)
                break
    # fallback: top 10 by vram if none matched
    if not found:
        found = sorted(GPUS, key=lambda g: g.get('vram', 0), reverse=True)[:10]
    return found

# ── Badge helpers ────────────────────────────────────────────────────────────
def badge_vram(gpu_vram, needed):
    ratio = gpu_vram / needed if needed else 0
    if ratio >= 1.1:
        return f'<span class="badge badge-ok">✓ {gpu_vram} GB</span>'
    elif ratio >= 0.85:
        return f'<span class="badge badge-warn">~ {gpu_vram} GB</span>'
    else:
        return f'<span class="badge badge-no">✗ {gpu_vram} GB</span>'

def best_quant(gpu_vram, model):
    for qk in ('q8', 'q4', 'q3', 'q2'):
        needed = model.get(qk, 999)
        if needed and gpu_vram / needed >= 0.85:
            qlabel = {'q8':'Q8.0','q4':'Q4_K_M','q3':'Q3_K_M','q2':'Q2_K'}[qk]
            return qlabel
    return "ไม่รองรับ"

def tok_speed(gpu, model):
    bw = gpu.get('bandwidth', gpu.get('bw', 0))
    base = model.get('baseTokPerSec', 80)
    if not bw:
        return "—"
    spd = max(1, round(base * bw / 600))
    return f"~{spd} tok/s"

# ── GPU comparison table rows ────────────────────────────────────────────────
def gpu_rows(model):
    pop = get_popular_gpus()
    if not pop:
        # generate from scratch using known data
        return "<tr><td colspan='6' style='padding:20px;color:var(--text3);text-align:center'>ไม่พบข้อมูล GPU</td></tr>"
    rows = []
    for g in sorted(pop, key=lambda x: x.get('vram',0)):
        vram = g.get('vram', 0)
        name = g.get('name', g.get('id','?'))
        bq   = best_quant(vram, model)
        spd  = tok_speed(g, model) if bq != "ไม่รองรับ" else "—"
        rec  = f'<span class="rec-badge">{bq}</span>' if bq != "ไม่รองรับ" else '<span style="color:var(--text3);font-size:12px">ไม่รองรับ</span>'
        q4_b = badge_vram(vram, model.get('q4', 999))
        q8_b = badge_vram(vram, model.get('q8', 999))
        price_str = g.get('price','—')
        slug  = g.get('slug', str(g.get('id','')).lower().replace(' ','-'))
        link  = f'<a href="../gpu/{slug}.html" style="color:var(--gold);text-decoration:none">{name}</a>'
        rows.append(
            f'<tr><td><strong>{link}</strong><div style="font-family:\'DM Mono\',monospace;font-size:9px;color:var(--text3);margin-top:2px">{vram} GB · {g.get("bandwidth",g.get("bw","?"))} GB/s</div></td>'
            f'<td>{q4_b}</td><td>{q8_b}</td><td>{rec}</td>'
            f'<td style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--text2)">{spd}</td>'
            f'<td style="font-size:12px;color:var(--text3)">{price_str}</td></tr>'
        )
    return "\n".join(rows) if rows else "<tr><td colspan='6' style='padding:20px;text-align:center;color:var(--text3)'>ไม่พบข้อมูล GPU ยอดนิยม</td></tr>"

# ── Minimum VRAM section ─────────────────────────────────────────────────────
def min_vram_list(model):
    items = []
    for qk, ql in [('q4','Q4_K_M ⭐ แนะนำ'), ('q8','Q8.0'), ('q3','Q3_K_M'), ('q2','Q2_K')]:
        gb = model.get(qk)
        if gb:
            items.append(f'<div style="display:flex;align-items:center;gap:16px;padding:12px 0;border-bottom:1px solid var(--border)"><div style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--gold);width:110px">{ql}</div><div style="font-size:22px;font-weight:600;color:var(--text);width:80px">{gb} <span style="font-size:13px;font-weight:400;color:var(--text3)">GB</span></div><div style="font-size:12px;color:var(--text2)">{"คุณภาพ ~97% ของ FP16 — ดีที่สุดสำหรับ VRAM จำกัด" if qk=="q4" else "คุณภาพ ~99% — ใกล้เคียง FP16 มากที่สุด" if qk=="q8" else "คุณภาพ ~91% — ประหยัด VRAM สำหรับ GPU เล็ก" if qk=="q3" else "คุณภาพ ~80% — ประหยัด VRAM สูงสุด รับได้สำหรับงาน chat"}</div></div>')
    return "\n".join(items)

# ── FAQ JSON-LD ───────────────────────────────────────────────────────────────
def faqs(m):
    name = m['name']
    dev  = m['developer']
    q4   = m.get('q4', 4.1)
    q8   = m.get('q8', 7.2)
    cmd  = m.get('ollama_cmd','ollama pull model')
    ctx  = m.get('context', 4096)
    ctx_k = f"{ctx//1000}K" if ctx >= 1000 else str(ctx)

    return f"""{{
      "@type": "Question",
      "name": "{name} ต้องการ GPU VRAM เท่าไหร่?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{name} จาก {dev} ต้องการ VRAM อย่างน้อย {q4} GB สำหรับ Q4_K_M (แนะนำ) หรือ {q8} GB สำหรับ Q8.0 GPU ยอดนิยมที่รันได้คือ RTX 4060 8GB (Q4), RTX 4070 12GB (Q8) ขึ้นไป"
      }}
    }},
    {{
      "@type": "Question",
      "name": "รัน {name} บน PC ทั่วไปได้ไหม?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "ได้ครับ {name} รันได้บน PC ที่มี GPU VRAM {q4} GB ขึ้นไป ใช้ Ollama ด้วยคำสั่ง '{cmd}' หรือ LM Studio สำหรับ GUI รัน context window ได้สูงสุด {ctx_k} tokens"
      }}
    }},
    {{
      "@type": "Question",
      "name": "{name} Q4 กับ Q8 ต่างกันยังไง?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "Q4_K_M ใช้ {q4} GB VRAM คุณภาพ ~97% ของ FP16 เหมาะสำหรับ GPU VRAM 8-12 GB ส่วน Q8.0 ใช้ {q8} GB VRAM คุณภาพ ~99% เหมาะสำหรับ GPU 12 GB ขึ้นไป สำหรับงาน chat ทั่วไป Q4_K_M เพียงพอและเร็วกว่า Q8"
      }}
    }}"""

# ── Related model cards ───────────────────────────────────────────────────────
def related_models(current_slug):
    others = [m for m in MODELS if m['slug'] != current_slug]
    cards  = []
    for m in others:
        cards.append(
            f'<a href="{m["slug"]}.html" class="related-card">'
            f'<div class="rc-name">{m["name"]}</div>'
            f'<div class="rc-vram">{m["developer"]} · {m.get("paramB","?")}B</div>'
            f'<div class="rc-arrow">ดูรายละเอียด →</div></a>'
        )
    return "\n".join(cards)

# ── Main HTML generator ───────────────────────────────────────────────────────
def generate(m):
    slug  = m['slug']
    name  = m['name']
    dev   = m['developer']
    desc  = f"ตรวจสอบว่า {name} จาก {dev} ต้องการ GPU VRAM เท่าไหร่ — ตาราง compatibility ทุก GPU พร้อม Quantization แนะนำ Q2–Q8 และ Token/s โดยประมาณ"
    url   = f"{BASE_URL}/html/model/{slug}.html"
    ctx_k = f"{m.get('context',4096)//1000}K" if m.get('context',4096) >= 1000 else str(m.get('context',4096))

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
<title>{name} ต้องการ GPU อะไร — VRAM {m.get('q4','?')} GB+ | ComPair</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{name} ต้องการ GPU อะไร — VRAM Guide | ComPair">
<meta property="og:description" content="{desc}">
<meta property="og:locale" content="th_TH">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "{name} GPU Requirements Guide",
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
    {faqs(m)}
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
    <div class="hero-label">{dev} · {m.get('family', name)} · {m.get('license','Open')}</div>
    <h1>รัน <em>{name}</em><br>ต้องการ GPU อะไร?</h1>
    <p class="hero-desc">{m['description']}</p>
    <div class="hero-meta">
      <span class="hero-chip gold">Q4_K_M: {m.get('q4','?')} GB</span>
      <span class="hero-chip gold">Q8.0: {m.get('q8','?')} GB</span>
      <span class="hero-chip">{m.get('paramB','?')}B Parameters</span>
      <span class="hero-chip">Context {ctx_k}</span>
      <span class="hero-chip">{m.get('usecase','—')}</span>
    </div>
    <a href="../ai-calculator.html" class="cta-link">เปิด GPU Calculator →</a>
  </div>
</div>

<div class="wrap">
  <div class="spec-bar">
    <div class="sb-cell">
      <div class="sb-lbl">VRAM ขั้นต่ำ (Q4)</div>
      <div class="sb-val gold">{m.get('q4','?')} GB</div>
      <div class="sb-sub">Q4_K_M แนะนำ</div>
    </div>
    <div class="sb-cell">
      <div class="sb-lbl">VRAM คุณภาพสูง (Q8)</div>
      <div class="sb-val">{m.get('q8','?')} GB</div>
      <div class="sb-sub">Q8.0 ≈ FP16</div>
    </div>
    <div class="sb-cell">
      <div class="sb-lbl">Parameters</div>
      <div class="sb-val" style="font-size:14px">{m.get('paramB','?')}B</div>
      <div class="sb-sub">{m.get('family', name)}</div>
    </div>
    <div class="sb-cell">
      <div class="sb-lbl">Context Window</div>
      <div class="sb-val" style="color:var(--blue)">{ctx_k}</div>
      <div class="sb-sub">Max tokens</div>
    </div>
    <div class="sb-cell">
      <div class="sb-lbl">RAM ขั้นต่ำ</div>
      <div class="sb-val" style="font-size:14px">{m.get('minRamGB','16')} GB</div>
      <div class="sb-sub">System RAM</div>
    </div>
  </div>
</div>

<div class="wrap">
  <div class="section">
    <div class="section-head">
      <div class="section-title">VRAM ที่ต้องการแต่ละ Quantization</div>
      <div class="section-sub">Q4_K_M แนะนำสำหรับ GPU ทั่วไป · Q8.0 สำหรับ GPU 12 GB+ ที่ต้องการคุณภาพสูง</div>
    </div>
    <div style="padding:20px 28px">
      {min_vram_list(m)}
    </div>
  </div>
</div>

<div class="wrap">
  <div class="section">
    <div class="section-head">
      <div class="section-title">GPU ที่รัน {name} ได้ — เปรียบเทียบ</div>
      <div class="section-sub">เรียงตาม VRAM น้อยไปมาก · ✓ รันได้สบาย · ~ รันได้แต่ตึง · ✗ VRAM ไม่พอ</div>
    </div>
    <table class="compat">
      <thead>
        <tr>
          <th>GPU</th>
          <th>Q4_K_M</th>
          <th>Q8.0</th>
          <th>แนะนำ</th>
          <th>ความเร็ว</th>
          <th>ราคาโดยประมาณ</th>
        </tr>
      </thead>
      <tbody>
        {gpu_rows(m)}
      </tbody>
    </table>
  </div>
</div>

<div class="wrap">
  <div class="divider"><div class="div-line"></div><div class="div-label">วิธีรัน {name} บน PC</div><div class="div-line"></div></div>
  <div class="section">
    <div class="tips-grid">
      <div class="tip">
        <div class="tip-num">01</div>
        <div class="tip-title">ติดตั้ง Ollama (ง่ายที่สุด)</div>
        <div class="tip-text">ดาวน์โหลด Ollama จาก ollama.com แล้วรัน <code>{m.get('ollama_cmd','ollama pull model')}</code> — detect GPU อัตโนมัติ รองรับทั้ง NVIDIA CUDA และ Apple Silicon Metal</div>
      </div>
      <div class="tip">
        <div class="tip-num">02</div>
        <div class="tip-title">ใช้ LM Studio (มี GUI)</div>
        <div class="tip-text">LM Studio รองรับ {name} เลือก Quantization ได้ผ่าน UI ดาวน์โหลดจาก HuggingFace ในแอปได้เลย เหมาะกับผู้ที่ไม่ถนัด command line</div>
      </div>
      <div class="tip">
        <div class="tip-num">03</div>
        <div class="tip-title">Context Window {ctx_k}</div>
        <div class="tip-text">{name} รองรับ context สูงสุด {ctx_k} tokens แต่ context ที่ยาวขึ้นใช้ VRAM เพิ่ม ถ้า VRAM ตึงให้ตั้ง <code>--ctx-size 4096</code> ใน llama.cpp เพื่อลด VRAM ใช้งาน</div>
      </div>
    </div>
  </div>
</div>

<div class="wrap">
  <div class="divider"><div class="div-line"></div><div class="div-label">Model อื่นที่น่าสนใจ</div><div class="div-line"></div></div>
  <div class="related-grid">
    {related_models(slug)}
  </div>
</div>

<footer>
  <div class="wrap">
    <div class="footer-inner">
      <div class="footer-logo">ComPair — {name} GPU Guide</div>
      <div class="footer-meta">ข้อมูลอ้างอิงจาก {m.get('hf_url','HuggingFace')} · llama.cpp · 2025–2026</div>
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
    print(f"  Created: html/model/{slug}.html ({len(html.splitlines())} lines)")

if __name__ == '__main__':
    print("Generating Model pages...")
    for m in MODELS:
        generate(m)
    print(f"\nDone! {len(MODELS)} pages in html/model/")
    print("\nSitemap entries to add:")
    for m in MODELS:
        print(f"  {BASE_URL}/html/model/{m['slug']}.html")
