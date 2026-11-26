import sys, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'Liberation Serif','mathtext.fontset':'custom','mathtext.rm':'Liberation Serif','mathtext.it':'Liberation Serif:italic','font.size':12})
x=[0,1876,1996,2112,2305,2388,2683,2877,3075]
mode=sys.argv[1]
H={'old':[100,53.54,50.55,47.53,43.97,41.25,35.17,32.63,26.81],'new':[100,53.54,50.55,47.53,39.94,37.22,31.13,28.60,22.78]}[mode]
exec(open('calc/hyd.py').read().split('base=')[0])
import math
def dHs(Dys):
    Hc=100.0; out=[]
    for i,(l,Gr,Dy) in enumerate(zip(L,G,Dys)):
        d=din[Dy]; R=13.62e-6*Gr**2/d**5.25; n=math.ceil(l/step(Dy)); xi=n*(0.2 if Dy>=300 else 2.5)+extra[i]
        le=60.7*d**1.25*xi; out.append(R*(l+le)/(rho*g))
    return out
dH=dHs({'old':[400,400,350,350,300,300,300,250],'new':[400,400,350,300,300,300,300,250]}[mode])
H=[100]
for d in dH: H.append(H[-1]-2*d)
Hp=[120];Ho=[20]
for d in dH: Hp.append(Hp[-1]-d); Ho.append(Ho[-1]+d)
fig,ax=plt.subplots(figsize=(9.72,5.55))
ax.plot(x,Hp,'k-',marker='o',mfc='white',ms=5,lw=1.6,mew=1.3,label='Подающая линия H$_п$')
ax.plot(x,Ho,'k--',marker='s',mfc='white',ms=5,lw=1.6,mew=1.3,label='Обратная линия H$_о$')
ax.axhline(40,color='#555',ls='-.',lw=1.5,label='Статический напор H$_{ст}$ = 40 м')
ax.axhline(30,color='#666',ls=':',lw=1.3,label='Высота зданий (9 эт.) ≈ 30 м')
for xi,n in zip(x,['ТЭЦ','К1','К2','К3','К4','К5','К6','К7','К8']):
    ax.axvline(xi,color='#888',ls=':',lw=0.8)
    ax.text(xi-10,2,n,rotation=90,ha='right',va='bottom',fontsize=10)
for i in range(8):
    xm=(x[i]+x[i+1])/2; ym=(Hp[i]+Hp[i+1])/2
    ax.text(xm,ym+(18 if i==0 else 3.5),str(i+1),ha='center',fontsize=10)
xe=x[-1]+60
ax.annotate('',xy=(xe,Ho[-1]+1),xytext=(xe,Hp[-1]-1),arrowprops=dict(arrowstyle='<->',lw=1.1))
ax.text(xe+20,(Hp[-1]+Ho[-1])/2,'H$_а$ = %s м'%f'{H[-1]:.1f}'.replace('.',','),va='center',fontsize=10)
ax.set_xlim(-75,3490); ax.set_ylim(0,135)
ax.set_yticks(range(0,121,20)); ax.set_xticks(range(0,3001,500))
ax.grid(True,ls=':',color='#999',lw=0.7)
ax.tick_params(direction='in',labelsize=12); 
for s in ax.spines.values(): s.set_linewidth(1.3)
ax.set_xlabel('Длина главной магистрали от ТЭЦ, м',fontsize=13); ax.set_ylabel('Напор H, м',fontsize=13)
ax.legend(loc=(0.025,0.46),fontsize=10,fancybox=False,edgecolor='#333',framealpha=1)
fig.savefig(f'calc/piezo_{mode}.png',dpi=200,bbox_inches='tight',pad_inches=0.03,facecolor='white')
from PIL import Image; print(Image.open(f'calc/piezo_{mode}.png').size)
print([round(v,2) for v in Hp],[round(v,2) for v in Ho])
