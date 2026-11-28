import sys, re
sys.path.insert(0,'/home/user/meikursovie/инструменты')
from pravki import Doc, build_pdf, fix_toc, formula_png
from calc06 import solve
from texts06 import P, f
from tpl06 import build
R=solve(0.12); sh=R['sh']; kp=R['kp']
d=Doc('../k7.docx')
x=d.xml
for i in sorted(P,reverse=True):
    a,b,s=d.blocks[i]; ppr=re.search(r'<w:pPr>.*?</w:pPr>',s); ppr=ppr.group(0) if ppr else ''
    x=x[:a]+'<w:p>'+ppr+Doc.runs(P[i])+'</w:p>'+x[b:]
d.xml=x; d._reindex()
d.replace_text('Вариант 1','Вариант 10'); d.replace_text('Беленьков А.','Ретивов О.')
E_=build(R)
for k,t in E_.items():
    formula_png(t,f'new/{k}.png'); d.replace_image(k,f'new/{k}.png')
d.replace_image(8,'new/10.png',keep_width=True); d.replace_image(9,'new/11.png',keep_width=True)
d.save('out.docx')
import docx
D=docx.Document('out.docx')
def setc(c,t):
    rs=[r for r in c.paragraphs[0].runs if r.text]; rs[0].text=t
    for r in rs[1:]: r.text=''
def fill(t,rows):
    for r,vals in zip(t.rows[1:],rows):
        for c,v in zip(r.cells,vals):
            if v is not None: setc(c,v)
T=D.tables
fill(T[0],[['10',None,None,'0,12',None,None]])
Qsh=R['Qshl']+sh['Qb']
fill(T[5],[[None,None,'2 001,2','1 108,9',f(kp['Fp'],1)],[None,None,f(R['Ql'],1),f(Qsh,1),f(R['Qk'],1)],
           [None,None,f(R['dtT'],1),f(sh['dt'],1),f(kp['dt'],1)],[None,None,f(R['kT']),f(sh['k']),f(kp['k'])],
           [None,None,f(R['ql']),f(R['B']*Qsh/1108.9),f(kp['q'])],[None,None,f(R['wT']),f(sh['w']),f(kp['w'])],[None,None,None,None,f(kp['wr'],0)]])
fill(T[6],[[None,None,f(R['q2'],3)],[None,None,f(R['eta'])],[None,None,f(R['B'],3)],[None,None,f(R['Qt'],0)],[None,None,f(R['tha'],0)],
           [None,None,f(R['tht'],0)],[None,None,f(R['Ql'],0)],[None,None,f(R['ql'],1)],[None,None,f(R['qf'])],[None,None,f(R['tT'],1)],[None,None,f(R['tgv'],1)]])
fill(T[7],[[None,f(R['tha'],0),f(R['tht'],0),'315',f(R['tT'],0),f(R['Ql'],0),'2 001'],
           [None,f(R['tht'],0),f(sh['th2'],0),f(R['tsh1'],0),f(sh['t2'],0),f(Qsh,0),'1 109'],
           [None,f(sh['th2'],0),f(R['th1k'],0),'–','–',f(R['Qpk'],0),'–'],
           [None,f(R['th1k'],0),f(R['th2k'],0),f(R['tk1'],0),'545',f(R['Qk'],0),f(kp['Fp'],0)],
           [None,f(R['th2k'],0),f(R['th2n'],0),'310','545',f(R['Qn'],0),f(R['Fn'],0)+' (9 400)'],
           [None,f(R['th2n'],0),f(R['th2e'],0),'265',f(R['te2'],0),f(R['Qe'],0),f(R['F1e']*R['zre'],0)],
           [None,f(R['th2e'],0),'150','70',f(R['tgv'],0),f(R['Qvp'],0),'2 × '+f(R['Fv'],0)]])
D.save('out.docx')
pdf=build_pdf('out.docx'); print(fix_toc('out.docx',pdf)); build_pdf('out.docx')
