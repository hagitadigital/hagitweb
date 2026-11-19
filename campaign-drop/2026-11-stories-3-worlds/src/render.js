// Renders each .story section of stories.html to a 1080x1920 PNG in ../
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(__dirname, 'stories.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  const n = await p.locator('.story').count();
  for (let i = 0; i < n; i++)
    await p.locator('.story').nth(i).screenshot({ path: path.join(__dirname, '..', `story-0${i + 1}.png`) });
  await b.close();
})();
