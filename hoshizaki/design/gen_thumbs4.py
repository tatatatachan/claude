import math,random,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from thumbs3 import *
SKY='#7FD3FF'; INK='#0A2A4A'
def rect(x,y,w,h,f,st=None,sw=0): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{f}"'+(f' stroke="{st}" stroke-width="{sw}"' if st else '')+'/>'
def windows(x,y,w,h,cols,rows,col='#CFF1FF',sz=10):
    s=''
    for i in range(cols):
        for j in range(rows):
            s+=rect(round(x+(i+0.5)*w/cols-sz/2),round(y+(j+0.5)*h/rows-sz/2),sz,sz,col)
    return s
def central_towers(x,base):
    s=rect(x,base-330,90,330,INK)+rect(x+100,base-400,90,400,INK)+rect(x+90,base-250,10,250,INK)
    s+=windows(x,base-330,90,330,3,10)+windows(x+100,base-400,90,400,3,12)
    s+=f'<circle cx="{x+145}" cy="{base-350}" r="22" fill="#ffffff" stroke="{INK}" stroke-width="5"/><path d="M{x+145} {base-350} v-14 M{x+145} {base-350} l10 6" stroke="{INK}" stroke-width="4"/>'
    return s
def tv_tower(x,base):
    s=f'<path d="M{x-60} {base} L{x-12} {base-300} L{x+12} {base-300} L{x+60} {base} Z" fill="none" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>'
    for i in range(6):
        y=base-i*50; w=60-i*8.4
        s+=f'<path d="M{x-w:.0f} {y} L{x+w-8.4:.0f} {y-50} M{x+w:.0f} {y} L{x-w+8.4:.0f} {y-50}" stroke="{INK}" stroke-width="5"/>'
    s+=rect(x-34,base-190,68,26,INK)+rect(x-26,base-312,52,36,INK)+f'<path d="M{x} {base-312} V{base-372}" stroke="{INK}" stroke-width="8"/>'
    s+=f'<path d="M{x-20} {base-330} h40" stroke="#CFF1FF" stroke-width="5"/>'
    return s
def castle(x,base):
    s=f'<path d="M{x-150} {base} L{x-120} {base-70} L{x+120} {base-70} L{x+150} {base} Z" fill="{INK}"/>'
    levels=[(-100,-70,200,70),(-70,-140,140,70),(-44,-205,88,65)]
    for dx,dy,w,h in levels:
        s+=rect(x+dx,base+dy,w,h,'#ffffff',INK,6)+windows(x+dx,base+dy,w,h,max(2,w//40),1,INK,12)
        s+=f'<path d="M{x+dx-26} {base+dy+4} Q{x+dx+w/2:.0f} {base+dy-34} {x+dx+w+26} {base+dy+4} Z" fill="{INK}"/>'
    s+=f'<path d="M{x-12} {base-250} q-14 -34 6 -50 q6 14 4 22 q8 -8 14 -2 q6 22 -8 40 Z" fill="{A}" stroke="{INK}" stroke-width="3"/>'
    s+=f'<path d="M{x+12} {base-250} q14 -34 -6 -50 q-6 14 -4 22 q-8 -8 -14 -2 q-6 22 8 40 Z" fill="{A}" stroke="{INK}" stroke-width="3" transform="translate(0 0)"/>'
    return s
def oasis(x,base):
    s=f'<ellipse cx="{x}" cy="{base-150}" rx="190" ry="34" fill="#EAF8FF" stroke="{INK}" stroke-width="7"/><ellipse cx="{x}" cy="{base-160}" rx="150" ry="20" fill="#BFE9FB"/>'
    for dx in (-120,-60,0,60,120): s+=f'<path d="M{x+dx} {base-120} V{base}" stroke="{INK}" stroke-width="9"/>'
    s+=rect(x-150,base-70,300,70,INK)+windows(x-150,base-70,300,70,10,2,'#CFF1FF',12)
    return s
def blocks(base):
    s=''
    for x,w,h in [(0,70,140),(470,60,200),(560,80,160),(1190,60,210),(1280,90,150),(1400,70,230),(1500,90,170)]:
        s+=rect(x,base-h,w,h,INK)+windows(x,base-h,w,h,max(2,w//28),max(3,h//32),'#CFF1FF',9)
    return s
def march(cx,cy,sc,card=True,glass=False,flag=False,flip=False):
    s=hz_peng(cx,cy,sc*1.36)
    if card:
        s+=f'<g transform="translate({cx+30*sc:.0f} {cy-62*sc:.0f}) rotate(10)"><rect x="0" y="0" width="{44*sc:.0f}" height="{58*sc:.0f}" rx="6" fill="#ffffff" stroke="{NAVY}" stroke-width="5"/><rect x="6" y="6" width="{32*sc:.0f}" height="{24*sc:.0f}" fill="{ICE}"/><path d="M{10*sc:.0f} {40*sc:.0f} h{24*sc:.0f}" stroke="{ICE}" stroke-width="5"/></g>'
    if glass:
        s+=f'<circle cx="{cx-46*sc:.0f}" cy="{cy-48*sc:.0f}" r="{16*sc:.0f}" fill="{ICE}" fill-opacity="0.7" stroke="{NAVY}" stroke-width="5"/><path d="M{cx-35*sc:.0f} {cy-38*sc:.0f} l{-22*sc:.0f} {26*sc:.0f}" stroke="{NAVY}" stroke-width="7" stroke-linecap="round"/>'
    if flag:
        s+=f'<path d="M{cx-44*sc:.0f} {cy-40*sc:.0f} V{cy-150*sc:.0f}" stroke="{NAVY}" stroke-width="6"/><path d="M{cx-44*sc:.0f} {cy-150*sc:.0f} l{56*sc:.0f} {16*sc:.0f} l{-56*sc:.0f} {16*sc:.0f} Z" fill="{A}" stroke="{NAVY}" stroke-width="4"/>'
    return s
def parade():
    s=f'<rect width="1600" height="900" fill="{SKY}"/>'
    # clouds
    for x,y in [(300,150),(900,130),(1180,190)]: s+=f'<ellipse cx="{x}" cy="{y}" rx="90" ry="26" fill="#ffffff" fill-opacity="0.8"/><ellipse cx="{x+50}" cy="{y-18}" rx="60" ry="24" fill="#ffffff" fill-opacity="0.8"/>'
    # sun
    s+=sun_(1400,230)
    base=570
    s+=blocks(base)+central_towers(100,base)+tv_tower(420,base)+castle(760,base)+oasis(1090,base)
    # street
    s+=rect(0,base,1600,170,'#EAF8FF')+rect(0,base,1600,8,INK)
    for x in range(0,1600,160): s+=rect(x+20,base+120,90,10,'#BFE9FB')
    # penguins marching (right-facing)
    pos=[(230,722,1.45,True,False,True),(470,722,1.45,True,False,False),(710,722,1.45,False,True,False),(950,722,1.45,True,False,False),(1190,722,1.45,True,False,False)]
    for cx,cy,sc,card,glass,flag in pos:
        for k in (1,2,3): s+=f'<ellipse cx="{cx-70-k*34}" cy="{cy+6}" rx="14" ry="6" fill="#8FD3F3"/>'
        s+=march(cx,cy,sc,card,glass,flag)
    s+=header(W,NAVY,'ホシザキ　象徴IS','技術カードを持って、夏の名古屋へ。')
    s+=icicles(0,1600,79,40,30,70,'#EAF8FF','#5BB8E6',seed=3)
    s+=f'<g transform="rotate(-5 300 230)">'+tp('冷たっ！ウヒョー！',50,250,112,W)+'</g>'
    s+=f'<rect x="0" y="752" width="1600" height="148" fill="{INK}"/>'
    s+=tp('熱冷ませインターンシップ',50,850,100,W)
    s+=tp('暑い街の、熱をどれだけ冷ませるか！？',54,893,34,'#7FD3FF')
    s+=sticker(1430,600,120,'名古屋を','練り歩け！',rot=-8) if False else ''
    return vb(s,'象徴インターン サムネイル案 練り歩き')
def sun_(cx,cy):
    s=''
    for i in range(16):
        a=2*math.pi*i/16
        s+=f'<path d="M{cx+110*math.cos(a):.0f} {cy+110*math.sin(a):.0f} L{cx+160*math.cos(a):.0f} {cy+160*math.sin(a):.0f}" stroke="{A}" stroke-width="12" stroke-linecap="round"/>'
    s+=f'<circle cx="{cx}" cy="{cy}" r="95" fill="{A}" stroke="{NAVY}" stroke-width="8"/>'
    s+=f'<path d="M{cx-60} {cy-20} h120" stroke="{NAVY}" stroke-width="14" stroke-linecap="round"/><path d="M{cx-52} {cy-18} h44 v26 q0 8 -8 8 h-28 q-8 0 -8 -8 Z M{cx+8} {cy-18} h44 v26 q0 8 -8 8 h-28 q-8 0 -8 -8 Z" fill="{NAVY}"/>'
    s+=f'<path d="M{cx-34} {cy+46} q34 22 68 0" fill="none" stroke="{NAVY}" stroke-width="8" stroke-linecap="round"/>'
    return s
if __name__=='__main__':
    d=os.path.dirname(os.path.abspath(__file__))
    for k,v in {'is2_parade':parade(),'is2_ice_a':ice_a(),'is2_ice_b':ice_b()}.items():
        open(f'{d}/{k}.svg','w').write(v); open(f'{d}/{k}.html','w').write(f'<html><body style="margin:0">{v}</body></html>')
