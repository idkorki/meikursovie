import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
plt.rcParams.update({'font.family':'Liberation Serif','mathtext.fontset':'custom','mathtext.rm':'Liberation Serif'})
f1=lambda v,d=1: f'{v:.{d}f}'.replace('.',',')
def box(ax,x,y,w,h,t,fs=10):
    ax.add_patch(Rectangle((x,y),w,h,fill=False,lw=1.3)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs)
def arr(ax,x1,y1,x2,y2,ls='-'):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='-|>',lw=1.1,ls=ls,color='k',shrinkA=0,shrinkB=0))
def water(R,out):
    fig=plt.figure(figsize=(1745/200,902/200)); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,1745); ax.set_ylim(902,0); ax.axis('off')
    y=235; h=110; bx=[(240,'ЭК'),(570,'Экраны топки\n(НРЧ, СРЧ, ВРЧ)'),(955,'ШП'),(1340,'КПВД')]
    ws={0:180,1:220,2:180,3:180}
    xs=[]
    for i,(x,t) in enumerate(bx): box(ax,x,y,ws[i],h,t,11 if i!=1 else 10); xs.append((x,x+ws[i]))
    arr(ax,130,y+h/2,240,y+h/2)
    for (a,b),(c,d) in zip(xs,xs[1:]): arr(ax,b,y+h/2,c,y+h/2)
    arr(ax,xs[-1][1],y+h/2,1740,y+h/2)
    # впрыски
    ax.plot([180,180,1270,1270],[y+h/2,85,85,y+h/2-10],'k--',lw=1.1); ax.plot([880,880],[85,y+h/2-10],'k--',lw=1.1)
    arr(ax,880,y+h/2-30,880,y+h/2); arr(ax,1270,y+h/2-30,1270,y+h/2)
    ax.text(530,72,'ΣDвпр = 21 кг/с',fontsize=10)
    ax.text(895,135,'впрыск I\n12,6 кг/с',fontsize=9,va='top'); ax.text(1285,135,'впрыск II\n8,4 кг/с',fontsize=9,va='top')
    fs=9.3; yt=y+h+25
    ax.text(140,yt,'пит. вода\n278 кг/с\n31,5 МПа\n265 °С',fontsize=fs,va='top')
    ax.text(465,yt,'30,75 МПа\n315 °С',fontsize=fs,va='top',ha='center')
    ax.text(855,yt,'26,25 МПа\n%s °С\n→ %s °С'%(f1(R['tT']),f1(R['tsh1'])),fontsize=fs,va='top',ha='center')
    ax.text(1245,yt,'25,625 МПа\n%s °С\n→ %s °С'%(f1(R['sh']['t2']),f1(R['tk1'])),fontsize=fs,va='top',ha='center')
    ax.text(1650,yt,'острый пар\n278 кг/с\n25 МПа\n545 °С',fontsize=fs,va='top',ha='center')
    y2=690; box(ax,790,y2,360,105,'КПНД (промперегрев)',11)
    arr(ax,330,y2+52,790,y2+52); arr(ax,1150,y2+52,1600,y2+52)
    ax.text(330,y2+35,'от ЦВД: 233,5 кг/с, 3,9 МПа, 310 °С',fontsize=fs); ax.text(1170,y2+35,'в ЦСД: 3,7 МПа, 545 °С',fontsize=fs)
    fig.savefig(out,dpi=200,facecolor='white'); plt.close(fig)
def gas(R,out):
    fig=plt.figure(figsize=(1745/200,871/200)); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,1745); ax.set_ylim(871,0); ax.axis('off')
    names=['Топка','ШП','ПК','КПВД','КПНД','ЭК','РВП']; x0=150; w=130; gap=95; y=245; h=115
    xs=[x0+i*(w+gap) for i in range(7)]
    for x,t in zip(xs,names): box(ax,x,y,w,h,t,11)
    for a,b in zip(xs,xs[1:]): arr(ax,a+w,y+h/2,b,y+h/2)
    arr(ax,xs[-1]+w,y+h/2,1740,y+h/2); ax.text(1700,y+h/2-15,'к ДС',fontsize=9.5,ha='center')
    vals=[(f1(R['tht'],0),'1,05'),(f1(R['sh']['th2'],0),'1,05'),(f1(R['th1k'],0),'1,05'),(f1(R['th2k'],0),'1,08'),(f1(R['th2n'],0),'1,14'),(f1(R['th2e'],0),'1,16'),('120','1,31')]
    for x,(t,a) in zip(xs,vals):
        ax.text(x+w+6,y+h/2+12,('%s °С'%t if t!='–' else '–'),fontsize=8.5,va='top'); ax.text(x+w+6,y+h/2+38,'α = '+a,fontsize=8.5,va='top')
    ax.text(xs[0]+w+6,y+h+28,'ϑа = %s °С'%f1(R['tha'],0),fontsize=9,va='top')
    xr=xs[5]+w+45
    ax.plot([xr,xr,xs[0]+70,xs[0]+70],[y+h/2,95,95,y-8],'k--',lw=1.1); arr(ax,xs[0]+70,y-30,xs[0]+70,y)
    ax.text(620,82,'рециркуляция газов, rг = %s  (ДРГ)'%f1(R['r'],2),fontsize=10)
    ax.add_patch(Rectangle((xs[6],y+h),w,240,fill=False,lw=1.1,ls='--'))
    ax.plot([xs[6],xs[0]+45],[y+h+225,y+h+225],'k',lw=1.2); arr(ax,xs[0]+45,y+h+225,xs[0]+45,y+h)
    ax.text(820,y+h+210,'горячий воздух к горелкам, tгв = 300 °С (расчёт %s °С)'%f1(R['tgv']),fontsize=10,ha='center')
    arr(ax,1740,y+h+225,xs[6]+w,y+h+225); ax.text(1735,y+h+300,'холодный воздух 30 °С (от ДВ)',fontsize=9.5,ha='right')
    fig.savefig(out,dpi=200,facecolor='white'); plt.close(fig)
if __name__=='__main__':
    from calcg import solve
    R=solve(0.05)
    water(R,'new/10.png'); gas(R,'new/11.png')
