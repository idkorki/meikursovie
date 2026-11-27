import sys, re
sys.path.insert(0,'/home/user/meikursovie/инструменты')
from pravki import Doc, build_pdf, fix_toc, formula_png
from PIL import Image
from v15 import P, TASK
from textsnv import T as TX, f
from tplnv import T
d=Doc('b7.docx')
x=d.xml
for i in sorted(TX,reverse=True):
    a,b,s=d.blocks[i]; ppr=re.search(r'<w:pPr>.*?</w:pPr>',s)
    ppr=ppr.group(0) if ppr else ''
    sz=re.search(r'<w:sz w:val="(\d+)"/>',s); sz=int(sz.group(1)) if sz else 28
    x=x[:a]+'<w:p>'+ppr+Doc.runs(TX[i],sz)+'</w:p>'+x[b:]
d.xml=x; d._reindex()
d.replace_text('Вариант 13','Вариант 15')
E_=T(P,TASK,'',30)
for k,t in E_.items():
    formula_png(t,f'new/{k}.png'); d.replace_image(int(k),f'new/{k}.png')
# формула Эрбса: две ветви
a=r'\dfrac{\bar{H}_d}{\bar{H}}=1{,}391-3{,}560\bar{K}_T+4{,}189\bar{K}_T^2-2{,}137\bar{K}_T^3,\quad \omega_s\leq 81{,}4^{\circ}'
b=r'\dfrac{\bar{H}_d}{\bar{H}}=1{,}311-3{,}022\bar{K}_T+3{,}427\bar{K}_T^2-1{,}821\bar{K}_T^3,\quad \omega_s>81{,}4^{\circ}'
formula_png(a,'new/18a.png'); formula_png(b,'new/18b.png')
A=Image.open('new/18a.png'); B=Image.open('new/18b.png'); C=Image.new('RGB',(max(A.width,B.width),A.height+B.height+10),'white'); C.paste(A,(0,0)); C.paste(B,(0,A.height+10)); C.save('new/18.png',dpi=(300,300))
d.replace_image(18,'new/18.png')
for k in (10,25,48,49): d.replace_image(k,f'new/{k}.png',keep_width=True)
d.save('out.docx')
import docx
D=docx.Document('out.docx')
def setc(cell,text):
    p=cell.paragraphs[0]; rs=[r for r in p.runs if r.text]
    if not rs: p.add_run(text); return
    rs[0].text=text
    for r in rs[1:]: r.text=''
MN=['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
NDAYS=[31,28,31,30,31,30,31,31,30,31,30,31]
ts=D.tables; rows=P['rows']; mt=lambda v,d: f(v,d).replace('-','–')
def fill(t,data):
    for r,vals in zip(t.rows[1:],data):
        for c,v in zip(r.cells,vals): setc(c,v)
fill(ts[0],[[MN[i],f(P['H'][i]),f(rows[i]['KT'],3),f(P['D'][i],1),mt(P['T'][i],1),f(P['rho'][i])] for i in range(12)]+[['Год',f(sum(P['H'])/12),'–',f(sum(P['D']),1),mt(sum(P['T'])/12,1),'–']])
fill(ts[1],[[MN[i],str(NDAYS[i]),f(P['D'][i],1),f(P['Qot'][i]/1000),f(P['Qgv'][i]/1000),f(P['L'][i]/1000)] for i in range(12)]+[['Год','365',f(sum(P['D']),1),f(sum(P['Qot'])/1000),f(sum(P['Qgv'])/1000),f(sum(P['L'])/1000)]])
fill(ts[2],[[MN[i],str(rows[i]['n']),mt(rows[i]['de'],1),f(rows[i]['H0']),f(rows[i]['KT'],3),f(rows[i]['hd'],3),f(rows[i]['Rb'],3),f(rows[i]['HT']),f(rows[i]['R'],3)] for i in range(12)])
fill(ts[3],[[MN[i],f(rows[i]['HbT']),f(rows[i]['HdT']),f(rows[i]['HrT']),f(rows[i]['thb'],1),f(rows[i]['Kb'],3),f(rows[i]['ta'],3)] for i in range(12)])
for t,a in zip(ts[4:7],(30,60,100)):
    m=P['res'][a]['mon']
    fill(t,[[MN[i],f(P['L'][i]/1000),f(m[i]['X'],3),f(m[i]['Y'],3),f(m[i]['f'],3),f(m[i]['Qs']/1000)] for i in range(12)]+[['Год',f(sum(P['L'])/1000),'–','–',f(P['res'][a]['F'],3),f(P['res'][a]['Qs']/1000)]])
Lt=sum(P['L'])/1000
fill(ts[7],[[str(a),f(Lt),f(P['res'][a]['Qs']/1000),f(Lt-P['res'][a]['Qs']/1000),f(P['res'][a]['F']*100,1),f(P['res'][a]['Qs']/1000/a)] for a in (30,60,100)])
for p in D.paragraphs:
    if p.text.startswith('Таблица 7 – Расчёт по f-методу для Ac = 120'):
        for r in p.runs:
            if '120' in r.text: r.text=r.text.replace('120','100')
D.save('out.docx')
pdf=build_pdf('out.docx'); print(fix_toc('out.docx',pdf)); build_pdf('out.docx')
