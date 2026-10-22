# -*- coding: utf-8 -*-
"""共育実習 図解デッキ — single clean build with a strict layout system.
Canvas 1730x973 px (true 16:9). Margins 88. Exact line spacing everywhere."""
import math
from PIL import Image
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

_CAST=[(('selfie',84),('boy',84)),(('elder',92),('care',66)),(('runners',60),('picnic',74),('boy',80)),(('van',62),('boy',84)),(('runner',84),('selfie',80)),(('care',70),('elder',90),('boy',76))]
_cn=[0]
def _cast(sl,title):
    cast=_CAST[_cn[0]%len(_CAST)]; _cn[0]+=1
    x=max(1260,M+len(title)*44+40); base=152
    for nm,h in cast:
        im=Image.open('ill/'+nm+'.png'); w=h*im.width/im.height
        if x+w>W-60: break
        p=sl.shapes.add_picture('ill/'+nm+'.png',px(x),px(base-h),px(w),px(h)); p.name='イラスト_'+nm; x+=w+22

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
    _cast(sl,title)
    if notes: sl.notes_slide.notes_text_frame.text=notes
    return sl
def note(sl,t): text(sl,M,B0+26,1300,22,para(t,15,GRAY,lh=1.3),name='注記')

# ====================== 1. 共創モデル ======================
def s_ring():
    sl=new_slide('共育実習','共育実習の共創モデル','学ぶ人も、迎える人も、地域も。みんなが共に育つ')
    cx,cy,Ro,Ri=865,552,276,196
    segs=[(0,60,'F28C3C','C8651A','エフビー介護サービス','エフビー','若い世代との出会い',['学生から学び、地域の担い手づくりに','関わることができます。']),
     (60,120,'F7AB67','C8651A','社員','社員','学びと生きがいが育つ',['学生に教えることで、仕事の意味を再発見。','利用者の生きがいも育ちます。']),
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
    sl=new_slide('実習のブランド','実習のブランドは、先輩の声で育っていく','回るほど、大学にも学生さんにも、メリットが広がります')
    gap=22; cw=(CW-3*gap)/4; y0=T0+8
    steps=[('共育実習を行う',TEAL2,'現場を体験して、キャリアを考える',  '単位つき・社会テーマ型の、講義を生かす実践の場が増えます','現場の体験から、「自分に合う仕事か」を考えるきっかけになります'),
           ('声が集まる','2E9E8A','学びの成果が、見える形に','学生の気づきや感想が、先生にも伝わり、指導に生かせます','自分の体験が「価値のある声」として残ります'),
           ('実習サイトに載せる',ORG,'内容と口コミを、公開する','プログラムと口コミで、受け入れを安心して判断できます','先輩のリアルな声で、参加前に実習のイメージがつかめます'),
           ('見て、動く','F7AB67','選んで、次の一歩へ','実習の評判が、学部・学科の魅力と連携先の広がりにつながります','自分に合う実習を選び、次の学びと進路へつなげられます')]
    for i,(h,c,_,u,st) in enumerate(steps):
        x=M+i*(cw+gap)
        shape(sl,MSO_SHAPE.PENTAGON if i==0 else MSO_SHAPE.CHEVRON,x,y0,cw+(gap if i<3 else 0),104,c,None,name=f'手順_{h}')
        text(sl,x+(30 if i==0 else 54),y0,cw-80,104,[para(f'STEP {i+1}',16,'FFFFFF',True,lh=1.2,spc=2),para(h,25,'FFFFFF',True,lh=1.25)],anchor='middle',name=f'手順文_{h}')
        for j,(lab,body,lc,pc) in enumerate((('大学にとって',u,ORGD,PALEO),('学生さんにとって',st,TEALD,PALE))):
            yy=y0+150+j*232
            pill(sl,x,yy,200,40,pc,'ラベル'); text(sl,x,yy,200,40,para(lab,20,lc,True,lh=1.2),align='c',anchor='middle',name=f'ラベル_{lab}')
            text(sl,x,yy+60,cw-8,150,para(body,23,INK,lh=1.6),name=f'本文_{h}_{lab}')
    for j in (1,):
        hline(sl,M,y0+150+232-26,M+CW,y0+150+232-26,LINE,1.5,name='区切り')
    ay=B0-66
    a=shape(sl,MSO_SHAPE.LEFT_ARROW,M,ay,CW,66,PALE,None,name='循環矢印'); a.adjustments[0]=0.62; a.adjustments[1]=0.9
    text(sl,M+110,ay,CW-160,66,para('次の大学・次の学生へ。回るほど、実習への信頼が積み上がります',24,TEALD,True,lh=1.2),anchor='middle',name='循環文')
    return sl

def _ill(sl,name,x,y,h=None,w=None,al='l'):
    im=Image.open('ill/'+name+'.png'); r=im.width/im.height
    if h is None: h=w/r
    w=h*r
    p=sl.shapes.add_picture('ill/'+name+'.png',px(x if al=='l' else x-w),px(y),px(w),px(h)); p.name='イラスト_'+name; return w

def s_cover():
    """表紙 パターンA：深い緑 × 下いっぱいのイラスト"""
    DEEP='1E4B42'; sl=prs.slides.add_slide(prs.slide_layouts[6])
    shape(sl,MSO_SHAPE.RECTANGLE,0,0,W,H,DEEP,None,name='背景')
    h_=W*420/1190; y0=H-h_
    p=sl.shapes.add_picture('cover_illust.png',0,px(y0),px(W),px(h_)); p.name='表紙イラスト（公式LINEバナーより）'
    edge=lambda x:y0+34+18*math.sin(2*math.pi*x/W*1.5+0.6)
    poly(sl,[(0,y0-4),(W,y0-4)]+[(W-i*W/120,edge(W-i*W/120)) for i in range(121)],DEEP,'波')
    text(sl,100,70,900,30,para('EFB CARE SERVICE  ×  CO-GROWTH PRACTICE',20,'E8C872',True,lh=1.3,spc=5),name='英字')
    text(sl,96,112,1100,170,para('共育実習',130,'FBF8EC',True,lh=1.1),name='タイトル')
    hline(sl,104,292,200,292,'E8C872',3,name='ライン')
    text(sl,100,316,1200,46,para('学ぶ人も、迎える人も、地域も。みんなが共に育つ。',28,'DDEBE0',lh=1.4),name='キャッチ')
    text(sl,W-100-420,76,420,32,para('大学の先生・学生のみなさまへ',20,'E8C872',True,lh=1.3,spc=2),align='r',name='宛名')
    return sl

def s_cover_mint():
    """表紙：ミントの落ち着いた面に、イラストを少しだけ"""
    sl=prs.slides.add_slide(prs.slide_layouts[6])
    shape(sl,MSO_SHAPE.RECTANGLE,0,0,W,H,BAND,None,name='背景')
    def ridge(pts,col,name,bottom=H):
        out=[]
        for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
            for t in range(0,12):
                u=t/12; v=(1-math.cos(math.pi*u))/2; out.append((x0+(x1-x0)*u,y0+(y1-y0)*v))
        out.append(pts[-1]); poly(sl,[(0,bottom)]+out+[(W,bottom)],col,name)
    dot(sl,1380,330,300,'8ACFC0','太陽'); dot(sl,1380,330,180,'A6DDD1','太陽中')
    ridge([(0,640),(170,540),(330,470),(520,590),(760,700),(980,745),(1200,670),(1400,520),(1580,430),(1730,540)],'8ACFC0','遠い山')
    ridge([(0,780),(200,690),(430,745),(720,815),(1000,850),(1300,800),(1500,690),(1730,730)],'64B3A1','手前の山')
    ridge([(0,905),(500,885),(900,862),(1300,870),(1730,835)],'E3F4F0','盆地の底')
    text(sl,120,170,900,36,para('エフビー介護サービス',28,'EAF8F4',True,lh=1.3,spc=6),name='小見出し')
    text(sl,120,230,900,260,para('共育実習',150,'FFFFFF',True,lh=1.15),name='タイトル')
    hline(sl,124,500,300,500,'FCE08E',4,name='ライン')
    text(sl,120,540,820,160,[para('学ぶ人も、迎える人も、地域も。',38,'FFFFFF',True,lh=1.5),para('みんなが共に育つ、ケアの現場の実習。',38,'FFFFFF',True,lh=1.5)],name='キャッチ')
    text(sl,120,820,900,34,para('大学の先生・学生のみなさまへ',22,'EAF8F4',True,lh=1.3,spc=2),name='宛名')
    for cx,cy,d,c in ((1110,250,26,'FCE08E'),(1250,170,16,'FFFFFF'),(1680,520,22,'FCE08E'),(1000,470,14,'F7AB67'),(1640,160,18,'F7AB67'),(1560,640,12,'FCE08E')): dot(sl,cx,cy,d,c,'飾り')
    _ill(sl,'van',1280,555,w=190)
    _ill(sl,'picnic',1470,640,w=180)
    _ill(sl,'care',1010,590,h=125)
    base=925; x=760
    for nm,h in (('runner',180),('selfie',210),('boy',195),('elder',225),('runners',118)):
        x+=_ill(sl,nm,x,base-h,h=h)+6
    return sl

def s_cover_b():
    """表紙 パターンB：やわらかな緑 × アーチの窓"""
    sl=prs.slides.add_slide(prs.slide_layouts[6])
    shape(sl,MSO_SHAPE.RECTANGLE,0,0,W,H,'DCE8DC',None,name='背景')
    ax,ay,aw,ah=1010,80,620,813
    ar=shape(sl,MSO_SHAPE.ROUND_2_SAME_RECTANGLE,ax,ay,aw,ah,'F6F9EE',None,name='アーチ'); ar.adjustments[0]=0.5; ar.adjustments[1]=0
    poly(sl,[(ax,700),(ax+190,640),(ax+400,690),(ax+aw,625),(ax+aw,ay+ah),(ax,ay+ah)],'B5DCCB','丘1')
    poly(sl,[(ax,790),(ax+250,742),(ax+500,785),(ax+aw,735),(ax+aw,ay+ah),(ax,ay+ah)],'7FBBA6','丘2')
    _ill(sl,'van',ax+170,ay+130,w=270)
    _ill(sl,'selfie',ax+24,ay+385,h=250)
    _ill(sl,'boy',ax+280,ay+430,h=235)
    _ill(sl,'elder',ax+415,ay+360,h=290)
    shape(sl,MSO_SHAPE.RECTANGLE,ax-2,ay+ah-8,aw+4,8,'DCE8DC',None,name='アーチ下端')
    text(sl,100,100,900,30,para('エフビー介護サービス',24,'2F6F5E',True,lh=1.3,spc=6),name='小見出し')
    text(sl,96,150,900,200,para('共育実習',150,'1F5A4C',True,lh=1.1),name='タイトル')
    hline(sl,104,400,200,400,'C9A24A',3,name='ライン')
    text(sl,100,440,820,130,[para('学ぶ人も、迎える人も、地域も。',34,'26323A',True,lh=1.5),para('みんなが共に育つ、ケアの現場の実習。',34,'26323A',True,lh=1.5)],name='キャッチ')
    text(sl,100,820,800,30,para('大学の先生・学生のみなさまへ',20,'2F6F5E',True,lh=1.3,spc=2),name='宛名')
    return sl

def s_vision():
    sl=prs.slides.add_slide(prs.slide_layouts[6])
    shape(sl,MSO_SHAPE.RECTANGLE,0,0,W,H,BAND,None,name='背景')
    poly(sl,[(1100,973),(1330,760),(1450,850),(1580,700),(1730,860),(1730,973)],MTN,'山1')
    text(sl,120,90,900,36,para('PROJECT VISION',24,'EAF8F4',True,lh=1.3,spc=8),name='小見出し')
    text(sl,120,140,1500,200,[para('長寿の国、長野発、',68,'FFFFFF',True,lh=1.25),para('希望の地域モデルづくりへ',68,'FFFFFF',True,lh=1.25)],name='ビジョン')
    hline(sl,124,380,300,380,'FCE08E',4,name='ライン')
    P=lambda t,**k: para(t,27,'F0FBF8',lh=1.75,**k)
    text(sl,120,410,1500,500,[
      P('「実習」と聞いて、どんなイメージを持ちますか？大変そう？ 自分にはまだ早いかも？',after=2),
      P('もし少しでも「やってみたい」と思うなら、ぜひ、私たちの現場に来てください。',after=20),
      P('共育実習は、「教える・教わる」だけの実習ではありません。',after=2),
      P('学生さんも、先生も、利用者さんも、社員も、地域の人も。みんなで福祉の人材を育てていく取り組みです。',after=2),
      P('学生さんは現場から学び、社員は学生さんから、仕事の意味を学びなおす。',after=20),
      P('人が育てば、地域の幸福度が高まる。',after=2),
      P('これから人口が減っていく長野で、支え合う人が育つことが、地域の希望になる。',after=20),
      para('介護や老後の話は、なんだか暗い。そんなイメージを、一緒にひっくり返したい。',27,'FFFFFF',True,lh=1.75)],name='実習ステートメント')
    return sl

def s_agenda():
    sl=new_slide('アジェンダ','このあと、お伝えすること')
    pw=700; ph=B0-T0
    shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,M,T0,pw,ph,BAND,None,rad=28,name='コンセプト面')
    text(sl,M+56,T0+48,pw-112,30,para('CARE PRACTICE',20,'EAF8F4',True,lh=1.3,spc=6),name='コンセプト小見出し')
    text(sl,M+56,T0+96,pw-90,300,[para('FUN LIFE!',92,'FFFFFF',True,lh=1.1),para('FUN LOCAL!',92,'FCE08E',True,lh=1.1)],name='コンセプト')
    text(sl,M+56,T0+400,pw-112,60,para('生きがい、持ち寄る。地域の未来。',32,'FFFFFF',True,lh=1.4),name='コンセプト文')
    def pic(name,x,y,h,al='l'):
        im=Image.open('ill/'+name+'.png'); w=h*im.width/im.height
        if w>200: h=h*200/w; w=200; y=y+0
        p=sl.shapes.add_picture('ill/'+name+'.png',px(x if al=='l' else x-w),px(y),px(w),px(h)); p.name='イラスト_'+name; return w
    pic('picnic',M+60,T0+ph-190,150); pic('runners',M+pw-60-230,T0+ph-170,125)
    rx=M+pw+70; rw=W-M-rx; rh=ph/5
    items=[('共育実習が目指すこと','ビジョンと、みんなで育つ共創モデル','P.2–4',TEAL2,'selfie'),
           ('いま、なぜ福祉人材か','人口の変化と、介護の需要、福祉の価値','P.5–7',TEAL2,'elder'),
           ('エフビー介護サービスを知る','介護の考え方、沿革、事業の展開と成長','P.8–12',ORG,'van'),
           ('実習で得られること','他社との違い、プログラム、受け入れ体制','P.13–16',ORG,'care'),
           ('実習のひろがり','ブランドの育ち方と、応募までの流れ','P.17–18',TEAL2,'boy')]
    for i,(h,d,pg,c,im) in enumerate(items):
        y=T0+i*rh
        if i: hline(sl,rx,y,W-M,y,LINE,1.5,name='区切り')
        dot(sl,rx+34,y+rh/2,64,c,'番号点'); text(sl,rx+2,y+rh/2-32,64,64,para(str(i+1),26,'FFFFFF',True,lh=1.1),align='c',anchor='middle',name=f'番号{i+1}')
        text(sl,rx+110,y+10,rw-110-210,rh-20,[para(h,31,INK,True,after=6,lh=1.3),para(d,20,SUB,after=8,lh=1.45),para(pg,18,TEALD if c==TEAL2 else ORGD,True,lh=1.3)],anchor='middle',name=f'項目_{h}')
        pic(im,W-M-10,y+14,rh-28,al='r')
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
    note(sl,'※ 日程・内容は調整中です。決まり次第ご案内します。')
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
            w=len(t)*21+44; pill(sl,x,y,w,44,PALEO if c=='o' else PALE,'チップ'); text(sl,x,y,w,44,para(t,19,ORGD if c=='o' else TEALD,True,lh=1.2),align='c',anchor='middle',name=f'チップ_{t}'); x+=w+6
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

POP_PRJ2=[12441, 12384, 12326, 12266, 12204, 12141, 12077, 12012, 11945, 11877, 11807, 11736, 11664, 11590, 11515, 11439, 11362, 11284, 11204, 11124, 11043, 10962, 10880, 10798, 10716, 10634, 10551, 10469, 10386, 10303, 10219, 10135, 10051, 9965, 9879, 9792, 9704, 9615, 9525, 9434, 9343, 9251, 9159, 9066, 8974, 8882, 8790, 8700]
UN_POP={2075:8575,2080:8284,2085:8030,2090:7796,2095:7574,2100:7364}
CARE5=[('2000',3.3),('2005',5.9),('2010',7.5),('2015',9.5),('2020',11.4)]

def bubble(sl,x,y,w,h,tx,ty,fill,name='吹き出し',rad=0.22):
    s=sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGULAR_CALLOUT,px(x),px(y),px(w),px(h))
    s.fill.solid(); s.fill.fore_color.rgb=rgb(fill); s.line.fill.background()
    s.adjustments[0]=(tx-(x+w/2))/w; s.adjustments[1]=(ty-(y+h/2))/h; s.adjustments[2]=rad
    s.name=name; _fix(s); return s

def _axis_style(ch,vmax,unit,fmt='#,##0',skip=None):
    va=ch.value_axis; va.minimum_scale=0; va.maximum_scale=vmax; va.major_unit=unit; va.has_major_gridlines=True
    va.major_gridlines.format.line.color.rgb=rgb('E8EFEC'); va.tick_labels.font.size=Pt(13); va.tick_labels.font.name=FONT
    va.tick_labels.number_format=fmt; va.tick_labels.number_format_is_linked=False; va.format.line.fill.background()
    ca=ch.category_axis; ca.tick_labels.font.size=Pt(13); ca.tick_labels.font.name=FONT; ca.format.line.color.rgb=rgb('C9D6D1')
    if skip:
        for tag in ('c:tickLblSkip','c:tickMarkSkip'):
            el=ca._element.find(qn(tag))
            if el is None: el=etree.SubElement(ca._element,qn(tag))
            el.set('val',str(skip))

# ====================== 人口の推移（〜2100年） ======================
def s_pop():
    sl=new_slide('時代の背景','日本の人口は、2008年をピークに減り続けていきます',notes='人口：1947〜2022年は実績（総務省統計局・人口統計資料集）、2023〜2070年は推計（社人研・令和5年推計 出生中位）、2075〜2100年は国連推計（5年ごと）。')
    text(sl,M,T0-6,900,30,para('日本の総人口（万人）  第一次ベビーブーム（1947年）から2100年まで',20,SUB,lh=1.3),name='グラフ見出し')
    yrs=list(range(1947,2101)); cd=CategoryChartData(); cd.categories=[str(y) for y in yrs]
    act=POP_ACT+[None]*(len(yrs)-len(POP_ACT))
    prj=[None]*len(POP_ACT)+POP_PRJ2+[None]*30
    anc={2070:8700,**UN_POP}; ks=sorted(anc)
    def _itp(y):
        a=max(k for k in ks if k<=y); b=min(k for k in ks if k>=y)
        return anc[a] if a==b else round(anc[a]+(anc[b]-anc[a])*(y-a)/(b-a))
    un=[None]*(len(POP_ACT)+len(POP_PRJ2))+[_itp(y) for y in range(2071,2101)]
    cd.add_series('実績',act); cd.add_series('推計（社人研）',prj); cd.add_series('参考（国連推計。5年ごとの値を結んだ年次）',un)
    cx,cy,cw,chh=M-8,T0+30,CW+16,B0-T0-30
    gf=sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,px(cx),px(cy),px(cw),px(chh),cd); gf.name='総人口グラフ'; ch=gf.chart
    from pptx.enum.chart import XL_LEGEND_POSITION
    ch.has_legend=True; ch.legend.include_in_layout=False; ch.legend.font.size=Pt(14); ch.legend.font.name=FONT; ch.legend.position=XL_LEGEND_POSITION.BOTTOM
    ch.has_title=False; pl=ch.plots[0]; pl.gap_width=15; pl.overlap=100
    for ser,c in zip(pl.series,(TEAL2,ORG,'F7C9A0')): ser.format.fill.solid(); ser.format.fill.fore_color.rgb=rgb(c)
    _axis_style(ch,18000,3000,skip=10)
    px0=cx+84; pw=cw-84-14; xi=lambda y: px0+(y-1947+.5)*pw/len(yrs)
    ytop=cy+14; yb=cy+chh-84; yv=lambda v: yb-(yb-ytop)*v/18000
    bubble(sl,xi(2008)-250,T0+66,300,84,xi(2008),yv(12808)-6,TEAL2,'吹き出し_2008')
    text(sl,xi(2008)-236,T0+72,272,72,[para('2008年がピーク',17,'EAF8F4',True,lh=1.3),para('1億2,808万人',28,'FFFFFF',True,lh=1.2)],anchor='middle',name='吹き出し文_2008')
    bubble(sl,xi(2050)-130,T0+104,270,84,xi(2050),yv(10469)-6,ORG,'吹き出し_2050')
    text(sl,xi(2050)-116,T0+110,244,72,[para('2050年',17,'FFF4EA',True,lh=1.3),para('約1億469万人',28,'FFFFFF',True,lh=1.2)],anchor='middle',name='吹き出し文_2050')
    bubble(sl,xi(2100)-300,T0+176,290,84,xi(2100)-6,yv(7364)-6,'E9A56B','吹き出し_2100')
    text(sl,xi(2100)-286,T0+182,262,72,[para('2100年',17,'FFF4EA',True,lh=1.3),para('約7,364万人',28,'FFFFFF',True,lh=1.2)],anchor='middle',name='吹き出し文_2100')
    note(sl,'出典：総務省統計局／社人研 令和5年推計・出生中位（〜2070年）／国連 World Population Prospects（2075年〜は5年ごとの値を直線で結んだ参考値）')
    return sl

# ====================== 介護の市場（5年ごと） ======================
def s_market():
    sl=new_slide('時代の背景','介護の社会保障給付費は、2040年度に向けて広がります',notes='介護費：社会保障費用統計 第8表「介護対策」（2000〜2020年度）、2025・2040年度は厚生労働省「2040年を見据えた社会保障の将来見通し」計画ベース。')
    lw_=1010
    text(sl,M,T0-6,lw_,30,para('社会保障給付費「介護」の推移（兆円・年度）  5年ごとの比較',20,SUB,lh=1.3),name='グラフ見出し')
    cats=[c for c,_ in CARE5]+['2025','2030','2035','2040']; cd=CategoryChartData(); cd.categories=cats
    cd.add_series('実績（社会保障費用統計）',[v for _,v in CARE5]+[None]*4); cd.add_series('見通し（厚生労働省）',[None]*5+[15.3,None,None,25.8]); cd.add_series('参考：2025年度と2040年度を直線で補間',[None]*6+[18.8,22.3,None])
    gf=sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,px(M-8),px(T0+30),px(lw_),px(B0-T0-30),cd); gf.name='介護費グラフ'; ch=gf.chart
    from pptx.enum.chart import XL_LEGEND_POSITION
    ch.has_legend=True; ch.legend.include_in_layout=False; ch.legend.font.size=Pt(14); ch.legend.font.name=FONT; ch.legend.position=XL_LEGEND_POSITION.TOP
    ch.has_title=False; pl=ch.plots[0]; pl.gap_width=45; pl.overlap=100; pl.has_data_labels=True; dl=pl.data_labels
    dl.font.size=Pt(20); dl.font.bold=True; dl.font.name=FONT; dl.number_format='0.0'; dl.number_format_is_linked=False; dl.position=XL_LABEL_POSITION.OUTSIDE_END
    for ser,c in zip(pl.series,(TEAL2,ORG,'F7C9A0')): ser.format.fill.solid(); ser.format.fill.fore_color.rgb=rgb(c)
    _axis_style(ch,30,10); ch.value_axis.visible=False; ch.value_axis.has_major_gridlines=False
    ch.category_axis.tick_labels.font.size=Pt(18)
    rx=M+lw_+50; rw=W-M-rx
    bubble(sl,rx,T0+40,rw,150,rx+40,T0+250,TEAL2,'吹き出し_8倍',0.14)
    text(sl,rx+34,T0+52,rw-68,126,[para('2000年度と比べて',18,'EAF8F4',True,lh=1.3),para('2040年度は約8倍',34,'FFFFFF',True,lh=1.25)],anchor='middle',name='吹き出し文_8倍')
    ty=T0+300
    for h,d,c in (('65歳以上の割合',['2020年 28.6%  →  2050年 37.1%','2100年には 約38.7%（国連推計）'],TEALD),('支える人は減っていく',['15〜64歳の人口は','2020年の7,509万人から減少が続きます'],ORGD)):
        shape(sl,MSO_SHAPE.RECTANGLE,rx,ty+4,6,112,c,None,name='ライン')
        text(sl,rx+24,ty,rw-24,124,[para(h,22,c,True,after=4,lh=1.3)]+[para(t,18,INK,lh=1.5) for t in d],name=f'補足_{h}')
        ty+=160
    note(sl,'出典：社人研『社会保障費用統計』（〜2020年度）／厚生労働省『2040年を見据えた社会保障の将来見通し』計画ベース。2030・2035年度は公表値がなく、直線補間の参考値')
    return sl

# ====================== 沿革（西暦の目盛り） ======================
def s_history():
    sl=new_slide('沿革','福祉用具から、地域に根ざす介護の総合企業へ',notes='沿革。西暦は5年ごとの目盛り。')
    Y0,Y1=1987,2026; X0,X1=130,1600; xy=lambda y:X0+(y-Y0)*(X1-X0)/(Y1-Y0); yc=500; bh=64; ev=(1987,2000,2002,2019,2022,2026)
    shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,X0-44,yc-bh/2,X1-X0+88,bh,PALE,None,rad=bh/2,name='年表の帯')
    for y in range(Y0,Y1+1):
        x=xy(y)
        if y in ev: dot(sl,x,yc,bh-6,ORG if y!=2026 else ORGD,f'年_{y}'); text(sl,x-34,yc-16,68,32,para(str(y),17,'FFFFFF',True,lh=1.2),align='c',anchor='middle',name=f'年ラベル_{y}')
        elif y%5==0 and y not in (2000,2020,2025): text(sl,x-30,yc-14,60,28,para(str(y),18,TEALD,True,lh=1.2),align='c',anchor='middle',name=f'年ラベル_{y}')
        else: hline(sl,x,yc-6,x,yc+6,'B9DDD5',1.5,name='目盛り')
    def block(y,up,head,line,tag,al='l',w=380,hh=190):
        x=xy(y); top=yc-bh/2-30-hh if up else yc+bh/2+30
        if up: hline(sl,x,top+hh+4,x,yc-bh/2,TEAL2,2,name='接続線')
        else: hline(sl,x,yc+bh/2,x,top-4,TEAL2,2,name='接続線')
        bx=x if al=='l' else x-w
        text(sl,bx,top,w,hh,[para(tag,22,ORGD,True,lh=1.3),para(head,32,INK,True,after=6,lh=1.3),para(line,21,SUB,lh=1.5)],anchor='bottom' if up else 'top',align=al,name=f'沿革_{y}')
    block(1987,True,'エフビー信州を設立','フランスベッドの代理店から','1987年')
    block(2002,True,'商号を変更','エフビー介護サービスへ','2002年')
    block(2022,True,'東証に上場','スタンダード市場へ','2022年',al='r')
    block(2000,False,'レンタル開始','福祉用具の取り扱いを広げる','2000年')
    block(2019,False,'海外人材を受け入れ','ベトナム・ネパールなど','2019年',al='r',w=420)
    ry=yc+bh/2+290; x1,x2=xy(2003),xy(2018)
    shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,x1,ry,x2-x1,16,TEAL2,None,rad=8,name='期間バー')
    text(sl,x1,ry+26,x2-x1,70,[para('居宅介護・小規模多機能へ事業を広げる',24,TEALD,True,lh=1.3)],name='事業の広がり')
    bubble(sl,W-M-330,yc+bh/2+150,330,150,xy(2026),yc+bh/2+6,ORG,'吹き出し_現在',0.14)
    text(sl,W-M-300,yc+bh/2+160,290,130,[para('現在',21,'FFF4EA',True,lh=1.3),para('7種109拠点',34,'FFFFFF',True,lh=1.2),para('従業員 1,250名',22,'FFFFFF',lh=1.4)],anchor='middle',name='吹き出し文_現在')
    note(sl,'※ 出典：エフビー介護サービス 企業説明会資料、経営者ヒアリング、決算説明資料（従業員数は2023年4月時点）。')
    return sl

# ====================== 6. 小規模 × 多拠点 × 7つのサービス ======================
def s_scale():
    sl=new_slide('事業の展開','小規模な施設を、地域ごとに。7つのサービスで暮らしを支える',notes='小規模・多拠点・サービスの見せ方。')
    ph=262; lw_=760
    shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,M,T0,lw_,ph,TEAL,None,rad=24,name='こだわり')
    text(sl,M+48,T0+34,lw_-96,ph-50,[para('わたしたちのちょっとしたこだわり',19,'EAF8F4',True,after=10,lh=1.3,spc=2),
        para('大規模な施設ではなく、',38,'FFFFFF',True,lh=1.3),para('小規模な施設をメインに展開する。',38,'FFFFFF',True,after=12,lh=1.3),
        para('地域の文化・風土を取り入れた、きめ細やかなサービス。住み慣れた地元で、長く生活できる環境を。',19,'F0FBF8',lh=1.55)],name='こだわり本文')
    rx=M+lw_+60; rw=CW-lw_-60
    text(sl,rx,T0+26,rw,34,para('多拠点で、地域に根ざす',24,INK,True,lh=1.3),name='拠点見出し')
    sw=rw/3
    for i,(n,u,c) in enumerate([('109','拠点',TEALD),('7','種のサービス',TEALD),('5','県',ORGD)]):
        x=rx+i*sw
        if i: hline(sl,x-14,T0+90,x-14,T0+188,LINE,1,name='区切り')
        text(sl,x,T0+78,sw-24,150,[para('',10,runs=[(n,{'size':72,'bold':True,'color':c})],lh=1.1,after=0),para(u,22,INK,True,lh=1.3,after=4)],name=f'数字_{u}')
    # services
    sy=T0+ph+34
    text(sl,M,sy,900,36,para('暮らし方に合わせて選べる、7つのサービス',28,INK,True,lh=1.3),name='サービス見出し')
    gy=sy+54; gh=B0-gy; gw=(CW-2*28)/3
    groups=[('自宅で暮らし続ける','自宅での生活を支援',TEAL2,[('訪問介護','ご自宅で、生活を支援'),('訪問看護','ご自宅へ、看護を届ける')]),
            ('通い・訪問・泊まりで支える','小規模多機能で、暮らしを支える',ORG,[('デイサービス','通いで過ごす'),('小規模多機能型','通い・訪問・泊まりを組み合わせて'),('看護小規模多機能型','看護も組み合わせて')]),
            ('住まいで暮らす','居住いただき、支援する','2E9E8A',[('有料老人ホーム','住まいで、暮らしを支援'),('グループホーム','少人数で暮らす、家庭的な雰囲気')])]
    for i,(h,s,c,items) in enumerate(groups):
        x=M+i*(gw+28)
        shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,x,gy,gw,84,c,None,rad=20,name=f'ヘッダー_{h}')
        shape(sl,MSO_SHAPE.RECTANGLE,x,gy+52,gw,32,c,None,name='ヘッダー下')
        text(sl,x+32,gy+12,gw-64,62,[para(h,24,'FFFFFF',True,lh=1.25),para(s,17,'FFFFFF',lh=1.3)],anchor='middle',name=f'見出し_{h}')
        th=(gh-84-36-(len(items)-1)*12)/max(len(items),2) if len(items)<3 else (gh-84-36-24)/3
        th=min(th,138)
        for j,(n,d) in enumerate(items):
            ty=gy+84+18+j*(th+12)
            hline(sl,x+20,ty+th+6,x+gw-20,ty+th+6,LINE,1,name='区切り')
            dot(sl,x+20+26,ty+th/2,14,c,'ドット')
            text(sl,x+20+50,ty+8,gw-40-70,th-16,[para(n,23,INK,True,lh=1.3),para(d,17,SUB,lh=1.4)],anchor='middle',name=f'サービス_{n}')
    note(sl,'出典：企業説明会資料、経営者ヒアリング、実習サイトの掲載内容。サービスの分け方は暮らし方に合わせた整理です。')
    return sl

# ====================== 7. 売上の推移 ======================
def s_sales():
    sl=new_slide('事業の成長','事業は着実に成長。上場企業ならではの安心感',notes='売上推移（26期〜36期）。出典：企業説明会資料。')
    lw_=1040; ph=B0-T0
    text(sl,M,T0+4,600,36,para('売上の推移（26期〜36期）',27,INK,True,lh=1.3),name='売上見出し')
    # legend
    lx=M+lw_-420
    for k,(nm,c) in enumerate([('用具',TEAL2),('介護',ORG),('居宅','F2C14E')]):
        x=lx+k*140; shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,x,T0+10,22,22,c,None,rad=5,name=f'凡例_{nm}')
        text(sl,x+32,T0+6,100,30,para(nm,20,INK,True,lh=1.3),name=f'凡例文字_{nm}')
    text(sl,M,T0+46,600,26,para('単位：百万円',16,SUB,lh=1.3),name='単位')
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
    bx=x0+10*(bw+gap)+bw/2
    bubble(sl,bx-470,T0+84,360,96,bx-26,topy-40,ORG,'吹き出し_成長')
    text(sl,bx-444,T0+92,310,80,[para('2013年 → 2023年',18,'FFF4EA',True,lh=1.3),para('10年で約2.5倍に成長',28,'FFFFFF',True,lh=1.25)],anchor='middle',name='吹き出し文_成長')
    x2=M+lw_+60; w2=CW-lw_-60; hline(sl,x2-30,T0+10,x2-30,B0-10,LINE,1.5,name='区切り')
    text(sl,x2+36,T0+30,w2-72,36,para('これから目指すこと',26,INK,True,lh=1.3),name='戦略見出し')
    blocks=[('福祉用具事業',['福祉用具のラインナップの充実','より多くの方へのご提案'],TEAL2),('介護事業',['事業所の運営方法の見直し','新たな介護サービスへの挑戦','ニーズにあったきめ細やかなサービス'],TEAL2),('人と技術',['ICT・DXを進めながらも、介護には人の力が不可欠。業務効率化と質の高いサービスの両立を目指します'],ORG)]
    y=T0+100; hs=[150,226,150]; gp=(ph-100-24-sum(hs))/2
    for (h,items,c),bh in zip(blocks,hs):
        pill(sl,x2+36,y,176,40,PALE if c==TEAL2 else PALEO,'タグ'); text(sl,x2+36,y,176,40,para(h,19,TEALD if c==TEAL2 else ORGD,True,lh=1.2),align='c',anchor='middle',name=f'タグ文字_{h}')
        text(sl,x2+36,y+54,w2-72,bh-54,[para('・'+t,19,INK,after=6,lh=1.45) for t in items],name=f'戦略_{h}')
        y+=bh+gp
    note(sl,'※ 売上は用具・介護・居宅の合計（エフビー介護サービス 企業説明会資料）。')
    return sl

# ====================== 社会の変化（人口・介護市場） ======================
POP_ACT=[7810, 8000, 8177, 8320, 8454, 8581, 8698, 8824, 8928, 9017, 9093, 9177, 9264, 9342, 9429, 9518, 9616, 9718, 9828, 9904, 10020, 10133, 10254, 10372, 10514, 10760, 10910, 11057, 11194, 11309, 11416, 11519, 11616, 11706, 11790, 11873, 11954, 12030, 12105, 12166, 12224, 12274, 12320, 12361, 12410, 12457, 12494, 12526, 12557, 12586, 12616, 12647, 12667, 12693, 12732, 12749, 12769, 12779, 12777, 12790, 12803, 12808, 12803, 12806, 12783, 12759, 12741, 12724, 12710, 12704, 12692, 12675, 12656, 12615, 12550, 12495]
POP_PRJ=[12441, 12384, 12326, 12266, 12204, 12141, 12077, 12012, 11945, 11877, 11807, 11736, 11664, 11590, 11515, 11439, 11362, 11284, 11204, 11124, 11043, 10962, 10880, 10798, 10716, 10634, 10551, 10469]
CARE=[3.3, 4.2, 4.7, 5.2, 5.6, 5.9, 6.0, 6.4, 6.7, 7.1, 7.5, 7.9, 8.4, 8.8, 9.2, 9.5, 9.7, 10.1, 10.4, 10.7, 11.4, 11.2, 11.3]
# ====================== 8. 他社比較 ======================
def s_compare():
    sl=new_slide('実習の魅力','ほかの法人と比べて見える、エフビーの実習の魅力',notes='')
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
    text(sl,M,ty,CW,36,para('エフビーの実習ならではの、3つの魅力',27,INK,True,lh=1.3),name='魅力見出し')
    cy=ty+56; ch=B0-cy; cw=(CW-2*28)/3
    pts=[('成長産業の上場企業','その根本となる理念がある'),('ニーズに合わせたサービス展開','ご利用者さんに合わせた、実習経験の幅'),('ダイバーシティな環境','女性や技能実習生など、多様な人が活躍できる環境')]
    for i,(h,d) in enumerate(pts):
        x=M+i*(cw+28); card(sl,x,cy,cw,ch,name=f'カード_{h}')
        dot(sl,x+34+26,cy+ch/2,52,ORG if i==2 else TEAL2,'番号'); text(sl,x+34,cy+ch/2-26,52,52,para(str(i+1),26,'FFFFFF',True,lh=1.1),align='c',anchor='middle',name=f'番号{i+1}')
        text(sl,x+110,cy+12,cw-140,ch-24,[para(h,23,TEALD,True,after=2,lh=1.3),para(d,18,INK,lh=1.4)],anchor='middle',name=f'魅力_{i+1}')
    note(sl,'※ 他法人の記載は、公開情報をもとにした要約です。')
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
    note(sl,'※ 内容は検討中のものです。')
    return sl

# ====================== 10. プログラム ======================
def s_program():
    sl=new_slide('実習プログラム','1日で、5日間で。目的に合わせて選べる2つのプログラム',notes='')
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
    note(sl,'※ プログラムの内容・日程は調整中です。')
    return sl

# ====================== 11. 受け入れ体制 ======================
def s_system():
    sl=new_slide('実習の受け入れ体制','誰が担当しても伝わる、再現性の高い受け入れの仕組み',notes='')
    lw_=520; shape(sl,MSO_SHAPE.ROUNDED_RECTANGLE,M,T0,lw_,B0-T0,TEAL,None,rad=24,name='方針')
    text(sl,M+48,T0+48,lw_-96,B0-T0-96,[para('実習の運営体制',19,'EAF8F4',True,after=30,lh=1.3,spc=2),
        para('誰が担当しても、温かさとメッセージが伝わる。',38,'FFFFFF',True,after=36,lh=1.45),
        para('「再現性の高い仕組み」をつくります。学生向けの学習シートなどを用意し、プログラムを標準化します。',21,'F0FBF8',lh=1.7)],name='方針本文')
    items=[('メンター体制','現場スタッフを「実習メンター」として配置。学生1〜2名につき1名が、親身に伴走します。',TEAL2,TEALD),
     ('標準動画（ツール）','「ショート導入動画」などを活用。誰が説明しても、エフビーの温かさや社風がストレートに伝わります。',TEAL2,TEALD),
     ('実習生の声の資産化','リアルな体験談・本音の感想を、Web上に蓄積・公開。次年度の学生や学校（教授・就職課）にも届けます。',ORG,ORGD),
     ('年間PDCAの循環','受け入れと振り返りを定期的にくり返し、学校や地域とのつながりを広げていきます。',ORG,ORGD)]
    gx=M+lw_+32; gw=(W-M-gx-32)/2; gh=(B0-T0-32)/2
    for i,(h,d,c,dk) in enumerate(items):
        x=gx+(i%2)*(gw+32); y=T0+(i//2)*(gh+32)
        card(sl,x,y,gw,gh,name=f'カード_{h}')
        dot(sl,x+36+28,y+38+28,56,c,'番号'); text(sl,x+36,y+38,56,56,para(str(i+1),28,'FFFFFF',True,lh=1.1),align='c',anchor='middle',name=f'番号{i+1}')
        text(sl,x+116,y+38,gw-150,56,para(h,27,dk,True,lh=1.2),anchor='middle',name=f'見出し_{h}')
        text(sl,x+36,y+122,gw-72,gh-140,para(d,23,INK,lh=1.65),name=f'説明_{h}')
    note(sl,'出典：エフビー介護サービス。')
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
    note(sl,'※ 申込フォーム・SNS・問い合わせ先は準備中です。')
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

for f in (s_cover_mint,s_vision,s_agenda,s_ring,s_pop,s_market,s_why,s_philosophy,s_emotion,s_history,s_scale,s_sales,s_compare,s_learn,s_program,s_system,s_loop,s_flow): f()
N=len(prs.slides)
for k,sl in enumerate(prs.slides,1):
    if k==1: continue
    text(sl,W-M-120,B0+26,120,22,para(f'{k} / {N}',15,GRAY,lh=1.3),align='r',name='ページ番号')
prs.save('共育実習_図解.pptx'); print(N)
