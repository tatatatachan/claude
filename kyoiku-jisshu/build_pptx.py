import math, copy
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree
import gen  # reuses segs / constants

W=12192000; E=W/1730; H=int(E*936)
FONT='游ゴシック'
FS=lambda px: Pt(px*E/12700)
rgb=lambda h: RGBColor.from_string(h.lstrip('#').upper())
cx,cy,Ro,Ri=gen.cx,gen.cy,gen.Ro,gen.Ri
INK,SUB='26323A','5B6B73'

prs=Presentation(); prs.slide_width=W; prs.slide_height=H
sl=prs.slides.add_slide(prs.slide_layouts[6])
sh=sl.shapes
def px(v): return Emu(int(v*E))

def fill(s,c):
    s.fill.solid(); s.fill.fore_color.rgb=rgb(c)
def noline(s): s.line.fill.background()
def shadow(s,color='2E9E8A',alpha=16,blur=16,dist=6):
    sp=s._element.spPr
    eff=etree.SubElement(sp,qn('a:effectLst'))
    o=etree.SubElement(eff,qn('a:outerShdw'),blurRad=str(int(blur*E)),dist=str(int(dist*E)),dir='5400000',algn='t',rotWithShape='0')
    c=etree.SubElement(o,qn('a:srgbClr'),val=color); etree.SubElement(c,qn('a:alpha'),val=str(alpha*1000))
def text(x,y,w,h,lines,size,color,bold=False,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,spacing=None,rot=0,name=None,ls=None):
    tb=sh.add_textbox(px(x),px(y),px(w),px(h)); tf=tb.text_frame
    tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
    tf.word_wrap=True; tf.vertical_anchor=anchor
    if isinstance(lines,str): lines=[lines]
    for i,l in enumerate(lines):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align
        if ls: p.line_spacing=ls
        r=p.add_run(); r.text=l; f=r.font; f.size=FS(size); f.bold=bold; f.name=FONT; f.color.rgb=rgb(color)
        rPr=r._r.get_or_add_rPr()
        for tag in ('a:ea','a:cs'):
            el=etree.SubElement(rPr,qn(tag)); el.set('typeface',FONT)
        if spacing: rPr.set('spc',str(int(spacing*100)))
    tb.rotation=rot
    if name: tb.name=name
    return tb
def rect(x,y,w,h,c,shape=MSO_SHAPE.RECTANGLE,rad=None):
    s=sh.add_shape(shape,px(x),px(y),px(w),px(h)); fill(s,c); noline(s)
    if rad is not None: s.adjustments[0]=rad
    return s

# background + header band (wave as freeform)
rect(0,0,1730,936,'E4F5E8').name='背景'
pts=[(0,0),(1730,0),(1730,132)]
for i in range(0,241):
    t=i/240; xx=1730*(1-t)
    pts.append((xx,132+10*t-20*math.sin(t*2*math.pi)))
fb=sh.build_freeform(px(pts[0][0]),px(pts[0][1]))
fb.add_line_segments([(px(a),px(b)) for a,b in pts[1:]],close=True)
band=fb.convert_to_shape(); fill(band,'54C5AF'); noline(band); band.name='ヘッダー帯'
text(64,30,700,30,'施策①　共育実習',20,'D9F6EE',True,spacing=4,name='小見出し')
text(64,60,1200,70,'共育実習の共創モデル',46,'FFFFFF',True,name='タイトル')

# center circle
c=sh.add_shape(MSO_SHAPE.OVAL,px(cx-178),px(cy-178),px(356),px(356)); fill(c,'FFFFFF'); noline(c); shadow(c); c.name='中央円'
d=sh.add_shape(MSO_SHAPE.OVAL,px(cx-164),px(cy-164),px(328),px(328)); d.fill.background()
d.line.color.rgb=rgb('CFEEE3'); d.line.width=Pt(1.2); d.line.dash_style=3  # dash
text(cx-150,cy-78,300,30,'エフビー介護の',23,'2E9E8A',True,PP_ALIGN.CENTER,spacing=2,name='中央ミニ見出し')
text(cx-165,cy-52,330,100,'共育実習',68,INK,True,PP_ALIGN.CENTER,name='中央タイトル')
pill=rect(cx-78,cy+52,156,38,'F28C3C',MSO_SHAPE.ROUNDED_RECTANGLE,0.5); pill.name='共に育つ帯'
text(cx-78,cy+52,156,38,'共に育つ',21,'FFFFFF',True,PP_ALIGN.CENTER,MSO_ANCHOR.MIDDLE,spacing=3,name='共に育つ')

# ring sectors (block arcs)
GAP=2.6
thick=(Ro-Ri)/(2*Ro)*100000
for i,(a0,a1,col,dark,name,ring,head,desc) in enumerate(gen.segs):
    s_=sh.add_shape(MSO_SHAPE.BLOCK_ARC,px(cx-Ro),px(cy-Ro),px(2*Ro),px(2*Ro)); fill(s_,col); noline(s_)
    s_.name=f'環_{name}'
    av=s_._element.spPr.find(qn('a:prstGeom')).find(qn('a:avLst'))
    for g in list(av): av.remove(g)
    st=((a0+GAP-90)%360)*60000; en=((a1-GAP-90)%360)*60000
    for n,v in (('adj1',st),('adj2',en),('adj3',thick)):
        etree.SubElement(av,qn('a:gd'),name=n,fmla=f'val {int(v)}')
    mid=(a0+a1)/2; rm=(Ro+Ri)/2
    mx=cx+rm*math.sin(math.radians(mid)); my=cy-rm*math.cos(math.radians(mid))
    rot=mid if (mid<=90 or mid>=270) else mid-180
    fs=24 if len(ring)>=4 else 27
    bw=150
    text(mx-bw/2,my-18,bw,36,ring,fs,'FFFFFF',True,PP_ALIGN.CENTER,MSO_ANCHOR.MIDDLE,spacing=2,rot=rot,name=f'環ラベル_{name}')
# cycle chevrons in gaps
rm=(Ro+Ri)/2
for a in range(0,360,60):
    gx=cx+rm*math.sin(math.radians(a)); gy=cy-rm*math.cos(math.radians(a))
    o=sh.add_shape(MSO_SHAPE.OVAL,px(gx-13),px(gy-13),px(26),px(26)); fill(o,'FFFFFF'); noline(o); o.name='循環マーク白'
    t=math.radians(a); tx_,ty_=math.cos(t),math.sin(t)   # clockwise tangent (screen coords)
    nx_,ny_=-ty_,tx_
    tip=(gx+8*tx_,gy+8*ty_); b1=(gx-4*tx_+4*nx_,gy-4*ty_+4*ny_); b2=(gx-4*tx_-4*nx_,gy-4*ty_-4*ny_)
    fb=sh.build_freeform(px(tip[0]),px(tip[1])); fb.add_line_segments([(px(b1[0]),px(b1[1])),(px(b2[0]),px(b2[1]))],close=True)
    ch=fb.convert_to_shape(); fill(ch,'2E9E8A'); noline(ch); ch.name='循環マーク矢印'

# cards
CW,CH=480,170
for (a0,a1,col,dark,name,ring,head,desc) in gen.segs:
    mid=(a0+a1)/2; left=mid>180
    k=int(mid//60) if not left else int((mid-180)//60)
    off=[-236,0,236][k] if not left else [236,0,-236][k]
    ly=cy+off; x=64 if left else 1730-64-CW; y=ly-CH/2
    R=Ro+14; dx=math.sqrt(R*R-off*off); ex=cx-dx if left else cx+dx
    cedge=x+CW if left else x
    ln=sh.add_connector(MSO_CONNECTOR.STRAIGHT,px(cedge),px(ly),px(ex),px(ly)); ln.line.color.rgb=rgb(col); ln.line.width=Pt(1.8); ln.name=f'接続線_{name}'
    dot=sh.add_shape(MSO_SHAPE.OVAL,px(ex-6),px(ly-6),px(12),px(12)); fill(dot,col); noline(dot)
    card=rect(x,y,CW,CH,'FFFFFF',MSO_SHAPE.ROUNDED_RECTANGLE,0.13); shadow(card); card.name=f'カード_{name}'
    bar=rect(x,y+28,8,CH-56,col,MSO_SHAPE.ROUNDED_RECTANGLE,0.5); bar.name='カード色バー'
    tx=x+36
    text(tx,y+24,420,28,name,21,SUB,True,spacing=1,name=f'名称_{name}')
    text(tx,y+52,430,42,head,29,dark.lstrip('#'),True,name=f'要点_{name}')
    text(tx,y+100,430,60,desc,19,INK,ls=1.15,name=f'説明_{name}')

text(165,848,1400,56,'学ぶ人も、迎える人も、地域も。みんなが共に育つ',32,INK,True,PP_ALIGN.CENTER,MSO_ANCHOR.MIDDLE,name='キャッチコピー')
rect(440,908,850,4,'F28C3C',MSO_SHAPE.ROUNDED_RECTANGLE,0.5).name='下線'
for el in sh._spTree.iter(qn('p:sp')):
    sp=el.find(qn('p:spPr'))
    if el.find(qn('p:style')) is not None and sp.find(qn('a:effectLst')) is None:
        etree.SubElement(sp,qn('a:effectLst'))
for er in sh._spTree.iter(qn('a:effectRef')):
    er.set('idx','0')
sl.notes_slide.notes_text_frame.text='共育実習の共創モデル。学校（高校・専門学校・大学）とエフビー側（エフビー介護サービス・社員・地域）がそれぞれ得る価値を示す。'
prs.save('共育実習_共創モデル.pptx')
