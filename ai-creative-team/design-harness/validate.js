#!/usr/bin/env node
// デザインハーネス 第3層(検証): HTMLで組んだサムネ/ポスターの決定的チェック。
// 使い方: node validate.js <file.html> [--w 1280] [--h 720] [--rules rules.json] [--json out.json]
// 判定: FAIL(直す) / WARN(確認) / PASS。FAILがあれば終了コード1。
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const file = args.find(a => !a.startsWith('--') && a.endsWith('.html'));
const opt = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
if (!file) { console.error('usage: node validate.js <file.html> [--w W --h H --rules rules.json --json out.json]'); process.exit(2); }
const W = +opt('w', 1280), H = +opt('h', 720);
const rules = JSON.parse(fs.readFileSync(opt('rules', path.join(__dirname, 'rules.json')), 'utf8'));

const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
const ratio = (a, b) => { const [hi, lo] = a > b ? [a, b] : [b, a]; return (hi + 0.05) / (lo + 0.05); };

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.goto('file://' + path.resolve(file));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);

  // 1) テキスト要素の収集(要素直下のテキストノード)。各要素に data-vid を付ける
  const blocks = await page.evaluate(() => {
    const out = []; let n = 0;
    for (const el of document.querySelectorAll('body *')) {
      const nodes = [...el.childNodes].filter(x => x.nodeType === 3 && x.textContent.trim());
      if (!nodes.length) continue;
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
      el.setAttribute('data-vid', String(n));
      let dl = 1e9, dr = -1e9;
      for (const x of nodes) { const rg = document.createRange(); rg.selectNodeContents(x); for (const q of rg.getClientRects()) { if (q.width < 1) continue; dl = Math.min(dl, q.left); dr = Math.max(dr, q.right); } }
      out.push({ domL: dl, domR: dr, vid: n++, text: nodes.map(x => x.textContent.trim()).join(' ').slice(0, 40),
        fontSize: parseFloat(cs.fontSize), weight: cs.fontWeight, family: cs.fontFamily.split(',')[0].replace(/['"]/g, '').trim(), color: cs.color, wcolor: cs.webkitTextFillColor || cs.color });
    }
    return out;
  });
  // 2) 文字を1つずつだけ表示して撮る → 背景との差分=実際に描かれたインク(はみ出し/重なり/コントラストを正確に測る)
  const styleId = 'harness-style';
  const setStyle = css => page.evaluate(([id, c]) => { let t = document.getElementById(id); if (!t) { t = document.createElement('style'); t.id = id; document.head.appendChild(t); } t.textContent = c; }, [styleId, css]);
  const HIDE = '*{color:transparent !important;-webkit-text-fill-color:transparent !important;text-shadow:none !important;-webkit-text-stroke:0 !important}';
  await setStyle(HIDE);
  const bgShot = (await page.screenshot()).toString('base64');
  const shots = [];
  for (const b of blocks) {
    await setStyle(HIDE + `[data-vid="${b.vid}"]{color:${b.color} !important;-webkit-text-fill-color:${b.wcolor} !important}`);
    shots.push((await page.screenshot()).toString('base64'));
  }
  const probe = await browser.newPage();
  const ink = await probe.evaluate(async ({ bgShot, shots, W, H, colors }) => {
    const load = async b64 => { const im = new Image(); im.src = 'data:image/png;base64,' + b64; await im.decode(); const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const g = c.getContext('2d'); g.drawImage(im, 0, 0); return g.getImageData(0, 0, im.width, im.height); };
    const bg = await load(bgShot); const N = bg.width * bg.height; const sc = bg.width / W;
    const L = rgb => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(rgb[0]) + 0.7152 * f(rgb[1]) + 0.0722 * f(rgb[2]); };
    const masks = [], info = [];
    for (let k = 0; k < shots.length; k++) {
      const im = await load(shots[k]); const m = new Uint8Array(N); let l = 1e9, t = 1e9, r = -1, b = -1, cnt = 0; const bl = []; let faint = false;
      for (let pass = 0; pass < 2 && !cnt; pass++) {
       const TH = pass === 0 ? 60 : 12; faint = pass === 1;
       for (let i = 0, p = 0; i < N; i++, p += 4) {
        const d = Math.abs(im.data[p] - bg.data[p]) + Math.abs(im.data[p + 1] - bg.data[p + 1]) + Math.abs(im.data[p + 2] - bg.data[p + 2]);
        if (d > TH) { m[i] = 1; cnt++; const x = i % bg.width, y = (i / bg.width) | 0; if (x < l) l = x; if (x > r) r = x; if (y < t) t = y; if (y > b) b = y; if (cnt % 5 === 0) bl.push(L([bg.data[p], bg.data[p + 1], bg.data[p + 2]])); }
       }
      }
      bl.sort((a, c) => a - c);
      info.push(cnt ? { faint, l: l / sc, t: t / sc, r: (r + 1) / sc, b: (b + 1) / sc, cnt, p10: bl[Math.floor(bl.length * 0.1)], p90: bl[Math.min(bl.length - 1, Math.floor(bl.length * 0.9))] } : null);
      masks.push(m);
    }
    const pairs = [];
    for (let i = 0; i < masks.length; i++) for (let j = i + 1; j < masks.length; j++) {
      if (!info[i] || !info[j]) continue;
      if (info[i].r < info[j].l || info[j].r < info[i].l || info[i].b < info[j].t || info[j].b < info[i].t) continue;
      let inter = 0; for (let p = 0; p < N; p++) if (masks[i][p] & masks[j][p]) inter++;
      if (inter) pairs.push([i, j, inter / Math.min(info[i].cnt, info[j].cnt)]);
    }
    return { info, pairs };
  }, { bgShot, shots, W, H, colors: [] });
  await browser.close();

  // 3) 判定
  const R = rules, res = [];
  const add = (level, rule, msg) => res.push({ level, rule, msg });
  const maxFont = Math.max(...blocks.map(b => b.fontSize));
  const scale = R.thumbnail_display_width_px / W;
  const needPrimary = R.min_legible_px_at_display / scale;
  blocks.forEach((b, i) => {
    const k = ink.info[i]; const tag = `「${b.text}」(${Math.round(b.fontSize)}px)`;
    const isPrimary = b.fontSize >= maxFont * 0.7;
    if (b.fontSize < R.min_text_px_fail) add('FAIL', 'min-text', `${tag} は ${R.min_text_px_fail}px 未満で読めない`);
    else if (b.fontSize < R.min_text_px_warn) add('WARN', 'min-text', `${tag} は ${R.min_text_px_warn}px 未満(細かい注記。一覧では読めない前提)`);
    if (isPrimary && b.fontSize < needPrimary) add('FAIL', 'primary-size', `${tag} は主役の文字だが、一覧(幅${R.thumbnail_display_width_px}px)で ${R.min_legible_px_at_display}px 以上にするには ${Math.ceil(needPrimary)}px 以上が必要`);
    if (b.domL < -2 || b.domR > W + 2) add('FAIL', 'overflow', `${tag} が横方向にキャンバスからはみ出している(DOM上で ${Math.round(b.domL)}〜${Math.round(b.domR)}px)`);
    if (!k) { add('FAIL', 'invisible', `${tag} は描画されていない(背景と同色か、画面外)`); return; }
    if (k.faint) add('FAIL', 'invisible', `${tag} は背景との差がほとんどなく、ほぼ読めない(白背景に白字など)`);
    const m = W * R.safe_margin_pct / 100;
    if (k.l < -1 || k.t < -1 || k.r > W + 1 || k.b > H + 1) add('FAIL', 'overflow', `${tag} の文字がキャンバスからはみ出している`);
    else if (k.l < m || k.t < m || k.r > W - m || k.b > H - m) add('WARN', 'safe-margin', `${tag} が端から ${R.safe_margin_pct}% 以内(動画の時間表示や切り抜きで欠ける)`);
    const cc = (b.wcolor.match(/[\d.]+/g) || []).map(Number); const alpha = cc.length > 3 ? cc[3] : 1;
    const tl = lum(cc.slice(0, 3));
    const worst = Math.min(ratio(tl, k.p10), ratio(tl, k.p90));
    const need = b.fontSize >= R.large_text_px ? R.contrast_min_large : R.contrast_min_normal;
    // 半透明の文字色は、背景輝度との混合で実効コントラストを概算する(輝度空間での近似)
    const eff = alpha < 1 ? Math.min(...[k.p10, k.p90].map(bl => ratio(alpha * tl + (1 - alpha) * bl, bl))) : worst;
    if (eff < need) add('FAIL', 'contrast', `${tag} のコントラスト比が約 ${eff.toFixed(1)}:1(必要 ${need}:1)${alpha < 1 ? '。半透明の文字色なので概算' : ''}`);
  });
  ink.pairs.forEach(([i, j, f]) => { if (f > R.overlap_fail_ratio) add('FAIL', 'overlap', `「${blocks[i].text}」と「${blocks[j].text}」の文字が重なっている(小さい方の ${(100 * f).toFixed(0)}%)`); });
  const fams = new Set(blocks.map(b => b.family));
  if (fams.size > R.max_font_families_warn) add('WARN', 'fonts', `フォントが ${fams.size} 種類(${[...fams].join(', ')})`);
  if (blocks.length > R.max_text_blocks_warn) add('WARN', 'density', `テキストのかたまりが ${blocks.length} 個(情報が多い)`);

  const fails = res.filter(r => r.level === 'FAIL').length, warns = res.filter(r => r.level === 'WARN').length;
  console.log(`${path.basename(file)}  ${fails ? 'FAIL' : warns ? 'WARN' : 'PASS'}  (FAIL ${fails} / WARN ${warns} / 文字 ${blocks.length} 個)`);
  res.forEach(r => console.log(`  [${r.level}] ${r.rule}: ${r.msg}`));
  const jo = opt('json', null); if (jo) fs.writeFileSync(jo, JSON.stringify({ file, fails, warns, results: res }, null, 2));
  process.exit(fails ? 1 : 0);
})();
