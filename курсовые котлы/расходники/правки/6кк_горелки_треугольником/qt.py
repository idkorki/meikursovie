import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, json, sys
plt.rcParams.update({'font.family':'Liberation Serif','font.size':12})
d=json.loads(sys.argv[1]); out=sys.argv[2]
Q=[d['Ql'],d['Qsh'],d['Qg'],d['Qx'],d['Qek'],d['Qtvp']]
names=['Топка','Ширмы','ГП КПП','ХП КПП','ЭК','ТВП']
x=[0]
for q in Q: x.append(x[-1]+q)
tg=[d['ta'],980,840,d['thg'],d['thx'],d['thek'],140]
fig,ax=plt.subplots(figsize=(10,5.6))
fig.subplots_adjust(left=0.077,right=0.972,top=0.972,bottom=0.18)
for xi in x[1:]: ax.axvline(xi,color='#bbb',lw=0.8)
ax.plot(x,tg,'-o',color='#c0392b',lw=2.2,ms=5,label='газы')
for xi,t in zip(x,tg): ax.text(xi+60,t+40,f'{t:.0f}',color='#c0392b',fontsize=11)
B='#2980b9'
ax.plot([0,x[1]],[d['ts'],d['ts']],'--',color='#2c3e50',lw=1.5); ax.text(60,d['ts']+40,f"{d['ts']:.0f} (кипение)",fontsize=11)
seg=[(x[1],d['tsh1'],x[2],d['tsh2']),(x[2],d['tg1'],x[3],540),(x[3],d['thpp2'],x[4],d['ts']),(x[4],d['tek2'],x[5],215)]
ax.plot([seg[0][0],seg[0][2]],[seg[0][1],seg[0][3]],color=B,lw=2,label='вода и пар')
for s in seg[1:]: ax.plot([s[0],s[2]],[s[1],s[3]],color=B,lw=2)
fs=9.5
ax.text(seg[0][0]+30,seg[0][1]+40,f"{d['tsh1']:.0f}",color=B,fontsize=fs)
ax.text(seg[0][2]-230,seg[0][3]-110,f"{d['tsh2']:.0f}",color=B,fontsize=fs)
ax.text(seg[1][0]+30,seg[1][1]+40,f"{d['tg1']:.0f}",color=B,fontsize=fs)
ax.text(seg[1][2]-300,540-75,'540',color=B,fontsize=fs)
ax.text(seg[2][0]+30,seg[2][1]+40,f"{d['thpp2']:.0f}",color=B,fontsize=fs)
ax.text(seg[2][2]-520,d['ts']-110,f"{d['ts']:.0f}",color=B,fontsize=fs)
ax.text(seg[3][0]+30,seg[3][1]+40,f"{d['tek2']:.0f}",color=B,fontsize=fs)
ax.text(seg[3][0]+60,215-130,'215',color=B,fontsize=fs)
G='#27ae60'
ax.plot([x[5],x[6]],[250,50],color=G,lw=2,label='воздух')
ax.text(x[5]+30,250+30,'250',color=G,fontsize=fs); ax.text(x[6]-230,50-110,'50',color=G,fontsize=fs)
ax.set_xlim(0,x[-1]+450); ax.set_ylim(0,2200)
ax.set_ylabel('t, °C',fontsize=13)
ax.legend(loc='upper right',fontsize=11,framealpha=1)
for i,n in enumerate(names):
    xm=(x[i]+x[i+1])/2
    ax.text(xm,-120,f'{n}\n{Q[i]:.0f}',ha='center',va='top',fontsize=10)
ax.text(x[-1]/2+600,-370,'Q, кДж/кг',ha='center',va='top',fontsize=13)
ax.tick_params(labelsize=12.5)
fig.savefig(out,dpi=200,facecolor='white')
