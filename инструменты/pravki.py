"""Правки готовых записок (docx) без исходного генератора.

Записки курсовых/расчёток собраны генераторами, которые лежат у пользователя на компьютере
(~/работы мэи/.../расходники/расчёты/...). Когда генератора нет под рукой, работу правят прямо в docx:

    from pravki import Doc, formula_png, num, DEG
    d = Doc('записка.docx')
    d.find('3.11 Поверочный расчёт топки')        # индекс блока (абзац или таблица) по началу текста
    d.image_ids_between(i0, i1)                   # номера картинок-формул внутри раздела
    d.replace_image(113, 'new113.png')            # заменить картинку, extent пересчитывается
    d.replace_section(i0, i1, blocks)             # заменить содержимое раздела списком блоков
    d.set_text_run(...), d.replace_text(old, new) # правка текста по runs
    d.save('out.docx')
    pdf = build_pdf('out.docx')                   # LibreOffice + инструменты/fc.conf
    fix_toc('out.docx', pdf)                      # номера страниц в СОДЕРЖАНИИ по факту

Блоки для replace_section:
    ('p', 'текст с индексами: X_{т}, A^{р}')     абзац как в записке (шаблон берётся из соседнего абзаца)
    ('f', r'q_F=\\dfrac{...}{...}=263{,}3')       формула mathtext -> картинка 300 dpi
    ('img', 112)                                  существующая картинка записки (по номеру imageNNN)
    ('tbl', 'Таблица 5 – ...', [шапка], [[строки]])

Формулы: matplotlib mathtext, шрифт Liberation Serif 14 pt, 300 dpi, pad 0,03 дюйма – так рисуют генераторы
(картинки совпадают по ширине до пикселя). Дробь крупно – \\dfrac, «°С» – DEG, тысячи – '19\\ 508{,}2' (num()).
"""
import io, os, re, math, shutil, subprocess, tempfile, zipfile
from copy import deepcopy

HERE = os.path.dirname(os.path.abspath(__file__))
FC_CONF = os.path.join(HERE, 'fc.conf')
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
DEG = r'\ ^{\circ}\;\mathrm{C}'          # «979,6 °C» как в формулах генератора котлов
DEG_THIN = r'\ ^{\circ}\,\mathrm{C}'     # вариант с узким пробелом (у части формул)

# ---------------------------------------------------------------- числа
def num(v, n, tex=True):
    """Число по-русски: запятая, пробел между тысячами. tex=True – для mathtext."""
    s = f'{v:,.{n}f}'
    if tex:
        return s.replace(',', 'X').replace('.', '{,}').replace('X', '\\ ')
    return s.replace(',', ' ').replace('.', ',')

# ---------------------------------------------------------------- формулы
_plt = None
def _pyplot():
    global _plt
    if _plt is None:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.rcParams.update({'mathtext.fontset': 'custom', 'mathtext.rm': 'Liberation Serif',
                             'mathtext.it': 'Liberation Serif:italic', 'mathtext.bf': 'Liberation Serif:bold',
                             'font.family': 'Liberation Serif'})
        _plt = plt
    return _plt

def formula_png(tex, out, fs=14, pad=0.03, dpi=300):
    """Нарисовать формулу (без $...$) в PNG. Возвращает (ширина, высота) в пикселях."""
    plt = _pyplot()
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, '$' + tex + '$', fontsize=fs)
    fig.savefig(out, dpi=dpi, bbox_inches='tight', pad_inches=pad, facecolor='white')
    plt.close(fig)
    from PIL import Image
    return Image.open(out).size

# ---------------------------------------------------------------- docx
def _esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def _txt(xml):
    return ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', xml))

class Doc:
    """docx как zip + document.xml; блоки верхнего уровня – абзацы и таблицы."""
    BLOCK = re.compile(r'<w:tbl>.*?</w:tbl>|<w:p[ >].*?</w:p>', re.S)

    def __init__(self, path):
        self.path = path
        z = zipfile.ZipFile(path)
        self.files = {i.filename: z.read(i.filename) for i in z.infolist()}
        self.infos = z.infolist()
        self.xml = self.files['word/document.xml'].decode('utf8')
        self.rels = self.files['word/_rels/document.xml.rels'].decode('utf8')
        self._reindex()

    # --- служебное
    def _reindex(self):
        start = self.xml.find('<w:body>')
        self.blocks = [(m.start(), m.end(), m.group(0)) for m in self.BLOCK.finditer(self.xml, start)]
        self.rid2target = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', self.rels))
        self.target2rid = {v: k for k, v in self.rid2target.items()}

    def text(self, i):
        return _txt(self.blocks[i][2])

    def image_ids(self, i):
        """Номера imageNNN.png в блоке i."""
        out = []
        for r in re.findall(r'r:embed="(rId\d+)"', self.blocks[i][2]):
            m = re.match(r'media/image(\d+)\.png', self.rid2target.get(r, ''))
            if m:
                out.append(int(m.group(1)))
        return out

    def find(self, start, last=True, after=0):
        """Индекс блока, текст которого начинается с start (last=True – последний: не строка содержания)."""
        hits = [i for i in range(after, len(self.blocks)) if self.text(i).startswith(start)]
        if not hits:
            raise KeyError(start)
        return hits[-1] if last else hits[0]

    def dump(self, i0=0, i1=None, width=110):
        """Список блоков: номер, картинки, начало текста – чтобы спланировать правку."""
        for i in range(i0, i1 or len(self.blocks)):
            b = self.blocks[i][2]
            kind = 'T' if b.startswith('<w:tbl>') else ' '
            ims = ','.join('#%d' % k for k in self.image_ids(i))
            t = self.text(i)
            if t.strip() or ims:
                print(f'{i:4d}{kind} {ims:10s} {t[:width]}')

    def media(self, k):
        return self.files[f'word/media/image{k}.png']

    # --- картинки
    def replace_image(self, k, png, keep_width=False):
        """Заменить imageK.png. Размер в документе масштабируется так же, как у старой картинки
        (keep_width=True – ширина прежняя, высота по пропорции: для рисунков во всю ширину)."""
        from PIL import Image
        old = Image.open(io.BytesIO(self.media(k)))
        new = Image.open(png)
        ow, oh = old.size; nw, nh = new.size
        rid = self.target2rid[f'media/image{k}.png']
        pat = re.compile(r'<w:drawing>(?:(?!</w:drawing>).)*r:embed="%s"(?:(?!</w:drawing>).)*</w:drawing>' % rid, re.S)
        for blk in set(pat.findall(self.xml)):
            cx, cy = map(int, re.search(r'<wp:extent cx="(\d+)" cy="(\d+)"', blk).groups())
            if keep_width:
                ncx, ncy = cx, round(cx * nh / nw)
            else:
                ncx, ncy = round(cx * nw / ow), round(cy * nh / oh)
            self.xml = self.xml.replace(blk, blk.replace(f'cx="{cx}" cy="{cy}"', f'cx="{ncx}" cy="{ncy}"'))
        b = io.BytesIO()
        dpi = old.info.get('dpi', (300, 300))
        new.save(b, 'PNG', dpi=tuple(round(x) for x in dpi))
        self.files[f'word/media/image{k}.png'] = b.getvalue()
        self._reindex()

    def _new_image(self, png):
        from PIL import Image
        nums = [int(m) for m in re.findall(r'word/media/image(\d+)\.png', '\n'.join(self.files))]
        n = max(nums + [0]) + 1
        rmax = max(int(r[3:]) for r in re.findall(r'Id="(rId\d+)"', self.rels))
        rid = f'rId{rmax + 1}'
        self.rels = self.rels.replace('</Relationships>',
            f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Target="media/image{n}.png"/></Relationships>')
        self.files[f'word/media/image{n}.png'] = open(png, 'rb').read()
        self.rid2target[rid] = f'media/image{n}.png'
        w, h = Image.open(png).size
        dpi = Image.open(png).info.get('dpi', (300, 300))[0] or 300
        return n, rid, round(w / dpi * 914400), round(h / dpi * 914400)

    # --- вставка блоков
    def _templates(self, i0, i1):
        """Шаблоны из раздела: обычный абзац, абзац-формула по центру, таблица и подпись таблицы."""
        tp = tf = None
        for i in range(i0, i1):
            b = self.blocks[i][2]
            if b.startswith('<w:tbl>'):
                continue
            if self.image_ids(i) and '<w:jc w:val="center"/>' in b and '<w:tab/>' not in b and tf is None:
                tf = b
            if not self.image_ids(i) and 'w:firstLine' in b and tp is None and len(self.text(i)) > 20:
                tp = b
        cap = next(b for _, _, b in self.blocks if _txt(b).startswith('Таблица ') and not b.startswith('<w:tbl>'))
        tbl = [b for _, _, b in self.blocks if b.startswith('<w:tbl>')][-1]
        if tp is None or tf is None:
            raise RuntimeError('в разделе нет шаблона абзаца или формулы – передайте tmpl_range')
        return tp, tf, cap, tbl

    @staticmethod
    def runs(s, sz=28, bold=False):
        """Текст -> runs; X_{т} – нижний индекс, A^{р} – верхний."""
        out = []
        for part in re.split(r'(_\{[^}]*\}|\^\{[^}]*\})', s):
            if not part:
                continue
            va = ''
            if part.startswith('_{'):
                va, part = '<w:vertAlign w:val="subscript"/>', part[2:-1]
            elif part.startswith('^{'):
                va, part = '<w:vertAlign w:val="superscript"/>', part[2:-1]
            out.append('<w:r><w:rPr><w:b w:val="%d"/><w:i w:val="0"/><w:sz w:val="%d"/>%s</w:rPr>'
                       '<w:t xml:space="preserve">%s</w:t></w:r>' % (1 if bold else 0, sz, va, _esc(part)))
        return ''.join(out)

    def replace_section(self, i0, i1, blocks, tmpl_range=None, workdir=None):
        """Заменить блоки i0+1 .. i1-1 (i0 – заголовок раздела, i1 – следующий заголовок) на blocks."""
        tp, tf, cap, tbl = self._templates(*(tmpl_range or (i0 + 1, i1)))
        ppr = re.search(r'<w:pPr>.*?</w:pPr>', tp).group(0)
        old_imgs = {}
        for i in range(i0 + 1, i1):
            for k in self.image_ids(i):
                old_imgs[k] = self.blocks[i][2]
        workdir = workdir or tempfile.mkdtemp(prefix='pravki_')
        out, nf = [], 0
        for b in blocks:
            kind = b[0]
            if kind == 'p':
                out.append('<w:p>' + ppr + self.runs(b[1]) + '</w:p>')
            elif kind == 'img':
                out.append(old_imgs.pop(b[1]))
            elif kind == 'f':
                nf += 1
                fn = os.path.join(workdir, f'f{nf}.png')
                formula_png(b[1], fn)
                n, rid, cx, cy = self._new_image(fn)
                s = re.sub(r'r:embed="rId\d+"', f'r:embed="{rid}"', tf)
                s = re.sub(r'cx="\d+" cy="\d+"', f'cx="{cx}" cy="{cy}"', s)
                s = re.sub(r'<wp:docPr id="\d+" name="Picture \d+"/>', f'<wp:docPr id="{9000 + n}" name="Picture {9000 + n}"/>', s)
                out.append(s)
            elif kind == 'tbl':
                out.append(self._table(cap, tbl, *b[1:]))
            else:
                raise ValueError(kind)
        a = self.blocks[i0][1]; z = self.blocks[i1][0]
        self.xml = self.xml[:a] + ''.join(out) + self.xml[z:]
        self._reindex()
        return old_imgs  # картинки раздела, которые не вошли в новый текст

    def _table(self, cap_tmpl, tbl_tmpl, caption, head, rows, widths=None):
        cp = re.sub(r'<w:t>[^<]*</w:t>', '<w:t>%s</w:t>' % _esc(caption), cap_tmpl, count=1)
        grid = re.search(r'<w:tblGrid>.*?</w:tblGrid>', tbl_tmpl).group(0)
        tpr = re.search(r'<w:tblPr>.*?</w:tblPr>', tbl_tmpl).group(0)
        ws = widths or [int(v) for v in re.findall(r'w:w="(\d+)"', grid)]
        if widths:
            grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths) + '</w:tblGrid>'
        def cell(s, w, jc, bold):
            return (f'<w:tc><w:tcPr><w:tcW w:type="dxa" w:w="{w}"/></w:tcPr><w:p><w:pPr><w:keepNext/>'
                    f'<w:spacing w:line="240" w:lineRule="auto"/><w:jc w:val="{jc}"/></w:pPr>'
                    + self.runs(s, 22, bold) + '</w:p></w:tc>')
        tr = ['<w:tr><w:trPr><w:tblHeader w:val="true"/><w:cantSplit/></w:trPr>'
              + ''.join(cell(h, w, 'center', True) for h, w in zip(head, ws)) + '</w:tr>']
        for r in rows:
            tr.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>'
                      + ''.join(cell(v, w, 'left' if j == 0 else 'center', False) for j, (v, w) in enumerate(zip(r, ws)))
                      + '</w:tr>')
        return cp + '<w:tbl>' + tpr + grid + ''.join(tr) + '</w:tbl>'

    # --- текст
    def replace_text(self, old, new, count=1):
        """Заменить текст внутри одного <w:t> (не через границу runs). count=0 – все вхождения."""
        n = self.xml.count(_esc(old))
        if n == 0:
            raise KeyError(old)
        self.xml = self.xml.replace(_esc(old), _esc(new), n if count == 0 else count)
        self._reindex()
        return n

    # --- сохранение
    def save(self, out):
        self.files['word/document.xml'] = self.xml.encode('utf8')
        self.files['word/_rels/document.xml.rels'] = self.rels.encode('utf8')
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zo:
            names = set()
            for it in self.infos:
                zo.writestr(it, self.files[it.filename]); names.add(it.filename)
            for k, v in self.files.items():
                if k not in names:
                    zo.writestr(k, v)
        open(out, 'wb').write(buf.getvalue())

# ---------------------------------------------------------------- PDF и содержание
def build_pdf(docx, outdir=None):
    """docx -> pdf через LibreOffice. Шрифты как в сданных PDF: Times New Roman -> Liberation Serif,
    Calibri (заголовки части записок) -> Noto Serif, Carlito/Caladea отключены (fc.conf)."""
    outdir = outdir or os.path.dirname(os.path.abspath(docx))
    env = dict(os.environ, FONTCONFIG_FILE=FC_CONF)
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', outdir, docx],
                   env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    return os.path.join(outdir, os.path.splitext(os.path.basename(docx))[0] + '.pdf')

def pdf_pages(pdf):
    """Тексты страниц PDF (pdftotext -layout)."""
    t = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True, check=True).stdout
    return t.split('\f')

def heading_pages(pdf, toc_last_page=3):
    """{начало заголовка: номер страницы} по тексту PDF (страницы содержания пропускаются)."""
    res = {}
    for p, page in enumerate(pdf_pages(pdf), start=1):
        if p <= toc_last_page:
            continue
        for line in page.splitlines():
            s = re.sub(r'\s+', ' ', line.strip())
            if s and s not in res:
                res[s] = p
    return res

def fix_toc(docx, pdf, max_par=80, toc_last_page=3):
    """Проставить в строках содержания («Заголовок<TAB>N») фактические номера страниц из pdf.
    Сравнение по началу заголовка (первые 25 символов). Возвращает список изменений."""
    import docx as _docx
    hp = heading_pages(pdf, toc_last_page)
    d = _docx.Document(docx)
    changes = []
    for p in d.paragraphs[:max_par]:
        m = re.match(r'(.+?)\t(\d+)$', p.text)
        if not m:
            continue
        head = re.sub(r'\s+', ' ', m.group(1)).strip()
        key = head[:25]
        page = next((v for k, v in hp.items() if k.startswith(key)), None)
        if page is None or str(page) == m.group(2):
            continue
        r = [r for r in p.runs if re.search(r'\t\d+$', r.text)]
        if not r:
            continue
        r[-1].text = re.sub(r'\t\d+$', f'\t{page}', r[-1].text)
        changes.append((head, m.group(2), page))
    if changes:
        d.save(docx)
    return changes

def renumber_tables(doc, start_from, shift):
    """Сдвинуть номера «Таблица N –» начиная с N >= start_from на shift (подписи и «таблице N» в тексте)."""
    def sub(m):
        n = int(m.group(2))
        return m.group(1) + str(n + shift if n >= start_from else n)
    for pat in (r'(<w:t[^>]*>Таблица )(\d+)(?= –)', r'([ (]таблиц[аеуы] )(\d+)'):
        doc.xml = re.sub(pat, sub, doc.xml)
    doc._reindex()
