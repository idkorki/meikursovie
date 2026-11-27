"""ТГМП-314А, поток ТФ-07-24 (Апаров): цепочка до КПВД, как в 5кк/10кк/11кк."""
import math
from iapws import IAPWS97
def h_PT(P,t): return IAPWS97(P=P,T=t+273.15).h
def t_PH(P,h): return IAPWS97(P=P,h=h).T-273.15
H2200={'RO2':5391.58,'N2':3289.76,'H2O':4396.70,'air':3402.0}   # кДж/м3 при 2200 °С (Нормы 1998, табл. XVI)
def gas_from_comp(c):
    CH4,C2,C3,C4,C5,C6,CO2,N2=c
    V0=0.0476*(2*CH4+3.5*C2+5*C3+6.5*C4+8*C5+9.5*C6)
    RO2=0.01*(CO2+CH4+2*C2+3*C3+4*C4+5*C5+6*C6); VN=0.79*V0+0.01*N2
    H2O=0.01*(2*CH4+3*C2+4*C3+5*C4+6*C5+7*C6)+0.0161*V0
    return V0,RO2,VN,H2O
def solve(G,r,thux,txv,s1_mm=142):
    R={}
    Q=G['Q']*1000; V0=G['V0']; V0g=G['V0g']; Hg=G['Hg']; Hv=G['Hv']
    R.update(Q=Q,V0=V0,V0g=V0g,Hg=Hg,Hv=Hv,r=r,thux=thux,txv=txv)
    hpp=h_PT(25,545); hvt1=h_PT(3.9,310); hvt2=h_PT(3.7,545); hpv=h_PT(31.5,265); hek=h_PT(30.75,315)
    R.update(hpp=hpp,hvt1=hvt1,hvt2=hvt2,hpv=hpv,hek=hek)
    Dp=278; Dvt=0.84*Dp
    tgv=265+45+0.7*(thux-120); R['tgv']=tgv
    aux=1.05+0+0.03+2*0.03+0.02+0.15
    H0ux=(Hg+(aux-1)*Hv)*(1+r); Hux=H0ux*thux/(2695-0.3*thux); Hxv=aux*Hv*txv/(2610-0.25*txv)
    q2=(Hux-Hxv)*100/Q; eta=100-(q2+0.15+0+0.2+0)
    B=(Dp*(hpp-hpv)+Dvt*(hvt2-hvt1))/(Q*eta/100); phi=1-0.2/(eta+0.2)
    R.update(aux=aux,H0ux=H0ux,Hux=Hux,Hxv=Hxv,q2=q2,eta=eta,B=B,phi=phi)
    Fpr=2*(8.51+17.32)*24.20; Fvch=(2*9.45+17.32)*8.3+17.32*9.45; Fpod=8.51*17.32; Ft=Fpr+Fvch+Fpod
    Fsh=((8.51-9.45)+8.3)*17.32; Vt=Fpod*24.20+9.45*17.32*8.3; s=3.6*Vt/(Ft+Fsh)
    hgor=2.38+0.5*3.04; htr=8.3+24.20-0.5*8.3; chi=hgor/htr+0.05; M=(0.54-0.2*chi)-0.12*r
    R.update(Fpr=Fpr,Fvch=Fvch,Fpod=Fpod,Ft=Ft,Fsh=Fsh,Vt=Vt,s=s,chi=chi,M=M)
    H0gv=Hv*tgv/(2610-0.25*tgv); H0xv=1.313*V0*txv; Qv=1.02*H0gv+0.03*H0xv
    trc=tgv+45; H0rc=Hg+(1.16-1)*Hv; Hrc=H0rc*trc/(2695-0.3*trc)
    Qt=Q*(100-0.15)/100+Qv+r*Hrc; H0t=(Hg+0.05*Hv)*(1+r); tha=2050*(Qt/H0t+0.075); qF=B*Qt/Ft/1000
    R.update(H0gv=H0gv,H0xv=H0xv,Qv=Qv,trc=trc,H0rc=H0rc,Hrc=Hrc,Qt=Qt,H0t=H0t,tha=tha,qF=qF)
    psi_e=0.65; psi_pod=0.9*psi_e; psi_sh=0.8*psi_e; psi=(psi_e*Fpr+psi_pod*Fpod+psi_sh*Fvch)/(Fpr+Fpod+Fvch)
    m=0.1*(1.05/1.05)**3*1.05; R.update(psi=psi,m=m)
    its=[]; th=1300.0
    while True:
        T=th+273; kgg=1.18*(4/s)**0.54*1470/T; kc=0.55*(T/1470)**1.33*2.9/1.05; k2=kgg+kc
        ef=m*(1-math.exp(-k2*0.1*s))+(1-m)*(1-math.exp(-kgg*0.1*s)); et=ef/(ef+(1-ef)*psi)
        mt=et*psi*(tha+273)**2/(9800*qF*1000); tc=(tha+273)*(1-M*mt**0.6)-273
        its.append(dict(th=th,kgg=kgg,kc=kc,k2=k2,ef=ef,et=et,mt=mt,tc=tc,d=abs(th-tc)))
        if abs(th-tc)<=30: break
        th=round(tc,-1)
    tht=its[-1]['tc']; R['its']=its; R['tht']=tht
    Ht=H0t*(tht/2050-0.075); Ql=(Qt-Ht)*phi; ql=B*Ql/(0.99*Ft); qV=B*Q/Vt; qf=B*Q/147.39
    R.update(Ht=Ht,Ql=Ql,ql=ql,qV=qV,qf=qf)
    hnk=h_PT(30.75,318); Dt=257.0; hT=hnk+B*Ql*1.135/Dt*0.95; tT=t_PH(26.25,hT)
    R.update(hnk=hnk,hT=hT,tT=tT)
    ssh=17.32/21; csh=4.848-1.5; phish=1+4.848/ssh-(1+(4.848/ssh)**2)**0.5
    bsh=700/tht; Fsh1=(4.848+8.1)*17.32; Qlsh=ql*bsh*0.8*phish*Fsh1/B
    d1=21*0.6/278*100; dh1=17.4*d1; hsh1=hT-dh1; tsh1=t_PH(26.25,hsh1)
    d2=21*0.4/278; Dsh=278*(1-d2)
    R.update(ssh=ssh,phish=phish,bsh=bsh,Fsh1=Fsh1,Qlsh=Qlsh,d1=d1,dh1=dh1,hsh1=hsh1,tsh1=tsh1,d2=d2,Dsh=Dsh)
    Vg=(V0g+0.05*V0)*(1+r); kzh=1-0.032/ssh; Fsht=2*csh*8.1*0.96*20
    def shirma(dth):
        th2=tht-dth; thc=(tht+th2)/2; H2=H0t*th2/(2695-0.3*th2); Qsb=(Ht-H2)*20/22
        dh=B*(Qlsh+Qsb)/Dsh; h2=hsh1+dh; t2=t_PH(25.625,h2); dt=thc-0.5*(tsh1+t2)
        w=B*Vg/(17.32*(8.1+4.848)*kzh)*(thc+273)/273; k=71*(tht+273)*(1+0.3*(w/7)**0.5)/1400
        Qst=k*dt*Fsht/(B*1000); mm=(Qst-Qsb)/Qst
        return dict(dth=dth,th2=th2,thc=thc,H2=H2,Qsb=Qsb,dh=dh,h2=h2,t2=t2,dt=dt,w=w,k=k,Qst=Qst,m=mm)
    sh165=shirma(165); best=min((shirma(d) for d in range(165,400,5)),key=lambda z:abs(z['m']))
    assert abs(best['m'])<0.05
    Qsb2=best['Qst']*(1-0.1*best['m']); H2b=Ht-Qsb2*22/20; x=H2b/H0t; th2b=2695*x/(1+0.3*x)
    h2b=hsh1+B*(Qlsh+Qsb2)/Dsh; t2b=t_PH(25.625,h2b); Qlvyh=Qlsh*(1-phish)/phish
    R.update(Vg=Vg,kzh=kzh,Fsht=Fsht,sh165=sh165,sh=best,Qsb2=Qsb2,H2b=H2b,th2b=th2b,h2b=h2b,t2b=t2b,Qlvyh=Qlvyh)
    th1k=th2b-50; H1k=H0t*th1k/(2695-0.3*th1k); Qpk=H2b-H1k
    dh2=17.4*0.4*21/278*100; hk1=h2b-dh2; tk1=t_PH(25.625,hk1); Qk=278*(hpp-hk1)/B
    H2k=H1k-Qk*1.03; H0k=(Hg+0.08*Hv)*(1+r); xk=H2k/H0k; th2k=2695*xk/(1+0.3*xk)
    R.update(th1k=th1k,H1k=H1k,Qpk=Qpk,dh2=dh2,hk1=hk1,tk1=tk1,Qk=Qk,H2k=H2k,H0k=H0k,xk=xk,th2k=th2k)
    def kpvd(s1mm):
        s1_0=s1mm/1000; n1=round(7.53/s1_0-1+0.4999) if False else math.ceil(7.53/s1_0-1-1e-9)
        s1=7.53/(n1+1); fp=math.pi*0.020**2/4*n1*6; wr=278/(2*fp)
        db=th1k-tk1; dm=th2k-545; dt=(db-dm)/math.log(db/dm); thc=0.5*(th1k+th2k)
        Vk=(V0g+(1.065-1)*V0)*(1+r); kz=1-0.032/s1; Fg=17.32*7.53*kz; w=B*Vk*(thc+273)/(273*Fg)
        sig=s1/0.032; k=0.86*1.03*100*(w/9)**0.5*1*(sig/2.5)**0.15; q=k*dt/1000; F=B*Qk/q
        F1=math.pi*0.032*17.32*n1; zr=round(F/F1); zp=zr/6; lp=(zr-1)*0.054+0.032+0.070*(zp+1)
        Fp=F1*zr; dF=(F-Fp)/F*100; Qr=k*dt*Fp/(B*1000); dQ=(Qr-Qk)/Qr*100
        return dict(s1mm=s1mm,s1_0=s1_0,n1=n1,s1=s1,fp=fp,wr=wr,db=db,dm=dm,dt=dt,thc=thc,Vk=Vk,kz=kz,Fg=Fg,w=w,sig=sig,k=k,q=q,F=F,F1=F1,zr=zr,zrr=F/F1,zp=zp,lp=lp,Fp=Fp,dF=dF,Qr=Qr,dQ=dQ)
    kp=kpvd(s1_mm); tried=[kp]
    if abs(kp['dQ'])>2 or abs(kp['dF'])>2:
        for s in sorted(range(130,171),key=lambda v:abs(v-142)):
            kk=kpvd(s); tried.append(kk)
            if abs(kk['dQ'])<=2 and abs(kk['dF'])<=2: kp=kk; break
    R.update(kp=kp,kp0=tried[0],Dp=Dp,Dvt=Dvt)
    return R
G10=dict(Q=35.59,V0=9.44,V0g=10.59,Hg=39311,Hv=32122,RO2=0.99,N2=7.47,H2O=2.13)
if __name__=='__main__':
    R=solve(G10,0.05,125,20)
    for k in ['tgv','H0ux','Hux','Hxv','q2','eta','B','phi','s','M','H0gv','H0xv','Qv','Hrc','Qt','H0t','tha','qF','psi','tht','Ht','Ql','ql','qV','qf','hnk','hT','tT','Qlsh','hsh1','tsh1','Qsb2','th2b','h2b','t2b','th1k','Qpk','hk1','tk1','Qk','H2k','th2k']:
        print(k, round(R[k],4))
    for i in R['its']: print({k:round(v,4) for k,v in i.items()})
    print({k:round(v,4) for k,v in R['sh'].items()}); print('m165',round(R['sh165']['m'],4))
    print({k:round(v,4) if isinstance(v,float) else v for k,v in R['kp'].items()})
