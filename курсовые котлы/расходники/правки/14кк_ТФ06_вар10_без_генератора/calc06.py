"""ТГМП-314А, ТФ-06-24, мазут № 22 (KK_NOTES=1, как 7кк): весь тракт до РВП."""
import math
from iapws import IAPWS97
hPT=lambda P,t: IAPWS97(P=P,T=t+273.15).h
tPH=lambda P,h: IAPWS97(P=P,h=h).T-273.15
def Hg(H0,t): return H0*(t/2050-0.075) if t>1150 else H0*t/(2695-0.3*t)
def tg(H0,H): x=H/H0; return 2695*x/(1+0.3*x)
def Hv(H0,t): return H0*t/(2610-0.25*t)
def tv(H0,H): return 2610*H/(H0+0.25*H)
def solve(r, Dvpr=12.0, fuel=dict(Q=38.77,V0=10.20,V0g=10.99,Hv=34690,Hg=40950)):
    R=dict(r=r); H0v=fuel['Hv']; H0g=fuel['Hg']; V0=fuel['V0']; V0g=fuel['V0g']
    hpp=hPT(25,545); hvt1=hPT(3.9,310); hvt2=hPT(3.7,545); hpv=hPT(31.5,265); hek=hPT(30.75,315)
    Dp=278; Dvt=0.84*Dp; D1=0.6*Dvpr; D2=0.4*Dvpr
    at_=1.03; aux=1.03+0.03+2*0.03+0.02+0.15
    kq=1+0.055*120e-3; Qr=round(kq*fuel['Q'],3)*1000
    H0ux=H0g+(aux-1)*H0v; Hux=Hg(H0ux,150); Hxv=aux*Hv(H0v,30); q2=(Hux-Hxv)*100/Qr
    eta=100-(q2+0.1+0+0.2+0); B=(Dp*(hpp-hpv)+Dvt*(hvt2-hvt1))/(Qr*eta/100); phi=1-0.2/(eta+0.2)
    R.update(locals_:=None) if False else None
    Fpod=17.36*8.53; Fpr=2*(17.36+8.53)*24.22; Fvch=(17.36+2*9.47)*8.1; Fpot=17.36*9.47; Fok=17.36*8.1
    FT=Fpod+Fpr+Fvch+Fpot+Fok; Fe=(FT-Fpod-Fok)*0.99; Vt=Fpod*24.22+Fpot*8.1; S=3.6*Vt/FT
    hgor=(2.35+(2.35+3.02))/2; htp=32.32-0.5*8.1; X=hgor/htp+0.05; M=0.54-0.2*X
    H0gv=Hv(H0v,300); H0xv=Hv(H0v,30); Qv=1.00*H0gv+0.03*H0xv
    H0rc=H0g+(1.14-1)*H0v; Hrc=Hg(H0rc,350); Qt=Qr*(100-0.1)/100+Qv+r*Hrc
    H0t=(H0g+(at_-1)*H0v)*(1+r); tha=2050*(Qt/H0t+0.075); qF=B*Qt/Fe
    xe=1-0.2*(35/32-1); pe=0.55*xe; ppod=0.9*pe; m=0.55*(1.05/1.03)**3*1.05
    its=[]; th=1230.0
    while True:
        b=900/th if th<=1250 else (900/th)**1.2; psh=b*0.55
        psi=(pe*Fe+ppod*Fpod+psh*Fok)/FT; T=th+273
        kg=1.02*(4/S)**0.54*1470/T; kc=0.55*(T/1470)**1.33*8.0/1.03; k2=kg+kc
        af=m*(1-math.exp(-k2*0.1*S))+(1-m)*(1-math.exp(-kg*0.1*S)); at=af/(af+(1-af)*psi)
        mt=at*psi*(tha+273)**2/(9800*qF); tc=(tha+273)*(1-M*mt**0.6)-273
        its.append(dict(th=th,b=b,psh=psh,psi=psi,kg=kg,kc=kc,k2=k2,af=af,at=at,mt=mt,tc=tc,d=th-tc))
        if abs(th-tc)<=30: break
        th=round(tc,-1)
    tht=its[-1]['tc']; bsh=its[-1]['b']
    Ht=H0t*(tht/2050-0.075); Ql=Qt-Ht
    Dt=Dp-D1-D2; hT=hek+Ql*B*(1+0.075)/Dt; tT=tPH(26.25,hT)
    thg=0.5*(0.85*tha+tht); trs=0.5*(315+tT); dtT=thg-trs; ql=B*Ql/(FT*xe); kT=ql*1e3/dtT
    qf=B*fuel['Q']/(17.36*8.53); wT=qf*0.3*at_*(0.9*(tha+273)+tht+273)/546
    # ширмы
    Dsh=Dt+D1; wrsh=Dsh/0.1634; phish=1+4.988/0.827-math.sqrt(1+(4.988/0.827)**2)
    Qshl=bsh*0.6*ql*phish*170.9/B; dh1=17.4*0.6*Dvpr/Dp*100; hsh1=hT-dh1; tsh1=tPH(26.25,hsh1)
    Vg=(V0g+(at_-1)*V0)*(1+r); kzh=1-0.032/0.827
    def shirma(dth):
        dr=1.5*dth/(1+r)**0.33; th2=tht-dr; H2=Hg(H0t,th2); Qb=(Ht-H2)*20/21
        dh=B*(Qshl+Qb)/Dsh; h2=hsh1+dh; t2=tPH(25.625,h2); thc=0.5*(tht+th2); tc=0.5*(tsh1+t2); dt=thc-tc
        w=B*Vg*(thc+273)/(273*17.36*8.1*kzh); k=43*(tht+273)/1400*(1+0.4*(w/7)**0.5); Qtt=k*dt*1108.9/(B*1e3)
        return dict(dth=dth,dr=dr,th2=th2,H2=H2,Qb=Qb,dh=dh,h2=h2,t2=t2,thc=thc,tc=tc,dt=dt,w=w,k=k,Qt=Qtt,dQ=(Qtt-Qb)/Qtt*100)
    R['shirma']=shirma
    sh=min((shirma(d) for d in range(50,300,5)),key=lambda z:abs(z['dQ']))
    Qlv=Qshl*(1-phish)/phish
    # поворотная камера, КПВД
    th1k=sh['th2']-50; H1k=Hg(H0t,th1k); Qpk=sh['H2']-H1k
    dh2=17.4*0.4*Dvpr/Dp*100; hk1=sh['h2']-dh2; tk1=tPH(25.625,hk1); Qk=Dp*(hpp-hk1)/B
    H2k=H1k-Qk*1.03; H0k=(H0g+0.06*H0v)*(1+r); xk=H2k/H0k; th2k=tg(H0k,H2k)
    def kpvd(s1mm):
        n1=math.ceil(7.53/(s1mm/1000)-1-1e-9); s1=7.53/(n1+1); fp=math.pi*0.02**2/4*n1*6; wr=Dp/(2*fp)
        db=th1k-tk1; dm=th2k-545; dt=(db-dm)/math.log(db/dm); thc=0.5*(th1k+th2k)
        Vk=(V0g+0.045*V0)*(1+r); kz=1-0.032/s1; Fg=17.36*7.53*kz; w=B*Vk*(thc+273)/(273*Fg)
        sig=s1/0.032; k=0.86*1.03*74*(w/9)**0.5*(sig/2.5)**0.15; q=k*dt/1000; F=B*Qk/q
        F1=math.pi*0.032*17.36*n1; zr=round(F/F1); zp=zr/6; lp=(zr-1)*0.054+0.032+0.070*(zp+1)
        Fp=F1*zr; dF=(F-Fp)/F*100; Qrr=k*dt*Fp/(B*1000); dQ=(Qrr-Qk)/Qrr*100
        return dict(s1mm=s1mm,n1=n1,s1=s1,fp=fp,wr=wr,db=db,dm=dm,dt=dt,thc=thc,Vk=Vk,kz=kz,Fg=Fg,w=w,sig=sig,k=k,q=q,F=F,F1=F1,zr=zr,zrr=F/F1,zp=zp,lp=lp,Fp=Fp,dF=dF,Qr=Qrr,dQ=dQ)
    kp=kpvd(142)
    if abs(kp['dQ'])>2 or abs(kp['dF'])>2:
        for s in sorted(range(130,171),key=lambda v:abs(v-142)):
            kk=kpvd(s)
            if abs(kk['dQ'])<=2 and abs(kk['dF'])<=2: kp=kk; break
    # КПНД
    Qn=Dvt*(hvt2-hvt1)/B; H2n=H2k-Qn*1.015; H0n=(H0g+0.12*H0v)*(1+r); th2n=tg(H0n,H2n)
    thcn=0.5*(th2k+th2n); Vn=(V0g+0.09*V0)*(1+r); Fgn=17.36*7.53*0.7; wn=B*Vn*(thcn+273)/(273*Fgn)
    dbn=th2k-545; dmn=th2n-310; dtn=(dbn-dmn)/math.log(dbn/dmn)
    kn=0.86*1.03*69*(wn/9)**0.5*(0.032/0.042)**0.35*(0.14/0.042/2.5)**0.15; qn=kn*dtn/1000; Fn=B*Qn/qn
    # ЭК
    n1e=math.ceil(7.53/0.1-1); fek=math.pi*0.022**2/4*n1e*4; Dek=Dp-Dvpr; wre=Dek/(2*fek)
    H2e=Qt-Qr*eta/100; Qe=phi*(H2n-H2e+0.02*H0xv); he2=hpv+B*Qe/Dek; te2=tPH(30.75,he2)
    H0e=(H0g+0.14*H0v)*(1+r); th2e=tg(H0e,H2e); thce=0.5*(th2n+th2e); Ve=(V0g+0.13*V0)*(1+r)
    Fge=17.36*7.53*0.68; we=B*Ve*(thce+273)/(273*Fge)
    dbe=th2n-te2; dme=th2e-265; dte=(dbe-dme)/math.log(dbe/dme)
    ke=0.86*1.0*75*(we/9)**0.5*(3.125/2.5)**0.15; qe=ke*dte/1000; Fe_=B*Qe/qe; F1e=math.pi*0.032*17.36*n1e
    zre=round(Fe_/F1e); zpe=zre/8; lpe=(zre-1)*0.048+0.032+0.070*(zpe+1); Qer=ke*dte*F1e*zre/(B*1000); dQe=(Qer-Qe)/Qer*100
    # РВП
    tsr=0.5*(70+300); H0sr=Hv(H0v,tsr); H1v=H2e/(1+r); Qvp=phi*(H1v-Hux+0.15*H0sr)
    rv=(1.00+0.15)*(70-30)/(300-70); bvp=1.03-0.03+0.075+rv; H0vp1=Hv(H0v,70); H0gv2=H0vp1+Qvp/bvp; tgv=tv(H0v,H0gv2)
    dbv=150-70; dmv=th2e-tgv; dtv=(dbv-dmv)/math.log(dbv/dmv); thcv=0.5*(th2e+150); tcv=0.5*(70+tgv)
    Vgr=V0g+(aux-1-0.075)*V0; Vvr=bvp*V0; wgr=B*Vgr*(thcv+273)/(2*273*29.5); wvr=B*Vvr*(tcv+273)/(2*273*29.5)
    ag=33*(wgr/7)**0.8*1.18*1.425; av=29*(wvr/6)**0.8*1.03*1.425; kv=0.89/(1/(0.5*ag)+1/(0.5*av))
    Fv=B*Qvp*1e3/(2*kv*dtv); Hvp=Fv/24380; qvp=kv*dtv/1e3; Qvt=2*qvp*Fv/B
    L=dict(locals()); L.pop('fuel'); L.pop('kpvd')
    R.update(L); return R
if __name__=='__main__':
    R=solve(0.11)
    for k in ['q2','eta','B','Qt','H0t','tha','qF','tht','Ht','Ql','hT','tT','dtT','ql','kT','qf','wT','Qshl','tsh1','Qlv','th1k','Qpk','tk1','Qk','H2k','th2k','Qn','H2n','th2n','wn','dtn','kn','Fn','H2e','Qe','he2','te2','th2e','we','dte','ke','Fe_','zre','lpe','dQe','H1v','Qvp','tgv','dtv','wgr','wvr','ag','av','kv','Fv','Hvp']:
        print(k,round(float(R[k]),3),end='; ')
    print(); 
    for i in R['its']: print({k:round(v,4) for k,v in i.items()})
    print({k:round(float(v),3) for k,v in R['sh'].items()})
    print({k:round(float(v),3) for k,v in R['kp'].items()})
