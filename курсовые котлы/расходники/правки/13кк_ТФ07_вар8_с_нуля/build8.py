import sys, re
sys.path.insert(0,'/home/user/meikursovie/инструменты')
from pravki import Doc, build_pdf, fix_toc
from var8 import R, G8
from texts8 import P, f
from tpl import T
d=Doc('../k10.docx')
# абзацы: замена и удаление второго приближения (244..259)
DROP=set(range(244,260))
assert d.text(244).startswith('Второе приближение') and d.text(259).startswith('Теперь расхождение')
ops=sorted(set(P)|DROP, reverse=True)
x=d.xml
for i in ops:
    a,b,s=d.blocks[i]
    if i in DROP: x=x[:a]+x[b:]; continue
    ppr=re.search(r'<w:pPr>.*?</w:pPr>',s).group(0)
    x=x[:a]+'<w:p>'+ppr+Doc.runs(P[i])+'</w:p>'+x[b:]
d.xml=x; d._reindex()
GAS='Саратов – Москва'
d.replace_text('Надым – Пунга – Нижняя Тура – Свердловск – Челябинск',GAS,count=0)
d.replace_text('Вариант 4','Вариант 8'); d.replace_text('Ласточкин О.С.','Семенов О.К.')
d.replace_text('Данные варианта № 4','Данные варианта № 8')
d.replace_text(' = 0,05;',' = 0,08;'); d.replace_text(' = 20 °С.',' = 30 °С.')
# формулы и схемы
E=T(R,G8)
for k in E: 
    if k in range(83,92): continue
    d.replace_image(k,f'new/{k}.png')
d.replace_image(10,'new/10.png',keep_width=True); d.replace_image(11,'new/11.png',keep_width=True)
import re as _re
d.xml=_re.sub(r'<w:t>\(1\.(6[6-9]|7[0-6])\)</w:t>',lambda m:'<w:t>(1.%d)</w:t>'%(int(m.group(1))-7),d.xml); d._reindex()
d.save('out.docx')
# таблицы
import docx
D=docx.Document('out.docx')
def setc(cell,text):
    p=cell.paragraphs[0]; rs=[r for r in p.runs if r.text]
    rs[0].text=text
    for r in rs[1:]: r.text=''
for t in D.tables:
    h=[c.text for c in t.rows[0].cells]
    if h[0]=='CH4':
        for c,v in zip(t.rows[1].cells,['84,50','3,80','1,90','0,90','0,30','–','0,80','7,80']): setc(c,v)
    elif h[0].startswith('Qрн'):
        for c,v in zip(t.rows[-1].cells,['35,80','9,52','1,04','7,60','2,10','10,74','32 370','39 820']): setc(c,v)
    elif h[0]=='Величина' and len(h)==5:   # 2.2
        sh=R['sh']; kp=R['kp']
        vals={'Поверхность':[f(1861.9,1),f(1041.4,1),f(kp['Fp'],1)],'Тепловосприятие':[f(R['Ql'],1),f(R['Qlsh']+R['Qsb2'],1),f(R['Qk'],1)],
              'Температурный':['–',f(sh['dt'],1),f(kp['dt'],1)],'Коэффициент':['–',f(sh['k']),f(kp['k'])],
              'Тепловой':[f(R['ql'],1),f(sh['k']*sh['dt']/1000),f(kp['q'])],'Скорость':['–',f(sh['w']),f(kp['w'])],'Массовая':['–','1 788',f(kp['wr'],0)]}
        for row in t.rows[1:]:
            key=row.cells[0].text.split()[0].rstrip(',')
            for c,v in zip(row.cells[2:],vals[key]): setc(c,v)
    elif h[0]=='Величина' and len(h)==3 and t.rows[1].cells[1].text.strip()=='q2':   # 2.3
        m={'q2':f(R['q2'],3),'ηк':f(R['eta']),'B':f(R['B'],3),'Qт':f(R['Qt'],0),'ϑа':f(R['tha'],0),'ϑ″т':f(R['tht'],0),'Qл':f(R['Ql'],0),'qл':f(R['ql'],1),'qf':f(R['qf']/1000),'qV':f(R['qV'],1),'t″т':f(R['tT'],1)}
        for row in t.rows[1:]:
            k=row.cells[1].text.strip()
            if k in m: setc(row.cells[2],m[k])
            else: print('2.3 row?',[c.text for c in row.cells])
    elif h[0]=='Поверхность' and len(h)==7:  # 2.4
        rows={'Топка':[f(R['tha'],0),f(R['tht'],0),'315',f(R['tT'],0),f(R['Ql'],0),'1 862'],
              'ШП':[f(R['tht'],0),f(R['th2b'],0),f(R['tsh1'],0),f(R['t2b'],0),f(R['Qlsh']+R['Qsb2'],0),'1 041'],
              'Поворотная камера':[f(R['th2b'],0),f(R['th1k'],0),'–','–',f(R['Qpk'],0),'–'],
              'КПВД':[f(R['th1k'],0),f(R['th2k'],0),f(R['tk1'],0),'545',f(R['Qk'],0),f(R['kp']['Fp'],0)]}
        for row in t.rows[1:]:
            for c,v in zip(row.cells[1:],rows[row.cells[0].text.strip()]): setc(c,v)
D.save('out.docx')
pdf=build_pdf('out.docx'); print(fix_toc('out.docx',pdf)); pdf=build_pdf('out.docx'); print(pdf)
