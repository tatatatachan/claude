import math
cx,cy=865,522
Ro,Ri=282,200          # outer / inner radius of ring (before stroke rounding)
INK='#26323a'; SUB='#5b6b73'
def pt(a,rr):
    t=math.radians(a); return cx+rr*math.sin(t), cy-rr*math.cos(t)
# (start,end,color,dark,name,ring label,headline,desc lines)
segs=[
 (0,60,'#f28c3c','#c8651a','エフビー介護サービス','エフビー','営業の差になる',['志と実利で学校から選ばれ、','将来の担い手と出会えます。']),
 (60,120,'#f7ab67','#c8651a','社員','社員','学びと生きがいが育つ',['学生から学び、仕事の意味を再発見。','利用者の生きがいも育ちます。']),
 (120,180,'#2e9e8a','#1f7d6c','地域','地域','担い手とまちの未来',['地域を担う人が育ち、','介護の現場が身近になります。']),
 (180,240,'#54c5af','#1f7d6c','大学','大学','学部・学科の魅力向上',['魅力的な実習を提供。社会テーマ型','プログラム「STA」で連携します。']),
 (240,300,'#3fb39d','#1f7d6c','専門学校','専門学校','実習先の選択肢が広がる',['単位つきの実習先が増え、','介護の学びの入口が広がります。']),
 (300,360,'#86d6c4','#1f7d6c','高校','高校','探究と進路に生きる実績',['単位つきで受け入れやすく、探究テーマ','探しと面接で語れる実績になります。']),
]
GAP=2.6; ST=10
ro,ri=Ro-ST/2,Ri+ST/2
out=[]; cards=[]
for i,(a0,a1,col,dark,name,ring,head,desc) in enumerate(segs):
    s,e=a0+GAP,a1-GAP
    # extra angular inset so rounded stroke doesn't eat the gap
    so,eo=s+ (ST/2)/ro*57.3, e-(ST/2)/ro*57.3
    si,ei=s+ (ST/2)/ri*57.3, e-(ST/2)/ri*57.3
    P=lambda a,rr: "%.1f,%.1f"%pt(a,rr)
    d=f'M{P(so,ro)} A{ro},{ro} 0 0 1 {P(eo,ro)} L{P(ei,ri)} A{ri},{ri} 0 0 0 {P(si,ri)} Z'
    out.append(f'<path d="{d}" fill="{col}" stroke="{col}" stroke-width="{ST}" stroke-linejoin="round"/>')
    rm=(Ro+Ri)/2; mid=(a0+a1)/2
    if 90<mid<270: p0,p1,rr,fl=pt(e-3,rm-9),pt(s+3,rm-9),rm-9,0
    else: p0,p1,rr,fl=pt(s+3,rm+9),pt(e-3,rm+9),rm+9,1
    out.append(f'<path id="t{i}" d="M{p0[0]:.1f},{p0[1]:.1f} A{rr},{rr} 0 0 {fl} {p1[0]:.1f},{p1[1]:.1f}" fill="none"/>')
    fs=24 if len(ring)>=4 else 27
    out.append(f'<text font-size="{fs}" font-weight="700" letter-spacing="2" fill="#fff"><textPath href="#t{i}" startOffset="50%" text-anchor="middle">{ring}</textPath></text>')
    # card
    left=mid>180
    k=int(mid//60) if not left else int((mid-180)//60)
    off=[-236,0,236][k] if not left else [236,0,-236][k]
    ly=cy+off; CW,CH=480,170
    x=64 if left else 1730-64-CW
    y=ly-CH/2
    R=Ro+14
    dx=math.sqrt(R*R-off*off)
    ex=cx-dx if left else cx+dx
    cedge=x+CW if left else x
    out.append(f'<line x1="{cedge}" y1="{ly}" x2="{ex:.1f}" y2="{ly}" stroke="{col}" stroke-width="2.5"/>')
    out.append(f'<circle cx="{ex:.1f}" cy="{ly}" r="6" fill="{col}"/>')
    out.append(f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="22" fill="#fff"/></g>')
    out.append(f'<rect x="{x}" y="{y+28}" width="8" height="{CH-56}" rx="4" fill="{col}"/>')
    tx=x+36
    out.append(f'<text x="{tx}" y="{y+46}" font-size="21" font-weight="700" letter-spacing="1" fill="{SUB}">{name}</text>')
    out.append(f'<text x="{tx}" y="{y+86}" font-size="29" font-weight="800" fill="{dark}">{head}</text>')
    for j,l in enumerate(desc):
        out.append(f'<text x="{tx}" y="{y+121+j*28}" font-size="19" fill="{INK}">{l}</text>')
# cycle arrows in gaps
for a in range(0,360,60):
    out.append(f'<g transform="rotate({a} {cx} {cy})"><circle cx="{cx}" cy="{cy-(Ro+Ri)/2}" r="13" fill="#fff"/><path d="M{cx-4},{cy-(Ro+Ri)/2-6} L{cx+5},{cy-(Ro+Ri)/2} L{cx-4},{cy-(Ro+Ri)/2+6}" fill="none" stroke="#2e9e8a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1730" height="936" viewBox="0 0 1730 936" font-family="Hiragino Sans,Noto Sans JP,Noto Sans CJK JP,IPAPGothic,sans-serif">
<defs><filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#2e9e8a" flood-opacity="0.16"/></filter></defs>
<rect width="1730" height="936" fill="#e4f5e8"/>
<path d="M0,0H1730V132Q1300,172 865,132T0,152Z" fill="#54c5af"/>
<text x="64" y="50" font-size="20" font-weight="700" letter-spacing="4" fill="#d9f6ee">施策①　共育実習</text>
<text x="64" y="106" font-size="46" font-weight="800" fill="#fff">共育実習の共創モデル</text>
<circle cx="{cx}" cy="{cy}" r="178" fill="#fff" filter="url(#sh)"/>
<circle cx="{cx}" cy="{cy}" r="164" fill="none" stroke="#cfeee3" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round"/>
<text x="{cx}" y="{cy-50}" text-anchor="middle" font-size="23" font-weight="700" letter-spacing="2" fill="#2e9e8a">エフビー介護の</text>
<text x="{cx}" y="{cy+26}" text-anchor="middle" font-size="68" font-weight="800" fill="{INK}">共育実習</text>
<rect x="{cx-78}" y="{cy+52}" width="156" height="38" rx="19" fill="#f28c3c"/>
<text x="{cx}" y="{cy+79}" text-anchor="middle" font-size="21" font-weight="800" letter-spacing="3" fill="#fff">共に育つ</text>
{chr(10).join(out)}
<text x="865" y="893" text-anchor="middle" font-size="32" font-weight="800" fill="{INK}">学ぶ人も、迎える人も、地域も。みんなが共に育つ</text>
<rect x="440" y="908" width="850" height="4" rx="2" fill="#f28c3c"/>
</svg>'''
open('co-creation-model.svg','w').write(svg)
open('co-creation-model.html','w').write('<!doctype html><meta charset="utf-8"><title>共育実習 共創モデル</title><body style="margin:0;overflow:hidden">'+svg)
