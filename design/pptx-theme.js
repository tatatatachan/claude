// スライドのデザイン定義（design/slide-rules.md と対応）。色・ヘッダーはここだけに書く。
const F = "Arial";
const PALETTE = {
  MINT: "55C5B0", MINTM: "70CEBC", LIGHT: "DBF2E2", SHADOW: "BFE4D3",
  TEAL: "2F9D89", ORANGE: "F28A3C", NAVY: "323042", SUB: "6B6A7A", WHITE: "FFFFFF",
};
const FOOT = "Copyright © PARADOX Corporation. All Right Reserved.";

// pres: pptxgenjs の Presentation。ヘッダー帯・タイトル・フッターを描いたスライドと、テキスト用ヘルパーTを返す。
function chrome(pres, eyebrow, title, src) {
  const { MINT, MINTM, NAVY, SUB, WHITE } = PALETTE;
  const s = pres.addSlide();
  s.background = { color: WHITE };
  const T = (t, x, y, w, h, o = {}) =>
    s.addText(t, Object.assign({ x, y, w, h, fontFace: F, fontSize: 14, color: NAVY, margin: 0, valign: "middle", isTextBox: true }, o));
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 1.25, fill: { color: MINT }, line: { color: MINT, width: 0 } });
  s.addShape(pres.ShapeType.triangle, { x: 9.3, y: 0.25, w: 2.6, h: 1.0, fill: { color: MINTM }, line: { color: MINTM, width: 0 } });
  s.addShape(pres.ShapeType.triangle, { x: 11.2, y: 0.55, w: 2.1, h: 0.7, fill: { color: MINTM }, line: { color: MINTM, width: 0 } });
  s.addShape(pres.ShapeType.ellipse, { x: -1.5, y: 1.12, w: 8, h: 0.5, fill: { color: WHITE }, line: { color: WHITE, width: 0 } });
  s.addShape(pres.ShapeType.ellipse, { x: 6.5, y: 1.14, w: 8, h: 0.5, fill: { color: WHITE }, line: { color: WHITE, width: 0 } });
  T(eyebrow, 0.6, 0.2, 8, 0.3, { fontSize: 12, bold: true, color: WHITE, charSpacing: 4 });
  T(title, 0.6, 0.5, 12, 0.65, { fontSize: 30, bold: true, color: WHITE });
  T(FOOT, 0.6, 7.08, 8, 0.28, { fontSize: 10, color: SUB });
  T(src, 8.0, 7.08, 4.73, 0.28, { fontSize: 10, color: SUB, align: "right" });
  return { s, T };
}

// 行の区切り線（ミントの点線）
function dottedLine(pres, s, x, y, w) {
  s.addShape(pres.ShapeType.line, { x, y, w, h: 0, line: { color: PALETTE.MINT, width: 1.25, dashType: "sysDot" } });
}

module.exports = { F, PALETTE, FOOT, chrome, dottedLine };
