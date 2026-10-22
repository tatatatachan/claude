import re,sys
sys.path.insert(0,'/tmp/claude-0/-home-user-claude/689257e3-17f4-5714-b5b4-463ef5bcf49a/scratchpad/ill')
from scenes import SC
base='/tmp/claude-0/-home-user-claude/689257e3-17f4-5714-b5b4-463ef5bcf49a/scratchpad/deck/project/slides/'
CARD='background:#ffffff;border-radius:8px;box-shadow:0 2px 10px rgba(0,71,103,0.10)'
chrome=open(base+'is1-roles.html').read().split('<h2')[0]
def mk(id_,page,h2,st,sub,body,foot,aside):
    ch=chrome.replace('id="is1-roles"',f'id="{id_}"'); ch=re.sub(r'(font-size:40px;color:#ffffff">)\d+',lambda m:m.group(1)+str(page),ch)
    return (ch+f'<h2 style="font-size:52px;font-weight:700;line-height:1.3;color:#0087C6">{h2}</h2>\n<div style="display:flex;flex-direction:column;align-items:center;gap:6px;padding-bottom:12px"><p style="font-size:44px;font-weight:700;line-height:1.35;color:#111111;text-align:center">{st}</p><p style="font-size:28px;line-height:1.6;text-align:center">{sub}</p></div>\n'+body+f'\n<p style="position:absolute;left:110px;top:1004px;width:1660px;text-align:right;font-size:24px;color:#3d4b5f">{foot}</p>\n<aside>{aside}</aside>\n</section>\n')
def table(head,rows,widths,fs=24):
    r=''
    for i,rw in enumerate(rows):
        bg=' style="background:#F4F7F9"' if i%2 else ''
        r+=f'<tr{bg}>'+''.join(f'<td>{"<b>"+c+"</b>" if j==0 else c}</td>' for j,c in enumerate(rw))+'</tr>\n'
    h=''.join(f'<th style="width:{w}%;color:#ffffff">{x}</th>' for x,w in zip(head,widths))
    return f'<div style="padding:12px 20px;{CARD}">\n<table style="font-size:{fs}px;line-height:1.35;color:#3d4b5f">\n<tr style="background:#004767">{h}</tr>\n{r}</table>\n</div>'
def row(*bs):
    if len(bs)==1 and isinstance(bs[0],list): bs=bs[0]
    return '<div style="display:flex;gap:16px;align-items:stretch">'+''.join(bs)+'</div>'
TY={'tech':('#C2E6FA','#004767','#ffffff'),'scene':('#E3F3FC','#00A0E9','#ffffff'),'need':('#F4F7F9','#0087C6','#ffffff')}
def card(kind,tag,badge,scene,title,desc):
    tint,chip,fg=TY[kind]
    bd=f'<p style="position:absolute;right:10px;top:8px;padding:0px 12px;background:#ffffff;border-radius:4px;font-family:\'Barlow\',sans-serif;font-size:24px;font-weight:700;color:#004767">{badge}</p>' if badge else ''
    return (f'<div style="flex:1;display:flex;flex-direction:column;{CARD}"><div style="position:relative;height:150px;background:{tint};border-radius:8px 8px 0 0;overflow:hidden">{SC[scene]()}<p style="position:absolute;left:10px;top:8px;padding:0px 12px;background:{chip};border-radius:4px;font-size:24px;font-weight:700;color:{fg}">{tag}</p>{bd}</div>'
    f'<div style="display:flex;flex-direction:column;gap:6px;padding:12px 16px 16px"><div style="width:36px;height:4px;background:{chip}"></div><p style="font-size:28px;font-weight:700;line-height:1.3;color:#004767">{title}</p><p style="font-size:24px;line-height:1.4;color:#3d4b5f">{desc}</p></div></div>')
def sub(f,pairs):
    t=open(base+f).read()
    for a_,b_ in pairs:
        if a_ not in t: print('MISS',f,a_[:30])
        t=t.replace(a_,b_)
    open(base+f,'w').write(t)
