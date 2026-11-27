import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Arc
plt.rcParams['font.family']='osifont'
import sys
hxv=3584; hkg=5508; hpr=float(sys.argv[1]); htr=2632; hvch=7344; bt=6120; cs=1836; bpp=bt-cs; hgo=6120; bp=1000
ht=hkg+hpr+htr+hvch; V=sys.argv[2]
fig=plt.figure(figsize=(1013/220,1771/220)); ax=fig.add_axes([0,0,1,1])
B=-hxv/2-2393; T=ht+2380; L=-3900; Rr=L+(T-B)*1013/1771
ax.set_xlim(L,Rr); ax.set_ylim(B,T); ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(plt.Rectangle((L+80,B+80),Rr-L-160,T-B-160,fill=False,lw=2.2))
lw=2.2
y0=hxv/2; ynose1=hkg+hpr; yapex=ynose1+htr; ygo=ht-hgo
x_open1=bt/2-bp/2; x_open2=bt/2+bp/2
ax.plot([x_open1,0,0,bt],[-hxv/2,y0,ht,ht],'k',lw=lw)
ax.plot([x_open2,bt,bt,bpp,bt],[-hxv/2,y0,ynose1,yapex,ygo],'k',lw=lw)
ax.plot([bt,bt],[ygo,ht],'k--',lw=0.8)
ax.plot([x_open1,x_open2],[-hxv/2,-hxv/2],'k--',lw=0.8)
ax.plot([bpp,bpp],[ht,ht+60],'k',lw=1)
# screens
for i in range(6):
    x=bpp+150+i*(cs-250)/5; ax.plot([x,x],[ht-300,ht-hvch+(cs-150-(x-bpp))*0.55],'k',lw=1.5)
ax.annotate('ширмы',xy=(bpp+450,ht-1250),xytext=(bpp-1500,ht-700),fontsize=10.5,arrowprops=dict(arrowstyle='-',lw=0.8))
ax.plot([bpp+450],[ht-1250],'ko',ms=3)
# axis line mid hopper
ax.plot([-2600,bt+600],[0,0],'k-.',lw=0.8)
def vdim(x,y1,y2,txt,ext_from=None,side='left'):
    ax.annotate('',xy=(x,y1),xytext=(x,y2),arrowprops=dict(arrowstyle='<|-|>,head_width=0.18,head_length=0.6',lw=0.9,color='k',shrinkA=0,shrinkB=0))
    ax.text(x-120 if side=='left' else x+120,(y1+y2)/2,txt,rotation=90,ha='right' if side=='left' else 'left',va='center',fontsize=11)
def hdim(y,x1,x2,txt,below=False):
    ax.annotate('',xy=(x1,y),xytext=(x2,y),arrowprops=dict(arrowstyle='<|-|>,head_width=0.18,head_length=0.6',lw=0.9,color='k',shrinkA=0,shrinkB=0))
    ax.text((x1+x2)/2,y-150 if below else y+150,txt,ha='center',va='top' if below else 'bottom',fontsize=11)
X1=-2400; X2=-1200
for yy in [0,ht]: ax.plot([X1-150,0 if yy==ht else -150],[yy,yy],'k',lw=0.7)
vdim(X1,0,ht,'hт=%d'%round(ht))
lv=[0,hkg,hkg+hpr,hkg+hpr+htr,ht]
for yy in lv[1:-1]: ax.plot([X2-150,0],[yy,yy],'k',lw=0.7)
names=['hкг=%d'%hkg,'hпр=%d'%round(hpr),'hтр=%d'%htr,'hвч=%d'%hvch]
for a,b,n in zip(lv,lv[1:],names): vdim(X2,a,b,n)
XR=8100
ax.plot([bt,XR+150],[ygo,ygo],'k',lw=0.7); ax.plot([bt,XR+150],[ht,ht],'k',lw=0.7)
vdim(XR,ygo,ht,'hго=%d'%hgo,side='right')
ax.plot([bt,XR+150],[y0,y0],'k',lw=0.7); ax.plot([x_open2,XR+150],[-hxv/2,-hxv/2],'k',lw=0.7)
vdim(XR,-hxv/2,y0,'hхв=%d'%hxv,side='right')
yt=ht+950
ax.plot([0,0],[ht,yt+150],'k',lw=0.7); ax.plot([bt,bt],[ht,yt+150],'k',lw=0.7)
hdim(yt,0,bpp,"b''=%d"%bpp); hdim(yt,bpp,bt,'cш=%d'%cs)
yb=-hxv/2-1000
ax.plot([0,0],[y0,yb-150],'k',lw=0.7); ax.plot([bt,bt],[y0,yb-150],'k',lw=0.7)
hdim(yb,0,bt,'bт=%d'%bt,below=True)
hdim(-hxv/2-330,x_open1,x_open2,'')
ax.text(bt/2,-hxv/2-420,"b'=%d"%bp,ha='center',va='top',fontsize=11)
ax.add_patch(Arc((x_open1,-hxv/2),1500,1500,theta1=125,theta2=180,lw=0.9))
ax.text(x_open1-1350,-hxv/2+250,'55°',fontsize=11,ha='right')
# gas arrow
ax.annotate('',xy=(bt+1400,ygo+hgo/2+500),xytext=(bt+150,ygo+hgo/2+500),arrowprops=dict(arrowstyle='-|>,head_width=0.3,head_length=0.8',lw=2,color='k'))
ax.text(bt+950,ygo+hgo/2,'газы в\nгориз.\nгазоход',ha='center',va='top',fontsize=10.5,linespacing=1.15)
ax.text(bt/2,yapex-1300,'aт=10404\n(ширина фронта)\nVт=%s м³'%V,ha='center',va='top',fontsize=11,linespacing=1.2)
ax.text(bt/2,hkg+hpr-1000,'горелки: 2 яруса, 6 шт.,\nпо 3 на боковых стенах\nтреугольником вершиной вниз',ha='center',va='top',fontsize=10,linespacing=1.2)
def burner(x,y):
    ax.add_patch(Circle((x,y),425,fill=False,lw=1.6))
    ax.plot([x-560,x+560],[y,y],'k-.',lw=0.6); ax.plot([x,x],[y-560,y+560],'k-.',lw=0.6)
burner(bt/2,1700); burner(bt/4,3825); burner(3*bt/4,3825)
vdim(bt/2+800,0,1700,'1700',side='right'); vdim(bt/4-800,0,3825,'3825',side='right')
for s in ['furnace_new.png']:
    fig.savefig(s,dpi=220,facecolor='white')
