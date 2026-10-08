# LOCAL LONG LIFE インターンシップ チラシ（A4 1枚）

LPをベースにしたチラシです。

- `index.html` … 元データ（ブラウザで開く／印刷でPDF化できます）
- `flyer.pdf` … 印刷用 A4 PDF（1ページ）
- `flyer.png` … 約300dpiのプレビュー画像
- `assets/` … 画像素材

## 公開前に差し替える箇所
- 申込フォームのQRコードとURL（`index.html` の `.qr` / `.entry__url`）
- お問い合わせ先（`.brand`）
- 交通費補助の上限・条件

## PDFの作り直し
`index.html` を編集後、Chromiumで A4・背景グラフィックありで印刷（`@page` でA4指定済み）。
