import math
from chain import *
def c(v,n): # number with comma and thin-space thousands
    s=f'{v:,.{n}f}'.replace(',','X').replace('.','{,}').replace('X','\\ ')
    return s
def build(hg_mode):
    if hg_mode=='old':
        hg=(1.70+3.825)/2; ht=17.75
    else:
        hg=(2*1.70+4*3.825)/6; ht=18.30
    co=constr(hg); p=pover(ht-hr,hg); r=run(p['V'],p['F']); hx=r['hx']; gp=r['gp']
    v={}
    # displayed rounded intermediates
    X=co['X']; M=co['M']; qF=co['qF']; Ft=co['Ft']; dF=co['dF']; dh=co['dh']; V=co['V']
    dhf=ht-hr; Vf=p['V']; Ff=p['F']; qV=7.082*22400/Vf; qFp=p['qF']; Mp=p['M']; etp=p['et']; th=p['th']
    E={}
    if hg_mode=='old':
        E[87]=r'h_{\mathrm{гор}}=\dfrac{h_{\mathrm{ниж}}+h_2}{2}=\dfrac{1{,}70+3{,}825}{2}=2{,}763\ \mathrm{м}'
    else:
        E[87]=r'h_{\mathrm{гор}}=\dfrac{n_{\mathrm{ниж}}h_{\mathrm{ниж}}+n_2h_2}{n_{\mathrm{ниж}}+n_2}=\dfrac{2\cdot 1{,}70+4\cdot 3{,}825}{2+4}=%s\ \mathrm{м}'%c(hg,3)
    E[89]=r'X_{\mathrm{т}}=\dfrac{h_{\mathrm{гор}}}{h_{\mathrm{т}}^{\prime}}=\dfrac{%s}{21{,}354}=%s'%(c(hg,3),c(X,3))
    E[90]=r'M=0{,}59-0{,}5\,X_{\mathrm{т}}=0{,}59-0{,}5\cdot %s=%s'%(c(X,3),c(M,3))
    E[99]=r'q_F=\dfrac{\varepsilon_{\mathrm{т}}\,\psi_{\mathrm{т}}\,T_{\mathrm{а}}^2}{N}\left(\dfrac{M}{1-\Theta_{\mathrm{т}}^{\prime\prime}}\right)^{1{,}67}=\dfrac{0{,}927\cdot 0{,}420\cdot 2\ 307{,}2^2}{9200}\left(\dfrac{%s}{1-0{,}543}\right)^{1{,}67}'%c(M,3)
    E[100]=r'=%s\ \mathrm{кВт/м}^2'%c(qF,1)
    E[101]=r'F_{\mathrm{т}}=\dfrac{B\,Q_{\mathrm{т}}}{q_F}=\dfrac{7{,}082\cdot 24\ 424{,}1}{%s}=%s\ \mathrm{м}^2'%(c(qF,1),c(Ft,1))
    E[102]=r'\Delta F_{\mathrm{пр}}=F_{\mathrm{т}}-F_{\mathrm{ст}}^{\mathrm{р}}=%s-898{,}5=%s\ \mathrm{м}^2'%(c(Ft,1),c(dF,1).replace('-','-'))
    E[103]=r'\Delta h_{\mathrm{пр}}=\dfrac{0{,}5\,\Delta F_{\mathrm{пр}}}{a_{\mathrm{т}}+b_{\mathrm{т}}}=\dfrac{0{,}5\cdot (%s)}{10{,}404+6{,}12}=%s\ \mathrm{м}'%(c(dF,1),c(dh,3))
    E[104]=r'V_{\mathrm{т}}=V_{\mathrm{т}}^{\mathrm{р}}+\Delta h_{\mathrm{пр}}\,a_{\mathrm{т}}\,b_{\mathrm{т}}=1\ 371{,}4+(%s)\cdot 10{,}404\cdot 6{,}12=%s\ \mathrm{м}^3'%(c(dh,3),c(V,1))
    E[105]=r'\Delta h_{\mathrm{пр}}=\dfrac{V_{\mathrm{т}}-V_{\mathrm{т}}^{\mathrm{р}}}{a_{\mathrm{т}}\,b_{\mathrm{т}}}=\dfrac{%s-1\ 371{,}4}{10{,}404\cdot 6{,}12}=%s\ \mathrm{м}'%(c(Vf,1),c(dhf,3))
    E[106]=r'h_{\mathrm{т}}=h_{\mathrm{т}}^{\mathrm{р}}+\Delta h_{\mathrm{пр}}=24{,}414+(%s)=%s\ \mathrm{м}'%(c(dhf,3),c(ht,3))
    E[107]=r'F_{\mathrm{ст}}=F_{\mathrm{ст}}^{\mathrm{р}}+2\,\Delta h_{\mathrm{пр}}(a_{\mathrm{т}}+b_{\mathrm{т}})=898{,}5+2\cdot (%s)(10{,}404+6{,}12)'%c(dhf,3)
    E[108]=r'=%s\ \mathrm{м}^2'%c(Ff,1)
    E[110]=r'q_V=\dfrac{B\,Q_{\mathrm{н}}^{\mathrm{р}}}{V_{\mathrm{т}}}=\dfrac{7{,}082\cdot 22\ 400}{%s}=%s\ \mathrm{кВт/м}^3'%(c(Vf,1),c(qV,1))
    E[112]=r'q_F=\dfrac{B\,Q_{\mathrm{т}}}{F_{\mathrm{ст}}}=\dfrac{7{,}082\cdot 24\ 424{,}1}{%s}=%s\ \mathrm{кВт/м}^2'%(c(Ff,1),c(qFp,1))
    E[113]=r'\vartheta_{\mathrm{т}}^{\prime\prime}=2\ 307{,}2\left[1-%s\left(\dfrac{%s\cdot 0{,}420\cdot 2\ 307{,}2^2}{9200\cdot %s}\right)^{0{,}6}\right]-273=%s\ ^{\circ}\;\mathrm{C}'%(c(Mp,3),c(etp,3),c(qFp,1),c(th,1))
    E[114]=r'\Delta\vartheta=|\vartheta_{\mathrm{т}}^{\prime\prime}-\vartheta_{\mathrm{т.\,р}}^{\prime\prime}|=|980-%s|=%s\ ^{\circ}\,\mathrm{C}'%(c(th,1),c(abs(980-th),1))
    v.update(hg=hg,ht=ht,X=X,M=M,qF=qF,Ft=Ft,dF=dF,dh=dh,V=V,dhf=dhf,Vf=Vf,Ff=Ff,qV=qV,qFp=qFp,Mp=Mp,etp=etp,th=th,p=p,co=co,r=r)
    return E,v
