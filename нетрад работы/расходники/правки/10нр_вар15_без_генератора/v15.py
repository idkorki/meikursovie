import nvcalc, curve, json
phys=nvcalc.ta_ratio; _s=curve.Kf(68)/phys(68)
nvcalc.ta_ratio=lambda t: curve.Kf(t) if t<=68 else max(0,phys(t)*_s)
TASK=dict(phi=40+54/60,S=40+54/60+9,UA=700,n=11,Thot=60,Tcold=10,FRta=0.68,FRUL=4.8,maf=0.025,cpaf=3350,mw=0.035,V=120,eL=0.74,Vw=0.7,Vair=500,Ac=[30,60,100],Kd=0.877,Kr=0.704)
clim=json.load(open('power15.json'))['properties']['parameter']
P=nvcalc.solve(TASK,clim)
