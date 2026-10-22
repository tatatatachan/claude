import build_pptx3 as m3
b=m3.b
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt
INK,SUB,TEAL,TEAL2,TEALD,ORG,ORGD=m3.INK,m3.SUB,m3.TEAL,m3.TEAL2,m3.TEALD,m3.ORG,m3.ORGD
card,num,note=m3.card,m3.circle_num,m3.note
n0=len(b.prs.slides)

# ---------- A: 介護への考え方 ----------
sl=m3.new_slide('介護への考え方','エフビー介護サービスの、介護への考え方','創業からの想いと、介護で大切にしている姿勢。出典：エフビー介護サービス 企業説明会資料、経営者ヒアリング。')
card(64,176,1602,150)
b.text(104,192,400,28,'わたしたちの夢',20,SUB,True,spacing=2,name='夢ラベル')
b.text(104,222,1500,56,'人生の最終ステージを、利用者様の幸せと満足で元気にする',40,TEALD,True,name='夢')
b.text(104,284,1500,30,'利用者様の笑顔と、数多くの「ありがとう」を求め、喜ばれること',23,INK,name='夢補足')
def panel(x,w,title,rows,col):
    card(x,346,w,516)
    b.text(x+36,364,w-72,36,title,28,INK,True,name=f'見出し_{title}')
    for i,txt in enumerate(rows):
        y=422+i*144
        if i: 
            ln=b.sh.add_connector(1,b.px(x+36),b.px(y-14),b.px(x+w-36),b.px(y-14)); ln.line.color.rgb=b.rgb('E3ECE8'); ln.line.width=Pt(1.2)
        num(x+36,y+10,56,i+1,col if i<2 or col!=ORG else ORG,28)
        b.text(x+116,y,w-160,120,txt,23,INK,anchor=MSO_ANCHOR.TOP,ls=1.35,name=f'{title}_{i+1}')
panel(64,780,'創業からの想い',['経営理念と介護方針を基本として、利用者様とご家族の安心感と満足を目指します','心の温かい法人、事業所、そして心の優しい人間の集団になります','利用者様に喜ばれる介護サービスと介護用品を提供し、スピーディーな対応に専心する社員になります'],TEAL2)
panel(886,780,'大切にしている姿勢',['利用者様を「お客様」として敬い、その人としての尊厳を大切にします','「自分の親を面倒見るつもりで」。笑顔・言葉づかい・態度の接遇に力を入れています','介護する人・される人の区別なく、できることを持ち寄る。「誰かのためにはたらき、笑顔とありがとうをいただく」ことが生きがいになります'],ORG)
note('出典：エフビー介護サービス 企業説明会資料／経営者ヒアリング（2025年）。文言は要約しています。')
m3.post(sl); m3.finish(sl)

# ---------- B: 小規模 × 多拠点 ----------
sl=m3.new_slide('事業の展開（1）','大規模ではなく、小規模な施設を、地域ごとに広げる','わたしたちのちょっとしたこだわり。小規模な施設をメインに、信越・北関東に7種109拠点。')
p=b.rect(64,176,800,340,TEAL,MSO_SHAPE.ROUNDED_RECTANGLE,0.06); p.name='こだわり'
b.text(104,200,700,30,'わたしたちのちょっとしたこだわり',22,'EAF8F4',True,spacing=2,name='こだわりラベル')
b.text(104,240,720,130,['大規模な施設ではなく、','小規模な施設をメインに展開する。'],42,'FFFFFF',True,ls=1.2,name='こだわり本文')
b.text(104,392,720,110,['地域に深く根ざし、地域の文化・風土を取り入れた、','きめ細やかなサービスを届けています。','住み慣れた地元で、長く生活できる環境が「生きる力」に。'],21,'FFFFFF',ls=1.4,name='こだわり補足')
card(900,176,766,340)
b.text(940,196,600,34,'多拠点で、地域に根ざす',26,INK,True,name='多拠点見出し')
b.text(940,240,200,90,'109',78,TEALD,True,name='拠点数'); b.text(1100,278,200,40,'拠点',28,INK,True,name='拠点単位')
b.text(1280,262,360,40,'7種のサービス',26,ORGD,True,name='サービス数')
for i,(pf,n) in enumerate([('長野県',57),('新潟県',15),('埼玉県',15),('群馬県',12),('栃木県',10)]):
    x=940+i*142
    chip=b.rect(x,370,128,110,'E3F4F0' if i else 'FDEBDC',MSO_SHAPE.ROUNDED_RECTANGLE,0.18); chip.name=f'県_{pf}'
    b.text(x,380,128,30,pf,19,ORGD if i==0 else TEALD,True,PP_ALIGN.CENTER,name=f'県名_{pf}')
    b.text(x,410,128,60,str(n),44,ORGD if i==0 else TEALD,True,PP_ALIGN.CENTER,name=f'県数_{pf}')
b.text(64,540,1000,34,'暮らし方に合わせて選べる、3つのかたち',28,INK,True,name='3つのかたち見出し')
cols=[('自宅で暮らし続ける','自宅での生活を支援',['居宅介護支援','訪問介護'],TEAL2),('住まいで暮らす','居住いただき、支援する',['有料老人ホーム','グループホーム（少人数で暮らす、家庭的な雰囲気）'],TEAL2),('通い・訪問・泊まりを組み合わせる','小規模多機能で、暮らしを支える',['小規模多機能型居宅介護','看護小規模多機能型（看護も組み合わせ）'],ORG)]
for i,(h,s,items,c) in enumerate(cols):
    x=64+i*544; card(x,586,514,278)
    b.rect(x+30,610,8,60,c,MSO_SHAPE.ROUNDED_RECTANGLE,0.5).name='色バー'
    b.text(x+54,606,440,34,h,24 if len(h)<12 else 22,TEALD if c!=ORG else ORGD,True,name=f'見出し_{h}')
    b.text(x+54,642,440,30,s,19,SUB,name=f'補足_{h}')
    b.text(x+36,700,450,150,['・'+t for t in items],21,INK,ls=1.5,name=f'内容_{h}')
note('※ このほか、デイサービス（通い）・訪問看護で7種。出典：企業説明会資料、経営者ヒアリング、実習サイトの掲載内容。')
m3.post(sl); m3.finish(sl)

# ---------- C: 事業展開の歩み ----------
sl=m3.new_slide('事業の展開（2）','福祉用具から介護サービスへ。事業を広げてきた歩み','福祉用具レンタル・販売と各種介護サービスの2本柱で拡大。2022年4月東証スタンダード上場。')
steps=[('はじまり','福祉用具のレンタル・販売','フランスベッドの代理店が原点。2000年に福祉レンタルを開始',TEAL2),
       ('自宅を支える','居宅介護支援・訪問介護','自宅での生活を支援するサービスへ',TEAL2),
       ('住まいと暮らしを支える','老人ホーム・グループホーム・小規模多機能','居住の支援と、通い・訪問・泊まりの組み合わせへ',TEAL2),
       ('2022年4月','東証スタンダード市場に上場','事業成長の加速へ。信越・北関東に7種109拠点',ORG)]
for i,(t,h,d,c) in enumerate(steps):
    x=64+i*410; card(x,176,372,300)
    b.rect(x+30,200,70,8,c,MSO_SHAPE.ROUNDED_RECTANGLE,0.5).name='色バー'
    b.text(x+30,222,320,30,t,20,SUB,True,spacing=1,name=f'時期_{i+1}')
    b.text(x+30,258,316,100,h,24,TEALD if c!=ORG else ORGD,True,ls=1.2,name=f'見出し_{i+1}')
    b.text(x+30,372,316,90,d,19,INK,ls=1.35,name=f'説明_{i+1}')
    if i<3:
        a=b.sh.add_shape(MSO_SHAPE.RIGHT_ARROW,b.px(x+376),b.px(310),b.px(30),b.px(44)); b.fill(a,'2E9E8A'); b.noline(a); a.name='矢印'
card(64,504,780,360)
b.text(100,522,700,34,'売上は、10年で約2.4倍に',26,INK,True,name='売上見出し')
maxh=170
for i,(yr,v,col) in enumerate([('2013年',39,TEAL2),('2023年',92,ORG)]):
    h=int(maxh*v/92); x=160+i*300
    b.rect(x,780-h,200,h,col,MSO_SHAPE.RECTANGLE).name=f'棒_{yr}'
    b.text(x,780-h-46,200,40,f'{v}億円',32,TEALD if i==0 else ORGD,True,PP_ALIGN.CENTER,name=f'売上_{yr}')
    b.text(x,788,200,30,yr,20,SUB,True,PP_ALIGN.CENTER,name=f'年_{yr}')
card(884,504,782,360)
b.text(920,522,700,34,'これからの成長戦略',26,INK,True,name='戦略見出し')
blocks=[('福祉用具事業','自社仕入レンタル品販売の拡充／新規利用者様の開拓'),('介護事業','事業所運営方法の見直し／新たな介護サービスへの挑戦／ニーズにあったきめ細やかなサービスの提供'),('あわせて','同業種を対象としたM&Aで業績拡大を図る')]
y=576
for k,(h,d) in enumerate(blocks):
    chip=b.rect(920,y,150,42,'E3F4F0' if k<2 else 'FDEBDC',MSO_SHAPE.ROUNDED_RECTANGLE,0.5); chip.name=f'タグ_{h}'
    b.text(920,y,150,42,h,19,TEALD if k<2 else ORGD,True,PP_ALIGN.CENTER,MSO_ANCHOR.MIDDLE,name=f'タグ文字_{h}')
    b.text(1090,y-2,550,100,d,20,INK,ls=1.35,name=f'戦略_{h}')
    y+=100 if k==1 else 84
note('※ 開始年は経営者ヒアリング、売上は企業説明会資料、成長戦略は2026年3月期 決算説明資料に基づきます（数値は要確認）。')
m3.post(sl); m3.finish(sl)

# ---------- move new slides after slide 3 ----------
lst=b.prs.slides._sldIdLst; ids=list(lst)
new=ids[n0:]; 
for el in new: lst.remove(el)
for k,el in enumerate(new): lst.insert(3+k,el)
b.prs.save('共育実習_図解.pptx'); print(len(b.prs.slides))
