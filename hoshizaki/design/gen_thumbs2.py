import math,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from thumbs import *
from hzpeng import *
NAVY='#001F33'; CY='#00A9F4'
def snow(cx,cy,r,col):
    s=''
    for i in range(3):
        a=math.pi*i/3
        s+=f'<path d="M{cx-r*math.cos(a):.0f} {cy-r*math.sin(a):.0f} L{cx+r*math.cos(a):.0f} {cy+r*math.sin(a):.0f}" stroke="{col}" stroke-width="7" stroke-linecap="round"/>'
    return s
def vb(inner,label,w=1600,h=900): return f'<svg aria-label="{label}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">{HZ_DEFS}{inner}</svg>'
def poly(pts,fill): return '<path d="M'+' L'.join(f'{x} {y}' for x,y in pts)+f' Z" fill="{fill}"/>'
def tp(txt,x,y,size,fill,tr='',sp=0.0,sw=0):
    p,w=text_path(txt,x,y,size,fill,sw=sw,tr=tr,sp=sp); return p
def header(bg,fg,left,pill):
    pass
def header(bg,fg,left,pill):
    s=f'<rect x="0" y="0" width="1600" height="78" fill="{bg}"/><rect x="0" y="74" width="1600" height="5" fill="{fg}"/>'
    s+=hz_emblem(14,8,62)+tp(left,92,54,36,fg)
    s+=f'<path d="M740 12 H1400 Q1428 12 1428 40 Q1428 66 1400 66 H1060 L1030 76 L1036 66 H740 Q712 66 712 40 Q712 12 740 12 Z" fill="{bg}" stroke="{fg}" stroke-width="3"/>'
    s+=tp(pill,760,52,34,fg)
    return s
def sticker(cx,cy,r,l1,l2,fill=A,fg=NAVY,rot=-10):
    t1=text_width(l1,48); t2=text_width(l2,48)
    return (star(cx,cy,r,fill,n=14,ri=0.8,rot=0.2)+f'<g transform="rotate({rot} {cx} {cy})">'+tp(l1,cx-t1/2,cy-4,48,fg)+tp(l2,cx-t2/2,cy+52,48,fg)+'</g>')
def face(cx,cy,r,seed):
    s=blob(cx,cy,r,r*0.95,W,seed,stroke=NAVY,sw=12,jit=0.04,n=10)
    for dx in (-0.36,0.36):
        s+=f'<ellipse cx="{cx+dx*r:.0f}" cy="{cy-0.12*r:.0f}" rx="{r*0.25:.0f}" ry="{r*0.28:.0f}" fill="{W}" stroke="{NAVY}" stroke-width="8"/><circle cx="{cx+dx*r+ (6 if dx<0 else -6):.0f}" cy="{cy-0.08*r:.0f}" r="{r*0.12:.0f}" fill="{NAVY}"/>'
    s+=f'<path d="M{cx-r*0.2:.0f} {cy+r*0.12:.0f} L{cx+r*0.2:.0f} {cy+r*0.12:.0f} L{cx:.0f} {cy+r*0.55:.0f} Z" fill="{A}" stroke="{NAVY}" stroke-width="8" stroke-linejoin="round"/>'
    return s
def slits(x0,x1,ys,bg,h=16):
    return ''.join(f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="{h}" fill="{bg}"/>' for y in ys)

def loud2():
    s=f'<rect width="1600" height="900" fill="{CY}"/>'
    s+=poly([(0,420),(250,270),(250,500),(0,650)],NAVY)
    s+=poly([(1350,240),(1600,90),(1600,330),(1350,480)],NAVY)+poly([(1350,740),(1600,590),(1600,810),(1350,810)],NAVY)
    s+=header(W,NAVY,'ホシザキ　象徴IS','技術カードを持って、夏の街へ。')
    s+=tp('冷',290,640,600,NAVY)
    s+=slits(290,890,[400,520],CY,14)
    s+=hz_peng(1090,655,7.6)
    for (x,y,rr) in [(930,300,34),(1260,230,26),(1290,420,30)]:
        s+=snow(x,y,rr,W)
    # shout
    cx=1090
    sh=text_width('冷たっ！',110)
    s+=f'<g transform="rotate(-8 {cx} 150)">'+tp('冷たっ！',cx-sh/2-20,160,110,W)+'</g>'
    s+=tp('熱冷ませインターンシップ',50,760,100,NAVY)
    s+=f'<rect x="0" y="796" width="1600" height="104" fill="{NAVY}"/>'
    s+=tp('暑い街の、熱をどれだけ冷ませるか！？',50,862,56,W)
    s+=sticker(1450,600,150,'ウヒョー','！！')
    return vb(s,'象徴インターン サムネイル案 虎ノ門風')
def loud1():
    BG='#004767'
    s=f'<rect width="1600" height="900" fill="{BG}"/>'
    s+=poly([(0,470),(250,310),(250,540),(0,700)],S)+poly([(0,900),(130,900),(250,820),(250,640),(120,730)],S)
    s+=poly([(1380,760),(1600,640),(1600,900),(1380,900)],S)
    s+=header(W,NAVY,'ホシザキ　常設IS','6職種で、1台の新型製氷機を送り出す。')
    s+=tp('待',290,700,640,W)
    s+=slits(290,930,[430,560],BG,14)
    # speech bubbles
    for i,(txt,cx,cy,rot) in enumerate([('つくれる？',1140,230,-6),('間に合う？',1200,400,4),('買える？',1130,570,-4)]):
        w=text_width(txt,60)+60
        s+=f'<g transform="rotate({rot} {cx} {cy})"><path d="M{cx-w/2:.0f} {cy-55} H{cx+w/2:.0f} Q{cx+w/2+30:.0f} {cy-55} {cx+w/2+30:.0f} {cy-25} V{cy+25} Q{cx+w/2+30:.0f} {cy+55} {cx+w/2:.0f} {cy+55} H{cx-w/2+60:.0f} L{cx-w/2+20:.0f} {cy+95} L{cx-w/2+30:.0f} {cy+55} H{cx-w/2:.0f} Q{cx-w/2-30:.0f} {cy+55} {cx-w/2-30:.0f} {cy+25} V{cy-25} Q{cx-w/2-30:.0f} {cy-55} {cx-w/2:.0f} {cy-55} Z" fill="{W}" stroke="{NAVY}" stroke-width="6"/>'+tp(txt,cx-w/2+30-30+0,cy+20,60,BG)+'</g>'
    s+=tp('製氷機インターンシップ',60,790,96,W)
    s+=f'<rect x="0" y="816" width="1600" height="84" fill="{S}"/>'
    s+=tp('新製品リリース会議　3マンで、1台を出せ。',60,876,52,NAVY)
    s+=sticker(1450,700,140,'3マンで','出せ！')
    return vb(s,'常設インターン サムネイル案 虎ノ門風')
def calm1():
    t=thumbs.thumb1() if False else None
if __name__=='__main__':
    import thumbs as T
    out={'is1_loud':loud1(),'is2_loud':loud2(),'is1_bubble':T.thumb1().replace('width="1160" height="652" viewBox="0 0 1600 900" style="width:1160px;height:652px"','width="1600" height="900" viewBox="0 0 1600 900" xmlns="http://www.w3.org/2000/svg"'),'is2_bubble':T.thumb2().replace('width="1160" height="652" viewBox="0 0 1600 900" style="width:1160px;height:652px"','width="1600" height="900" viewBox="0 0 1600 900" xmlns="http://www.w3.org/2000/svg"')}
    d=os.path.dirname(os.path.abspath(__file__))
    for k,v in out.items():
        open(f'{d}/{k}.svg','w').write(v); open(f'{d}/{k}.html','w').write(f'<html><body style="margin:0">{v}</body></html>')
