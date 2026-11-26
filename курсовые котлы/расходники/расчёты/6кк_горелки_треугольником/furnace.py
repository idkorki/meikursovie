import math
B=7.081957679200712; Qt=24424.1; Ta=2307.2; psi=0.934*0.45; N=9200; Ap=26.3
at=10.404; bt=6.12; Vr=1371.36262774361; hr=24.414160548098803; Fr=898.4743469689948; hgo=6.12
def kfun(S,T=1253):
    kg=0.92*(4/S)**0.54*1470/T; kzl=2.96*(Ap/35)**1.33*(1470/T)**0.67
    return kg,kzl,kg+kzl+0.2
def eps(S):
    kg,kzl,k=kfun(S); ef=1-math.exp(-k*0.1*S); et=ef/(ef+(1-ef)*psi); return k,ef,et
def pover(dh,hgor):
    V=Vr+dh*at*bt; F=Fr+2*dh*(at+bt); ht=hr+dh
    S=3.6*V/F; k,ef,et=eps(S); X=hgor/(ht-hgo/2); M=0.59-0.5*X
    qF=B*Qt/F; th=Ta*(1-M*(et*psi*Ta**2/(N*qF))**0.6)-273
    return dict(V=V,F=F,ht=ht,S=S,k=k,ef=ef,et=et,X=X,M=M,qF=qF,th=th)
def constr(hgor):
    htp=hr-hgo/2; X=hgor/htp; M=0.59-0.5*X
    S=3.6*Vr/Fr; k,ef,et=eps(S); Th=1253/Ta
    qF=et*psi*Ta**2/N*(M/(1-Th))**1.67; Ft=B*Qt/qF; dF=Ft-Fr; dh=0.5*dF/(at+bt); V=Vr+dh*at*bt
    return dict(htp=htp,X=X,M=M,S=S,k=k,ef=ef,et=et,Th=Th,qF=qF,Ft=Ft,dF=dF,dh=dh,V=V)
if __name__=='__main__':
    h_old=(1.70+3.825)/2
    print(constr(h_old))
    print(pover(-6.664,h_old))
    dmin=(906.5-Vr)/(at*bt); print('Vmin',pover(dmin,h_old)['th'])
