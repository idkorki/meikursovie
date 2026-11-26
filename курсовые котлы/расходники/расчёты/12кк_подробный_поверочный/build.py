import re, math, io, zipfile, os, sys
sys.path.insert(0,'../kk')
from R import R
from PIL import Image
SRC='../k43/in.docx'
c=lambda v,n: f'{v:,.{n}f}'.replace(',','X').replace('.','{,}').replace('X','\\ ')
t=lambda v,n: f'{v:,.{n}f}'.replace(',',' ').replace('.',',')
DEG=r'\ ^{\circ}\;\mathrm{C}'
Ta=2229.9; psi=0.934*0.45; Ap=27.0; V=905.1; F=656.5; ht=17.092; hg=2.7625; B=8.859; Qt=19508.2; N=9200
S=3.6*V/F; htp=ht-6.12/2; X=hg/htp; M=0.59-0.5*X; qF=B*Qt/F
def it(th):
    T=th+273; kg=0.92*(4/S)**0.54*1470/T; kzl=2.96*(Ap/35)**1.33*(1470/T)**0.67; k=kg+kzl+0.2
    ef=1-math.exp(-k*0.1*S); et=ef/(ef+(1-ef)*psi); P=et*psi*Ta**2/(N*qF); tc=round(Ta*(1-M*P**0.6)-273,1)
    return dict(th=th,T=T,kg=kg,kzl=kzl,k=k,ef=ef,et=et,P=P,tc=tc,d=abs(th-tc))
I1,I2=it(1110),it(1005)
Ql=10195.7
def step(I,first):
    T=I['T']
    return [
     ('f',r'T_{\mathrm{т}}^{\prime\prime}=\vartheta_{\mathrm{т}}^{\prime\prime}+273=%d+273=%d\ \mathrm{K}'%(I['th'],T)),
     ('p','Трёхатомные газы (CO_{2}, SO_{2}, H_{2}O) ослабляют лучи согласно (3.44) [2]; для каменного угля коэффициент k′_{г} = 0,92:' if first else 'Коэффициент ослабления лучей трёхатомными газами (3.44) [2] при новой температуре:'),
     ('f',r'k_{\mathrm{г}}=k_{\mathrm{г}}^{\prime}\left(\dfrac{4}{S}\right)^{0{,}54}\dfrac{1470}{T_{\mathrm{т}}^{\prime\prime}}=0{,}92\cdot \left(\dfrac{4}{%s}\right)^{0{,}54}\dfrac{1470}{%d}=%s'%(c(S,3),T,c(I['kg'],3))),
     ('p','Ослабление лучей летучей золой (3.45) [2]: при помоле в молотковых мельницах k′_{зл} = 2,96, зольность рабочей массы A^{р} = 27,0 %:' if first else 'Коэффициент ослабления лучей частицами золы (3.45) [2]:'),
     ('f',r'k_{\mathrm{зл}}=k_{\mathrm{зл}}^{\prime}\left(\dfrac{A^{\mathrm{р}}}{35}\right)^{1{,}33}\left(\dfrac{1470}{T_{\mathrm{т}}^{\prime\prime}}\right)^{0{,}67}=2{,}96\cdot \left(\dfrac{27{,}0}{35}\right)^{1{,}33}\left(\dfrac{1470}{%d}\right)^{0{,}67}=%s'%(T,c(I['kzl'],3))),
     ('p','С учётом частиц горящего кокса (k_{к} = 0,2) суммарный коэффициент ослабления лучей средой топки (3.43):' if first else 'Суммарный коэффициент ослабления лучей:'),
     ('f',r'k=k_{\mathrm{г}}+k_{\mathrm{зл}}+k_{\mathrm{к}}=%s+%s+0{,}2=%s'%(c(I['kg'],3),c(I['kzl'],3),c(I['k'],3))),
     ('p','Излучательная способность (степень черноты) пылеугольного факела по закону Бугера (3.42), давление газов в топке p = 0,1 МПа:' if first else 'Степень черноты факела (3.42):'),
     ('f',r'\varepsilon_{\mathrm{ф}}=1-e^{-kpS}=1-e^{-%s\cdot 0{,}1\cdot %s}=%s'%(c(I['k'],3),c(S,3),c(I['ef'],3))),
     ('p','Степень черноты топочной камеры (3.41), в которой учтено отражение излучения от загрязнённых экранов с коэффициентом эффективности ψ_{т} = 0,420:' if first else 'Степень черноты топочной камеры (3.41):'),
     ('f',r'\varepsilon_{\mathrm{т}}=\dfrac{\varepsilon_{\mathrm{ф}}}{\varepsilon_{\mathrm{ф}}+(1-\varepsilon_{\mathrm{ф}})\psi_{\mathrm{т}}}=\dfrac{%s}{%s+(1-%s)\cdot 0{,}420}=%s'%(c(I['ef'],3),c(I['ef'],3),c(I['ef'],3),c(I['et'],3))),
     ('p','Безразмерный комплекс в круглых скобках формулы (7) и его значение в степени 0,6:' if first else 'Комплекс в скобках формулы (7):'),
     ('f',r'\Pi=\dfrac{\varepsilon_{\mathrm{т}}\,\psi_{\mathrm{т}}\,T_{\mathrm{а}}^2}{N\,q_F}=\dfrac{%s\cdot 0{,}420\cdot 2\ 229{,}9^2}{9200\cdot %s}=%s;\qquad \Pi^{0{,}6}=%s'%(c(I['et'],3),'263{,}3',c(I['P'],3),c(I['P']**0.6,3))),
     ('p','Температура газов на выходе из топки, рассчитанная по (7):')]
blocks=[
 ('p','После того как в п. 3.10 окончательно определены размеры топки, выполняется её поверочный расчёт. Его цель – найти температуру газов, с которой они действительно выходят из топочной камеры заданной конструкции, и убедиться, что она близка к температуре, принятой в начале расчёта, и не опасна для ширм по условию шлакования. Расчёт ведётся методом последовательных приближений: если принятая и расчётная температуры различаются более чем на 30 °С, принимается новое значение и вычисления повторяются [2]. Данные, необходимые для расчёта, приведены в таблице 5.'),
 ('tbl','Таблица 5 – Данные для поверочного расчёта топки',['Величина','Обозначение','Значение'],[
   ['Объём топочной камеры, м³','V_{т}',t(V,1)],['Площадь поверхности стен, м²','F_{ст}',t(F,1)],['Высота топки, м','h_{т}',t(ht,3)],
   ['Ширина и глубина топки, м','a_{т} / b_{т}','10,404 / 6,12'],['Высота выходного окна, м','h′_{го}','6,12'],
   ['Средняя высота горелок, м','h_{гор}','2,763'],['Расчётный расход топлива, кг/с','B',t(B,3)],
   ['Полезное тепловыделение в топке, кДж/кг','Q_{т}','19 508,2'],['Адиабатная температура горения, °С / К','ϑ_{а} / T_{а}','1 956,9 / 2 229,9'],
   ['Коэффициент тепловой эффективности экранов','ψ_{т}','0,420'],['Зольность рабочей массы, %','A^{р}','27,0'],
   ['Коэффициент N для твёрдого топлива','N','9200'],['Температура газов за топкой, принятая в п. 3.10, °С','ϑ″_{т}','1110'],
   ['Температура начала деформации золы, °С','t_{1}','1130']]),
 ('p','Температура газов на выходе из топки определяется по формуле (3.54) [2]:'),
 ('img',110),
 ('p','Часть величин, входящих в (7), определяется только конструкцией топки и топливом и в ходе приближений не меняется. Они вычисляются один раз.'),
 ('p','Средняя длина пути луча – эффективная толщина излучающего слоя топки (3.49):'),
 ('f',r'S=\dfrac{3{,}6\,V_{\mathrm{т}}}{F_{\mathrm{ст}}}=\dfrac{3{,}6\cdot 905{,}1}{656{,}5}=%s\ \mathrm{м}'%c(S,3)),
 ('p','Высота факела, отсчитываемая от середины холодной воронки до середины выходного газового окна:'),
 ('f',r'h_{\mathrm{т}}^{\prime}=h_{\mathrm{т}}-\dfrac{h_{\mathrm{го}}^{\prime}}{2}=17{,}092-\dfrac{6{,}12}{2}=%s\ \mathrm{м}'%c(htp,3)),
 ('p','Относительная высота размещения горелок (3.33) [2] при средней высоте двух ярусов горелок h_{гор} = 2,763 м:'),
 ('f',r'X_{\mathrm{т}}=\dfrac{h_{\mathrm{гор}}}{h_{\mathrm{т}}^{\prime}}=\dfrac{2{,}763}{%s}=%s'%(c(htp,3),c(X,3))),
 ('p','Параметр M, характеризующий положение максимума температур по высоте факела; уголь высокореакционный, приведённая зольность A_{п} = 1,51 %·кг/МДж < 2, поэтому по (3.30) [2]:'),
 ('f',r'M=0{,}59-0{,}5\,X_{\mathrm{т}}=0{,}59-0{,}5\cdot %s=%s'%(c(X,3),c(M,3))),
 ('p','Удельная тепловая нагрузка поверхности экранов (3.26):'),
 ('img',111),
 ('p','Первое приближение. Принимается температура газов за топкой ϑ″_{т} = 1110 °С, заданная при конструктивном расчёте:'),
]+step(I1,True)+[
 ('img',112),
 ('p','Отклонение расчётной температуры от принятой:'),
 ('f',r'\Delta\vartheta=|\vartheta_{\mathrm{т}}^{\prime\prime}-\vartheta_{\mathrm{т.р}}^{\prime\prime}|=|1110-%s|=%s'%(c(I1['tc'],1),c(I1['d'],1))+DEG+r'\ >\ 30'+DEG),
 ('p','Отклонение превышает 30 °С, и расчёт необходимо повторить. Топка заданных размеров охлаждает газы сильнее, чем предполагалось, поэтому во втором приближении принимается более низкая температура ϑ″_{т} = 1005 °С, близкая к полученной. Величины S, X_{т}, M и q_{F} сохраняются, заново определяются коэффициенты ослабления лучей и степени черноты.'),
 ('p','Второе приближение, ϑ″_{т} = 1005 °С.'),
]+step(I2,False)+[
 ('img',113),
 ('p','Отклонение расчётной температуры от принятой во втором приближении:'),
 ('img',114),
 ('p','Отклонение 0,6 °С значительно меньше допустимого, расчёт сошёлся, и далее температура газов на выходе из топки принимается ϑ″_{т} = 1005 °С. Она на 125 °С ниже температуры начала деформации золы t_{1} = 1130 °С, поэтому зола затвердевает раньше, чем газы достигают ширм, и шлакование ширмовых поверхностей не грозит. Результаты двух приближений сопоставлены в таблице 6.'),
 ('tbl','Таблица 6 – Сопоставление приближений поверочного расчёта топки',['Величина','1-е приближение','2-е приближение'],[
   ['Принятая температура ϑ″_{т}, °С','1110','1005'],['Абсолютная температура T″_{т}, К','1383','1278'],
   ['k_{г}, 1/(м·МПа)',t(I1['kg'],3),t(I2['kg'],3)],['k_{зл}, 1/(м·МПа)',t(I1['kzl'],3),t(I2['kzl'],3)],
   ['k, 1/(м·МПа)',t(I1['k'],3),t(I2['k'],3)],['Степень черноты факела ε_{ф}',t(I1['ef'],3),t(I2['ef'],3)],
   ['Степень черноты топки ε_{т}',t(I1['et'],3),t(I2['et'],3)],['Комплекс Π',t(I1['P'],3),t(I2['P'],3)],
   ['Расчётная температура ϑ″_{т.р}, °С',t(I1['tc'],1),t(I2['tc'],1)],['Отклонение Δϑ, °С',t(I1['d'],1),t(I2['d'],1)]]),
 ('p','При понижении температуры газов коэффициенты ослабления лучей растут, факел становится «чернее», и расчётная температура уменьшается – этим объясняется быстрая сходимость приближений.'),
 ('p','Энтальпия продуктов сгорания на выходе из топки (2.16) и теплота, переданная экранам излучением (3.22):'),
 ('img',115),('img',116),
 ('p','Доля полезного тепловыделения, воспринятая экранами топки, полное тепловосприятие экранов и средняя тепловая нагрузка их поверхности:'),
 ('f',r'\dfrac{Q_{\mathrm{л}}}{Q_{\mathrm{т}}}=\dfrac{10\ 195{,}7}{19\ 508{,}2}=%s'%c(Ql/Qt,3)),
 ('f',r'Q_{\mathrm{экр}}=B\,Q_{\mathrm{л}}=8{,}859\cdot 10\ 195{,}7=%s\ \mathrm{кВт}'%c(B*Ql,0)),
 ('f',r'q_{\mathrm{экр}}=\dfrac{B\,Q_{\mathrm{л}}}{F_{\mathrm{ст}}}=\dfrac{8{,}859\cdot 10\ 195{,}7}{656{,}5}=%s\ \mathrm{кВт/м}^2'%c(B*Ql/F,1)),
 ('p','Таким образом, в топке излучением передаётся около %d %% полезного тепловыделения (≈ %s МВт), газы покидают её с температурой 1005 °С, а оставшаяся теплота воспринимается ширмами и конвективными поверхностями, расчёт которых приведён в следующих разделах.'%(round(Ql/Qt*100),t(B*Ql/1000,1))),
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
textP=[s for a,b,s in items[i0+1:i1] if txt(s).startswith('Удельная тепловая нагрузка поверхности экранов')][0]
formP=old[111]
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
