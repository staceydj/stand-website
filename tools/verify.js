// Remake verification: writes REMAKE_REPORT.md and says REMAKE COMPLETE only if every check passes.
// Usage: node tools/verify.js <original-en.html> <original-image-dir> <stand-source.txt>
const fs = require('fs');
const path = require('path');
const http = require('http');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const ORIGINAL = process.argv[2];
// Optional: folder holding the original site's image files, to prove none of them is reused.
const ORIGINAL_IMG_DIR = process.argv[3];
// Optional: plain-text copy of standaction.co.za, the source for every claim and figure.
const STAND_SOURCE = process.argv[4];
const ALLOWED_IMG_DIRS = ['assets/gen/', 'assets/stand/', 'assets/art/'];
const SHOTS = path.join(ROOT, 'screenshots');
fs.mkdirSync(SHOTS, { recursive: true });

// Original lines that intentionally differ, with the reason.
const ALLOWED_DIFFS = {
  'Christopher': 'Founder photo replaced with STAND\'s Charity Monareng; label now matches the person pictured.',
  'Bettina': 'Founder photo replaced with STAND\'s Stacey Doorly-Jones; label now matches the person pictured.',
  'Known from:': 'Media-logo strip removed: those were TO TOP press logos and STAND has none to show yet.',
  'experienced in consulting I versatile I resilient': 'Capital "I" separators normalised to "|" like the other rows.',
  'Oops! Something went wrong while submitting the form.': 'Third-party form embed replaced by a mailto form with its own status messages.',
  'Thank you very much. We will be in touch!': 'Replaced by honest mailto status text (no server submission exists).',
  'Start': 'Part of the "TO TOP Start program" button, rendered with line breaks.',
  'program': 'Part of the "TO TOP Start program" button, rendered with line breaks.',
  'INFO': 'Rendered as "Info video" button label.',
  'VIDEO': 'Rendered as "Info video" button label.',
  'WHERE DO YOU WANT TO GO?': 'Hero circle button label, rendered as "Where do you want to go?".',
  'WHERE DO': 'Hero circle button label, rendered as "Where do you want to go?".',
  'YOU WANT TO GO?': 'Hero circle button label, rendered as "Where do you want to go?".',
  'TO TOP - for better organizations': 'Page title (present in <title>).',
  'Booking': 'Present as the "Booking" link.',
};

const norm = (s) => s.replace(/ /g, ' ').replace(/[“”]/g, '"').replace(/[’]/g, "'").replace(/\s+/g, ' ').trim().toLowerCase();

function originalLines(file) {
  const s = fs.readFileSync(file, 'utf8');
  let body = s.replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/g, '');
  body = body.replace(/<[^>]+>/g, '\n')
    .replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'").replace(/&nbsp;/g, ' ')
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>');
  return [...new Set(body.split('\n').map((l) => l.trim()).filter((l) => l && l !== '|' && l !== ':'))];
}

function serve() {
  const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.avif': 'image/avif', '.webp': 'image/webp', '.png': 'image/png', '.ttf': 'font/ttf', '.pdf': 'application/pdf' };
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0].split('#')[0]) === '/' ? 'index.html' : decodeURIComponent(req.url.split('?')[0]));
      if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end('nf'); }
      res.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream' });
      fs.createReadStream(p).pipe(res);
    });
    srv.listen(0, '127.0.0.1', () => resolve(srv));
  });
}

async function checkUrl(url) {
  return new Promise((resolve) => {
    const { execFile } = require('child_process');
    execFile('curl', ['-sS', '-o', '/dev/null', '-L', '-w', '%{http_code}', '--max-time', '20', url], (err, out) => resolve(err ? `ERR` : out.trim()));
  });
}

(async () => {
  const results = [];
  let usedText = '';
  const add = (name, pass, detail) => results.push({ name, pass, detail });
  const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
  const PAGES = fs.readdirSync(ROOT).filter((f) => f.endsWith('.html')).sort();
  const pageHtml = Object.fromEntries(PAGES.map((f) => [f, fs.readFileSync(path.join(ROOT, f), 'utf8')]));
  const allHtml = Object.values(pageHtml).join('\n');

  // 1. Local asset references resolve, on every page
  const refs = [...allHtml.matchAll(/(?:src|href)="([^"#][^"]*)"/g)].map((m) => m[1].split('#')[0])
    .filter((u) => !/^(https?:|mailto:|tel:|\/\/)/.test(u));
  const css = ['css/styles.css', 'css/pages.css'].filter((f) => fs.existsSync(path.join(ROOT, f))).map((f) => fs.readFileSync(path.join(ROOT, f), 'utf8')).join('\n');
  const cssRefs = [...css.matchAll(/url\("?\.\.\/([^")]+)"?\)/g)].map((m) => m[1]);
  const missing = [...new Set([...refs.filter((u) => !fs.existsSync(path.join(ROOT, u))), ...cssRefs.filter((u) => !fs.existsSync(path.join(ROOT, u)))])];
  add(`Local files referenced by all ${PAGES.length} pages and the CSS exist`, missing.length === 0, missing.length ? `Missing: ${missing.join(', ')}` : `${refs.length + cssRefs.length} references OK`);

  // 1b. Every picture comes from the new STAND sets, and none is byte-identical to an original image
  {
    const crypto = require('crypto');
    const imgRefs = [...allHtml.matchAll(/<img[^>]+src="([^"]+)"/g)].map((m) => m[1])
      .concat([...allHtml.matchAll(/<link[^>]+rel="(?:icon|apple-touch-icon)"[^>]+href="([^"]+)"/g)].map((m) => m[1]))
      .concat(cssRefs.filter((u) => !u.startsWith('assets/fonts/')));
    const outside = imgRefs.filter((u) => !ALLOWED_IMG_DIRS.some((d) => u.startsWith(d)));
    add('Every image is from the new STAND sets (generated, STAND photos, new line art)', outside.length === 0,
      outside.length ? `Outside new sets: ${outside.join(', ')}` : `${new Set(imgRefs).size} distinct images, all in ${ALLOWED_IMG_DIRS.join(', ')}`);
    if (ORIGINAL_IMG_DIR && fs.existsSync(ORIGINAL_IMG_DIR)) {
      const hash = (f) => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
      const orig = new Set(fs.readdirSync(ORIGINAL_IMG_DIR).map((f) => path.join(ORIGINAL_IMG_DIR, f)).filter((f) => fs.statSync(f).isFile()).map(hash));
      const shipped = [];
      const walk = (d) => fs.readdirSync(d).forEach((f) => { const p = path.join(d, f); fs.statSync(p).isDirectory() ? walk(p) : shipped.push(p); });
      walk(path.join(ROOT, 'assets'));
      const reused = shipped.filter((f) => orig.has(hash(f))).map((f) => path.relative(ROOT, f));
      add('No file in assets/ is a copy of an original TO TOP image', reused.length === 0,
        reused.length ? `Reused: ${reused.join(', ')}` : `${shipped.length} shipped files compared against ${orig.size} originals`);
    } else {
      add('No file in assets/ is a copy of an original TO TOP image', false, 'Original image folder not supplied');
    }
  }

  // 2. Every link between pages lands on a page and, where given, an existing anchor
  {
    const bad = [];
    let n = 0;
    for (const [f, h] of Object.entries(pageHtml)) {
      for (const m of h.matchAll(/href="([^"]*#[^"]*)"/g)) {
        if (/^(https?:|mailto:)/.test(m[1])) continue;
        const [file, frag] = m[1].split('#');
        const target = file || f;
        n += 1;
        if (!frag) continue;
        const th = pageHtml[target];
        if (!th || !th.includes(`id="${frag}"`)) bad.push(`${f} -> ${m[1]}`);
      }
    }
    add('Every link between pages lands on an existing page and anchor', bad.length === 0, bad.length ? `Broken: ${[...new Set(bad)].join(', ')}` : `${n} internal links OK`);
  }

  // 3. Copy: nothing of TO TOP's remains, and every figure is backed by STAND's own site
  const srv = await serve();
  const base = `http://127.0.0.1:${srv.address().port}/index.html`;
  const browser = await chromium.launch();
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(base, { waitUntil: 'load' });
    const raw = await page.evaluate(() => document.body.innerText + ' ' + document.title + ' ' +
      [...document.querySelectorAll('[alt],[aria-label],[title],[href]')].map((e) => [e.getAttribute('alt'), e.getAttribute('aria-label'), e.getAttribute('title'), e.getAttribute('href')].join(' ')).join(' '));
    usedText = norm(raw);
    const terms = ['to-top', 'totop', 'bettina', 'christoph', 'weidmann', 'logotio', '+ 41', '+41', 'transforming organizations', 'people, planet, profit', 'iubenda'];
    const hitsTerms = terms.filter((t) => usedText.includes(t)).concat(/TO TOP/.test(raw) ? ['TO TOP'] : []);
    const lines = ORIGINAL ? originalLines(ORIGINAL).filter((l) => l.length >= 15) : [];
    const hitsLines = lines.filter((l) => usedText.includes(norm(l)));
    const hits = [...hitsTerms, ...hitsLines];
    add('No TO TOP names, contacts or copy remain (text, alt text, links)', ORIGINAL && hits.length === 0,
      hits.length ? `Found: ${hits.map((h) => `"${h}"`).join(', ')}` : `${terms.length} TO TOP terms and ${lines.length} original sentences checked`);

    if (STAND_SOURCE && fs.existsSync(STAND_SOURCE)) {
      const src = norm(fs.readFileSync(STAND_SOURCE, 'utf8')).replace(/\s/g, '');
      const visible = await page.evaluate(() => document.body.innerText);
      const figures = [...new Set((visible.match(/\+?\d[\d ,.]*\d|\d/g) || []).map((f) => f.trim()))]
        .filter((f) => !/^0[1-9]$/.test(f));            // card numbering 01-05
      const unbacked = figures.filter((f) => !src.includes(f.replace(/\s/g, '').toLowerCase()));
      add('Every figure on the page appears on standaction.co.za', unbacked.length === 0,
        unbacked.length ? `Not found in STAND source: ${unbacked.join(', ')}` : `${figures.length} figures checked: ${figures.join(', ')}`);
    } else {
      add('Every figure on the page appears on standaction.co.za', false, 'STAND source text not supplied');
    }
    await page.close();
  }

  // 4. Rendering at three widths
  const widths = [375, 768, 1440];
  for (const w of widths) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    const errors = [];
    page.on('pageerror', (e) => errors.push(`pageerror: ${e.message}`));
    page.on('console', (m) => { if (m.type() === 'error') errors.push(`console: ${m.text()}`); });
    page.on('requestfailed', (r) => { if (r.url().startsWith('http://127.0.0.1')) errors.push(`failed: ${r.url()}`); });
    await page.goto(base, { waitUntil: 'load' });
    // Scroll to the true bottom (lazy images grow the page as we go).
    for (let y = 0; y <= await page.evaluate(() => document.documentElement.scrollHeight); y += 500) {
      await page.evaluate((yy) => window.scrollTo(0, yy), y); await page.waitForTimeout(60);
    }
    // Force any remaining lazy images (closed dropdowns, hover photos) to load so we test the files themselves.
    await page.evaluate(() => Promise.all([...document.images].map((i) => { i.loading = 'eager'; return i.decode().catch(() => {}); })));
    await page.waitForTimeout(1000);
    const info = await page.evaluate(() => {
      const broken = [...document.images].filter((i) => !(i.complete && i.naturalWidth > 0)).map((i) => i.getAttribute('src'));
      const overflow = document.documentElement.scrollWidth - window.innerWidth;
      const hidden = [...document.querySelectorAll('.reveal')].filter((el) => getComputedStyle(el).opacity === '0').length;
      const fonts = [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family.replace(/"/g, ''));
      return { broken, overflow, hidden, fonts: [...new Set(fonts)] };
    });
    // Treat network errors for third-party hosts as environmental, not page bugs.
    const realErrors = errors.filter((e) => !/fonts\.googleapis|fonts\.gstatic|ERR_TUNNEL|ERR_PROXY|net::ERR_FAILED/.test(e));
    add(`${w}px: no JS errors or failed local requests`, realErrors.length === 0, realErrors.length ? realErrors.slice(0, 5).join(' | ') : 'clean');
    add(`${w}px: no horizontal page scroll`, info.overflow <= 0, `overflow ${info.overflow}px`);
    add(`${w}px: every image loads`, info.broken.length === 0, info.broken.length ? info.broken.join(', ') : `${await page.evaluate(() => document.images.length)} images loaded`);
    add(`${w}px: all reveal elements become visible after scrolling`, info.hidden === 0, `${info.hidden} still hidden`);
    add(`${w}px: brand fonts load (Bonvivant, Handwritten)`, info.fonts.includes('Bonvivant') && info.fonts.includes('Handwritten'), `loaded: ${info.fonts.join(', ')}`);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(SHOTS, `remake-${w}.png`), fullPage: true });
    await page.close();
  }

  // 5. Interactions
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(base, { waitUntil: 'load' });
    const before = await page.$eval('.slide.is-active .stmt', (e) => e.textContent);
    await page.click('.slider-arrow.next');
    await page.waitForTimeout(700);
    const after = await page.$eval('.slide.is-active .stmt', (e) => e.textContent);
    add('Recognition slider advances', before !== after, `"${before.slice(0, 30)}..." -> "${after.slice(0, 30)}..."`);

    await page.click('.nav-item:nth-of-type(1) .nav-toggle');
    await page.waitForTimeout(400);
    const ddVisible = await page.$eval('#dd-focus', (e) => getComputedStyle(e).visibility === 'visible');
    add('Desktop dropdown opens on click', ddVisible, ddVisible ? 'visible' : 'not visible');
    await page.keyboard.press('Escape');


    await page.click('#contact-form button[type=submit]');
    const msg = await page.$eval('#contact-form .form-status', (e) => e.textContent);
    add('Contact form validates empty submission', /Please fill in/.test(msg), msg || 'no message');
    await page.close();

    const m = await browser.newPage({ viewport: { width: 375, height: 800 } });
    await m.goto(base, { waitUntil: 'load' });
    await m.click('#burger');
    await m.waitForTimeout(400);
    const menuVisible = await m.$eval('#nav-menu', (e) => getComputedStyle(e).visibility === 'visible');
    add('Mobile menu opens from burger', menuVisible, menuVisible ? 'visible' : 'not visible');
    await m.close();
  }

  await browser.close();
  srv.close();

  const allPass = results.every((r) => r.pass);
  const rows = results.map((r) => `| ${r.pass ? 'PASS' : 'FAIL'} | ${r.name} | ${String(r.detail).replace(/\|/g, '\\|')} |`).join('\n');
  const diffs = Object.entries(ALLOWED_DIFFS).filter(([k]) => !usedText.includes(norm(k))).map(([k, v]) => `- "${k}": ${v}`).join('\n');
  const report = `# STAND homepage report (layout from the to-top.ch/en remake, STAND pictures and copy)

Generated: ${new Date().toISOString()}

| Result | Check | Detail |
|---|---|---|
${rows}

Screenshots: \`screenshots/remake-375.png\`, \`screenshots/remake-768.png\`, \`screenshots/remake-1440.png\`

## Status
${allPass ? 'REMAKE COMPLETE' : `NOT COMPLETE: ${results.filter((r) => !r.pass).length} check(s) failing`}
`;
  fs.writeFileSync(path.join(ROOT, 'REMAKE_REPORT.md'), report);
  console.log(report);
  process.exit(allPass ? 0 : 1);
})();
