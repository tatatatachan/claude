// 例：事業所アンケート表と実績まとめ。色とヘッダーは pptx-theme.js と同じ定義を、このファイル内に持っている（単体で動かすため）。
// 使い方: FS=14 node example-build.js（pptxgenjs が必要）
const pptxgen = require("pptxgenjs");
const F="Arial";
// palette (イベントの流れ／この体験で得られる3つのこと／Program 図版より)
const MINT="55C5B0", MINTM="70CEBC", LIGHT="DBF2E2", SHADOW="BFE4D3", TEAL="2F9D89", ORANGE="F28A3C", NAVY="323042", SUB="6B6A7A", WHITE="FFFFFF";
const FOOT="Copyright © PARADOX Corporation. All Right Reserved.";

function chrome(pres,eyebrow,title,src){
  const s=pres.addSlide(); s.background={color:WHITE};
  const T=(t,x,y,w,h,o={})=>s.addText(t,Object.assign({x,y,w,h,fontFace:F,fontSize:14,color:NAVY,margin:0,valign:"middle",isTextBox:true},o));
  // header band + mountains + soft wave
  s.addShape(pres.ShapeType.rect,{x:0,y:0,w:13.333,h:1.25,fill:{color:MINT},line:{color:MINT,width:0}});
  s.addShape(pres.ShapeType.triangle,{x:9.3,y:0.25,w:2.6,h:1.0,fill:{color:MINTM},line:{color:MINTM,width:0}});
  s.addShape(pres.ShapeType.triangle,{x:11.2,y:0.55,w:2.1,h:0.7,fill:{color:MINTM},line:{color:MINTM,width:0}});
  s.addShape(pres.ShapeType.ellipse,{x:-1.5,y:1.12,w:8,h:0.5,fill:{color:WHITE},line:{color:WHITE,width:0}});
  s.addShape(pres.ShapeType.ellipse,{x:6.5,y:1.14,w:8,h:0.5,fill:{color:WHITE},line:{color:WHITE,width:0}});
  s.addShape(pres.ShapeType.rect,{x:0,y:7.38,w:13.333,h:0.12,fill:{color:"FFFFFF"},line:{color:"FFFFFF",width:0}});
  T(eyebrow,0.6,0.2,8,0.3,{fontSize:12,bold:true,color:WHITE,charSpacing:4});
  T(title,0.6,0.5,12,0.65,{fontSize:30,bold:true,color:WHITE});
  T(FOOT,0.6,7.08,8,0.28,{fontSize:10,color:SUB});
  T(src,8.0,7.08,4.73,0.28,{fontSize:10,color:SUB,align:"right"});
  return {s,T};
}
const X0=0.6, TW=12.13;
{
  const FS=+(process.env.FS||14);
  const X=[X0,4.3,8.55], W=[3.5,4.1,4.18];
  function lines(t,w,fs){ const cpl=Math.max(1,Math.floor(w/(fs*0.0135))); return t.split("\n").reduce((a,p)=>a+Math.max(1,Math.ceil(p.length/cpl)),0); }
  const prog="レクリエーションの実施・食事やお茶の準備、提供・利用者様とのコミュニケーション";
  const goal="・今回の佐久大学の実習に関しては、対象の利用者様を1人決め、会話や介護の中から、アセスメントを行い、ケアプランを立てることを目的としている。\n・毎年8～9月頃に大学側から事業所へ電話があり、受けている。";
  const items=[
   ["sec","基本情報"],
   ["row","担当者名・役職","中澤所長","江原所長"],
   ["row","時間","9:30～13:30","9:30～13:30"],
   ["row","3日間のタイムスケジュール","9:30～バイタルチェック\n9:45～お茶の時間 対応\n10:00～レク・体操\n11:00～昼食準備・配膳等","9:30～お茶の時間 対応\n10:00～レク・体操・入浴\n11:30～口腔体操\n12:00～昼食"],
   ["note","※実習中の学生の動き、担当者の指導している姿など、お写真を撮影ください（外部には公開いたしません）"],
   ["sec","1. 受入体制・事前準備について"],
   ["row","事前オリエンテーション・研修の有無","なし","なし"],
   ["row","初日または事前の、注意事項・個人情報保護・マナーの説明","初日の最初の時間に注意事項等を説明","なし"],
   ["row","指導担当者（バイザー）の配置","なし","あり"],
   ["row","特定の指導担当者か、日替わり・業務ごとか","なし","日替わり（出勤している者で対応）"],
   ["row","事前共有資料・日誌の有無","事業所パンフレットを配布","なし"],
   ["row","日誌・振り返りの時間、提出用フォーマットの指定","指定なし","指定なし"],
   ["sec","2. 実習の具体的な実施内容について"],
   ["row","学年・対象（高校生／大学生）による内容の差","基本的には同じ業務を行っている","内容の差なし"],
   ["row","高校生と大学生での、プログラム・任せる業務範囲の違い","なし","なし"],
   ["row","体験・見学・実務の比率","90％以上実務","実務100％"],
   ["row","主な実施プログラム・業務内容","事業所の日程に合わせて、介護業務を行ってもらう","事業所の日程に合わせて、介護業務を行ってもらう"],
   ["row","含まれる具体的なプログラム",prog,prog],
   ["row","3日間の割合（見学・講義／見守り・コミュニケーション／身体介護等の補助／間接業務・事務作業）","90％以上「見守り・コミュニケーション」・「身体介護等の補助」","100％「見守り・コミュニケーション」"],
   ["sec","3. 安全管理・リスク対応について"],
   ["row","事故・トラブル時の対応手順","状況に応じて地区担当に連絡し、指示を仰ぐ\n注意が必要な利用者様の情報は事前に伝える","地区担当へ相談\n大学へ報告"],
   ["row","怪我・体調不良・利用者とのトラブル時の報告ルート","地区担当へ報告","地区担当へ連絡"],
   ["row","保険の適用・加入状況","なし","なし"],
   ["row","実習生用の保険（傷害・賠償責任）の加入確認","なし","なし"],
   ["sec","4. 評価・フィードバックについて"],
   ["row","実習後の振り返り・評価シート","なし","なし"],
   ["row","終了時の学生へのフィードバック面談、学校提出用の評価シート記入","一日の最後に面談を実施","なし"],
   ["row","学生からのアンケート・改善フィードバック","なし","なし"],
   ["row","実習終了後に学生から感想や改善点を聞く機会（アンケート等）","なし","最後にお話をする程度"],
   ["sec","5. そのほか（全事業所で標準化していくために、お伝えしきれていないこと）"],
   ["span","両事業所の回答（同じ内容）",goal]
  ];
  const H=it=>{
    if(it[0]==="sec") return 0.45;
    if(it[0]==="note") return 0.38;
    if(it[0]==="span") return Math.max(0.44,(lines(it[1],W[0],FS)>0?Math.max(lines(it[1],W[0],FS),lines(it[2],W[1]+W[2]+0.2,FS)+1):1)*FS*0.0175+0.1);
    return Math.max(0.44,Math.max(lines(it[1],W[0],FS),lines(it[2],W[1],FS),lines(it[3],W[2],FS))*FS*0.0175+0.1);
  };
  const TOP=2.1, BOT=6.95;
  const pages=[[]]; let used=0, curSec=null;
  items.forEach(it=>{
    const h=H(it);
    if(it[0]==="sec"){ curSec=it[1]; if(used+h+0.5>BOT-TOP){pages.push([]);used=0;} pages[pages.length-1].push({it,h}); used+=h; return; }
    if(used+h>BOT-TOP){ pages.push([]); used=0; pages[pages.length-1].push({it:["sec",curSec+"（続き）"],h:0.45}); used+=0.45; }
    pages[pages.length-1].push({it,h}); used+=h;
  });
  const N=pages.length;
  const pres=new pptxgen(); pres.layout="LAYOUT_WIDE";
  pages.forEach((pg,pi)=>{
    const {s,T}=chrome(pres,"QUESTIONNAIRE",`事業所アンケートの回答　${pi+1} / ${N}`,"出典：採用管理シート「実習」");
    const hy=1.5;
    s.addShape(pres.ShapeType.line,{x:X0,y:hy+0.5,w:TW,h:0,line:{color:TEAL,width:2}});
    T("あったかホーム中込",X[1],hy,W[1],0.45,{bold:true,color:TEAL,fontSize:15});
    T("あったかホームあさま",X[2],hy,W[2],0.45,{bold:true,color:TEAL,fontSize:15});
    let y=TOP-0.05;
    pg.forEach(({it,h})=>{
      if(it[0]==="sec"){
        T(it[1],X0,y+0.05,TW,0.36,{fontSize:FS+2,bold:true,color:TEAL});
      } else if(it[0]==="note"){
        T(it[1],X0,y,TW,h,{fontSize:12,color:SUB});
      } else if(it[0]==="span"){
        T(it[1],X[0],y,W[0],h,{bold:true,fontSize:FS});
        T(it[2],X[1],y,W[1]+W[2]+0.2,h,{fontSize:FS});
        s.addShape(pres.ShapeType.line,{x:X0,y:y+h,w:TW,h:0,line:{color:MINT,width:1.25,dashType:"sysDot"}});
      } else {
        T(it[1],X[0],y,W[0],h,{bold:true,fontSize:FS});
        T(it[2],X[1],y,W[1],h,{fontSize:FS});
        T(it[3],X[2],y,W[2],h,{fontSize:FS});
        s.addShape(pres.ShapeType.line,{x:X0,y:y+h,w:TW,h:0,line:{color:MINT,width:1.25,dashType:"sysDot"}});
      }
      y+=h;
    });
    console.log("page",pi+1,"ends",y.toFixed(2));
  });
  console.log("pages",N,"FS",FS);
  pres.writeFile({fileName:"jisshu-questionnaire-table.pptx"}).then(()=>console.log("ok table"));
}
{
  const pres=new pptxgen(); pres.layout="LAYOUT_WIDE";
  const {s,T}=chrome(pres,"RESULTS","実習実績のまとめ","出典：採用管理シート「実習実績」");
  s.addChart(pres.charts.BAR,[{name:"確定受入人数",labels:["2016頃","2018","2020","2021","2022","2023","2024","2025","2026(7月)"],values:[2,1,1,6,13,1,4,11,1]}],{
    x:0.7,y:1.6,w:6.0,h:4.7,barDir:"col",chartColors:[MINT],showValue:true,dataLabelFontSize:15,dataLabelColor:NAVY,dataLabelFontFace:F,dataLabelPosition:"outEnd",
    catAxisLabelFontSize:12,catAxisLabelColor:SUB,catAxisLabelFontFace:F,valAxisHidden:true,valGridLine:{style:"none"},catGridLine:{style:"none"},
    showLegend:false,showTitle:true,title:"確定受入人数（名）　記録のない年は省略",titleFontSize:13,titleColor:SUB,titleFontFace:F,barGapWidthPct:55});
  T("2025年は「11名＋α」。2026年は7月時点の確定分。2022年のピークはエクセラン高校8名ほか。",0.9,6.3,5.8,0.6,{fontSize:12,color:SUB});
  const X=7.1,W=5.55;
  const secs=[
   ["主な受入校","高校：エクセラン高校、上田西高校、東御清翔高校、丸子修学館高校、柏崎常盤高校、地球環境高校\n看護・医療系：松本看護大学、佐久大学、深谷大里看護専門学校、長野医療衛生専門学校\n福祉・その他：長岡こども福祉カレッジ、アミカレッジ、大東文化大学",1.85],
   ["受入事業所","約80事業所のうち約20（概数）。佐久・小諸・上田・長野・松本・新潟・栃木・埼玉に実績があり、群馬は実績なし。",0.95],
   ["毎年の定期受入","約15〜17名枠。中込 約5〜6名、あさま 6名、新戒・深谷 各1〜2名。",0.8],
   ["入職","記録上は柏崎常盤高校の1名（2016年頃、翌年に入職）。",0.7],
   ["2026年秋の予定","松本看護大学 8名（2名×4グループ）、佐久大学 4名、地球環境高校 2名、深谷大里看護専門学校（通年）、アミカレッジ。",0.95]];
  let y=1.6;
  secs.forEach((c,i)=>{
    s.addText([{text:c[0],options:{bold:true,color:TEAL,fontSize:15,breakLine:true}},{text:c[1],options:{fontSize:12.5,color:NAVY}}],
      {x:X,y,w:W,h:c[2],fontFace:F,margin:0,valign:"middle",isTextBox:true,paraSpaceAfter:3});
    y+=c[2];
    if(i<secs.length-1) s.addShape(pres.ShapeType.line,{x:X,y,w:W,h:0,line:{color:MINT,width:1.25,dashType:"sysDot"}});
  });
  console.log("summary ends",y.toFixed(2));
  pres.writeFile({fileName:"jisshu-summary-slide.pptx"}).then(()=>console.log("ok summary"));
}
