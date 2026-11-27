import math
def n(v,d):
    s=f'{float(v):,.{d}f}'
    return s.replace(',','X').replace('.','{,}').replace('X','\\ ')
rm=lambda s:r'\mathrm{'+s+'}'
DEG=r'\ ^{\circ}\;\mathrm{C}'
KJ=r'\ \mathrm{кДж/м}^3'; KJKG=r'\ \mathrm{кДж/кг}'
def T(R,G):
    E={}; it=R['its']; i1=it[0]; sh=R['sh']; kp=R['kp']
    comp=G['comp']; names=[(2,'CH4'),(3.5,'C2'),(5,'C3'),(6.5,'C4'),(8,'C5'),(9.5,'C6')]
    terms='+'.join(('%s\\cdot %s'%(('%g'%c).replace('.','{,}'),n(v,1 if G.get('dec1') else 2))) for (c,_),v in zip(names,comp[:6]) if v>0)
    E[3]=r'=0{,}0476(%s)=%s\ \mathrm{м}^3/\mathrm{м}^3'%(terms,n(G['V0'],2))
    E[25]=r'=(%s+(1{,}31-1)\cdot %s)(1+%s)=%s'%(n(G['Hg'],0),n(G['Hv'],0),n(R['r'],2),n(R['H0ux'],1))+KJ
    E[26]=r'H_{\mathrm{ух}}=\dfrac{H_0^{\mathrm{ух}}\vartheta_{\mathrm{ух}}}{2695-0{,}3\,\vartheta_{\mathrm{ух}}}=\dfrac{%s\cdot %d}{2695-0{,}3\cdot %d}=%s'%(n(R['H0ux'],1),R['thux'],R['thux'],n(R['Hux'],2))+KJ
    E[27]=r'H_{\mathrm{х.в}}=\alpha_{\mathrm{ух}}\dfrac{H_{\mathrm{в}}^0\,t_{\mathrm{х.в}}}{2610-0{,}25\,t_{\mathrm{х.в}}}=1{,}31\dfrac{%s\cdot %d}{2610-0{,}25\cdot %d}=%s'%(n(G['Hv'],0),R['txv'],R['txv'],n(R['Hxv'],2))+KJ
    E[28]=r'q_2=\dfrac{(H_{\mathrm{ух}}-H_{\mathrm{х.в}})(100-q_4)}{Q_{\mathrm{р}}^{\mathrm{р}}}=\dfrac{(%s-%s)(100-0)}{%s}'%(n(R['Hux'],2),n(R['Hxv'],2),n(R['Q'],0))
    E[29]=r'=%s\ \%%'%n(R['q2'],3)
    E[31]=r'=100-(%s+0{,}15+0+0{,}2+0)=%s\ \%%'%(n(R['q2'],3),n(R['eta'],3))
    E[33]=r'=\dfrac{278(3\ 323{,}02-1\ 158{,}11)+233{,}52(3\ 551{,}65-2\ 992{,}50)}{%s\cdot %s}'%(n(R['Q'],0),n(R['eta']/100,5))
    E[34]=r'=%s\ \mathrm{м}^3/\mathrm{с}'%n(R['B'],3)
    E[35]=r'B_{\mathrm{р}}=B(1-0{,}01\,q_4)=%s(1-0)=%s\ \mathrm{м}^3/\mathrm{с}'%(n(R['B'],3),n(R['B'],3))
    E[36]=r'\varphi=1-\dfrac{q_5}{\eta_{\mathrm{к}}+q_5}=1-\dfrac{0{,}2}{%s+0{,}2}=%s'%(n(R['eta'],3),n(R['phi'],4))
    E[49]=r'M=(0{,}54-0{,}2\,\chi_{\mathrm{т}})-0{,}12\,r_{\mathrm{г}}=(0{,}54-0{,}2\cdot 0{,}188)-0{,}12\cdot %s'%n(R['r'],2)
    E[50]=r'=%s'%n(R['M'],3)
    E[51]=r'H_{\mathrm{г.в}}^0=\dfrac{H_{\mathrm{в}}^0\,t_{\mathrm{г.в}}}{2610-0{,}25\,t_{\mathrm{г.в}}}=\dfrac{%s\cdot %d}{2610-0{,}25\cdot %d}=%s'%(n(G['Hv'],0),round(R['tgv']),round(R['tgv']),n(R['H0gv'],2))+KJ
    E[52]=r'H_{\mathrm{х.в}}^0=1{,}313\,V_{\mathrm{в}}^0\,t_{\mathrm{х.в}}=1{,}313\cdot %s\cdot %d=%s'%(n(G['V0'],2),R['txv'],n(R['H0xv'],2))+KJ
    E[53]=r'Q_{\mathrm{в}}=\beta_{\mathrm{г.в}}H_{\mathrm{г.в}}^0+(\Delta\alpha_{\mathrm{т}}+\Delta\alpha_{\mathrm{пл}})H_{\mathrm{х.в}}^0=1{,}02\cdot %s+0{,}03\cdot %s'%(n(R['H0gv'],2),n(R['H0xv'],2))
    E[54]=r'=%s'%n(R['Qv'],2)+KJ
    E[55]=r'H_0^{\mathrm{рц}}=H_{\mathrm{г}}^0+(\alpha_{\mathrm{рц}}-1)H_{\mathrm{в}}^0=%s+(1{,}16-1)\cdot %s'%(n(G['Hg'],0),n(G['Hv'],0))
    E[56]=r'=%s'%n(R['H0rc'],1)+KJ
    E[57]=r'H_{\mathrm{рц}}=\dfrac{H_0^{\mathrm{рц}}\vartheta_{\mathrm{рц}}}{2695-0{,}3\,\vartheta_{\mathrm{рц}}}=\dfrac{%s\cdot %d}{2695-0{,}3\cdot %d}=%s'%(n(R['H0rc'],1),round(R['trc']),round(R['trc']),n(R['Hrc'],2))+KJ
    E[59]=r'=\dfrac{%s(100-0{,}15)}{100}+%s+%s\cdot %s'%(n(R['Q'],0),n(R['Qv'],2),n(R['r'],2),n(R['Hrc'],2))
    E[60]=r'=%s'%n(R['Qt'],2)+KJ
    E[62]=r'=(%s+(1{,}05-1)\cdot %s)(1+%s)=%s'%(n(G['Hg'],0),n(G['Hv'],0),n(R['r'],2),n(R['H0t'],1))+KJ
    E[63]=r'\vartheta_{\mathrm{а}}=2050\left(\dfrac{Q_{\mathrm{т}}}{H_0^{\mathrm{т}}}+0{,}075\right)=2050\left(\dfrac{%s}{%s}+0{,}075\right)'%(n(R['Qt'],2),n(R['H0t'],1))
    E[64]=r'=%s'%n(R['tha'],2)+DEG
    E[65]=r'q_F=\dfrac{BQ_{\mathrm{т}}}{F_{\mathrm{т}}}=\dfrac{%s\cdot %s}{1\ 861{,}9}=%s\ \mathrm{МВт/м}^2'%(n(R['B'],3),n(R['Qt']/1000,3),n(R['qF'],4))
    def iters(i,b):
        th=i['th']
        E[b]=r'k_{\mathrm{г.г}}=k^{\prime}{}_{\mathrm{г}}\left(\dfrac{4}{s}\right)^{0{,}54}\dfrac{1470}{\vartheta^{\prime\prime}{}_{\mathrm{т}}+273}=1{,}18\left(\dfrac{4}{8{,}913}\right)^{0{,}54}\dfrac{1470}{%s+273}'%n(th,0)
        E[b+1]=r'=%s\ 1/(\mathrm{м}\cdot\mathrm{МПа})'%n(i['kgg'],3)
        E[b+2]=r'k_{\mathrm{с}}=0{,}55\left(\dfrac{\vartheta^{\prime\prime}{}_{\mathrm{т}}+273}{1470}\right)^{1{,}33}\dfrac{k_{\mathrm{у}}}{\alpha_{\mathrm{т}}}=0{,}55\left(\dfrac{%s+273}{1470}\right)^{1{,}33}\dfrac{2{,}9}{1{,}05}'%n(th,0)
        E[b+3]=r'=%s\ 1/(\mathrm{м}\cdot\mathrm{МПа})'%n(i['kc'],3)
        E[b+4]=r'k_2=k_{\mathrm{г.г}}+k_{\mathrm{с}}=%s+%s=%s\ 1/(\mathrm{м}\cdot\mathrm{МПа})'%(n(i['kgg'],3),n(i['kc'],3),n(i['k2'],3))
    iters(i1,72)
    E[78]=r'=0{,}105(1-e^{-%s\cdot 0{,}1\cdot 8{,}913})+0{,}895(1-e^{-%s\cdot 0{,}1\cdot 8{,}913})=%s'%(n(i1['k2'],3),n(i1['kgg'],3),n(i1['ef'],4))
    E[79]=r'\varepsilon_{\mathrm{т}}=\dfrac{\varepsilon_{\mathrm{ф}}}{\varepsilon_{\mathrm{ф}}+(1-\varepsilon_{\mathrm{ф}})\psi_{\mathrm{т}}}=\dfrac{%s}{%s+(1-%s)\cdot 0{,}6124}=%s'%(n(i1['ef'],4),n(i1['ef'],4),n(i1['ef'],4),n(i1['et'],4))
    E[80]=r'm_{\mathrm{т}}=\dfrac{\varepsilon_{\mathrm{т}}\psi_{\mathrm{т}}(\vartheta_{\mathrm{а}}+273)^2}{9800\,q_F\cdot 1000}=\dfrac{%s\cdot 0{,}6124(%s+273)^2}{9800\cdot %s\cdot 1000}=%s'%(n(i1['et'],4),n(R['tha'],2),n(R['qF'],4),n(i1['mt'],4))
    E[82]=r'=(%s+273)(1-%s\cdot %s^{0{,}6})-273=%s'%(n(R['tha'],2),n(R['M'],3),n(i1['mt'],4),n(i1['tc'],2))+DEG
    if len(it)>1:
        i2=it[1]; iters(i2,83)
        E[88]=r'=0{,}105(1-e^{-%s\cdot 0{,}1\cdot 8{,}913})+0{,}895(1-e^{-%s\cdot 0{,}1\cdot 8{,}913})=%s'%(n(i2['k2'],3),n(i2['kgg'],3),n(i2['ef'],4))
        E[89]=E[79].replace(n(i1['ef'],4),n(i2['ef'],4)).replace(n(i1['et'],4),n(i2['et'],4))
        E[90]=r'm_{\mathrm{т}}=\dfrac{\varepsilon_{\mathrm{т}}\psi_{\mathrm{т}}(\vartheta_{\mathrm{а}}+273)^2}{9800\,q_F\cdot 1000}=\dfrac{%s\cdot 0{,}6124(%s+273)^2}{9800\cdot %s\cdot 1000}=%s'%(n(i2['et'],4),n(R['tha'],2),n(R['qF'],4),n(i2['mt'],4))
        E[91]=r'=(%s+273)(1-%s\cdot %s^{0{,}6})-273=%s'%(n(R['tha'],2),n(R['M'],3),n(i2['mt'],4),n(i2['tc'],2))+DEG
    E[92]=r'H^{\prime\prime}{}_{\mathrm{т}}=H_0^{\mathrm{т}}\left(\dfrac{\vartheta^{\prime\prime}{}_{\mathrm{т}}}{2050}-0{,}075\right)=%s\left(\dfrac{%s}{2050}-0{,}075\right)'%(n(R['H0t'],1),n(R['tht'],2))
    E[93]=r'=%s'%n(R['Ht'],2)+KJ
    E[94]=r'\varphi_{\mathrm{тепл}}=1-\dfrac{q_5}{q_5+\eta_{\mathrm{к}}}=1-\dfrac{0{,}2}{0{,}2+%s}=%s'%(n(R['eta'],3),n(R['phi'],4))
    E[95]=r'Q_{\mathrm{л}}=(Q_{\mathrm{т}}-H^{\prime\prime}{}_{\mathrm{т}})\,\varphi_{\mathrm{тепл}}=(%s-%s)\cdot %s'%(n(R['Qt'],2),n(R['Ht'],2),n(R['phi'],4))
    E[96]=r'=%s'%n(R['Ql'],2)+KJ
    E[97]=r'q_{\mathrm{л}}=\dfrac{BQ_{\mathrm{л}}}{\chi F_{\mathrm{т}}}=\dfrac{%s\cdot %s}{0{,}99\cdot 1\ 861{,}9}=%s\ \mathrm{кВт/м}^2'%(n(R['B'],3),n(R['Ql'],2),n(R['ql'],2))
    E[98]=r'q_V=\dfrac{BQ_{\mathrm{н}}^{\mathrm{р}}}{V_{\mathrm{т}}}=\dfrac{%s\cdot %s}{4\ 925}=%s\ \mathrm{кВт/м}^3'%(n(R['B'],3),n(R['Q'],0),n(R['qV'],1))
    E[100]=r'q_f=\dfrac{BQ_{\mathrm{н}}^{\mathrm{р}}}{f_{\mathrm{т}}}=\dfrac{%s\cdot %s}{147{,}39}=%s\ \mathrm{кВт/м}^2'%(n(R['B'],3),n(R['Q'],0),n(R['qf'],0))
    E[105]=r'=%s+\dfrac{%s\cdot %s(1+0{,}135)}{257{,}0}\cdot 0{,}95'%(n(R['hnk'],2),n(R['B'],3),n(R['Ql'],2))
    E[106]=r'=%s'%n(R['hT'],2)+KJKG
    E[112]=r'\beta^{\prime}{}_{\mathrm{ш}}=\dfrac{A}{\vartheta^{\prime\prime}{}_{\mathrm{т}}}=\dfrac{700}{%s}=%s'%(n(R['tht'],2),n(R['bsh'],4))
    E[114]=r'Q_{\mathrm{лш}}=\dfrac{q_{\mathrm{л}}\beta^{\prime}{}_{\mathrm{ш}}\eta_{\mathrm{в}}\varphi_{\mathrm{ш}}F^{\prime}{}_{\mathrm{ш}}}{B}=\dfrac{%s\cdot %s\cdot 0{,}8\cdot 0{,}9155\cdot 224{,}3}{%s}'%(n(R['ql'],2),n(R['bsh'],4),n(R['B'],3))
    E[115]=r'=%s'%n(R['Qlsh'],2)+KJ
    E[118]=r'h^{\prime}{}_{\mathrm{шпп}}=h^{\prime\prime}{}_{\mathrm{т}}-\Delta h_{\mathrm{впр1}}=%s-78{,}86=%s'%(n(R['hT'],2),n(R['hsh1'],2))+KJKG
    E[121]=r'\vartheta^{\prime\prime}{}_{\mathrm{ш}}=\vartheta^{\prime\prime}{}_{\mathrm{т}}-\Delta\vartheta_{\mathrm{рш}}=%s-%d=%s'%(n(R['tht'],2),sh['dth'],n(sh['th2'],2))+DEG
    E[122]=r'\vartheta_{\mathrm{шср}}=\dfrac{\vartheta^{\prime\prime}{}_{\mathrm{т}}+\vartheta^{\prime\prime}{}_{\mathrm{ш}}}{2}=\dfrac{%s+%s}{2}=%s'%(n(R['tht'],2),n(sh['th2'],2),n(sh['thc'],2))+DEG
    E[123]=r'H^{\prime\prime}{}_{\mathrm{ш}}=\dfrac{H_0^{\mathrm{т}}\vartheta^{\prime\prime}{}_{\mathrm{ш}}}{2695-0{,}3\,\vartheta^{\prime\prime}{}_{\mathrm{ш}}}=\dfrac{%s\cdot %s}{2695-0{,}3\cdot %s}=%s'%(n(R['H0t'],1),n(sh['th2'],2),n(sh['th2'],2),n(sh['H2'],2))+KJ
    E[124]=r'Q_{\mathrm{шб}}=(H^{\prime\prime}{}_{\mathrm{т}}-H^{\prime\prime}{}_{\mathrm{ш}})\dfrac{z_{\mathrm{ш}}}{z_{\mathrm{ш}}+2}=(%s-%s)\dfrac{20}{20+2}'%(n(R['Ht'],2),n(sh['H2'],2))
    E[125]=r'=%s'%n(sh['Qsb'],2)+KJ
    E[126]=r'\Delta h_{\mathrm{ш}}=\dfrac{B(Q_{\mathrm{лш}}+Q_{\mathrm{шб}})}{D_{\mathrm{ш}}}=\dfrac{%s(%s+%s)}{269{,}6}'%(n(R['B'],3),n(R['Qlsh'],2),n(sh['Qsb'],2))
    E[127]=r'=%s'%n(sh['dh'],2)+KJKG
    E[128]=r'h^{\prime\prime}{}_{\mathrm{ш}}=h^{\prime}{}_{\mathrm{шпп}}+\Delta h_{\mathrm{ш}}=%s+%s=%s'%(n(R['hsh1'],2),n(sh['dh'],2),n(sh['h2'],2))+KJKG
    E[134]=r'\Delta t_{\mathrm{ш}}=\vartheta_{\mathrm{шср}}-0{,}5(t^{\prime}{}_{\mathrm{ш}}+t^{\prime\prime}{}_{\mathrm{ш}})=%s-0{,}5(%s+%s)'%(n(sh['thc'],2),n(R['tsh1'],2),n(sh['t2'],2))
    E[135]=r'=%s'%n(sh['dt'],2)+DEG
    E[136]=r'V_{\mathrm{г}}=(V_{\mathrm{г}}^0+(\alpha_{\mathrm{т}}-1)V_{\mathrm{в}}^0)(1+r_{\mathrm{г}})=(%s+(1{,}05-1)\cdot %s)(1+%s)'%(n(G['V0g'],2),n(G['V0'],2),n(R['r'],2))
    E[137]=r'=%s\ \mathrm{м}^3/\mathrm{м}^3'%n(R['Vg'],3)
    E[140]=r'=\dfrac{%s\cdot %s}{17{,}32(8{,}1+4{,}848)\cdot 0{,}9612}\cdot\dfrac{%s+273}{273}=%s\ \mathrm{м/с}'%(n(R['B'],3),n(R['Vg'],3),n(sh['thc'],2),n(sh['w'],2))
    E[142]=r'=\dfrac{71(%s+273)(1+0{,}3(%s/7)^{0{,}5})}{1400}=%s\ \mathrm{Вт/(м}^2\cdot\mathrm{К)}'%(n(R['tht'],2),n(sh['w'],2),n(sh['k'],2))
    E[144]=r'Q_{\mathrm{шт}}=\dfrac{k_{\mathrm{ш}}\Delta t_{\mathrm{ш}}F_{\mathrm{ш.то}}}{B\cdot 10^3}=\dfrac{%s\cdot %s\cdot 1\ 041{,}4}{%s\cdot 10^3}=%s'%(n(sh['k'],2),n(sh['dt'],2),n(R['B'],3),n(sh['Qst'],2))+KJ
    E[145]=r'm=\dfrac{Q_{\mathrm{шт}}-Q_{\mathrm{шб}}}{Q_{\mathrm{шт}}}=\dfrac{%s-%s}{%s}=%s'%(n(sh['Qst'],2),n(sh['Qsb'],2),n(sh['Qst'],2),n(sh['m'],4))
    E[146]=r"Q^{\prime}{}_{\mathrm{шб}}=Q_{\mathrm{шт}}(1-0{,}1m)=%s(1-0{,}1\cdot %s)"%(n(sh['Qst'],2),n(sh['m'],4))
    E[147]=r'=%s'%n(R['Qsb2'],2)+KJ
    E[148]=r'H^{\prime\prime}{}_{\mathrm{ш}}=H^{\prime\prime}{}_{\mathrm{т}}-Q^{\prime}{}_{\mathrm{шб}}\dfrac{z_{\mathrm{ш}}+2}{z_{\mathrm{ш}}}=%s-%s\dfrac{20+2}{20}'%(n(R['Ht'],2),n(R['Qsb2'],2))
    E[149]=r'=%s'%n(R['H2b'],2)+KJ
    E[150]=r'\vartheta^{\prime\prime}{}_{\mathrm{ш}}=\dfrac{2695\,H^{\prime\prime}{}_{\mathrm{ш}}/H_0^{\mathrm{т}}}{1+0{,}3\,H^{\prime\prime}{}_{\mathrm{ш}}/H_0^{\mathrm{т}}}=\dfrac{2695\cdot %s/%s}{1+0{,}3\cdot %s/%s}'%(n(R['H2b'],2),n(R['H0t'],1),n(R['H2b'],2),n(R['H0t'],1))
    E[151]=r'=%s'%n(R['th2b'],2)+DEG
    E[153]=r'=%s+\dfrac{%s(%s+%s)}{269{,}6}=%s'%(n(R['hsh1'],2),n(R['B'],3),n(R['Qlsh'],2),n(R['Qsb2'],2),n(R['h2b'],2))+KJKG
    E[154]=r'Q_{\mathrm{лвых}}=\dfrac{Q_{\mathrm{лш}}(1-\varphi_{\mathrm{ш}})}{\varphi_{\mathrm{ш}}}=\dfrac{%s(1-0{,}9155)}{0{,}9155}=%s'%(n(R['Qlsh'],2),n(R['Qlvyh'],2))+KJ
    E[155]=r'\vartheta^{\prime}{}_{\mathrm{кпвд}}=\vartheta^{\prime\prime}{}_{\mathrm{ш}}-\Delta\vartheta_{\mathrm{пк}}=%s-50=%s'%(n(R['th2b'],2),n(R['th1k'],2))+DEG
    E[156]=r'H^{\prime}{}_{\mathrm{кпвд}}=\dfrac{H_0^{\mathrm{т}}\vartheta^{\prime}{}_{\mathrm{кпвд}}}{2695-0{,}3\,\vartheta^{\prime}{}_{\mathrm{кпвд}}}=\dfrac{%s\cdot %s}{2695-0{,}3\cdot %s}'%(n(R['H0t'],1),n(R['th1k'],2),n(R['th1k'],2))
    E[157]=r'=%s'%n(R['H1k'],2)+KJ
    E[158]=r'Q_{\mathrm{пк}}=H^{\prime\prime}{}_{\mathrm{ш}}-H^{\prime}{}_{\mathrm{кпвд}}=%s-%s=%s'%(n(R['H2b'],2),n(R['H1k'],2),n(R['Qpk'],2))+KJ
    E[161]=r'h^{\prime}{}_{\mathrm{кпвд}}=h^{\prime\prime}{}_{\mathrm{ш}}-\Delta h_{\mathrm{впр2}}=%s-52{,}58=%s'%(n(R['h2b'],2),n(R['hk1'],2))+KJKG
    E[162]=r'Q_{\mathrm{кпвд}}=\dfrac{D_{\mathrm{п}}(h^{\prime\prime}{}_{\mathrm{кпвд}}-h^{\prime}{}_{\mathrm{кпвд}})}{B_{\mathrm{р}}}=\dfrac{278(3\ 323{,}02-%s)}{%s}'%(n(R['hk1'],2),n(R['B'],3))
    E[163]=r'=%s'%n(R['Qk'],2)+KJ
    E[165]=r'=%s-%s(1+0{,}03)=%s'%(n(R['H1k'],2),n(R['Qk'],2),n(R['H2k'],2))+KJ
    E[167]=r'=(%s+(1{,}08-1)\cdot %s)(1+%s)=%s'%(n(G['Hg'],0),n(G['Hv'],0),n(R['r'],2),n(R['H0k'],1))+KJ
    E[168]=r'\vartheta^{\prime\prime}{}_{\mathrm{кпвд}}=\dfrac{2695\,H^{\prime\prime}{}_{\mathrm{кпвд}}/H_0^{\mathrm{кпвд}}}{1+0{,}3\,H^{\prime\prime}{}_{\mathrm{кпвд}}/H_0^{\mathrm{кпвд}}}=\dfrac{2695\cdot %s}{1+0{,}3\cdot %s}=%s'%(n(R['xk'],5),n(R['xk'],5),n(R['th2k'],2))+DEG
    E[173]=r'\Delta t_{\mathrm{б}}=\vartheta^{\prime}{}_{\mathrm{кпвд}}-t^{\prime}{}_{\mathrm{кпвд}}=%s-%s=%s'%(n(R['th1k'],2),n(R['tk1'],2),n(kp['db'],2))+DEG
    E[174]=r'\Delta t_{\mathrm{м}}=\vartheta^{\prime\prime}{}_{\mathrm{кпвд}}-t^{\prime\prime}{}_{\mathrm{кпвд}}=%s-545=%s'%(n(R['th2k'],2),n(kp['dm'],2))+DEG
    E[175]=r'\Delta t_{\mathrm{кпвд}}=\dfrac{\Delta t_{\mathrm{б}}-\Delta t_{\mathrm{м}}}{\ln(\Delta t_{\mathrm{б}}/\Delta t_{\mathrm{м}})}=\dfrac{%s-%s}{\ln(%s/%s)}=%s'%(n(kp['db'],2),n(kp['dm'],2),n(kp['db'],2),n(kp['dm'],2),n(kp['dt'],2))+DEG
    E[176]=r'\bar{\vartheta}_{\mathrm{кпвд}}=0{,}5(\vartheta^{\prime}{}_{\mathrm{кпвд}}+\vartheta^{\prime\prime}{}_{\mathrm{кпвд}})=0{,}5(%s+%s)=%s'%(n(R['th1k'],2),n(R['th2k'],2),n(kp['thc'],2))+DEG
    E[179]=r'=(%s+(1{,}065-1)\cdot %s)(1+%s)=%s\ \mathrm{м}^3/\mathrm{м}^3'%(n(G['V0g'],2),n(G['V0'],2),n(R['r'],2),n(kp['Vk'],3))
    E[182]=r'w_{\mathrm{кпвд}}^{\mathrm{г}}=\dfrac{B_{\mathrm{р}}V_{\mathrm{кпвд}}^{\mathrm{г}}(\bar{\vartheta}_{\mathrm{кпвд}}+273)}{273\,F_{\mathrm{кпвд}}^{\mathrm{г}}}=\dfrac{%s\cdot %s(%s+273)}{273\cdot 100{,}49}'%(n(R['B'],3),n(kp['Vk'],3),n(kp['thc'],2))
    E[183]=r'=%s\ \mathrm{м/с}'%n(kp['w'],2)
    E[185]=r'=0{,}86\cdot 1{,}03\cdot 100\left(\dfrac{%s}{9}\right)^{0{,}5}\cdot 1\cdot\left(\dfrac{4{,}358}{2{,}5}\right)^{0{,}15}'%n(kp['w'],2)
    E[186]=r'=%s\ \mathrm{Вт/(м}^2\cdot\mathrm{К)}'%n(kp['k'],2)
    E[187]=r'q_{\mathrm{кпвд}}=\dfrac{k_{\mathrm{кпвд}}\Delta t_{\mathrm{кпвд}}}{1000}=\dfrac{%s\cdot %s}{1000}=%s\ \mathrm{кВт/м}^2'%(n(kp['k'],2),n(kp['dt'],2),n(kp['q'],3))
    E[188]=r'F_{\mathrm{кпвд}}=\dfrac{B_{\mathrm{р}}Q_{\mathrm{кпвд}}}{q_{\mathrm{кпвд}}}=\dfrac{%s\cdot %s}{%s}=%s\ \mathrm{м}^2'%(n(R['B'],3),n(R['Qk'],2),n(kp['q'],3),n(kp['F'],1))
    E[190]=r'z_{\mathrm{р}}=\dfrac{F_{\mathrm{кпвд}}}{F_{\mathrm{кпвд}}^1}=\dfrac{%s}{92{,}28}=%s\approx %d'%(n(kp['F'],1),n(kp['zrr'],2),kp['zr'])
    E[191]=r'z_{\mathrm{пет}}=\dfrac{z_{\mathrm{р}}}{n_2}=\dfrac{%d}{6}=%s'%(kp['zr'],n(kp['zp'],2))
    E[193]=r'=(%d-1)\cdot 0{,}054+0{,}032+0{,}070(%s+1)=%s\ \mathrm{м}'%(kp['zr'],n(kp['zp'],2),n(kp['lp'],3))
    E[194]=r"F^{\prime}{}_{\mathrm{кпвд}}=F_{\mathrm{кпвд}}^1z_{\mathrm{р}}=92{,}28\cdot %d=%s\ \mathrm{м}^2"%(kp['zr'],n(kp['Fp'],1))
    E[195]=r"\delta F=\dfrac{F_{\mathrm{кпвд}}-F^{\prime}{}_{\mathrm{кпвд}}}{F_{\mathrm{кпвд}}}100=\dfrac{%s-%s}{%s}100=%s\ \%%"%(n(kp['F'],1),n(kp['Fp'],1),n(kp['F'],1),n(kp['dF'],2))
    E[196]=r"Q_{\mathrm{кпвд}}^{\mathrm{р}}=\dfrac{k_{\mathrm{кпвд}}\Delta t_{\mathrm{кпвд}}F^{\prime}{}_{\mathrm{кпвд}}}{B_{\mathrm{р}}\cdot 1000}=\dfrac{%s\cdot %s\cdot %s}{%s\cdot 1000}"%(n(kp['k'],2),n(kp['dt'],2),n(kp['Fp'],1),n(R['B'],3))
    E[197]=r'=%s'%n(kp['Qr'],2)+KJ
    E[198]=r"\delta Q=\dfrac{Q_{\mathrm{кпвд}}^{\mathrm{р}}-Q_{\mathrm{кпвд}}}{Q_{\mathrm{кпвд}}^{\mathrm{р}}}100=\dfrac{%s-%s}{%s}100=%s\ \%%"%(n(kp['Qr'],2),n(R['Qk'],2),n(kp['Qr'],2),n(kp['dQ'],2))
    return E
