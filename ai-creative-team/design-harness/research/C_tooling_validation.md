# C. デザインハーネス向け 既存ツールと検証データ調査(2026-10-25時点)

> ⚠ 調査メモ(2026-10-25)。WebFetchの要約と検索スニペットに基づく。「未確認」「[S]=検索スニペットのみ」の項目は事実として使わないこと。原文の逐語確認はしていない。

凡例: [R]=URLを実際に取得して読んだ / [S]=検索結果の要約のみ(本文未取得、要裏取り) / 取得失敗は「未確認」。数値は読んだ出典のみ。

## 出典一覧(表)

| # | 区分 | 出典URL | 状態 |
|---|---|---|---|
| 1 | Figma MCP公式ヘルプ | https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server | R |
| 2 | Figma Code Connect | https://developers.figma.com/docs/code-connect/ | R |
| 3 | DTCG フォーマット草案 | https://www.designtokens.org/tr/drafts/format/ | R(末尾約1.5万字は未読) |
| 4 | Storybook MCP | https://storybook.js.org/docs/ai/mcp/overview | R |
| 5 | shadcn MCP | https://ui.shadcn.com/docs/mcp | R |
| 6 | llms.txt | https://llmstxt.org/ | R |
| 7 | AGENTS.md | https://agents.md/ | R |
| 8 | Google DESIGN.md発表 | https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/ | R |
| 9 | DESIGN.md仕様/CLI | https://github.com/google-labs-code/design.md | R |
| 10 | Atlassian DESIGN.md検証 | https://www.atlassian.com/blog/how-we-build/atlassians-design-md-is-here-what-we-learned-testing-portable-design-context-in-practice | R |
| 11 | Primer MCP | https://primer.style/product/getting-started/foundations/mcp | R |
| 12 | IBM Carbon MCP | https://carbondesignsystem.com/developing/carbon-mcp/overview/ | R |
| 13 | Shopify Dev MCP | https://shopify.dev/docs/apps/build/devmcp | R |
| 14 | 三菱電機 Serendie MCP/llms.txt | https://serendie.design/en/ai/mcp-server | R |
| 15 | kufu/smarthr-design-system(GitHub) | https://github.com/kufu/smarthr-design-system | R |
| 16 | Design Systems with Figma Tokyo 参加レポート(Zenn) | https://zenn.dev/perksh/articles/803aa65b75c67c | R(二次情報) |
| 17 | WCAG G18 | https://www.w3.org/WAI/WCAG22/Techniques/general/G18 | R |
| 18 | axe-core | https://github.com/dequelabs/axe-core | R |
| 19 | Lighthouse | https://developer.chrome.com/docs/lighthouse/overview | R |
| 20 | Playwright snapshots | https://playwright.dev/docs/test-snapshots | R |
| 21 | Chromatic Visual | https://www.chromatic.com/docs/visual | R |
| 22 | Design2Code | https://arxiv.org/abs/2403.03163 | R(抄録のみ) |
| 23 | MLLM as a UI Judge | https://arxiv.org/html/2510.08783v1 | R |
| 24 | ArtifactsBench | https://arxiv.org/html/2507.04952v2 | R(抄録のみ) |
| 25 | WebGen-V Bench | https://arxiv.org/pdf/2510.15306 | メタデータのみ(PDFで本文読めず) |
| 26 | 美的批評MLLM(2606.29689) | https://arxiv.org/abs/2606.29689 | R(抄録のみ) |
| S1 | Adobe Express Brand Check等 | 検索結果(business.adobe.com/products/express-business/pricing 等) | S。直接取得は503/403/404 |
| S2 | Canva Brand Kit/AIコネクタ | 検索結果(canva.com/help/brand-kit-best-practices/, /resources/connect-canva-to-ai-agent/) | S。直接取得は403 |
| S3 | Mozilla stylelint-plugin-mozilla | firefox-source-docs.mozilla.org(use-design-tokens系) | S |
| S4 | SmartHRのスキル型プラグイン | skillselion.com/marketplace/kufu/smarthr-design-system | S |

## AIに読ませる(デザインシステム/ブランドの機械可読化)

### Figma MCPサーバー [#1]
- 内容: Figma製。フレームのリンクを渡すと、変数・コンポーネント・レイアウトを開発環境へ渡す。キャンバスへの書き込み(Design/FigJam/Slides)、ブラウザUIのFigmaへの取り込み、FigJam内容とMakeのコードリソース取得、Figma Specs(open beta)、アップロード済みフォント参照にも対応。Code Connectの対応付けも再利用する。
- 状態: キャンバス書き込みはベータ中無料、将来は従量課金予定(日付の記載なし)。リモート版(mcp.figma.com/mcp)が推奨で最も機能が広い。デスクトップ版はDev/Fullシートが必要。個別ツール名は同ページになく別記事参照(未確認)。レート制限の数値は未確認。
- ハーネス利用: 「文脈」層。正本のFigmaから変数・コンポーネントをエージェントに供給。
- 限界: リンク単位の取得のため大画面は文脈過多になりうる(日本語記事 azukiazusa.dev が分割実装を勧めると検索要約に記載、[S])。Figma Makeそのものの仕様は本調査では一次取得できず未確認(MCPがMakeコードを取得できる点のみ[#1]で確認)。

### Code Connect [#2]
- Figma製。コード上のコンポーネントをFigmaコンポーネントへ対応付け、Dev Modeとエージェントに実コードを参照させる。CLI(TypeScriptテンプレート)とUI(GitHub連携、一対多可)がある。
- 制約: Dev/FullシートのProfessional以上。Professionalは有効なライブラリ1・フレームワーク1。
- ハーネス利用: 「AIが新規にUI部品を捏造しない」ための制約・文脈。コード実装が無いチーム(サムネ制作など)には直接は適用しにくい(筆者見解)。

### W3C DTCG トークン形式 [#3]
- Design Tokens Community Groupの「Draft Community Group Report」2026-09-08版。最新の公開版は2025.10。W3C標準ではなく標準化トラックにも載っていない。文書自体が「この版を実装しようとしないこと」と明記。
- 内容: 型必須(color, dimension, typography, shadow等)、エイリアス `{group.token}`、グループ、`$extends`(深いマージ)。テーマは読めた範囲では未確認。
- 利用: トークンの交換フォーマット(DESIGN.mdのexportもDTCG JSONに対応 [#9])。安定版を名乗れる段階ではない点に注意。

### Storybook MCP [#4]
- Storybook製。`@storybook/addon-mcp`で提供。コンポーネントmanifest(既定オフ、`componentsManifest: true`)をdocsツールが読む。ツール例: docs-list, docs-show, stories-preview, test-run, review-create。状態は「プレビュー」でAPIは変わりうると明記。
- 限界: manifest生成はReact系・Angular(vite)・Vue3(vite)のみ。他FWはdocsツールが使えない。
- 利用: コンポーネント実在確認と、a11yテスト実行を同じ窓口に集約。

### shadcn/ui レジストリ + MCP [#5]
- shadcn/ui公式。`components.json`のレジストリ(公式・第三者・非公開)を検索・インストールできる。独自レジストリに自社部品を載せ、エージェントの調達先を限定する使い方が可能。
- 限界: レジストリ仕様に準拠する必要。React/Tailwind系前提(筆者の理解、ページでは未確認)。

### llms.txt / AGENTS.md / DESIGN.md
- llms.txt [#6]: Jeremy Howard提唱、2024-09-03公開、最終更新2026-08-10。非公式の提案(v2)。H1+要約+リンク集のMarkdown。標準ではない。
- AGENTS.md [#7]: 現在はLinux Foundation傘下のAgentic AI Foundationが管理。公式ページ記載で6万超のOSSが採用(自己申告)。形式は自由なMarkdownで、最寄りのファイルが優先される。デザイン規則をここに書く運用が可能だが、デザイン専用の構造はない。
- DESIGN.md [#8][#9]: Google Labs(Stitch)が2026-04-21にドラフト仕様をオープンソース化。YAMLのトークン+Markdownの理由付け。CLI `@google/design.md` に lint(構造・参照切れ・WCAGコントラスト)、diff、export(Tailwind/DTCG)、spec。lintルールは11個(error 1/warning 7/info 3)。バージョンはalphaでスキーマ・CLIは変わりうる。Apache-2.0。
- Atlassianの検証 [#10](2026-06-15、同社自身の検証で結論は断定的でないと本人が断り書き): ログイン画面タスクで、平均トークンは MCP 3.75M、スキル 4.43M、DESIGN.md 7.21M、文脈なし 4.20M。「デザインシステム文脈の取り込み率」は同社の指標でMCP約80%、スキル約80%、DESIGN.md約30%、なし約5%。DESIGN.mdは80KB(約19,800トークン)で、全量を毎回読むためコスト増・既存部品の再作成が起きた。結論は「本番はMCP/スキル、可搬性・プロトタイプにDESIGN.md」。1社・1タスクの結果で一般化は不可。

### 各社デザインシステムのAI対応
- GitHub Primer [#11]: ローカルstdioの`@primer/mcp`。トークン検索(find_tokens)、コンポーネント例・利用/a11yガイド、`lint_css`(Primerトークン使用の検査)、`review_alt_text`など。Primer React/Octicons中心。
- IBM Carbon [#12]: Carbon MCP。トークン・コンポーネント・アイコン・ガイダンスを提供。パブリックプレビュー、非IBM社員はアクセス申請が必要(検索結果 [S]。取得ページは設定手順なし)。
- Shopify [#13]: Dev MCP(`@shopify/dev-mcp`)。Polaris網羅かは同ページで未確認。Polarisは`shopify`スキル側で言及とのこと。Shopify Polaris単独のAI対応は未確認。
- Material、Salesforce SLDS: 該当ページを確認できず未確認。
- 三菱電機 Serendie [#14]: リモートMCP(serendie.design/mcp)+ llms.txt / llms-full.txt + Agent Skills。MCPが使えない場合の代替としてllms.txtを案内。実装は`serendie/serendie-web`で公開と記載。

## 自動検証(決定的チェック)

- WCAGコントラスト [#17]: G18は通常テキストで4.5:1以上を求める技法。比率計算は完全に決定的で、ハーネスの最も堅い検証。ただしサムネ画像上の文字は背景が一様でなく、領域サンプリングの設計が要る(筆者見解)。
- axe-core [#18]: Deque製OSS(MPL-2.0)。READMEは「平均でWCAG問題の57%を自動検出」と記載(ベンダー自己申告)。判定不能は「incomplete」で返す。DOM前提でありラスター画像(サムネ)には使えない。
- Lighthouse [#19]: Google Chrome。性能・アクセシビリティ・ベストプラクティス・SEOに加え「Agentic browsing」(WebMCP、llms.txt発見性など)カテゴリが載っている。CIはLighthouse CIで可。スコア算出の詳細は別ページで未確認。
- トークン遵守lint: Mozillaの`stylelint-plugin-mozilla`に色をトークン変数に強制するルール群(use-design-tokens等)がある [S3]。ただしMozilla固有のトークン名前提。汎用の定番プラグインは今回確認できず未確認。PrimerのMCP `lint_css` [#11]、DESIGN.md lint [#9]、Figma「Check Design」(早期アクセス、ハードコード色/余白を検出とZenn報告 [#16])も同系統。
- 視覚回帰: Playwright `toHaveScreenshot` [#20] は初回に2回連続一致で基準画像を作り、以後pixelmatchで比較(threshold既定0.2、maxDiffPixels既定なし)。OS/ブラウザ差でレンダリングが変わるため同一環境で基準を作る必要。Chromatic [#21] はStorybookのstoryをクラウドで撮影し基準と比較、差分を人が承認。Percyは未取得で未確認。
- 限界: これらは「崩れていない/規約に合う」を測れるが、「良いデザインか」「ブランドらしいか」は測れない。画像生成物(サムネ)はDOM・トークンが無く、適用できるのはコントラスト、文字サイズ下限、セーフエリア、ロゴ配置など画像解析で自作する項目に限られる(筆者見解)。

## AIによる評価(研究とベンチマーク)

- Design2Code [#22]: 実在Webページ484件、スクリーンショット→コード。自動指標+人手評価。モデルは視覚要素の再現とレイアウトで苦戦と述べる。抄録に個別スコアなし。
- MLLM as a UI Judge [#23](arXiv 2510.08783): UI 30件、AMTによる人間評価(除外後9,296回答)、GPT-4o/Claude 3.5 Sonnet/Llama-3.2-11B。絶対評価はPearson 0.69〜0.73、±1以内の一致72〜77%、完全一致35〜38%。ペア比較の人間との一致はClaude 59.98%、GPT-4o 59.60%、Llama 52.96%で、人間スコア差が大きいと90〜93%、差が小さいとほぼ偶然。「美的快さ」は過小評価傾向。著者は「テストの近似であり代替ではない」と結論。論文内の数値に不整合があると取得要約が指摘(要注意)。静止画・西洋風プロ製UI中心・3モデルのみ。
- ArtifactsBench [#24]: 1,825タスク。チェックリスト誘導のMLLM審査が、WebDev Arenaとの順位一致94.4%、人間専門家とのペア一致最大90.95%(著者主張)。
- WebGen-V Bench [#25]: Kuang-Da Wangら、2025-10提出。本文は読めず内容は未確認。
- 美的批評(arXiv 2606.29689)[#26]: r/photocritique 1,227件。LLM審査は人間批評よりフロンティアモデル批評を好む傾向など。批評の実質は人間と「ほぼ別物」(1.81〜2.59/5)。抄録のみ。検索要約にあった「完全一致29〜35%」等の数値は本文未確認のため不採用。
- ハーネスへの含意: 審査モデルは大差の優劣判定には使えるが、僅差の判断・ブランドらしさ・「面白さ」の絶対評価は不安定。人間のゴールデンセット(合否例)で審査プロンプトを較正し、定期的に人間と一致率を測るべき(筆者見解)。

## 4層×既存ツール(表)

| 層 | 既存ツール(出典) | 使いどころ | 限界 |
|---|---|---|---|
| 制約 | DTCGトークン[#3]、DESIGN.md(YAML部)[#9]、Code Connect[#2]、shadcnレジストリ[#5]、Figma変数[#1] | 色・余白・文字の許容値と使用可能部品を機械可読化 | DTCGは草案、DESIGN.mdはalpha。画像制作向けのスキーマは無い |
| 文脈 | Figma MCP[#1]、Storybook MCP[#4]、Primer/Carbon/Serendie MCP[#11][#12][#14]、llms.txt[#6]、AGENTS.md[#7]、DESIGN.md(散文部)[#8] | 必要な規則・部品を必要な時だけ供給 | 全量投入はコスト増(Atlassian検証[#10]) |
| 検証 | WCAGコントラスト[#17]、axe-core[#18]、Lighthouse[#19]、DESIGN.md lint[#9]、Primer lint_css[#11]、stylelintトークン規則[S3]、Playwright[#20]、Chromatic[#21] | 決定的な合否判定。CIで自動化 | 美しさは測れない。サムネ(ラスター)には画像解析の自作が必要 |
| 評価 | MLLM審査(UI Judge[#23]、ArtifactsBench[#24])、Design2Code[#22]の自動指標 | 案の絞り込み、大差の優劣、ドラフト批評 | 僅差・美的判断は人間との一致が低い。最終判断は人間 |
| ブランド機能(参考) | Adobe Express Brand Check(「coming soon」と料金ページに表示とされる)[S1]、Canva Brand Kit/Brand Voice/AIコネクタ[S2] | 既存SaaS内の統制 | 本文を読めておらず仕様未確認 |

## 日本の事例

- 三菱電機 Serendie [#14][#16]: 公開MCP+llms.txt+スキル。Figmaプラグインで色・タイポ・命名の適合チェックを開発中(2026年度内に外部公開目標とZennが報告)。
- メルカリ DS4 [#16]: 意味を持つセマンティックトークンとCode Connectが「AIが毎回同じコードを出す土台」と登壇者が説明。「デザインシステムを使うとAI開発速度が2倍超になったプロジェクトが約半数」との発言は登壇者の主張を二次報告したもので未検証。
- SmartHR [#15][S4]: `kufu/smarthr-design-system`リポジトリにCLAUDE.md/AGENTS.md/プラグインフォルダがあることを確認。所有者がSmartHRと明記はなく、README内のNotionリンクから推定。公式MCP/llms.txtは確認できず。検索ではコミュニティ製のスキル型プラグインも見つかったが公式性は未確認。
- freee、LINE、Goodpatch: 該当情報を見つけられず未確認。

## 未確認

- 取得失敗: Adobe(adobe.com/express/learn/blog/brand-kit=404、business.adobe.com料金ページ=503、helpx.adobe.com=403)。Canva(brand-kit、help、AIコネクタ各ページ=403)。Adobe Brand CheckとCanvaの機能は検索要約のみで、厳密な仕様・提供状況は未確認。
- WebGen-V Bench本文、Design2Code個別スコア、UICrit系論文、Percy、Material/Salesforce/Polaris固有のAI対応、Figma Make仕様、freee/LINE/Goodpatch事例、汎用stylelintトークンプラグイン。
- DTCG草案の末尾約1.5万字(テーマ関連の有無)。
- 「ベンダー自己申告」の数値(axe 57%、Atlassian検証、ArtifactsBench一致率、メルカリ2倍)は第三者検証なし。
