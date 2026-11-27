import math
def n(v,d):
    s=f'{float(v):,.{d}f}'; return s.replace(',','X').replace('.','{,}').replace('X','\\ ').replace('-','-')
def dm(x):
    d=int(x); m=round((x-d)*60)
    if m==60: d+=1; m=0
    return d,m
it=lambda s:r'\mathit{'+s+'}'
def T(P,task,lab,Ac0):
    E={}; r0=P['rows'][0]; res=P['res'][Ac0]['mon'][0]
    pd,pm=dm(task['phi']); sd,sm=dm(task['S'])
    E['2']=r'S=\varphi+%d^{\circ}\,=%d^{\circ}\,%02d^{\prime}'%(round(task['S']-task['phi']),sd,sm) if abs(task['S']-task['phi'])>0.01 else r'S=\varphi=%d^{\circ}\,%d^{\prime}'%(pd,pm)
    L0=P['L'][0]
    E['4']=r'Q_{от,I}=%d\cdot %s\cdot 86\ 400\cdot 10^{-6}=%s\ \mathrm{МДж}'%(task['UA'],n(P['D'][0],2),n(P['Qot'][0],0))
    E['5']=r'V_{гв}=n_{ж}\,q_{гв}=%d\cdot 105=%d\ \mathrm{л/сут}'%(task['n'],P['Vgv'])
    E['6']=r'q_{гв}=\rho_wV_{гв}c_w(T_{hot}-T_{cold})=1\cdot %d\cdot 4180\cdot (%d-%d)\cdot 10^{-6}'%(P['Vgv'],task['Thot'],task['Tcold'])
    E['7']=r'=%s\ \mathrm{МДж/сут}'%n(P['qgv'],2)
    E['8']=r'Q_{гв,I}=%s\cdot 31=%s\ \mathrm{МДж}'%(n(P['qgv'],2),n(P['Qgv'][0],0))
    E['9']=r'L_I=%s+%s=%s\ \mathrm{МДж}'%(n(P['Qot'][0],0),n(P['Qgv'][0],0),n(L0,0))
    E['13']=r'\delta_I=23{,}45^{\circ}\,\ \sin\left[\dfrac{360^{\circ}\,(284+17)}{365}\right]=%s^{\circ}\,'%n(r0['de'],2)
    E['14']=r'\omega_{s,I}=\arccos(-\mathrm{tg}\,%d^{\circ}\,%02d^{\prime}\ \mathrm{tg}(%s^{\circ}\,))=%s^{\circ}\,'%(pd,pm,n(r0['de'],2),n(r0['ws'],2))
    E['16']=r'\bar{H}_{0,I}=%s\ \mathrm{МДж/(м^2\cdot сут)}'%n(r0['H0'],2)
    E['17']=r'\bar{K}_T=\dfrac{\bar{H}}{\bar{H}_0}=\dfrac{%s}{%s}=%s'%(n(P['H'][0],2),n(r0['H0'],2),n(r0['KT'],3))
    E['19']=r'\left(\dfrac{\bar{H}_d}{\bar{H}}\right)_I=1{,}391-3{,}560\cdot %s+4{,}189\cdot %s^2-2{,}137\cdot %s^3=%s'%(n(r0['KT'],3),n(r0['KT'],3),n(r0['KT'],3),n(r0['hd'],3))
    E['21']=r'\bar{R}_{b,I}=%s'%n(r0['Rb'],3)
    cS=math.cos(math.radians(task['S']))
    E['23']=r'\bar{H}_{T,I}=%s(1-%s)\cdot %s+%s\cdot %s\cdot \dfrac{1+%s}{2}+%s\cdot %s\cdot \dfrac{1-%s}{2}'%(n(P['H'][0],2),n(r0['hd'],3),n(r0['Rb'],3),n(P['H'][0],2),n(r0['hd'],3),n(cS,4),n(P['H'][0],2),n(P['rho'][0],2),n(cS,4))
    E['24']=r'=%s\ \mathrm{МДж/(м^2\cdot сут)}'%n(r0['HT'],2)
    E['26']=r'\theta_d^{eff}=59{,}7^{\circ}\,-0{,}1388S+0{,}001497S^2=%s^{\circ}\,'%n(P['thd'],2)
    E['27']=r'\theta_r^{eff}=90^{\circ}\,-0{,}5788S+0{,}002693S^2=%s^{\circ}\,'%n(P['thr'],2)
    E['29']=r'\left(\dfrac{\overline{(\tau\alpha)}}{(\tau\alpha)_n}\right)_I=\dfrac{%s\cdot %s+%s\cdot %s+%s\cdot %s}{%s}=%s'%(n(r0['HbT'],2),n(r0['Kb'],3),n(r0['HdT'],2),n(P['Kd'],3),n(r0['HrT'],2),n(P['Kr'],3),n(r0['HT'],2),n(r0['ta'],3))
    E['30']=r'(\dot{m}c_p)_c=\dot{m}_{af}\,c_{p,af}=%s\cdot 3350=%s\ \mathrm{Вт/(м^2\cdot К)}'%(n(task['maf'],3),n(P['Cc'],2))
    E['31']=r'(\dot{m}c_p)_w=\dot{m}_wc_w=%s\cdot 4180=%s\ \mathrm{Вт/(м^2\cdot К)}'%(n(task['mw'],3),n(P['Cw'],1))
    Cm=min(P['Cc'],P['Cw'])
    E['33']=r'=\left[1+\dfrac{4{,}8}{%s}\left(\dfrac{%s}{0{,}70\cdot %s}-1\right)\right]^{-1}=%s'%(n(P['Cc'],2),n(P['Cc'],2),n(Cm,2),n(P['FF'],4))
    E['34']=r'\dfrac{X_c}{X}=\left(\dfrac{V}{75}\right)^{-0{,}25}=\left(\dfrac{%d}{75}\right)^{-0{,}25}=%s'%(task['V'],n(P['XcX'],4))
    E['35']=r'C_w=\rho_w\dot{V}_wc_w=1000\cdot %s\cdot 4180=%s\ \mathrm{Вт/К}'%(n(task['Vw']/1000,4),n(P['Cwl'],0))
    E['36']=r'C_{air}=\rho_{в}\dot{V}_{air}c_{в}=1{,}2\cdot %s\cdot 1005=%s\ \mathrm{Вт/К}'%(n(task['Vair']/1000,3),n(P['Cair'],1))
    E['37']=r'z_L=\dfrac{\varepsilon_LC_{min}}{(UA)_L}=\dfrac{%s\cdot %s}{%d}=%s'%(n(task['eL'],2),n(P['CminL'],1),task['UA'],n(P['zL'],3))
    E['38']=r'\dfrac{Y_c}{Y}=0{,}39+0{,}65\,\exp\left(-\dfrac{0{,}139}{z_L}\right)=0{,}39+0{,}65\,\exp\left(-\dfrac{0{,}139}{%s}\right)=%s'%(n(P['zL'],3),n(P['YcY'],4))
    E['41']=r'X_I=\dfrac{%d\cdot 4{,}8\cdot %s\cdot (100-(%s))\cdot 31\cdot 86\ 400}{%s\cdot 10^6}\cdot %s=%s'%(Ac0,n(P['FF'],4),n(P['T'][0],2),n(L0,0),n(P['XcX'],4),n(res['X'],3))
    E['42']=r'Y_I=\dfrac{%d\cdot 0{,}68\cdot %s\cdot %s\cdot %s\cdot 31}{%s}\cdot %s=%s'%(Ac0,n(P['FF'],4),n(r0['ta'],3),n(r0['HT'],2),n(L0,0),n(P['YcY'],4),n(res['Y'],4))
    X=res['X']; Y=res['Y']
    E['44']=r'f_I=1{,}029\cdot %s-0{,}065\cdot %s-0{,}245\cdot %s^2+0{,}0018\cdot %s^2+0{,}0215\cdot %s^3'%(n(Y,4),n(X,3),n(Y,4),n(X,3),n(Y,4))
    E['45']=r'=%s'%n(res['f'],4)
    E['47']=r'F_{%d}=\dfrac{%s}{%s}=%s'%(Ac0,n(P['res'][Ac0]['Qs']/1000,2),n(sum(P['L'])/1000,2),n(P['res'][Ac0]['F'],4))
    return E
