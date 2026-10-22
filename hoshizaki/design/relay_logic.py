def clamp(x): return max(0.0,min(1.0,x))
P=dict(T_MIN=90,T_MAX=360,DT_MAX=6.0,R_LO=0.92,R_HI=0.99,L5_MAX=200,BUDGET=1000,C_FULL=400,C_ZERO=1000)
W={'標準':(30,30,30,10),'急ぎ':(50,20,20,10),'冷たさ命':(20,50,20,10),'品質重視':(20,20,50,10),'コスパ':(25,25,25,25)}
def score(T,dT,R,defects,L5,C,penalty=0,card='標準'):
    St=100*clamp((P['T_MAX']-T)/(P['T_MAX']-P['T_MIN']))
    Sc=100*clamp(1-dT/P['DT_MAX'])
    Qm=clamp((R-P['R_LO'])/(P['R_HI']-P['R_LO'])); Ql=clamp((5-defects)/5); Qh=clamp(1-L5/P['L5_MAX'])
    Sq=100*(0.5*Qm+0.2*Ql+0.3*Qh)
    Sd=100*clamp((P['C_ZERO']-C)/(P['C_ZERO']-P['C_FULL']))
    w=W[card]; tot=(w[0]*St+w[1]*Sc+w[2]*Sq+w[3]*Sd)/100-penalty
    return dict(St=St,Sc=Sc,Sq=Sq,Sd=Sd,total=tot,Qm=Qm,Ql=Ql,Qh=Qh)
EX={'A':dict(T=150,dT=2.1,R=0.975,defects=1,L5=80,C=520,penalty=0),
    'B':dict(T=125,dT=3.4,R=0.962,defects=2,L5=120,C=380,penalty=5),
    'C':dict(T=210,dT=1.2,R=0.985,defects=0,L5=40,C=860,penalty=0),
    'D':dict(T=175,dT=2.6,R=0.970,defects=1,L5=95,C=600,penalty=0)}
if __name__=='__main__':
    for card in W:
        print(card,{k:round(score(card=card,**v)['total'],1) for k,v in EX.items()})
    for k,v in EX.items():
        s=score(**v); print(k,{x:round(s[x],1) for x in ['St','Sc','Sq','Sd','total']})
