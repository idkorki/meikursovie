import docx, re, io, zipfile, sys
from PIL import Image
from spec2 import build2, c
F='/home/user/meikursovie/курсовые котлы/6кк/6кк_Поверочный_расчёт_БКЗ-210-140Ф_вар9.docx'
E0,E,v=build2('new'); r=v['r']; hx=r['hx']; gp=r['gp']; p=v['p']
f=lambda x,n: f'{x:,.{n}f}'.replace(',',' ').replace('.',',')
d=docx.Document(F); P=d.paragraphs
def rset(i,repl):
    runs=P[i].runs
    for k,(old,new) in repl.items():
        assert old in runs[k].text,(i,k,old,runs[k].text); runs[k].text=runs[k].text.replace(old,new)
rset(273,{2:(' = 0,85 м. Отметки нижнего и второго ярусов над серединой холодной воронки и средняя высота горелок (ярусы одинаковой производительности):',
  ' = 0,85 м. Горелки на каждой боковой стене стоят треугольником вершиной вниз: в нижнем ярусе одна, в верхнем – две, всего в нижнем ярусе nниж = 2 горелки, в верхнем n2 = 4. Отметки ярусов над серединой холодной воронки и средняя высота горелок, взвешенная по числу горелок в ярусах (горелки одинаковой производительности):')})
rset(302,{4:(' = 1 011 °С',' = 1 039 °С'),10:(' = 947,0 м',' = %s м'%f(p['V'],1))})
rset(317,{0:('S = 3,6·947,0/678,2 = 5,027 м','S = 3,6·%s/%s = %s м'%(f(p['V'],1),f(p['F'],1),f(p['S'],3))),
          2:(' = 2,763/(17,750 − 3,06) = 0,188, M = 0,496',' = %s/(%s − 3,06) = %s, M = %s'%(f(v['hg'],3),f(p['ht'],3),f(p['X'],3),f(p['M'],3))),
          4:('k = 3,407','k = %s'%f(p['k'],3)),6:(' = 0,820',' = %s'%f(p['ef'],3)),8:(' = 0,915',' = %s'%f(p['et'],3))})
rset(430,{0:('с 570,0 до 422,4','с %s до %s'%(f(r['thg'],1),f(r['thx'],1)))})
rset(468,{0:('t′ = 422,62 °С','t′ = %s °С'%f(r['t_g1'],2)),})
P[468].runs[0].text=P[468].runs[0].text.replace('с 840,0 до 570,0','с 840,0 до %s'%f(r['thg'],1))
rset(535,{0:('215 → 235,15 °С, газы остывают 422,4','215 → %s °С, газы остывают %s'%(f(r['tek2'],2),f(r['thx'],1)))})
rset(623,{0:('высота 17,75 м; объём 947 м','высота %s м; объём %s м'%(f(p['ht'],2),f(p['V'],0))),2:('678 м','%s м'%f(p['F'],0))})
rset(625,{0:('3 017 м','%s м'%f(gp['F'],0)),2:('2 356 м','%s м'%f(hx['F'],0)),4:('484 м','%s м'%f(r['Fek'],0))})
rset(626,{0:('235,1 °С','%s °С'%f(r['tek2'],1))})
# table 5
for t in d.tables:
    if t.rows[0].cells[0].text=='Поверхность':
        vals={'Горячий пакет КПП':('840 → %s'%f(r['thg'],0),f(r['Qgpp'],1)),'Холодный пакет КПП':('%s → %s'%(f(r['thg'],0),f(r['thx'],0)),f(r['Qhpp'],1)),
              'Экономайзер':('%s → 353'%f(r['thx'],0),f(r['Qek'],1))}
        for row in t.rows:
            n=row.cells[0].text
            if n in vals:
                for ci,val in zip((1,2),vals[n]):
                    runs=[x for x in row.cells[ci].paragraphs[0].runs if x.text]; print(n,runs[0].text,'->',val); runs[0].text=val
                    for x in runs[1:]: x.text=''
d.save('/tmp/claude-0/-home-user-meikursovie/9cc32649-d3ec-5a22-abdb-5578563dc433/scratchpad/k6out/tmp.docx')
# images
repl={k:f'new/{k}.png' for k in list(E0)+list(E)}
repl[109]='furnace_new.png'; repl[282]='qt_new.png'
zin=zipfile.ZipFile('/tmp/claude-0/-home-user-meikursovie/9cc32649-d3ec-5a22-abdb-5578563dc433/scratchpad/k6out/tmp.docx')
xml=zin.read('word/document.xml').decode('utf8'); rels=zin.read('word/_rels/document.xml.rels').decode('utf8')
rid={b.replace('media/image','').replace('.png',''):a for a,b in re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"',rels)}
for k,fn in repl.items():
    rr=rid[str(k)]
    blks=re.findall(r'<w:drawing>(?:(?!</w:drawing>).)*r:embed="%s"(?:(?!</w:drawing>).)*</w:drawing>'%rr,xml,re.S)
    ow,oh=Image.open(f'../k6/word/media/image{k}.png').size; nw,nh=Image.open(fn).size
    for blk in set(blks):
        cx,cy=map(int,re.search(r'<wp:extent cx="(\d+)" cy="(\d+)"',blk).groups())
        if k in (109,282): ncx=cx; ncy=round(cx*nh/nw)
        else: ncx=round(cx*nw/ow); ncy=round(cy*nh/oh)
        xml=xml.replace(blk,blk.replace(f'cx="{cx}" cy="{cy}"',f'cx="{ncx}" cy="{ncy}"'))
buf=io.BytesIO(); zo=zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    data=zin.read(it.filename)
    if it.filename=='word/document.xml': data=xml.encode('utf8')
    m=re.match(r'word/media/image(\d+)\.png$',it.filename)
    if m and int(m.group(1)) in repl:
        k=int(m.group(1)); im=Image.open(repl[k]); dpi=Image.open(f'../k6/word/media/image{k}.png').info.get('dpi',(300,300))
        b=io.BytesIO(); im.save(b,'PNG',dpi=tuple(round(x) for x in dpi)); data=b.getvalue()
    zo.writestr(it,data)
zo.close(); open(F,'wb').write(buf.getvalue()); print('ok',len(repl))
