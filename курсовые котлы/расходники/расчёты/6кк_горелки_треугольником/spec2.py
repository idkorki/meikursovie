from spec import c, build
import math
def rm(s): return r'\mathrm{'+s+'}'
U_kg=r'\ \mathrm{кДж/кг}'; DEG=r'\ ^{\circ}\;\mathrm{C}'
def build2(mode):
    E0,v=build(mode); r=v['r']; hx=r['hx']; gp=r['gp']
    E={}
    Ff=v['Ff']
    E[131]=r'q_{\mathrm{л}}=\dfrac{B\,Q_{\mathrm{л}}}{F_{\mathrm{ст}}\chi}=\dfrac{7{,}082\cdot 13\ 556{,}3}{%s\cdot 0{,}985}=%s\ \mathrm{кВт/м}^2'%(c(Ff,1),c(r['ql'],3))
    E[132]=r'Q_{\mathrm{ш.л}}=\dfrac{\beta_{\mathrm{ш}}\,\eta_{\mathrm{в}}\,q_{\mathrm{л}}\,\varphi_{\mathrm{ш}}\,F_{\mathrm{ш.л}}}{B}=\dfrac{1\cdot 0{,}8\cdot %s\cdot 0{,}799\cdot 83{,}50}{7{,}082}'%c(r['ql'],3)
    E[133]=r'=%s'%c(r['Qshl'],1)+U_kg
    E[137]=r'\Delta h_{\mathrm{ш}}=\dfrac{B\left(Q_{\mathrm{ш.л}}+Q_{\mathrm{ш.б}}\,\dfrac{z_{\mathrm{ш}}}{z_{\mathrm{ш}}+1}\right)}{D_{\mathrm{ш}}}=\dfrac{7{,}082\left(%s+1\ 712{,}7\cdot \dfrac{17}{17+1}\right)}{57{,}036}'%c(r['Qshl'],1)
    E[138]=r'=%s'%c(r['dhsh'],2)+U_kg
    E[150]=r'h_{\mathrm{шпп}}^{\prime\prime}=h_{\mathrm{шпп}}^{\prime}+\Delta h_{\mathrm{ш}}=2\ 774{,}71+%s=%s'%(c(r['dhsh'],2),c(r['h_sh2'],2))+U_kg
    E[151]=r't_{\mathrm{шпп}}^{\prime\prime}=t(P_{\mathrm{шпп}}^{\prime\prime};\ h_{\mathrm{шпп}}^{\prime\prime})=%s'%c(r['t_sh2'],2)+DEG
    E[152]=r'h_{\mathrm{гпп}}^{\prime}=\dfrac{D_{\mathrm{ш}}\,h_{\mathrm{шпп}}^{\prime\prime}+D_{\mathrm{впр2}}\,h_{\mathrm{впр}}}{D_{\mathrm{ш}}+D_{\mathrm{впр2}}}=\dfrac{57{,}036\cdot %s+1{,}164\cdot 925{,}55}{57{,}036+1{,}164}'%c(r['h_sh2'],2)
    E[153]=r'=%s'%c(r['h_g1'],2)+U_kg
    E[154]=r't_{\mathrm{гпп}}^{\prime}=t(P_{\mathrm{гпп}}^{\prime};\ h_{\mathrm{гпп}}^{\prime})=%s'%c(r['t_g1'],2)+DEG
    E[156]=r'Q_{\mathrm{л.вых}}=\dfrac{Q_{\mathrm{ш.л}}(1-\varphi_{\mathrm{ш}})}{\varphi_{\mathrm{ш}}}=\dfrac{%s(1-0{,}799)}{0{,}799}=%s'%(c(r['Qshl'],1),c(r['Qlv'],1))+U_kg
    E[157]=r'Q_{\mathrm{гпп}}=\dfrac{D(h_{\mathrm{гпп}}^{\prime\prime}-h_{\mathrm{гпп}}^{\prime})}{B}=\dfrac{58{,}2(3\ 432{,}13-%s)}{7{,}082}=%s'%(c(r['h_g1'],2),c(r['Qgpp'],1))+U_kg
    E[158]=r'Q_{\mathrm{хпп}}=\dfrac{D_{\mathrm{хп}}(h_{\mathrm{хпп}}^{\prime\prime}-h_{\mathrm{хпп}}^{\prime})}{B}-Q_{\mathrm{л.вых}}=\dfrac{55{,}290(2\ 833{,}10-2\ 584{,}18)}{7{,}082}-%s'%c(r['Qlv'],1)
    E[159]=r'=%s'%c(r['Qhpp'],1)+U_kg
    E[160]=r'H_{\mathrm{гпп}}^{\prime\prime}=H_{\mathrm{ш}}^{\prime\prime}-Q_{\mathrm{гпп}}=9\ 155{,}1-%s=%s'%(c(r['Qgpp'],1),c(r['Hgpp'],1))+U_kg
    E[161]=r'H_{\mathrm{хпп}}^{\prime\prime}=H_{\mathrm{гпп}}^{\prime\prime}-Q_{\mathrm{хпп}}=%s-%s=%s'%(c(r['Hgpp'],1),c(r['Qhpp'],1),c(r['Hhpp'],1))+U_kg
    E[163]=r'\vartheta_{\mathrm{гп}}^{\prime\prime}=\dfrac{2695\,H_{\mathrm{гпп}}^{\prime\prime}/H_{0\mathrm{гг}}}{1+0{,}3\,H_{\mathrm{гпп}}^{\prime\prime}/H_{0\mathrm{гг}}}=\dfrac{2695\cdot %s}{1+0{,}3\cdot %s}=%s'%(c(r['Hgpp']/27228.9,4),c(r['Hgpp']/27228.9,4),c(r['thg'],1))+DEG
    E[164]=r'\vartheta_{\mathrm{хп}}^{\prime\prime}=\dfrac{2695\,H_{\mathrm{хпп}}^{\prime\prime}/H_{0\mathrm{гг}}}{1+0{,}3\,H_{\mathrm{хпп}}^{\prime\prime}/H_{0\mathrm{гг}}}=\dfrac{2695\cdot %s}{1+0{,}3\cdot %s}=%s'%(c(r['Hhpp']/27228.9,4),c(r['Hhpp']/27228.9,4),c(r['thx'],1))+DEG
    # ХПП
    E[175]=r'\vartheta_{\mathrm{ср}}=\dfrac{\vartheta_{\mathrm{гп}}^{\prime\prime}+\vartheta_{\mathrm{хп}}^{\prime\prime}}{2}=\dfrac{%s+%s}{2}=%s'%(c(r['thg'],1),c(r['thx'],1),c(hx['thc'],1))+DEG
    E[176]=r'w_{\mathrm{ср}}=\dfrac{B\,V_{\mathrm{г}}(\vartheta_{\mathrm{ср}}+273)}{273\,F_{\mathrm{газ}}\,k_{\mathrm{ж}}}=\dfrac{7{,}082\cdot 7{,}381(%s+273)}{273\cdot 63{,}67\cdot 0{,}652}=%s\ \mathrm{м/с}'%(c(hx['thc'],1),c(hx['w'],2))
    E[178]=r'=0{,}86\cdot 1{,}03\cdot 71\left(\dfrac{%s}{9}\right)^{0{,}5}\cdot 1\cdot 1=%s\ \mathrm{Вт/(м}^2\cdot\mathrm{К)}'%(c(hx['w'],2),c(hx['k'],2))
    E[179]=r'\Delta t_{\mathrm{б}}=%s'%c(hx['db'],1)+DEG
    E[180]=r'\Delta t_{\mathrm{м}}=%s'%c(hx['dm'],1)+DEG
    E[181]=r'\Delta t=\dfrac{\Delta t_{\mathrm{б}}-\Delta t_{\mathrm{м}}}{\ln(\Delta t_{\mathrm{б}}/\Delta t_{\mathrm{м}})}=\dfrac{%s-%s}{\ln(%s/%s)}=%s'%(c(hx['db'],1),c(hx['dm'],1),c(hx['db'],1),c(hx['dm'],1),c(hx['dt'],1))+DEG
    E[182]=r'F=\dfrac{B\,Q_{\mathrm{хпп}}}{k\,\Delta t}\cdot 10^3=\dfrac{7{,}082\cdot %s}{%s\cdot %s}\cdot 10^3=%s\ \mathrm{м}^2'%(c(r['Qhpp'],1),c(hx['k'],2),c(hx['dt'],1),c(hx['F'],1))
    E[183]=r'z_{\mathrm{р}}=\dfrac{F}{F_1}=\dfrac{%s}{68{,}91}=%s\ \rightarrow\ %d'%(c(hx['F'],1),c(hx['zrr'],2),hx['zr'])
    E[184]=r'z_{\mathrm{пет}}=\dfrac{z_{\mathrm{р}}}{2n_2}=\dfrac{%d}{2\cdot 2}=%s\ \rightarrow\ %s'%(hx['zr'],c(hx['zpr'],2),c(hx['zp'],1))
    E[187]=r'l_{\mathrm{п}}=(z_{\mathrm{р}}-1)s_2+d_{\mathrm{н}}+m_{\mathrm{г}}(z_{\mathrm{пет}}+1)=(%d-1)\cdot 0{,}064+0{,}032+0{,}112(%s+1)'%(hx['zr'],c(hx['zp'],1))
    E[188]=r'=%s\ \mathrm{м}'%c(hx['lp'],2)
    # ГПП
    E[196]=r'\vartheta_{\mathrm{ср}}=\dfrac{\vartheta_{\mathrm{ш}}^{\prime\prime}+\vartheta_{\mathrm{гп}}^{\prime\prime}}{2}=\dfrac{840{,}0+%s}{2}=%s'%(c(r['thg'],1),c(gp['thc'],1))+DEG
    E[197]=r'w_{\mathrm{ср}}=\dfrac{B\,V_{\mathrm{г}}(\vartheta_{\mathrm{ср}}+273)}{273\,F_{\mathrm{газ}}\,k_{\mathrm{ж}}}=\dfrac{7{,}082\cdot 7{,}381(%s+273)}{273\cdot 63{,}67\cdot 0{,}618}=%s\ \mathrm{м/с}'%(c(gp['thc'],1),c(gp['w'],2))
    E[198]=r'=0{,}86\cdot 1{,}08\cdot 71\left(\dfrac{%s}{9}\right)^{0{,}5}\cdot 1\cdot 1=%s\ \mathrm{Вт/(м}^2\cdot\mathrm{К)}'%(c(gp['w'],2),c(gp['k'],2))
    E[199]=r'\Delta t_{\mathrm{б}}=%s'%c(gp['db'],1)+DEG
    E[200]=r'\Delta t_{\mathrm{м}}=%s'%c(gp['dm'],1)+DEG
    E[201]=r'\Delta t=\dfrac{\Delta t_{\mathrm{б}}-\Delta t_{\mathrm{м}}}{\ln(\Delta t_{\mathrm{б}}/\Delta t_{\mathrm{м}})}=\dfrac{%s-%s}{\ln(%s/%s)}=%s'%(c(gp['db'],1),c(gp['dm'],1),c(gp['db'],1),c(gp['dm'],1),c(gp['dt'],1))+DEG
    E[202]=r'F=\dfrac{B\,Q_{\mathrm{гпп}}}{k\,\Delta t}\cdot 10^3=\dfrac{7{,}082\cdot %s}{%s\cdot %s}\cdot 10^3=%s\ \mathrm{м}^2'%(c(r['Qgpp'],1),c(gp['k'],2),c(gp['dt'],1),c(gp['F'],1))
    E[203]=r'z_{\mathrm{р}}=\dfrac{F}{F_1}=\dfrac{%s}{75{,}68}=%s\ \rightarrow\ %d'%(c(gp['F'],1),c(gp['zrr'],2),gp['zr'])
    E[204]=r'z_{\mathrm{пет}}=\dfrac{z_{\mathrm{р}}}{2n_2}=\dfrac{%d}{2\cdot 2}=%s\ \rightarrow\ %s'%(gp['zr'],c(gp['zpr'],2),c(gp['zp'],1))
    E[206]=r'=(%d-1)\cdot 0{,}064+0{,}032+0{,}112(%s+1)=%s\ \mathrm{м}'%(gp['zr'],c(gp['zp'],1),c(gp['lp'],2))
    # экономайзер
    E[213]=r'=\dfrac{22\ 400\cdot 92{,}225}{100}-(13\ 556{,}3+1\ 712{,}7+%s+%s)'%(c(r['Qgpp'],1),c(r['Qhpp'],1))
    E[214]=r'=%s'%c(r['Qek'],1)+U_kg
    E[215]=r'\Delta h_{\mathrm{эк}}=\dfrac{Q_{\mathrm{эк}}\,B}{D_{\mathrm{эк}}}=\dfrac{%s\cdot 7{,}082}{55{,}290}=%s'%(c(r['Qek'],1),c(r['dhek'],2))+U_kg
    E[216]=r'h_{\mathrm{эк}}^{\prime\prime}=h_{\mathrm{эк}}^{\prime}+\Delta h_{\mathrm{эк}}=925{,}60+%s=%s'%(c(r['dhek'],2),c(r['hek2'],2))+U_kg
    E[217]=r't_{\mathrm{эк}}^{\prime\prime}=t(P_{\mathrm{эк}}^{\prime\prime};\ h_{\mathrm{эк}}^{\prime\prime})=%s'%c(r['tek2'],2)+DEG
    E[218]=r'\Delta t=t_s-t_{\mathrm{эк}}^{\prime\prime}=346{,}81-%s=%s'%(c(r['tek2'],2),c(346.813-r['tek2'],1))+DEG
    E[219]=r'H_{\mathrm{эк}}^{\prime\prime}=H_{\mathrm{хпп}}^{\prime\prime}-Q_{\mathrm{эк}}=%s-%s=%s'%(c(r['Hhpp'],1),c(r['Qek'],1),c(r['Hek'],1))+U_kg
    E[232]=r'\vartheta_{\mathrm{ср}}=\dfrac{\vartheta_{\mathrm{хп}}^{\prime\prime}+\vartheta_{\mathrm{эк}}^{\prime\prime}}{2}=\dfrac{%s+352{,}9}{2}=%s'%(c(r['thx'],1),c(r['thc'],1))+DEG
    E[233]=r'F_{\mathrm{газ.эк}}=\dfrac{B\,V_{\mathrm{г.эк}}(\vartheta_{\mathrm{ср}}+273)}{273\,w_{\mathrm{ср}}\,k_{\mathrm{ж}}}=\dfrac{7{,}082\cdot 7{,}501(%s+273)}{273\cdot 7\cdot 0{,}667}=%s\ \mathrm{м}^2'%(c(r['thc'],1),c(r['Fgaz'],2))
    E[234]=r'b_{\mathrm{ш}}=\dfrac{F_{\mathrm{газ.эк}}}{a_{\mathrm{т}}}=\dfrac{%s}{10{,}404}=%s\ \mathrm{м}'%(c(r['Fgaz'],2),c(r['bsh'],2))
    E[237]=r'\Delta t_{\mathrm{б}}=%s'%c(r['db'],1)+DEG
    E[239]=r'\Delta t_{\mathrm{эк}}=\dfrac{\Delta t_{\mathrm{б}}-\Delta t_{\mathrm{м}}}{\ln(\Delta t_{\mathrm{б}}/\Delta t_{\mathrm{м}})}=\dfrac{%s-137{,}9}{\ln(%s/137{,}9)}=%s'%(c(r['db'],1),c(r['db'],1),c(r['dt'],1))+DEG
    E[240]=r'F_{\mathrm{эк}}=\dfrac{B\,Q_{\mathrm{эк}}}{k_{\mathrm{эк}}\,\Delta t_{\mathrm{эк}}}\cdot 10^3=\dfrac{7{,}082\cdot %s}{64{,}61\cdot %s}\cdot 10^3=%s\ \mathrm{м}^2'%(c(r['Qek'],1),c(r['dt'],1),c(r['Fek'],1))
    E[241]=r'z_{\mathrm{р}}=\dfrac{F_{\mathrm{эк}}}{F_1}=\dfrac{%s}{65{,}22}=%s\ \rightarrow\ %d'%(c(r['Fek'],1),c(r['Fek']/65.22,2),r['zr'])
    E[278]=r'Q_{\mathrm{эк.п}}=\dfrac{Q_{\mathrm{р}}^{\mathrm{р}}\,\eta_{\mathrm{пк}}}{100}-(Q_{\mathrm{л}}+Q_{\mathrm{ш.б}}+Q_{\mathrm{гпп}}+Q_{\mathrm{хпп}})=%s'%c(r['Qek'],1)+U_kg
    E[279]=r'\delta Q=\dfrac{|Q_{\mathrm{эк}}-Q_{\mathrm{эк.п}}|}{Q_{\mathrm{эк}}}\cdot 100=\dfrac{|%s-%s|}{%s}\cdot 100=0{,}00\ \%%'%(c(r['Qek'],1),c(r['Qek'],1),c(r['Qek'],1))
    S=13556.3+1712.7+round(r['Qgpp'],1)+round(r['Qhpp'],1)+round(r['Qek'],1)
    E[281]=r'=13\ 556{,}3+1\ 712{,}7+%s+%s+%s=%s'%(c(r['Qgpp'],1),c(r['Qhpp'],1),c(r['Qek'],1),c(S,1))+U_kg
    return E0,E,v
