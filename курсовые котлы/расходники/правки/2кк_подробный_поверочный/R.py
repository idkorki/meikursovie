import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'mathtext.fontset':'custom','mathtext.rm':'Liberation Serif','mathtext.it':'Liberation Serif:italic','mathtext.bf':'Liberation Serif:bold','font.family':'Liberation Serif'})
def R(tex,out,fs=14,pad=0.03):
    fig=plt.figure(figsize=(0.01,0.01)); fig.text(0,0,'$'+tex+'$',fontsize=fs)
    fig.savefig(out,dpi=300,bbox_inches='tight',pad_inches=pad,facecolor='white'); plt.close(fig)
