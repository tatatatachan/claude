import sys,os,base64,math
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from thumbs5 import *
def cambodia(embed=True):
    b64=base64.b64encode(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cambodia_bg.jpg'),'rb').read()).decode()
    s=f'<rect width="1600" height="900" fill="#001F33"/><image href="data:image/jpeg;base64,{b64}" x="0" y="0" width="1600" height="900" preserveAspectRatio="xMidYMid slice"/>'
    s+='<rect width="1600" height="900" fill="#001F33" fill-opacity="0.18"/>'
    # heat shimmer
    for k,y in enumerate((210,250,290)):
        s+=f'<path d="M0 {y} Q100 {y-26} 200 {y} T400 {y} T600 {y} T800 {y} T1000 {y} T1200 {y} T1400 {y} T1600 {y}" fill="none" stroke="{A}" stroke-width="7" stroke-opacity="{0.9-k*0.2}" stroke-linecap="round"/>'
    s+=poly([(0,500),(230,360),(230,590),(0,730)],NAVY)+poly([(1380,300),(1600,170),(1600,420),(1380,550)],NAVY)
    s+=header(W,NAVY,'ホシザキ　本気の象徴IS','暑い国の、リアルな課題へ。')
    s+=icicles(0,1600,79,40,26,60,'#EAF8FF','#5BB8E6',seed=3)
    # giant hot glyph
    p,_=text_path('熱',70,640,640,A,sw=12,stroke=NAVY)
    s+=p
    s+=slits(70,730,[400,520],'#00000000',0) if False else ''
    # cold glyph small overlapping
    p2,_=text_path('冷',520,700,300,'#EAF8FF',sw=12,stroke=NAVY)
    s+=p2
    # official penguin
    s+=hz_peng(1190,740,7.2)
    s+=icecube(1260,560,34,'#F4FCFF','#BFE9FB','#8FD3F3',NAVY)
    s+=snow(1350,540,16,'#ffffff')
    # title + strip
    s+=f'<rect x="0" y="752" width="1600" height="148" fill="{NAVY}"/>'
    s+=tp('熱冷ませインターンシップ　本気編',44,846,84,W)
    s+=tp('カンボジアの街の、熱をどれだけ冷ませるか！？',50,890,38,'#7FD3FF')
    s+=sticker(1450,430,120,'リアルな','課題へ！',rot=-8)
    return vb(s,'本気の象徴IS カンボジア サムネイル案')
if __name__=='__main__':
    d=os.path.dirname(os.path.abspath(__file__))
    v=cambodia(); open(f'{d}/is3_cambodia.svg','w').write(v); open(f'{d}/is3_cambodia.html','w').write(f'<html><body style="margin:0">{v}</body></html>')
