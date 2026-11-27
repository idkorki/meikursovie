import math,itertools
rho,g=979.7,9.81; nu=0.453e-6
L=[1876,120,116,193,83,295,194,198]
G=[265.29,242.98,180.34,158.03,135.72,113.42,91.11,68.80]
din={175:0.184,200:0.207,250:0.259,300:0.309,350:0.359,400:0.408,450:0.466}
# extra (non-compensator) xi per section
extra=[2*0.5+1.0+2*1.27, 0.5+1.0, 0.5+1.0, 0.5+1.0, 0.5+1.0, 0.5+1.0+1.27, 0.5+1.0, 2*0.5+1.0]
def step(Dy):
    pts=[(100,35),(300,50),(1000,80)]
    for (a,b),(c,d) in zip(pts,pts[1:]):
        if Dy<=c: return b+(Dy-a)/(c-a)*(d-b)
def calc(Dys,verbose=False):
    H=100.0; rows=[]
    for i,(l,Gr,Dy) in enumerate(zip(L,G,Dys)):
        SL=sum(L[i:])
        Rl=rho*g*(H-20)/(2*SL*1.1)
        dpre=117e-3*Gr**0.38/Rl**0.19
        d=din[Dy]; w=4*Gr/(rho*math.pi*d*d); Re=w*d/nu
        R=13.62e-6*Gr**2/d**5.25
        n=math.ceil(l/step(Dy)); xic=0.2 if Dy>=300 else 2.5
        xi=n*xic+extra[i]; le=60.7*d**1.25*xi
        dp=R*(l+le); dH=dp/(rho*g); H2=H-2*dH
        rows.append((i+1,l,Gr,H,Rl,dpre*1000,d*1000,Dy,w,Re/1e6,R,n,xi,le,dp,dH,H2, 568*d/0.0005/1e6))
        H=H2
    if verbose:
        for r in rows: print(' '.join(f'{v:.2f}' if isinstance(v,float) else str(v) for v in r))
    return H
base=[400,400,350,350,300,300,300,250]
print(calc(base,True))
print('first pass', calc([400,400,350,350,300,300,250,250]))
