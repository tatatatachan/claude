# -*- coding: utf-8 -*-
"""共育実習 図解デッキ — single clean build with a strict layout system.
Canvas 1730x973 px (true 16:9). Margins 88. Exact line spacing everywhere."""
import math
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.oxml.ns import qn
from lxml import etree

W,H=1730,973; E=12192000/W; M=88; CW=W-2*M; T0=208; B0=902
FONT='游ゴシック'
INK,SUB,GRAY='26323A','5B6B73','8A9A96'
TEAL,TEAL2,TEALD,PALE='54C5AF','3FB39D','1F7D6C','E3F4F0'
ORG,ORGD,PALEO='F28C3C','C8651A','FDEBDC'
LINE,BG='E1EAE6','FFFFFF'
BAND,MTN='74C2B2','8ACFC0'

prs=Presentation(); prs.slide_width=int(W*E); prs.slide_height=int(H*E)
def px(v): return Emu(int(round(v*E)))
def pt(v): return Pt(v*E/12700)
def rgb(h): return RGBColor.from_string(h.lstrip('#').upper())

def _fix(sp):
    st=sp._element.find(qn('p:style'))
    if st is not None:
        er=st.find(qn('a:effectRef'))
        if er is not None: er.set('idx','0')
    spPr=sp._element.find(qn('p:spPr'))
    if spPr is not None and spPr.find(qn('a:effectLst')) is None: etree.SubElement(spPr,qn('a:effectLst'))

def shape(sl,kind,x,y,w,h,fill=None,line=None,lw=1,rad=None,name=None):
    s=sl.shapes.add_shape(kind,px(x),px(y),px(w),px(h))
    if fill: s.fill.solid(); s.fill.fore_color.rgb=rgb(fill)
    else: s.fill.background()
    if line: s.line.color.rgb=rgb(line); s.line.width=Pt(lw)
    else: s.line.fill.background()
    if rad is not None and kind==MSO_SHAPE.ROUNDED_RECTANGLE: s.adjustments[0]=min(0.5,rad/min(w,h))
    if name: s.name=name
    _fix(s); return s
def card(sl,x,y,w,h,fill=BG,line=LINE,rad=20,name='カード'): return shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,x,y,w,h,fill,line,1,rad,name)
def pill(sl,x,y,w,h,fill,name='タグ'): return shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,x,y,w,h,fill,None,1,h/2,name)
def dot(sl,cx,cy,d,fill,name='点'): return shape(sl,MSO_SHAPE.OVAL,cx-d/2,cy-d/2,d,d,fill,None,1,None,name)
def hline(sl,x1,y1,x2,y2,color=LINE,w=1,dash=False,name='線'):
    c=sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,px(x1),px(y1),px(x2),px(y2)); c.line.color.rgb=rgb(color); c.line.width=Pt(w); c.name=name; _fix(c)
    if dash:
        ln=c.line._get_or_add_ln(); etree.SubElement(ln,qn('a:prstDash')).set('val','sysDot')
    return c
def poly(sl,pts,fill,name='図形',pos=None):
    fb=sl.shapes.build_freeform(px(pts[0][0]),px(pts[0][1])); fb.add_line_segments([(px(a),px(b)) for a,b in pts[1:]],close=True)
    s=fb.convert_to_shape(); s.fill.solid(); s.fill.fore_color.rgb=rgb(fill); s.line.fill.background(); s.name=name; _fix(s)
    if pos is not None:
        el=s._element; el.getparent().remove(el); sl.shapes._spTree.insert(pos,el)
    return s

def para(t,size,color=INK,bold=False,after=0,lh=1.5,runs=None,spc=0):
    return dict(t=t,size=size,color=color,bold=bold,after=after,lh=lh,runs=runs,spc=spc)
def text(sl,x,y,w,h,paras,anchor='top',align='l',name='テキスト',rot=0):
    tb=sl.shapes.add_textbox(px(x),px(y),px(w),px(h)); tf=tb.text_frame
    tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
    tf.word_wrap=True; tf.auto_size=MSO_AUTO_SIZE.NONE
    tf.vertical_anchor={'top':MSO_ANCHOR.TOP,'middle':MSO_ANCHOR.MIDDLE,'bottom':MSO_ANCHOR.BOTTOM}[anchor]
    if isinstance(paras,dict): paras=[paras]
    for i,pp in enumerate(paras):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment={'l':PP_ALIGN.LEFT,'c':PP_ALIGN.CENTER,'r':PP_ALIGN.RIGHT}[align]
        msz=max([pp['size']]+[o.get('size',pp['size']) for _,o in (pp['runs'] or [])]); p.line_spacing=pt(msz*pp['lh']); p.space_after=pt(pp['after']); p.space_before=0
        for rt in (pp['runs'] or [(pp['t'],{})]):
            r=p.add_run(); r.text=rt[0]; o=rt[1]; f=r.font
            f.size=pt(o.get('size',pp['size'])); f.bold=o.get('bold',pp['bold']); f.name=FONT; f.color.rgb=rgb(o.get('color',pp['color']))
            rPr=r._r.get_or_add_rPr()
            for tag in ('a:ea','a:cs'): etree.SubElement(rPr,qn(tag)).set('typeface',FONT)
            if pp['spc']: rPr.set('spc',str(int(pp['spc']*100)))
    tb.rotation=rot; tb.name=name; return tb

def new_slide(tag,title,sub=None,notes=''):
    sl=prs.slides.add_slide(prs.slide_layouts[6])
    shape(sl,MSO_SHAPE.RECTANGLE,0,0,W,H,BG,None,name='背景')
    edge=lambda x:166-12*math.sin(2*math.pi*(1-x/W))
    band=[(0,0),(W,0)]+[(W-i*W/240,edge(W-i*W/240)) for i in range(241)]
    poly(sl,band,BAND,'ヘッダー帯')
    poly(sl,[(1190,152),(1352,62),(1486,152)],MTN,'ヘッダー山1'); poly(sl,[(1410,152),(1556,98),(1700,152)],MTN,'ヘッダー山2')
    text(sl,M,32,900,26,para(tag,19,'EAF8F4',True,spc=3),name='小見出し')
    text(sl,M,60,1300,60,para(title,44,'FFFFFF',True,lh=1.2),name='タイトル')
    if sub: text(sl,M,118,1200,28,para(sub,20,'EAF8F4',lh=1.3),name='サブタイトル')
    if notes: sl.notes_slide.notes_text_frame.text=notes
    return sl
def note(sl,t): text(sl,M,B0+26,1300,22,para(t,15,GRAY,lh=1.3),name='注記')

# ====================== 1. 共創モデル ======================
def s_ring():
    sl=new_slide('施策①　共育実習','共育実習の共創モデル','学ぶ人も、迎える人も、地域も。みんなが共に育つ')
    cx,cy,Ro,Ri=865,552,276,196
    segs=[(0,60,'F28C3C','C8651A','エフビー介護サービス','エフビー','営業の差になる',['志と実利で学校から選ばれ、','将来の担い手と出会えます。']),
     (60,120,'F7AB67','C8651A','社員','社員','学びと生きがいが育つ',['学生から学び、仕事の意味を再発見。','利用者の生きがいも育ちます。']),
     (120,180,'2E9E8A','1F7D6C','地域','地域','担い手とまちの未来',['地域を担う人が育ち、','介護の現場が身近になります。']),
     (180,240,'54C5AF','1F7D6C','大学','大学','学部・学科の魅力向上',['魅力的な実習で、学部・学科の魅力が向上。','社会テーマ型プログラム「STA」で連携。']),
     (240,300,'3FB39D','1F7D6C','専門学校','専門学校','実習先の選択肢が広がる',['単位つきの実習先が増え、','介護の学びの入口が広がります。']),
     (300,360,'86D6C4','1F7D6C','高校','高校','探究と進路に生きる実績',['単位つきで受け入れやすく、探究テーマ','探しと面接で語れる実績になります。'])]
    # centre
    dot(sl,cx,cy,336,'FFFFFF','中央円').line.color.rgb=rgb(LINE)
    text(sl,cx-150,cy-96,300,30,para('エフビー介護の',23,'2E9E8A',True,spc=2),align='c',name='中央ミニ')
    text(sl,cx-170,cy-60,340,96,para('共育実習',70,INK,True,lh=1.2),align='c',name='中央タイトル')
    pill(sl,cx-82,cy+52,164,40,ORG,'共に育つ帯'); text(sl,cx-82,cy+52,164,40,para('共に育つ',21,'FFFFFF',True,spc=3,lh=1.2),anchor='middle',align='c',name='共に育つ')
    GAP=2.6; thick=(Ro-Ri)/(2*Ro)*100000
    def P(a,rr): t=math.radians(a); return cx+rr*math.sin(t),cy-rr*math.cos(t)
    for i,(a0,a1,col,dark,name,ring,head,desc) in enumerate(segs):
        s=shape(sl,MSO_SHAPE.BLOCK_ARC,cx-Ro,cy-Ro,2*Ro,2*Ro,col,None,name=f'環_{name}')
        av=s._element.spPr.find(qn('a:prstGeom')).find(qn('a:avLst'))
        for g in list(av): av.remove(g)
        for n,v in (('adj1',((a0+GAP-90)%360)*60000),('adj2',((a1-GAP-90)%360)*60000),('adj3',thick)): etree.SubElement(av,qn('a:gd'),name=n,fmla=f'val {int(v)}')
        mid=(a0+a1)/2; rm=(Ro+Ri)/2; mx,my=P(mid,rm)
        rot=mid if (mid<=90 or mid>=270) else mid-180
        text(sl,mx-80,my-20,160,40,para(ring,26 if len(ring)<4 else 23,'FFFFFF',True,spc=2,lh=1.2),anchor='middle',align='c',name=f'環ラベル_{name}',rot=rot)
        left=mid>180; k=int(mid//60) if not left else int((mid-180)//60)
        off=[-236,0,236][k] if not left else [236,0,-236][k]
        ly=cy+off; CWd,CHd=470,176; x=M if left else W-M-CWd; y=ly-CHd/2
        R=Ro+16; dx=math.sqrt(R*R-off*off); ex=cx-dx if left else cx+dx
        hline(sl,(x+CWd) if left else x,ly,ex,ly,col,2,name=f'接続線_{name}'); dot(sl,ex,ly,12,col,f'接続点_{name}')
        card(sl,x,y,CWd,CHd,name=f'カード_{name}')
        text(sl,x+34,y+22,CWd-68,CHd-30,[para(name,18,SUB,True,after=2,lh=1.4),para(head,28,dark,True,after=8,lh=1.35),para(desc[0],19,INK,lh=1.5),para(desc[1],19,INK,lh=1.5)],name=f'本文_{name}')
    for a in range(0,360,60):
        gx,gy=P(a,(Ro+Ri)/2); dot(sl,gx,gy,28,'FFFFFF','循環マーク白')
        t=math.radians(a); tx,ty=math.cos(t),math.sin(t); nx,ny=-ty,tx
        poly(sl,[(gx+8*tx,gy+8*ty),(gx-4*tx+4*nx,gy-4*ty+4*ny),(gx-4*tx-4*nx,gy-4*ty-4*ny)],'2E9E8A','循環マーク矢印')
    return sl

# ====================== 2. ブランド循環 ======================
def s_loop():
    sl=new_slide('施策　実習','どうブランドを育てていくか','実習の体験が声になり、声がサイトに載り、次の実習へつながる')
    cx=865; CWd,CHd=580,176; xl=M; xr=W-M-CWd; yt=T0; yb=T0+CHd+150
    steps=[('共育実習を行う',['高校・専門学校・大学で','共育実習を実施します。'],TEAL2,TEALD,xl,yt),
           ('声が集まる',['学生・先生・社員・','利用者さんの声が集まります。'],'86D6C4',TEALD,xr,yt),
           ('実習サイトに載せる',['プログラム内容と','口コミを掲載します。'],ORG,ORGD,xr,yb),
           ('見て、動く',['学校は受け入れを判断し、','次の学生は参加を決めます。'],'2E9E8A',TEALD,xl,yb)]
    def arrow(kind,x,y,w,h,col,name):
        a=shape(sl,kind,x,y,w,h,col,None,name=name); a.adjustments[0]=0.5; a.adjustments[1]=0.55; return a
    ym=yt+CHd/2
    arrow(MSO_SHAPE.RIGHT_ARROW,xl+CWd+20,ym-32,xr-xl-CWd-40,64,TEAL2,'矢印_1から2')
    arrow(MSO_SHAPE.DOWN_ARROW,xr+CWd/2-30,yt+CHd+14,60,yb-yt-CHd-28,'86D6C4','矢印_2から3')
    arrow(MSO_SHAPE.LEFT_ARROW,xl+CWd+20,yb+CHd/2-32,xr-xl-CWd-40,64,ORG,'矢印_3から4')
    arrow(MSO_SHAPE.UP_ARROW,xl+CWd/2-30,yt+CHd+14,60,yb-yt-CHd-28,'2E9E8A','矢印_4から1')
    text(sl,xl+CWd/2+52,yt+CHd+60,360,30,para('次の共育実習につながる',21,TEALD,True,lh=1.3),name='循環ラベル')
    cy=(yt+yb+CHd)/2
    for r_,col in ((118,'DDF1EA'),(90,'B5E4D6'),(62,TEAL)): dot(sl,cx,cy-8,2*r_,col,'広がる輪')
    text(sl,cx-60,cy-8-28,120,56,[para('実習',24,'FFFFFF',True,lh=1.2),para('ブランド',24,'FFFFFF',True,lh=1.2)],align='c',anchor='middle',name='中央')
    pill(sl,cx-96,cy+120,192,38,ORG,'帯'); text(sl,cx-96,cy+120,192,38,para('回るほど育つ',19,'FFFFFF',True,lh=1.2),align='c',anchor='middle',name='帯文字')
    for n,(h,d,c,dk,x,y) in enumerate(steps,1):
        card(sl,x,y,CWd,CHd,name=f'カード_{h}')
        dot(sl,x+34+28,y+30+28,56,c,'番号'); text(sl,x+34,y+30,56,56,para(str(n),28,'FFFFFF',True,lh=1.1),align='c',anchor='middle',name=f'番号{n}')
        text(sl,x+114,y+30,CWd-150,56,para(h,32,dk if c!=ORG else ORGD,True,lh=1.2),anchor='middle',name=f'見出し_{h}')
        text(sl,x+34,y+100,CWd-68,66,[para(d[0],22,INK,lh=1.5),para(d[1],22,INK,lh=1.5)],name=f'説明_{h}')
    by=yb+CHd+30; bh=B0-by
    card(sl,M,by,800,bh,name='サイトに載せるもの'); card(sl,M+800+30,by,CW-830,bh,fill='F6F9F8',name='ほかの施策')
    text(sl,M+36,by+18,730,bh-24,[para('サイトに載せるもの',24,INK,True,after=4,lh=1.3),para('プログラム内容と口コミ。学校の先生が受け入れを判断でき、学生が参加を決められる状態にする。',19,SUB,lh=1.45)],name='サイトに載せるもの本文')
    text(sl,M+800+30+36,by+18,CW-830-72,bh-24,[para('ほかの施策',24,SUB,True,after=4,lh=1.3),para('関連大学・専門学校を増やす／対応地域／産官学で連携（次世代の育成を地域のみなさんで実施）',19,SUB,lh=1.45)],name='ほかの施策本文')
    return sl

# ====================== 3. 全体像 ======================
def s_overview():
    sl=new_slide('実習応募サイト','実習応募サイトの全体像',notes='実習応募サイトの概要。')
    ph=492; p=shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,M,T0,704,ph,TEAL,None,rad=24,name='コンセプト')
    text(sl,M+52,T0+44,600,ph-80,[para('CARE PRACTICE',18,'D9F6EE',True,after=14,lh=1.3,spc=5),
        para('FUN LIFE!',76,'FFFFFF',True,lh=1.08),para('FUN LOCAL!',76,'FFE08A',True,after=22,lh=1.08),
        para('生きがい、持ち寄る。地域の未来。',30,'FFFFFF',True,after=14,lh=1.3),
        para('介護や老後の話は、なんだか暗い。そんなイメージを、一緒にひっくり返したい。',20,'F0FBF8',lh=1.55)],name='コンセプト本文')
    facts=[('目的','介護の現場を実際に体験し、\n仕事のイメージをつかむ'),('対象','学生のみなさん\n保護者・先生もご覧ください'),('費用','無償'),('期間・時間','1DAY　9:30〜15:00ごろ\n5DAYS　5日間じっくり')]
    fw=(CW-704-32-32)/2; fh=(ph-32)/2
    for i,(lab,val) in enumerate(facts):
        x=M+704+32+(i%2)*(fw+32); y=T0+(i//2)*(fh+32)
        card(sl,x,y,fw,fh,name=f'カード_{lab}')
        ps=[para(lab,18,SUB,True,after=10,lh=1.3,spc=1)]
        if lab=='費用': ps+= [para('無償',60,ORGD,True,after=2,lh=1.15),para('実習は無料で参加できます',19,INK,lh=1.4)]
        else: ps+=[para(v,23 if lab=='対象' else 25,INK,True,lh=1.5) for v in val.split('\n')]
        text(sl,x+34,y+28,fw-68,fh-40,ps,name=f'本文_{lab}')
    sy=T0+ph+32; sh=B0-sy; sw=(CW-3*32)/4
    stats=[('109','拠点','信越・北関東に展開',TEALD),('7','種のサービス','ホーム・デイ・訪問など',TEALD),('2','つのプログラム','1DAY と 5DAYS',ORGD),('9','事業所','360°ツアーで見学できる',ORGD)]
    for i,(n,u,s,c) in enumerate(stats):
        x=M+i*(sw+32); card(sl,x,sy,sw,sh,name=f'カード_{u}')
        text(sl,x+34,sy+26,sw-60,sh-40,[para('',10,runs=[(n,{'size':68,'bold':True,'color':c}),(' '+u,{'size':24,'bold':True,'color':INK})],lh=1.2,after=4),para(s,19,SUB,lh=1.4)],name=f'本文_{u}')
    note(sl,'※ 対象・期間・時間などはサイト上でも仮・調整中の内容です。')
    return sl

# ====================== 4. 介護への考え方 ======================
def s_philosophy():
    sl=new_slide('介護への考え方','エフビー介護サービスの、介護への考え方',notes='出典：企業説明会資料・経営者ヒアリング。')
    dh=172; card(sl,M,T0,CW,dh,name='夢')
    text(sl,M+44,T0+26,CW-88,dh-34,[para('わたしたちの夢',18,SUB,True,after=6,lh=1.3,spc=2),para('人生の最終ステージを、利用者様の幸せと満足で元気にする',38,TEALD,True,after=10,lh=1.3),para('利用者様の笑顔と、数多くの「ありがとう」を求め、喜ばれること',21,INK,lh=1.4)],name='夢本文')
    py=T0+dh+28; ph=B0-py; pw=(CW-32)/2
    def panel(x,title,rows,col):
        card(sl,x,py,pw,ph,name=f'カード_{title}')
        text(sl,x+40,py+30,pw-80,36,para(title,27,INK,True,lh=1.3),name=f'見出し_{title}')
        rh=(ph-100)/3
        for i,t in enumerate(rows):
            y=py+90+i*rh
            hline(sl,x+40,y,x+pw-40,y,LINE,1,name='区切り')
            dot(sl,x+40+26,y+rh/2,52,col,'番号'); text(sl,x+40,y+rh/2-26,52,52,para(str(i+1),26,'FFFFFF',True,lh=1.1),align='c',anchor='middle',name=f'番号{i+1}')
            text(sl,x+120,y+10,pw-170,rh-20,para(t,22,INK,lh=1.5),anchor='middle',name=f'{title}_{i+1}')
    panel(M,'創業からの想い',['経営理念と介護方針を基本として、利用者様とご家族の安心感と満足を目指します','心の温かい法人、事業所、そして心の優しい人間の集団になります','利用者様に喜ばれる介護サービスと介護用品を提供し、スピーディーな対応に専心する社員になります'],TEAL2)
    panel(M+pw+32,'大切にしている姿勢',['利用者様を「お客様」として敬い、その人としての尊厳を大切にします','「自分の親を面倒見るつもりで」。笑顔・言葉づかい・態度の接遇に力を入れています','介護する人・される人の区別なく、できることを持ち寄る。「誰かのためにはたらく」ことが生きがい'],ORG)
    note(sl,'出典：エフビー介護サービス 企業説明会資料／経営者ヒアリング（2025年）。文言は要約しています。')
    return sl

# ====================== なぜ、福祉が大切か ======================
def s_why():
    sl=new_slide('福祉人材のこれからの価値','なぜ、福祉が大切なのか',notes='長野大学×エフビー 産学連携プロジェクト資料（社会状況・やりがい）をもとに整理。')
    lw_=540; shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,M,T0,lw_,B0-T0,TEAL,None,rad=24,name='問い')
    text(sl,M+48,T0+48,lw_-96,B0-T0-96,[para('WHY WELFARE',18,'EAF8F4',True,after=26,lh=1.3,spc=4),
        para('人を支える仕事が、地域の未来を支える。',40,'FFFFFF',True,after=32,lh=1.45),
        para('2040年に向けて、支える人は減り、支えられる人は増えていきます。福祉は、社会を成り立たせる土台です。',21,'F0FBF8',after=22,lh=1.7),
        para('それでも「福祉」が若者に選ばれにくいのは、仕事の価値が、まだ十分に伝わっていないから。',21,'F0FBF8',lh=1.7)],name='問い本文')
    items=[('社会を支えるインフラだから','現役世代2.1人で1人の高齢者を支える構造（2020年）から、2040年には約1.6人で1人を支える構造へ。「支える人」と「支えられる人」のバランスが崩れ、社会インフラの持続可能性が問われています。',TEAL2,TEALD),
           ('「生きてて良かった」を支える仕事だから','福祉は、残された命をいかに生きるかを支える仕事。人の命と生活を預かり、利用者さんの「最終ページ」に出てくる人物として、その人の生きがいに関わります。',ORG,ORGD),
           ('地域の未来をつくる人を育てるから','「3K」というイメージを変え、福祉人材が福祉の枠を超えて活躍できる場へ。長寿の国・長野発の、希望の地域モデルをつくる起点になります。',TEAL2,TEALD)]
    gx=M+lw_+32; gw=W-M-gx; gap=24; gh=(B0-T0-2*gap)/3
    for i,(h,d,c,dk) in enumerate(items):
        y=T0+i*(gh+gap); card(sl,gx,y,gw,gh,name=f'カード_{h}')
        dot(sl,gx+36+30,y+gh/2,60,c,'番号'); text(sl,gx+36,y+gh/2-30,60,60,para(str(i+1),30,'FFFFFF',True,lh=1.1),align='c',anchor='middle',name=f'番号{i+1}')
        text(sl,gx+130,y+22,gw-166,gh-44,[para(h,27,dk,True,after=10,lh=1.3),para(d,20,INK,lh=1.65)],anchor='middle',name=f'理由_{i+1}')
    note(sl,'出典：エフビー介護サービス×長野大学 産学連携プロジェクト資料（2025年12月・2026年3月）、雫石部長ヒアリング。人口の数字は国立社会保障・人口問題研究所の推計に基づきます。')
    return sl

# ====================== 感情労働の価値 ======================
def s_emotion():
    sl=new_slide('感情労働','感情労働の価値：人の心を動かし、意欲を引き出す仕事',notes='visions college（エフビー介護サービス回）Chapter02「感情労働の未来」をもとに整理。')
    gap=28; cw=(CW-2*gap)/3; h1=252
    cols=[('肉体労働','体力を使って、対価を得る',None,TEAL2),('頭脳労働','アイデアなどを提供する',None,TEAL2),('感情労働','つねに自分の感情をコントロールし、相手に合わせた言葉や態度で応対する','介護・医療など「ひと」を相手にする仕事',ORG)]
    for i,(h,d,tg,c) in enumerate(cols):
        x=M+i*(cw+gap)
        card(sl,x,T0,cw,h1,fill='FFF6EC' if c==ORG else BG,line=ORG if c==ORG else LINE,name=f'カード_{h}')
        pill(sl,x+32,T0+28,110,36,PALEO if c==ORG else PALE,'タグ'); text(sl,x+32,T0+28,110,36,para(['TYPE 1','TYPE 2','TYPE 3'][i],16,ORGD if c==ORG else TEALD,True,lh=1.2),align='c',anchor='middle',name='番号タグ')
        ps=[para(h,34,ORGD if c==ORG else TEALD,True,after=8,lh=1.25),para(d,21,INK,lh=1.6,after=6)]
        if tg: ps.append(para(tg,18,ORGD,True,lh=1.4))
        text(sl,x+32,T0+84,cw-64,h1-100,ps,name=f'本文_{h}')
    y2=T0+h1+gap; h2=204; lw_=960
    card(sl,M,y2,lw_,h2,name='従来これから')
    text(sl,M+36,y2+24,400,32,para('働き方のとらえ方が、変わっていく',23,INK,True,lh=1.3),name='変化見出し')
    def chips(y,label,items,hl=False):
        text(sl,M+36,y,110,44,para(label,19,SUB,True,lh=1.2),anchor='middle',name=f'ラベル_{label}')
        x=M+150
        for t,c in items:
            w=len(t)*21+44; pill(sl,x,y,w,44,PALEO if c=='o' else PALE,'チップ'); text(sl,x,y,w,44,para(t,19,ORGD if c=='o' else TEALD,True,lh=1.2),align='c',anchor='middle',name=f'チップ_{t}'); x+=w+14
    chips(y2+78,'従来',[('頭脳労働（感情労働を含む）','t'),('肉体労働','t')])
    chips(y2+138,'これから',[('頭脳労働','t'),('感情労働','o'),('肉体労働','t')])
    rx=M+lw_+gap; rw=CW-lw_-gap
    card(sl,rx,y2,rw,h2,fill='F6F9F8',name='定義')
    text(sl,rx+32,y2+24,rw-64,h2-40,[para('感情労働とは',22,TEALD,True,after=8,lh=1.3),para('相手に感謝や安心の気持ちを喚起させるために行う、感情の管理。（A.R.ホックシールドが提唱）',19,INK,lh=1.6)],name='定義本文')
    y3=y2+h2+gap; h3=B0-y3; qw=820
    shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,M,y3,qw,h3,TEAL,None,rad=20,name='雫石部長')
    text(sl,M+40,y3+20,qw-80,h3-30,[para('雫石部長（介護事業部）より',17,'EAF8F4',True,after=6,lh=1.3),para('介護は、感情労働。単に感情を使うのではなく、自分と相手の感情を管理する仕事です。',25,'FFFFFF',True,lh=1.55)],anchor='middle',name='引用')
    sx=M+qw+gap; sw=CW-qw-gap; card(sl,sx,y3,sw,h3,name='まとめ')
    text(sl,sx+36,y3+18,sw-72,h3-26,[para('・人の心を動かし、人の意欲を引き出す仕事',20,INK,after=6,lh=1.5),para('・お互いの感情を管理しながら行う、高度な技術',20,INK,after=6,lh=1.5),para('・これから社会に出る人にとって、どの仕事でも必須のスキル',20,INK,lh=1.5)],anchor='middle',name='まとめ本文')
    note(sl,'出典：visions college（エフビー介護サービス回、2026年2月24日）、長野大学×エフビー介護サービス 産学連携プロジェクト資料。')
    return sl

# ====================== 5. 沿革（うねる帯） ======================
def s_history():
    sl=new_slide('沿革','福祉用具から、地域に根ざす介護の総合企業へ',notes='沿革。年次が資料で確認できた出来事のみ年を表示。')
    yc=596; A=32; T=112; lam=1500
    cl=lambda x: yc+A*math.sin(2*math.pi*(x/lam)+0.6)
    N=160; top=[(W*i/N,cl(W*i/N)-T/2) for i in range(N+1)]; bot=[(W*(N-i)/N,cl(W*(N-i)/N)+T/2) for i in range(N+1)]
    poly(sl,top+bot,'D9F0E9','沿革リボン')
    for yr,x in (('2000',520),('2010',900),('2020',1200)):
        text(sl,x-110,cl(x)-36,220,72,para(yr,60,TEAL2,True,lh=1.1),align='c',anchor='middle',name=f'年代_{yr}')
    items=[
     (230,True,'1987年4月','エフビー信州として設立',['フランスベッドの代理店が原点。','本社は長野県佐久市'],False),
     (445,False,'2000年4月','福祉用具のレンタルを開始',['福祉用具の取り扱いの範囲を','広げていく'],False),
     (660,True,'2002年10月','エフビー介護サービスへ商号変更',['介護サービスの会社として','歩みを進める'],False),
     (875,False,'時期は確認中','居宅介護・小規模多機能へ',['自宅での生活の支援から、','住まい・通い訪問泊まりへ'],True),
     (1090,True,'2019年','海外人材の受け入れ',['ベトナム・ミャンマー・','ネパール・フィリピンなど'],False),
     (1305,False,'2022年4月','東証スタンダード市場に上場',['事業成長の加速へ'],False),
     (1520,True,'現在','7種109拠点／1,250名',['信越・北関東に展開','（従業員数は2023年4月時点）'],False)]
    cwid=340; chh=200
    for i,(x,up,pl_,h,d,und) in enumerate(items):
        cx0=min(max(x-cwid/2,M),W-M-cwid)
        if up: y=T0-12; ry=cl(x)-T/2; hline(sl,x,y+chh,x,ry,TEAL2,2,name='接続線'); dot(sl,x,ry,14,TEAL2,'接続点')
        else: y=B0-chh+12; ry=cl(x)+T/2; hline(sl,x,ry,x,y,TEAL2,2,name='接続線'); dot(sl,x,ry,14,TEAL2,'接続点')
        card(sl,cx0,y,cwid,chh,name=f'カード_{h}')
        pw_=(len(pl_)*18+36) if not und else 156
        pill(sl,cx0+26,y+22,pw_,34,'EEF1F0' if und else PALE,'年タグ'); text(sl,cx0+26,y+22,pw_,34,para(pl_,17 if und else 19,GRAY if und else TEALD,True,lh=1.2),align='c',anchor='middle',name='年')
        text(sl,cx0+26,y+70,cwid-52,chh-80,[para(h,21,INK,True,after=4,lh=1.35)]+[para(t,17,SUB,lh=1.45) for t in d],name=f'本文_{h}')
    note(sl,'※ 設立・商号変更・従業員数は企業説明会資料、2000年は会長ヒアリング、海外人材は経営者ヒアリング、上場は決算説明資料に基づきます。「時期は確認中」は年次の確認が必要です。')
    return sl

# ====================== 6. 小規模 × 多拠点 × 7つのサービス ======================
def s_scale():
    sl=new_slide('事業の展開','小規模な施設を、地域ごとに。7つのサービスで暮らしを支える',notes='小規模・多拠点・サービスの見せ方。')
    ph=262; lw_=760
    shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,M,T0,lw_,ph,TEAL,None,rad=24,name='こだわり')
    text(sl,M+48,T0+34,lw_-96,ph-50,[para('わたしたちのちょっとしたこだわり',19,'EAF8F4',True,after=10,lh=1.3,spc=2),
        para('大規模な施設ではなく、',38,'FFFFFF',True,lh=1.3),para('小規模な施設をメインに展開する。',38,'FFFFFF',True,after=12,lh=1.3),
        para('地域の文化・風土を取り入れた、きめ細やかなサービス。住み慣れた地元で、長く生活できる環境を。',19,'F0FBF8',lh=1.55)],name='こだわり本文')
    rx=M+lw_+32; rw=CW-lw_-32; card(sl,rx,T0,rw,ph,name='拠点カード')
    text(sl,rx+36,T0+26,rw-72,34,para('多拠点で、地域に根ざす',24,INK,True,lh=1.3),name='拠点見出し')
    sw=(rw-72)/3
    for i,(n,u,c) in enumerate([('109','拠点',TEALD),('7','種のサービス',TEALD),('5','県',ORGD)]):
        x=rx+36+i*sw
        if i: hline(sl,x-14,T0+90,x-14,T0+188,LINE,1,name='区切り')
        text(sl,x,T0+78,sw-24,150,[para('',10,runs=[(n,{'size':72,'bold':True,'color':c})],lh=1.1,after=0),para(u,22,INK,True,lh=1.3,after=4)],name=f'数字_{u}')
    text(sl,rx+36,T0+ph-60,rw-72,34,para('長野57・新潟15・埼玉15・群馬12・栃木10',20,SUB,lh=1.4),name='県別')
    # services
    sy=T0+ph+34
    text(sl,M,sy,900,36,para('暮らし方に合わせて選べる、7つのサービス',28,INK,True,lh=1.3),name='サービス見出し')
    gy=sy+54; gh=B0-gy; gw=(CW-2*28)/3
    groups=[('自宅で暮らし続ける','自宅での生活を支援',TEAL2,[('訪問介護','ご自宅で、生活を支援'),('訪問看護','ご自宅へ、看護を届ける')]),
            ('通い・訪問・泊まりで支える','小規模多機能で、暮らしを支える',ORG,[('デイサービス','通いで過ごす'),('小規模多機能型','通い・訪問・泊まりを組み合わせて'),('看護小規模多機能型','看護も組み合わせて')]),
            ('住まいで暮らす','居住いただき、支援する','2E9E8A',[('有料老人ホーム','住まいで、暮らしを支援'),('グループホーム','少人数で暮らす、家庭的な雰囲気')])]
    for i,(h,s,c,items) in enumerate(groups):
        x=M+i*(gw+28)
        card(sl,x,gy,gw,gh,fill='F8FBFA',name=f'カード_{h}')
        shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,x,gy,gw,84,c,None,rad=20,name=f'ヘッダー_{h}')
        shape(sl,MSO_SHAPE.RECTANGLE,x,gy+52,gw,32,c,None,name='ヘッダー下')
        text(sl,x+32,gy+12,gw-64,62,[para(h,24,'FFFFFF',True,lh=1.25),para(s,17,'FFFFFF',lh=1.3)],anchor='middle',name=f'見出し_{h}')
        th=(gh-84-36-(len(items)-1)*12)/max(len(items),2) if len(items)<3 else (gh-84-36-24)/3
        th=min(th,138)
        for j,(n,d) in enumerate(items):
            ty=gy+84+18+j*(th+12)
            card(sl,x+20,ty,gw-40,th,rad=14,name=f'タイル_{n}')
            dot(sl,x+20+26,ty+th/2,14,c,'ドット')
            text(sl,x+20+50,ty+8,gw-40-70,th-16,[para(n,23,INK,True,lh=1.3),para(d,17,SUB,lh=1.4)],anchor='middle',name=f'サービス_{n}')
    note(sl,'出典：企業説明会資料、経営者ヒアリング、実習サイトの掲載内容。サービスの分け方は暮らし方に合わせた整理です。')
    return sl

# ====================== 7. 売上の推移 ======================
def s_sales():
    sl=new_slide('事業の成長','売上は10年で大きく成長。用具と介護の2本柱で拡大',notes='売上推移（26期〜36期）。出典：企業説明会資料。')
    lw_=1040; ph=B0-T0; card(sl,M,T0,lw_,ph,name='売上カード')
    text(sl,M+40,T0+30,600,36,para('売上の推移（26期〜36期）',27,INK,True,lh=1.3),name='売上見出し')
    # legend
    lx=M+lw_-40-420
    for k,(nm,c) in enumerate([('用具',TEAL2),('介護',ORG),('居宅','F2C14E')]):
        x=lx+k*140; shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,x,T0+38,22,22,c,None,rad=5,name=f'凡例_{nm}')
        text(sl,x+32,T0+34,100,30,para(nm,20,INK,True,lh=1.3),name=f'凡例文字_{nm}')
    text(sl,M+40,T0+74,600,26,para('単位：百万円（資料のグラフ値。単位は推定）',16,SUB,lh=1.3),name='単位')
    yo=[2137,2323,2431,2604,2791,3003,3229,3520,3800,3813,4324]
    kai=[1632,1835,2087,2407,2643,2918,3771,3970,4100,4740,5133]
    kyo=[74,86,100,109,118,123,150,177,190,223,303]
    tot=[a+b_+c for a,b_,c in zip(yo,kai,kyo)]
    base=B0-84; topy=T0+190; maxh=base-topy; mx=max(tot)
    bw=58; gap=28; x0=M+(lw_-(11*bw+10*gap))/2
    for i in range(11):
        x=x0+i*(bw+gap); y=base
        for v,c,tc in ((yo[i],TEAL2,'FFFFFF'),(kai[i],ORG,'FFFFFF'),(kyo[i],'F2C14E',INK)):
            h=maxh*v/mx; y-=h; shape(sl,MSO_SHAPE.RECTANGLE,x,y,bw,h,c,None,name=f'棒_{26+i}期')
            if i in (0,10) and v>1000: text(sl,x-12,y,bw+24,h,para(f'{v:,}',16,tc,True,lh=1.2),align='c',anchor='middle',name='値')
        text(sl,x-14,y-34,bw+28,28,para(f'{tot[i]:,}',17,INK,True,lh=1.2),align='c',name=f'合計_{26+i}期')
        text(sl,x-14,base+12,bw+28,26,para(f'{26+i}期',17,SUB,True,lh=1.2),align='c',name=f'期_{26+i}')
    hline(sl,M+40,base,M+lw_-40,base,LINE,1.5,name='基準線')
    # callouts for first / last bar
    for i,yr in ((0,'2013年'),(10,'2023年')):
        x=x0+i*(bw+gap)+bw/2
        pill(sl,x-48,T0+118,96,34,PALEO if i else PALE,'年'); text(sl,x-48,T0+118,96,34,para(yr,18,ORGD if i else TEALD,True,lh=1.2),align='c',anchor='middle',name=f'年_{yr}')
    text(sl,M+40,T0+ph-40,lw_-80,26,para('資料の記載：売上は10年で235%成長（2013年 39億円 → 2023年 92億円）',17,SUB,lh=1.3),name='資料の記載')
    x2=M+lw_+32; w2=CW-lw_-32; card(sl,x2,T0,w2,ph,name='戦略カード')
    text(sl,x2+36,T0+30,w2-72,36,para('これからの成長戦略',26,INK,True,lh=1.3),name='戦略見出し')
    blocks=[('福祉用具事業',['自社仕入レンタル品販売の拡充','新規利用者様の開拓'],TEAL2),('介護事業',['介護サービス・事業所運営方法の見直し','新たな介護サービスへの挑戦','ニーズにあったきめ細やかなサービス'],TEAL2),('あわせて',['同業種を対象としたM&Aで業績拡大'],ORG)]
    y=T0+100; hs=[170,236,120]; gp=(ph-100-24-sum(hs))/2
    for (h,items,c),bh in zip(blocks,hs):
        pill(sl,x2+36,y,176,40,PALE if c==TEAL2 else PALEO,'タグ'); text(sl,x2+36,y,176,40,para(h,19,TEALD if c==TEAL2 else ORGD,True,lh=1.2),align='c',anchor='middle',name=f'タグ文字_{h}')
        text(sl,x2+36,y+54,w2-72,bh-54,[para('・'+t,19,INK,after=6,lh=1.45) for t in items],name=f'戦略_{h}')
        y+=bh+gp
    note(sl,'※ 売上は企業説明会資料（用具・介護・居宅の合計。給食事業等は含まない可能性あり）、成長戦略は2026年3月期 決算説明資料に基づきます。')
    return sl

# ====================== 社会の変化（人口・介護市場） ======================
def s_market():
    sl=new_slide('時代の背景','人口は減り、高齢者は増える。介護の需要は広がり続ける',notes='人口推移（2020→2050）と介護費の見通し。')
    lw_=900; ph=B0-T0; card(sl,M,T0,lw_,ph,name='人口カード')
    text(sl,M+40,T0+30,lw_-80,36,para('日本の人口推移（2020年 → 2050年）',27,INK,True,lh=1.3),name='人口見出し')
    text(sl,M+40,T0+72,lw_-80,26,para('総人口（万人）と、65歳以上の割合（高齢化率）',17,SUB,lh=1.3),name='人口補足')
    cd=CategoryChartData(); cd.categories=['2020年','2040年','2050年']; cd.add_series('総人口',[12615,11284,10468])
    gf=sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,px(M+30),px(T0+110),px(lw_-60),px(330),cd); gf.name='総人口グラフ'; ch=gf.chart
    ch.has_legend=False; ch.has_title=False; pl=ch.plots[0]; pl.gap_width=45; pl.has_data_labels=True; dl=pl.data_labels
    dl.font.size=Pt(20); dl.font.bold=True; dl.font.name=FONT; dl.position=XL_LABEL_POSITION.OUTSIDE_END; dl.number_format='#,##0'; dl.number_format_is_linked=False
    for i,c in enumerate((TEAL2,TEAL2,ORG)): p_=pl.series[0].points[i]; p_.format.fill.solid(); p_.format.fill.fore_color.rgb=rgb(c)
    ch.value_axis.visible=False; ch.value_axis.has_major_gridlines=False; ch.value_axis.minimum_scale=0; ch.value_axis.maximum_scale=14500
    ca=ch.category_axis; ca.tick_labels.font.size=Pt(22); ca.tick_labels.font.name=FONT; ca.format.line.color.rgb=rgb('C9D6D1')
    cw3=(lw_-80-2*24)/3
    for i,(yr,rate,cnt,c) in enumerate([('2020年','28.6%','約3,619万人',TEALD),('2040年','34.8%','約3,928万人',TEALD),('2050年','37.1%','約3,880万人',ORGD)]):
        x=M+40+i*(cw3+24); y=T0+ph-188
        card(sl,x,y,cw3,150,fill='F6F9F8',rad=16,name=f'高齢化率_{yr}')
        text(sl,x+24,y+16,cw3-48,120,[para('高齢化率（65歳以上）',16,SUB,True,after=2,lh=1.3),para(rate,46,c,True,after=0,lh=1.15),para('65歳以上　'+cnt,17,INK,lh=1.4)],name=f'高齢化率本文_{yr}')
    x2=M+lw_+32; w2=CW-lw_-32; card(sl,x2,T0,w2,ph,name='市場カード')
    text(sl,x2+40,T0+30,w2-80,36,para('介護費の見通し',27,INK,True,lh=1.3),name='市場見出し')
    text(sl,x2+40,T0+72,w2-80,26,para('公的な見通し（兆円）',17,SUB,lh=1.3),name='市場補足')
    base=T0+ph-130; maxh=360
    for i,(yr,v,c,tc) in enumerate([('2018年度',10.7,TEAL2,TEALD),('2040年度',25.8,ORG,ORGD)]):
        h=maxh*v/25.8; bw=170; x=x2+w2/2-bw-34+i*(bw+68)
        shape(sl,MSO_SHAPE.RECTANGLE,x,base-h,bw,h,c,None,name=f'棒_{yr}')
        text(sl,x-20,base-h-56,bw+40,50,para(f'{v}兆円',34,tc,True,lh=1.2),align='c',name=f'値_{yr}')
        text(sl,x-20,base+14,bw+40,30,para(yr,20,SUB,True,lh=1.3),align='c',name=f'年度_{yr}')
    hline(sl,x2+40,base,x2+w2-40,base,LINE,1.5,name='基準線')
    pill(sl,x2+w2/2-204,T0+230,200,40,PALEO,'倍率'); text(sl,x2+w2/2-204,T0+230,200,40,para('約2.4倍に',21,ORGD,True,lh=1.2),align='c',anchor='middle',name='倍率文字')
    text(sl,x2+40,T0+ph-76,w2-80,56,para('介護の需要は、2040年、さらに2050年に向けて続く見込みです。',18,INK,lh=1.5),name='まとめ')
    note(sl,'※ 人口：国立社会保障・人口問題研究所『日本の将来推計人口（令和5年推計）』。2050年の65歳以上人口は総人口×高齢化率による概算。介護費：厚生労働省『2040年を見据えた社会保障の将来見通し（2018年）』。2050年の介護市場の公的推計は確認できていません。')
    return sl

# ====================== 8. 他社比較 ======================
def s_compare():
    sl=new_slide('採用戦略テーマ','他社と並べて見える、エフビーの実習の魅力',notes='P24：採用戦略テーマ（他社比較）。')
    cols=['','エフビー介護サービス','A社','B社','C社']
    rows=[('ビジョン',['「共生」をテーマにした、人々が助け合う地域創生（エフビータウン構想・コミュニティタワー構想）','―','―','暮らしを、共に。']),
     ('事業フェーズ',['成長期〜拡大期（2022年 スタンダード市場上場）','安定期〜成熟期','地域密着・安定運営期','成長期〜拡大期（2024年 スタンダード市場上場）']),
     ('事業・特徴',['有料老人ホーム、グループホーム、デイ、訪問介護・看護、小規模多機能、福祉用具ほか','特養、ケアハウス、デイ、ショートステイ、居宅介護支援、地域包括支援センター','病院運営、老健、デイケア、グループホーム、訪問看護ほか。病院母体の医療＋介護連携','有料老人ホームをシリーズで運営（首都圏中心）。都市型の有料老人ホーム特化']),
     ('人・メンバー',['関わる人たちが、みんな優しく・温かい','「感謝の心を基にした関係」を築き、真心をもってサービスを提供できる人材','「利用者はもちろん、職員にとっても安心できる居場所」を重視','近年は毎年170名以上の新卒社員を受け入れ'])]
    rh=[44,92,76,128,96]; widths=[186,402,322,322,322]
    gs=sl.shapes.add_table(5,5,px(M),px(T0),px(sum(widths)),px(sum(rh))); gs.name='他社比較表'; tb=gs.table
    tp=tb._tbl.tblPr
    for a in ('firstRow','bandRow'): tp.set(a,'0')
    sid=tp.find(qn('a:tableStyleId'))
    if sid is not None: sid.text='{2D5ABB26-0587-4C30-8999-92F81FD0307C}'
    for i,w in enumerate(widths): tb.columns[i].width=px(w)
    for i,h in enumerate(rh): tb.rows[i].height=px(h)
    def border(cell,color=LINE):
        tcPr=cell._tc.get_or_add_tcPr()
        ln=etree.SubElement(tcPr,qn('a:lnB'),w='9525',cap='flat',cmpd='sng',algn='ctr'); sf=etree.SubElement(ln,qn('a:solidFill')); etree.SubElement(sf,qn('a:srgbClr'),val=color)
    def cellset(c,t,size,color,bold=False,fill=None,align=PP_ALIGN.LEFT):
        c.margin_left=c.margin_right=px(18); c.margin_top=c.margin_bottom=px(8); c.vertical_anchor=MSO_ANCHOR.MIDDLE
        p=c.text_frame.paragraphs[0]; p.alignment=align; p.line_spacing=pt(size*1.45)
        r=p.add_run(); r.text=t; f=r.font; f.size=pt(size); f.bold=bold; f.name=FONT; f.color.rgb=rgb(color)
        rPr=r._r.get_or_add_rPr()
        for tag in ('a:ea','a:cs'): etree.SubElement(rPr,qn(tag)).set('typeface',FONT)
        if fill: c.fill.solid(); c.fill.fore_color.rgb=rgb(fill)
        else: c.fill.background()
    for j,h in enumerate(cols): cellset(tb.cell(0,j),h,19,'FFFFFF' if j==1 else INK,True,ORG if j==1 else 'EEF4F1',PP_ALIGN.CENTER)
    for i,(lab,vals) in enumerate(rows,1):
        cellset(tb.cell(i,0),lab,19,TEALD,True)
        for j,v in enumerate(vals,1): cellset(tb.cell(i,j),v,17 if i==3 else 18,INK if j==1 else '55636B',False,'FFF6EC' if j==1 else None)
        for j in range(5): border(tb.cell(i,j))
    ty=T0+sum(rh)+40
    text(sl,M,ty,CW,36,para('実習こそ、県内の他社には伝えられない魅力を、プログラムに落とし込む',27,INK,True,lh=1.3),name='魅力見出し')
    cy=ty+56; ch=B0-cy; cw=(CW-2*28)/3
    pts=[('成長産業の上場企業','その根本となる理念がある'),('ニーズに合わせたサービス展開','ご利用者さんに合わせた、実習経験の幅'),('ダイバーシティな環境','女性・技能実習生の採用など（例：県内の女性管理職の割合No.1）')]
    for i,(h,d) in enumerate(pts):
        x=M+i*(cw+28); card(sl,x,cy,cw,ch,name=f'カード_{h}')
        dot(sl,x+34+26,cy+ch/2,52,ORG if i==2 else TEAL2,'番号'); text(sl,x+34,cy+ch/2-26,52,52,para(str(i+1),26,'FFFFFF',True,lh=1.1),align='c',anchor='middle',name=f'番号{i+1}')
        text(sl,x+110,cy+12,cw-140,ch-24,[para(h,23,TEALD,True,after=2,lh=1.3),para(d,18,INK,lh=1.4)],anchor='middle',name=f'魅力_{i+1}')
    note(sl,'※ 他社の記載は公開情報の要約です。県内の女性管理職割合などの実績は、根拠資料の確認が必要です。')
    return sl

# ====================== 9. エフビー流の学び ======================
def s_learn():
    sl=new_slide('エフビー流の学び','介護の現場を体験して学ぶ、4つのステップ',notes='実習サイト「エフビー流の学び」。')
    pill(sl,W/2-300,T0,600,60,TEAL,'帯'); text(sl,W/2-300,T0,600,60,para('介護の現場を体験して学ぶ',29,'FFFFFF',True,lh=1.2),align='c',anchor='middle',name='帯文字')
    steps=[('話して知る','利用者さんの人生にふれる',['昔の暮らしや仕事の話を聴く','笑顔が生まれる瞬間を見る','「ありがとう」をもらう手応え'],TEAL2,TEALD),
     ('見て学ぶ','職員の仕事を観察する',['声かけ・見守りの基本','介護職の一日の流れと仕事の幅','看護師など他職種との連携'],TEAL2,TEALD),
     ('やってみる','できることから体験する',['食事・レクのお手伝い','畑や行事など、地域にふれる','職員がそばでサポート'],ORG,ORGD),
     ('振り返る','気づきから、キャリアを考える',['感じたことを職員と話し合う','資格や仕事の道すじを知る','これからのキャリアを考える','自分に向いているかの見極め'],ORG,ORGD)]
    gap=40; cw=(CW-3*gap)/4; cy=T0+96; ch=B0-cy-110
    for i,(h,s,bl,c,dk) in enumerate(steps):
        x=M+i*(cw+gap); card(sl,x,cy,cw,ch,name=f'カード_{h}')
        dot(sl,x+32+30,cy+40+30,60,c,'番号'); text(sl,x+32,cy+40,60,60,para(str(i+1),30,'FFFFFF',True,lh=1.1),align='c',anchor='middle',name=f'番号{i+1}')
        text(sl,x+112,cy+40,cw-130,60,para(h,32,dk,True,lh=1.2),anchor='middle',name=f'見出し_{h}')
        text(sl,x+32,cy+124,cw-64,60,para(s,20,SUB,True,lh=1.4),name=f'小見出し_{h}')
        hline(sl,x+32,cy+196,x+cw-32,cy+196,LINE,1.2,name='区切り')
        text(sl,x+32,cy+216,cw-64,ch-236,[para('・'+t,20,INK,after=10,lh=1.5) for t in bl],name=f'内容_{h}')
        if i<3:
            a=shape(sl,MSO_SHAPE.RIGHT_ARROW,x+cw+6,cy+ch/2-22,gap-12,44,'2E9E8A',None,name='矢印')
    by=B0-76; a=shape(sl,MSO_SHAPE.LEFT_ARROW,M,by,CW,76,'D4EEE6',None,name='戻り矢印'); a.adjustments[0]=0.5; a.adjustments[1]=0.9
    text(sl,M+90,by,CW-120,76,para('④ 振り返りから、次の ① へ　体験をくり返しながら、学びを深めていく',22,TEALD,True,lh=1.2),align='c',anchor='middle',name='戻り矢印文字')
    note(sl,'※ 文章はサイト上でも仮の内容です（決まり次第、差し替え）。')
    return sl

# ====================== 10. プログラム ======================
def s_program():
    sl=new_slide('実習プログラム','1日で、5日間で。目的に合わせて選べる2つのプログラム',notes='1DAYと5DAYS（P25・P26）。')
    gap=32; lw_=(CW-gap)*0.52; rw=CW-gap-lw_
    def head(x,w,tag,t1,t2,col):
        shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,x,T0,w,84,col,None,rad=24,name=f'帯_{tag}')
        text(sl,x+32,T0,170,84,para(tag,36,'FFFFFF',True,lh=1.2),anchor='middle',name=tag)
        text(sl,x+210,T0+10,w-232,64,[para(t1,24,'FFFFFF',True,lh=1.3),para(t2,18,'FFFFFF',lh=1.3)],anchor='middle',name=f'{tag}_見出し')
    head(M,lw_,'1DAY','1日で、現場をのぞいてみる','9:30〜15:00ごろ　はじめての方に',TEAL2)
    head(M+lw_+gap,rw,'5DAYS','5日間で、じっくり向き合う','DAY1〜DAY5　じっくり学びたい方に',ORG)
    d1=[('9:30','受付とオープニング','メンターが温かく出迎え。会社紹介のショート動画で雰囲気を共有'),
        ('10:00','現場シャドーイング＆その人らしさへの傾聴体験','現場業務のサポートと利用者様へのインタビュー。対話・傾聴が中心'),
        ('12:00','ランチセッション','美味しいご飯と、先輩社員の地方暮らし・働き方のホンネトーク'),
        ('13:00','対話ワーク『100歳までの履歴書』','「どんな大人になっていたいか」から逆算し、大切にしたい「CARE」を言語化'),
        ('14:30','リフレクション＆フィードバック','メンターからの応援メッセージとフィードバックシートをお渡し')]
    d5=[('DAY1','インストール','オリエンテーション・動画鑑賞・目標設定。利用者様の人生のお話に耳を傾ける'),
        ('DAY2-3','現場ケアと人間関係の構築','現場サポートと利用者様へのインタビュー。毎日の振り返り（※実習サイトへ）'),
        ('DAY4','笑顔を届けるプチ企画','学生が考えた「利用者様を喜ばせる小さな企画」を実践'),
        ('DAY5','履歴書の発表会＆結びのランチ','「100歳までの履歴書」の発表、メンター全員からのメッセージ、修了式')]
    y0=T0+84+24; rg=12; rh=(B0-y0-4*rg)/5
    def row(x,w,y,h,tag,title,desc,col,pale,tw):
        card(sl,x,y,w,h,rad=16,name=f'行_{title}')
        pill(sl,x+24,y+h/2-24,tw,48,pale,'時刻'); text(sl,x+24,y+h/2-24,tw,48,para(tag,21,col,True,lh=1.2),align='c',anchor='middle',name=f'時刻_{tag}')
        text(sl,x+24+tw+24,y+10,w-(24+tw+24)-24,h-20,[para(title,23,INK,True,after=2,lh=1.3),para(desc,17,SUB,lh=1.4)],anchor='middle',name=f'行本文_{title}')
    for i,(t,h,d) in enumerate(d1): row(M,lw_,y0+i*(rh+rg),rh,t,h,d,TEALD,PALE,116)
    for i,(t,h,d) in enumerate(d5): row(M+lw_+gap,rw,y0+i*(rh+rg),rh,t,h,d,ORGD,PALEO,124)
    by=y0+4*(rh+rg); bx=M+lw_+gap
    shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,bx,by,rw,rh,'FFF3E4',None,rad=16,name='標準化ボックス')
    text(sl,bx+30,by+10,rw-60,rh-20,[para('体験はサイトへ、運営は標準化',22,ORGD,True,after=4,lh=1.3),para('体験・感想は後日、実習サイトに掲載。学習シートを用意し、プログラムを標準化します。',17,INK,lh=1.45)],anchor='middle',name='標準化本文')
    note(sl,'※ プログラムの内容・日程はサイト上でも「調整中」です。')
    return sl

# ====================== 11. 受け入れ体制 ======================
def s_system():
    sl=new_slide('実習の受け入れ体制','誰が担当しても伝わる、再現性の高い受け入れの仕組み',notes='P27：実習の受け入れ体制。')
    lw_=520; shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,M,T0,lw_,B0-T0,TEAL,None,rad=24,name='方針')
    text(sl,M+48,T0+48,lw_-96,B0-T0-96,[para('実習コンテンツ（体制）',19,'EAF8F4',True,after=30,lh=1.3,spc=2),
        para('誰が担当しても、温かさとメッセージが伝わる。',38,'FFFFFF',True,after=36,lh=1.45),
        para('「再現性の高い仕組み」をつくります。学生向けの学習シートなどを用意し、プログラムを標準化します。',21,'F0FBF8',lh=1.7)],name='方針本文')
    items=[('メンター体制','現場スタッフを「実習メンター」として配置。学生1〜2名につき1名が、親身に伴走します。',TEAL2,TEALD),
     ('標準動画（ツール）','「ショート導入動画」などを活用。誰が説明しても、エフビーの温かさや社風がストレートに伝わります。',TEAL2,TEALD),
     ('実習生の声の資産化','リアルな体験談・本音の感想をWeb上に蓄積・公開。次年度の学生や学校（教授・就職課）への開拓ツールに。',ORG,ORGD),
     ('年間PDCAの循環','定期的に受け入れと振り返りを回し、学校や地域とのつながりを広げていきます。',ORG,ORGD)]
    gx=M+lw_+32; gw=(W-M-gx-32)/2; gh=(B0-T0-32)/2
    for i,(h,d,c,dk) in enumerate(items):
        x=gx+(i%2)*(gw+32); y=T0+(i//2)*(gh+32)
        card(sl,x,y,gw,gh,name=f'カード_{h}')
        dot(sl,x+36+28,y+38+28,56,c,'番号'); text(sl,x+36,y+38,56,56,para(str(i+1),28,'FFFFFF',True,lh=1.1),align='c',anchor='middle',name=f'番号{i+1}')
        text(sl,x+116,y+38,gw-150,56,para(h,27,dk,True,lh=1.2),anchor='middle',name=f'見出し_{h}')
        text(sl,x+36,y+122,gw-72,gh-140,para(d,23,INK,lh=1.65),name=f'説明_{h}')
    note(sl,'出典：1023採用定例資料（実習の受け入れ体制）。')
    return sl

# ====================== 12. 流れ & サイト ======================
def s_flow():
    sl=new_slide('実習の流れ','はじめてでも安心。4つのステップと、サイトで届ける内容',notes='申込から振り返りまでの流れと、サイトのコンテンツ。')
    fl=[('申し込む','フォームから、行きたい日と事業所を選んで申込。質問だけでも大丈夫です。'),('事前の連絡','持ち物や服装、当日の集合場所をお知らせします。'),('実習の当日','職員がそばでサポート。利用者さんとおしゃべりしながら、現場を体験。'),('振り返り','感じたことや気づいたことを、職員と話し合います。')]
    gap=40; cw=(CW-3*gap)/4; ch=232
    for i,(h,d) in enumerate(fl):
        x=M+i*(cw+gap); c=TEAL2 if i<3 else ORG
        card(sl,x,T0,cw,ch,name=f'カード_{h}')
        shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,x,T0,cw,72,c,None,rad=20,name='ステップ帯'); shape(sl,MSO_SHAPE.RECTANGLE,x,T0+40,cw,32,c,None,name='ステップ帯下')
        text(sl,x+30,T0,cw-60,72,para('',10,runs=[(f'STEP 0{i+1}',{'size':18,'bold':True}),('   '+h,{'size':27,'bold':True})],color='FFFFFF',lh=1.2),anchor='middle',name=f'見出し_{h}')
        text(sl,x+30,T0+96,cw-60,ch-110,para(d,21,INK,lh=1.6),name=f'説明_{h}')
        if i<3: shape(sl,MSO_SHAPE.RIGHT_ARROW,x+cw+6,T0+ch/2-22,gap-12,44,'2E9E8A',None,name='矢印')
    sy=T0+ch+44
    text(sl,M,sy,900,38,para('実習サイトで届ける内容',29,INK,True,lh=1.3),name='サイト見出し')
    tiles=[('実習レポート','実習の1日の流れをたどる記事',TEAL2),('職員の声','仕事のやりがいと、実習生へのメッセージ',TEAL2),('人生の先輩の\nメッセージ','ご利用者さんから、実習に来るみなさんへのひとこと',ORG),('お知らせ','実習受け入れ拠点の追加など',TEAL2),('事業所の\n360°ツアー','事業所の中の様子をのぞける',TEAL2),('経営者\nインタビュー','社長に聞いた、これからのまちのカタチ（visions）',ORG)]
    ty=sy+56; tg=24; tw=(CW-5*tg)/6; th=B0-ty-100
    for i,(h,d,c) in enumerate(tiles):
        x=M+i*(tw+tg); card(sl,x,ty,tw,th,rad=18,name=f'タイル_{h}')
        shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,x+24,ty+24,48,8,c,None,rad=4,name='色')
        text(sl,x+24,ty+46,tw-48,th-60,[para(l,23,INK,True,lh=1.3,after=(8 if k==len(h.split('\n'))-1 else 0)) for k,l in enumerate(h.split('\n'))]+[para(d,17,SUB,lh=1.5)],name=f'タイル本文_{h}')
    oy=B0-76; card(sl,M,oy,CW,76,fill='F6F9F8',rad=16,name='そのほか')
    text(sl,M+36,oy,CW-72,76,para('',10,runs=[('そのほか　',{'size':21,'bold':True,'color':TEALD}),('よくある質問／個人情報の取扱い／気になるキーワードから記事を探す／実習の申込フォーム',{'size':20})],lh=1.3),anchor='middle',name='そのほか本文')
    note(sl,'※ 申込フォーム・SNS・問い合わせ先は準備中です。記事の内容はサンプルです。')
    return sl

# ====================== 13. 拠点 ======================
def s_area():
    sl=new_slide('拠点','長野を中心に、信越・北関東に109の拠点',notes='7種109拠点。')
    lw_=900; card(sl,M,T0,lw_,B0-T0,name='グラフカード')
    text(sl,M+40,T0+30,lw_-80,36,para('都県別の拠点数（計109拠点）',27,INK,True,lh=1.3),name='グラフ見出し')
    cd=CategoryChartData(); cd.categories=['長野県','新潟県','埼玉県','群馬県','栃木県']; cd.add_series('拠点数',[57,15,15,12,10])
    gf=sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,px(M+30),px(T0+84),px(lw_-60),px(B0-T0-110),cd); ch=gf.chart; gf.name='拠点数グラフ'
    ch.has_legend=False; ch.has_title=False
    pl=ch.plots[0]; pl.gap_width=50; pl.has_data_labels=True; dl=pl.data_labels
    dl.font.size=Pt(28); dl.font.bold=True; dl.font.name=FONT; dl.position=XL_LABEL_POSITION.OUTSIDE_END; dl.number_format='0'; dl.number_format_is_linked=False
    for i in range(5):
        p_=pl.series[0].points[i]; p_.format.fill.solid(); p_.format.fill.fore_color.rgb=rgb(ORG if i==0 else TEAL2)
    ch.value_axis.visible=False; ch.value_axis.has_major_gridlines=False; ch.value_axis.maximum_scale=66; ch.value_axis.minimum_scale=0
    ca=ch.category_axis; ca.tick_labels.font.size=Pt(22); ca.tick_labels.font.name=FONT; ca.format.line.color.rgb=rgb('C9D6D1')
    rx=M+lw_+32; rw=CW-lw_-32; h1=300
    card(sl,rx,T0,rw,h1,name='サービスカード')
    text(sl,rx+36,T0+28,rw-72,36,para('提供しているサービス　7種',25,INK,True,lh=1.3),name='サービス見出し')
    svc=['有料老人ホーム','グループホーム','デイサービス','小規模多機能','看護小規模多機能型','訪問介護','訪問看護']
    cw_=(rw-72-16)/2
    for k,t in enumerate(svc):
        col=k%2; row=k//2; x=rx+36+col*(cw_+16) if k<6 else rx+36; y=T0+84+row*(52+14)
        pill(sl,x,y,cw_,52,PALE,f'サービス_{t}'); text(sl,x,y,cw_,52,para(t,19,TEALD,True,lh=1.2),align='c',anchor='middle',name=f'サービス文字_{t}')
    y2=T0+h1+32; card(sl,rx,y2,rw,B0-y2,name='ツアーカード')
    text(sl,rx+36,y2+28,rw-72,36,para('360°ツアーで見学できる事業所　9拠点',24,INK,True,lh=1.3),name='ツアー見出し')
    rows=[('長野県','5拠点','安曇野・松本・佐久・諏訪・上田'),('新潟県','1拠点','糸魚川'),('栃木県','2拠点','宇都宮・小山'),('埼玉県','1拠点','羽生')]
    rhh=(B0-y2-96)/4
    for i,(pf,n,pl2) in enumerate(rows):
        y=y2+84+i*rhh
        pill(sl,rx+36,y+rhh/2-24,128,48,PALEO,'県'); text(sl,rx+36,y+rhh/2-24,128,48,para(pf,19,ORGD,True,lh=1.2),align='c',anchor='middle',name=f'県_{pf}')
        text(sl,rx+184,y,100,rhh,para(n,22,INK,True,lh=1.2),anchor='middle',name=f'拠点数_{pf}')
        text(sl,rx+290,y,rw-326,rhh,para(pl2,19,SUB,lh=1.3),anchor='middle',name=f'所在地_{pf}')
    note(sl,'※ 出典：エフビー介護サービス コーポレートサイト（360°ツアー）ほか、実習サイトの掲載内容。')
    return sl

for f in (s_ring,s_loop,s_overview,s_market,s_why,s_philosophy,s_emotion,s_history,s_scale,s_sales,s_compare,s_learn,s_program,s_system,s_flow,s_area): f()
N=len(prs.slides)
for k,sl in enumerate(prs.slides,1):
    text(sl,W-M-120,B0+24,120,22,para(f'{k} / {N}',15,GRAY,lh=1.3),align='r',name='ページ番号')
prs.save('共育実習_図解.pptx'); print(N)
