import re, math, io, zipfile, os, sys
sys.path.insert(0,'../kk')
from R import R
from PIL import Image
SRC='/home/user/meikursovie/курсовые котлы/2кк/2кк_Поверочный_расчёт_БКЗ-210-140Ф_вар33.docx'
c=lambda v,n: f'{v:,.{n}f}'.replace(',','X').replace('.','{,}').replace('X','\\ ')
t=lambda v,n: f'{v:,.{n}f}'.replace(',',' ').replace('.',',')
DEG=r'\ ^{\circ}\;\mathrm{C}'
Ta=2275.0; psi=0.934*0.45; Ap=32.2; V=907.6; F=657.7; ht=17.13; hg=2.7625; B=8.195; Qt=21146.0; N=9200
S=3.6*V/F; htp=ht-6.12/2; X=hg/htp; M=0.59-0.5*X; qF=B*Qt/F
def it(th):
    T=th+273; kg=0.92*(4/S)**0.54*1470/T; kzl=2.96*(Ap/35)**1.33*(1470/T)**0.67; k=kg+kzl+0.2
    ef=1-math.exp(-k*0.1*S); et=ef/(ef+(1-ef)*psi); P=et*psi*Ta**2/(N*qF); tc=round(Ta*(1-M*P**0.6)-273,1)
    return dict(th=th,T=T,kg=kg,kzl=kzl,k=k,ef=ef,et=et,P=P,tc=tc,d=abs(th-tc))
I1,I2=it(1075),it(990)
Ql=11462.8
def iter_blocks(I,n):
    L=[('f',r'T_{\mathrm{т}}^{\prime\prime}=\vartheta_{\mathrm{т}}^{\prime\prime}+273=%d+273=%d\ \mathrm{K}'%(I['th'],I['T'])),
     ('p','Коэффициент ослабления лучей трёхатомными газами (3.44) [2] при k′_{г} = 0,92 для каменных углей:'),
     ('f',r'k_{\mathrm{г}}=k_{\mathrm{г}}^{\prime}\left(\dfrac{4}{S}\right)^{0{,}54}\dfrac{1470}{T_{\mathrm{т}}^{\prime\prime}}=0{,}92\cdot \left(\dfrac{4}{%s}\right)^{0{,}54}\dfrac{1470}{%d}=%s'%(c(S,3),I['T'],c(I['kg'],3))),
     ('p','Коэффициент ослабления лучей золовыми частицами (3.45) [2], k′_{зл} = 2,96 при размоле в молотковых мельницах, зольность A^{р} = 32,2 %:'),
     ('f',r'k_{\mathrm{зл}}=k_{\mathrm{зл}}^{\prime}\left(\dfrac{A^{\mathrm{р}}}{35}\right)^{1{,}33}\left(\dfrac{1470}{T_{\mathrm{т}}^{\prime\prime}}\right)^{0{,}67}=2{,}96\cdot \left(\dfrac{32{,}2}{35}\right)^{1{,}33}\left(\dfrac{1470}{%d}\right)^{0{,}67}=%s'%(I['T'],c(I['kzl'],3))),
     ('p','Суммарный коэффициент ослабления лучей топочной средой (3.43) [2], для частиц кокса k_{к} = 0,2:'),
     ('f',r'k=k_{\mathrm{г}}+k_{\mathrm{зл}}+k_{\mathrm{к}}=%s+%s+0{,}2=%s'%(c(I['kg'],3),c(I['kzl'],3),c(I['k'],3))),
     ('p','Степень черноты факела по закону Бугера (3.42) при давлении в топке p = 0,1 МПа:'),
     ('f',r'\varepsilon_{\mathrm{ф}}=1-e^{-kpS}=1-e^{-%s\cdot 0{,}1\cdot %s}=%s'%(c(I['k'],3),c(S,3),c(I['ef'],3))),
     ('p','Степень черноты топки с учётом тепловой эффективности экранов (3.41):'),
     ('f',r'\varepsilon_{\mathrm{т}}=\dfrac{\varepsilon_{\mathrm{ф}}}{\varepsilon_{\mathrm{ф}}+(1-\varepsilon_{\mathrm{ф}})\psi_{\mathrm{т}}}=\dfrac{%s}{%s+(1-%s)\cdot 0{,}420}=%s'%(c(I['ef'],3),c(I['ef'],3),c(I['ef'],3),c(I['et'],3))),
     ('p','Безразмерный комплекс, входящий в формулу (7), и его степень:'),
     ('f',r'\Pi=\dfrac{\varepsilon_{\mathrm{т}}\,\psi_{\mathrm{т}}\,T_{\mathrm{а}}^2}{N\,q_F}=\dfrac{%s\cdot 0{,}420\cdot 2\ 275{,}0^2}{9200\cdot %s}=%s;\qquad \Pi^{0{,}6}=%s'%(c(I['et'],3),c(qF,1),c(I['P'],3),c(I['P']**0.6,3))),
     ('p','Расчётная температура газов на выходе из топки по (7):')]
    return L
blocks=[
 ('p','Поверочный расчёт выполняется для топки окончательных размеров, полученных в п. 3.10. По известным объёму топки, площади её стен, положению горелок и тепловой эффективности экранов находится действительная температура газов на выходе из топки ϑ″_{т} и сравнивается с температурой, принятой при конструктивном расчёте. Если они различаются более чем на 30 °С, расчёт повторяется с уточнённой температурой [2]. Исходные данные приведены в таблице 5.'),
 ('tbl','Таблица 5 – Исходные данные для поверочного расчёта топки',['Величина','Обозначение','Значение'],[
   ['Объём топочной камеры, м³','V_{т}',t(V,1)],['Площадь стен топки, м²','F_{ст}',t(F,1)],['Высота топки, м','h_{т}',t(ht,3)],
   ['Ширина фронта / глубина топки, м','a_{т} / b_{т}','10,404 / 6,12'],['Высота газового окна, м','h′_{го}','6,12'],
   ['Средняя высота горелок, м','h_{гор}',t(hg,3)],['Расчётный расход топлива, кг/с','B',t(B,3)],
   ['Полезное тепловыделение в топке, кДж/кг','Q_{т}','21 146,0'],['Адиабатная температура, °С / К','ϑ_{а} / T_{а}','2 002,0 / 2 275,0'],
   ['Коэффициент тепловой эффективности экранов','ψ_{т}','0,420'],['Зольность рабочей массы, %','A^{р}','32,2'],
   ['Коэффициент для твёрдого топлива','N','9200'],['Температура газов на выходе, принятая в п. 3.10, °С','ϑ″_{т}','1075']]),
 ('p','Температура газов на выходе из топки окончательных размеров находится по (3.54) [2]:'),
 ('img',111),
 ('p','Геометрические характеристики топки. Эффективная толщина излучающего слоя для топки окончательных размеров (3.49):'),
 ('f',r'S=\dfrac{3{,}6\,V_{\mathrm{т}}}{F_{\mathrm{ст}}}=\dfrac{3{,}6\cdot 907{,}6}{657{,}7}=%s\ \mathrm{м}'%c(S,3)),
 ('p','Расчётная высота топки – от середины холодной воронки до середины выходного газового окна:'),
 ('f',r'h_{\mathrm{т}}^{\prime}=h_{\mathrm{т}}-\dfrac{h_{\mathrm{го}}^{\prime}}{2}=17{,}130-\dfrac{6{,}12}{2}=%s\ \mathrm{м}'%c(htp,3)),
 ('p','Относительная высота расположения горелок (3.33) [2]; горелки размещены в два яруса, средняя высота h_{гор} = 2,763 м (п. 3.10):'),
 ('f',r'X_{\mathrm{т}}=\dfrac{h_{\mathrm{гор}}}{h_{\mathrm{т}}^{\prime}}=\dfrac{2{,}763}{%s}=%s'%(c(htp,3),c(X,3))),
 ('p','Параметр M, учитывающий положение ядра факела по высоте топки, для высокореакционных каменных углей (3.30) [2]:'),
 ('f',r'M=0{,}59-0{,}5\,X_{\mathrm{т}}=0{,}59-0{,}5\cdot %s=%s'%(c(X,3),c(M,3))),
 ('p','Удельная тепловая нагрузка поверхности экранов (3.26) – отношение полезного тепловыделения в топке к площади её стен:'),
 ('img',112),
 ('p','Первое приближение. Температура газов на выходе из топки принимается равной значению, заданному при конструктивном расчёте, ϑ″_{т} = 1075 °С:'),
]+iter_blocks(I1,1)+[
 ('img',113),
 ('p','Расхождение принятой и расчётной температур:'),
 ('f',r'\Delta\vartheta=|\vartheta_{\mathrm{т}}^{\prime\prime}-\vartheta_{\mathrm{т.р}}^{\prime\prime}|=|1075-%s|=%s'%(c(I1['tc'],1),c(I1['d'],1))+DEG+r'\ >\ 30'+DEG),
 ('p','Расхождение больше допустимых 30 °С, поэтому расчёт повторяется. Во втором приближении принимается ϑ″_{т} = 990 °С – ближайшее к полученному значению меньшее, кратное 10 °С. Геометрические характеристики S, X_{т}, M и тепловая нагрузка q_{F} от температуры не зависят и остаются прежними; пересчитываются коэффициенты ослабления лучей и степени черноты.'),
 ('p','Второе приближение, ϑ″_{т} = 990 °С:'),
]+iter_blocks(I2,2)+[
 ('img',114),
 ('p','Расхождение между принятой и расчётной температурами:'),
 ('img',115),
 ('p','Расхождение меньше 30 °С, уточнения расчёта не требуется; дальнейший расчёт ведётся при ϑ″_{т} = 990 °С. Эта температура ниже температуры начала деформации золы t_{1} = 1120 °С, шлакование ширм исключено. Результаты обоих приближений сведены в таблицу 6.'),
 ('tbl','Таблица 6 – Результаты поверочного расчёта топки',['Величина','1-е приближение','2-е приближение'],[
   ['Принятая температура ϑ″_{т}, °С','1075','990'],['Абсолютная температура T″_{т}, К','1348','1263'],
   ['Коэффициент ослабления лучей газами k_{г}',t(I1['kg'],3),t(I2['kg'],3)],['Коэффициент ослабления лучей золой k_{зл}',t(I1['kzl'],3),t(I2['kzl'],3)],
   ['Суммарный коэффициент ослабления k',t(I1['k'],3),t(I2['k'],3)],['Степень черноты факела ε_{ф}',t(I1['ef'],3),t(I2['ef'],3)],
   ['Степень черноты топки ε_{т}',t(I1['et'],3),t(I2['et'],3)],['Комплекс Π',t(I1['P'],3),t(I2['P'],3)],
   ['Расчётная температура ϑ″_{т.р}, °С',t(I1['tc'],1),t(I2['tc'],1)],['Расхождение Δϑ, °С',t(I1['d'],1),t(I2['d'],1)]]),
 ('p','Энтальпия газов на выходе из топки (2.16) и количество теплоты, переданное в топке излучением (3.22):'),
 ('img',116),('img',117),
 ('p','Доля полезного тепловыделения, воспринятая экранами топки, и средняя удельная тепловая нагрузка экранов по воспринятой теплоте:'),
 ('f',r'\dfrac{Q_{\mathrm{л}}}{Q_{\mathrm{т}}}=\dfrac{11\ 462{,}8}{21\ 146{,}0}=%s'%c(Ql/Qt,3)),
 ('f',r'q_{\mathrm{экр}}=\dfrac{B\,Q_{\mathrm{л}}}{F_{\mathrm{ст}}}=\dfrac{8{,}195\cdot 11\ 462{,}8}{657{,}7}=%s\ \mathrm{кВт/м}^2'%c(B*Ql/F,1)),
 ('p','Таким образом, около 54 % полезного тепловыделения передаётся излучением экранам топки, газы выходят из неё с температурой 990 °С, и остальная теплота воспринимается ширмами и конвективными поверхностями нагрева.'),
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
