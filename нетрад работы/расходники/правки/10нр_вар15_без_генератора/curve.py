import re,numpy as np, math
pts=[]
for d in ['1нр','2нр','3нр','4нр','5нр','6нр','7нр','8нр']:
    t=open(d+'.txt').read()
    seg=t[t.find('Таблица 4 – '):][:3000]
    for m in re.finditer(r'(Январь|Февраль|Март|Апрель|Май|Июнь|Июль|Август|Сентябрь|Октябрь|Ноябрь|Декабрь)\s.*?(\d+,\d)\s+(0,\d{3})\s+0,\d{3}\s*\n',seg):
        pts.append((float(m.group(2).replace(',','.')),float(m.group(3).replace(',','.'))))
Sv={'1нр':40.9+5,'2нр':43+34/60+5,'3нр':45.8,'4нр':44+44/60+5,'5нр':46+46/60+3,'6нр':44.05+5,'8нр':46+23/60+3,'7нр':48+13/60}
Kr={'1нр':0.674,'2нр':0.694,'3нр':0.673,'4нр':0.703,'5нр':0.703,'6нр':0.698,'8нр':0.700,'7нр':0.692}
for k,S in Sv.items():
    pts.append((90-0.5788*S+0.002693*S**2,Kr[k])); pts.append((59.7-0.1388*S+0.001497*S**2,0.877))
pts.append((0,1.0))
P=np.array(pts); th=P[:,0]; K=P[:,1]
u=1/np.cos(np.radians(th))-1
A=np.vstack([u,u**2,u**3]).T; c,*_=np.linalg.lstsq(A,1-K,rcond=None)
def Kf(t):
    uu=1/math.cos(math.radians(min(t,89)))-1; return 1-(c[0]*uu+c[1]*uu**2+c[2]*uu**3)
res=[K[i]-Kf(th[i]) for i in range(len(th))]
if __name__=='__main__':
    print(len(pts),c, 'maxerr',max(abs(np.array(res))))
    for t in (0,20,30,40,50,56.5,60,67.8,68.35,70,80): print(t,round(Kf(t),4))
