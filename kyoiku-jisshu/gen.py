import math
cx,cy,r,sw=865,520,262,96
INK='#26323a'
def pt(a,rr=r):
    t=math.radians(a); return cx+rr*math.sin(t), cy-rr*math.cos(t)
segs=[ # start,end(clockwise from top), color, name, ring label, desc lines
 (0,60,'#f28c3c','エフビー介護サービス','エフビー',['志と実利で営業の差になり、','将来の担い手と出会えます。']),
 (60,120,'#f6a45e','社員','社員',['学生から学び、仕事の意味を再発見。','利用者の生きがいも育ちます。']),
 (120,180,'#2e9e8a','地域','地域',['地域を担う人が育ち、','介護の現場が身近になります。']),
 (180,240,'#54c5af','大学','大学',['魅力的な実習で学部・学科の魅力が向上。','社会テーマ型プログラム「STA」で連携。']),
 (240,300,'#3fb39d','専門学校','専門',['単位つきの実習先が増え、','介護の学びの入口が広がります。']),
 (300,360,'#7fd3c1','高校','高校',['単位つきで受け入れやすく、探究テーマと','面接で語れる実績が得られます。']),
]
cap=(sw/2)/r*180/math.pi; out=[]
for i,(a0,a1,col,name,ring,desc) in enumerate(segs):
    s,e=a0+cap+1.2,a1-cap-1.2
    (x0,y0),(x1,y1)=pt(s),pt(e)
    out.append(f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" fill="none"/>')
    mid=(a0+a1)/2
    if 90<mid<270: (p0,p1),rr,flag=(pt(e,r-9),pt(s,r-9)),r-9,0
    else: (p0,p1),rr,flag=(pt(s,r+9),pt(e,r+9)),r+9,1
    out.append(f'<path id="t{i}" d="M{p0[0]:.1f},{p0[1]:.1f} A{rr},{rr} 0 0 {flag} {p1[0]:.1f},{p1[1]:.1f}" fill="none"/>')
    out.append(f'<text font-size="30" font-weight="700" letter-spacing="3" fill="#fff"><textPath href="#t{i}" startOffset="50%" text-anchor="middle">{ring}</textPath></text>')
    left=mid>180
    off=[-232,0,232][min(int(mid//60),5)%3] if not left else [232,0,-232][int((mid-180)//60)]
    ly=cy+off
    dx=math.sqrt(max((r+sw/2+10)**2-off**2,0))
    ex=cx-dx if left else cx+dx
    tx=56 if left else 1230
    lx=ex-0 ; endx=(tx+ (462 if left else 0)) if left else tx-14
    if left: endx=520
    out.append(f'<line x1="{ex:.1f}" y1="{ly}" x2="{endx}" y2="{ly}" stroke="{col}" stroke-width="3" stroke-dasharray="1 7" stroke-linecap="round"/>')
    out.append(f'<rect x="{tx}" y="{ly-62}" width="48" height="7" rx="3.5" fill="{col}"/>')
    out.append(f'<text x="{tx}" y="{ly-12}" font-size="36" font-weight="800" fill="{INK}">{name}</text>')
    for j,l in enumerate(desc):
        out.append(f'<text x="{tx}" y="{ly+26+j*33}" font-size="22" fill="#44525a">{l}</text>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1730" height="936" viewBox="0 0 1730 936" font-family="Hiragino Sans,Noto Sans JP,Noto Sans CJK JP,IPAPGothic,sans-serif">
<rect width="1730" height="936" fill="#dcf1e1"/>
<path d="M0,0H1730V140Q1300,180 865,140T0,160Z" fill="#54c5af"/>
<text x="58" y="58" font-size="22" font-weight="700" letter-spacing="3" fill="#fff">施策①　共育実習</text>
<text x="58" y="122" font-size="52" font-weight="800" fill="#fff">共育実習の共創モデル</text>
<circle cx="{cx}" cy="{cy}" r="172" fill="#fff"/>
<text x="{cx}" y="{cy-52}" text-anchor="middle" font-size="24" font-weight="700" fill="#2e9e8a">エフビー介護の</text>
<text x="{cx}" y="{cy+28}" text-anchor="middle" font-size="76" font-weight="800" fill="{INK}">共育実習</text>
<rect x="{cx-80}" y="{cy+58}" width="160" height="38" rx="19" fill="#f28c3c"/>
<text x="{cx}" y="{cy+85}" text-anchor="middle" font-size="22" font-weight="800" letter-spacing="3" fill="#fff">共に育つ</text>
{chr(10).join(out)}
<text x="865" y="890" text-anchor="middle" font-size="36" font-weight="800" fill="{INK}">学ぶ人も、迎える人も、地域も。みんなが共に育つ</text>
<rect x="400" y="906" width="930" height="5" rx="2.5" fill="#f28c3c"/>
</svg>'''
open('co-creation-model.svg','w').write(svg)
open('co-creation-model.html','w').write('<!doctype html><meta charset="utf-8"><title>共育実習 共創モデル</title><body style="margin:0;overflow:hidden">'+svg)
