/**
 * gen_affiliate_links.js
 * -------------------------------------------------------
 * ใช้ Playwright เพื่อ login Shopee Affiliate Portal แล้ว
 * generate short link (https://s.shopee.co.th/XXXXX)
 * สำหรับแต่ละ product ใน data/affiliate/*.json
 *
 * Usage:
 *   node scripts/gen_affiliate_links.js
 *
 * Requirements:
 *   npm install playwright
 *   npx playwright install chromium
 */

const { chromium } = require('playwright');
const fs   = require('fs');
const path = require('path');

// ── Config ─────────────────────────────────────────────
const PARTNER_ID     = '15358640421';
const DATA_DIR       = path.join(__dirname, '..', 'data', 'affiliate');
const AFFILIATE_URL  = 'https://affiliate.shopee.co.th';
const DELAY_MS       = 1500;   // หน่วงระหว่าง request (หลีกเลี่ยง rate limit)
const HEADLESS       = false;   // false = เปิดหน้าต่างให้ login เอง
const SESSION_FILE   = path.join(__dirname, 'shopee_session.json');

// ── Files to process ──────────────────────────────────
const DATA_FILES = [
  'gpu.json',
  'mac.json',
  'mac_accessories.json',
  'solar_panel.json',
  'solar_inverter.json',
  'ev_charger.json',
  'gold_invest.json',
];

// ── Helpers ────────────────────────────────────────────
function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

function saveJson(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
}

function countPending(items) {
  return items.filter(i => !i.shopee_short_link).length;
}

// ── Main ───────────────────────────────────────────────
async function main() {
  // ── 1. Launch browser ──────────────────────────────
  const launchOptions = { headless: HEADLESS, slowMo: 100 };

  // ถ้ามี saved session ให้ reuse (ไม่ต้อง login ใหม่)
  const storageState = fs.existsSync(SESSION_FILE) ? SESSION_FILE : undefined;

  const browser = await chromium.launch(launchOptions);
  const context = await browser.newContext({ storageState });
  const page    = await context.newPage();

  // ── 2. Login (ถ้ายังไม่มี session) ────────────────
  await page.goto(AFFILIATE_URL + '/login');

  const isLoggedIn = await page.url().includes('dashboard');
  if (!isLoggedIn) {
    console.log('⚠️  กรุณา login ด้วยตัวเองในหน้าต่างที่เปิดขึ้นมา...');
    console.log('   รอจนกว่าจะเข้าหน้า dashboard แล้ว script จะต่อเอง');
    await page.waitForURL('**dashboard**', { timeout: 300_000 }); // รอ 5 นาที
    // บันทึก session เพื่อใช้ครั้งต่อไป
    await context.storageState({ path: SESSION_FILE });
    console.log(`✅ Login สำเร็จ — บันทึก session ที่ ${SESSION_FILE}`);
  } else {
    console.log('✅ ใช้ saved session — ข้าม login');
  }

  // ── 3. ไปที่ Link Generator ────────────────────────
  await page.goto(AFFILIATE_URL + '/link-generation');
  await page.waitForLoadState('networkidle');
  console.log('✅ เข้า Link Generator แล้ว');

  // ── 4. วน loop แต่ละไฟล์ ──────────────────────────
  let totalUpdated = 0;
  let totalSkipped = 0;

  for (const fname of DATA_FILES) {
    const filePath = path.join(DATA_DIR, fname);
    if (!fs.existsSync(filePath)) {
      console.warn(`⚠️  ไม่พบไฟล์ ${fname} — ข้าม`);
      continue;
    }

    const data    = loadJson(filePath);
    const pending = countPending(data.items);
    console.log(`\n📂 ${fname} — ${pending} items ที่ยังไม่มี short link`);

    for (let i = 0; i < data.items.length; i++) {
      const item = data.items[i];

      // ข้ามถ้ามี short link แล้ว (checkpoint)
      if (item.shopee_short_link) {
        totalSkipped++;
        continue;
      }

      const productUrl = item.product_link;
      if (!productUrl) continue;

      try {
        // ── วาง URL ใน input field ────────────────────
        const inputSel = 'input[placeholder*="link"], input[placeholder*="URL"], input[type="text"]';
        await page.waitForSelector(inputSel, { timeout: 10_000 });
        await page.fill(inputSel, '');
        await page.fill(inputSel, productUrl);

        // ── กดปุ่ม Generate ───────────────────────────
        const btnSel = 'button:has-text("Get Link"), button:has-text("Generate"), button:has-text("สร้างลิงก์")';
        await page.click(btnSel);

        // ── รอผลลัพธ์ปรากฏ ────────────────────────────
        // selector อาจต้องปรับตาม DOM จริงของ portal
        await page.waitForFunction(
          () => {
            const links = document.querySelectorAll('a[href*="s.shopee.co.th"], input[value*="s.shopee.co.th"]');
            return links.length > 0;
          },
          { timeout: 15_000 }
        );

        // ── ดึง short link ────────────────────────────
        const shortLink = await page.evaluate(() => {
          const anchor = document.querySelector('a[href*="s.shopee.co.th"]');
          const input  = document.querySelector('input[value*="s.shopee.co.th"]');
          return anchor?.href || input?.value || null;
        });

        if (shortLink) {
          item.shopee_short_link = shortLink;
          item.affiliate_link    = shortLink; // override method-2 link ด้วย short link
          totalUpdated++;
          console.log(`  [${i+1}/${data.items.length}] ✅ ${item.title.slice(0,45)} → ${shortLink}`);
        } else {
          console.warn(`  [${i+1}/${data.items.length}] ⚠️  ไม่พบ short link — ${productUrl}`);
        }

      } catch (err) {
        console.error(`  [${i+1}/${data.items.length}] ❌ Error: ${err.message}`);
      }

      // ── หน่วงก่อน request ถัดไป ───────────────────
      await sleep(DELAY_MS);

      // ── Auto-save ทุก 10 items (checkpoint) ───────
      if (i % 10 === 9) {
        saveJson(filePath, data);
        console.log(`  💾 Checkpoint saved (${i+1} items)`);
      }
    }

    // ── Save ไฟล์ที่อัปเดตแล้ว ───────────────────────
    saveJson(filePath, data);
    console.log(`  💾 Saved ${fname}`);
  }

  // ── 5. Summary ─────────────────────────────────────
  console.log(`\n═══════════════════════════════`);
  console.log(`✅ เสร็จสิ้น`);
  console.log(`   Updated : ${totalUpdated} items`);
  console.log(`   Skipped : ${totalSkipped} items (มี short link แล้ว)`);

  await browser.close();
}

// ── Error handler ──────────────────────────────────────
main().catch(err => {
  console.error('❌ Fatal error:', err);
  process.exit(1);
});
