"""
test_lazada_api.py
--------------------------------------------------
ทดสอบ Lazada Affiliate API ด้วย official SDK
ใช้ /marketing/ endpoints ที่ถูกต้องสำหรับ Affiliate

Usage:
  python3 scripts/test_lazada_api.py

.env ที่ root:
  LAZADA_APP_KEY=105827
  LAZADA_APP_SECRET=xxxx
  LAZADA_USER_TOKEN=xxxx   ← user token จาก Affiliate Dashboard
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import lazop

# ── Load .env ──────────────────────────────────────────────
def load_env() -> dict:
    env_path = Path(__file__).parent.parent / '.env'
    if not env_path.exists():
        print('❌ ไม่พบไฟล์ .env')
        sys.exit(1)
    env = {}
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env

TH_URL = 'https://api.lazada.co.th/rest'

def call(client, path: str, params: dict) -> lazop.LazopResponse:
    req = lazop.LazopRequest(path, 'GET')
    for k, v in params.items():
        req.add_api_param(k, str(v))
    return client.execute(req)

def main():
    print('=' * 58)
    print('  Lazada Affiliate API Test — ComPair')
    print('=' * 58)

    env = load_env()
    app_key    = env.get('LAZADA_APP_KEY', '')
    secret     = env.get('LAZADA_APP_SECRET', '')
    user_token = env.get('LAZADA_USER_TOKEN', '')

    print(f'\n  App Key:    {app_key}')
    print(f'  Secret:     {secret[:8]}...')
    print(f'  UserToken:  {user_token[:16]}...')

    client = lazop.LazopClient(TH_URL, app_key, secret)

    # ── Test 1: Product Feed (offerType=1 = Regular) ───────
    print('\n🛍  Test 1: /marketing/product/feed (Regular offer)')
    resp = call(client, '/marketing/product/feed', {
        'offerType':  1,
        'userToken':  user_token,
        'page':       1,
        'limit':      5,
    })
    print(f'   code={resp.code}  message={resp.message}')
    if resp.code == '0':
        result   = resp.body.get('result', {})
        products = result.get('data', []) if isinstance(result, dict) else []
        print(f'   ✅ ได้ {len(products)} สินค้า')
        for p in products[:3]:
            price = p.get('discountPrice', 0)
            comm  = p.get('totalCommissionRate', 0)
            name  = str(p.get('productName', ''))[:55]
            print(f'      [{p.get("productId")}] {name}')
            print(f'       ราคา ฿{price:,.0f}  commission {comm*100:.1f}%  sold7d={p.get("sales7d")}')
    else:
        print(f'   full response: {json.dumps(resp.body)[:300]}')

    # ── Test 2: Batch Get Link (from product URL) ───────────
    print('\n🔗 Test 2: /marketing/getlink (batch by URL)')
    sample_url = 'https://www.lazada.co.th/products/apple-macbook-air-m2-i.html'
    resp = call(client, '/marketing/getlink', {
        'userToken':   user_token,
        'inputType':   'url',
        'inputValue':  sample_url,
    })
    print(f'   code={resp.code}  message={resp.message}')
    if resp.code == '0':
        result = resp.body.get('result', resp.body.get('data', {}))
        urls   = (result.get('urlBatchGetLinkInfoList', [])
                  if isinstance(result, dict) else [])
        if urls:
            item = urls[0]
            print(f'   ✅ trackingLink: {item.get("regularPromotionLink","")}')
            print(f'      commission:   {item.get("regularCommission","")}')
        else:
            success = result.get('success', True) if isinstance(result, dict) else True
            if not success:
                errs = result.get('errorInfoList', []) if isinstance(result, dict) else []
                print(f'   ⚠ {errs}')
            else:
                print(f'   ✅ endpoint ใช้งานได้')
    else:
        print(f'   full response: {json.dumps(resp.body)[:300]}')

    # ── Test 3: Conversion Report ───────────────────────────
    print('\n📊 Test 3: /marketing/conversion/report')
    resp = call(client, '/marketing/conversion/report', {
        'userToken':  user_token,
        'dateStart':  '2026-07-01',
        'dateEnd':    '2026-07-01',
        'limit':      10,
        'page':       1,
    })
    print(f'   code={resp.code}  message={resp.message}')
    if resp.code == '0':
        result = resp.body.get('result', {})
        items  = result.get('data', []) if isinstance(result, dict) else []
        print(f'   ✅ {len(items)} conversion records (July 2026)')
    else:
        print(f'   full response: {json.dumps(resp.body)[:300]}')

    print('\n' + '=' * 58)
    print('  Portal: https://open.lazada.com/apps/myapp')
    print('  ⚠  ถ้า code=RGV2ZWxvcGVy... → API pending approval')
    print('     ถ้า code=IllegalAccessToken → user token หมดอายุ')
    print('=' * 58)

if __name__ == '__main__':
    main()
