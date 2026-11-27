import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({'font.family':'Liberation Serif','mathtext.fontset':'custom','mathtext.rm':'Liberation Serif','mathtext.it':'Liberation Serif:italic','font.size':10})
M=['Янв','Фев','Мар','Апр','Май','Июн','Июл','Авг','Сен','Окт','Ноя','Дек']
B='#3a6ea5'; O='#d9773a'; G='#3c8c4c'
f1=lambda v,d=1: f'{v:.{d}f}'.replace('.',',')
def loads(P,out):
    fig,ax=plt.subplots(figsize=(1432/200,703/200),dpi=200)
    q=np.array(P['Qot'])/1000; g=np.array(P['Qgv'])/1000; x=np.arange(12)
    ax.bar(x,q,0.72,color=B,label='отопление Q$_{от}$'); ax.bar(x,g,0.72,bottom=q,color=O,label='горячее водоснабжение Q$_{гв}$')
    ax.set_xticks(x); ax.set_xticklabels(M); ax.set_ylabel('L, ГДж/мес'); ax.grid(alpha=0.35); ax.set_axisbelow(True)
    ax.legend(loc='upper center',ncol=2,frameon=False); ax.set_ylim(0,max(q+g)*1.15)
    fig.tight_layout(); fig.savefig(out,facecolor='white'); plt.close(fig)
def rad(P,Slab,out):
    fig,ax=plt.subplots(figsize=(1433/200,703/200),dpi=200); x=np.arange(12)
    ax.plot(x,[r['H0'] for r in P['rows']],'--s',color='#777',ms=4,label=r'$\bar{H}_0$ – вне атмосферы')
    ax.plot(x,P['H'],'-o',color=B,ms=4,label=r'$\bar{H}$ – горизонтальная площадка')
    ax.plot(x,[r['HT'] for r in P['rows']],'-^',color=O,ms=5,label=r'$\bar{H}_T$ – коллектор, S = '+Slab)
    ax.set_xticks(x); ax.set_xticklabels(M); ax.set_ylabel('МДж/(м²·сут)'); ax.grid(alpha=0.35); ax.legend(loc='upper left',frameon=False)
    fig.tight_layout(); fig.savefig(out,facecolor='white'); plt.close(fig)
def fm(P,areas,out):
    fig,ax=plt.subplots(figsize=(1449/200,703/200),dpi=200); x=np.arange(12)
    for a,c,ms in zip(areas,[B,O,G],[8,6,4.5]):
        ax.plot(x,[m['f']*100 for m in P['res'][a]['mon']],'-o',color=c,ms=ms,label='A$_c$ = %d м², F = %s %%'%(a,f1(P['res'][a]['F']*100)))
    ax.set_xticks(x); ax.set_xticklabels(M); ax.set_ylabel('f, %'); ax.set_ylim(0,105); ax.grid(alpha=0.35); ax.legend(loc='upper left',frameon=True)
    fig.tight_layout(); fig.savefig(out,facecolor='white'); plt.close(fig)
def Fcurve(P,solve_area,areas,out):
    fig,ax=plt.subplots(figsize=(1394/200,726/200),dpi=200)
    A=np.linspace(1,180,60); ax.plot([0]+list(A),[0]+[solve_area(a)*100 for a in A],color='#777',lw=1.3)
    for a,c in zip(areas,[B,O,G]):
        F=P['res'][a]['F']*100; ax.plot(a,F,'o',color=c,ms=9); ax.annotate(f1(F)+' %',(a,F),textcoords='offset points',xytext=(0,10),ha='center')
    ax.set_xlim(0,180); ax.set_ylim(0,max(solve_area(180)*100,70)*1.1); ax.set_xlabel('A$_c$, м²'); ax.set_ylabel('F, %'); ax.grid(alpha=0.35)
    fig.tight_layout(); fig.savefig(out,facecolor='white'); plt.close(fig)
