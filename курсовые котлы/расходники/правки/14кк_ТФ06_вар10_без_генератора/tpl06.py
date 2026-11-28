import math
def n(v,d):
    s=f'{float(v):,.{d}f}'; return s.replace(',','X').replace('.','{,}').replace('X','\\ ')
D=r'\ ^{\circ}\;\mathrm{C}'
KJ=r'\ \mathrm{кДж/кг}'
rm=lambda s: r'\mathrm{'+s+'}'
def vals(R):
    V={}
    def put(k,v,d): V[k]=n(v,d)
    i1,i2=R['its'][0],R['its'][-1]; sh=R['sh']; kp=R['kp']
    for k,d in [('r',2),('Qt',2),('H0t',1),('tha',2),('qF',2),('tht',2),('Ht',2),('Ql',2),('hT',2),('tT',2),('thg',2),('trs',2),('dtT',2),('ql',2),('kT',2),('wT',2),
                ('Qshl',2),('hsh1',2),('tsh1',2),('tk1',2),('te2',2),('Vg',3),('Qlv',2),('th1k',2),('H1k',2),('Qpk',2),('hk1',2),('Qk',2),('H2k',2),('H0k',1),('xk',5),('th2k',2),
                ('H2n',2),('H0n',1),('th2n',2),('thcn',2),('Vn',3),('wn',2),('dbn',2),('dmn',2),('dtn',2),('kn',2),('qn',3),('Fn',0),
                ('H2e',2),('Qe',2),('he2',2),('H0e',1),('th2e',2),('thce',2),('Ve',3),('we',2),('dbe',2),('dme',2),('dte',2),('ke',2),('qe',3),('Fe_',1),('zre',0),('zpe',3),('lpe',3),('Qer',2),('dQe',2),
                ('H1v',2),('Qvp',2),('H0gv2',2),('tgv',2),('dmv',2),('dtv',2),('thcv',2),('tcv',2),('wgr',3),('wvr',3),('ag',3),('av',3),('kv',3),('Fv',0),('Hvp',3),('qvp',4)]:
        put(k,R[k],d)
    V['xn']=n(R['H2n']/R['H0n'],5); V['xe']=n(R['H2e']/R['H0e'],5)
    for p,i in (('a',i1),('b',i2)):
        for k,d in [('th',0),('b',4),('psh',4),('psi',4),('kg',3),('kc',3),('k2',3),('af',4),('at',4),('mt',4),('tc',2)]: V[p+k]=n(i[k],d)
    for k,d in [('dth',0),('dr',2),('th2',2),('H2',2),('Qb',2),('dh',2),('h2',2),('t2',2),('thc',2),('tc',2),('dt',2),('w',2),('k',2),('Qt',2),('dQ',2)]: V['s'+k]=n(sh[k],d)
    for k,d in [('n1',0),('s1',4),('fp',4),('wr',0),('db',2),('dm',2),('dt',2),('thc',2),('Vk',3),('kz',4),('Fg',2),('w',2),('sig',3),('k',2),('q',3),('F',1),('F1',2),('zr',0),('zrr',2),('zp',2),('lp',3),('Fp',1),('dF',2),('Qr',2),('dQ',2)]: V['k'+k]=n(kp[k],d)
    V['ks1mm']=n(kp['s1mm']/1000,3); V['kn1r']=n(7.53/(kp['s1mm']/1000)-1,2)
    V['zreR']=n(R['Fe_']/R['F1e'],2)
    return V
T={}
T[57]=r'=\dfrac{39\ 026(100-0{,}1)}{100}+4\ 117{,}32+%(r)s\cdot 6\ 190{,}08=%(Qt)s'+KJ
T[58]=r'H_0^{\mathrm{т}}=(H_{\mathrm{г}}^0+(\alpha_{\mathrm{т}}-1)H_{\mathrm{в}}^0)(1+r_{\mathrm{г}})=(40\ 950+(1{,}03-1)\cdot 34\ 690)(1+%(r)s)'
T[59]=r'=%(H0t)s'+KJ
T[60]=r'\vartheta_{\mathrm{а}}=2050\left(\dfrac{Q_{\mathrm{т}}}{H_0^{\mathrm{т}}}+0{,}075\right)=2050\left(\dfrac{%(Qt)s}{%(H0t)s}+0{,}075\right)=%(tha)s'+D
T[61]=r'q_F=\dfrac{B_{\mathrm{р}}Q_{\mathrm{т}}}{F_{\mathrm{э}}}=\dfrac{20{,}046\cdot %(Qt)s}{1\ 695{,}4}=%(qF)s\ \mathrm{кВт/м}^2'
T[78]=r'm_{\mathrm{т}}=\dfrac{a_{\mathrm{т}}\psi_{\mathrm{т}}(\vartheta_{\mathrm{а}}+273)^2}{9800\,q_F}=\dfrac{%(aat)s\cdot %(apsi)s(%(tha)s+273)^2}{9800\cdot %(qF)s}=%(amt)s'
T[80]=r'=(%(tha)s+273)(1-0{,}503\cdot %(amt)s^{0{,}6})-273=%(atc)s'+D
T[81]=r'\beta_{\mathrm{ш}}=\left(\dfrac{A}{\vartheta^{\prime\prime}{}_{\mathrm{т}}}\right)^{1{,}2}=\left(\dfrac{900}{%(bth)s}\right)^{1{,}2}=%(bb)s'
T[82]=r'\psi_{\mathrm{ш}}=\beta_{\mathrm{ш}}\xi=%(bb)s\cdot 0{,}55=%(bpsh)s'
T[83]=r'=\dfrac{0{,}5397\cdot 1\ 695{,}4+0{,}4857\cdot 148{,}1+%(bpsh)s\cdot 140{,}6}{2\ 001{,}2}=%(bpsi)s'
T[84]=r'k_{\mathrm{г}}=k^{\prime}{}_{\mathrm{г}}\left(\dfrac{4}{S_{\mathrm{т}}}\right)^{0{,}54}\dfrac{1470}{\vartheta^{\prime\prime}{}_{\mathrm{т}}+273}=1{,}02\left(\dfrac{4}{8{,}85}\right)^{0{,}54}\dfrac{1470}{%(bth)s+273}'
T[85]=r'=%(bkg)s\ 1/(\mathrm{м}\cdot\mathrm{МПа})'
T[86]=r'k_{\mathrm{с}}=0{,}55\left(\dfrac{\vartheta^{\prime\prime}{}_{\mathrm{т}}+273}{1470}\right)^{1{,}33}\dfrac{k_{\mathrm{у}}}{\alpha_{\mathrm{т}}}=0{,}55\left(\dfrac{%(bth)s+273}{1470}\right)^{1{,}33}\dfrac{8{,}0}{1{,}03}'
T[87]=r'=%(bkc)s\ 1/(\mathrm{м}\cdot\mathrm{МПа})'
T[88]=r'k_2=k_{\mathrm{г}}+k_{\mathrm{с}}=%(bkg)s+%(bkc)s=%(bk2)s\ 1/(\mathrm{м}\cdot\mathrm{МПа})'
T[89]=r'=0{,}612(1-e^{-%(bk2)s\cdot 0{,}1\cdot 8{,}85})+0{,}388(1-e^{-%(bkg)s\cdot 0{,}1\cdot 8{,}85})=%(baf)s'
T[90]=r'a_{\mathrm{т}}=\dfrac{a_{\mathrm{ф}}}{a_{\mathrm{ф}}+(1-a_{\mathrm{ф}})\psi_{\mathrm{т}}}=\dfrac{%(baf)s}{%(baf)s+(1-%(baf)s)\cdot %(bpsi)s}=%(bat)s'
T[91]=r'm_{\mathrm{т}}=\dfrac{a_{\mathrm{т}}\psi_{\mathrm{т}}(\vartheta_{\mathrm{а}}+273)^2}{9800\,q_F}=\dfrac{%(bat)s\cdot %(bpsi)s(%(tha)s+273)^2}{9800\cdot %(qF)s}=%(bmt)s'
T[92]=r'=(%(tha)s+273)(1-0{,}503\cdot %(bmt)s^{0{,}6})-273=%(btc)s'+D
T[93]=r'H^{\prime\prime}{}_{\mathrm{т}}=H_0^{\mathrm{т}}\left(\dfrac{\vartheta^{\prime\prime}{}_{\mathrm{т}}}{2050}-0{,}075\right)=%(H0t)s\left(\dfrac{%(tht)s}{2050}-0{,}075\right)'
T[94]=r'=%(Ht)s'+KJ
T[95]=r'Q_{\mathrm{л}}=Q_{\mathrm{т}}-H^{\prime\prime}{}_{\mathrm{т}}=%(Qt)s-%(Ht)s=%(Ql)s'+KJ
T[99]=r'h^{\prime\prime}{}_{\mathrm{т}}=h^{\prime\prime}{}_{\mathrm{эк}}+\dfrac{Q_{\mathrm{л}}B_{\mathrm{р}}(1+\Delta q_{\mathrm{доп}})}{D_{\mathrm{т}}}=1\ 406{,}06+\dfrac{%(Ql)s\cdot 20{,}046(1+0{,}075)}{266{,}0}'
T[100]=r'=%(hT)s'+KJ
T[101]=r'\bar{\vartheta}_{\mathrm{г}}=0{,}5(0{,}85\,\vartheta_{\mathrm{а}}+\vartheta^{\prime\prime}{}_{\mathrm{т}})=0{,}5(0{,}85\cdot %(tha)s+%(tht)s)=%(thg)s'+D
T[102]=r'\bar{t}_{\mathrm{рс}}=0{,}5(t^{\prime\prime}{}_{\mathrm{эк}}+t^{\prime\prime}{}_{\mathrm{т}})=0{,}5(315+%(tT)s)=%(trs)s'+D
T[103]=r'\Delta t=\bar{\vartheta}_{\mathrm{г}}-\bar{t}_{\mathrm{рс}}=%(thg)s-%(trs)s=%(dtT)s'+D
T[104]=r'q_{\mathrm{л}}=\dfrac{B_{\mathrm{р}}Q_{\mathrm{л}}}{\Sigma F_{\mathrm{т}}x_{\mathrm{э}}}=\dfrac{20{,}046\cdot %(Ql)s}{2\ 001{,}2\cdot 0{,}9812}=%(ql)s\ \mathrm{кВт/м}^2'
T[105]=r'k=\dfrac{q_{\mathrm{л}}}{\Delta t}=\dfrac{%(ql)s\cdot 10^3}{%(dtT)s}=%(kT)s\ \mathrm{Вт/(м}^2\cdot\mathrm{К)}'
T[108]=r'=5{,}248\cdot 0{,}3\cdot 1{,}03\dfrac{0{,}9(%(tha)s+273)+%(tht)s+273}{546}=%(wT)s\ \mathrm{м/с}'
T[113]=r'Q_{\mathrm{ш.л}}=\dfrac{\beta_{\mathrm{ш}}\eta_{\mathrm{в}}q_{\mathrm{л}}\varphi_{\mathrm{ш}}F_{\mathrm{ш.л}}}{B_{\mathrm{р}}}=\dfrac{%(bb)s\cdot 0{,}6\cdot %(ql)s\cdot 0{,}9177\cdot 170{,}9}{20{,}046}'
T[114]=r'=%(Qshl)s'+KJ
T[116]=r"h^{\prime}{}_{\mathrm{ш}}=h^{\prime\prime}{}_{\mathrm{т}}-\Delta h_{\mathrm{впр1}}=%(hT)s-45{,}06=%(hsh1)s"+KJ
T[117]=r'\Delta\vartheta_{\mathrm{ш}}^{\mathrm{р}}=\dfrac{1{,}5\,\Delta\vartheta_{\mathrm{ш}}}{(1+r_{\mathrm{г}})^{0{,}33}}=\dfrac{1{,}5\cdot %(sdth)s}{(1+%(r)s)^{0{,}33}}=%(sdr)s'+D
T[118]=r'\vartheta^{\prime\prime}{}_{\mathrm{ш}}=\vartheta^{\prime\prime}{}_{\mathrm{т}}-\Delta\vartheta_{\mathrm{ш}}^{\mathrm{р}}=%(tht)s-%(sdr)s=%(sth2)s'+D
T[119]=r'H^{\prime\prime}{}_{\mathrm{ш}}=H_0^{\mathrm{т}}\left(\dfrac{\vartheta^{\prime\prime}{}_{\mathrm{ш}}}{2050}-0{,}075\right)=%(H0t)s\left(\dfrac{%(sth2)s}{2050}-0{,}075\right)=%(sH2)s'+KJ
T[120]=r'Q_{\mathrm{ш.б}}=(H^{\prime\prime}{}_{\mathrm{т}}-H^{\prime\prime}{}_{\mathrm{ш}})\dfrac{z_{\mathrm{ш}}}{z_{\mathrm{ш}}+1}=(%(Ht)s-%(sH2)s)\dfrac{20}{21}'
T[121]=r'=%(sQb)s'+KJ
T[122]=r'\Delta h_{\mathrm{ш}}=\dfrac{B_{\mathrm{р}}(Q_{\mathrm{ш.л}}+Q_{\mathrm{ш.б}})}{D_{\mathrm{ш}}}=\dfrac{20{,}046(%(Qshl)s+%(sQb)s)}{273{,}2}=%(sdh)s'+KJ
T[123]=r"h^{\prime\prime}{}_{\mathrm{ш}}=h^{\prime}{}_{\mathrm{ш}}+\Delta h_{\mathrm{ш}}=%(hsh1)s+%(sdh)s=%(sh2)s"+KJ
T[124]=r'\bar{\vartheta}_{\mathrm{ш}}=0{,}5(\vartheta^{\prime\prime}{}_{\mathrm{т}}+\vartheta^{\prime\prime}{}_{\mathrm{ш}})=0{,}5(%(tht)s+%(sth2)s)=%(sthc)s'+D
T[125]=r"\bar{t}_{\mathrm{ш}}=0{,}5(t^{\prime}{}_{\mathrm{ш}}+t^{\prime\prime}{}_{\mathrm{ш}})=0{,}5(%(tsh1)s+%(st2)s)=%(stc)s"+D
T[126]=r'\Delta t_{\mathrm{ш}}=\bar{\vartheta}_{\mathrm{ш}}-\bar{t}_{\mathrm{ш}}=%(sthc)s-%(stc)s=%(sdt)s'+D
T[127]=r'V_{\mathrm{г}}=(V_{\mathrm{г}}^0+(\alpha_{\mathrm{т}}-1)V_{\mathrm{в}}^0)(1+r_{\mathrm{г}})=(10{,}99+(1{,}03-1)\cdot 10{,}20)(1+%(r)s)'
T[128]=r'=%(Vg)s\ \mathrm{м}^3/\mathrm{кг}'
T[130]=r'w_{\mathrm{г}}=\dfrac{B_{\mathrm{р}}V_{\mathrm{г}}(\bar{\vartheta}_{\mathrm{ш}}+273)}{273\,a_{\mathrm{т}}h_{\mathrm{ш}}k_{\mathrm{ж}}}=\dfrac{20{,}046\cdot %(Vg)s(%(sthc)s+273)}{273\cdot 17{,}36\cdot 8{,}1\cdot 0{,}9613}=%(sw)s\ \mathrm{м/с}'
T[132]=r'=\dfrac{43(%(tht)s+273)}{1400}\left(1+0{,}4\left(\dfrac{%(sw)s}{7}\right)^{0{,}5}\right)=%(sk)s\ \mathrm{Вт/(м}^2\cdot\mathrm{К)}'
T[133]=r'Q_{\mathrm{ш.т}}=\dfrac{k_{\mathrm{ш}}\Delta t_{\mathrm{ш}}F_{\mathrm{ш}}}{B_{\mathrm{р}}\cdot 10^3}=\dfrac{%(sk)s\cdot %(sdt)s\cdot 1\ 108{,}9}{20{,}046\cdot 10^3}=%(sQt)s'+KJ
T[134]=r'\delta Q=\dfrac{Q_{\mathrm{ш.т}}-Q_{\mathrm{ш.б}}}{Q_{\mathrm{ш.т}}}100=\dfrac{%(sQt)s-%(sQb)s}{%(sQt)s}100=%(sdQ)s\ \%%'
T[135]=r'Q_{\mathrm{л.вых}}=\dfrac{Q_{\mathrm{ш.л}}(1-\varphi_{\mathrm{ш}})}{\varphi_{\mathrm{ш}}}=\dfrac{%(Qshl)s(1-0{,}9177)}{0{,}9177}=%(Qlv)s'+KJ
T[136]=r"\vartheta^{\prime}{}_{\mathrm{кпвд}}=\vartheta^{\prime\prime}{}_{\mathrm{ш}}-\Delta\vartheta_{\mathrm{пк}}=%(sth2)s-50=%(th1k)s"+D
T[137]=r"H^{\prime}{}_{\mathrm{кпвд}}=\dfrac{H_0^{\mathrm{т}}\vartheta^{\prime}{}_{\mathrm{кпвд}}}{2695-0{,}3\,\vartheta^{\prime}{}_{\mathrm{кпвд}}}=\dfrac{%(H0t)s\cdot %(th1k)s}{2695-0{,}3\cdot %(th1k)s}=%(H1k)s"+KJ
T[138]=r"Q_{\mathrm{пк}}=H^{\prime\prime}{}_{\mathrm{ш}}-H^{\prime}{}_{\mathrm{кпвд}}=%(sH2)s-%(H1k)s=%(Qpk)s"+KJ
T[140]=r"h^{\prime}{}_{\mathrm{кпвд}}=h^{\prime\prime}{}_{\mathrm{ш}}-\Delta h_{\mathrm{впр2}}=%(sh2)s-30{,}04=%(hk1)s"+KJ
T[141]=r"Q_{\mathrm{кпвд}}=\dfrac{D_{\mathrm{п}}(h^{\prime\prime}{}_{\mathrm{кпвд}}-h^{\prime}{}_{\mathrm{кпвд}})}{B_{\mathrm{р}}}=\dfrac{278(3\ 323{,}02-%(hk1)s)}{20{,}046}"
T[142]=r'=%(Qk)s'+KJ
T[143]=r"H^{\prime\prime}{}_{\mathrm{кпвд}}=H^{\prime}{}_{\mathrm{кпвд}}-Q_{\mathrm{кпвд}}(1+\Delta q_{\mathrm{доп}})=%(H1k)s-%(Qk)s(1+0{,}03)"
T[144]=r'=%(H2k)s'+KJ
T[146]=r'=(40\ 950+(1{,}06-1)\cdot 34\ 690)(1+%(r)s)=%(H0k)s'+KJ
T[147]=r"\vartheta^{\prime\prime}{}_{\mathrm{кпвд}}=\dfrac{2695\,H^{\prime\prime}{}_{\mathrm{кпвд}}/H_0^{\mathrm{кпвд}}}{1+0{,}3\,H^{\prime\prime}{}_{\mathrm{кпвд}}/H_0^{\mathrm{кпвд}}}=\dfrac{2695\cdot %(xk)s}{1+0{,}3\cdot %(xk)s}=%(th2k)s"+D
T[152]=r"\Delta t_{\mathrm{б}}=\vartheta^{\prime}{}_{\mathrm{кпвд}}-t^{\prime}{}_{\mathrm{кпвд}}=%(th1k)s-%(tk1)s=%(kdb)s"+D
T[153]=r"\Delta t_{\mathrm{м}}=\vartheta^{\prime\prime}{}_{\mathrm{кпвд}}-t^{\prime\prime}{}_{\mathrm{кпвд}}=%(th2k)s-545=%(kdm)s"+D
T[154]=r'\Delta t_{\mathrm{кпвд}}=\dfrac{\Delta t_{\mathrm{б}}-\Delta t_{\mathrm{м}}}{\ln(\Delta t_{\mathrm{б}}/\Delta t_{\mathrm{м}})}=\dfrac{%(kdb)s-%(kdm)s}{\ln(%(kdb)s/%(kdm)s)}=%(kdt)s'+D
T[155]=r"\bar{\vartheta}_{\mathrm{кпвд}}=0{,}5(\vartheta^{\prime}{}_{\mathrm{кпвд}}+\vartheta^{\prime\prime}{}_{\mathrm{кпвд}})=0{,}5(%(th1k)s+%(th2k)s)=%(kthc)s"+D
T[158]=r'=(10{,}99+(1{,}045-1)\cdot 10{,}20)(1+%(r)s)=%(kVk)s\ \mathrm{м}^3/\mathrm{кг}'
T[161]=r'w_{\mathrm{кпвд}}^{\mathrm{г}}=\dfrac{B_{\mathrm{р}}V_{\mathrm{кпвд}}^{\mathrm{г}}(\bar{\vartheta}_{\mathrm{кпвд}}+273)}{273\,F_{\mathrm{кпвд}}^{\mathrm{г}}}=\dfrac{20{,}046\cdot %(kVk)s(%(kthc)s+273)}{273\cdot %(kFg)s}'
T[162]=r'=%(kw)s\ \mathrm{м/с}'
T[164]=r'=0{,}86\cdot 1{,}03\cdot 74\left(\dfrac{%(kw)s}{9}\right)^{0{,}5}\cdot 1\cdot\left(\dfrac{%(ksig)s}{2{,}5}\right)^{0{,}15}=%(kk)s\ \mathrm{Вт/(м}^2\cdot\mathrm{К)}'
T[165]=r'q_{\mathrm{кпвд}}=\dfrac{k_{\mathrm{кпвд}}\Delta t_{\mathrm{кпвд}}}{1000}=\dfrac{%(kk)s\cdot %(kdt)s}{1000}=%(kq)s\ \mathrm{кВт/м}^2'
T[166]=r'F_{\mathrm{кпвд}}=\dfrac{B_{\mathrm{р}}Q_{\mathrm{кпвд}}}{q_{\mathrm{кпвд}}}=\dfrac{20{,}046\cdot %(Qk)s}{%(kq)s}=%(kF)s\ \mathrm{м}^2'
T[168]=r'z_{\mathrm{р}}=\dfrac{F_{\mathrm{кпвд}}}{F_{\mathrm{кпвд}}^1}=\dfrac{%(kF)s}{%(kF1)s}=%(kzrr)s\approx %(kzr)s'
T[169]=r'z_{\mathrm{пет}}=\dfrac{z_{\mathrm{р}}}{n_2}=\dfrac{%(kzr)s}{6}=%(kzp)s'
T[170]=r'l_{\mathrm{п}}=(z_{\mathrm{р}}-1)s_2+d+m_{\mathrm{г}}(z_{\mathrm{пет}}+1)=(%(kzr)s-1)\cdot 0{,}054+0{,}032+0{,}070(%(kzp)s+1)'
T[171]=r'=%(klp)s\ \mathrm{м}'
T[172]=r"F^{\prime}{}_{\mathrm{кпвд}}=F_{\mathrm{кпвд}}^1z_{\mathrm{р}}=%(kF1)s\cdot %(kzr)s=%(kFp)s\ \mathrm{м}^2"
T[173]=r"\delta F=\dfrac{F_{\mathrm{кпвд}}-F^{\prime}{}_{\mathrm{кпвд}}}{F_{\mathrm{кпвд}}}100=\dfrac{%(kF)s-%(kFp)s}{%(kF)s}100=%(kdF)s\ \%%"
T[174]=r"Q_{\mathrm{кпвд}}^{\mathrm{р}}=\dfrac{k_{\mathrm{кпвд}}\Delta t_{\mathrm{кпвд}}F^{\prime}{}_{\mathrm{кпвд}}}{B_{\mathrm{р}}\cdot 1000}=\dfrac{%(kk)s\cdot %(kdt)s\cdot %(kFp)s}{20{,}046\cdot 1000}=%(kQr)s"+KJ
T[175]=r'\delta Q=\dfrac{Q_{\mathrm{кпвд}}^{\mathrm{р}}-Q_{\mathrm{кпвд}}}{Q_{\mathrm{кпвд}}^{\mathrm{р}}}100=\dfrac{%(kQr)s-%(Qk)s}{%(kQr)s}100=%(kdQ)s\ \%%'
T[178]=r"H^{\prime\prime}{}_{\mathrm{кпнд}}=H^{\prime\prime}{}_{\mathrm{кпвд}}-Q_{\mathrm{кпнд}}(1+\Delta q_{\mathrm{доп}}^{\mathrm{вт}})=%(H2k)s-6\ 513{,}69(1+0{,}015)"
T[179]=r'=%(H2n)s'+KJ
T[181]=r'=(40\ 950+(1{,}12-1)\cdot 34\ 690)(1+%(r)s)=%(H0n)s'+KJ
T[182]=r"\vartheta^{\prime\prime}{}_{\mathrm{кпнд}}=\dfrac{2695\,H^{\prime\prime}{}_{\mathrm{кпнд}}/H_0^{\mathrm{кпнд}}}{1+0{,}3\,H^{\prime\prime}{}_{\mathrm{кпнд}}/H_0^{\mathrm{кпнд}}}=\dfrac{2695\cdot %(xn)s}{1+0{,}3\cdot %(xn)s}=%(th2n)s"+D
T[183]=r"\bar{\vartheta}_{\mathrm{кпнд}}=0{,}5(\vartheta^{\prime\prime}{}_{\mathrm{кпвд}}+\vartheta^{\prime\prime}{}_{\mathrm{кпнд}})=0{,}5(%(th2k)s+%(th2n)s)=%(thcn)s"+D
T[185]=r'V_{\mathrm{кпнд}}^{\mathrm{г}}=(V_{\mathrm{г}}^0+(\bar{\alpha}_{\mathrm{кпнд}}-1)V_{\mathrm{в}}^0)(1+r_{\mathrm{г}})=(10{,}99+(1{,}09-1)\cdot 10{,}20)(1+%(r)s)'
T[186]=r'=%(Vn)s\ \mathrm{м}^3/\mathrm{кг}'
T[189]=r'w_{\mathrm{кпнд}}^{\mathrm{г}}=\dfrac{B_{\mathrm{р}}V_{\mathrm{кпнд}}^{\mathrm{г}}(\bar{\vartheta}_{\mathrm{кпнд}}+273)}{273\,F_{\mathrm{кпнд}}^{\mathrm{г}}}=\dfrac{20{,}046\cdot %(Vn)s(%(thcn)s+273)}{273\cdot 91{,}50}'
T[190]=r'=%(wn)s\ \mathrm{м/с}'
T[191]=r"\Delta t_{\mathrm{б}}=\vartheta^{\prime\prime}{}_{\mathrm{кпвд}}-t^{\prime\prime}{}_{\mathrm{вт}}=%(th2k)s-545=%(dbn)s"+D
T[192]=r"\Delta t_{\mathrm{м}}=\vartheta^{\prime\prime}{}_{\mathrm{кпнд}}-t^{\prime}{}_{\mathrm{вт}}=%(th2n)s-310=%(dmn)s"+D
T[193]=r'\Delta t_{\mathrm{кпнд}}=\dfrac{\Delta t_{\mathrm{б}}-\Delta t_{\mathrm{м}}}{\ln(\Delta t_{\mathrm{б}}/\Delta t_{\mathrm{м}})}=\dfrac{%(dbn)s-%(dmn)s}{\ln(%(dbn)s/%(dmn)s)}=%(dtn)s'+D
T[195]=r'=0{,}86\cdot 1{,}03\cdot 69\left(\dfrac{%(wn)s}{9}\right)^{0{,}5}\left(\dfrac{0{,}032}{0{,}042}\right)^{0{,}35}\left(\dfrac{3{,}333}{2{,}5}\right)^{0{,}15}=%(kn)s\ \mathrm{Вт/(м}^2\cdot\mathrm{К)}'
T[196]=r'q_{\mathrm{кпнд}}=\dfrac{k_{\mathrm{кпнд}}\Delta t_{\mathrm{кпнд}}}{1000}=\dfrac{%(kn)s\cdot %(dtn)s}{1000}=%(qn)s\ \mathrm{кВт/м}^2'
T[197]=r'F_{\mathrm{кпнд}}=\dfrac{B_{\mathrm{р}}Q_{\mathrm{кпнд}}}{q_{\mathrm{кпнд}}}=\dfrac{20{,}046\cdot 6\ 513{,}69}{%(qn)s}=%(Fn)s\ \mathrm{м}^2'
T[201]=r"H^{\prime\prime}{}_{\mathrm{эк}}=Q_{\mathrm{т}}-Q_{\mathrm{р}}^{\mathrm{р}}\dfrac{\eta_{\mathrm{к}}}{100}=%(Qt)s-39\ 026\cdot 0{,}93623=%(H2e)s"+KJ
T[203]=r'=0{,}9979(%(H2n)s-%(H2e)s+0{,}02\cdot 399{,}88)=%(Qe)s'+KJ
T[204]=r"h^{\prime\prime}{}_{\mathrm{эк}}=h_{\mathrm{пв}}+\dfrac{B_{\mathrm{р}}Q_{\mathrm{эк}}}{D_{\mathrm{п}}-\Sigma D_{\mathrm{впр}}}=1\ 158{,}11+\dfrac{20{,}046\cdot %(Qe)s}{266}"
T[205]=r'=%(he2)s'+KJ
T[206]=r"H_0^{\mathrm{эк}}=(H_{\mathrm{г}}^0+(\alpha^{\prime\prime}{}_{\mathrm{эк}}-1)H_{\mathrm{в}}^0)(1+r_{\mathrm{г}})=(40\ 950+(1{,}14-1)\cdot 34\ 690)(1+%(r)s)"
T[207]=r'=%(H0e)s'+KJ
T[208]=r"\vartheta^{\prime\prime}{}_{\mathrm{эк}}=\dfrac{2695\,H^{\prime\prime}{}_{\mathrm{эк}}/H_0^{\mathrm{эк}}}{1+0{,}3\,H^{\prime\prime}{}_{\mathrm{эк}}/H_0^{\mathrm{эк}}}=\dfrac{2695\cdot %(xe)s}{1+0{,}3\cdot %(xe)s}=%(th2e)s"+D
T[209]=r"\bar{\vartheta}_{\mathrm{эк}}=0{,}5(\vartheta^{\prime\prime}{}_{\mathrm{кпнд}}+\vartheta^{\prime\prime}{}_{\mathrm{эк}})=0{,}5(%(th2n)s+%(th2e)s)=%(thce)s"+D
T[211]=r'V_{\mathrm{эк}}^{\mathrm{г}}=(V_{\mathrm{г}}^0+(\bar{\alpha}_{\mathrm{эк}}-1)V_{\mathrm{в}}^0)(1+r_{\mathrm{г}})=(10{,}99+(1{,}13-1)\cdot 10{,}20)(1+%(r)s)'
T[212]=r'=%(Ve)s\ \mathrm{м}^3/\mathrm{кг}'
T[215]=r'w_{\mathrm{эк}}^{\mathrm{г}}=\dfrac{B_{\mathrm{р}}V_{\mathrm{эк}}^{\mathrm{г}}(\bar{\vartheta}_{\mathrm{эк}}+273)}{273\,F_{\mathrm{эк}}^{\mathrm{г}}}=\dfrac{20{,}046\cdot %(Ve)s(%(thce)s+273)}{273\cdot 88{,}89}=%(we)s\ \mathrm{м/с}'
T[216]=r"\Delta t_{\mathrm{б}}=\vartheta^{\prime\prime}{}_{\mathrm{кпнд}}-t^{\prime\prime}{}_{\mathrm{эк}}=%(th2n)s-%(te2)s=%(dbe)s"+D
T[217]=r"\Delta t_{\mathrm{м}}=\vartheta^{\prime\prime}{}_{\mathrm{эк}}-t_{\mathrm{пв}}=%(th2e)s-265=%(dme)s"+D
T[218]=r'\Delta t_{\mathrm{эк}}=\dfrac{\Delta t_{\mathrm{б}}-\Delta t_{\mathrm{м}}}{\ln(\Delta t_{\mathrm{б}}/\Delta t_{\mathrm{м}})}=\dfrac{%(dbe)s-%(dme)s}{\ln(%(dbe)s/%(dme)s)}=%(dte)s'+D
T[220]=r'=0{,}86\cdot 1{,}0\cdot 75\left(\dfrac{%(we)s}{9}\right)^{0{,}5}\cdot 1\cdot\left(\dfrac{3{,}125}{2{,}5}\right)^{0{,}15}=%(ke)s\ \mathrm{Вт/(м}^2\cdot\mathrm{К)}'
T[221]=r'q_{\mathrm{эк}}=\dfrac{k_{\mathrm{эк}}\Delta t_{\mathrm{эк}}}{1000}=\dfrac{%(ke)s\cdot %(dte)s}{1000}=%(qe)s\ \mathrm{кВт/м}^2'
T[222]=r'F_{\mathrm{эк}}=\dfrac{B_{\mathrm{р}}Q_{\mathrm{эк}}}{q_{\mathrm{эк}}}=\dfrac{20{,}046\cdot %(Qe)s}{%(qe)s}=%(Fe_)s\ \mathrm{м}^2'
T[224]=r'z_{\mathrm{р}}=\dfrac{F_{\mathrm{эк}}}{F_{\mathrm{эк}}^1}=\dfrac{%(Fe_)s}{130{,}89}=%(zreR)s\approx %(zre)s'
T[225]=r'z_{\mathrm{пет}}=\dfrac{z_{\mathrm{р}}}{2n_2}=\dfrac{%(zre)s}{2\cdot 4}=%(zpe)s'
T[227]=r'=(%(zre)s-1)\cdot 0{,}048+0{,}032+0{,}070(%(zpe)s+1)=%(lpe)s\ \mathrm{м}'
T[228]=r'Q_{\mathrm{эк}}^{\mathrm{р}}=\dfrac{k_{\mathrm{эк}}\Delta t_{\mathrm{эк}}F_{\mathrm{эк}}^1z_{\mathrm{р}}}{B_{\mathrm{р}}\cdot 1000}=\dfrac{%(ke)s\cdot %(dte)s\cdot 130{,}89\cdot %(zre)s}{20{,}046\cdot 1000}=%(Qer)s'+KJ
T[229]=r'\delta Q=\dfrac{Q_{\mathrm{эк}}^{\mathrm{р}}-Q_{\mathrm{эк}}}{Q_{\mathrm{эк}}^{\mathrm{р}}}100=\dfrac{%(Qer)s-%(Qe)s}{%(Qer)s}100=%(dQe)s\ \%%'
T[232]=r"H^{\prime}{}_{\mathrm{вп}}=\dfrac{H^{\prime\prime}{}_{\mathrm{эк}}}{1+r_{\mathrm{г}}}=\dfrac{%(H2e)s}{1+%(r)s}=%(H1v)s"+KJ
T[234]=r'=0{,}9979(%(H1v)s-2\ 887{,}36+0{,}15\cdot 2\ 503{,}23)=%(Qvp)s'+KJ
T[238]=r"H_{\mathrm{г.в}}^0=H_{\mathrm{вп}}^{0\prime}+\dfrac{Q_{\mathrm{вп}}}{\bar{\beta}_{\mathrm{вп}}}=936{,}66+\dfrac{%(Qvp)s}{1{,}275}=%(H0gv2)s"+KJ
T[239]=r't_{\mathrm{г.в}}^{\mathrm{р}}=\dfrac{2610\,H_{\mathrm{г.в}}^0}{H_{\mathrm{в}}^0+0{,}25\,H_{\mathrm{г.в}}^0}=\dfrac{2610\cdot %(H0gv2)s}{34\ 690+0{,}25\cdot %(H0gv2)s}=%(tgv)s'+D
T[241]=r"\Delta t_{\mathrm{м}}=\vartheta^{\prime\prime}{}_{\mathrm{эк}}-t^{\prime\prime}{}_{\mathrm{вп}}=%(th2e)s-%(tgv)s=%(dmv)s"+D
T[242]=r'\Delta t_{\mathrm{рвп}}=\dfrac{\Delta t_{\mathrm{б}}-\Delta t_{\mathrm{м}}}{\ln(\Delta t_{\mathrm{б}}/\Delta t_{\mathrm{м}})}=\dfrac{80{,}00-%(dmv)s}{\ln(80{,}00/%(dmv)s)}=%(dtv)s'+D
T[243]=r"\bar{\vartheta}_{\mathrm{вп}}=0{,}5(\vartheta^{\prime\prime}{}_{\mathrm{эк}}+\vartheta_{\mathrm{ух}})=0{,}5(%(th2e)s+150)=%(thcv)s"+D
T[244]=r"\bar{t}_{\mathrm{вп}}=0{,}5(t^{\prime}{}_{\mathrm{вп}}+t^{\prime\prime}{}_{\mathrm{вп}})=0{,}5(70+%(tgv)s)=%(tcv)s"+D
T[248]=r'w_{\mathrm{г}}=\dfrac{B_{\mathrm{р}}V_{\mathrm{рвп}}^{\mathrm{г}}(\bar{\vartheta}_{\mathrm{вп}}+273)}{2\cdot 273\,f_{\mathrm{г}}}=\dfrac{20{,}046\cdot 13{,}183(%(thcv)s+273)}{2\cdot 273\cdot 29{,}5}=%(wgr)s\ \mathrm{м/с}'
T[249]=r'w_{\mathrm{в}}=\dfrac{B_{\mathrm{р}}V_{\mathrm{в}}(\bar{t}_{\mathrm{вп}}+273)}{2\cdot 273\,f_{\mathrm{в}}}=\dfrac{20{,}046\cdot 13{,}005(%(tcv)s+273)}{2\cdot 273\cdot 29{,}5}=%(wvr)s\ \mathrm{м/с}'
T[250]=r'\alpha_{\mathrm{г}}=33\left(\dfrac{w_{\mathrm{г}}}{7}\right)^{0{,}8}C_{\mathrm{ф}}C_{\mathrm{н}}=33\left(\dfrac{%(wgr)s}{7}\right)^{0{,}8}\cdot 1{,}18\cdot 1{,}425=%(ag)s\ \mathrm{Вт/(м}^2\cdot\mathrm{К)}'
T[251]=r"\alpha_{\mathrm{в}}=29\left(\dfrac{w_{\mathrm{в}}}{6}\right)^{0{,}8}C^{\prime}{}_{\mathrm{ф}}C_{\mathrm{н}}=29\left(\dfrac{%(wvr)s}{6}\right)^{0{,}8}\cdot 1{,}03\cdot 1{,}425=%(av)s\ \mathrm{Вт/(м}^2\cdot\mathrm{К)}"
T[252]=r'k=\dfrac{\xi_{\mathrm{вп}}}{\dfrac{1}{x_{\mathrm{г}}\alpha_{\mathrm{г}}}+\dfrac{1}{x_{\mathrm{в}}\alpha_{\mathrm{в}}}}=\dfrac{0{,}89}{\dfrac{1}{0{,}5\cdot %(ag)s}+\dfrac{1}{0{,}5\cdot %(av)s}}=%(kv)s\ \mathrm{Вт/(м}^2\cdot\mathrm{К)}'
T[253]=r'F_{\mathrm{вп}}=\dfrac{B_{\mathrm{р}}Q_{\mathrm{вп}}\cdot 10^3}{2k\,\Delta t_{\mathrm{рвп}}}=\dfrac{20{,}046\cdot %(Qvp)s\cdot 10^3}{2\cdot %(kv)s\cdot %(dtv)s}=%(Fv)s\ \mathrm{м}^2'
T[254]=r'H_{\mathrm{вп}}=\dfrac{F_{\mathrm{вп}}}{F_{\mathrm{уд}}}=\dfrac{%(Fv)s}{24\ 380}=%(Hvp)s\ \mathrm{м}'
T[255]=r'q_{\mathrm{вп}}=\dfrac{k\,\Delta t_{\mathrm{рвп}}}{10^3}=\dfrac{%(kv)s\cdot %(dtv)s}{10^3}=%(qvp)s\ \mathrm{кВт/м}^2'
T[256]=r'Q_{\mathrm{вп}}^{\mathrm{т}}=\dfrac{2q_{\mathrm{вп}}F_{\mathrm{вп}}}{B_{\mathrm{р}}}=\dfrac{2\cdot %(qvp)s\cdot %(Fv)s}{20{,}046}=%(Qvp)s'+KJ
def build(R):
    V=vals(R); return {k:t%V for k,t in T.items()}
