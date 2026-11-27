import docx, math, copy, re, shutil
from docx.shared import Emu
exec(open('calc/hyd.py').read().split('base=')[0])
SRC='/home/user/meikursovie/курсовые тепло/3кт/Курсовая_Теплоснабжение_Владивосток.docx'
OUT='out/Курсовая_Теплоснабжение_Владивосток.docx'
d=docx.Document(SRC)
f2=lambda v,n=2: f'{v:.{n}f}'.replace('.',',')
def sp(v): # thousands with space
    s=f'{v:,.0f}'.replace(',',' '); return s
def setc(cell,text):
    p=cell.paragraphs[0]; rs=[r for r in p.runs if r.text]
    assert rs, cell.text
    old=rs[0].text; rs[0].text=text
    for r in rs[1:]: r.text=''
    return old
# ---- main line
Dys=[400,400,350,300,300,300,300,250]
H=100.0; rows=[]
for i,(l,Gr,Dy) in enumerate(zip(L,G,Dys)):
    SL=sum(L[i:]); Rl=rho*g*(H-20)/(2*SL*1.1); dpre=117e-3*Gr**0.38/Rl**0.19
    dd=din[Dy]; w=4*Gr/(rho*math.pi*dd*dd); Re=w*dd/nu; R=13.62e-6*Gr**2/dd**5.25
    n=math.ceil(l/step(Dy)); xi=n*(0.2 if Dy>=300 else 2.5)+extra[i]; le=60.7*dd**1.25*xi
    dp=R*(l+le); dH=dp/(rho*g); rows.append(dict(H0=H,Rl=Rl,dpre=dpre,d=dd,Dy=Dy,w=w,Re=Re,R=R,n=n,xi=xi,le=le,dp=dp,dH=dH,H1=H-2*dH)); H-=2*dH
Hk=[100]+[r['H1'] for r in rows]
t5=d.tables[4]
r4=rows[3]
col={4:r4}
for j in range(4,9):
    r=rows[j-1]; c=lambda k: t5.rows[k].cells[j]
    setc(c(4),f2(r['H0'])); setc(c(5),f2(r['Rl'],1)); setc(c(6),f"{r['dpre']*1000:.0f}"); setc(c(16),f2(r['H1']))
    if j==4:
        setc(c(7),f"{r['d']*1000:.0f} ({r['Dy']})"); setc(c(8),f2(r['w'])); setc(c(9),f2(r['Re']/1e6)); setc(c(10),f2(r['R'],1))
        setc(c(11),str(r['n'])); setc(c(12),f2(r['xi'])); setc(c(13),f2(r['le'],1)); setc(c(14),sp(r['dp'])); setc(c(15),f2(r['dH']))
# ---- branches
def br(l,Dy,Gb=34.40):
    dd=din[Dy]; n=math.ceil(l/step(Dy)); xi=n*(0.2 if Dy>=300 else 2.5)+2.5
    le=60.7*dd**1.25*xi; R=13.62e-6*Gb*Gb/dd**5.25; w=4*Gb/(rho*math.pi*dd*dd)
    return dd,w,R,R*(l+le)/(rho*g)
t6=d.tables[5]
brs=[(109,175,1),(None,None,2),(109,175,3),(109,175,4),(113,175,5),(113,175,6),(113,175,7),(113,200,8),(194,250,8)]
Hu={}
for i,(l,Dy,k) in enumerate(brs):
    row=t6.rows[i+1]
    if l is None:
        Hu[i]=None; continue
    dd,w,R,dH=br(l,Dy)
    if i>=7:
        setc(row.cells[3],f"{dd*1000:.0f} ({Dy})"); setc(row.cells[4],f2(w)); setc(row.cells[5],f2(R,1)); setc(row.cells[6],f2(dH))
    if k>=4:
        setc(row.cells[7],f2(Hk[k])); setc(row.cells[8],f2(Hk[k]-2*dH))
    Hu[i]=Hk[k]-2*dH
print('Hu',{k:round(v,2) for k,v in Hu.items() if v})
HuI7,HuI8=Hu[7],Hu[8]
# ---- table 7
t7=d.tables[6]
for k in range(4,9):
    row=t7.rows[k+1]; h=Hk[k]
    setc(row.cells[2],f2(70+h/2)); setc(row.cells[3],f2(70-h/2)); setc(row.cells[4],f2(h))
# ---- table 8
q={175:(70,83),200:(77,93),250:(92,106),300:(105,121),350:(118,135),400:(130,148)}
kq=((78.00+53.45)/2-6.3-52.5)/(65-52.5)
t8=d.tables[7]
segs=list(zip([1876,120,116,193,83,295,194,198],Dys))+[(109,175),(392,250),(109,175),(109,175),(113,175),(113,175),(113,175),(113,200),(194,250)]
S=V=0
for i,(l,D) in enumerate(segs):
    qn=q[D][0]+(q[D][1]-q[D][0])*kq; ql=qn*l/1000; v=2*math.pi*din[D]**2/4*l; S+=ql; V+=v
    row=t8.rows[i+1]
    if i in (3,15,16):
        setc(row.cells[1],str(D)); setc(row.cells[3],f2(q[D][0],1)); setc(row.cells[4],f2(q[D][1],1)); setc(row.cells[5],f2(qn,1)); setc(row.cells[6],f2(ql)); setc(row.cells[7],f2(v))
last=t8.rows[-1]; setc(last.cells[6],f2(S)); setc(last.cells[7],f2(V,1))
print('S V',S,V)
# ---- table 9
Qold=1.15*519.5405; Qnew=1.15*S; kk=Qnew/Qold
t9=d.tables[8]
for row in t9.rows[1:]:
    c=[x.text for x in row.cells]; num=lambda s: float(s.replace(',','.'))
    t1,t2,Gt=num(c[1]),num(c[2]),num(c[3])
    QS,Qp,Qo=[num(c[j])*kk for j in (4,5,6)]
    dt1=Qp/(Gt/3.6*4.19); dt2=Qo/(Gt/3.6*4.19)
    # consistency check with old
    assert abs(num(c[7])-num(c[5])/(Gt/3.6*4.19))<0.006, c
    new=[f2(QS,1),f2(Qp,1),f2(Qo,1),f2(dt1),f2(dt2)]
    if [c[j] for j in range(4,9)]!=new: print('T9',c[0],[c[j] for j in range(4,9)],'->',new)
    for j,v in zip(range(4,9),new): setc(row.cells[j],v)
    # tau_i: recompute delta and adjust only if old rounding pattern shows shift
    o1=num(c[9])-(t1+num(c[7])); n1=round(t1+dt1+o1,1)
    o2=num(c[10])-(t2-num(c[8])); n2=round(t2-dt2+o2,1)
    if f2(n1,1)!=c[9] or f2(n2,1)!=c[10]: print('tau change?',c[0],c[9],n1,c[10],n2)
# ---- table 10
t10=d.tables[9]
def t10set(label,val):
    for row in t10.rows:
        if row.cells[0].text.startswith(label): print('T10',label,setc(row.cells[1],val),'->',val); return
    raise KeyError(label)
t10set('Напор у последнего абонента',f2(HuI8))
t10set('Годовые потери теплоты в сетях','6 111')
# ---- paragraphs
P=d.paragraphs
def runs(p): return [r for r in p.runs]
p=P[201]; rs=runs(p)
assert rs[2].text.startswith(' = 20 м. Поэтому')
rs[2].text=' = 20 м. Поэтому диаметр участка 7 с наибольшей удельной потерей давления увеличен на один типоразмер, с D'
rs[6].text=('300. После этого напор в концевой камере К8 вырос до 26,81 м, т. е. превысил рекомендуемые для конца '
 'главной магистрали 20–25 м; избыточный напор пришлось бы гасить дросселированием у абонентов. Поэтому диаметр '
 'участка 4 (К3–К4) уменьшен на один типоразмер – с D')
# append subscript runs: "у" + "350 до D" + "у" + "300 ..."
def addrun(after,text,sub=False):
    new=copy.deepcopy(rs[5]._r if sub else rs[6]._r)
    for t in new.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
        t.text=text; t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    after.addnext(new); return new
r4d=rows[3]
a=addrun(rs[6]._r,'у',True)
a=addrun(a,'350 до D')
a=addrun(a,'у',True)
a=addrun(a,(f"300 (скорость {f2(r4d['w'])} м/с, R'л = {f2(r4d['R'],1)} Па/м – в допустимых пределах), и расчёт повторён "
  'с сохранением остальных диаметров. Вследствие этих двух поправок значение d предв. в табл. 5 у участка 4 больше принятого диаметра, '
  'а у участков 7 и 8 – меньше.'))
p=P[202]; rs=runs(p)
rs[2].text=(f' = {f2(Hk[8])} м, что находится в пределах 20–25 м. Напор у абонентов, присоединённых к концевой камере '
 f'(ответвления рассчитаны в п. 4.3): И7 – {f2(HuI7)} м, И8 – {f2(HuI8)} м, что не ниже требуемых H')
rs[4].text=f" = 20 м. Скорости воды на участках составляют 1,24–{f2(max(r['w'] for r in rows))} м/с. Все участки работают в квадратичной области сопротивления."
p=P[204]; rs=[r for r in p.runs if r.text]
rs[-1].text=rs[-1].text+(' Из-за снижения напора в концевой камере К8 условие Hу ≥ 20 м для ответвлений от неё '
  'выполняется только при увеличенных диаметрах: К8–И7 – D')
last=rs[-1]._r
def addrun2(after,text,sub,tmpl_plain,tmpl_sub):
    new=copy.deepcopy(tmpl_sub if sub else tmpl_plain)
    for t in new.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
        t.text=text; t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    after.addnext(new); return new
tp=P[201].runs[0]._r; ts=P[201].runs[1]._r
a=addrun2(last,'у',True,tp,ts); a=addrun2(a,'200, К8–И8 – D',False,tp,ts); a=addrun2(a,'у',True,tp,ts); a=addrun2(a,'250.',False,tp,ts)
print(P[201].text); print(P[202].text); print(P[204].text)
d.save(OUT)

# ---- images
import zipfile, io
from PIL import Image
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
rels=open('d/word/_rels/document.xml.rels',encoding='utf8').read()
rid={b:a for a,b in re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"',rels)}
repl={80:'calc/piezo_new.png',84:'eq/new84.png',85:'eq/new85.png',86:'eq/new86.png',88:'eq/new88.png',89:'eq/new89.png',90:'eq/new90.png',91:'eq/new91.png'}
zin=zipfile.ZipFile(OUT); xml=zin.read('word/document.xml').decode('utf8')
for k,f in repl.items():
    r=rid[f'media/image{k}.png']
    m=re.search(r'<w:drawing>(?:(?!</w:drawing>).)*r:embed="%s"(?:(?!</w:drawing>).)*</w:drawing>'%r,xml,re.S); blk=m.group(0)
    cx,cy=map(int,re.search(r'<wp:extent cx="(\d+)" cy="(\d+)"',blk).groups())
    ow,oh=Image.open(f'd/word/media/image{k}.png').size; nw,nh=Image.open(f).size
    if k==80: ncx=cx; ncy=round(cx*nh/nw)
    else: ncx=round(cx*nw/ow); ncy=round(cy*nh/oh)
    nb=blk.replace(f'cx="{cx}" cy="{cy}"',f'cx="{ncx}" cy="{ncy}"')
    xml=xml.replace(blk,nb); print(k,cx,cy,'->',ncx,ncy)
buf=io.BytesIO(); zout=zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    data=zin.read(it.filename)
    if it.filename=='word/document.xml': data=xml.encode('utf8')
    mm=re.match(r'word/media/image(\d+)\.png$',it.filename)
    if mm and int(mm.group(1)) in repl:
        im=Image.open(repl[int(mm.group(1))]); b=io.BytesIO(); im.save(b,'PNG',dpi=(300,300) if int(mm.group(1))!=80 else (200,200)); data=b.getvalue()
    zout.writestr(it,data)
zout.close(); zin.close(); open(OUT,'wb').write(buf.getvalue())
print('saved')
