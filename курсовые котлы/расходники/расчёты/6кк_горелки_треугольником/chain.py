import math
from iapws import IAPWS97
from furnace import *
def hPT(P,t): return IAPWS97(P=P,T=t+273.15).h
def tPH(P,h): return IAPWS97(P=P,h=h).T-273.15
D=58.2; Qp=22400; eta=92.225; H0t=26626.1; H0gg=27228.9; Vg=7.381
Pb=15.893; Ppp=14.19; dP=Pb-Ppp
P_hpp=Pb-0.4*dP; P_shpp=P_hpp-0.2*dP; P_gpp=P_shpp-0.4*dP
ts=IAPWS97(P=Pb,x=1).T-273.15
h_hpp1=IAPWS97(P=Pb,x=1).h; t_hpp2=ts+25; h_hpp2=hPT(P_hpp,t_hpp2)
hpv=925.55; Dvpr=0.05*D; D1=0.6*Dvpr; D2=0.4*Dvpr; Dsh=D-D2; Dhp=D-Dvpr
h_pp=hPT(Ppp,540)
def Hg(th,H0): return H0*th/(2695-0.3*th)
def thH(H,H0): x=H/H0; return 2695*x/(1+0.3*x)
def run(V,F,verbose=True):
    R={}
    Ht2=Hg(980,H0t); Ql=Qt-Ht2
    csh=2*18*0.0352+0.096; phish=1+csh/0.57-math.sqrt(1+(csh/0.57)**2); Fshl=(1.2*6.12+0.5*csh)*at
    ql=B*Ql/(F*0.985); Qshl=1*0.8*ql*phish*Fshl/B
    Hsh=Hg(840,H0t); Qshb=Ht2-Hsh; zsh=17
    dhsh=B*(Qshl+Qshb*zsh/(zsh+1))/Dsh
    h_sh1=(Dhp*h_hpp2+D1*hpv)/(Dhp+D1); t_sh1=tPH(P_hpp,h_sh1)
    h_sh2=h_sh1+dhsh; t_sh2=tPH(P_shpp,h_sh2)
    h_g1=(Dsh*h_sh2+D2*hpv)/(Dsh+D2); t_g1=tPH(P_shpp,h_g1)
    Qlv=Qshl*(1-phish)/phish
    Qgpp=D*(h_pp-h_g1)/B; Qhpp=Dhp*(h_hpp2-h_hpp1)/B-Qlv
    Hgpp=Hsh-Qgpp; Hhpp=Hgpp-Qhpp; thg=thH(Hgpp,H0gg); thx=thH(Hhpp,H0gg)
    # HPP design
    def pack(s1,wr,Dst,xi,thin,thout,tin,tout,Q,counter):
        dn=0.032; dvn=0.022; n0=Dst/(0.785*wr*dvn**2); lk=at-2*s1; n1=math.floor(lk/s1+1)
        n2=round(n0/n1); F1=math.pi*dn*6.12*n1; kzh=1-dn/s1; Fgaz=at*6.12
        thc=(thin+thout)/2; w=B*Vg*(thc+273)/(273*Fgaz*kzh); k=0.86*xi*71*(w/9)**0.5
        if counter: db,dm=thin-tout,thout-tin
        else: db,dm=thin-tin,thout-tout
        if db<dm: db,dm=dm,db
        dt=(db-dm)/math.log(db/dm); Fs=B*Q/(k*dt)*1e3; zr=math.ceil(Fs/F1); zp=math.ceil(zr/(2*n2)*2)/2
        lp=(zr-1)*0.064+dn+0.112*(zp+1)
        return dict(n0=n0,n1=n1,n2=n2,F1=F1,thc=thc,w=w,k=k,db=db,dm=dm,dt=dt,F=Fs,zr=zr,zrr=Fs/F1,zp=zp,zpr=zr/(2*n2),lp=lp)
    hx=pack(0.0918,580,Dhp,1.03,thg,thx,ts,t_hpp2,Qhpp,True)
    gp=pack(0.0838,803,D,1.08,840,thg,t_g1,540,Qgpp,False)
    # economizer
    Pek1=1.18*Ppp; Pek2=Pek1-0.06*Ppp; hek1=hPT(Pek1,215); Dek=D-Dvpr
    Qek=Qp*eta/100-(Ql+Qshb+Qgpp+Qhpp); dhek=Qek*B/Dek; hek2=hek1+dhek; tek2=tPH(Pek2,hek2)
    Hek=Hhpp-Qek; H0ek=23612+0.2*20094; thek=thH(Hek,H0ek)
    s=0.096; kzh=1-0.032/s; Vgek=6.30+1.016*0.2*5.91; thc=(thx+thek)/2
    Fgaz=B*Vgek*(thc+273)/(273*7*kzh); bsh=Fgaz/at; kek=0.86*1.0*85*(7/9)**0.6*(3/2.5)**0.15
    db,dm=thx-tek2,thek-215
    if db<dm: db,dm=dm,db
    dt=(db-dm)/math.log(db/dm); Fek=B*Qek/(kek*dt)*1e3; F1=math.pi*0.032*6.12*106
    zr=math.ceil(Fek/F1); n2=2; zp=math.ceil(zr/(2*n2)*2)/2; lp=(zr-1)*0.0384+0.032+0.0704*(zp+1)
    R.update(locals()); R.update(ts=ts,h_hpp1=h_hpp1,h_hpp2=h_hpp2,h_pp=h_pp,t_hpp2=t_hpp2); return R
if __name__=='__main__':
    r=run(947.0866,678.2681)
    for k in ['Ql','phish','Fshl','ql','Qshl','Qshb','dhsh','h_sh1','t_sh1','h_sh2','t_sh2','h_g1','t_g1','Qlv','Qgpp','Qhpp','Hgpp','Hhpp','thg','thx','Qek','dhek','hek1','hek2','tek2','Hek','thek','thc','Fgaz','bsh','kek','db','dm','dt','Fek','zr','zp','lp','ts','h_hpp1','h_hpp2','h_pp']:
        v=r[k]; print(k, round(v,3) if isinstance(v,float) else v)
    print('hx',{k:round(v,3) for k,v in r['hx'].items()}); print('gp',{k:round(v,3) for k,v in r['gp'].items()})
