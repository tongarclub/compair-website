"""
pull_lazada_products.py
--------------------------------------------------
ดึงสินค้าจาก Lazada Affiliate API → บันทึกเป็น JSON
ใช้ /marketing/product/feed และ /marketing/getlink

Format output เข้ากันได้กับ Shopee JSON + aff-utils.js

กลยุทธ์การค้นหา:
  1. ถ้า category มี 'keywords' → ดึงด้วย keyword (ตรงกว่า)
  2. ถ้าไม่มี → fallback ดึงด้วย categoryL1 แล้ว filter ทีหลัง
  3. ดึงเยอะกว่า limit (fetch_multiplier) แล้ว keyword-filter ก่อน save

Usage:
  python3 scripts/pull_lazada_products.py --list-categories
  python3 scripts/pull_lazada_products.py --category ev_charger
  python3 scripts/pull_lazada_products.py --all
  python3 scripts/pull_lazada_products.py --links 123,456,789
  python3 scripts/pull_lazada_products.py --test-keyword "EV Charger"

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

# ── Category config ─────────────────────────────────────────
# keywords: ใช้ค้นหาแทน / เสริม categoryL1 เพื่อ relevancy ที่ดีขึ้น
# filter_kw: กรอง title หลัง fetch (ตัดสินค้าไม่เกี่ยวออก)
# fetch_multiplier: ดึงเยอะกว่า limit กี่เท่า (เพื่อมีให้ filter)
CATEGORIES = {
    'air_conditioner': {
        'category_l1':  3833,
        'keywords':     'เครื่องปรับอากาศ air conditioner',
        'filter_kw':    ['air conditioner','เครื่องปรับอากาศ','แอร์','inverter ac',
                         'ductless','split type','ceiling cassette'],
        'desc':         'เครื่องปรับอากาศ',
        'output':       'lazada_air_conditioner',
    },
    'washing_machine': {
        'category_l1':  3833,
        'keywords':     'เครื่องซักผ้า washing machine',
        'filter_kw':    ['washing machine','เครื่องซักผ้า','washer','laundry',
                         'washtower','tumble dryer'],
        'desc':         'เครื่องซักผ้า',
        'output':       'lazada_washing_machine',
    },
    'water_filter': {
        'category_l1':  3833,
        'keywords':     'เครื่องกรองน้ำ water filter purifier',
        'filter_kw':    ['water filter','เครื่องกรองน้ำ','water purifier',
                         'reverse osmosis','ro filter','ระบบกรองน้ำ'],
        'desc':         'เครื่องกรองน้ำ',
        'output':       'lazada_water_filter',
    },
    'air_purifier': {
        'category_l1':  3833,
        'keywords':     'เครื่องฟอกอากาศ air purifier',
        'filter_kw':    ['air purifier','เครื่องฟอกอากาศ','hepa filter',
                         'pm2.5','air cleaner'],
        'desc':         'เครื่องฟอกอากาศ',
        'output':       'lazada_air_purifier',
    },
    'solar_panel': {
        # L1=3833 คืน washing machine — ใช้ keyword เป็นหลักแทน
        'category_l1':  None,
        'keywords':     'solar panel แผงโซล่าเซลล์ MPPT inverter off-grid',
        'filter_kw':    ['solar panel','แผงโซล่า','โซล่าเซลล์','pv panel',
                         'photovoltaic','mppt','solar inverter','off grid',
                         'on grid','hybrid inverter','charge controller',
                         'solar charger','อินเวอร์เตอร์ solar'],
        'filter_excl':  ['solar light','ไฟโซล่า','solar lamp','garden light'],
        'fetch_multiplier': 4,   # ดึง 200 items เพื่อกรองเหลือ 50
        'desc':         'แผงโซล่าเซลล์ + Inverter',
        'output':       'lazada_solar_panel',
    },
    'ev_charger': {
        # L1=3833 คืน washing machine — ใช้ keyword เป็นหลักแทน
        'category_l1':  None,
        'keywords':     'EV Charger ที่ชาร์จรถยนต์ไฟฟ้า wallbox type2 EVSE',
        'filter_kw':    ['ev charger','ev charging','wallbox','wall box',
                         'type 2 charger','type2 charger','ที่ชาร์จ ev',
                         'ชาร์จรถยนต์ไฟฟ้า','home ev','ac ev charger',
                         'evse','7kw charger','11kw charger','22kw charger'],
        'fetch_multiplier': 4,
        'desc':         'EV Charger',
        'output':       'lazada_ev_charger',
    },
    'gpu': {
        'category_l1':  3834,
        'keywords':     'การ์ดจอ RTX GTX RX VGA GPU graphics card',
        'filter_kw':    ['rtx','gtx','geforce','radeon','graphics card',
                         'การ์ดจอ','vga card'],
        'filter_excl':  ['notebook','laptop','โน้ตบุ๊ก'],
        'fetch_multiplier': 3,
        'desc':         'GPU / การ์ดจอ',
        'output':       'lazada_gpu',
    },
    'laptop': {
        'category_l1':  3834,
        # L1=3834 คืนเฉพาะ laptops/computers อยู่แล้ว — ไม่ filter_kw (ตัดทิ้งน้อยลง)
        # แค่ตัด GPU card และ desktop peripherals ออก
        'filter_excl':  ['graphics card','vga card','gpu ','การ์ดจอ',
                         'gaming mouse','gaming keyboard','gaming headset',
                         'monitor ','จอมอนิเตอร์'],
        'fetch_multiplier': 2,
        'desc':         'Laptop / Notebook',
        'output':       'lazada_laptop',
    },
    'headphone': {
        'category_l1':  10100387,
        'keywords':     'หูฟัง earphone headphone wireless bluetooth',
        'filter_kw':    ['headphone','earphone','หูฟัง','earbud',
                         'in-ear','over-ear','anc','noise cancel'],
        'fetch_multiplier': 2,
        'desc':         'หูฟัง / Earphone',
        'output':       'lazada_headphone',
    },
    'smartwatch': {
        'category_l1':  10100412,
        'keywords':     'smartwatch smart watch นาฬิกา smart band',
        'filter_kw':    ['smartwatch','smart watch','นาฬิกาสมาร์ท',
                         'smart band','fitness tracker','sport watch'],
        'fetch_multiplier': 2,
        'desc':         'Smartwatch',
        'output':       'lazada_smartwatch',
    },
    'gaming': {
        'category_l1':  10100871,
        'keywords':     'gaming mouse keyboard controller joystick',
        'filter_kw':    ['gaming','controller','joystick','gamepad',
                         'gaming mouse','gaming keyboard','gaming headset'],
        'fetch_multiplier': 2,
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

# ── กรอง product list ด้วย keyword ─────────────────────────
def filter_items(raw_items: list, filter_kw: list = None, filter_excl: list = None) -> list:
    """
    กรองสินค้าด้วย keyword:
    - filter_kw:   ถ้ามี → ต้องผ่านอย่างน้อย 1 keyword (inclusion filter)
    - filter_excl: ถ้ามี keyword ใด keyword หนึ่ง → ตัดออก (exclusion filter)
    ถ้าไม่มี filter_kw → ใช้ exclusion-only
    """
    incl = [k.lower() for k in (filter_kw   or [])]
    excl = [k.lower() for k in (filter_excl or [])]
    if not incl and not excl:
        return raw_items
    result = []
    for p in raw_items:
        t = (p.get('productName') or '').lower()
        if excl and any(k in t for k in excl):
            continue
        if incl and not any(k in t for k in incl):
            continue
        result.append(p)
    return result


# ── ดึง product feed ───────────────────────────────────────
def fetch_feed(client, user_token: str,
               category_l1: int = None,
               keywords: str = None,
               limit: int = 50) -> list:
    """
    ดึง product feed จาก Lazada Affiliate API
    - ถ้ามี keywords → ลอง pass เป็น param ก่อน (undocumented แต่บางครั้งรองรับ)
    - ถ้า API ไม่รองรับ → fetch ปกติด้วย categoryL1
    """
    items = []
    page  = 1

    while len(items) < limit:
        params = {
            'offerType':  1,
            'userToken':  user_token,
            'page':       page,
            'limit':      min(50, limit - len(items)),
        }
        if category_l1:
            params['categoryL1'] = category_l1
        # ลอง pass keyword (undocumented — บางเวอร์ชัน API รองรับ)
        if keywords:
            params['keyword'] = keywords.split()[0]  # คำแรกที่เฉพาะเจาะจงที่สุด

        resp = call(client, '/marketing/product/feed', params)

        if resp.code != '0':
            print(f'   ⚠ feed code={resp.code}: {resp.message}')
            # ถ้า keyword param ทำให้ error → retry โดยไม่มี keyword
            if keywords and 'keyword' in params:
                print('   ↩ retry โดยไม่มี keyword param...')
                del params['keyword']
                resp = call(client, '/marketing/product/feed', params)
                if resp.code != '0':
                    break
            else:
                break

        result   = resp.body.get('result', {})
        products = result.get('data', []) if isinstance(result, dict) else []
        if not products:
            break

        items.extend(products)
        # หยุดเมื่อ API คืน 0 items หรือน้อยกว่า 10 (end of feed)
        # ไม่ break เมื่อได้ 49 เพราะ Lazada คืน max=49 ต่อ page
        if len(products) < 10:
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
    parser.add_argument('--test-keyword',     help='ทดสอบ keyword search: --test-keyword "EV Charger"')
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

    # ── ทดสอบ keyword search ──────────────────────────────
    if args.test_keyword:
        kw = args.test_keyword
        print(f'\n🔍 ทดสอบ keyword: "{kw}"')
        raw = fetch_feed(client, user_token, keywords=kw, limit=20)
        print(f'   ได้: {len(raw)} รายการ')
        for p in raw[:10]:
            print(f'   • {(p.get("productName",""))[:70]}')
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
        multiplier   = info.get('fetch_multiplier', 1)
        fetch_limit  = min(args.limit * multiplier, 200)
        kw           = info.get('keywords')
        filter_kw    = info.get('filter_kw') or []
        filter_excl  = info.get('filter_excl') or []
        cat_l1       = info.get('category_l1')

        print(f'\n📦 {info["desc"]}')
        print(f'   category_l1: {cat_l1 or "none"}, keywords: {kw or "none"}')
        print(f'   fetch {fetch_limit} items → filter → save top {args.limit}')

        raw = fetch_feed(client, user_token,
                         category_l1=cat_l1,
                         keywords=kw,
                         limit=fetch_limit)
        print(f'   ดึงมาได้: {len(raw)} รายการ (raw)')

        if not raw:
            print('   ⚠ ไม่มีข้อมูล — ข้ามไป')
            continue

        # กรอง keyword client-side
        if filter_kw:
            filtered = filter_items(raw, filter_kw, filter_excl)
            print(f'   หลัง keyword filter: {len(filtered)} รายการ'
                  f'  ({"ตรง" if filtered else "❌ ไม่มีสินค้าตรง — ใช้ raw แทน"})')
            if not filtered:
                # fallback: ใช้ raw แต่แจ้งเตือน
                filtered = raw
        else:
            filtered = raw

        # ดึง tracking links (top 100 เท่านั้นเพื่อประหยัด rate limit)
        top = filtered[:max(args.limit, 100)]
        pids  = [str(p.get('productId','')) for p in top if p.get('productId')]
        print(f'   กำลังดึง tracking links ({len(pids)} IDs)...')
        links = fetch_links(client, user_token, pids)

        items = []
        for p in top:
            parsed = parse_feed_item(p, links)
            if parsed:
                items.append(parsed)

        # dedup by title (เอา title เดียวกันออก)
        seen_titles = set()
        deduped = []
        for it in items:
            key = (it.get('title') or '')[:60].lower()
            if key not in seen_titles:
                seen_titles.add(key)
                deduped.append(it)
        items = deduped

        # เรียงตาม sales7d ↓ แล้วเก็บแค่ limit
        items.sort(key=lambda x: float(x.get('item_sold','0') or 0), reverse=True)
        items = items[:args.limit]
        save_json(items, info['output'], info['desc'])

    print('\n✅ เสร็จสิ้น')

if __name__ == '__main__':
    main()
