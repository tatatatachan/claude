import math
D='#004767';B='#0087C6';S='#00A0E9';I='#C2E6FA';W='#ffffff';A='#F59E0B';G='#64748b';T='#E3F3FC'
def st(w=3): return f'stroke="{D}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'
def svg(inner,bg):
    return (f'<svg aria-label="カードの絵（仮）" width="319" height="150" viewBox="0 0 320 150" style="position:absolute;left:0px;top:0px;width:319px;height:150px">'
            f'<rect x="0" y="0" width="320" height="150" fill="{bg}"/>{inner}</svg>')
def rays(cx,cy,n=14,col=W,op=0.55,r=260):
    s=''
    for i in range(n):
        a0=2*math.pi*i/n; a1=a0+math.pi/n
        s+=f'<path d="M{cx} {cy} L{cx+r*math.cos(a0):.0f} {cy+r*math.sin(a0):.0f} L{cx+r*math.cos(a1):.0f} {cy+r*math.sin(a1):.0f} Z" fill="{col}" fill-opacity="{op}"/>'
    return s
def ground(y=122,col=I):
    s=f'<rect x="0" y="{y}" width="320" height="{150-y}" fill="{col}"/>'
    for x in range(-20,340,14): s+=f'<path d="M{x} 150 L{x+12} {y+4}" stroke="{D}" stroke-opacity="0.25" stroke-width="2"/>'
    s+=f'<path d="M0 {y} L320 {y}" {st(3)}/>'
    return s
def peng(cx,cy,sc=1,extra='',flip=False,arm=''):
    f=f'translate({cx} {cy}) scale({-sc if flip else sc} {sc})'
    return (f'<g transform="{f}">'
      f'<ellipse cx="-11" cy="0" rx="11" ry="4.5" fill="{A}" {st(2)}/><ellipse cx="11" cy="0" rx="11" ry="4.5" fill="{A}" {st(2)}/>'
      f'<ellipse cx="0" cy="-40" rx="25" ry="38" fill="{D}" {st(3)}/><ellipse cx="0" cy="-32" rx="16" ry="27" fill="{W}"/>'
      +(arm or f'<path d="M-24 -48 Q-40 -30 -30 -14 L-21 -32 Z" fill="{D}" {st(2.5)}/>')+
      f'<path d="M24 -48 Q40 -30 30 -14 L21 -32 Z" fill="{D}" {st(2.5)}/>'
      f'<circle cx="-9" cy="-58" r="6" fill="{W}"/><circle cx="9" cy="-58" r="6" fill="{W}"/><circle cx="-8" cy="-58" r="2.6" fill="{D}"/><circle cx="8" cy="-58" r="2.6" fill="{D}"/>'
      f'<path d="M-7 -50 L7 -50 L0 -40 Z" fill="{A}" {st(2)}/>'+extra+'</g>')
def hardhat(): return f'<path d="M-20 -66 Q0 -92 20 -66 Z" fill="{A}" {st(2.5)}/><rect x="-24" y="-67" width="48" height="6" rx="3" fill="{A}" {st(2.5)}/><path d="M0 -84 L0 -68" {st(2.5)}/>'
def cape(c=S): return f'<path d="M-22 -62 L-40 -6 L40 -6 L22 -62 Z" fill="{c}" fill-opacity="0.9" {st(2.5)}/>'
def cube(x,y,s=26,col=I):
    return (f'<path d="M{x} {y} L{x+s} {y-s*0.45:.0f} L{x+2*s} {y} L{x+s} {y+s*0.45:.0f} Z" fill="{W}" {st(2.5)}/>'
            f'<path d="M{x} {y} L{x+s} {y+s*0.45:.0f} L{x+s} {y+s*1.45:.0f} L{x} {y+s} Z" fill="{col}" {st(2.5)}/>'
            f'<path d="M{x+2*s} {y} L{x+s} {y+s*0.45:.0f} L{x+s} {y+s*1.45:.0f} L{x+2*s} {y+s} Z" fill="{S}" fill-opacity="0.5" {st(2.5)}/>')
def icemaker(x,y,w=70,h=80,door=True):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{W}" {st(3)}/><rect x="{x+6}" y="{y+8}" width="{w-12}" height="{h*0.4:.0f}" rx="4" fill="{I}" {st(2.5)}/>'
    s+=f'<rect x="{x+6}" y="{y+h*0.55:.0f}" width="{w-12}" height="{h*0.36:.0f}" rx="4" fill="{T}" {st(2.5)}/>'
    s+=f'<circle cx="{x+w-14}" cy="{y+h*0.45:.0f}" r="3" fill="{A}"/>'
    return s
def gear(cx,cy,r,col=S):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{D}" stroke-width="{r*0.5:.0f}" stroke-dasharray="{r*0.45:.1f} {r*0.45:.1f}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.78:.0f}" fill="{col}" {st(3)}/><circle cx="{cx}" cy="{cy}" r="{r*0.28:.0f}" fill="{W}" {st(2.5)}/>')
def arrow_up(x,y,h=60,col=A,w=26):
    return f'<path d="M{x} {y} L{x+w} {y+w} L{x+w*0.35:.0f} {y+w} L{x+w*0.35:.0f} {y+h} L{x-w*0.35:.0f} {y+h} L{x-w*0.35:.0f} {y+w} L{x-w} {y+w} Z" fill="{col}" {st(3)}/>'
def arrow_down(x,y,h=60,col=A,w=26):
    return f'<path d="M{x} {y+h} L{x+w} {y+h-w} L{x+w*0.35:.0f} {y+h-w} L{x+w*0.35:.0f} {y} L{x-w*0.35:.0f} {y} L{x-w*0.35:.0f} {y+h-w} L{x-w} {y+h-w} Z" fill="{col}" {st(3)}/>'
def coin(cx,cy,r=16):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{A}" {st(3)}/><circle cx="{cx}" cy="{cy}" r="{r*0.72:.0f}" fill="none" stroke="{D}" stroke-width="2"/>'
            f'<path d="M{cx-r*0.3:.0f} {cy-r*0.4:.0f} L{cx} {cy} L{cx+r*0.3:.0f} {cy-r*0.4:.0f} M{cx} {cy} L{cx} {cy+r*0.45:.0f} M{cx-r*0.3:.0f} {cy+r*0.05:.0f} L{cx+r*0.3:.0f} {cy+r*0.05:.0f}" fill="none" {st(2.5)}/>')
def sun(cx,cy,r=22,rays_n=12):
    s=''
    for i in range(rays_n):
        a=2*math.pi*i/rays_n
        s+=f'<path d="M{cx+(r+5)*math.cos(a):.0f} {cy+(r+5)*math.sin(a):.0f} L{cx+(r+16)*math.cos(a):.0f} {cy+(r+16)*math.sin(a):.0f}" stroke="{A}" stroke-width="4" stroke-linecap="round"/>'
    return s+f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{A}" {st(3)}/>'
def palm(x,y):
    s=f'<path d="M{x} {y} Q{x+8} {y-30} {x+4} {y-58}" fill="none" stroke="{D}" stroke-width="7" stroke-linecap="round"/>'
    for dx,dy in [(-34,10),(-26,-12),(30,-12),(36,8),(2,-24)]:
        s+=f'<path d="M{x+4} {y-58} Q{x+4+dx*0.5:.0f} {y-58+dy-18} {x+4+dx} {y-58+dy}" fill="none" stroke="{B}" stroke-width="9" stroke-linecap="round"/>'
    return s
def wave(y,col=S):
    return f'<path d="M0 {y} Q20 {y-8} 40 {y} T80 {y} T120 {y} T160 {y} T200 {y} T240 {y} T280 {y} T320 {y} L320 150 L0 150 Z" fill="{col}" {st(3)}/>'
def snow(cx,cy,r=14,col=D):
    s=''
    for i in range(3):
        a=math.pi*i/3
        s+=f'<path d="M{cx-r*math.cos(a):.0f} {cy-r*math.sin(a):.0f} L{cx+r*math.cos(a):.0f} {cy+r*math.sin(a):.0f}" stroke="{col}" stroke-width="3" stroke-linecap="round"/>'
    return s
def bubble(x,y,w,h,inner='',tail='l'):
    t=f'<path d="M{x+16} {y+h-2} L{x+6} {y+h+14} L{x+30} {y+h-2}" fill="{W}" {st(3)}/>' if tail=='l' else f'<path d="M{x+w-16} {y+h-2} L{x+w-6} {y+h+14} L{x+w-30} {y+h-2}" fill="{W}" {st(3)}/>'
    return t+f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{W}" {st(3)}/>'+f'<rect x="{x+3}" y="{y+h-6}" width="{w-6}" height="8" fill="{W}"/>'+inner

def star(cx,cy,r,fill,n=5,ri=0.5):
    d=''
    for i in range(n*2):
        rr=r if i%2==0 else r*ri; a=math.pi*i/n-math.pi/2
        d+=('M' if i==0 else 'L')+f'{cx+rr*math.cos(a):.1f} {cy+rr*math.sin(a):.1f} '
    return f'<path d="{d}Z" fill="{fill}" {st(2.5)}/>'

SC={}
# ---------- IS1
def man1():
    x=rays(160,150,16,W,0.5)+ground(124)
    sheet=f'<rect x="206" y="26" width="86" height="82" rx="4" fill="{W}" {st(3)}/><path d="M216 44 H282 M216 56 H260" stroke="{B}" stroke-width="3" stroke-linecap="round"/><rect x="224" y="64" width="34" height="34" rx="3" fill="{I}" {st(2.5)}/><rect x="228" y="68" width="26" height="12" fill="{W}" stroke="{D}" stroke-width="2"/><circle cx="276" cy="86" r="8" fill="none" stroke="{D}" stroke-width="3"/>'
    compass=f'<path d="M-34 -20 L-34 -50" {st(3)}/><path d="M-44 -50 L-24 -50" {st(3)}/><path d="M-34 -50 L-44 -22 M-34 -50 L-24 -22" {st(3)}/>'
    return svg(x+sheet+peng(120,124,1.0,hardhat()+compass),'#C2E6FA')
def man2():
    x=rays(160,150,16,W,0.5)+ground(124)
    clip=f'<rect x="212" y="22" width="76" height="90" rx="6" fill="{W}" {st(3)}/><rect x="238" y="16" width="24" height="12" rx="4" fill="{A}" {st(2.5)}/>'
    for i,yy in enumerate([48,68,88]): clip+=f'<path d="M222 {yy} L228 {yy+6} L238 {yy-8}" fill="none" stroke="{B}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M246 {yy} H278" stroke="{I}" stroke-width="5" stroke-linecap="round"/>'
    lens=f'<circle cx="-42" cy="-26" r="14" fill="{I}" fill-opacity="0.7" {st(3.5)}/><path d="M-32 -16 L-24 -6" {st(5)}/>'
    cap=f'<path d="M-18 -66 Q0 -84 18 -66 Z" fill="{S}" {st(2.5)}/><rect x="-22" y="-67" width="44" height="5" rx="2.5" fill="{S}" {st(2.5)}/>'
    return svg(x+clip+peng(116,124,1.0,cap+lens),'#C2E6FA')
def man3():
    x=rays(160,150,16,W,0.5)+ground(124)
    box=f'<rect x="-20" y="-36" width="40" height="30" rx="3" fill="{I}" {st(3)}/><path d="M0 -36 V-6" stroke="{D}" stroke-width="3"/><rect x="-6" y="-30" width="12" height="8" fill="{A}"/>'
    coins=''.join(coin(250,118-i*12,13) for i in range(3))+coin(284,118,13)
    return svg(x+coins+f'<path d="M232 60 Q260 36 290 56" fill="none" stroke="{D}" stroke-width="3" stroke-dasharray="3 7" stroke-linecap="round"/>'+peng(124,124,1.0,f'<path d="M-22 -26 L-30 -4 Z" fill="{D}"/>'+box+f'<path d="M-24 -4 Q-34 -8 -24 -30" fill="none" stroke="{D}" stroke-width="2"/>'),'#C2E6FA')
def wait1():
    x=ground(124,'#E2EEF4')
    octo=f'<path d="M232 28 H262 L284 50 V80 L262 102 H232 L210 80 V50 Z" fill="{A}" {st(3.5)}/><rect x="222" y="58" width="52" height="14" rx="3" fill="{W}"/>'
    up=f'<path d="M-24 -48 Q-46 -66 -40 -92 L-30 -88 Q-32 -72 -20 -58 Z" fill="{D}" {st(2.5)}/>'
    return svg(x+octo+peng(130,124,1.0,'',arm=up),'#E2EEF4')
def policy1():
    x=ground(124,I)
    arrows=f'<path d="M110 52 Q160 14 210 52" fill="none" stroke="{A}" stroke-width="7" stroke-linecap="round"/><path d="M200 36 L212 54 L192 56 Z" fill="{A}"/><path d="M210 100 Q160 134 110 100" fill="none" stroke="{A}" stroke-width="7" stroke-linecap="round"/><path d="M120 116 L108 98 L128 96 Z" fill="{A}"/>'
    return svg(x+gear(100,76,34,S)+gear(222,76,34,B)+arrows,'#C2E6FA')
def inc1():
    x=ground(124,'#FDE9B8')
    mach=icemaker(76,34,92,90)
    crack=f'<path d="M118 56 L124 72 L114 80 L124 96" fill="none" stroke="{A}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    ng=f'<circle cx="236" cy="62" r="34" fill="{W}" {st(3.5)}/><path d="M220 46 L252 78 M252 46 L220 78" stroke="{A}" stroke-width="9" stroke-linecap="round"/>'
    return svg(x+mach+crack+cube(190,100,16)+ng,'#FEF3C7')
def inc2():
    x=ground(124,'#FDE9B8')
    part=gear(88,78,36,S)
    tag=f'<path d="M168 40 L252 40 Q262 40 262 50 L262 96 Q262 106 252 106 L168 106 L148 73 Z" fill="{W}" {st(3.5)}/><circle cx="170" cy="73" r="6" fill="#FEF3C7" {st(3)}/>'
    return svg(x+part+tag+coin(214,73,22)+arrow_up(284,46,56),'#FEF3C7')
def inc3():
    x=ground(124,'#FDE9B8')
    boxes=''.join(f'<rect x="{58+i*34}" y="{96-j*30}" width="30" height="28" rx="3" fill="{W}" {st(3)}/><path d="M{58+i*34} {104-j*30} H{88+i*34}" stroke="{D}" stroke-width="2"/>' for j in range(3) for i in range(4-j))
    bars=''.join(f'<rect x="{214+i*26}" y="{108-(i+1)*20}" width="20" height="{(i+1)*20}" fill="{S if i<3 else A}" {st(3)}/>' for i in range(4))
    return svg(x+boxes+bars,'#FEF3C7')
def wait2():
    x=ground(124,'#E2EEF4')
    octo=f'<path d="M60 28 H90 L112 50 V80 L90 102 H60 L38 80 V50 Z" fill="{A}" {st(3.5)}/><rect x="50" y="58" width="52" height="14" rx="3" fill="{W}"/>'
    up=f'<path d="M-24 -48 Q-46 -66 -40 -92 L-30 -88 Q-32 -72 -20 -58 Z" fill="{D}" {st(2.5)}/>'
    return svg(x+octo+peng(190,124,1.0,'',arm=up,flip=True),'#E2EEF4')
def policy2():
    x=ground(124,I)
    belt=f'<rect x="30" y="104" width="190" height="14" rx="7" fill="{W}" {st(3)}/><circle cx="42" cy="111" r="9" fill="{S}" {st(3)}/><circle cx="208" cy="111" r="9" fill="{S}" {st(3)}/>'
    bx=''.join(f'<rect x="{50+i*54}" y="70" width="40" height="34" rx="3" fill="{W}" {st(3)}/><path d="M{70+i*54} 70 V104" stroke="{D}" stroke-width="2.5"/>' for i in range(3))
    return svg(x+belt+bx+arrow_up(272,30,80,A,24),'#C2E6FA')
# ---------- IS2
def cA():
    x=sun(260,36,20)+wave(100,S)+f'<path d="M0 118 H320" {st(3)}/>'
    boat=f'<path d="M96 96 L190 96 L176 118 L110 118 Z" fill="{W}" {st(3)}/><path d="M142 94 V32 L186 88 Z" fill="{I}" {st(3)}/><path d="M142 94 V44 L108 88 Z" fill="{W}" {st(3)}/>'
    pier=f'<rect x="0" y="108" width="70" height="8" fill="{D}"/><path d="M12 116 V140 M40 116 V140 M64 116 V140" stroke="{D}" stroke-width="5"/>'
    return svg(x+palm(66,108)+boat+pier+f'<path d="M210 128 q10 -8 20 0 q-10 8 -20 0 Z M250 136 q10 -8 20 0 q-10 8 -20 0 Z" fill="{I}" {st(2.5)}/>','#C2E6FA')
def cB():
    x=sun(160,34,20)+f'<path d="M0 100 Q60 72 130 94 T250 86 T320 98 V150 H0 Z" fill="{I}" {st(3)}/>'+ground(116,'#E2EEF4')
    tree=f'<path d="M236 118 V70" stroke="{D}" stroke-width="7" stroke-linecap="round"/><ellipse cx="236" cy="62" rx="44" ry="14" fill="{B}" {st(3)}/><ellipse cx="250" cy="56" rx="26" ry="9" fill="{S}" {st(2.5)}/>'
    stall=f'<rect x="96" y="60" width="104" height="14" fill="{W}" {st(3)}/>'+''.join(f'<rect x="{96+i*26}" y="60" width="26" height="14" fill="{A if i%2==0 else W}" {st(2.5)}/>' for i in range(4))+f'<path d="M104 74 V118 M192 74 V118" {st(4)}/><rect x="110" y="98" width="76" height="20" rx="3" fill="{W}" {st(3)}/>'+''.join(f'<circle cx="{124+i*20}" cy="94" r="8" fill="{A}" {st(2.5)}/>' for i in range(3))
    return svg(x+tree+stall,'#C2E6FA')
def q():
    x=ground(124,I)
    qm=f'<path d="M-6 8 Q-6 -4 6 -4 Q18 -4 18 8 Q18 16 8 20 V26" fill="none" stroke="{B}" stroke-width="5" stroke-linecap="round"/><circle cx="8" cy="36" r="3.5" fill="{B}"/>'
    return svg(x+bubble(104,8,86,50,f'<g transform="translate(134 12)">{qm}</g>','l')+bubble(214,8,90,50,f'<circle cx="242" cy="33" r="5" fill="{D}"/><circle cx="260" cy="33" r="5" fill="{D}"/><circle cx="278" cy="33" r="5" fill="{D}"/>','r')+peng(76,124,0.7,'')+peng(244,124,0.7,'',flip=True),'#E3F3FC')
def need():
    x=ground(124,'#E2EEF4')
    card=f'<rect x="92" y="20" width="136" height="98" rx="8" fill="{W}" {st(3.5)}/>'+''.join(f'<path d="M108 {44+i*20} H212" stroke="{I}" stroke-width="4" stroke-linecap="round" stroke-dasharray="2 8"/>' for i in range(4))
    pencil=f'<path d="M200 112 L262 46 L274 58 L212 124 L196 128 Z" fill="{A}" {st(3)}/><path d="M262 46 L270 38 Q276 34 282 42 Q286 48 280 54 L274 58 Z" fill="{I}" {st(3)}/>'
    return svg(x+card+cube(40,100,14)+pencil,'#F4F7F9')
def crisis():
    x=sun(180,34,20)+ground(124,'#FDE9B8')
    crate=f'<g transform="rotate(-14 150 100)"><rect x="84" y="78" width="130" height="46" rx="4" fill="{W}" {st(3.5)}/><path d="M84 94 H214 M84 110 H214" stroke="{D}" stroke-width="2.5"/>'+''.join(f'<circle cx="{100+i*22}" cy="72" r="10" fill="{A}" {st(2.5)}/>' for i in range(4))+'</g>'
    fruit=''.join(f'<circle cx="{c}" cy="{y}" r="9" fill="{A}" {st(2.5)}/>' for c,y in [(236,116),(256,118),(276,112),(250,100),(268,92)])
    return svg(x+crate+fruit+arrow_down(292,20,46,A,12),'#FEF3C7')
def lim_power():
    x=ground(124,'#E2EEF4')
    pole=f'<path d="M80 124 V30" {st(5)}/><path d="M56 44 H104 M64 62 H96" {st(4)}/><path d="M104 44 Q140 70 190 54" fill="none" stroke="{D}" stroke-width="3" stroke-dasharray="5 6"/>'
    bulb=f'<circle cx="236" cy="58" r="30" fill="{W}" {st(3.5)}/><rect x="224" y="86" width="24" height="18" rx="4" fill="{G}" {st(3)}/><path d="M214 40 L258 76" stroke="{A}" stroke-width="8" stroke-linecap="round"/>'
    bolt=f'<path d="M168 40 L150 78 L166 78 L156 112 L186 68 L170 68 L182 40 Z" fill="{A}" {st(3)}/>'
    return svg(x+pole+bulb+bolt,'#E2EEF4')
def lim_water():
    x=ground(124,'#E2EEF4')
    crackp=f'<path d="M20 126 L60 138 L96 128 L130 142 M210 130 L250 140 L290 128" fill="none" stroke="{D}" stroke-width="3" stroke-linecap="round"/>'
    drop=f'<path d="M110 22 Q74 66 74 84 Q74 108 110 108 Q146 108 146 84 Q146 66 110 22 Z" fill="{S}" {st(3.5)}/><path d="M92 82 Q92 96 104 98" fill="none" stroke="{W}" stroke-width="5" stroke-linecap="round"/>'
    bucket=f'<path d="M186 54 H262 L252 118 H196 Z" fill="{W}" {st(3.5)}/><path d="M186 54 Q224 22 262 54" fill="none" stroke="{D}" stroke-width="3.5"/><path d="M200 70 H248" stroke="{I}" stroke-width="5" stroke-linecap="round"/>'
    return svg(x+crackp+drop+bucket,'#E2EEF4')
def lim_budget():
    x=ground(124,'#E2EEF4')
    purse=f'<path d="M84 70 Q84 40 120 40 H180 Q216 40 216 70 V100 Q216 118 198 118 H102 Q84 118 84 100 Z" fill="{W}" {st(3.5)}/><path d="M84 72 H216" {st(3)}/><circle cx="196" cy="94" r="8" fill="{A}" {st(3)}/>'
    return svg(x+purse+coin(256,100,15)+arrow_down(40,26,60,A,16),'#E2EEF4')
def tech_ref():
    x=ground(124,I)
    unit=icemaker(60,38,96,86)
    leaf=f'<path d="M206 108 Q196 50 262 40 Q274 100 206 108 Z" fill="{B}" {st(3.5)}/><path d="M206 108 Q226 82 252 56" fill="none" stroke="{W}" stroke-width="3.5" stroke-linecap="round"/>'
    return svg(x+unit+snow(108,64,14)+leaf+f'<circle cx="274" cy="36" r="10" fill="{I}" {st(3)}/>','#C2E6FA')
def tech_iot():
    x=ground(124,I)
    unit=icemaker(52,38,96,86)
    wifi=''.join(f'<path d="M{170+i*0} {70-i*0} " />' for i in range(0))
    arcs=''.join(f'<path d="M{150+r*0.2:.0f} {66-r*0.9:.0f} Q{150+r*1.2:.0f} 66 {150+r*0.2:.0f} {66+r*0.9:.0f}" fill="none" stroke="{D}" stroke-width="4" stroke-linecap="round"/>' for r in (14,28,42))
    phone=f'<rect x="228" y="26" width="56" height="96" rx="9" fill="{W}" {st(3.5)}/><rect x="236" y="38" width="40" height="64" rx="3" fill="{T}" {st(2.5)}/><path d="M240 92 L250 76 L258 84 L270 58" fill="none" stroke="{A}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(x+unit+arcs+phone,'#C2E6FA')
SC=dict(man1=man1,man2=man2,man3=man3,wait1=wait1,wait2=wait2,policy1=policy1,policy2=policy2,inc1=inc1,inc2=inc2,inc3=inc3,cA=cA,cB=cB,q=q,need=need,crisis=crisis,lim_power=lim_power,lim_water=lim_water,lim_budget=lim_budget,tech_ref=tech_ref,tech_iot=tech_iot)

# ---------- IS2 v2 (technology cards)
def t_ice():
    x=rays(160,150,16,W,0.5)+ground(124)
    unit=icemaker(70,30,100,94)
    cubes=cube(206,100,18)+cube(240,84,18)+cube(224,60,14)
    return svg(x+unit+snow(120,60,14)+cubes,'#C2E6FA')
def t_freeze():
    x=rays(160,150,16,W,0.5)+ground(124)
    fish=f'<path d="M96 76 Q130 40 170 76 Q130 112 96 76 Z" fill="{I}" {st(3.5)}/><path d="M170 76 L196 56 L196 96 Z" fill="{I}" {st(3.5)}/><circle cx="116" cy="70" r="4" fill="{D}"/>'
    dash=''.join(f'<path d="M{34+i*0} {50+i*20} H{70-i*6}" stroke="{D}" stroke-width="4" stroke-linecap="round"/>' for i in range(3))
    return svg(x+fish+snow(236,60,20)+snow(262,100,14)+dash,'#C2E6FA')
def t_micro():
    x=rays(160,150,16,W,0.5)+ground(124)
    box=f'<rect x="60" y="34" width="140" height="88" rx="8" fill="{W}" {st(3.5)}/><rect x="72" y="46" width="76" height="64" rx="4" fill="{I}" {st(3)}/><rect x="160" y="50" width="28" height="12" rx="3" fill="{T}" {st(2.5)}/><circle cx="174" cy="86" r="8" fill="{A}" {st(2.5)}/>'
    waves=''.join(f'<path d="M{84+i*18} 70 Q{92+i*18} 58 {100+i*18} 70 T{116+i*18} 70" fill="none" stroke="{B}" stroke-width="3.5" stroke-linecap="round"/>' for i in range(0,2))
    return svg(x+box+waves+cube(100,86,12)+f'<path d="M222 90 Q250 60 282 84" fill="none" stroke="{D}" stroke-width="3" stroke-dasharray="3 7" stroke-linecap="round"/>'+f'<path d="M232 108 q16 -22 36 0 z" fill="{A}" {st(3)}/>','#C2E6FA')
def t_electro():
    x=rays(160,150,16,W,0.5)+ground(124)
    drop=f'<path d="M96 24 Q64 62 64 80 Q64 106 96 106 Q128 106 128 80 Q128 62 96 24 Z" fill="{S}" {st(3.5)}/><path d="M78 80 Q78 94 90 96" fill="none" stroke="{W}" stroke-width="5" stroke-linecap="round"/>'
    spark=star(150,50,12,A,n=4,ri=0.3)+star(172,84,8,A,n=4,ri=0.3)
    veg=f'<path d="M222 122 V84" {st(4)}/><path d="M222 100 Q190 90 196 62 Q224 66 222 100 Z" fill="{B}" {st(3)}/><path d="M222 88 Q256 82 252 54 Q224 58 222 88 Z" fill="{S}" {st(3)}/><circle cx="266" cy="106" r="12" fill="{A}" {st(3)}/>'
    return svg(x+drop+spark+veg,'#C2E6FA')
def t_chill():
    x=rays(160,150,16,W,0.5)+ground(124)
    pot=f'<path d="M70 62 H190 V108 Q190 120 178 120 H82 Q70 120 70 108 Z" fill="{W}" {st(3.5)}/><path d="M58 62 H202" {st(4)}/><path d="M100 50 Q108 36 100 24 M130 50 Q138 36 130 24 M160 50 Q168 36 160 24" fill="none" stroke="{B}" stroke-width="3.5" stroke-linecap="round"/>'
    arrow=f'<path d="M214 40 V96" stroke="{D}" stroke-width="6" stroke-linecap="round"/><path d="M200 82 L214 100 L228 82" fill="none" stroke="{D}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(x+pot+arrow+snow(262,70,16)+snow(268,110,10),'#C2E6FA')
def s_hospital():
    x=sun(270,32,16)+ground(124,'#BFE5F7')
    bld=f'<rect x="40" y="36" width="130" height="88" fill="{W}" {st(3.5)}/>'+''.join(f'<rect x="{54+i*30}" y="{50+j*28}" width="18" height="16" fill="{I}" {st(2.5)}/>' for i in range(4) for j in range(2))+f'<rect x="92" y="96" width="26" height="28" fill="{S}" {st(3)}/><rect x="96" y="22" width="30" height="14" fill="{W}" {st(3)}/><path d="M111 24 V34 M106 29 H116" stroke="{B}" stroke-width="4"/>'
    tray=f'<rect x="196" y="82" width="96" height="34" rx="6" fill="{W}" {st(3.5)}/><circle cx="222" cy="98" r="11" fill="{I}" {st(3)}/><circle cx="260" cy="98" r="11" fill="{A}" {st(3)}/>'
    return svg(x+bld+tray,'#E3F3FC')
def s_stall():
    x=sun(60,36,20)+ground(124,'#FDE9B8')
    stall=f'<rect x="96" y="56" width="132" height="14" fill="{W}" {st(3)}/>'+''.join(f'<rect x="{96+i*33}" y="56" width="33" height="14" fill="{A if i%2==0 else W}" {st(2.5)}/>' for i in range(4))+f'<path d="M104 70 V122 M220 70 V122" {st(4)}/><rect x="112" y="98" width="100" height="24" rx="3" fill="{W}" {st(3)}/>'
    cup=f'<path d="M244 64 H282 L276 112 H250 Z" fill="{W}" {st(3.5)}/><path d="M248 82 H278 L276 112 H250 Z" fill="{I}"/>'+cube(252,72,8)+f'<path d="M270 64 L278 40" {st(3.5)}/>'
    return svg(x+stall+cup,'#FEF3C7')
SC.update(t_ice=t_ice,t_freeze=t_freeze,t_micro=t_micro,t_electro=t_electro,t_chill=t_chill,s_hospital=s_hospital,s_stall=s_stall)

# ---------- ice relay race scenes
def thermo(cx,cy,h=80,col=B):
    return (f'<rect x="{cx-9}" y="{cy-h}" width="18" height="{h}" rx="9" fill="{W}" {st(3.5)}/><circle cx="{cx}" cy="{cy+4}" r="17" fill="{col}" {st(3.5)}/>'
            f'<rect x="{cx-4}" y="{cy-h*0.55:.0f}" width="8" height="{h*0.55:.0f}" fill="{col}"/>'+''.join(f'<path d="M{cx+13} {cy-h+14+i*14} h10" stroke="{D}" stroke-width="3" stroke-linecap="round"/>' for i in range(4)))
def cust_rush():
    x=rays(160,150,16,W,0.5)+ground(124)
    clock=f'<circle cx="236" cy="62" r="40" fill="{W}" {st(4)}/><path d="M236 62 V36 M236 62 L256 74" {st(5)}/>'+''.join(f'<path d="M{236+34*math.cos(a):.0f} {62+34*math.sin(a):.0f} L{236+39*math.cos(a):.0f} {62+39*math.sin(a):.0f}" {st(3)}/>' for a in [i*math.pi/6 for i in range(12)])
    wings=f'<path d="M168 70 H208 M158 90 H198 M172 50 H204" stroke="{A}" stroke-width="7" stroke-linecap="round"/>'
    return svg(x+clock+wings+peng(80,124,0.95,''),'#C2E6FA')
def cust_cold():
    x=rays(160,150,16,W,0.5)+ground(124)
    th=thermo(120,100,84,S)+snow(190,50,18)+snow(228,86,12)+snow(262,48,10)
    cup=f'<path d="M206 70 H270 L262 118 H214 Z" fill="{W}" {st(3.5)}/><path d="M211 92 H266 L262 118 H214 Z" fill="{I}"/>'+cube(222,76,12)
    return svg(x+th+cup,'#C2E6FA')
def hap_sun():
    x=sun(240,44,24)+ground(124,'#FDE9B8')
    blk=cube(86,92,34)
    drip=''.join(f'<path d="M{110+i*30} 112 q-6 12 0 18 q6 -6 0 -18 z" fill="{S}" {st(2.5)}/>' for i in range(2))
    heat=''.join(f'<path d="M{160+i*26} 116 q10 -14 0 -28 q-10 -14 0 -28" fill="none" stroke="{A}" stroke-width="5" stroke-linecap="round"/>' for i in range(3))
    return svg(x+blk+drip+heat,'#FEF3C7')
def hap_step():
    x=ground(124,'#FDE9B8')
    steps=f'<path d="M140 124 V104 H180 V84 H220 V64 H260 V124 Z" fill="{W}" {st(3.5)}/>'
    box=f'<g transform="rotate(-16 100 96)"><rect x="64" y="70" width="72" height="50" rx="5" fill="{I}" {st(3.5)}/><path d="M64 88 H136" stroke="{D}" stroke-width="3"/></g>'
    return svg(x+steps+box+star(150,44,16,A,n=4,ri=0.3)+star(120,36,10,A,n=4,ri=0.3),'#FEF3C7')
def hap_crowd():
    x=ground(124,'#FDE9B8')
    pe=peng(70,124,0.55,'')+peng(124,124,0.55,'')+peng(178,124,0.55,'')+peng(232,124,0.55,'',flip=True)
    return svg(x+pe+bubble(180,8,100,44,f'<path d="M205 30 H255" stroke="{D}" stroke-width="5" stroke-linecap="round"/>','r')+'' ,'#FEF3C7')
def mat_box():
    x=rays(160,150,16,W,0.5)+ground(124)
    box=f'<rect x="70" y="52" width="150" height="72" rx="8" fill="{W}" {st(3.5)}/><rect x="62" y="40" width="166" height="20" rx="6" fill="{S}" {st(3.5)}/><path d="M130 40 V24 H160 V40" fill="none" stroke="{D}" stroke-width="5"/>'
    return svg(x+box+cube(104,84,16)+snow(250,60,16)+snow(268,100,10),'#C2E6FA')
def mat_foam():
    x=rays(160,150,16,W,0.5)+ground(124)
    panel=lambda px,py,w,h:f'<path d="M{px} {py} l16 -12 h{w} l-16 12 Z" fill="{W}" {st(3)}/><rect x="{px}" y="{py}" width="{w}" height="{h}" fill="{T}" {st(3)}/><path d="M{px+w} {py} l16 -12 v{h} l-16 12 Z" fill="{I}" {st(3)}/>'
    return svg(x+panel(60,60,120,50)+panel(190,40,60,70)+f'<path d="M72 80 h96 M72 92 h96" stroke="{I}" stroke-width="3"/>','#C2E6FA')
SC.update(cust_rush=cust_rush,cust_cold=cust_cold,hap_sun=hap_sun,hap_step=hap_step,hap_crowd=hap_crowd,mat_box=mat_box,mat_foam=mat_foam)
