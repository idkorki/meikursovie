import math, json
from math import radians as r, degrees as dg, sin, cos, tan, acos, pi
MON=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
NDAYS=[31,28,31,30,31,30,31,31,30,31,30,31]; NDAY=[17,47,75,105,135,162,198,228,258,288,318,344]
def ta_ratio(th):
    """(τα)/(τα)n: одно стекло n=1,526, KL=0,0125; поглощательная способность по Даффи–Бекману (4.11.1)."""
    def tau(t):
        if t<1e-6: t=1e-6
        t=r(t); t2=math.asin(sin(t)/1.526)
        rs=sin(t2-t)**2/sin(t2+t)**2; rp=tan(t2-t)**2/tan(t2+t)**2
        ta=math.exp(-0.0125/cos(t2)); return 0.5*ta*((1-rp)/(1+rp)+(1-rs)/(1+rs))
    def alpha(t):
        return 1-1.5879e-3*t+2.7314e-4*t**2-2.3026e-5*t**3+9.0244e-7*t**4-1.8e-8*t**5+1.7734e-10*t**6-6.9937e-13*t**7
    if th>=90: return 0.0
    rho_d=0.16
    ta_=lambda t: tau(t)*alpha(t)/(1-(1-alpha(t))*rho_d)
    return ta_(th)/ta_(0)
def th_of_K(K):
    lo,hi=0.0,89.9
    for _ in range(60):
        m=(lo+hi)/2
        if ta_ratio(m)>K: lo=m
        else: hi=m
    return (lo+hi)/2
def solve(task,clim):
    phi=task['phi']; S=task['S']; P={}
    H=[clim['ALLSKY_SFC_SW_DWN'][m]*3.6 for m in MON]; D=[clim['HDD18_3'][m] for m in MON]
    T=[clim['T2M'][m] for m in MON]; rho=[clim['ALLSKY_SRF_ALB'][m] for m in MON]
    UA=task['UA']; n=task['n']
    Vgv=n*105; qgv=1*Vgv*4180*(task['Thot']-task['Tcold'])*1e-6
    Qot=[UA*D[i]*86400*1e-6 for i in range(12)]; Qgv=[qgv*NDAYS[i] for i in range(12)]; L=[Qot[i]+Qgv[i] for i in range(12)]
    P.update(H=H,D=D,T=T,rho=rho,Vgv=Vgv,qgv=qgv,Qot=Qot,Qgv=Qgv,L=L)
    thd=59.7-0.1388*S+0.001497*S**2; thr=90-0.5788*S+0.002693*S**2; Kd=task.get('Kd') or ta_ratio(thd); Kr=task.get('Kr') or ta_ratio(thr)
    P.update(thd=thd,thr=thr,Kd=Kd,Kr=Kr)
    rows=[]
    for i in range(12):
        nd=NDAY[i]; de=23.45*sin(r(360*(284+nd)/365))
        ws=dg(acos(-tan(r(phi))*tan(r(de)))); wsp=min(ws,dg(acos(max(-1,min(1,-tan(r(phi-S))*tan(r(de)))))))
        H0=24*3600*1367/pi*(1+0.033*cos(r(360*nd/365)))*(cos(r(phi))*cos(r(de))*sin(r(ws))+pi*ws/180*sin(r(phi))*sin(r(de)))/1e6
        KT=H[i]/H0; hd=(1.391-3.560*KT+4.189*KT**2-2.137*KT**3) if ws<=81.4 else (1.311-3.022*KT+3.427*KT**2-1.821*KT**3)
        Rb=(cos(r(phi-S))*cos(r(de))*sin(r(wsp))+pi*wsp/180*sin(r(phi-S))*sin(r(de)))/(cos(r(phi))*cos(r(de))*sin(r(ws))+pi*ws/180*sin(r(phi))*sin(r(de)))
        Hd=H[i]*hd; HbT=(H[i]-Hd)*Rb; HdT=Hd*(1+cos(r(S)))/2; HrT=H[i]*rho[i]*(1-cos(r(S)))/2; HT=HbT+HdT+HrT
        # эффективный угол прямого излучения: усреднение по часам
        a=0.409+0.5016*sin(r(ws-60)); b=0.6609-0.4767*sin(r(ws-60))
        num=den=0.0; N=400
        for k in range(N):
            w=-ws+(k+0.5)*2*ws/N
            if w<-wsp or w>wsp: continue
            cw=cos(r(w)); cws=cos(r(ws))
            rt=pi/24*(a+b*cw)*(cw-cws)/(sin(r(ws))-pi*ws/180*cws)
            rd=pi/24*(cw-cws)/(sin(r(ws))-pi*ws/180*cws)
            Ib=max(0.0,rt*H[i]-rd*Hd)
            cz=cos(r(phi))*cos(r(de))*cw+sin(r(phi))*sin(r(de)); ct=cos(r(phi-S))*cos(r(de))*cw+sin(r(phi-S))*sin(r(de))
            if cz<=0.01 or ct<=0: continue
            IbT=Ib*ct/cz; th=dg(acos(min(1,ct)))
            num+=IbT*ta_ratio(th); den+=IbT
        Kb=num/den; thb=th_of_K(Kb)
        ta=(HbT*Kb+HdT*Kd+HrT*Kr)/HT
        rows.append(dict(n=nd,de=de,ws=ws,wsp=wsp,H0=H0,KT=KT,hd=hd,Rb=Rb,HbT=HbT,HdT=HdT,HrT=HrT,HT=HT,R=HT/H[i],Kb=Kb,thb=thb,ta=ta))
    P['rows']=rows
    Cc=task['maf']*task['cpaf']; Cw=task['mw']*4180; Cmin=min(Cc,Cw)
    FF=1/(1+task['FRUL']/Cc*(Cc/(0.70*Cmin)-1)); XcX=(task['V']/75)**-0.25
    Cwl=1000*task['Vw']/1000*4180; Cair=1.2*task['Vair']/1000*1005; CminL=min(Cwl,Cair)
    zL=task['eL']*CminL/UA; YcY=0.39+0.65*math.exp(-0.139/zL)
    P.update(Cc=Cc,Cw=Cw,FF=FF,XcX=XcX,Cwl=Cwl,Cair=Cair,CminL=CminL,zL=zL,YcY=YcY)
    res={}
    for Ac in task['Ac']:
        mon=[]
        for i in range(12):
            dt=NDAYS[i]*86400
            X=Ac*task['FRUL']*FF*(100-T[i])*dt/(L[i]*1e6)*XcX
            Y=Ac*task['FRta']*FF*rows[i]['ta']*rows[i]['HT']*NDAYS[i]/L[i]*YcY
            f=1.029*Y-0.065*X-0.245*Y**2+0.0018*X**2+0.0215*Y**3; f=max(0,min(1,f))
            mon.append(dict(X=X,Y=Y,f=f,Qs=f*L[i]))
        Qs=sum(m['Qs'] for m in mon); res[Ac]=dict(mon=mon,Qs=Qs,F=Qs/sum(L))
    P['res']=res
    return P
TASK13=dict(phi=48+13/60,S=48+13/60,UA=630,n=7,Thot=60,Tcold=12,FRta=0.68,FRUL=4.8,maf=0.023,cpaf=3350,mw=0.025,V=85,eL=0.74,Vw=1.2,Vair=610,Ac=[30,60,120])
if __name__=='__main__':
    c=json.load(open('power13.json'))['properties']['parameter']
    P=solve(TASK13,c)
    print('Kd Kr',round(P['Kd'],3),round(P['Kr'],3),'thd',round(P['thd'],2),round(P['thr'],2))
    for i,rw in enumerate(P['rows']): print(i+1,round(rw['H0'],2),round(rw['KT'],3),round(rw['Rb'],3),round(rw['HT'],2),round(rw['thb'],1),round(rw['Kb'],3),round(rw['ta'],3))
    print('L',round(sum(P['L']),2),[round(P['res'][a]['F']*100,1) for a in (30,60,120)], round(P['FF'],4),round(P['XcX'],4),round(P['YcY'],4))
