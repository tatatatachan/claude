# -*- coding: utf-8 -*-
"""総人口グラフ(1947-2100)をPNGで書き出す。deck.pyと同じデータ。"""
import re, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Polygon
src=open('deck.py',encoding='utf-8').read()
ns={}
for name in ('POP_ACT','POP_PRJ2','UN_POP'):
    m=re.search(r'^'+name+r'=(.*)$',src,re.M); ns[name]=eval(m.group(1))
POP_ACT,POP_PRJ2,UN_POP=ns['POP_ACT'],ns['POP_PRJ2'],ns['UN_POP']
anc={2070:8700,**UN_POP}; ks=sorted(anc)
def itp(y):
    a=max(k for k in ks if k<=y); b=min(k for k in ks if k>=y)
    return anc[a] if a==b else anc[a]+(anc[b]-anc[a])*(y-a)/(b-a)
fm.fontManager.addfont('/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf')
plt.rcParams['font.family']='IPAGothic'
INK,SUB='#26323A','#5B6B73'; TEAL,ORG,ORGL='#3FB39D','#F28C3C','#F7C9A0'
ya=list(range(1947,2023)); yp=list(range(2023,2071)); yu=list(range(2071,2101))
fig,ax=plt.subplots(figsize=(17.3,8.2),dpi=150)
ax.bar(ya,POP_ACT,width=0.78,color=TEAL,label='実績')
ax.bar(yp,POP_PRJ2,width=0.78,color=ORG,label='推計（社人研）')
ax.bar(yu,[itp(y) for y in yu],width=0.78,color=ORGL,label='参考（国連推計。5年ごとの値を結んだ年次）')
ax.set_xlim(1945,2102); ax.set_ylim(0,18000)
ax.set_yticks(range(0,18001,3000)); ax.set_yticklabels([f'{v:,}' for v in range(0,18001,3000)],fontsize=15,color=SUB)
ax.set_xticks(range(1950,2101,10)); ax.tick_params(axis='x',labelsize=15,colors=SUB,length=0); ax.tick_params(axis='y',length=0)
ax.grid(axis='y',color='#E3EBE7',lw=1); ax.set_axisbelow(True)
for s in ('top','right','left'): ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color('#C9D6D1')
X0,X1,Y1=1945,2102,18000
fx=lambda x:(x-X0)/(X1-X0); fy=lambda y:y/Y1
AR=(0.925*17.3)/(0.80*8.2)
def bubble(x,y,w,h,tx,ty,col,small,big):
    # x,y,w,h は データ座標（左下基準）
    p=FancyBboxPatch((fx(x),fy(y)),w/(X1-X0),h/Y1,boxstyle='round,pad=0,rounding_size=0.012',mutation_aspect=AR,
                     fc=col,ec='none',transform=ax.transAxes,zorder=5); ax.add_patch(p)
    ax.add_patch(Polygon([(x+w*0.30,y+60),(x+w*0.62,y+60),(tx,ty)],fc=col,ec='none',zorder=4))
    ax.text(x+w*0.07,y+h*0.74,small,color='white',fontsize=17,va='center',zorder=6)
    ax.text(x+w*0.07,y+h*0.34,big,color='white',fontsize=29,va='center',zorder=6)
bubble(1970,14300,40,2900,2008,12950,'#3FB39D','2008年がピーク','1億2,808万人')
bubble(2022,12900,40,2900,2050,10650,ORG,'2050年','約1億469万人')
bubble(2064,9500,38,2900,2100,7650,'#E9A56B','2100年','約7,364万人')
fig.text(0.012,0.965,'総人口（万人）',fontsize=16,color=SUB)
ax.legend(loc='lower center',bbox_to_anchor=(0.5,-0.14),ncol=3,frameon=False,fontsize=15)
fig.subplots_adjust(left=0.06,right=0.985,top=0.93,bottom=0.17)
fig.savefig('総人口グラフ_1947-2100.png',facecolor='white')
