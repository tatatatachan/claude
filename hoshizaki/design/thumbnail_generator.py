import math,random,re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
F=TTFont('/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'); GS=F.getGlyphSet(); CM=F.getBestCmap(); UPM=F['head'].unitsPerEm; HM=F['hmtx']
D='#004767';DD='#0B2A6F';B='#0087C6';S='#00A0E9';I='#C2E6FA';W='#ffffff';A='#F59E0B';ICE='#9ED9F0';T='#E3F3FC'
def glyph_d(ch,size,x,y):
    g=CM.get(ord(ch)); 
    if not g: return '',size*0.5
    pen=SVGPathPen(GS); sc=size/UPM
    GS[g].draw(TransformPen(pen,(sc,0,0,-sc,x,y)))
    return pen.getCommands(),HM[g][0]*sc
def text_path(txt,x,y,size,fill,sw=0,stroke=None,tr='',sp=0.0):
    d='';cx=x
    for ch in txt:
        p,adv=glyph_d(ch,size,cx,y); d+=p; cx+=adv+size*sp
    stk=f' stroke="{stroke or fill}" stroke-width="{sw}" stroke-linejoin="round"' if sw else ''
    return f'<path d="{d}" fill="{fill}"{stk}'+(f' transform="{tr}"' if tr else '')+'/>', cx-x
def text_width(txt,size,sp=0.0):
    w=0
    for ch in txt:
        g=CM.get(ord(ch)); w+=(HM[g][0]*size/UPM if g else size*0.5)+size*sp
    return w
def text_on_ellipse(txt,size,t0,cx,cy,rx,ry,gap,fill,sw=0,sp=0.1):
    out='';t=t0
    for ch in txt:
        g=CM.get(ord(ch)); adv=(HM[g][0]*size/UPM if g else size*0.5)
        # advance by arc length
        def pt(tt): return (cx+(rx+gap)*math.cos(tt), cy+(ry+gap)*math.sin(tt))
        # center of glyph: step half advance
        def step(tt,L):
            n=0
            while n<L:
                x1,y1=pt(tt); tt2=tt+0.002; x2,y2=pt(tt2); n+=math.hypot(x2-x1,y2-y1); tt=tt2
            return tt
        tm=step(t,adv/2); x,y=pt(tm)
        x2,y2=pt(tm+0.01); ang=math.degrees(math.atan2(y2-y,x2-x))
        p,_=glyph_d(ch,size,-adv/2,0)
        stk=f' stroke="{fill}" stroke-width="{sw}" stroke-linejoin="round"' if sw else ''
        out+=f'<path d="{p}" fill="{fill}"{stk} transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f})"/>'
        t=step(t,adv+size*sp)
    return out
def blob(cx,cy,rx,ry,fill,seed=1,tail=None,stroke=None,sw=0,op=1,n=9,jit=0.12):
    r=random.Random(seed); pts=[]
    for i in range(n):
        a=2*math.pi*i/n; k=1+r.uniform(-jit,jit)
        pts.append((cx+rx*k*math.cos(a),cy+ry*k*math.sin(a)))
    d=''
    for i in range(n):
        p0=pts[(i-1)%n];p1=pts[i];p2=pts[(i+1)%n];p3=pts[(i+2)%n]
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6);c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        if i==0: d+=f'M{p1[0]:.1f} {p1[1]:.1f}'
        d+=f' C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    s=''
    stk=f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ''
    if tail:
        tx,ty=tail; s+=f'<path d="M{cx+tx*0.55:.0f} {cy+ty*0.55-rx*0.1:.0f} L{cx+tx:.0f} {cy+ty:.0f} L{cx+tx*0.35:.0f} {cy+ty*0.75+rx*0.1:.0f} Z" fill="{fill}" fill-opacity="{op}"{stk}/>'
    return s+f'<path d="{d} Z" fill="{fill}" fill-opacity="{op}"{stk}/>'
def peng(cx,cy,sc=1,flip=False,arm_up=False):
    f=f'translate({cx} {cy}) scale({-sc if flip else sc} {sc})'
    st=f'stroke="{D}" stroke-width="3" stroke-linejoin="round"'
    return (f'<g transform="{f}"><ellipse cx="-11" cy="0" rx="11" ry="4.5" fill="{A}" {st}/><ellipse cx="11" cy="0" rx="11" ry="4.5" fill="{A}" {st}/>'
      f'<ellipse cx="0" cy="-40" rx="25" ry="38" fill="{D}" {st}/><ellipse cx="0" cy="-32" rx="16" ry="27" fill="{W}"/>'
      +(f'<path d="M-24 -48 Q-46 -66 -40 -92 L-30 -88 Q-32 -72 -20 -58 Z" fill="{D}" {st}/>' if arm_up else f'<path d="M-24 -48 Q-40 -30 -30 -14 L-21 -32 Z" fill="{D}" {st}/>')+
      f'<path d="M24 -48 Q40 -30 30 -14 L21 -32 Z" fill="{D}" {st}/><circle cx="-9" cy="-58" r="6" fill="{W}"/><circle cx="9" cy="-58" r="6" fill="{W}"/><circle cx="-8" cy="-58" r="2.6" fill="{D}"/><circle cx="8" cy="-58" r="2.6" fill="{D}"/><path d="M-7 -50 L7 -50 L0 -40 Z" fill="{A}" {st}/></g>')
def star(cx,cy,r,fill,stroke=None,sw=0,n=9,ri=0.55,rot=0):
    d=''
    for i in range(n*2):
        rr=r if i%2==0 else r*ri; a=math.pi*i/n+rot
        d+=('M' if i==0 else 'L')+f'{cx+rr*math.cos(a):.1f} {cy+rr*math.sin(a):.1f} '
    stk=f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ''
    return f'<path d="{d}Z" fill="{fill}"{stk}/>'
def wrap(inner,label):
    return f'<svg aria-label="{label}" width="1160" height="652" viewBox="0 0 1600 900" style="width:1160px;height:652px">{inner}</svg>'

def thumb1():
    s=f'<rect width="1600" height="900" fill="{W}"/>'
    sm=[(1480,400,70,52,D,4,(-30,60)),(60,560,60,44,S,3,(40,50)),(1330,60,70,44,S,8,None),(260,40,60,38,I,7,None),(1540,250,50,36,I,9,None),(1560,120,40,30,D,10,None)]
    for cx,cy,rx,ry,fill,sd,tl in sm: s+=blob(cx,cy,rx,ry,fill,sd,tl)
    s+=blob(800,400,620,310,I,21,(250,310),jit=0.05,n=11)
    # four speech bubbles with words
    for cx,cy,fill,txt,tcol,tail in [(170,340,S,'待った！',W,(-20,80)),(1440,180,I,'つくれる？',D,(20,80)),(1440,620,I,'間に合う？',D,(-20,80)),(160,640,S,'買える？',W,(30,70))]:
        s+=blob(cx,cy,130,72,fill,cy,tail)
        p,_=text_path(txt,0,0,52,tcol,sw=2.5); w=text_width(txt,52)
        s+=f'<g transform="translate({cx-w/2:.0f} {cy+18}) rotate(-6)">{p}</g>'
    t1,_=text_path('新製品',0,0,230,DD,sw=14)
    t2,_=text_path('リリース会議',0,0,140,DD,sw=10)
    s+=f'<g transform="translate(360 395) rotate(-6) skewX(-12)">{t1}</g>'
    s+=f'<g transform="translate(330 540) rotate(-6) skewX(-12)">{t2}</g>'
    l,_=text_path('常設インターン',0,0,70,DD,sw=5)
    s+=f'<g transform="translate(90 170) rotate(-8) skewX(-12)">{l}</g>'
    s+=star(1390,740,34,S,rot=0.3,n=5,ri=0.45)+star(1450,690,18,I,n=5,ri=0.45)
    s+=peng(1480,860,1.0,arm_up=True)
    a,_=text_path('設計マン／保証マン／届けマン　6職種を、3人1組で',60,780,44,DD,sw=1.5); s+=a
    b,_=text_path('2026年__月__日（__）　9:30–16:15　［会場］愛知本社',60,860,42,DD,sw=2); s+=b
    return wrap(s,'業務理解インターンのサムネイル（仮）')

def thumb2():
    s=f'<rect width="1600" height="900" fill="#EEF3F6"/>'
    cx,cy,rx,ry=930,500,480,290
    s+=blob(cx,cy,rx,ry,ICE,31,stroke=ICE,sw=3,op=0.55,jit=0.05,n=12)
    s+=blob(cx-10,cy-6,rx-26,ry-24,'#D8F0FA',32,op=0.85,jit=0.05,n=12)
    s+=blob(cx-90,cy-70,rx-190,ry-140,W,33,op=0.55,jit=0.06,n=10)
    s+=blob(cx+40,cy+90,rx-250,ry-210,ICE,34,op=0.25,jit=0.08,n=9)
    s+=f'<path d="M{cx-rx+60} {cy-30} Q{cx-rx+70} {cy-180} {cx-240} {cy-220}" fill="none" stroke="{W}" stroke-width="8" stroke-linecap="round" stroke-opacity="0.8"/>'
    for r in (36,68,100): s+=f'<ellipse cx="1130" cy="640" rx="{r*1.6:.0f}" ry="{r*0.5:.0f}" fill="none" stroke="{B}" stroke-width="4" stroke-opacity="0.45"/>'
    s+=f'<path d="M680 590 Q840 270 1120 600" fill="none" stroke="{D}" stroke-width="5" stroke-dasharray="4 16" stroke-linecap="round"/>'
    s+=peng(680,610,1.9)
    s+=f'<g transform="translate(940 360) rotate(24)">{peng(0,0,1.0,flip=True,arm_up=True)}</g>'
    s+=text_on_ellipse('冷ませ！',120,math.radians(190),cx,cy,rx,ry,34,D,sw=3,sp=0.06)
    s+=text_on_ellipse('FIRST PENGUIN',34,math.radians(258),cx,cy,rx,ry,30,B,sw=0,sp=0.22)
    s+=text_on_ellipse('世界の隅々まで。',78,math.radians(-56),cx,cy,rx,ry,52,D,sw=3,sp=0.05)
    for i,tx in enumerate(['暑くても、そこに飛び込む','ファーストペンギン','東南アジア・アフリカ','第1回　2026.__.__','7〜10名　年3回']):
        p,_=text_path(tx,60,610+i*58,42,D,sw=1.5); s+=p
    p,_=text_path('ホシザキ　象徴インターンシップ',60,70,44,B,sw=1.5); s+=p
    return wrap(s,'象徴インターンのサムネイル（仮）')
