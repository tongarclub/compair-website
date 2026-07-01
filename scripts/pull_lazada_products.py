"""
pull_lazada_products.py
--------------------------------------------------
ดึงสินค้าจาก Lazada Affiliate API → บันทึกเป็น JSON
ใช้ /marketing/product/feed และ /marketing/getlink

Format output เข้ากันได้กับ Shopee JSON + aff-utils.js

Usage:
  python3 scripts/pull_lazada_products.py --list-categories
  python3 scripts/pull_lazada_products.py --category air_conditioner
  python3 scripts/pull_lazada_products.py --all
  python3 scripts/pull_lazada_products.py --links 123,456,789

.env:
  LAZADA_APP_KEY, LAZADA_APP_SECRET, LAZADA_USER_TOKEN
"""

import sys
import json
import time
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import lazop

# ── Category L1 IDs (จาก /category/tree/get) ───────────────
# ดู category_id จริงได้จาก:
#   python3 scripts/pull_lazada_products.py --list-categories
CATEGORIES = {
    'air_conditioner': {
        'category_l1':  3833,    # Home Appliances
        'desc':         'เครื่องปรับอากาศ',
        'output':       'lazada_air_conditioner',
    },
    'washing_machine': {
        'category_l1':  3833,    # Home Appliances
        'desc':         'เครื่องซักผ้า',
        'output':       'lazada_washing_machine',
    },
    'water_filter': {
        'category_l1':  3833,    # Home Appliances
        'desc':         'เครื่องกรองน้ำ',
        'output':       'lazada_water_filter',
    },
    'air_purifier': {
        'category_l1':  3833,    # Home Appliances
        'desc':         'เครื่องฟอกอากาศ',
        'output':       'lazada_air_purifier',
    },
    'solar_panel': {
        'category_l1':  3833,    # Home Appliances
        'desc':         'แผงโซล่าเซลล์',
        'output':       'lazada_solar_panel',
    },
    'ev_charger': {
        'category_l1':  3833,    # Home Appliances
        'desc':         'EV Charger',
        'output':       'lazada_ev_charger',
    },
    'gpu': {
        'category_l1':  3834,    # Computers & Components
        'desc':         'GPU / การ์ดจอ',
        'output':       'lazada_gpu',
    },
    'laptop': {
        'category_l1':  3834,    # Computers & Components
        'desc':         'Laptop / Notebook',
        'output':       'lazada_laptop',
    },
    'headphone': {
        'category_l1':  10100387, # Audio
        'desc':         'หูฟัง / Earphone',
        'output':       'lazada_headphone',
    },
    'smartwatch': {
        'category_l1':  10100412, # Smart Devices
        'desc':         'Smartwatch',
        'output':       'lazada_smartwatch',
    },
    'gaming': {
        'category_l1':  10100871, # Gaming Devices & Software
        'desc':         'Gaming Devices',
        'output':       'lazada_gaming',
    },
}

TH_URL   = 'https://api.lazada.co.th/rest'
DATA_DIR = Path(__file__).parent.parent / 'data' / 'affiliate'

def load_env() -> dict:
    env_path = Path(__file__).parent.parent / '.env'
    env = {}
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env

def call(client, path: str, params: dict) -> lazop.LazopResponse:
    req = lazop.LazopRequest(path, 'GET')
    for k, v in params.items():
        req.add_api_param(k, str(v))
    return client.execute(req)

# ── แปลง Lazada product feed item → ComPair JSON ──────────
def parse_feed_item(p: dict, tracking_links: dict) -> dict | None:
    pid   = str(p.get('productId', ''))
    name  = (p.get('productName') or '').strip()
    if not name:
        return None

    image = ''
    pics  = p.get('pictures', [])
    if isinstance(pics, list) and pics:
        image = pics[0] if isinstance(pics[0], str) else ''

    sale_price = str(p.get('discountPrice') or p.get('price') or '0')
    commission = str(p.get('totalCommissionRate') or '0')
    sold_7d    = str(p.get('sales7d') or '0')
    brand      = str(p.get('brandName') or '')
    product_url = f'https://www.lazada.co.th/products/i{pid}.html'

    aff_link = tracking_links.get(pid, {}).get('trackingLink', product_url)

    # แปลง commission rate เป็น % string
    try:
        disc_pct = str(round(float(commission) * 100, 1)) if float(commission) < 1 else commission
    except Exception:
        disc_pct = commission

    return {
        'title':               name,
        'sale_price':          sale_price,
        'price':               sale_price,
        'discount_percentage': '0',
        'item_sold':           sold_7d,
        'item_rating':         '0',
        'brand':               brand,
        'image_link':          image,
        'product_link':        product_url,
        'affiliate_link':      aff_link,
        'commission_rate':     disc_pct,
        'source':              'lazada',
    }

# ── ดึง product feed ───────────────────────────────────────
def fetch_feed(client, user_token: str,
               category_l1: int = None,
               limit: int = 50) -> list:
    items = []
    page  = 1

    while len(items) < limit:
        params = {
            'offerType':  1,        # 1=Regular, 2=MM, 3=DM
            'userToken':  user_token,
            'page':       page,
            'limit':      min(50, limit - len(items)),
        }
        if category_l1:
            params['categoryL1'] = category_l1

        resp = call(client, '/marketing/product/feed', params)

        if resp.code != '0':
            print(f'   ⚠ feed code={resp.code}: {resp.message}')
            break

        # response structure: { result: { data: [...], success: bool }, code, ... }
        result   = resp.body.get('result', {})
        products = result.get('data', []) if isinstance(result, dict) else []
        if not products:
            break

        items.extend(products)
        if len(products) < 50:
            break

        page += 1
        time.sleep(0.3)

    return items[:limit]

# ── ดึง tracking links แบบ batch ──────────────────────────
def fetch_links(client, user_token: str, product_ids: list) -> dict:
    """
    Return dict: { productId -> { trackingLink, commission } }
    Batch max 100 per call
    """
    result = {}
    for i in range(0, len(product_ids), 100):
        chunk = product_ids[i:i+100]
        resp  = call(client, '/marketing/product/link', {
            'userToken': user_token,
            'productId': chunk[0],  # single first
        })
        # try batch endpoint
        resp2 = call(client, '/marketing/getlink', {
            'userToken':  user_token,
            'inputType':  'productId',
            'inputValue': ','.join(str(x) for x in chunk),
        })

        if resp2.code == '0':
            r2data = resp2.body.get('result', resp2.body.get('data', {}))
            links_list = (r2data.get('productBatchGetLinkInfoList', [])
                          if isinstance(r2data, dict) else [])
            for item in links_list:
                pid = str(item.get('productId', ''))
                result[pid] = {
                    'trackingLink': item.get('regularPromotionLink', ''),
                    'commission':   item.get('regularCommission', ''),
                }
        elif resp.code == '0':
            r1data = resp.body.get('result', resp.body.get('data', {}))
            if isinstance(r1data, dict):
                pid = str(r1data.get('productId', chunk[0]))
                result[pid] = {
                    'trackingLink': r1data.get('trackingLink', ''),
                    'commission':   r1data.get('commisionRate', ''),
                }
        time.sleep(0.2)

    return result

# ── บันทึก JSON ────────────────────────────────────────────
def save_json(items: list, slug: str, desc: str):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = {
        'desc':    f'Lazada — {desc}',
        'count':   len(items),
        'source':  'lazada',
        'updated': time.strftime('%Y-%m-%d'),
        'items':   items,
    }
    path = DATA_DIR / f'{slug}.json'
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f'   ✅ บันทึก {len(items)} รายการ → {path.name}')

# ── List categories ─────────────────────────────────────────
def list_categories(client):
    resp = call(client, '/category/tree/get', {})
    print('\nCategory Tree (Top Level):')
    if resp.code == '0':
        cats = resp.body.get('data', [])
        for c in cats:
            print(f'  {c.get("category_id"):<12} {c.get("name","")}')
    else:
        print(f'  ⚠ {resp.code}: {resp.message}')

# ── Main ───────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description='Pull Lazada Affiliate products → JSON')
    parser.add_argument('--category',         choices=list(CATEGORIES.keys()))
    parser.add_argument('--all',              action='store_true')
    parser.add_argument('--list-categories',  action='store_true')
    parser.add_argument('--links',            help='batch get links by productId, e.g. 123,456')
    parser.add_argument('--limit',            type=int, default=50)
    args = parser.parse_args()

    print('=' * 58)
    print('  Lazada Product Pull — ComPair')
    print('=' * 58)

    env = load_env()
    app_key    = env.get('LAZADA_APP_KEY', '')
    secret     = env.get('LAZADA_APP_SECRET', '')
    user_token = env.get('LAZADA_USER_TOKEN', '')

    if not app_key:
        print('❌ กรุณาอัปเดต .env ก่อน')
        sys.exit(1)

    client = lazop.LazopClient(TH_URL, app_key, secret)

    if args.list_categories:
        list_categories(client)
        return

    if args.links:
        pids  = [x.strip() for x in args.links.split(',')]
        print(f'\n🔗 Batch get links for {len(pids)} products')
        links = fetch_links(client, user_token, pids)
        for pid, data in links.items():
            print(f'  {pid}: {data["trackingLink"]}  ({data["commission"]})')
        return

    # กำหนด targets
    if args.all:
        targets = CATEGORIES
    elif args.category:
        targets = {args.category: CATEGORIES[args.category]}
    else:
        parser.print_help()
        return

    for slug, info in targets.items():
        print(f'\n📦 {info["desc"]} (L1: {info["category_l1"]})')
        raw = fetch_feed(client, user_token,
                         category_l1=info['category_l1'],
                         limit=args.limit)
        print(f'   ดึงมาได้: {len(raw)} รายการ (raw)')

        if not raw:
            print('   ⚠ ไม่มีข้อมูล — ข้ามไป')
            continue

        # ดึง tracking links
        pids  = [str(p.get('productId','')) for p in raw if p.get('productId')]
        print(f'   กำลังดึง tracking links...')
        links = fetch_links(client, user_token, pids[:100])

        items = []
        for p in raw:
            parsed = parse_feed_item(p, links)
            if parsed:
                items.append(parsed)

        # เรียงตาม sales7d ↓
        items.sort(key=lambda x: float(x.get('item_sold','0') or 0), reverse=True)
        save_json(items, info['output'], info['desc'])

    print('\n✅ เสร็จสิ้น')

if __name__ == '__main__':
    main()
