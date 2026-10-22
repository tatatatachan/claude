import math
cx,cy,r=865,505,240
def pt(a,rr=r):
    t=math.radians(a); return cx+rr*math.sin(t), cy-rr*math.cos(t)
segs=[ # start,end(clockwise from top), color, name, en, desc lines, side
 (0,60,'#f28c3c','エフビー介護サービス','エフビー',['志と実利で営業の差になり、','将来の担い手と出会えます。']),
 (60,120,'#f6a45e','社員','社員',['学生から学び、仕事の意味を再発見。','利用者の生きがいも育ちます。']),
 (120,180,'#2e9e8a','地域','地域',['地域を担う人が育ち、','介護の現場が身近になります。']),
 (180,240,'#54c5af','大学','大学',['魅力的な実習を提供でき、','STAとして連携。学部・学科の魅力に。']),
 (240,300,'#3fb39d','専門学校','専門学校',['単位つきの実習先が増え、','介護の学びの入口が広がります。']),
 (300,360,'#7fd3c1','高校','高校',['単位つきで受け入れやすく、探究テーマと','面接で語れる実績が得られます。']),
]
cap=11.5; out=[]
for i,(a0,a1,col,name,en,desc) in enumerate(segs):
    s,e=a0+cap+1,a1-cap-1
    (x0,y0),(x1,y1)=pt(s),pt(e)
    out.append(f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}" stroke="{col}" stroke-width="100" stroke-linecap="round" fill="none"/>')
    mid=(a0+a1)/2
    # text path
    if 90<mid<270:
        (tx0,ty0),(tx1,ty1)=pt(e,r-6),pt(s,r-6); sw=0; rr=r-6
    else:
        (tx0,ty0),(tx1,ty1)=pt(s,r+6),pt(e,r+6); sw=1; rr=r+6
    out.append(f'<path id="t{i}" d="M{tx0:.1f},{ty0:.1f} A{rr},{rr} 0 0 {sw} {tx1:.1f},{ty1:.1f}" fill="none"/>')
    out.append(f'<text font-size="26" font-weight="800" letter-spacing="4" fill="#fff"><textPath href="#t{i}" startOffset="50%" text-anchor="middle">{en}</textPath></text>')
    # label
    ex,ey=pt(mid,r+58); left= mid>180
    lx=1215 if not left else 515
    ly=ey
    ty=ly-8
    anchor_x = lx
    tx= 1230 if not left else 56
    out.append(f'<path d="M{ex:.1f},{ey:.1f} L{lx},{ey:.1f}" stroke="{col}" stroke-width="2.5" stroke-dasharray="2 6" stroke-linecap="round"/>')
    out.append(f'<text x="{tx}" y="{ly-4:.0f}" font-size="34" font-weight="800" fill="#2b2b3a">{name}</text>')
    for j,l in enumerate(desc):
        out.append(f'<text x="{tx}" y="{ly+34+j*30:.0f}" font-size="21" fill="#2b2b3a">{l}</text>')
    out.append(f'<rect x="{tx}" y="{ly-56:.0f}" width="54" height="8" rx="4" fill="{col}"/>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1730" height="936" viewBox="0 0 1730 936" font-family="Hiragino Sans,Noto Sans JP,IPAPGothic,sans-serif">
<rect width="1730" height="936" fill="#dcf1e1"/>
<path d="M0,0H1730V150Q1300,190 865,150T0,170Z" fill="#54c5af"/>
<text x="58" y="62" font-size="20" font-weight="800" letter-spacing="6" fill="#fff">施策① KYOIKU JISSHU</text>
<text x="58" y="128" font-size="56" font-weight="800" fill="#fff">共育実習の共創モデル</text>
<circle cx="{cx}" cy="{cy}" r="150" fill="#fff"/>
<text x="{cx}" y="{cy-52}" text-anchor="middle" font-size="20" font-weight="700" fill="#2e9e8a">エフビー介護の</text>
<text x="{cx}" y="{cy+22}" text-anchor="middle" font-size="70" font-weight="800" fill="#2b2b3a">共育実習</text>
<rect x="{cx-70}" y="{cy+44}" width="140" height="32" rx="16" fill="#f28c3c"/>
<text x="{cx}" y="{cy+67}" text-anchor="middle" font-size="19" font-weight="800" letter-spacing="2" fill="#fff">共に育つ</text>
{chr(10).join(out)}
<text x="865" y="890" text-anchor="middle" font-size="38" font-weight="800" fill="#2b2b3a">学ぶ人も、迎える人も、地域も。みんなが共に育つ</text>
<rect x="330" y="908" width="1070" height="5" rx="3" fill="#f28c3c"/>
</svg>'''
open('co-creation-model.svg','w').write(svg)
open('co-creation-model.html','w').write('<!doctype html><meta charset="utf-8"><title>共育実習 共創モデル</title><body style="margin:0;overflow:hidden">'+svg)
