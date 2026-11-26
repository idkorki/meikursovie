import re, math, io, zipfile, os, sys
sys.path.insert(0,'../kk')
from R import R
from PIL import Image
SRC='/home/user/meikursovie/курсовые котлы/9кк/9кк_Поверочный_расчёт_БКЗ-210-140Ф_вар31.docx'
c=lambda v,n: f'{v:,.{n}f}'.replace(',','X').replace('.','{,}').replace('X','\\ ')
t=lambda v,n: f'{v:,.{n}f}'.replace(',',' ').replace('.',',')
DEG=r'\ ^{\circ}\;\mathrm{C}'
Ta=2224.9; psi=0.934*0.45; Ap=27.4; V=909.3; F=658.6; ht=17.157; hg=2.7625; B=9.072; Qt=19151.6; N=9200
S=3.6*V/F; htp=ht-6.12/2; X=hg/htp; M=0.59-0.5*X; qF=B*Qt/F
def it(th):
    T=th+273; kg=0.92*(4/S)**0.54*1470/T; kzl=2.96*(Ap/35)**1.33*(1470/T)**0.67; k=kg+kzl+0.2
    ef=1-math.exp(-k*0.1*S); et=ef/(ef+(1-ef)*psi); P=et*psi*Ta**2/(N*qF); tc=round(Ta*(1-M*P**0.6)-273,1)
    return dict(th=th,T=T,kg=kg,kzl=kzl,k=k,ef=ef,et=et,P=P,tc=tc,d=abs(th-tc))
I1=it(1030)
Ql=9726.2; Ht=9425.3
I=I1
blocks=[
 ('p','Задача поверочного расчёта – проверить, с какой температурой газы действительно покидают топку, размеры которой окончательно установлены в п. 3.10. Конструкция топки теперь известна: объём, площадь экранированных стен и отметки горелок, а также тепловая эффективность экранов. По ним формула (3.54) [2] даёт расчётную температуру ϑ″_{т}, которую сравнивают с принятой в начале расчёта. Допустимое расхождение – 30 °С; при большем расхождении расчёт повторяют с новой температурой [2]. Величины, на которые опирается расчёт, собраны в таблицу 5.'),
 ('tbl','Таблица 5 – Исходные величины поверочного расчёта топки',['Величина','Обозначение','Значение'],[
   ['Объём топки, м³','V_{т}',t(V,1)],['Площадь стен топки, м²','F_{ст}',t(F,1)],['Высота топки от середины холодной воронки, м','h_{т}',t(ht,3)],
   ['Ширина фронта и глубина топки, м','a_{т} / b_{т}','10,404 / 6,12'],['Высота выходного газового окна, м','h′_{го}','6,12'],
   ['Средняя отметка горелок, м','h_{гор}','2,763'],['Расход топлива, кг/с','B',t(B,3)],
   ['Полезное тепловыделение в топке, кДж/кг','Q_{т}','19 151,6'],['Теоретическая температура горения, °С / К','ϑ_{а} / T_{а}','1 951,9 / 2 224,9'],
   ['Коэффициент тепловой эффективности экранов','ψ_{т}','0,420'],['Зольность топлива на рабочую массу, %','A^{р}','27,4'],
   ['Коэффициент N для твёрдых топлив','N','9200'],['Принятая температура газов за топкой, °С','ϑ″_{т}','1030'],
   ['Температура начала деформации золы, °С','t_{1}','1050']]),
 ('p','Расчётная температура газов за топкой определяется по (3.54) [2]:'),
 ('img',111),
 ('p','В формулу (7) входят величины двух видов. Первые – геометрия топки, положение горелок и тепловая нагрузка экранов – от температуры газов не зависят. Вторые – коэффициенты ослабления лучей и степени черноты – зависят от температуры и вычисляются для принятого значения ϑ″_{т}.'),
 ('p','Толщина излучающего слоя газов в топке окончательных размеров (3.49):'),
 ('f',r'S=\dfrac{3{,}6\,V_{\mathrm{т}}}{F_{\mathrm{ст}}}=\dfrac{3{,}6\cdot 909{,}3}{658{,}6}=%s\ \mathrm{м}'%c(S,3)),
 ('p','Высота факела: от середины холодной воронки, откуда отсчитываются отметки горелок, до середины выходного окна:'),
 ('f',r'h_{\mathrm{т}}^{\prime}=h_{\mathrm{т}}-\dfrac{h_{\mathrm{го}}^{\prime}}{2}=17{,}157-\dfrac{6{,}12}{2}=%s\ \mathrm{м}'%c(htp,3)),
 ('p','Относительное положение горелок по высоте факела (3.33) [2]; средняя отметка двух ярусов горелок h_{гор} = 2,763 м найдена в п. 3.10:'),
 ('f',r'X_{\mathrm{т}}=\dfrac{h_{\mathrm{гор}}}{h_{\mathrm{т}}^{\prime}}=\dfrac{2{,}763}{%s}=%s'%(c(htp,3),c(X,3))),
 ('p','Коэффициент M учитывает, на какой высоте находится зона наибольших температур. Для высокореакционного каменного угля, не относящегося к сильнозольным (A_{п} < 2 %·кг/МДж), он находится по (3.30) [2]:'),
 ('f',r'M=0{,}59-0{,}5\,X_{\mathrm{т}}=0{,}59-0{,}5\cdot %s=%s'%(c(X,3),c(M,3))),
 ('p','Тепловая нагрузка стен топки (3.26) – полезное тепловыделение, приходящееся на 1 м² поверхности экранов:'),
 ('img',112),
 ('p','Температурно-зависимые величины вычисляются для принятой при конструктивном расчёте температуры ϑ″_{т} = 1030 °С. Абсолютная температура газов за топкой:'),
 ('f',r'T_{\mathrm{т}}^{\prime\prime}=\vartheta_{\mathrm{т}}^{\prime\prime}+273=1030+273=1303\ \mathrm{K}'),
 ('p','Ослабление лучей трёхатомными газами CO_{2} и H_{2}O (3.44) [2]; для каменных углей k′_{г} = 0,92:'),
 ('f',r'k_{\mathrm{г}}=k_{\mathrm{г}}^{\prime}\left(\dfrac{4}{S}\right)^{0{,}54}\dfrac{1470}{T_{\mathrm{т}}^{\prime\prime}}=0{,}92\cdot \left(\dfrac{4}{%s}\right)^{0{,}54}\dfrac{1470}{1303}=%s'%(c(S,3),c(I['kg'],3))),
 ('p','Ослабление лучей взвешенными частицами золы (3.45) [2]. Уголь размалывается в молотковых мельницах, поэтому k′_{зл} = 2,96; зольность A^{р} = 27,4 %:'),
 ('f',r'k_{\mathrm{зл}}=k_{\mathrm{зл}}^{\prime}\left(\dfrac{A^{\mathrm{р}}}{35}\right)^{1{,}33}\left(\dfrac{1470}{T_{\mathrm{т}}^{\prime\prime}}\right)^{0{,}67}=2{,}96\cdot \left(\dfrac{27{,}4}{35}\right)^{1{,}33}\left(\dfrac{1470}{1303}\right)^{0{,}67}=%s'%c(I['kzl'],3)),
 ('p','Вклад горящих частиц кокса для каменного угля принимается k_{к} = 0,2. Суммарный коэффициент ослабления лучей (3.43):'),
 ('f',r'k=k_{\mathrm{г}}+k_{\mathrm{зл}}+k_{\mathrm{к}}=%s+%s+0{,}2=%s'%(c(I['kg'],3),c(I['kzl'],3),c(I['k'],3))),
 ('p','Степень черноты светящегося пылеугольного факела находится по закону Бугера (3.42); давление в топке p = 0,1 МПа:'),
 ('f',r'\varepsilon_{\mathrm{ф}}=1-e^{-kpS}=1-e^{-%s\cdot 0{,}1\cdot %s}=%s'%(c(I['k'],3),c(S,3),c(I['ef'],3))),
 ('p','Степень черноты топочной камеры (3.41) учитывает, что загрязнённые экраны часть излучения отражают обратно в топку:'),
 ('f',r'\varepsilon_{\mathrm{т}}=\dfrac{\varepsilon_{\mathrm{ф}}}{\varepsilon_{\mathrm{ф}}+(1-\varepsilon_{\mathrm{ф}})\psi_{\mathrm{т}}}=\dfrac{%s}{%s+(1-%s)\cdot 0{,}420}=%s'%(c(I['ef'],3),c(I['ef'],3),c(I['ef'],3),c(I['et'],3))),
 ('p','Для наглядности отдельно вычисляется безразмерный комплекс из скобок формулы (7) и его степень 0,6:'),
 ('f',r'\Pi=\dfrac{\varepsilon_{\mathrm{т}}\,\psi_{\mathrm{т}}\,T_{\mathrm{а}}^2}{N\,q_F}=\dfrac{%s\cdot 0{,}420\cdot 2\ 224{,}9^2}{9200\cdot %s}=%s;\qquad \Pi^{0{,}6}=%s'%(c(I['et'],3),c(qF,1),c(I['P'],3),c(I['P']**0.6,3))),
 ('p','Подстановка всех величин в (7) даёт расчётную температуру газов за топкой:'),
 ('img',113),
 ('p','Разница принятой и расчётной температур:'),
 ('img',114),
 ('p','Расхождение 24,4 °С меньше допустимых 30 °С, поэтому повторять расчёт с новой температурой не требуется, и в дальнейших расчётах сохраняется ϑ″_{т} = 1030 °С. Она на 20 °С ниже температуры начала деформации золы t_{1} = 1050 °С, поэтому частицы золы успевают затвердеть до входа в ширмы и не налипают на них. Расчётная температура 1 005,6 °С ниже принятой, то есть фактически топка охлаждает газы с некоторым запасом. Сводка поверочного расчёта приведена в таблице 6.'),
 ('tbl','Таблица 6 – Результаты поверочного расчёта топки',['Величина','Обозначение','Значение'],[
   ['Толщина излучающего слоя, м','S',t(S,3)],['Высота факела, м','h′_{т}',t(htp,3)],['Относительная отметка горелок','X_{т}',t(X,3)],
   ['Коэффициент положения ядра факела','M',t(M,3)],['Тепловая нагрузка стен топки, кВт/м²','q_{F}',t(qF,1)],
   ['Коэффициент ослабления лучей газами, 1/(м·МПа)','k_{г}',t(I['kg'],3)],['Коэффициент ослабления лучей золой, 1/(м·МПа)','k_{зл}',t(I['kzl'],3)],
   ['Суммарный коэффициент ослабления, 1/(м·МПа)','k',t(I['k'],3)],['Степень черноты факела','ε_{ф}',t(I['ef'],3)],
   ['Степень черноты топки','ε_{т}',t(I['et'],3)],['Расчётная температура газов за топкой, °С','ϑ″_{т.р}',t(I['tc'],1)],
   ['Принятая температура газов за топкой, °С','ϑ″_{т}','1030'],['Расхождение, °С','Δϑ',t(I['d'],1)]]),
 ('p','По принятой температуре находятся энтальпия газов на выходе из топки (2.16) и теплота, переданная экранам излучением (3.22):'),
 ('img',115),('img',116),
 ('p','Доля полезного тепловыделения, которую воспринимают экраны топки:'),
 ('f',r'\dfrac{Q_{\mathrm{л}}}{Q_{\mathrm{т}}}=\dfrac{9\ 726{,}2}{19\ 151{,}6}=%s'%c(Ql/Qt,3)),
 ('p','Полное тепловосприятие топочных экранов и средняя тепловая нагрузка их поверхности по воспринятой теплоте:'),
 ('f',r'Q_{\mathrm{экр}}=B\,Q_{\mathrm{л}}=9{,}072\cdot 9\ 726{,}2=%s\ \mathrm{кВт}'%c(B*Ql,0)),
 ('f',r'q_{\mathrm{экр}}=\dfrac{B\,Q_{\mathrm{л}}}{F_{\mathrm{ст}}}=\dfrac{9{,}072\cdot 9\ 726{,}2}{658{,}6}=%s\ \mathrm{кВт/м}^2'%c(B*Ql/F,1)),
 ('p','Итак, экраны топки воспринимают около %d %% полезного тепловыделения (≈ %s МВт). Газы покидают топку с температурой 1030 °С, а оставшаяся часть теплоты передаётся ширмам, пакетам конвективного пароперегревателя, экономайзеру и воздухоподогревателю, расчёт которых приведён далее.'%(round(Ql/Qt*100),t(B*Ql/1000,1))),
]
# ---------- docx manipulation
z=zipfile.ZipFile(SRC); x=z.read('word/document.xml').decode('utf8'); rels=z.read('word/_rels/document.xml.rels').decode('utf8')
rid={b:a for a,b in re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"',rels)}
body_start=x.find('<w:body>')
pat=re.compile(r'<w:tbl>.*?</w:tbl>|<w:p[ >].*?</w:p>',re.S)
items=[(m.start(),m.end(),m.group(0)) for m in pat.finditer(x,body_start)]
txt=lambda s:''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>',s))
i0=[i for i,(a,b,s) in enumerate(items) if txt(s)=='3.11 Поверочный расчёт топки'][-1]
i1=[i for i,(a,b,s) in enumerate(items) if txt(s).startswith('4. РАСЧЁТ ТЕПЛОВОСПРИЯТИЯ ШИРМОВОЙ')][-1]
old={}
for a,b,s in items[i0+1:i1]:
    m=re.search(r'r:embed="(rId\d+)"',s)
    if m:
        k=[kk for kk,v in rid.items() if v==m.group(1)][0]; old[int(k.replace('media/image','').replace('.png',''))]=s
textP=[s for a,b,s in items[i0+1:i1] if txt(s).startswith('Тепловая нагрузка поверхности экранов')][0]
formP=old[112]
capP=[s for a,b,s in items if txt(s).startswith('Таблица 5 –')][0]
tblX=[s for a,b,s in items if s.startswith('<w:tbl>')][-1]
RPR='<w:rPr><w:b w:val="0"/><w:i w:val="0"/><w:sz w:val="28"/>%s</w:rPr>'
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def runs(s,sz=28,bold=False):
    out=[]
    for part in re.split(r'(_\{[^}]*\}|\^\{[^}]*\})',s):
        if not part: continue
        va=''
        if part.startswith('_{'): va='<w:vertAlign w:val="subscript"/>'; part=part[2:-1]
        elif part.startswith('^{'): va='<w:vertAlign w:val="superscript"/>'; part=part[2:-1]
        out.append('<w:r><w:rPr><w:b w:val="%d"/><w:i w:val="0"/><w:sz w:val="%d"/>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>'%(1 if bold else 0,sz,va,esc(part)))
    return ''.join(out)
pPr=re.search(r'<w:pPr>.*?</w:pPr>',textP).group(0)
def para(s): return '<w:p>'+pPr+runs(s)+'</w:p>'
os.makedirs('img',exist_ok=True)
newrels=[]; newmedia={}
nid=[900]; rmax=max(int(r[3:]) for r in re.findall(r'Id="(rId\d+)"',rels))
def formula(tex):
    nid[0]+=1; n=nid[0]; fn=f'img/f{n}.png'; R(tex,fn)
    w,h=Image.open(fn).size; cx=round(w/300*914400); cy=round(h/300*914400)
    r=f'rId{rmax+n}'; newrels.append(f'<Relationship Id="{r}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{n}.png"/>')
    newmedia[f'word/media/image{n}.png']=open(fn,'rb').read()
    s=re.sub(r'r:embed="rId\d+"',f'r:embed="{r}"',formP)
    s=re.sub(r'cx="\d+" cy="\d+"',f'cx="{cx}" cy="{cy}"',s)
    s=re.sub(r'<wp:docPr id="\d+" name="Picture \d+"/>',f'<wp:docPr id="{n}" name="Picture {n}"/>',s)
    return s
def table(cap,head,rows):
    cp=re.sub(r'<w:t>[^<]*</w:t>','<w:t>%s</w:t>'%esc(cap),capP)
    g=re.search(r'<w:tblGrid>.*?</w:tblGrid>',tblX).group(0)
    tpr=re.search(r'<w:tblPr>.*?</w:tblPr>',tblX).group(0)
    ws=[int(v) for v in re.findall(r'w:w="(\d+)"',g)]
    def cell(s,w,jc,bold):
        return f'<w:tc><w:tcPr><w:tcW w:type="dxa" w:w="{w}"/></w:tcPr><w:p><w:pPr><w:keepNext/><w:spacing w:line="240" w:lineRule="auto"/><w:jc w:val="{jc}"/></w:pPr>'+runs(s,22,bold)+'</w:p></w:tc>'
    tr=['<w:tr><w:trPr><w:tblHeader w:val="true"/><w:cantSplit/></w:trPr>'+''.join(cell(h,w,'center',True) for h,w in zip(head,ws))+'</w:tr>']
    for r in rows: tr.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>'+''.join(cell(v,w,'left' if j==0 else 'center',False) for j,(v,w) in enumerate(zip(r,ws)))+'</w:tr>')
    return cp+'<w:tbl>'+tpr+g+''.join(tr)+'</w:tbl>'
out=[]
for b in blocks:
    if b[0]=='p': out.append(para(b[1]))
    elif b[0]=='f': out.append(formula(b[1]))
    elif b[0]=='img': out.append(old[b[1]])
    elif b[0]=='tbl': out.append(table(*b[1:]))
new_x=x[:items[i0][1]]+''.join(out)+x[items[i1][0]:]
new_x=new_x.replace('<w:t>Таблица 5 – Температуры газов','<w:t>Таблица 7 – Температуры газов')
assert 'Таблица 7 – Температуры' in new_x
rels2=rels.replace('</Relationships>',''.join(newrels)+'</Relationships>')
buf=io.BytesIO(); zo=zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED)
for itm in z.infolist():
    data=z.read(itm.filename)
    if itm.filename=='word/document.xml': data=new_x.encode('utf8')
    if itm.filename=='word/_rels/document.xml.rels': data=rels2.encode('utf8')
    zo.writestr(itm,data)
for k,v in newmedia.items(): zo.writestr(k,v)
zo.close(); open('out.docx','wb').write(buf.getvalue()); print('formulas',len(newmedia),'blocks',len(blocks))
