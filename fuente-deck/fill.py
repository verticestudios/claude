# Paso 2: carga el contenido de la propuesta sobre las láminas duplicadas del template maestro de Vértice.
import copy, os, re, sys
from lxml import etree
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "stage.pptx")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/user/claude/propuesta-move-37-vertice.pptx"

TUSK = "Tusker Grotesk 5600 Semibold"
NIMB = "Nimbus Sans Extended"
ROJO, AZUL, LIMA, NEGRO, BLANCO = "F10A09", "0024AD", "D7FE51", "000000", "FFFFFF"
CARBON, PAPEL, ROJOT, GRIS, META = "131313", "F2F2F0", "C60807", "5A5A5A", "8A8A8A"
FOOT = "VÉRTICE · MOVE 37 · PROPUESTA · NOVIEMBRE 2026"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"

prs = Presentation(SRC)
S = list(prs.slides)


# ---------------------------------------------------------------- utilidades
def shp(slide, name):
    for s in slide.shapes:
        if s.name == name:
            return s
        if s.shape_type == 6:  # grupo
            for c in s.shapes:
                if c.name == name:
                    return c
    raise KeyError(name)


def drop(slide, *names):
    for n in names:
        el = shp(slide, n)._element
        el.getparent().remove(el)


def segs(text):
    """Separa el texto en tramos normales y tramos [A CONFIRMAR]."""
    return [(p, bool(re.fullmatch(r"\[[^\]]+\]", p))) for p in re.split(r"(\[[^\]]+\])", text) if p]


def set_fill(rPr, hexcol):
    for old in rPr.findall(qn("a:solidFill")):
        rPr.remove(old)
    sf = etree.SubElement(rPr, qn("a:solidFill"))
    etree.SubElement(sf, qn("a:srgbClr")).set("val", hexcol)
    rPr.remove(sf)
    ln = rPr.find(qn("a:ln"))
    rPr.insert(list(rPr).index(ln) + 1 if ln is not None else 0, sf)


def set_text(shape, lines, hl=ROJOT, color=None, size=None, bold=None):
    """Reemplaza el texto de una forma del template conservando su estilo."""
    if isinstance(lines, str):
        lines = [lines]
    tb = shape.text_frame._txBody
    bp = tb.find(qn("a:bodyPr"))
    if bp is not None:
        for af in bp.findall(qn("a:normAutofit")):
            bp.remove(af)
    ps = tb.findall(qn("a:p"))
    p0 = ps[0]
    r0 = next((r for p in ps for r in p.findall(qn("a:r"))), None)
    if r0 is None:
        r0 = etree.SubElement(p0, qn("a:r"))
        etree.SubElement(r0, qn("a:rPr"))
        etree.SubElement(r0, qn("a:t"))
        p0.remove(r0)
    for p in ps:
        tb.remove(p)
    for line in lines:
        p = etree.SubElement(tb, qn("a:p"))
        if p0.find(qn("a:pPr")) is not None:
            p.append(copy.deepcopy(p0.find(qn("a:pPr"))))
        for txt, is_hl in segs(line):
            r = copy.deepcopy(r0)
            rPr = r.find(qn("a:rPr"))
            if rPr is None:
                rPr = etree.Element(qn("a:rPr"))
                r.insert(0, rPr)
            if size:
                rPr.set("sz", str(int(size * 100)))
            if bold is not None:
                rPr.set("b", "1" if bold else "0")
            if color:
                set_fill(rPr, color)
            if is_hl and hl:
                set_fill(rPr, hl)
                rPr.set("b", "1")
            r.find(qn("a:t")).text = txt
            p.append(r)


def move(shape, x=None, y=None, w=None, h=None):
    if x is not None: shape.left = Inches(x)
    if y is not None: shape.top = Inches(y)
    if w is not None: shape.width = Inches(w)
    if h is not None: shape.height = Inches(h)


def text(slide, x, y, w, h, lines, size=14, color=NEGRO, font=None, bold=False, spc=None,
         lnspc=None, align="l", anchor="t", bullets=False, hl=ROJOT, after=0, caps=False):
    """Caja de texto con el estilo del template (sin márgenes, tipografías de la marca)."""
    if isinstance(lines, str):
        lines = [lines]
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    body = tb.text_frame._txBody
    for p in body.findall(qn("a:p")):
        body.remove(p)
    bp = body.find(qn("a:bodyPr"))
    for k in ("lIns", "tIns", "rIns", "bIns"):
        bp.set(k, "0")
    bp.set("wrap", "square")
    bp.set("anchor", anchor)
    for line in lines:
        p = etree.SubElement(body, qn("a:p"))
        pPr = etree.SubElement(p, qn("a:pPr"))
        pPr.set("algn", align)
        if bullets:
            pPr.set("marL", "171450")
            pPr.set("indent", "-171450")
        if lnspc:
            ls = etree.SubElement(pPr, qn("a:lnSpc"))
            etree.SubElement(ls, qn("a:spcPct")).set("val", str(int(lnspc * 1000)))
        if after:
            sa = etree.SubElement(pPr, qn("a:spcAft"))
            etree.SubElement(sa, qn("a:spcPts")).set("val", str(int(after * 100)))
        if bullets:
            etree.SubElement(pPr, qn("a:buFont")).set("typeface", "Arial")
            etree.SubElement(pPr, qn("a:buChar")).set("char", "•")
        runs = line if isinstance(line, list) else [(t, {"hl": h}) for t, h in segs(line)]
        for t, o in runs:
            r = etree.SubElement(p, qn("a:r"))
            rPr = etree.SubElement(r, qn("a:rPr"))
            rPr.set("lang", "es-AR")
            rPr.set("sz", str(int(o.get("size", size) * 100)))
            b = o.get("b", bold) or (o.get("hl") and hl)
            rPr.set("b", "1" if b else "0")
            if spc:
                rPr.set("spc", str(spc))
            if caps:
                rPr.set("cap", "all")
            col = hl if (o.get("hl") and hl) else o.get("color", color)
            set_fill(rPr, col)
            f = o.get("font", font)
            if f:
                for tag in ("a:latin", "a:ea", "a:cs"):
                    etree.SubElement(rPr, qn(tag)).set("typeface", f)
            etree.SubElement(r, qn("a:t")).text = t
    return tb


def kicker(slide, x, y, w, s, color=ROJOT, size=10):
    return text(slide, x, y, w, 0.25, s, size=size, color=color, font=NIMB, spc=200)


def head(slide, x, y, w, h, s, size=22, color=NEGRO):
    return text(slide, x, y, w, h, s, size=size, color=color, font=TUSK, lnspc=95)


def box(slide, x, y, w, h, fill, line=None, adj=0.0171):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.adjustments[0] = adj
    s.fill.solid()
    s.fill.fore_color.rgb = __import__("pptx.dml.color", fromlist=["RGBColor"]).RGBColor.from_string(fill)
    if line:
        s.line.color.rgb = __import__("pptx.dml.color", fromlist=["RGBColor"]).RGBColor.from_string(line)
        s.line.width = Pt(1)
    else:
        s.line.fill.background()
    st = s._element.find(qn("p:style"))
    if st is not None:
        s._element.remove(st)
    return s


TABLE_STYLE = "{4C3C2611-4C71-4FC5-86AE-919BDF0F9419}"


def table(slide, x, y, w, colw, header, rows, size=11, first_bold=True, hl_row=None, hl_fill=LIMA):
    nr, nc = len(rows) + 1, len(header)
    gf = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(0.3 * nr))
    tbl = gf.table
    tblPr = tbl._tbl.tblPr
    for k in list(tblPr.attrib):
        del tblPr.attrib[k]
    for c in list(tblPr):
        tblPr.remove(c)
    etree.SubElement(tblPr, qn("a:tableStyleId")).text = TABLE_STYLE
    for i, cw in enumerate(colw):
        tbl.columns[i].width = Inches(cw)
    for ri in range(nr):
        tbl.rows[ri].height = Inches(0.3)
        for ci in range(nc):
            cell = tbl.cell(ri, ci)
            val = header[ci] if ri == 0 else rows[ri - 1][ci]
            tc = cell._tc
            txBody = tc.find(qn("a:txBody"))
            for p in txBody.findall(qn("a:p")):
                txBody.remove(p)
            p = etree.SubElement(txBody, qn("a:p"))
            pPr = etree.SubElement(p, qn("a:pPr"))
            pPr.set("algn", "l")
            ls = etree.SubElement(pPr, qn("a:lnSpc"))
            etree.SubElement(ls, qn("a:spcPct")).set("val", "105000")
            for t, h in segs(val):
                r = etree.SubElement(p, qn("a:r"))
                rPr = etree.SubElement(r, qn("a:rPr"))
                rPr.set("lang", "es-AR")
                rPr.set("sz", str(int((size - (1 if ri == 0 else 0)) * 100)))
                bold = ri == 0 or (first_bold and ci == 0) or h
                rPr.set("b", "1" if bold else "0")
                if ri == 0:
                    rPr.set("spc", "100")
                set_fill(rPr, ROJOT if h else NEGRO)
                etree.SubElement(r, qn("a:t")).text = t
            tcPr = tc.get_or_add_tcPr()
            for c in list(tcPr):
                tcPr.remove(c)
            for k, v in (("marL", "68580"), ("marR", "68580"), ("marT", "54864"), ("marB", "54864"), ("anchor", "t")):
                tcPr.set(k, v)
            for side in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
                ln = etree.SubElement(tcPr, qn(side))
                ln.set("w", "12700")
                sf = etree.SubElement(ln, qn("a:solidFill"))
                etree.SubElement(sf, qn("a:srgbClr")).set("val", "CBCBCB")
            fill = "ECECEC" if ri == 0 else (hl_fill if hl_row is not None and ri - 1 == hl_row else BLANCO)
            sf = etree.SubElement(tcPr, qn("a:solidFill"))
            etree.SubElement(sf, qn("a:srgbClr")).set("val", fill)
    return gf


def base(slide, kick, title, foot=FOOT):
    """Lámina de documento del template (kicker, título, pie) sin la tabla de ejemplo."""
    set_text(shp(slide, "Text 0"), kick)
    set_text(shp(slide, "Text 1"), title)
    set_text(shp(slide, "Text 5"), foot)
    drop(slide, "Shape 2", "Shape 3", "Shape 4", "Table 0")


X0, CW = 0.89, 11.56  # margen y ancho útil del template

# ---------------------------------------------------------------- 1 · portada
s = S[0]
set_text(shp(s, "Text 3"), "MOVE 37 · GRUPO ASEGURADOR PARANÁ · PROPUESTA")
move(shp(s, "Text 3"), x=1.67, w=10.0)
set_text(shp(s, "Text 4"), "MOVE 37")
set_text(shp(s, "Text 5"), "MARCA, NEGOCIO Y CAPTACIÓN B2B")
set_text(shp(s, "Text 9"), "CONTENT MARKETING STUDIO · BUENOS AIRES · NOVIEMBRE 2026")

# ---------------------------------------------------------------- 2 · índice
s = S[1]
set_text(shp(s, "Text 0"), "MOVE 37 · PROPUESTA · ÍNDICE")
set_text(shp(s, "Text 1"), "RECORRIDO: DEL DIAGNÓSTICO AL PLAN")
idx = [("DIAGNÓSTICO", "Contexto, mercado y prioridades."), ("MARCA", "Arquitectura, nombre y plataforma."),
       ("SERVICIOS", "Catálogo, precios y casos."), ("CAMPAÑA", "Lanzamiento, mensajes y Prospector."),
       ("PLAN", "Part time, cronograma y riesgos.")]
for i, (t, d) in enumerate(idx):
    n0 = 3 + 4 * i
    set_text(shp(s, f"Text {n0 + 1}"), t)
    set_text(shp(s, f"Text {n0 + 2}"), d)
    move(shp(s, f"Text {n0 + 1}"), y=4.87, h=0.36)
    move(shp(s, f"Text {n0 + 2}"), y=5.31, w=1.85, h=0.75)
set_text(shp(s, "Text 22"), FOOT)

# ---------------------------------------------------------------- 3 · resumen ejecutivo
s = S[2]
base(s, "01 · RESUMEN EJECUTIVO", "SEIS DECISIONES PARA SER NEGOCIO")
recs = [
    ("A · MARCA", "MARCA PROPIA CON RESPALDO DEL GRUPO", "Permite venderles a otras aseguradoras y a otras industrias, y traslada más de 60 años de confianza."),
    ("B · OPORTUNIDAD", "PRIMERO SEGUROS Y PRODUCTORES", "El conocimiento del negocio acorta la venta. Otras industrias entran en una segunda ola."),
    ("C · SERVICIOS", "CUATRO MODALIDADES, PRECIOS POR NIVEL", "Proyecto, producto, suscripción y staff part time. Montos: [MONTO A DEFINIR]."),
    ("D · CAMPAÑA", "LANZAMIENTO B2B DE 90 DÍAS", "Mensajes por segmento, con LinkedIn como canal principal [A VALIDAR]."),
    ("E · PROSPECTOR", "SISTEMA PROPIO DE LEADS B2B", "Se desarrolla con Move 37 y cumple la Ley 25.326 desde el diseño."),
    ("F · VÉRTICE PART TIME", "EQUIPO DEDICADO POR ÁREA", "Cinco áreas con horas y entregables mensuales. Montos: [MONTO A DEFINIR]."),
]
cw, ch, g = (CW - 2 * 0.17) / 3, 1.9, 0.17
for i, (k, t, d) in enumerate(recs):
    x, y = X0 + (i % 3) * (cw + g), 2.2 + (i // 3) * (ch + g)
    box(s, x, y, cw, ch, BLANCO)
    kicker(s, x + 0.25, y + 0.2, cw - 0.5, k)
    head(s, x + 0.25, y + 0.5, cw - 0.5, 0.65, t, size=20)
    text(s, x + 0.25, y + 1.17, cw - 0.5, 0.65, d, size=11.5, color=GRIS)
box(s, X0, 6.24, CW, 0.46, CARBON)
text(s, X0 + 0.25, 6.24, CW - 0.5, 0.46, "Qué pedimos hoy: aprobar la Fase 0 de validación. Plazos y montos dependen de los supuestos de esta propuesta. El uso de la marca Paraná está sujeto a aprobación del Grupo.",
     size=11.5, color=BLANCO, anchor="ctr", hl=LIMA)

# ---------------------------------------------------------------- 4 · contexto
s = S[3]
base(s, "02 · CONTEXTO", "EL PUNTO DE PARTIDA")
box(s, X0, 2.2, 5.7, 4.4, BLANCO)
kicker(s, X0 + 0.3, 2.45, 5.1, "GRUPO ASEGURADOR PARANÁ")
text(s, X0 + 0.3, 2.85, 5.1, 3.6, [
    "Integración estratégica de Paraná Seguros y Paraná ART.",
    "Más de 60 años en el mercado asegurador argentino. Paraná Seguros opera desde 1961.",
    "Seguros: Automotores, Motovehículos, Caución, Accidentes Personales, Vida, Hogar y Combinado Familiar, Responsabilidad Civil, Embarcaciones, Transporte, Consorcio y Comercio e Industria.",
    "ART: prevención, seguridad laboral y cobertura de accidentes y enfermedades profesionales.",
    "Canales digitales: Mi Pas, Mi Móvil, Tero Granizo y Paraná 24.",
], size=11.5, bullets=True, after=5)
box(s, 6.75, 2.2, 5.7, 4.4, CARBON)
kicker(s, 7.05, 2.45, 5.1, "MOVE 37 HOY", color=LIMA)
head(s, 7.05, 2.8, 2.6, 1.0, "+40", size=66, color=LIMA)
text(s, 7.05, 3.85, 2.5, 0.7, "proyectos de herramientas de IA, sobre todo de uso interno", size=11.5, color=BLANCO)
head(s, 9.85, 2.8, 2.4, 1.0, "<2", size=66, color=LIMA)
text(s, 9.85, 3.85, 2.4, 0.7, "años de operación para llegar a ese volumen", size=11.5, color=BLANCO)
text(s, 7.05, 4.85, 5.1, 1.6, [
    "Opera en oficinas separadas del Grupo.",
    "No está constituido como marca.",
    "Presta servicios tecnológicos a todas las marcas del Grupo.",
], size=11.5, color=BLANCO, bullets=True, after=5)

# ---------------------------------------------------------------- 5 · oportunidad
s = S[4]
set_text(shp(s, "Text 0"), "02 · LA OPORTUNIDAD")
set_text(shp(s, "Text 1"), "DOS CAMINOS")
t2 = shp(s, "Text 2")
move(t2, h=1.5, w=9.6)
set_text(t2, [
    "A · Seguros y productores: vender soluciones tecnológicas a aseguradoras y productores, con el conocimiento sectorial del Grupo.",
    "B · Cualquier industria: producir herramientas para empresas de otros sectores, con el método de más de 40 proyectos.",
    "Objetivo de esta propuesta: un plan integral en seis bloques, de la marca a la captación de clientes.",
], hl=LIMA)

# ---------------------------------------------------------------- 6 · capítulo 01
s = S[5]
set_text(shp(s, "Text 3"), "CAPÍTULO 01 · DÓNDE ESTÁ EL")
move(shp(s, "Text 3"), x=2.67, w=8.0)
set_text(shp(s, "Text 4"), "NEGOCIO")
set_text(shp(s, "Text 5"), "¿DÓNDE JUGAMOS PRIMERO?")
move(shp(s, "Text 5"), x=2.67, w=8.0)

# ---------------------------------------------------------------- 7 · diagnóstico
s = S[6]
base(s, "03 · DIAGNÓSTICO · BLOQUE B", "QUÉ SABEMOS Y QUÉ FALTA MEDIR")
table(s, X0, 2.2, CW, [2.2, 4.68, 4.68], ["DIMENSIÓN", "LÍNEA A · SEGUROS Y PRODUCTORES", "LÍNEA B · OTRAS INDUSTRIAS"], [
    ["Tamaño de mercado", "Aseguradoras y productores matriculados y su gasto en tecnología [DATO A CONFIRMAR · fuente sugerida: SSN]", "Gasto en soluciones de IA de empresas medianas y grandes [DATO A CONFIRMAR · estudio de mercado]"],
    ["Perfil de demanda", "Aseguradoras: suscripción, siniestros y atención, con compras largas. Productores: herramientas simples, precio accesible y adopción rápida.", "Empresas con procesos repetitivos y mucho volumen de documentos o de atención. Demanda heterogénea."],
    ["Competidores", "Insurtechs, software core para seguros y consultoras de transformación digital [RELEVAMIENTO A CONFIRMAR]", "Consultoras, integradores, software factories, agencias de IA y SaaS globales [RELEVAMIENTO A CONFIRMAR]"],
    ["Barreras de entrada", "Regulación de la SSN y seguridad de la información. Reparos a comprarle a otro grupo asegurador. Sistemas heredados.", "Sin credenciales fuera de seguros, competencia por precio y falta de casos propios."],
    ["Ventaja de Move 37", "Conoce el negocio desde adentro, tiene más de 40 proyectos con usuarios reales y el respaldo de un grupo con más de 60 años.", "Velocidad de producción y método probado. Menor diferenciación que en seguros."],
], size=11)

# ---------------------------------------------------------------- 8 · matriz
s = S[7]
set_text(shp(s, "Text 0"), "03 · PRIORIZACIÓN")
set_text(shp(s, "Text 1"), "DÓNDE JUGAMOS PRIMERO")
t2 = shp(s, "Text 2")
move(t2, y=3.35, h=2.4)
set_text(t2, ["Líneas de negocio según el atractivo del mercado y la capacidad de ejecución de Move 37.",
              "Lectura preliminar y cualitativa de Vértice. Se recalibra con datos de mercado [DATO A CONFIRMAR]."])
quads = [("Text 4", "Text 5", "ATRACTIVO ALTO · CAPACIDAD BAJA", "OTRAS INDUSTRIAS, NICHO DOCUMENTAL",
          "Proyectos internos que se trasladan casi sin cambios. Segunda ola.", 2.68, NEGRO),
         ("Text 7", "Text 8", "ATRACTIVO ALTO · CAPACIDAD ALTA", "PRODUCTORES Y ASEGURADORAS · PRIORIZAR",
          "Productores primero: herramientas simples y red del Grupo [DATO A CONFIRMAR]. Aseguradoras: alto valor, exige independencia demostrable.", 2.68, NEGRO),
         ("Text 10", "Text 11", "ATRACTIVO BAJO · CAPACIDAD BAJA", "OTRAS INDUSTRIAS EN GENERAL",
          "Exige fuerza comercial y casos que hoy no existen. Postergar.", 5.4, NEGRO),
         ("Text 13", "Text 14", "ATRACTIVO BAJO · CAPACIDAD ALTA", "PEDIDOS PUNTUALES",
          "Proyectos que llegan por la red del Grupo. Se toman sin salir a buscarlos.", 5.4, NEGRO)]
for k, t, kt, tt, dd, dy, col in quads:
    set_text(shp(s, k), kt)
    set_text(shp(s, t), tt, size=17)
    tb = shp(s, t)
    move(tb, h=0.75)
    text(s, tb.left / 914400, dy, 3.23, 1.0, dd, size=11, color=col, hl=BLANCO if k == "Text 7" else ROJOT)
set_text(shp(s, "Text 15"), "EJE X: CAPACIDAD DE EJECUCIÓN · EJE Y: ATRACTIVO")

# ---------------------------------------------------------------- 9 · capítulo 02
s = S[8]
set_text(shp(s, "Text 4"), "CAPÍTULO 02 · TODA JUGADA NECESITA UNA")
set_text(shp(s, "Text 5"), "MARCA")
set_text(shp(s, "Text 6"), "¿CÓMO NOS PRESENTAMOS?")
set_text(shp(s, "Text 0"), "MOVE 37")

# ---------------------------------------------------------------- 10 · arquitectura
s = S[9]
set_text(shp(s, "Text 0"), "04 · ARQUITECTURA DE MARCA · BLOQUE A")
set_text(shp(s, "Text 1"), "TRES ARQUITECTURAS POSIBLES")
text(s, X0, 2.15, CW, 0.9, "Recomendamos C: resuelve el principal freno comercial, que es venderles a otras aseguradoras, y habilita los caminos A y B. El respaldo se regula por segmento: fuerte con productores, discreto con aseguradoras y medio con otras industrias.",
     size=12.5, hl=AZUL)
arch = [("A", "DENTRO DEL GRUPO", "Monolítica o submarca de Paraná. Confianza inmediata, pero otras aseguradoras no le compran a un rival.", "AJUSTE BAJO"),
        ("B", "INDEPENDIENTE SIN VÍNCULO", "Marca propia sin mención al Grupo. Libertad comercial, pero pierde la confianza heredada.", "AJUSTE MEDIO"),
        ("C", "INDEPENDIENTE CON RESPALDO", "Marca propia firmada como \"una compañía del Grupo Asegurador Paraná\" [REQUIERE APROBACIÓN].", "RECOMENDADO")]
for i, (l, t, d, tag) in enumerate(arch):
    n = 3 + 5 * i
    set_text(shp(s, f"Text {n}"), l)
    set_text(shp(s, f"Text {n + 1}"), t)
    set_text(shp(s, f"Text {n + 2}"), d, hl=LIMA if i == 2 else AZUL, size=11)
    move(shp(s, f"Text {n + 2}"), h=0.75)
    set_text(shp(s, f"Text {n + 3}"), tag)
    move(shp(s, f"Text {n + 3}"), y=6.08)
set_text(shp(s, "Text 17"), FOOT)

# ---------------------------------------------------------------- 11 · el 37
s = S[10]
set_text(shp(s, "Text 0"), "04 · EL CONCEPTO DETRÁS DEL NOMBRE")
move(shp(s, "Text 0"), x=3.17, w=7.0)
set_text(shp(s, "Text 1"), "37")
t2 = shp(s, "Text 2")
move(t2, x=2.17, w=9.0, h=1.5)
set_text(t2, ["Marzo de 2016, segunda partida entre Lee Sedol y AlphaGo (Google DeepMind). La jugada 37 desafió 2500 años de tradición del Go y los comentaristas la tomaron por un error. Cien movimientos después resultó la clave de la victoria.",
              "Para Move 37 es inspiración: creatividad estratégica, innovación genuina y tecnología para problemas sin salida obvia. No implica vínculo con DeepMind ni derechos sobre el hecho."],
         hl=LIMA)

# ---------------------------------------------------------------- 12 · evaluación del nombre
s = S[11]
base(s, "04 · EVALUACIÓN DEL NOMBRE", "MOVE 37: CANDIDATO CON CONDICIONES")
table(s, X0, 2.2, 7.75, [2.2, 1.35, 4.2], ["CRITERIO", "EVALUACIÓN", "COMENTARIO"], [
    ["Relato y significado", "Fuerte", "Historia potente y verificable sobre la creatividad de la IA."],
    ["Memorabilidad", "Fuerte", "Corto, con una cifra distintiva."],
    ["Pronunciación", "Media", "Mezcla inglés y número. Hay que fijar una forma oral."],
    ["Descriptividad", "Baja", "Necesita un descriptor: \"Move 37 · Soluciones de IA\"."],
    ["Disponibilidad registral", "Sin evaluar", "Búsqueda en el INPI, clases 9, 35 y 42 [DATO A CONFIRMAR]."],
    ["Asociación con terceros", "Riesgo medio", "Remite a AlphaGo y DeepMind. Sin marcas ni imágenes de terceros."],
    ["Uso por terceros", "Sin evaluar", "Relevar empresas, productos y dominios [DATO A CONFIRMAR]."],
], size=11)
box(s, 8.85, 2.2, 3.6, 4.4, AZUL)
kicker(s, 9.1, 2.45, 3.1, "RECOMENDACIÓN", color=LIMA)
text(s, 9.1, 2.85, 3.1, 3.6, [
    "Mantener Move 37 como candidato principal: el equipo ya lo usa y el relato es fuerte.",
    "Antes de adoptarlo, cumplir tres condiciones: búsqueda de anterioridades, relevamiento de usos y dominio disponible.",
    "Plan B: taller de naming con alternativas en el mismo territorio.",
], size=12, color=BLANCO, bullets=True, after=6, hl=LIMA)

# ---------------------------------------------------------------- 13 · propósito
s = S[12]
set_text(shp(s, "Text 0"), "04 · PROPÓSITO")
move(shp(s, "Text 0"), x=3.67, w=6.0)
set_text(shp(s, "Text 4"), "LA JUGADA QUE OTROS NO VEN", size=60)
set_text(shp(s, "Text 8"), "Usar la inteligencia artificial para resolver problemas de negocio que parecen no tener una salida obvia.", size=14)

# ---------------------------------------------------------------- 14 · plataforma
s = S[13]
base(s, "04 · PLATAFORMA DE MARCA", "VALOR, ATRIBUTOS Y VOZ")
box(s, X0, 2.2, CW, 1.2, BLANCO)
kicker(s, X0 + 0.3, 2.38, 6, "PROPUESTA DE VALOR")
text(s, X0 + 0.3, 2.7, CW - 0.6, 0.65, "Soluciones de IA que ya funcionan en la operación de un grupo asegurador con más de 60 años, listas para adaptarse a otro negocio, hechas por un equipo que concretó más de 40 proyectos en menos de 2 años.", size=13)
attrs = [("CRITERIO ESTRATÉGICO", "Primero el problema de negocio, después la tecnología."),
         ("INNOVACIÓN GENUINA", "Soluciones propias, no copias de tendencias."),
         ("SOLIDEZ", "Respaldo de un grupo con trayectoria y procesos serios."),
         ("VELOCIDAD CON MÉTODO", "Entregas rápidas, medibles y documentadas.")]
aw = (CW - 3 * 0.17) / 4
for i, (t, d) in enumerate(attrs):
    x = X0 + i * (aw + 0.17)
    box(s, x, 3.57, aw, 1.5, BLANCO)
    head(s, x + 0.22, 3.75, aw - 0.44, 0.55, t, size=19)
    text(s, x + 0.22, 4.35, aw - 0.44, 0.65, d, size=11, color=GRIS)
box(s, X0, 5.24, CW, 1.36, CARBON)
kicker(s, X0 + 0.3, 5.42, 9, "TONO DE VOZ · DIRECTO, PRECISO, SIN HYPE", color=LIMA)
text(s, X0 + 0.3, 5.78, CW - 0.6, 0.75, [
    [("Sí: ", {"b": True, "color": LIMA}), ("hablar con casos y métricas, explicar simple, decir qué hacemos y cómo lo medimos.", {})],
    [("No: ", {"b": True, "color": LIMA}), ("promesas mágicas, jerga vacía ni comparaciones con la ciencia ficción.", {})],
], size=12, color=BLANCO, after=3)

# ---------------------------------------------------------------- 15 · relación de marca
s = S[14]
set_text(shp(s, "Text 0"), "04 · RELACIÓN DE MARCA")
set_text(shp(s, "Text 1"), "CONFIANZA QUE BAJA, INNOVACIÓN QUE SUBE")
text(s, X0, 2.3, CW, 1.0, "Move 37 hereda la solidez del Grupo y el Grupo capitaliza la innovación de Move 37. La relación se ordena con una firma de respaldo y reglas de uso por segmento.", size=14)
set_text(shp(s, "Text 3"), "DEL GRUPO A MOVE 37")
set_text(shp(s, "Text 4"), "CONFIANZA")
move(shp(s, "Text 4"), h=0.6)
set_text(shp(s, "Text 5"), "Trayectoria desde 1961, solvencia y conocimiento del negocio asegurador. Llega a través de la firma de respaldo y de los casos internos.")
move(shp(s, "Text 5"), y=5.15, h=1.0)
set_text(shp(s, "Text 8"), "DE MOVE 37 AL GRUPO")
set_text(shp(s, "Text 9"), "INNOVACIÓN")
set_text(shp(s, "Text 10"), "Casos de IA en producción y tecnología propia refuerzan los atributos de innovación del Grupo en su propia comunicación.")
move(shp(s, "Text 10"), y=5.15, h=1.0)
grp = shp(s, "Text 6")
for sub in grp.shapes:
    if sub.has_text_frame and sub.text_frame.text.strip():
        set_text(sub, "+")
set_text(shp(s, "Text 11"), "TODA APLICACIÓN DE LA MARCA PARANÁ REQUIERE APROBACIÓN DEL GRUPO [DATO A CONFIRMAR]")

# ---------------------------------------------------------------- 16 · capítulo 03
s = S[15]
set_text(shp(s, "Text 5"), "CAPÍTULO 03 · LO QUE MOVE 37 PUEDE")
set_text(shp(s, "Text 6"), "VENDER")
move(shp(s, "Text 6"), x=2.67, w=8.0)
set_text(shp(s, "Text 7"), "¿QUÉ OFRECEMOS?")
for g, word in (("Text 0", "PROYECTO · PRODUCTO · SUSCRIPCIÓN · STAFF PART TIME · PROYECTO · PRODUCTO · SUSCRIPCIÓN · STAFF PART TIME"),
                ("Text 1", "IA APLICADA · SEGUROS · PRODUCTORES · OTRAS INDUSTRIAS · IA APLICADA · SEGUROS · PRODUCTORES · OTRAS INDUSTRIAS")):
    for sub in shp(s, g).shapes:
        if sub.has_text_frame and sub.text_frame.text.strip():
            set_text(sub, word)

# ---------------------------------------------------------------- 17 · catálogo
s = S[16]
set_text(shp(s, "Text 0"), "05 · SERVICIOS · BLOQUE C")
set_text(shp(s, "Text 1"), "SIETE SERVICIOS, CUATRO MODALIDADES")
text(s, X0, 2.2, CW, 1.2, "Arrancamos con lo que Move 37 ya hace para el Grupo: baja el riesgo de entrega. Los productos generan ingresos recurrentes y el staff part time usa capacidad disponible [DATO A CONFIRMAR].",
     size=14, color=BLANCO, hl=LIMA)
cat = [("PROYECTO", ["Diagnóstico de oportunidades de IA", "Desarrollo a medida", "Soluciones para aseguradoras"]),
       ("PRODUCTO", ["Herramientas para productores", "Prospector"]),
       ("SUSCRIPCIÓN", ["Licencias de producto", "Mantenimiento y evolución"]),
       ("STAFF PART TIME", ["Ingeniería de IA por horas", "Producto y datos"])]
for i, (t, items) in enumerate(cat):
    tn, ln = 3 + 3 * i, 4 + 3 * i
    set_text(shp(s, f"Text {tn}"), t)
    move(shp(s, f"Text {tn}"), y=4.12, h=0.87)
    set_text(shp(s, f"Text {ln}"), items)
    move(shp(s, f"Text {ln}"), y=5.07, h=1.2)
set_text(shp(s, "Text 14"), "BASADO EN LOS MÁS DE 40 PROYECTOS INTERNOS · ALCANCES A VALIDAR")

# ---------------------------------------------------------------- 18 · pricing
s = S[17]
base(s, "05 · PAQUETES Y PRICING", "TRES NIVELES Y UNA VÍA POR PROYECTO")
tiers = [("ESENCIAL", "Productores y pymes", ["Un producto estándar", "Onboarding guiado", "Soporte por correo"], "Suscripción mensual por usuario"),
         ("PROFESIONAL", "Organizaciones medianas", ["Dos o tres productos o un desarrollo acotado", "Configuración a medida", "Soporte prioritario"], "Suscripción + setup"),
         ("CORPORATIVO", "Aseguradoras y grandes empresas", ["Desarrollo a medida e integración", "Acuerdo de nivel de servicio", "Staff part time incluido"], "Proyecto + abono mensual"),
         ("PROYECTO", "Necesidad puntual", ["Diagnóstico o desarrollo cerrado", "Alcance y entregables fijos", "Garantía post entrega [A DEFINIR]"], "Precio por alcance")]
tw = (CW - 3 * 0.17) / 4
for i, (t, who, items, mod) in enumerate(tiers):
    x, dark = X0 + i * (tw + 0.17), i == 2
    fg, sub, hl = (BLANCO, "ABABAB", LIMA) if dark else (NEGRO, GRIS, ROJOT)
    box(s, x, 2.2, tw, 3.75, CARBON if dark else BLANCO)
    head(s, x + 0.22, 2.4, tw - 0.44, 0.5, t, size=26, color=LIMA if dark else NEGRO)
    text(s, x + 0.22, 2.95, tw - 0.44, 0.3, who, size=11, color=sub)
    text(s, x + 0.22, 3.35, tw - 0.44, 1.5, items, size=11.5, color=fg, bullets=True, after=4, hl=hl)
    text(s, x + 0.22, 4.95, tw - 0.44, 0.3, mod, size=11, color=fg, bold=True)
    text(s, x + 0.22, 5.4, tw - 0.44, 0.35, "[MONTO A DEFINIR]", size=13, hl=hl)
text(s, X0, 6.12, CW, 0.55, "Con qué se definen los precios: costo hora del equipo [DATO A CONFIRMAR] · referencias de competidores [DATO A CONFIRMAR] · valor para el cliente · margen objetivo del Grupo [DATO A CONFIRMAR].", size=11.5)

# ---------------------------------------------------------------- 19 · casos
s = S[18]
set_text(shp(s, "Text 0"), "05 · CASOS DE USO")
set_text(shp(s, "Text 1"), "CÓMO CONTAMOS LOS 40 PROYECTOS")
text(s, X0, 2.15, CW, 0.9, "Cada proyecto pasa por inventario, clasificación, anonimización y aprobación escrita del Grupo antes de publicarse. No se publican datos de asegurados, montos ni sistemas internos.", size=13)
set_text(shp(s, "Text 4"), "EL PROBLEMA")
set_text(shp(s, "Text 5"), "[DATO A CONFIRMAR: qué proceso y qué dolor]")
set_text(shp(s, "Text 8"), "LA SOLUCIÓN")
set_text(shp(s, "Text 9"), "[DATO A CONFIRMAR: herramienta y enfoque de IA]")
move(shp(s, "Text 9"), h=0.59)
set_text(shp(s, "Text 12"), "EL RESULTADO")
set_text(shp(s, "Text 13"), "[+__]", hl=None)
set_text(shp(s, "Text 14"), "[DATO A CONFIRMAR: indicador antes y después]", hl=LIMA)
move(shp(s, "Text 14"), h=0.5)
set_text(shp(s, "Text 15"), "PLANTILLA DE FICHA DE CASO · UNA POR PROYECTO APROBADO")

# ---------------------------------------------------------------- 20 · capítulo 04
s = S[19]
set_text(shp(s, "Text 3"), "CAPÍTULO 04 · LANZAMIENTO Y")
set_text(shp(s, "Text 4"), "CAMPAÑA")
set_text(shp(s, "Text 5"), "MARKETING B2B Y PROSPECTOR")

# ---------------------------------------------------------------- 21 · concepto
s = S[20]
set_text(shp(s, "Text 0"), "06 · CONCEPTO DE CAMPAÑA · BLOQUE D")
set_text(shp(s, "Text 4"), "SIEMPRE HAY UNA JUGADA MEJOR.")
set_text(shp(s, "Text 5"), "Todo problema de negocio tiene una solución que todavía nadie vio. Move 37 la encuentra con IA y la pone a funcionar.")
move(shp(s, "Text 5"), w=9.0, h=0.7)

# ---------------------------------------------------------------- 22 · mensajes
s = S[21]
set_text(shp(s, "Text 0"), "06 · MENSAJES POR SEGMENTO")
set_text(shp(s, "Text 1"), "UN MENSAJE PARA CADA SEGMENTO")
text(s, X0, 2.15, CW, 1.1, "Un mismo concepto, tres promesas. Cada mensaje se apoya en pruebas: casos anonimizados y seguridad para aseguradoras, demo y precio para productores, método y velocidad para otras industrias.", size=13)
for t, d, tn, dn in (("ASEGURADORAS", "Tecnología hecha por gente que entiende el seguro.", "Text 3", "Text 4"),
                     ("PRODUCTORES", "Más tiempo para vender, menos para administrar.", "Text 6", "Text 7"),
                     ("OTRAS INDUSTRIAS", "La jugada que tu operación necesita.", "Text 9", "Text 10")):
    set_text(shp(s, tn), t)
    set_text(shp(s, dn), d)
    move(shp(s, dn), h=0.45)
set_text(shp(s, "Text 11"), FOOT)

# ---------------------------------------------------------------- 23 · 90 días
s = S[22]
set_text(shp(s, "Text 0"), "06 · PLAN DE 90 DÍAS")
set_text(shp(s, "Text 1"), "PREPARAR, LANZAR, CONVERTIR")
text(s, X0, 2.15, CW, 1.2, "LinkedIn es el canal principal [A VALIDAR CON DATOS DE AUDIENCIA]. El plan arranca cuando la marca está aprobada y las semanas exactas se fijan en el kickoff.", size=14, color=BLANCO, hl=LIMA)
for k, t, items, kn, tn, ln, hl in (
        ("MES 1", "PREPARAR", ["Página de LinkedIn y voceros", "Landing y one-pagers por segmento", "Comunicación interna del Grupo"], "Text 3", "Text 4", "Text 5", LIMA),
        ("MES 2", "LANZAR", ["Post de lanzamiento y video manifiesto", "Serie semanal \"Jugada 37\"", "Webinar y prensa sectorial [A VALIDAR]"], "Text 7", "Text 8", "Text 9", AZUL),
        ("MES 3", "CONVERTIR", ["Casos por segmento", "Pauta en LinkedIn [MONTO A DEFINIR]", "Outreach con Prospector"], "Text 11", "Text 12", "Text 13", LIMA)):
    set_text(shp(s, kn), k)
    set_text(shp(s, tn), t)
    set_text(shp(s, ln), items, hl=hl, size=11.5)
    move(shp(s, ln), y=5.15, h=1.1)

# ---------------------------------------------------------------- 24 · piezas y KPIs
s = S[23]
base(s, "06 · PIEZAS Y MEDICIÓN", "QUÉ SALE PRIMERO Y CÓMO SE MIDE")
box(s, X0, 2.2, 4.3, 4.4, AZUL)
kicker(s, X0 + 0.3, 2.45, 3.7, "CAMPAÑA INICIAL", color=LIMA)
text(s, X0 + 0.3, 2.85, 3.7, 3.6, ["Manifiesto de marca (texto y video de 60 s)", "Landing de Move 37", "Tres one-pagers por segmento",
                                   "Serie de carruseles \"Jugada 37\"", "Kit de vocería [A CONFIRMAR]", "Webinar de lanzamiento", "Presentación comercial"],
     size=12, color=BLANCO, bullets=True, after=5, hl=LIMA)
table(s, 5.35, 2.2, 7.1, [3.55, 1.75, 1.8], ["KPI", "ETAPA", "META A 90 DÍAS"], [
    ["Impresiones y alcance en LinkedIn", "Conocimiento", "[META A DEFINIR]"],
    ["Tasa de interacción", "Conocimiento", "[META A DEFINIR]"],
    ["Seguidores con perfil objetivo", "Conocimiento", "[META A DEFINIR]"],
    ["Visitas a la landing", "Consideración", "[META A DEFINIR]"],
    ["Leads calificados (MQL)", "Consideración", "[META A DEFINIR]"],
    ["Tasa de respuesta del outreach", "Conversión", "[META A DEFINIR]"],
    ["Reuniones comerciales", "Conversión", "[META A DEFINIR]"],
    ["Pipeline generado", "Negocio", "[META A DEFINIR]"],
], size=11.5)

# ---------------------------------------------------------------- 25 · prospector
s = S[24]
set_text(shp(s, "Text 0"), "07 · PROSPECTOR · BLOQUE E")
set_text(shp(s, "Text 1"), "PROSPECTOR EN CINCO ETAPAS")
kicker(s, X0, 2.2, 5.5, "MOVE 37 CONSTRUYE", color=LIMA)
text(s, X0, 2.5, 5.5, 1.0, "Motor de datos, integraciones, modelo de scoring, automatización de secuencias y tablero de medición.", size=13, color=BLANCO)
kicker(s, 6.95, 2.2, 5.5, "VÉRTICE APORTA", color=LIMA)
text(s, 6.95, 2.5, 5.5, 1.0, "Perfil de cliente ideal, mensajes, contenidos de las secuencias, reglas de scoring comercial y operación diaria.", size=13, color=BLANCO)
etapas = [("FUENTES", "Bases B2B licenciadas, registros públicos y formularios propios."),
          ("ENRIQUECER", "Rubro, tamaño, cargo y señales. Validación de correos."),
          ("PUNTUAR", "Ajuste al cliente ideal, intención e interacción. Modelo explicable."),
          ("CONTACTAR", "Correo y LinkedIn por segmento, con revisión humana y baja visible."),
          ("MEDIR", "Respuestas, reuniones y pipeline. Ajuste del scoring.")]
for i, (t, d) in enumerate(etapas):
    set_text(shp(s, f"Text {6 + 3 * i}"), t)
    set_text(shp(s, f"Text {7 + 3 * i}"), d)
    move(shp(s, f"Text {7 + 3 * i}"), w=2.2, h=0.75)

# ---------------------------------------------------------------- 26 · cumplimiento
s = S[25]
base(s, "07 · CUMPLIMIENTO DE DATOS PERSONALES", "LEY 25.326 DESDE EL DISEÑO")
req = [("LICITUD Y FINALIDAD", "Solo fuentes con legitimidad comprobable. El art. 27 admite datos con fines publicitarios si vienen de fuentes públicas, del titular o con su consentimiento."),
       ("RETIRO Y BLOQUEO", "Cada mensaje identifica al remitente y ofrece una baja simple. El retiro se ejecuta en un plazo definido [A DEFINIR]."),
       ("MINIMIZACIÓN", "Solo datos profesionales necesarios para el contacto. Nunca datos sensibles."),
       ("SEGURIDAD", "Accesos por rol, cifrado, registro de actividad y política de retención y borrado."),
       ("INSCRIPCIÓN DE LA BASE", "Evaluar la inscripción ante la Agencia de Acceso a la Información Pública [A VALIDAR CON ASESORÍA LEGAL]."),
       ("OTROS MARCOS", "Registro Nacional No Llame (Ley 26.951) si hay llamados. Términos de uso de cada plataforma: nada de extracción no permitida.")]
cw, ch = (CW - 2 * 0.17) / 3, 1.85
for i, (t, d) in enumerate(req):
    x, y = X0 + (i % 3) * (cw + 0.17), 2.2 + (i // 3) * (ch + 0.17)
    box(s, x, y, cw, ch, BLANCO)
    head(s, x + 0.22, y + 0.2, cw - 0.44, 0.4, t, size=18)
    text(s, x + 0.22, y + 0.65, cw - 0.44, 1.1, d, size=11, color=GRIS)
box(s, X0, 6.24, CW, 0.46, ROJO)
text(s, X0 + 0.25, 6.24, CW - 0.5, 0.46, "Prospector no opera sin dictamen de asesoría legal. Los datos de asegurados del Grupo no se usan para prospección sin base legal específica.", size=11.5, anchor="ctr")

# ---------------------------------------------------------------- 27 · esfuerzo
s = S[26]
set_text(shp(s, "Text 0"), "07 · ESFUERZO Y COSTOS")
set_text(shp(s, "Text 1"), "UN MVP EN CUATRO TRAMOS")
text(s, X0, 2.12, CW, 0.85, "* Estimación preliminar de Vértice: un líder técnico y dos desarrolladores de Move 37, más estrategia y contenidos de Vértice [DATO A CONFIRMAR]. Costos recurrentes: bases B2B, APIs de enriquecimiento, nube, modelos de IA, envío y CRM, asesoría legal [MONTOS A DEFINIR].", size=11.5)
tramos = [("1 · DISCOVERY", "Cliente ideal, fuentes, arquitectura y revisión legal · 2 a 3 semanas* · [MONTO A DEFINIR]", LIMA),
          ("2 · MVP DE DATOS", "Ingesta, enriquecimiento y scoring básico · 6 a 8 semanas* · [MONTO A DEFINIR]", ROJOT),
          ("3 · SECUENCIAS", "Outreach, revisión humana e integración con CRM · 4 a 6 semanas* · [MONTO A DEFINIR]", ROJOT),
          ("4 · PILOTO", "Operación real con un segmento, medición y ajustes · 4 semanas* · [MONTO A DEFINIR]", ROJOT)]
for i, (t, d, hl) in enumerate(tramos):
    set_text(shp(s, f"Text {3 + 3 * i}"), t)
    set_text(shp(s, f"Text {4 + 3 * i}"), d, hl=hl)
    move(shp(s, f"Text {4 + 3 * i}"), w=8.35)
set_text(shp(s, "Text 14"), FOOT)

# ---------------------------------------------------------------- 28 · capítulo 05
s = S[27]
set_text(shp(s, "Text 3"), "CAPÍTULO 05 · CÓMO LO")
set_text(shp(s, "Text 4"), "HACEMOS")
set_text(shp(s, "Text 5"), "PART TIME, CRONOGRAMA Y RIESGOS")
move(shp(s, "Text 5"), x=2.67, w=8.0)

# ---------------------------------------------------------------- 29 · part time
s = S[28]
base(s, "08 · DEDICACIÓN PART TIME · BLOQUE F", "CINCO ÁREAS, HORAS DEFINIDAS")
table(s, X0, 2.2, CW, [1.9, 2.75, 4.6, 2.31], ["ÁREA", "DEDICACIÓN PROPUESTA*", "ENTREGABLES MENSUALES", "PERFIL"], [
    ["Estrategia", "16 h/mes (2 días)", "Comité mensual, plan trimestral y reporte de KPIs.", "Dirección de estrategia"],
    ["Marca", "24 h/mes en Fase 1 · 16 h/mes después", "Plataforma e identidad en Fase 1. Después, guardianía y piezas clave.", "Dirección de arte y redacción"],
    ["Contenidos", "40 h/mes (5 días)", "Calendario, posts de LinkedIn [CANTIDAD A VALIDAR], un caso y newsletter.", "Redacción y diseño"],
    ["Performance", "16 h/mes (2 días)", "Pauta en LinkedIn, optimización de la landing y reporte.", "Especialista en performance"],
    ["Prospector", "24 h/mes (3 días)", "Cliente ideal, mensajes, secuencias y revisión semanal de leads.", "Estratega de growth B2B"],
], size=12)
text(s, X0, 5.95, CW, 0.5, "* Propuesta inicial de Vértice, ajustable tras el kickoff. Las horas se informan en el reporte mensual.", size=11.5, color=GRIS)

# ---------------------------------------------------------------- 30 · paquetes
s = S[29]
base(s, "08 · PAQUETES Y CONDICIONES", "TRES PAQUETES MENSUALES")
packs = [("DESPEGUE", "Estrategia · Marca · Contenidos base", "64 H"),
         ("CRECIMIENTO", "Estrategia · Marca · Contenidos · Performance", "88 H"),
         ("INTEGRAL", "Las cinco áreas, incluido Prospector · recomendado", "112 H")]
pw = (CW - 2 * 0.17) / 3
for i, (t, areas, hrs) in enumerate(packs):
    x, dark = X0 + i * (pw + 0.17), i == 2
    box(s, x, 2.2, pw, 2.2, CARBON if dark else BLANCO)
    head(s, x + 0.25, 2.4, pw - 0.5, 0.5, t, size=26, color=LIMA if dark else NEGRO)
    text(s, x + 0.25, 2.95, pw - 0.5, 0.5, areas, size=11.5, color=BLANCO if dark else GRIS)
    head(s, x + 0.25, 3.45, 1.6, 0.6, hrs, size=34, color=BLANCO if dark else NEGRO)
    text(s, x + 1.9, 3.62, pw - 2.15, 0.6, ["por mes", "[MONTO A DEFINIR]"], size=11, color=BLANCO if dark else NEGRO, hl=LIMA if dark else ROJOT)
kicker(s, X0, 4.65, 5.5, "CONDICIONES")
text(s, X0, 4.95, 5.6, 1.7, ["Plazo mínimo de contratación [A DEFINIR].", "Facturación mensual. Moneda y ajuste [A DEFINIR].",
                             "Horas no acumulables entre meses [A CONFIRMAR].", "Fuera de alcance: pauta, producción audiovisual y licencias."],
     size=11.5, bullets=True, after=3)
kicker(s, 6.85, 4.65, 5.5, "SUPUESTOS")
text(s, 6.85, 4.95, 5.6, 1.7, ["Un interlocutor único por parte de Move 37.", "Aprobaciones del Grupo en un plazo acordado [A DEFINIR].",
                               "Acceso a la información de proyectos para los casos.", "Integral se recomienda porque Prospector depende de la estrategia y los contenidos."],
     size=11.5, bullets=True, after=3)

# ---------------------------------------------------------------- 31 · cronograma
s = S[30]
set_text(shp(s, "Text 0"), "09 · CRONOGRAMA GENERAL")
set_text(shp(s, "Text 1"), "12 MESES EN SEIS FASES")
text(s, X0, 2.15, CW, 0.9, "Duraciones propuestas, no comprometidas: dependen de la aprobación del Grupo en F0, la disponibilidad del equipo de Move 37 y el dictamen legal sobre Prospector.", size=13)
for m in range(12):
    set_text(shp(s, f"Text {2 + m}"), f"M{m + 1}")
fases = [("F0 · Validación", "Text 14", "Shape 15", 0, 1, "F9BB02", None),
         ("F1 · Marca y oferta", "Text 16", "Shape 17", 0, 3, "B485FF", None),
         ("F2 · Lanzamiento", "Text 18", "Shape 19", 3, 3, "FBFBFB", "000000"),
         ("F3 · Prospector MVP", "Text 20", "Shape 21", 3, 4, "B485FF", None),
         ("F4 · Ventas piloto", "Text 22", "Shape 23", 5, 4, "FBFBFB", "000000"),
         ("F5 · Escala y línea B", "Text 24", "Shape 25", 8, 4, "FF73B9", None)]
from pptx.dml.color import RGBColor
for label, tn, bn, m0, n, col, ln in fases:
    set_text(shp(s, tn), label)
    move(shp(s, tn), w=2.0)
    b = shp(s, bn)
    move(b, x=2.89 + 0.8 * m0 + 0.02, w=0.8 * n - 0.04)
    b.fill.solid()
    b.fill.fore_color.rgb = RGBColor.from_string(col)
    if ln:
        b.line.color.rgb = RGBColor.from_string(ln)
        b.line.width = Pt(0.75)
    else:
        b.line.fill.background()
drop(s, "Shape 26")
set_text(shp(s, "Text 27"), "COLORES DE PILAR COCREATE · AMARILLO: ENTENDER · VIOLETA: TRANSFORMAR · BLANCO: CONECTAR · ROSA: IMPACTAR")

# ---------------------------------------------------------------- 32 · riesgos
s = S[31]
base(s, "10 · RIESGOS", "RIESGOS Y CÓMO LOS MITIGAMOS")
table(s, X0, 2.2, CW, [4.1, 1.45, 1.2, 4.81], ["RIESGO", "PROBABILIDAD", "IMPACTO", "MITIGACIÓN"], [
    ["Conflicto entre la demanda interna del Grupo y la comercial", "Alta", "Alto", "Cupo de capacidad comercial y gobierno de prioridades en F0."],
    ["Las aseguradoras no le compran a un proveedor de otro grupo", "Media", "Alto", "Marca independiente, confidencialidad y separación operativa demostrables."],
    ["El nombre Move 37 no resulta registrable", "Media", "Medio", "Búsqueda de anterioridades en F0 y alternativas de naming listas."],
    ["Prospector incumple la normativa de datos", "Baja con controles", "Alto", "Dictamen legal previo, baja en cada mensaje y fuentes auditadas."],
    ["Se publica información confidencial del Grupo", "Baja", "Alto", "Anonimización y aprobación escrita de cada caso."],
    ["Precios sin base de costos", "Media", "Medio", "Costeo con el CFO antes de publicar precios."],
    ["Bajo rendimiento de LinkedIn en algún segmento", "Media", "Medio", "Validación temprana y canales alternativos: eventos, cámaras y prensa sectorial."],
], size=11)

# ---------------------------------------------------------------- 33 · próximos pasos
s = S[32]
set_text(shp(s, "Text 0"), "10 · SUPUESTOS Y PRÓXIMOS PASOS")
set_text(shp(s, "Text 1"), "SEIS PASOS PARA ARRANCAR")
kicker(s, X0, 2.15, 8, "SUPUESTOS DE ESTA PROPUESTA", color=LIMA)
text(s, X0, 2.45, CW, 2.3, ["El Grupo aprueba explorar la comercialización de Move 37.",
                            "Move 37 puede destinar capacidad a clientes externos [DATO A CONFIRMAR].",
                            "Hay acceso al inventario de los más de 40 proyectos.",
                            "Cifras de mercado, precios y metas se completan en la Fase 0.",
                            "Toda aplicación de la marca Paraná requiere aprobación del Grupo."],
     size=12.5, color=BLANCO, bullets=True, after=3, hl=LIMA)
pasos = [("FASE 0", "Aprobación · Dirección del Grupo"), ("TALLER", "Marca · CEO, Director Comercial y Vértice"),
         ("REGISTRO", "Anterioridades del nombre · asesoría de marcas"), ("INVENTARIO", "Proyectos y casos · Move 37"),
         ("DICTAMEN", "Prospector · asesoría legal"), ("PRECIOS", "Costeo · CFO y equipo comercial de Vértice")]
im1, im4 = shp(s, "Image 1"), shp(s, "Image 4")
x1, x4, y1, y4 = im1.left, im4.left, im1.top, im4.top
im1.left, im4.left = x4 + (im4.width - im1.width) // 2, x1
im1.top = y4 + (im4.height - im1.height) // 2
for i, (t, d) in enumerate(pasos):
    a, b = shp(s, f"Text {5 + 2 * i}"), shp(s, f"Text {6 + 2 * i}")
    set_text(a, t)
    set_text(b, d)
    move(a, y=5.6)
    move(b, y=6.13, h=0.6)
    set_text(a, t, color=LIMA if i == 0 else BLANCO)
    set_text(b, d, bold=(i == 0))

# ---------------------------------------------------------------- 34 · anexo
s = S[33]
base(s, "ANEXO · DATOS A CONFIRMAR", "DATOS A CONFIRMAR EN LA FASE 0")
table(s, X0, 2.2, CW, [0.5, 6.6, 1.1, 3.36], ["#", "DATO", "BLOQUE", "RESPONSABLE SUGERIDO"], [
    ["1", "Tamaño del mercado de aseguradoras y productores y su gasto en tecnología", "B", "Vértice · fuente SSN"],
    ["2", "Gasto en soluciones de IA en otras industrias", "B", "Vértice"],
    ["3", "Relevamiento de competidores por categoría", "B", "Vértice"],
    ["4", "Tamaño de la red de productores del Grupo", "B", "Dirección Comercial del Grupo"],
    ["5", "Disponibilidad registral y usos de \"Move 37\"", "A", "Asesoría de marcas"],
    ["6", "Aprobación del uso de la marca Paraná en la firma de respaldo", "A", "Dirección del Grupo"],
    ["7", "Inventario de proyectos, resultados y nivel de confidencialidad", "C", "Move 37"],
    ["8", "Capacidad disponible y costo hora del equipo de Move 37", "C · E", "Move 37 · CFO"],
    ["9", "Precios por nivel y paquetes part time", "C · F", "Equipo comercial de Vértice · CFO"],
    ["10", "Metas de KPIs y presupuesto de pauta", "D", "Vértice · Move 37"],
    ["11", "Dictamen sobre Ley 25.326, inscripción de la base y fuentes", "E", "Asesoría legal"],
], size=11, first_bold=False)

# ---------------------------------------------------------------- 35 · cierre
s = S[34]
set_text(shp(s, "Text 0"), "VÉRTICE · PROPUESTA PARA MOVE 37")
move(shp(s, "Text 0"), x=3.67, w=6.0)
text(s, 2.67, 5.95, 8.0, 0.35, "Contacto Vértice: [DATO A CONFIRMAR]", size=12, color=BLANCO, align="ctr", hl=LIMA)

# Notas del orador: vacías (el template trae instrucciones de uso que no van al cliente)
for sl in prs.slides:
    if sl.has_notes_slide:
        sl.notes_slide.notes_text_frame.text = ""

prs.core_properties.title = "Propuesta Vértice para Move 37"
prs.core_properties.author = "Vértice"
prs.save(OUT)
print("OK", OUT)
