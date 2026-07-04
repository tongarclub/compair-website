#!/usr/bin/env python3
"""
import_picks.py — นำเข้าข้อมูล affiliate จาก picks.xlsx → manual-picks.json

picks.xlsx คือ Source of Truth:
  - แก้ไขใน sheet "Picks" แล้วรัน script นี้
  - ทุก section ที่ปรากฏใน Excel จะถูก replace ใน JSON
  - section อื่นที่ไม่ได้ระบุ → ไม่ถูกแตะ

Usage:
    python3 scripts/import_picks.py                    # ใช้ picks.xlsx default
    python3 scripts/import_picks.py path/to/file.xlsx  # ระบุไฟล์เอง
    python3 scripts/import_picks.py --dry-run          # preview ไม่บันทึก
    python3 scripts/import_picks.py --section mac_llm  # import แค่ section เดียว

Excel Columns (sheet "Picks"):
    section         key ใน manual-picks.json (ai_calculator, mac_llm, ...)
    type            item | guide
    ids             id คั่นด้วย | เช่น r9_7950x|r9_7900x  (items + filterId)
    title           ชื่อสินค้า (items) / ชื่อสินค้าใน guide column (guides)
    price           ราคา (ตัวเลข)
    original_price  ราคาก่อนลด (optional, items)
    link            affiliate URL
    image           URL รูปสินค้า (optional, items)
    source          Shopee | Lazada | ฯลฯ (optional, items)
    badge           ป้าย: ขายดี | แนะนำ | ราคาดี (optional, items)
    row             row index 0-based (guides)
    hint            คำอธิบายสั้น (optional, guides)
"""

import json
import sys
import argparse
from pathlib import Path

try:
    from openpyxl import load_workbook
except ImportError:
    print('❌ ต้องติดตั้ง openpyxl: pip3 install openpyxl --break-system-packages')
    sys.exit(1)

REPO_ROOT   = Path(__file__).parent.parent
PICKS_JSON  = REPO_ROOT / 'data' / 'affiliate' / 'manual-picks.json'
DEFAULT_XLS = REPO_ROOT / 'data' / 'affiliate' / 'picks.xlsx'

EXPECTED_HEADERS = [
    'section', 'type', 'ids', 'title',
    'price', 'original_price', 'link', 'image',
    'source', 'badge', 'shop_name', 'item_sold', 'row', 'hint',
]

# ─── helpers ──────────────────────────────────────────────────────────────────

def _str(v) -> str:
    return '' if v is None else str(v).strip()

def _price(raw) -> int | float | None:
    s = _str(raw).replace(',', '')
    if not s:
        return None
    try:
        v = float(s)
        return int(v) if v == int(v) else v
    except (ValueError, TypeError):
        return None

def _ids(raw: str) -> list:
    return [i.strip() for i in _str(raw).split('|') if i.strip()]

def _build_item(row: dict) -> dict | None:
    title = _str(row.get('title'))
    link  = _str(row.get('link'))
    price = _price(row.get('price'))
    if not title or not link or price is None:
        return None

    item: dict = {'title': title, 'price': price, 'link': link}

    op = _price(row.get('original_price'))
    if op is not None and op > price:
        item['original_price'] = op

    for field in ('image', 'source', 'badge', 'shop_name'):
        v = _str(row.get(field))
        if v:
            item[field] = v

    sold = _price(row.get('item_sold'))
    if sold is not None and sold > 0:
        item['item_sold'] = int(sold)

    ids = _ids(_str(row.get('ids', '')))
    if ids:
        item['ids'] = ids

    return item

def _build_guide(row: dict) -> dict | None:
    name  = _str(row.get('title'))
    link  = _str(row.get('link'))
    price = _price(row.get('price'))
    try:
        r = int(float(_str(row.get('row', ''))))
    except (ValueError, TypeError):
        return None
    if not name or not link:
        return None

    guide: dict = {'row': r, 'name': name, 'link': link}
    if price is not None:
        guide['price'] = price
    hint = _str(row.get('hint'))
    if hint:
        guide['hint'] = hint
    return guide

# ─── reader ───────────────────────────────────────────────────────────────────

def read_xlsx(path: Path) -> list[dict]:
    wb = load_workbook(path, data_only=True)
    ws = wb['Picks'] if 'Picks' in wb.sheetnames else wb.active

    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []

    header = [_str(h) for h in rows[0]]

    missing = [h for h in EXPECTED_HEADERS if h not in header]
    if missing:
        print(f'⚠ columns ที่หายไปใน Excel: {missing}')

    result = []
    for data_row in rows[1:]:
        row_dict = {header[i]: data_row[i] for i in range(min(len(header), len(data_row)))}
        if not any(_str(v) for v in row_dict.values()):
            continue
        result.append(row_dict)

    return result

# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='นำเข้า affiliate picks จาก picks.xlsx → manual-picks.json'
    )
    parser.add_argument('input_file', nargs='?', default=str(DEFAULT_XLS),
                        help='path ไปยัง .xlsx (default: data/affiliate/picks.xlsx)')
    parser.add_argument('--dry-run', action='store_true',
                        help='แสดงผลลัพธ์โดยไม่บันทึก JSON')
    parser.add_argument('--section', metavar='KEY',
                        help='import เฉพาะ section นี้เท่านั้น')
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f'❌ ไม่พบไฟล์: {input_path}')
        print(f'   สร้าง template ใหม่ได้ด้วย: python3 scripts/create_picks_xlsx.py')
        sys.exit(1)

    raw_rows = read_xlsx(input_path)
    print(f'📂 อ่าน {input_path.name} ({len(raw_rows)} แถว)')

    with open(PICKS_JSON, 'r', encoding='utf-8') as f:
        picks = json.load(f)

    collected_items: dict[str, list] = {}
    collected_guide: dict[str, list] = {}
    errors = []

    for lineno, row in enumerate(raw_rows, start=2):
        section = _str(row.get('section'))
        rtype   = _str(row.get('type', 'item')).lower()

        if not section:
            continue
        if args.section and section != args.section:
            continue

        if rtype == 'guide':
            obj = _build_guide(row)
            if obj:
                collected_guide.setdefault(section, []).append(obj)
            else:
                errors.append(f'  ⚠ แถว {lineno} [guide/{section}]: ข้อมูลไม่ครบ (title/link/row required)')
        else:
            obj = _build_item(row)
            if obj:
                collected_items.setdefault(section, []).append(obj)
            else:
                errors.append(f'  ⚠ แถว {lineno} [item/{section}]: ข้อมูลไม่ครบ (title/price/link required)')

    if errors:
        print('\n'.join(errors))

    if not collected_items and not collected_guide:
        print('❌ ไม่พบข้อมูลที่ valid')
        sys.exit(1)

    total = 0
    for section, items in collected_items.items():
        if section not in picks:
            picks[section] = {'label': f'{section}', 'items': []}
        picks[section]['items'] = items
        print(f'  ✅ {section}.items  → {len(items):>3} รายการ')
        total += len(items)

    for section, guide in collected_guide.items():
        if section not in picks:
            picks[section] = {'label': f'{section}', 'items': [], 'guide': []}
        guide.sort(key=lambda g: g['row'])
        picks[section]['guide'] = guide
        print(f'  ✅ {section}.guide  → {len(guide):>3} แถว')
        total += len(guide)

    if args.dry_run:
        print(f'\n[dry-run] จะ import {total} รายการ — ไม่บันทึก')
        print('─' * 60)
        preview = {k: v for k, v in picks.items() if not k.startswith('_')}
        print(json.dumps(preview, ensure_ascii=False, indent=2)[:3000])
        return

    with open(PICKS_JSON, 'w', encoding='utf-8') as f:
        json.dump(picks, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print(f'\n✅ บันทึกแล้ว → {PICKS_JSON.relative_to(REPO_ROOT)} ({total} รายการ)')

if __name__ == '__main__':
    main()
