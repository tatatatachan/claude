import math
import build_pptx as b   # slide 1 + helpers (b.sh is rebound to slide 2 below)
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt
from pptx.oxml.ns import qn
from lxml import etree
sl=b.prs.slides.add_slide(b.prs.slide_layouts[6]); b.sh=sh=sl.shapes
px,rect,text,fill,noline,shadow=b.px,b.rect,b.text,b.fill,b.noline,b.shadow
INK,SUB=b.INK,b.SUB
cx,cy,Ro,Ri=865,468,250,162

rect(0,0,1730,936,'E4F5E8').name='背景'
pts=[(0,0),(1730,0),(1730,132)]+[(1730*(1-i/240),132+10*i/240-20*math.sin(i/240*2*math.pi)) for i in range(241)]
fb=sh.build_freeform(px(pts[0][0]),px(pts[0][1])); fb.add_line_segments([(px(a),px(c)) for a,c in pts[1:]],close=True)
band=fb.convert_to_shape(); fill(band,'54C5AF'); noline(band); band.name='ヘッダー帯'
text(64,30,700,30,'施策　実習',20,'D9F6EE',True,spacing=4,name='小見出し')
text(64,60,1200,70,'どうブランドを育てていくか',46,'FFFFFF',True,name='タイトル')

steps=[ # color, dark, head, desc, x, y
 ('#3fb39d','1F7D6C','共育実習を行う',['高校・専門学校・大学で','共育実習を実施します。'],64,180),
 ('#86d6c4','1F7D6C','声が集まる',['学生・先生・社員・','利用者さんの声が集まります。'],1146,180),
 ('#f28c3c','C8651A','実習サイトに載せる',['プログラム内容と','口コミを掲載します。'],1146,516),
 ('#2e9e8a','1F7D6C','見て、動く',['学校は受け入れを判断し、','次の学生は参加を決めます。'],64,516),
]
CW,CH=520,170
def arrow(kind,x,y,w,h,col,name):
    a=sh.add_shape(kind,px(x),px(y),px(w),px(h)); fill(a,col); noline(a); a.name=name
    a.adjustments[0]=0.5; a.adjustments[1]=0.55; return a
arrow(MSO_SHAPE.RIGHT_ARROW,600,238,530,64,'#3fb39d','矢印_1から2')
arrow(MSO_SHAPE.DOWN_ARROW,1378,366,56,134,'#86d6c4','矢印_2から3')
arrow(MSO_SHAPE.LEFT_ARROW,600,574,530,64,'#f28c3c','矢印_3から4')
arrow(MSO_SHAPE.UP_ARROW,296,366,56,134,'#2e9e8a','矢印_4から1')
text(372,414,460,30,'次の共育実習につながる',21,'1F7D6C',True,name='循環ラベル')
for r_,col in ((112,'D3EEE4'),(86,'A9E0D0'),(60,'54C5AF')):
    o=sh.add_shape(MSO_SHAPE.OVAL,px(cx-r_),px(418-r_),px(2*r_),px(2*r_)); fill(o,col); noline(o); o.name='広がる輪'
text(cx-68,384,136,34,'実習',24,'FFFFFF',True,PP_ALIGN.CENTER,MSO_ANCHOR.MIDDLE,name='中央1')
text(cx-68,414,136,34,'ブランド',24,'FFFFFF',True,PP_ALIGN.CENTER,MSO_ANCHOR.MIDDLE,name='中央2')
pl=rect(cx-90,534,180,34,'F28C3C',MSO_SHAPE.ROUNDED_RECTANGLE,0.5); pl.name='帯'
text(cx-90,534,180,34,'回るほど育つ',19,'FFFFFF',True,PP_ALIGN.CENTER,MSO_ANCHOR.MIDDLE,name='帯文字')
for n,(col,dark,head,desc,x,y) in enumerate(steps,1):
    card=rect(x,y,CW,CH,'FFFFFF',MSO_SHAPE.ROUNDED_RECTANGLE,0.12); shadow(card); card.name=f'カード_{head}'
    rect(x,y+30,8,CH-60,col,MSO_SHAPE.ROUNDED_RECTANGLE,0.5).name='カード色バー'
    bd=sh.add_shape(MSO_SHAPE.OVAL,px(x+32),px(y+26),px(52),px(52)); fill(bd,col); noline(bd); bd.name='番号'
    text(x+32,y+26,52,52,str(n),28,'FFFFFF',True,PP_ALIGN.CENTER,MSO_ANCHOR.MIDDLE,name=f'番号文字{n}')
    text(x+102,y+30,400,44,head,32,dark,True,anchor=MSO_ANCHOR.MIDDLE,name=f'要点_{head}')
    text(x+36,y+96,470,60,desc,21,INK,ls=1.2,name=f'説明_{head}')

# bottom boxes
def box(x,w,title,lines,tc,bar,size,tcol):
    bx=rect(x,735,w,150,'FFFFFF',MSO_SHAPE.ROUNDED_RECTANGLE,0.1); shadow(bx); bx.name=f'ボックス_{title}'
    rect(x,761,8,98,bar,MSO_SHAPE.ROUNDED_RECTANGLE,0.5)
    text(x+34,754,w-60,34,title,26,tc,True,name=f'{title}_見出し')
    text(x+34,796,w-60,80,lines,size,tcol,ls=1.2,name=f'{title}_本文')
box(64,820,'サイトに載せるもの',['プログラム内容と口コミ。学校の先生が受け入れを判断でき、','学生が参加を決められる状態にする。'],INK,'F28C3C',21,INK)
box(910,756,'ほかの施策',['・関連大学・専門学校を増やす','・対応地域','・産官学で連携（次世代の育成を地域のみなさんで実施）'],SUB,'B8C4C0',19,SUB)

for el in sh._spTree.iter(qn('p:sp')):
    sp=el.find(qn('p:spPr'))
    if el.find(qn('p:style')) is not None and sp.find(qn('a:effectLst')) is None: etree.SubElement(sp,qn('a:effectLst'))
for er in sh._spTree.iter(qn('a:effectRef')): er.set('idx','0')
sl.notes_slide.notes_text_frame.text='実習ブランドが育つ循環：共育実習を行う→声が集まる→実習サイトに載せる→見て、動く→次の共育実習へ。'
b.prs.save('共育実習_図解.pptx')
