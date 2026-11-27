import sys; sys.path.insert(0,'eq')
from render import render
import matplotlib.pyplot as plt
from PIL import Image
def R(tex,out):
    fig=plt.figure(figsize=(0.01,0.01)); fig.text(0,0,'$'+tex+'$',fontsize=14)
    fig.savefig(out,dpi=300,bbox_inches='tight',pad_inches=0.03,facecolor='white'); plt.close(fig)
mode=sys.argv[1]  # old or new
V=dict(old=dict(S='519{,}54',Q='597{,}5',Qk='0{,}5975',Qg='5\\ 033',Vs='786{,}9',Vp='1{,}967',Qu='126{,}9',Quk='0{,}1269',Qug='1\\ 069',P='6\\ 102',T='147\\ 798',qp='0{,}0413',qt='0{,}0355'),
       new=dict(S='520{,}60',Q='598{,}7',Qk='0{,}5987',Qg='5\\ 044',Vs='785{,}8',Vp='1{,}964',Qu='126{,}7',Quk='0{,}1267',Qug='1\\ 067',P='6\\ 111',T='147\\ 806',qp='0{,}0413',qt='0{,}0356'))[mode]
E_={}
E_[84]=r'Q_{\mathrm{тп}}=(1+\beta)\sum q_{\mathrm{н}i}l_i=1{,}15\cdot %(S)s=%(Q)s\ \mathrm{кВт}'
E_[85]=r'Q_{\mathrm{тп}}^{\mathrm{год}}=Q_{\mathrm{тп}}Z=%(Qk)s\cdot 8424=%(Qg)s\ \mathrm{МВт}\cdot\mathrm{ч}'
E_[86]=r'V_{\mathrm{п}}=0{,}0025\sum 2\frac{\pi d_i^2}{4}l_i=0{,}0025\cdot %(Vs)s=%(Vp)s\ \mathrm{м}^3/\mathrm{ч}'
E_[88]=r'Q_{\mathrm{ут}}=V_{\mathrm{п}}\rho c\frac{\tau_{\mathrm{п}}-t_{\mathrm{х}}}{3600}=%(Vp)s\cdot 979{,}7\cdot 4{,}19\cdot \frac{65{,}73-9{,}14}{3600}=%(Qu)s\ \mathrm{кВт}'
E_[89]=r'Q_{\mathrm{ут}}^{\mathrm{год}}=Q_{\mathrm{ут}}Z=%(Quk)s\cdot 8424=%(Qug)s\ \mathrm{МВт}\cdot\mathrm{ч}'
E_[90]=r'Q_{\mathrm{пот}}^{\mathrm{год}}=%(Qg)s+%(Qug)s=%(P)s\ \mathrm{МВт}\cdot\mathrm{ч};\quad Q_{\mathrm{ТЭЦ}}^{\mathrm{год}}=141\ 695+%(P)s=%(T)s\ \mathrm{МВт}\cdot\mathrm{ч}'
E_[91]=r'\bar{q}_{\mathrm{пот}}=\frac{Q_{\mathrm{пот}}^{\mathrm{год}}}{Q_{\mathrm{ТЭЦ}}^{\mathrm{год}}}=%(qp)s;\qquad \bar{q}_{\mathrm{тп}}=\frac{Q_{\mathrm{тп}}^{\mathrm{год}}}{Q_{\mathrm{п}}^{\mathrm{год}}}=%(qt)s'
for k,t in E_.items():
    R(t%V,f'eq/{mode}{k}.png'); print(k, Image.open(f'eq/{mode}{k}.png').size, Image.open(f'd/word/media/image{k}.png').size)
