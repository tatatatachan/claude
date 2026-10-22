import math,random,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from thumbs2 import *
def flake(cx,cy,r,col,sw=7):
    s=''
    for i in range(6):
        a=math.pi*i/3
        x2,y2=cx+r*math.cos(a),cy+r*math.sin(a)
        s+=f'<path d="M{cx} {cy} L{x2:.0f} {y2:.0f}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>'
        for k in (0.55,):
            bx,by=cx+r*k*math.cos(a),cy+r*k*math.sin(a)
            for d in (-0.6,0.6):
                s+=f'<path d="M{bx:.0f} {by:.0f} L{bx+r*0.28*math.cos(a+d):.0f} {by+r*0.28*math.sin(a+d):.0f}" stroke="{col}" stroke-width="{sw*0.8:.1f}" stroke-linecap="round"/>'
    return s
def icicles(x0,x1,y,n,hmin,hmax,fill,edge,seed=1,sw=3):
    r=random.Random(seed); s=''; w=(x1-x0)/n
    for i in range(n):
        x=x0+i*w; h=r.uniform(hmin,hmax)
        s+=f'<path d="M{x:.0f} {y} L{x+w:.0f} {y} L{x+w*0.5+r.uniform(-6,6):.0f} {y+h:.0f} Z" fill="{fill}" stroke="{edge}" stroke-width="{sw}" stroke-linejoin="round"/>'
    return s
def icecube(x,y,s,top,left,right,edge,hl=True):
    d=f'<path d="M{x} {y} L{x+s} {y-s*0.5:.0f} L{x+2*s} {y} L{x+s} {y+s*0.5:.0f} Z" fill="{top}" stroke="{edge}" stroke-width="5" stroke-linejoin="round"/>'
    d+=f'<path d="M{x} {y} L{x+s} {y+s*0.5:.0f} L{x+s} {y+s*1.6:.0f} L{x} {y+s*1.1:.0f} Z" fill="{left}" stroke="{edge}" stroke-width="5" stroke-linejoin="round"/>'
    d+=f'<path d="M{x+2*s} {y} L{x+s} {y+s*0.5:.0f} L{x+s} {y+s*1.6:.0f} L{x+2*s} {y+s*1.1:.0f} Z" fill="{right}" stroke="{edge}" stroke-width="5" stroke-linejoin="round"/>'
    if hl: d+=f'<path d="M{x+s*0.25:.0f} {y+s*0.28:.0f} L{x+s*0.25:.0f} {y+s*0.85:.0f}" stroke="#ffffff" stroke-width="7" stroke-linecap="round" stroke-opacity="0.9"/><path d="M{x+s*0.7:.0f} {y-s*0.12:.0f} L{x+s*1.1:.0f} {y-s*0.3:.0f}" stroke="#ffffff" stroke-width="7" stroke-linecap="round" stroke-opacity="0.9"/>'
    return d
def facets(bg,col,seed):
    r=random.Random(seed); s=f'<rect width="1600" height="900" fill="{bg}"/>'
    for i in range(14):
        cx,cy=r.uniform(0,1600),r.uniform(80,820); k=r.uniform(120,320)
        pts=[(cx+k*math.cos(a+r.uniform(-.3,.3)),cy+k*0.7*math.sin(a+r.uniform(-.3,.3))) for a in (0,2.1,4.2)]
        s+=poly([(round(x),round(y)) for x,y in pts],col)
    return s
def icy(pal):
    bg,fac,stripe,glyph,title,strip,stripfg,cheek,edge=pal
    s=facets(bg,fac,7)
    s+=poly([(0,420),(250,270),(250,500),(0,650)],stripe)
    s+=poly([(1350,240),(1600,90),(1600,330),(1350,480)],stripe)+poly([(1350,740),(1600,590),(1600,810),(1350,810)],stripe)
    # ice cubes pile bottom right
    s+=icecube(1255,700,40,'#F4FCFF','#BFE9FB','#8FD3F3',edge)+icecube(1262,606,34,'#FFFFFF','#CFEFFF','#9ADBF6',edge)
    s+=header(W,NAVY,'ホシザキ　象徴IS','技術カードを持って、夏の街へ。')
    s+=icicles(0,1600,79,40,34,96,'#EAF8FF',edge,seed=3)
    s+=tp('冷',290,640,600,glyph)
    s+=slits(290,890,[400,520],bg,14)
    # glints on glyph
    for x,y,l in [(360,300,90),(470,250,60),(700,330,80),(790,470,60),(430,560,70)]:
        s+=f'<path d="M{x} {y} l{l*0.5:.0f} {-l*0.8:.0f}" stroke="#ffffff" stroke-width="9" stroke-linecap="round" stroke-opacity="0.85"/>'
    s+=icicles(330,850,636,9,22,44,'#F4FCFF',edge,seed=5,sw=4)
    # face
    cx,cy,r=1090,400,200
    s+=blob(cx,cy,r+16,r*0.95+16,'#EAF8FF',9,jit=0.04,n=10)
    s+=blob(cx,cy,r,r*0.95,W,5,stroke=NAVY,sw=12,jit=0.04,n=10)
    for dx in (-0.62,0.62): s+=f'<circle cx="{cx+dx*r:.0f}" cy="{cy+0.28*r:.0f}" r="{r*0.2:.0f}" fill="{cheek}"/>'
    for dx in (-0.36,0.36):
        s+=f'<ellipse cx="{cx+dx*r:.0f}" cy="{cy-0.18*r:.0f}" rx="{r*0.27:.0f}" ry="{r*0.32:.0f}" fill="{W}" stroke="{NAVY}" stroke-width="8"/><circle cx="{cx+dx*r:.0f}" cy="{cy-0.16*r:.0f}" r="{r*0.09:.0f}" fill="{NAVY}"/>'
    s+=f'<path d="M{cx-r*0.2:.0f} {cy+r*0.04:.0f} L{cx+r*0.2:.0f} {cy+r*0.04:.0f} L{cx:.0f} {cy+r*0.3:.0f} Z" fill="{A}" stroke="{NAVY}" stroke-width="8" stroke-linejoin="round"/>'
    s+=f'<ellipse cx="{cx}" cy="{cy+r*0.5:.0f}" rx="{r*0.2:.0f}" ry="{r*0.26:.0f}" fill="{NAVY}"/>'
    s+=icicles(cx-r*0.9,cx+r*0.9,cy-r*0.88,7,26,70,'#EAF8FF',edge,seed=11,sw=4)
    # breath puffs (shiver) + shiver lines
    for (x,y,rr) in [(cx+r*0.25,cy+r*1.0,30),(cx+r*0.5,cy+r*1.2,22)]:
        s+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr}" fill="{W}" stroke="{edge}" stroke-width="5"/>'
    for sx in (-1,1):
        for k in range(3):
            s+=f'<path d="M{cx+sx*(r+30+k*22):.0f} {cy-60+k*40:.0f} q{sx*14} 10 0 20 q{-sx*14} 10 0 20" fill="none" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/>'
    # flakes
    for (x,y,rr) in [(cx-r*1.3,cy-r*0.7,46),(cx+r*1.25,cy-r*0.95,34),(820,260,30)]:
        s+=flake(x,y,rr,W if bg!='#A9E4FF' else W)
    sh=text_width('冷たっ！',110)
    s+=f'<g transform="rotate(-8 {cx} 150)">'+tp('冷たっ！',cx-sh/2-20,160,110,W)+'</g>'
    s+=tp('熱冷ましインターンシップ',50,760,100,title)
    s+=f'<rect x="0" y="796" width="1600" height="104" fill="{strip}"/>'
    s+=tp('冷たい技術で、あらたな世の中の課題を解決せよ。',50,862,52,stripfg)
    s+=sticker(1470,470,140,'ウヒョー','！！')
    return s
PA=('#A9E4FF','#CFF1FF','#0A2A4A','#0A2A4A','#0A2A4A','#0A2A4A','#ffffff','#7FCFF5','#5BB8E6')
PB=('#0A2A4A','#123F66','#00A9F4','#EAF8FF','#EAF8FF','#00A9F4','#001F33','#2E8FC9','#7FD3FF')
def ice_a(): return vb(icy(PA),'象徴インターン サムネイル案 氷A')
def ice_b(): return vb(icy(PB),'象徴インターン サムネイル案 氷B')
if __name__=='__main__':
    d=os.path.dirname(os.path.abspath(__file__))
    for k,v in {'is2_ice_a':ice_a(),'is2_ice_b':ice_b()}.items():
        open(f'{d}/{k}.svg','w').write(v); open(f'{d}/{k}.html','w').write(f'<html><body style="margin:0">{v}</body></html>')
