import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from thumbs4 import *
YEL='#FFE24A'
def relay():
    s=f'<rect width="1600" height="900" fill="{YEL}"/>'
    s+=poly([(0,430),(250,280),(250,510),(0,660)],NAVY)+poly([(1350,300),(1600,150),(1600,390),(1350,540)],NAVY)
    s+=header(W,NAVY,'ホシザキ　常設IS','氷リレーレース　製氷機インターンシップ')
    s+=tp('氷',120,640,600,NAVY)
    s+=slits(120,720,[380,500],YEL,14)
    # ice baton glint on glyph
    s+=f'<g transform="translate(1480 190)">'+sun_(0,0).replace('r="95"','r="62"')+'</g>' if False else ''
    # heat shimmer lines
    for x in (770,1010,1250):
        s+=f'<path d="M{x} 640 q16 -24 0 -48 q-16 -24 0 -48" fill="none" stroke="{A}" stroke-width="8" stroke-linecap="round"/>'
    # speech bubble
    txt='ツメタクテハコベナイヨー'; w=text_width(txt,48)+70
    bx=760; by=140
    s+=f'<path d="M{bx} {by} H{bx+w:.0f} Q{bx+w+30:.0f} {by} {bx+w+30:.0f} {by+30} V{by+90} Q{bx+w+30:.0f} {by+120} {bx+w:.0f} {by+120} H{bx+170} L{bx+120} {by+176} L{bx+130} {by+120} H{bx} Q{bx-30} {by+120} {bx-30} {by+90} V{by+30} Q{bx-30} {by} {bx} {by} Z" fill="{W}" stroke="{NAVY}" stroke-width="7"/>'
    s+=tp(txt,bx+20,by+80,48,NAVY)
    for x in (820,1060,1300):
        for k,yy in enumerate((640,672,704)): s+=f'<path d="M{x-150-k*10} {yy} h{60+k*14}" stroke="{NAVY}" stroke-width="8" stroke-linecap="round"/>'
    # runners
    for i,(x,arm) in enumerate([(820,False),(1060,False),(1300,True)]):
        s+=hz_peng(x,722,3.3,rot=-7)
    # ice baton held up by last penguin
    s+=icecube(1186,505,30,'#F4FCFF','#BFE9FB','#8FD3F3',NAVY)
    s+=snow(1272,478,14,NAVY)
    s+=f'<rect x="0" y="728" width="1600" height="172" fill="{NAVY}"/>'
    s+=tp('暑い夏に、チームで、「冷」を届けろ。',50,832,88,W)
    s+=tp('氷リレーレース｜製氷機インターンシップ（常設IS）',54,882,38,'#7FD3FF')
    s+=sticker(1480,590,125,'3マンで','リレー！',rot=-8)
    return vb(s,'常設インターン サムネイル案 氷リレーレース')
if __name__=='__main__':
    d=os.path.dirname(os.path.abspath(__file__))
    v=relay(); open(f'{d}/is1_relay.svg','w').write(v); open(f'{d}/is1_relay.html','w').write(f'<html><body style="margin:0">{v}</body></html>')
