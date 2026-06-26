"""
apply_short_links.py
----------------------------------------------------
อ่าน shopee-urls-to-shorten.txt แล้วอัปเดต JSON files

Format ของ txt:
  --- Batch N/M ---
  https://shopee.co.th/product/...   ← original URL (5 บรรทัด)
  https://shopee.co.th/product/...
  ...

  https://s.shopee.co.th/XXXXX       ← short link ที่ paste ลงมา
  https://s.shopee.co.th/XXXXX
  ...

Usage:
  python3 scripts/apply_short_links.py
"""

import json
import re
import os
from pathlib import Path

TXT_FILE  = Path(__file__).parent.parent / 'data' / 'affiliate' / 'shopee-urls-to-shorten.txt'
DATA_DIR  = Path(__file__).parent.parent / 'data' / 'affiliate'

JSON_FILES = [
    'gpu.json', 'mac.json', 'mac_accessories.json',
    'solar_panel.json', 'solar_inverter.json',
    'ev_charger.json', 'gold_invest.json',
]

# ── โหลด JSON ทั้งหมดเป็น dict: product_link → item ──────────
def load_all_items():
    mapping = {}  # product_link → (data_dict, item_dict, filepath)
    for fname in JSON_FILES:
        fp = DATA_DIR / fname
        if not fp.exists():
            continue
        data = json.loads(fp.read_text(encoding='utf-8'))
        for item in data.get('items', []):
            url = item.get('product_link', '').strip()
            if url:
                mapping[url] = (data, item, fp)
    return mapping

# ── Parse txt: สร้าง list ของ (original_url, short_link) ────
def parse_txt():
    text = TXT_FILE.read_text(encoding='utf-8')
    pairs = []

    # หา block ของ original URLs + short links ที่ user paste แล้ว
    # Pattern: กลุ่ม shopee.co.th/product URLs ตามด้วย กลุ่ม s.shopee.co.th URLs
    block_pattern = re.compile(
        r'((?:https://shopee\.co\.th/\S+\n)+)'   # original URLs
        r'\s*'
        r'((?:https://s\.shopee\.co\.th/\S+\n?)+)',  # short links
        re.MULTILINE
    )

    for match in block_pattern.finditer(text):
        originals  = [u.strip() for u in match.group(1).strip().splitlines() if u.strip()]
        short_urls = [u.strip() for u in match.group(2).strip().splitlines() if u.strip()]

        for orig, short in zip(originals, short_urls):
            pairs.append((orig, short))

    return pairs

# ── Main ─────────────────────────────────────────────────────
def main():
    if not TXT_FILE.exists():
        print(f'❌ ไม่พบไฟล์: {TXT_FILE}')
        return

    mapping = load_all_items()
    pairs   = parse_txt()

    print(f'🔍 พบ {len(pairs)} คู่ URL ใน txt file\n')

    if not pairs:
        print('⚠️  ยังไม่มี short links ใน txt file')
        print('   วิธีใช้: วาง short links ใต้ original URLs ในไฟล์ txt แล้วรัน script นี้ใหม่')
        return

    updated    = 0
    not_found  = 0
    already    = 0

    changed_files = set()

    for orig, short in pairs:
        if orig not in mapping:
            print(f'  ⚠️  ไม่พบใน JSON: {orig}')
            not_found += 1
            continue

        data, item, fp = mapping[orig]

        if item.get('shopee_short_link'):
            already += 1
            continue

        item['shopee_short_link'] = short
        item['affiliate_link']    = short
        changed_files.add(fp)
        updated += 1
        print(f'  ✅ {short}  ←  {orig[-40:]}')

    # ── บันทึกไฟล์ที่เปลี่ยนแปลง ──
    for fp in changed_files:
        data, _, _ = next(v for v in mapping.values() if v[2] == fp)
        fp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'\n💾 Saved: {fp.name}')

    print(f'\n{"═"*50}')
    print(f'✅ Updated  : {updated}')
    print(f'⏭  Already  : {already}')
    print(f'⚠️  Not found: {not_found}')
    print(f'📂 Files saved: {len(changed_files)}')


if __name__ == '__main__':
    main()
