// Propuesta Vértice para Move 37 — deck estructurado con identidad Vértice
const path = require("path");
const pptxgen = require("pptxgenjs");
const SKILL = "/root/.claude/skills/synced/dce9a52a-1689-4ec5-925a-864a6d708050_1286b7b6-a582-46b0-b30e-3be5f35deb77/pptx";
const { applyTheme } = require(SKILL + "/scripts/apply_theme.js");

const OUT = process.argv[2] || "/home/user/claude/propuesta-move-37-vertice.pptx";

const THEME = {
  name: "Vertice",
  headFontFace: "Tusker Grotesk",
  bodyFontFace: "Arial",
  colors: {
    dk1: "000000", lt1: "FFFFFF", dk2: "131313", lt2: "F2F2F0",
    accent1: "F10A09", // Rojo VERTICE
    accent2: "0024AD", // Azul eléctrico
    accent3: "D7FE51", // Lima
    accent4: "C60807", // Rojo texto
    accent5: "5A5A5A", // Gris texto
    accent6: "8A8A8A", // Gris meta
    hlink: "0024AD", folHlink: "0024AD",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.author = "Vértice";
pres.company = "Vértice";
pres.title = "Propuesta Vértice para Move 37";
pres.subject = "Plan integral para convertir Move 37 en una oferta tecnológica comercial";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };

const C = pres.SchemeColor;
const K = {
  negro: C.text1, blanco: C.background1, carbon: C.text2, papel: C.background2,
  rojo: C.accent1, azul: C.accent2, lima: C.accent3, rojoT: C.accent4, gris: C.accent5, meta: C.accent6,
};
// Hex solo donde la opción no acepta colores de esquema
const LINEA = "E0E0DC";
const CAPS = { hub: "F9BB02", lens: "B485FF", spark: "FBFBFB", aon: "FF73B9" };

const W = 13.333, M = 0.5, CW = W - 2 * M;
const FOOT = "VÉRTICE  ·  PROPUESTA PARA MOVE 37  ·  BORRADOR PARA DISCUSIÓN  ·  NOVIEMBRE 2026";

// ---------- Filete con remates (firma gráfica) ----------
function fileteObjs(color, y, x = M, w = CW) {
  return [
    { rect: { x, y: y - 0.007, w, h: 0.014, fill: { color } } },
    { rect: { x, y: y - 0.021, w: 0.125, h: 0.042, fill: { color } } },
    { rect: { x: x + w - 0.125, y: y - 0.021, w: 0.125, h: 0.042, fill: { color } } },
  ];
}
function filete(slide, color, y, x = M, w = CW, name = "filete") {
  slide.addShape(pres.shapes.RECTANGLE, { objectName: name + "-linea", x, y: y - 0.007, w, h: 0.014, fill: { color }, line: { type: "none" } });
  slide.addShape(pres.shapes.RECTANGLE, { objectName: name + "-remate-izq", x, y: y - 0.021, w: 0.125, h: 0.042, fill: { color }, line: { type: "none" } });
  slide.addShape(pres.shapes.RECTANGLE, { objectName: name + "-remate-der", x: x + w - 0.125, y: y - 0.021, w: 0.125, h: 0.042, fill: { color }, line: { type: "none" } });
}

// ---------- Layouts ----------
function defLayout(title, bg, fil, kick, ttl, foot, size, h) {
  pres.defineSlideMaster({
    title,
    background: { color: bg },
    margin: [0.5, 0.5, 0.6, 0.5],
    objects: [
      ...fileteObjs(fil, 0.5),
      { text: { text: FOOT, options: { x: M, y: 7.02, w: 10, h: 0.22, fontSize: 8, color: foot, charSpacing: 1.5, margin: 0 } } },
      { placeholder: { options: { name: "kicker", type: "body", x: M, y: 0.64, w: CW, h: 0.26, fontSize: 10, color: kick, margin: 0, charSpacing: 2, valign: "top" }, text: "" } },
      { placeholder: { options: { name: "title", type: "title", x: M, y: 0.98, w: CW, h, fontSize: size, bold: true, color: ttl, margin: 0, valign: "top", align: "left" }, text: "" } },
    ],
    slideNumber: { x: W - M - 0.6, y: 7.02, w: 0.6, h: 0.22, fontSize: 8, color: foot, align: "right" },
  });
}
defLayout("PAPEL", K.papel, K.negro, K.rojoT, K.negro, K.meta, 32, 0.75);
defLayout("ROJO", K.rojo, K.negro, K.negro, K.blanco, K.negro, 54, 1.6);
defLayout("AZUL", K.azul, K.blanco, K.lima, K.blanco, K.blanco, 44, 1.2);
defLayout("NEGRO", K.negro, K.blanco, K.lima, K.lima, K.meta, 44, 1.2);
defLayout("LIMA", K.lima, K.negro, K.negro, K.negro, K.negro, 44, 1.2);

// ---------- Helpers ----------
let curSection = "";
function section(t) { curSection = t; pres.addSection({ title: t }); }
function newSlide(layout, kicker, title) {
  const s = pres.addSlide({ masterName: layout, sectionTitle: curSection });
  if (kicker) s.addText(kicker, { placeholder: "kicker", charSpacing: 2 });
  if (title) s.addText(title, { placeholder: "title" });
  return s;
}
// Marca [DATO A CONFIRMAR] y similares en rojo texto + negrita
function rich(text, base = {}, flag = K.rojoT) {
  const parts = String(text).split(/(\[[^\]]+\])/g).filter((p) => p !== "");
  return parts.map((p) => ({ text: p, options: Object.assign({}, base, /^\[.*\]$/.test(p) ? { color: flag, bold: true } : {}) }));
}
let nameIdx = 0;
function T(slide, text, o = {}) {
  const { flag: _f, ...oo } = o; const opts = Object.assign({ isTextBox: true, margin: 0, fontSize: 14, color: K.negro, valign: "top", objectName: "texto-" + ++nameIdx }, oo);
  slide.addText(typeof text === "string" ? rich(text, {}, o.flag || K.rojoT) : text, opts);
}
function bullets(items, base = {}, flag = K.rojoT) {
  const out = [];
  items.forEach((it, i) => {
    const runs = rich(it, base, flag);
    runs[0].options = Object.assign({}, runs[0].options, { bullet: { indent: 14 }, paraSpaceAfter: 5 });
    if (i < items.length - 1) runs[runs.length - 1].options.breakLine = true;
    out.push(...runs);
  });
  return out;
}
function box(slide, x, y, w, h, fill, name, opt = {}) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign({ objectName: name || "tarjeta-" + ++nameIdx, x, y, w, h, fill: { color: fill }, rectRadius: 0.08, line: { type: "none" } }, opt));
}
function outline(slide, x, y, w, h, color, name) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { objectName: name || "caja-outline-" + ++nameIdx, x, y, w, h, fill: { type: "none" }, rectRadius: 0.16, line: { color, width: 1 } });
}
function kick(slide, text, x, y, w, color = K.rojoT, size = 10) {
  T(slide, text, { x, y, w, h: 0.25, fontSize: size, color, charSpacing: 2 });
}
function head(slide, text, x, y, w, color = K.negro, size = 20, h = 0.4) {
  T(slide, text, { x, y, w, h, fontSize: size, bold: true, color, fontFace: "+mj-lt" });
}
// Tabla con estilo de documento
function table(slide, header, rows, o) {
  const fs = o.fontSize || 11;
  const hdr = header.map((h) => ({ text: h, options: { bold: true, color: K.blanco, fill: { color: o.headFill || K.carbon }, fontSize: fs - 1, charSpacing: 1, valign: "middle" } }));
  const border = [{ type: "none" }, { type: "none" }, { type: "solid", pt: 0.75, color: LINEA }, { type: "none" }];
  const body = rows.map((r, ri) =>
    r.map((c, ci) => {
      const isObj = c && typeof c === "object" && !Array.isArray(c);
      const txt = isObj ? c.text : c;
      const extra = isObj ? c.options || {} : {};
      const baseRun = { fontSize: fs, color: K.negro, bold: (o.boldFirst && ci === 0) || extra.bold };
      return { text: rich(txt, baseRun), options: Object.assign({ fill: { color: (o.hl && o.hl(ri)) || K.blanco }, border, valign: "top" }, extra) };
    })
  );
  slide.addTable([hdr, ...body], {
    x: o.x, y: o.y, w: o.w, colW: o.colW, margin: [0.07, 0.09, 0.07, 0.09], fontSize: fs, color: K.negro,
    border: { type: "solid", pt: 0.75, color: LINEA }, rowH: o.rowH, autoPage: false, objectName: o.name || "tabla-" + ++nameIdx,
  });
}

// =====================================================================
// PORTADA
// =====================================================================
section("Portada");
{
  const s = pres.addSlide({ masterName: "ROJO", sectionTitle: curSection });
  s.addText("VÉRTICE  ·  COMUNICACIÓN B2B, MARCA Y ESTRATEGIA DE MARKETING", { placeholder: "kicker", charSpacing: 2 });
  T(s, "PROPUESTA PARA", { x: M, y: 1.25, w: CW, h: 0.6, fontSize: 28, bold: true, color: K.blanco, fontFace: "+mj-lt" });
  T(s, "MOVE 37", { x: M, y: 1.8, w: CW, h: 2.3, fontSize: 150, bold: true, color: K.blanco, fontFace: "+mj-lt" });
  T(s, "Plan integral para convertir al equipo de tecnología del Grupo Asegurador Paraná en una oferta tecnológica comercial.", { x: M, y: 4.35, w: 7.4, h: 0.9, fontSize: 18, color: K.negro });
  outline(s, M, 5.55, 5.9, 1.05, K.negro, "caja-datos-portada");
  T(s, [
    { text: "Cliente: ", options: { bold: true } }, { text: "Move 37 · Grupo Asegurador Paraná", options: { breakLine: true } },
    { text: "Versión: ", options: { bold: true } }, { text: "borrador para discusión · noviembre 2026", options: { breakLine: true } },
    { text: "Confidencial. Uso de la marca Paraná sujeto a aprobación del Grupo.", options: {} },
  ], { x: M + 0.2, y: 5.68, w: 5.6, h: 0.85, fontSize: 12, color: K.negro });
  s.addNotes("Portada. La propuesta se presenta con la identidad de Vértice. La identidad de Move 37 es un entregable del bloque A y no se asume de antemano.");
}

// =====================================================================
// 1. RESUMEN EJECUTIVO
// =====================================================================
section("1. Resumen ejecutivo");
{
  const s = newSlide("PAPEL", "01 · RESUMEN EJECUTIVO", "SEIS DECISIONES PARA VOLVERSE NEGOCIO");
  const recs = [
    ["A · MARCA", "Marca independiente con respaldo del Grupo", "Permite vender a competidores del Grupo y a otras industrias sin quedar atada a una aseguradora, y el respaldo traslada más de 60 años de confianza."],
    ["B · OPORTUNIDAD", "Primero seguros y productores, después otras industrias", "El conocimiento del negocio asegurador y los proyectos internos acortan la venta. Otras industrias entran en una segunda ola, con casos propios."],
    ["C · SERVICIOS", "Oferta en cuatro modalidades con precios por nivel", "Proyecto, producto, suscripción y staff part time cubren desde un productor hasta una aseguradora. Montos: [MONTO A DEFINIR]."],
    ["D · CAMPAÑA", "Lanzamiento B2B de 90 días con LinkedIn como canal principal", "Mensajes distintos para aseguradoras, productores y otras industrias. La prioridad de LinkedIn queda [A VALIDAR] con datos de audiencia."],
    ["E · PROSPECTOR", "Sistema propio de captación de leads B2B", "Se desarrolla con Move 37, funciona como primer producto vitrina y cumple la Ley 25.326 desde el diseño."],
    ["F · VÉRTICE PART TIME", "Equipo dedicado por área con paquetes mensuales", "Estrategia, marca, contenidos, performance y Prospector con horas definidas y entregables mensuales. Montos: [MONTO A DEFINIR]."],
  ];
  const cw = (CW - 2 * 0.3) / 3, ch = 2.1;
  recs.forEach((r, i) => {
    const x = M + (i % 3) * (cw + 0.3), y = 1.9 + Math.floor(i / 3) * (ch + 0.2);
    box(s, x, y, cw, ch, K.blanco, "resumen-tarjeta-" + (i + 1));
    kick(s, r[0], x + 0.22, y + 0.2, cw - 0.44);
    T(s, r[1], { x: x + 0.22, y: y + 0.5, w: cw - 0.44, h: 0.6, fontSize: 15, bold: true });
    T(s, r[2], { x: x + 0.22, y: y + 1.12, w: cw - 0.44, h: 0.95, fontSize: 11.5, color: K.gris });
  });
  box(s, M, 6.38, CW, 0.5, K.carbon, "resumen-decision");
  T(s, "Qué pedimos hoy: aprobar la Fase 0 de validación de marca, mercado, proyectos y aspectos legales. Plazos y montos dependen de los supuestos de la sección 10.", { x: M + 0.2, y: 6.43, w: CW - 0.4, h: 0.4, fontSize: 11.5, color: K.blanco, valign: "middle" });
}

// =====================================================================
// 2. CONTEXTO Y OBJETIVOS
// =====================================================================
section("2. Contexto y objetivos");
{
  const s = newSlide("PAPEL", "02 · CONTEXTO", "UN GRUPO DE 60 AÑOS, UN EQUIPO QUE YA HACE IA");
  // Columna Grupo
  box(s, M, 1.95, 6.0, 4.85, K.blanco, "contexto-grupo");
  kick(s, "GRUPO ASEGURADOR PARANÁ", M + 0.25, 2.15, 5.5);
  T(s, bullets([
    "Integración estratégica de Paraná Seguros y Paraná ART.",
    "Más de 60 años en el mercado asegurador argentino. Paraná Seguros opera desde 1961.",
    "Paraná Seguros: Automotores, Motovehículos, Caución, Accidentes Personales, Vida, Hogar y Combinado Familiar, Responsabilidad Civil, Embarcaciones de Placer, Transporte de Mercaderías, Integral de Consorcio e Integral de Comercio e Industria.",
    "Paraná ART: prevención, seguridad laboral y cobertura de accidentes de trabajo y enfermedades profesionales.",
    "Canales digitales: Mi Pas, Mi Móvil, Tero Granizo y Paraná 24.",
    "Autoridades: Lic. Mariano Devoto (CEO), José Aramburu (Director Comercial), Mauro Gualco (CFO).",
  ], { fontSize: 12 }), { x: M + 0.25, y: 2.5, w: 5.5, h: 4.2, fontSize: 12 });
  // Columna Move 37
  box(s, 6.83, 1.95, 6.0, 4.85, K.carbon, "contexto-move37");
  kick(s, "MOVE 37 HOY", 7.08, 2.15, 5.5, K.lima);
  T(s, "+40", { x: 7.08, y: 2.5, w: 2.6, h: 1.1, fontSize: 72, bold: true, color: K.lima, fontFace: "+mj-lt" });
  T(s, "proyectos de herramientas basadas en IA, principalmente de uso interno", { x: 7.08, y: 3.6, w: 2.6, h: 0.9, fontSize: 12, color: K.blanco });
  T(s, "<2", { x: 10.08, y: 2.5, w: 2.5, h: 1.1, fontSize: 72, bold: true, color: K.lima, fontFace: "+mj-lt" });
  T(s, "años de operación para llegar a ese volumen", { x: 10.08, y: 3.6, w: 2.5, h: 0.9, fontSize: 12, color: K.blanco });
  filete(s, K.blanco, 4.75, 7.08, 5.5, "filete-move37");
  T(s, bullets([
    "Opera en oficinas separadas del Grupo.",
    "No está constituido como marca.",
    "Su razón de ser es prestar servicios tecnológicos a todas las marcas del Grupo.",
  ], { fontSize: 12, color: K.blanco }), { x: 7.08, y: 4.95, w: 5.5, h: 1.6, fontSize: 12, color: K.blanco });
}
{
  const s = newSlide("AZUL", "02 · LA OPORTUNIDAD", "DOS CAMINOS PARA QUE MOVE 37 SEA UN NEGOCIO");
  const cw = (CW - 0.4) / 2;
  [["CAMINO A", "Seguros y productores", "Vender soluciones tecnológicas a compañías de seguros y a productores, aprovechando el conocimiento sectorial del Grupo."],
   ["CAMINO B", "Cualquier industria", "Producir herramientas y soluciones tecnológicas para empresas de otros sectores, con el método probado en más de 40 proyectos."]].forEach((c, i) => {
    const x = M + i * (cw + 0.4);
    outline(s, x, 2.45, cw, 2.35, K.blanco, "camino-" + (i ? "b" : "a"));
    kick(s, c[0], x + 0.3, 2.7, cw - 0.6, K.lima);
    T(s, c[1].toUpperCase(), { x: x + 0.3, y: 3.0, w: cw - 0.6, h: 0.6, fontSize: 28, bold: true, color: K.blanco, fontFace: "+mj-lt" });
    T(s, c[2], { x: x + 0.3, y: 3.7, w: cw - 0.6, h: 1.0, fontSize: 14, color: K.blanco });
  });
  kick(s, "OBJETIVO DE ESTA PROPUESTA", M, 5.2, CW, K.lima);
  T(s, "Un plan integral en seis bloques: A posicionamiento y marca · B diagnóstico y oportunidades · C servicios · D campaña y marketing · E Prospector · F servicios part time de Vértice. Cada recomendación incluye su justificación y marca lo que el Grupo tiene que validar.", { x: M, y: 5.5, w: 11.5, h: 1.0, fontSize: 15, color: K.blanco, flag: K.lima });
}

// =====================================================================
// 3. DIAGNÓSTICO Y OPORTUNIDADES (B)
// =====================================================================
section("3. Diagnóstico y oportunidades");
{
  const s = newSlide("PAPEL", "03 · DIAGNÓSTICO Y OPORTUNIDADES · BLOQUE B", "QUÉ SABEMOS DE CADA LÍNEA Y QUÉ FALTA MEDIR");
  table(s, ["DIMENSIÓN", "LÍNEA A · SEGUROS Y PRODUCTORES", "LÍNEA B · OTRAS INDUSTRIAS"], [
    ["Tamaño de mercado", "Cantidad de aseguradoras y productores matriculados en Argentina y su gasto en tecnología [DATO A CONFIRMAR · fuente sugerida: SSN]", "Gasto en soluciones de IA de empresas medianas y grandes en Argentina [DATO A CONFIRMAR · estudio de mercado]"],
    ["Perfil de demanda", "Aseguradoras: automatización de suscripción, siniestros y atención, con compras largas que pasan por sistemas y compliance. Productores: herramientas simples, precio accesible y adopción rápida.", "Empresas con procesos repetitivos y alto volumen de documentos o de atención. Decide operaciones o tecnología. Demanda heterogénea."],
    ["Competidores (categorías)", "Insurtechs, proveedores de software core para seguros y consultoras de transformación digital [relevamiento A CONFIRMAR]", "Consultoras e integradores, software factories, agencias de IA y plataformas SaaS globales [relevamiento A CONFIRMAR]"],
    ["Barreras de entrada", "Regulación de la SSN y seguridad de la información. Reparos de una aseguradora a comprarle a un proveedor que pertenece a otro grupo asegurador. Integración con sistemas heredados.", "Falta de credenciales fuera de seguros, competencia por precio y necesidad de casos de otras industrias."],
    ["Ventaja de Move 37", "Conoce el negocio asegurador desde adentro, tiene más de 40 proyectos con usuarios reales y el respaldo de un grupo con más de 60 años.", "Velocidad de producción y método probado. Menor diferenciación que en seguros."],
  ], { x: M, y: 1.95, w: CW, colW: [2.2, 5.065, 5.068], fontSize: 11, boldFirst: true });
}
{
  const s = newSlide("PAPEL", "03 · PRIORIZACIÓN", "PRIMERO PRODUCTORES: MÁS ATRACTIVO Y VIABLE");
  const gx = 1.2, gy = 1.95, gw = 6.6, gh = 4.6, hw = gw / 2, hh = gh / 2;
  s.addShape(pres.shapes.RECTANGLE, { objectName: "matriz-q-apostar", x: gx, y: gy, w: hw, h: hh, fill: { color: K.blanco }, line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { objectName: "matriz-q-priorizar", x: gx + hw, y: gy, w: hw, h: hh, fill: { color: K.lima }, line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { objectName: "matriz-q-postergar", x: gx, y: gy + hh, w: hw, h: hh, fill: { color: K.blanco }, line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { objectName: "matriz-q-oportunista", x: gx + hw, y: gy + hh, w: hw, h: hh, fill: { color: K.blanco }, line: { type: "none" } });
  s.addShape(pres.shapes.LINE, { objectName: "matriz-eje-v", x: gx + hw, y: gy, w: 0, h: gh, line: { color: LINEA, width: 1 } });
  s.addShape(pres.shapes.LINE, { objectName: "matriz-eje-h", x: gx, y: gy + hh, w: gw, h: 0, line: { color: LINEA, width: 1 } });
  [["CONSTRUIR CAPACIDAD", gx + 0.15, gy + 0.12], ["PRIORIZAR", gx + hw + 0.15, gy + 0.12], ["POSTERGAR", gx + 0.15, gy + hh + 0.12], ["OPORTUNISTA", gx + hw + 0.15, gy + hh + 0.12]].forEach((q) => T(s, q[0], { x: q[1], y: q[2], w: 3, h: 0.22, fontSize: 9, color: K.negro, charSpacing: 1.5 }));
  T(s, "CAPACIDAD DE EJECUCIÓN  →", { x: gx, y: gy + gh + 0.08, w: gw, h: 0.25, fontSize: 9, color: K.gris, charSpacing: 1.5, align: "right" });
  T(s, "ATRACTIVO  →", { x: gx - 2.47, y: gy + gh / 2 - 0.12, w: 4.6, h: 0.25, fontSize: 9, color: K.gris, charSpacing: 1.5, align: "right", rotate: 270 });
  const pts = [
    ["1", "Productores de seguros", 0.82, 0.22],
    ["2", "Aseguradoras", 0.66, 0.36],
    ["3", "Otras industrias, procesos con muchos documentos", 0.28, 0.3],
    ["4", "Otras industrias en general", 0.24, 0.7],
  ];
  pts.forEach((p) => {
    const cx = gx + p[2] * gw, cy = gy + p[3] * gh;
    s.addShape(pres.shapes.OVAL, { objectName: "matriz-punto-" + p[0], x: cx - 0.2, y: cy - 0.2, w: 0.4, h: 0.4, fill: { color: K.azul }, line: { type: "none" } });
    T(s, p[0], { x: cx - 0.2, y: cy - 0.2, w: 0.4, h: 0.4, fontSize: 13, bold: true, color: K.blanco, align: "center", valign: "middle" });
    T(s, p[1], { x: cx + 0.28, y: cy - 0.17, w: p[2] > 0.6 ? 1.0 : 2.0, h: 0.6, fontSize: 10.5, color: K.negro });
  });
  // Lectura
  const rx = 8.35, rw = W - M - rx;
  kick(s, "CÓMO LEER LA MATRIZ", rx, 1.95, rw);
  T(s, bullets([
    "1 · Productores: el Grupo ya trabaja con productores [DATO A CONFIRMAR: tamaño de la red], las herramientas son simples y se pueden empaquetar.",
    "2 · Aseguradoras: alto valor por cliente, pero exige independencia operativa y confidencialidad demostrables.",
    "3 · Nicho de otras industrias donde los proyectos internos se trasladan casi sin cambios. Segunda ola.",
    "4 · Otras industrias en general: requiere casos propios y fuerza comercial que hoy no existe.",
  ], { fontSize: 12 }), { x: rx, y: 2.3, w: rw, h: 3.4, fontSize: 12 });
  box(s, rx, 5.85, rw, 0.95, K.blanco, "matriz-nota");
  T(s, "Ubicación preliminar y cualitativa, armada con el criterio de Vértice. Se recalibra con datos de mercado [DATO A CONFIRMAR].", { x: rx + 0.15, y: 5.95, w: rw - 0.3, h: 0.8, fontSize: 10.5, color: K.gris });
}

// =====================================================================
// 4. POSICIONAMIENTO Y MARCA (A)
// =====================================================================
section("4. Posicionamiento y marca");
{
  const s = newSlide("PAPEL", "04 · ARQUITECTURA DE MARCA · BLOQUE A", "MARCA PROPIA, CON EL GRUPO COMO RESPALDO");
  table(s, ["OPCIÓN", "CÓMO FUNCIONA", "A FAVOR", "EN CONTRA", "AJUSTE"], [
    ["Monolítica", "Move 37 se comunica como un área del Grupo, bajo la marca Paraná.", "Confianza inmediata y costo de marca mínimo.", "Otras aseguradoras no le compran a un rival. Se lee como un área de sistemas. Limita el camino B.", "Bajo"],
    ["Submarca", "Paraná + descriptor tecnológico.", "Lanzamiento rápido y apalanca la marca madre.", "Mismo conflicto con competidores y la innovación queda subordinada a la marca de seguros.", "Bajo"],
    [{ text: "Independiente con respaldo (recomendada)", options: { bold: true } }, "Marca propia con la firma \"una compañía del Grupo Asegurador Paraná\", de intensidad variable según el segmento.", "Identidad de tecnología propia y confianza dosificable. Habilita los caminos A y B.", "Requiere invertir en construir la marca y reglas claras de uso del respaldo.", { text: "Alto", options: { bold: true } }],
    ["Independiente sin vínculo", "Marca propia sin mención al Grupo.", "Máxima libertad comercial.", "Pierde la transferencia de confianza y el Grupo no capitaliza la innovación.", "Medio"],
  ], { x: M, y: 1.95, w: CW, colW: [2.0, 3.0, 2.85, 3.48, 1.0], fontSize: 11, boldFirst: true, hl: (r) => (r === 2 ? K.lima : null) });
  box(s, M, 5.55, CW, 1.3, K.blanco, "arquitectura-justificacion");
  kick(s, "POR QUÉ", M + 0.25, 5.68, 3);
  T(s, "La marca independiente resuelve el principal freno comercial, que es venderle a otras aseguradoras, y el respaldo se regula por segmento: fuerte con productores, discreto con aseguradoras y medio con otras industrias. El uso de la marca Paraná en la firma requiere aprobación del Grupo [DATO A CONFIRMAR].", { x: M + 0.25, y: 5.98, w: CW - 0.5, h: 0.8, fontSize: 12.5 });
}
{
  const s = newSlide("NEGRO", "04 · EL CONCEPTO DETRÁS DEL NOMBRE", "LA JUGADA QUE PARECÍA UN ERROR");
  T(s, "37", { x: M, y: 2.2, w: 3.6, h: 3.2, fontSize: 210, bold: true, color: K.lima, fontFace: "+mj-lt" });
  T(s, "En marzo de 2016, en la segunda partida entre Lee Sedol y AlphaGo (Google DeepMind), AlphaGo colocó una piedra en una posición que desafiaba 2500 años de tradición del Go. Los comentaristas la tomaron por un error. Cien movimientos después se reveló como la clave de la victoria.", { x: 4.4, y: 2.3, w: 8.4, h: 1.5, fontSize: 16, color: K.blanco });
  const mets = [["CREATIVIDAD", "Razonamiento estratégico que va más allá de lo convencional."], ["INNOVACIÓN GENUINA", "Soluciones propias, no imitación."], ["TECNOLOGÍA APLICADA", "Problemas que parecen no tener una salida obvia."]];
  const mw = (8.4 - 0.4) / 3;
  mets.forEach((m, i) => {
    const x = 4.4 + i * (mw + 0.2);
    outline(s, x, 4.15, mw, 1.65, K.lima, "metafora-" + (i + 1));
    T(s, m[0], { x: x + 0.18, y: 4.32, w: mw - 0.36, h: 0.3, fontSize: 11, bold: true, color: K.lima, charSpacing: 1.5 });
    T(s, m[1], { x: x + 0.18, y: 4.7, w: mw - 0.36, h: 1.0, fontSize: 12.5, color: K.blanco });
  });
  T(s, "La referencia funciona como inspiración. Move 37 no tiene ni reclama ningún derecho sobre el hecho, sobre AlphaGo ni sobre Google DeepMind, y la comunicación no debe sugerir ningún vínculo con ellos.", { x: 4.4, y: 6.05, w: 8.4, h: 0.7, fontSize: 11, color: "ABABAB" });
}
{
  const s = newSlide("PAPEL", "04 · EVALUACIÓN DEL NOMBRE", "MOVE 37 ES BUEN CANDIDATO, CON CONDICIONES");
  table(s, ["CRITERIO", "EVALUACIÓN", "COMENTARIO"], [
    ["Relato y significado", "Fuerte", "Historia potente y verificable sobre la creatividad de la IA."],
    ["Memorabilidad", "Fuerte", "Corto, con una cifra distintiva."],
    ["Pronunciación en español", "Media", "Mezcla inglés y número. Hay que fijar una forma oral."],
    ["Descriptividad", "Baja", "No dice qué hace. Necesita un descriptor (\"Move 37 · Soluciones de IA\")."],
    ["Disponibilidad registral", "Sin evaluar", "Búsqueda de anterioridades en el INPI, clases 9, 35 y 42 [DATO A CONFIRMAR]."],
    ["Asociación con terceros", "Riesgo medio", "Remite a AlphaGo y Google DeepMind. No usar marcas ni imágenes de terceros."],
    ["Uso del término por terceros", "Sin evaluar", "Relevar empresas, productos y dominios que ya usan \"Move 37\" [DATO A CONFIRMAR]."],
  ], { x: M, y: 1.95, w: 8.1, colW: [2.3, 1.45, 4.35], fontSize: 11, boldFirst: true });
  const rx = 8.9, rw = W - M - rx;
  box(s, rx, 1.95, rw, 4.9, K.azul, "nombre-recomendacion");
  kick(s, "RECOMENDACIÓN", rx + 0.25, 2.15, rw - 0.5, K.lima);
  T(s, bullets([
    "Mantener Move 37 como candidato principal: el equipo ya lo usa y el relato es fuerte.",
    "Antes de adoptarlo como nombre final, cumplir tres condiciones: búsqueda de anterioridades, relevamiento de usos por terceros y disponibilidad de dominio y redes.",
    "Plan B: un taller de naming con dos o tres alternativas dentro del mismo territorio (la jugada inesperada, la estrategia).",
  ], { fontSize: 12.5, color: K.blanco }), { x: rx + 0.25, y: 2.5, w: rw - 0.5, h: 4.2, fontSize: 12.5, color: K.blanco });
}
{
  const s = newSlide("PAPEL", "04 · PLATAFORMA DE MARCA", "PROPÓSITO, VALOR, ATRIBUTOS Y VOZ");
  box(s, M, 1.95, 4.6, 4.9, K.rojo, "plataforma-proposito");
  kick(s, "PROPÓSITO", M + 0.25, 2.15, 4.1, K.negro);
  T(s, "ENCONTRAR LA JUGADA QUE OTROS NO VEN", { x: M + 0.25, y: 2.5, w: 4.1, h: 1.6, fontSize: 32, bold: true, color: K.blanco, fontFace: "+mj-lt" });
  T(s, "Usar la inteligencia artificial para resolver problemas de negocio que parecen no tener una salida obvia.", { x: M + 0.25, y: 4.6, w: 4.1, h: 1.2, fontSize: 14, color: K.negro });
  const rx = 5.4, rw = W - M - rx;
  box(s, rx, 1.95, rw, 1.45, K.blanco, "plataforma-valor");
  kick(s, "PROPUESTA DE VALOR", rx + 0.25, 2.1, rw - 0.5);
  T(s, "Soluciones de IA que ya funcionan en la operación de un grupo asegurador con más de 60 años, listas para adaptarse a otro negocio, hechas por un equipo que concretó más de 40 proyectos en menos de 2 años.", { x: rx + 0.25, y: 2.4, w: rw - 0.5, h: 0.95, fontSize: 13 });
  const attrs = [["Criterio estratégico", "Primero el problema de negocio, después la tecnología."], ["Innovación genuina", "Soluciones propias, no copias de tendencias."], ["Solidez", "Respaldo de un grupo con trayectoria y procesos serios."], ["Velocidad con método", "Entregas rápidas, medibles y documentadas."]];
  const aw = (rw - 0.6) / 4;
  attrs.forEach((a, i) => {
    const x = rx + i * (aw + 0.2);
    box(s, x, 3.6, aw, 1.45, K.blanco, "atributo-" + (i + 1));
    T(s, a[0], { x: x + 0.15, y: 3.72, w: aw - 0.3, h: 0.5, fontSize: 12.5, bold: true });
    T(s, a[1], { x: x + 0.15, y: 4.25, w: aw - 0.3, h: 0.75, fontSize: 11, color: K.gris });
  });
  box(s, rx, 5.25, rw, 1.6, K.carbon, "plataforma-tono");
  kick(s, "TONO DE VOZ · DIRECTO, PRECISO, SIN HYPE", rx + 0.25, 5.38, rw - 0.5, K.lima);
  T(s, [
    { text: "Sí: ", options: { bold: true, color: K.lima } }, { text: "hablar con casos y métricas, explicar simple, decir qué hacemos y cómo lo medimos.", options: { color: K.blanco, breakLine: true } },
    { text: "No: ", options: { bold: true, color: K.lima } }, { text: "promesas mágicas, jerga vacía ni comparaciones con la ciencia ficción.", options: { color: K.blanco } },
  ], { x: rx + 0.25, y: 5.72, w: rw - 0.5, h: 1.05, fontSize: 12.5, paraSpaceAfter: 4 });
}
{
  const s = newSlide("PAPEL", "04 · RELACIÓN DE MARCA", "LA CONFIANZA BAJA, LA INNOVACIÓN SUBE");
  box(s, M, 2.1, 3.4, 3.1, K.carbon, "relacion-grupo");
  T(s, "GRUPO ASEGURADOR PARANÁ", { x: M + 0.25, y: 2.35, w: 2.9, h: 1.0, fontSize: 24, bold: true, color: K.blanco, fontFace: "+mj-lt" });
  T(s, "Trayectoria desde 1961, solvencia y conocimiento del negocio.", { x: M + 0.25, y: 3.75, w: 2.9, h: 1.2, fontSize: 12.5, color: K.blanco });
  box(s, 8.0, 2.1, 3.4, 3.1, K.azul, "relacion-move37");
  T(s, "MOVE 37", { x: 8.25, y: 2.35, w: 2.9, h: 1.0, fontSize: 24, bold: true, color: K.blanco, fontFace: "+mj-lt" });
  T(s, "Tecnología propia, casos de IA en producción y atracción de talento.", { x: 8.25, y: 3.75, w: 2.9, h: 1.2, fontSize: 12.5, color: K.blanco });
  s.addShape(pres.shapes.RIGHT_ARROW, { objectName: "flecha-confianza", x: 4.15, y: 2.35, w: 3.6, h: 1.0, fill: { color: K.rojo }, line: { type: "none" } });
  T(s, "CONFIANZA", { x: 4.3, y: 2.6, w: 2.9, h: 0.45, fontSize: 18, bold: true, color: K.blanco, fontFace: "+mj-lt", valign: "middle" });
  s.addShape(pres.shapes.LEFT_ARROW, { objectName: "flecha-innovacion", x: 4.15, y: 3.95, w: 3.6, h: 1.0, fill: { color: K.lima }, line: { type: "none" } });
  T(s, "INNOVACIÓN", { x: 4.75, y: 4.2, w: 2.9, h: 0.45, fontSize: 18, bold: true, color: K.negro, fontFace: "+mj-lt", valign: "middle", align: "right" });
  kick(s, "CÓMO SE TRANSFIERE", M, 5.5, 6);
  T(s, bullets([
    "Firma de respaldo con tres intensidades por segmento.",
    "Proyectos internos convertidos en casos, con aprobación del Grupo.",
  ], { fontSize: 12.5 }), { x: M, y: 5.8, w: 6.0, h: 1.0, fontSize: 12.5 });
  kick(s, "QUÉ GANA EL GRUPO", 6.83, 5.5, 6);
  T(s, bullets([
    "Comunica a Move 37 como su motor tecnológico y refuerza sus atributos de innovación.",
    "Toda aplicación de la marca Paraná pasa por aprobación del Grupo [DATO A CONFIRMAR].",
  ], { fontSize: 12.5 }), { x: 6.83, y: 5.8, w: 6.0, h: 1.0, fontSize: 12.5 });
}

// =====================================================================
// 5. SERVICIOS DE MOVE 37 (C)
// =====================================================================
section("5. Servicios de Move 37");
{
  const s = newSlide("PAPEL", "05 · CATÁLOGO · BLOQUE C", "SIETE SERVICIOS, CUATRO MODALIDADES");
  table(s, ["SERVICIO", "QUÉ RESUELVE", "MODALIDAD", "SEGMENTO", "ORIGEN"], [
    ["Diagnóstico de oportunidades de IA", "Mapa de procesos automatizables y priorización por impacto.", "Proyecto cerrado", "A y B", "Método interno"],
    ["Desarrollo a medida", "Automatización de procesos, asistentes y análisis de documentos.", "Proyecto", "A y B", "Proyectos internos"],
    ["Productos para productores", "Cotización, gestión de cartera y seguimiento [ALCANCE A VALIDAR].", "Producto · suscripción", "Productores", "Herramientas internas [A CONFIRMAR]"],
    ["Soluciones para aseguradoras", "Siniestros, suscripción y atención.", "Proyecto + licencia", "Aseguradoras", "Herramientas internas [A CONFIRMAR]"],
    ["Prospector", "Captación de leads B2B (bloque E).", "Suscripción", "A y B", "Desarrollo Vértice + Move 37"],
    ["Staff part time de IA", "Capacidad de ingeniería y producto sin contratar un equipo.", "Abono mensual por horas", "A y B", "Equipo Move 37"],
    ["Mantenimiento y evolución", "Soporte, monitoreo y mejoras de lo entregado.", "Suscripción", "Clientes activos", "Equipo Move 37"],
  ], { x: M, y: 1.95, w: CW, colW: [2.6, 4.0, 2.0, 1.55, 2.18], fontSize: 11, boldFirst: true });
  T(s, "Justificación: arrancar con servicios que ya existen en forma interna baja el riesgo de entrega. Los productos empaquetados generan ingresos recurrentes y el staff part time capitaliza la capacidad ociosa [DATO A CONFIRMAR: capacidad disponible del equipo].", { x: M, y: 6.15, w: CW, h: 0.7, fontSize: 11.5, color: K.gris });
}
{
  const s = newSlide("PAPEL", "05 · PAQUETES Y PRICING", "TRES NIVELES Y UNA VÍA POR PROYECTO");
  const tiers = [
    ["ESENCIAL", "Productores y pymes", ["Un producto estándar", "Onboarding guiado", "Soporte por correo"], "Suscripción mensual por usuario"],
    ["PROFESIONAL", "Organizaciones medianas", ["Dos o tres productos o un desarrollo acotado", "Configuración a medida", "Soporte prioritario y reporte mensual"], "Suscripción + setup"],
    ["CORPORATIVO", "Aseguradoras y grandes empresas", ["Desarrollo a medida e integración", "Acuerdo de nivel de servicio", "Staff part time incluido"], "Proyecto + abono mensual"],
    ["PROYECTO", "Necesidad puntual", ["Diagnóstico o desarrollo cerrado", "Alcance y entregables fijos", "Garantía post entrega [A DEFINIR]"], "Precio por alcance"],
  ];
  const tw = (CW - 3 * 0.25) / 4;
  tiers.forEach((t, i) => {
    const x = M + i * (tw + 0.25), dark = i === 2;
    box(s, x, 1.95, tw, 3.85, dark ? K.carbon : K.blanco, "nivel-" + t[0].toLowerCase());
    T(s, t[0], { x: x + 0.22, y: 2.12, w: tw - 0.44, h: 0.5, fontSize: 24, bold: true, color: dark ? K.lima : K.negro, fontFace: "+mj-lt" });
    T(s, t[1], { x: x + 0.22, y: 2.65, w: tw - 0.44, h: 0.3, fontSize: 11.5, color: dark ? "ABABAB" : K.gris });
    T(s, bullets(t[2], { fontSize: 12, color: dark ? K.blanco : K.negro }), { x: x + 0.22, y: 3.05, w: tw - 0.44, h: 1.5, fontSize: 12 });
    T(s, t[3], { x: x + 0.22, y: 4.6, w: tw - 0.44, h: 0.4, fontSize: 11, bold: true, color: dark ? K.blanco : K.negro });
    T(s, "[MONTO A DEFINIR]", { x: x + 0.22, y: 5.1, w: tw - 0.44, h: 0.35, fontSize: 13, bold: true, color: dark ? K.lima : K.rojoT, flag: dark ? K.lima : K.rojoT });
  });
  kick(s, "CON QUÉ SE DEFINEN LOS PRECIOS", M, 6.05, 5);
  T(s, "Costo hora del equipo [DATO A CONFIRMAR] · referencias de competidores [DATO A CONFIRMAR] · valor generado para el cliente · margen objetivo del Grupo [DATO A CONFIRMAR].", { x: M, y: 6.33, w: CW, h: 0.5, fontSize: 12 });
}
{
  const s = newSlide("PAPEL", "05 · CASOS DE USO", "40 PROYECTOS COMO PRUEBA, SIN EXPONER NADA");
  const steps = ["Inventario de los más de 40 proyectos", "Clasificación por tipo, área y madurez", "Anonimización de datos y nombres", "Aprobación del Grupo", "Ficha de caso publicable"];
  const sw = (CW - 4 * 0.2) / 5;
  steps.forEach((st, i) => {
    const x = M + i * (sw + 0.2);
    box(s, x, 1.95, sw, 1.05, K.azul, "caso-paso-" + (i + 1));
    T(s, String(i + 1), { x: x + 0.18, y: 2.05, w: 0.5, h: 0.3, fontSize: 11, bold: true, color: K.lima });
    T(s, st, { x: x + 0.18, y: 2.35, w: sw - 0.36, h: 0.6, fontSize: 12, color: K.blanco });
  });
  // Plantilla de ficha
  box(s, M, 3.3, 7.2, 3.5, K.blanco, "ficha-caso");
  kick(s, "PLANTILLA DE FICHA DE CASO", M + 0.25, 3.45, 6.7);
  const fields = [["Problema", "[DATO A CONFIRMAR: qué proceso, qué dolor]"], ["Solución", "[DATO A CONFIRMAR: herramienta y enfoque de IA]"], ["Resultado medible", "[DATO A CONFIRMAR: indicador antes y después]"], ["Trasladable a", "Aseguradoras · productores · otras industrias"], ["Confidencialidad", "Nivel aprobado por el Grupo [DATO A CONFIRMAR]"]];
  fields.forEach((f, i) => {
    const y = 3.8 + i * 0.58;
    T(s, f[0], { x: M + 0.25, y, w: 1.9, h: 0.5, fontSize: 12, bold: true });
    T(s, f[1], { x: M + 2.2, y, w: 4.75, h: 0.5, fontSize: 12 });
  });
  const rx = 8.0, rw = W - M - rx;
  box(s, rx, 3.3, rw, 3.5, K.lima, "casos-regla");
  kick(s, "REGLA DE CONFIDENCIALIDAD", rx + 0.25, 3.45, rw - 0.5, K.negro);
  T(s, bullets([
    "No se publican datos de asegurados, montos ni sistemas internos.",
    "Cada caso muestra el problema y el tipo de resultado, no la información del Grupo.",
    "Ningún caso sale sin aprobación escrita del Grupo.",
  ], { fontSize: 12.5 }), { x: rx + 0.25, y: 3.8, w: rw - 0.5, h: 2.9, fontSize: 12.5 });
}

// =====================================================================
// 6. CAMPAÑA Y MARKETING (D)
// =====================================================================
section("6. Estrategia de campaña y marketing");
{
  const s = newSlide("PAPEL", "06 · ESTRATEGIA DE COMUNICACIÓN · BLOQUE D", "UN CONCEPTO, TRES MENSAJES");
  box(s, M, 1.95, CW, 1.1, K.rojo, "concepto-campana");
  T(s, "CONCEPTO: SIEMPRE HAY UNA JUGADA MEJOR", { x: M + 0.25, y: 2.05, w: CW - 0.5, h: 0.5, fontSize: 26, bold: true, color: K.blanco, fontFace: "+mj-lt" });
  T(s, "Todo problema de negocio tiene una solución que todavía nadie vio. Move 37 la encuentra con IA y la pone a funcionar.", { x: M + 0.25, y: 2.6, w: CW - 0.5, h: 0.4, fontSize: 13, color: K.negro });
  const seg = [
    ["ASEGURADORAS", "Tecnología hecha por gente que entiende el seguro.", "Soluciones probadas en la operación de un grupo asegurador, con la confidencialidad que tu negocio exige.", "Casos anonimizados, políticas de seguridad, independencia operativa."],
    ["PRODUCTORES", "Más tiempo para vender, menos para administrar.", "Herramientas de IA simples, pensadas para el día a día del productor.", "Demo de 15 minutos, precio accesible, soporte cercano."],
    ["OTRAS INDUSTRIAS", "La jugada que tu operación necesita.", "Un equipo que ya llevó la IA a más de 40 procesos reales, ahora para tu empresa.", "Método, velocidad, casos trasladables."],
  ];
  const sw = (CW - 2 * 0.3) / 3;
  seg.forEach((g, i) => {
    const x = M + i * (sw + 0.3);
    box(s, x, 3.25, sw, 3.6, K.blanco, "mensaje-" + (i + 1));
    kick(s, g[0], x + 0.22, 3.42, sw - 0.44);
    T(s, g[1], { x: x + 0.22, y: 3.75, w: sw - 0.44, h: 0.75, fontSize: 16, bold: true });
    T(s, g[2], { x: x + 0.22, y: 4.55, w: sw - 0.44, h: 1.0, fontSize: 12.5 });
    T(s, [{ text: "Pruebas: ", options: { bold: true } }, { text: g[3] }], { x: x + 0.22, y: 5.75, w: sw - 0.44, h: 0.95, fontSize: 11, color: K.gris });
  });
}
{
  const s = newSlide("PAPEL", "06 · PLAN DE 90 DÍAS", "PREPARAR, LANZAR, CONVERTIR");
  table(s, ["", "MES 1 · PREPARAR", "MES 2 · LANZAR", "MES 3 · CONVERTIR"], [
    ["Objetivo", "Marca lista y Grupo alineado", "Presencia y conversación", "Primeras reuniones comerciales"],
    ["LinkedIn (prioridad, a validar)", "Página de marca y perfiles de voceros. Teasers dos veces por semana [FRECUENCIA A VALIDAR].", "Post de lanzamiento y video manifiesto. Serie semanal \"Jugada 37\" con casos.", "Casos por segmento y campaña paga a públicos definidos [PRESUPUESTO A DEFINIR]."],
    ["Otros canales", "Comunicación interna del Grupo y landing de Move 37.", "Webinar de lanzamiento, prensa sectorial [A VALIDAR] y newsletter.", "Outreach con Prospector y encuentros con productores."],
    ["Piezas", "Manifiesto, landing, tres one-pagers por segmento, kit de vocería.", "Video de 60 s, carruseles de casos, presentación comercial.", "Fichas de caso, demo de Prospector, secuencias de outreach."],
    ["Hito", "Aprobación de marca y mensajes", "Lanzamiento público", "Primer reporte de pipeline"],
  ], { x: M, y: 1.95, w: CW, colW: [2.3, 3.344, 3.344, 3.345], fontSize: 12.5, boldFirst: true });
  T(s, "El plan arranca cuando la marca está aprobada (Fase 1). Las semanas exactas se fijan en el kickoff.", { x: M, y: 6.4, w: CW, h: 0.4, fontSize: 11.5, color: K.gris });
}
{
  const s = newSlide("PAPEL", "06 · PIEZAS Y MEDICIÓN", "QUÉ SALE PRIMERO Y CÓMO LO MEDIMOS");
  box(s, M, 1.95, 4.6, 4.9, K.azul, "piezas-iniciales");
  kick(s, "CAMPAÑA INICIAL", M + 0.25, 2.12, 4.1, K.lima);
  T(s, bullets([
    "Manifiesto de marca (texto y video de 60 s)",
    "Landing de Move 37",
    "Tres one-pagers: aseguradoras, productores y otras industrias",
    "Serie de carruseles \"Jugada 37\"",
    "Kit de vocería para el CEO del Grupo y el líder de Move 37 [A CONFIRMAR]",
    "Webinar de lanzamiento",
    "Presentación comercial",
  ], { fontSize: 13, color: K.blanco }, K.lima), { x: M + 0.25, y: 2.5, w: 4.1, h: 4.2, fontSize: 13, color: K.blanco });
  const rx = 5.4, rw = W - M - rx;
  table(s, ["KPI", "ETAPA", "META A 90 DÍAS"], [
    ["Impresiones y alcance en LinkedIn", "Conocimiento", "[META A DEFINIR]"],
    ["Tasa de interacción de los posts", "Conocimiento", "[META A DEFINIR]"],
    ["Seguidores con perfil objetivo", "Conocimiento", "[META A DEFINIR]"],
    ["Visitas a la landing", "Consideración", "[META A DEFINIR]"],
    ["Leads calificados (MQL)", "Consideración", "[META A DEFINIR]"],
    ["Tasa de respuesta del outreach", "Conversión", "[META A DEFINIR]"],
    ["Reuniones comerciales", "Conversión", "[META A DEFINIR]"],
    ["Pipeline generado", "Negocio", "[META A DEFINIR]"],
  ], { x: rx, y: 1.95, w: rw, colW: [3.6, 1.85, 1.98], fontSize: 11.5, boldFirst: true });
}

// =====================================================================
// 7. PROSPECTOR (E)
// =====================================================================
section("7. Prospector");
{
  const s = newSlide("PAPEL", "07 · PROSPECTOR · BLOQUE E", "CINCO ETAPAS, DE LA FUENTE A LA REUNIÓN");
  const st = [
    ["FUENTES", ["Bases B2B licenciadas", "Registros públicos de empresas", "Formularios y eventos propios", "Contactos existentes, solo con base legal"]],
    ["ENRIQUECIMIENTO", ["Rubro, tamaño y ubicación", "Cargo y área", "Señales: búsquedas laborales, noticias", "Validación de correos"]],
    ["SCORING", ["Ajuste al cliente ideal", "Señales de intención", "Interacción con contenidos", "Modelo explicable y umbral de MQL"]],
    ["SECUENCIAS", ["Correo y LinkedIn por segmento", "Borradores con IA y revisión humana", "Baja visible en cada mensaje", "Pase a ventas al responder"]],
    ["MEDICIÓN", ["Respuesta, reuniones y pipeline", "Calidad de datos por fuente", "Ajuste periódico del scoring", "Registro de bajas y pedidos"]],
  ];
  const sw = (CW - 4 * 0.22) / 5;
  st.forEach((e, i) => {
    const x = M + i * (sw + 0.22);
    box(s, x, 1.95, sw, 0.75, K.azul, "etapa-cab-" + (i + 1));
    T(s, String(i + 1).padStart(2, "0") + "  " + e[0], { x: x + 0.15, y: 2.03, w: sw - 0.3, h: 0.6, fontSize: 12, bold: true, color: K.blanco, valign: "middle" });
    box(s, x, 2.8, sw, 2.6, K.blanco, "etapa-cuerpo-" + (i + 1));
    T(s, bullets(e[1], { fontSize: 11.5 }), { x: x + 0.15, y: 2.95, w: sw - 0.3, h: 2.35, fontSize: 11.5 });
  });
  box(s, M, 5.65, (CW - 0.3) / 2, 1.2, K.carbon, "roles-move37");
  T(s, [{ text: "MOVE 37 CONSTRUYE  ", options: { bold: true, color: K.lima, charSpacing: 1.5, fontSize: 10, breakLine: true } }, { text: "Motor de datos, integraciones, modelo de scoring, automatización de secuencias y tablero de medición.", options: { color: K.blanco } }], { x: M + 0.2, y: 5.78, w: (CW - 0.3) / 2 - 0.4, h: 1.0, fontSize: 12 });
  const x2 = M + (CW - 0.3) / 2 + 0.3;
  box(s, x2, 5.65, (CW - 0.3) / 2, 1.2, K.lima, "roles-vertice");
  T(s, [{ text: "VÉRTICE APORTA  ", options: { bold: true, charSpacing: 1.5, fontSize: 10, breakLine: true } }, { text: "Perfil de cliente ideal, mensajes, contenidos de las secuencias, reglas de scoring comercial y operación del día a día.", options: {} }], { x: x2 + 0.2, y: 5.78, w: (CW - 0.3) / 2 - 0.4, h: 1.0, fontSize: 12 });
}
{
  const s = newSlide("PAPEL", "07 · CUMPLIMIENTO DE DATOS PERSONALES", "LEY 25.326 DESDE EL DISEÑO, NO AL FINAL");
  const req = [
    ["Licitud y finalidad", "Solo fuentes con legitimidad comprobable. El art. 27 admite tratar datos con fines publicitarios si provienen de fuentes accesibles al público, del propio titular o con su consentimiento."],
    ["Retiro y bloqueo", "Cada mensaje identifica al remitente y ofrece una baja simple. El pedido de retiro se ejecuta en un plazo definido [A DEFINIR]."],
    ["Minimización", "Solo datos profesionales necesarios para el contacto. Nunca datos sensibles."],
    ["Seguridad y confidencialidad", "Accesos por rol, cifrado, registro de actividad y política de retención y borrado."],
    ["Inscripción de la base", "Evaluar la inscripción ante la Agencia de Acceso a la Información Pública [A VALIDAR CON ASESORÍA LEGAL]."],
    ["Otros marcos", "Registro Nacional No Llame (Ley 26.951) si hay llamados. Respetar los términos de uso de cada plataforma: nada de extracción automatizada no permitida."],
  ];
  const cw = (CW - 0.3) / 2, ch = 1.38;
  req.forEach((r, i) => {
    const x = M + (i % 2) * (cw + 0.3), y = 1.95 + Math.floor(i / 2) * (ch + 0.15);
    box(s, x, y, cw, ch, K.blanco, "requisito-" + (i + 1));
    T(s, r[0], { x: x + 0.22, y: y + 0.13, w: cw - 0.44, h: 0.3, fontSize: 13, bold: true });
    T(s, r[1], { x: x + 0.22, y: y + 0.47, w: cw - 0.44, h: 0.85, fontSize: 11.5, color: K.gris });
  });
  box(s, M, 6.55, CW, 0.38, K.rojo, "aviso-legal");
  T(s, "Prospector no opera sin dictamen de asesoría legal. Los datos de asegurados del Grupo no se usan para prospección sin base legal específica.", { x: M + 0.2, y: 6.6, w: CW - 0.4, h: 0.3, fontSize: 11.5, color: K.negro, valign: "middle" });
}
{
  const s = newSlide("PAPEL", "07 · ESFUERZO Y COSTOS", "UN MVP EN CUATRO TRAMOS");
  table(s, ["TRAMO", "ALCANCE", "ESFUERZO ESTIMADO*", "COSTO"], [
    ["1 · Discovery y diseño", "Perfil de cliente ideal, fuentes, arquitectura y revisión legal.", "2 a 3 semanas", "[MONTO A DEFINIR]"],
    ["2 · MVP de datos", "Ingesta de fuentes, enriquecimiento y scoring básico.", "6 a 8 semanas", "[MONTO A DEFINIR]"],
    ["3 · Secuencias y CRM", "Outreach automatizado, revisión humana e integración con CRM.", "4 a 6 semanas", "[MONTO A DEFINIR]"],
    ["4 · Piloto y ajuste", "Operación real con un segmento, medición y ajustes.", "4 semanas", "[MONTO A DEFINIR]"],
  ], { x: M, y: 1.95, w: 8.3, colW: [2.0, 3.0, 1.5, 1.8], fontSize: 11.5, boldFirst: true });
  T(s, "* Estimación preliminar de Vértice. Supone un equipo de un líder técnico y dos desarrolladores de Move 37, más estrategia y contenidos de Vértice [DATO A CONFIRMAR]. Se valida al cierre del tramo 1. Los tramos 2 y 3 pueden solaparse.", { x: M, y: 5.25, w: 8.3, h: 0.9, fontSize: 11, color: K.gris });
  const rx = 9.1, rw = W - M - rx;
  box(s, rx, 1.95, rw, 4.9, K.carbon, "costos-recurrentes");
  kick(s, "COSTOS RECURRENTES", rx + 0.25, 2.12, rw - 0.5, K.lima);
  T(s, bullets([
    "Licencias de bases de datos B2B",
    "APIs de enriquecimiento y validación de correos",
    "Infraestructura en la nube",
    "Uso de modelos de IA",
    "Herramienta de envío y CRM",
    "Asesoría legal inicial y periódica",
  ], { fontSize: 12.5, color: K.blanco }), { x: rx + 0.25, y: 2.5, w: rw - 0.5, h: 3.2, fontSize: 12.5, color: K.blanco });
  T(s, "[MONTOS A DEFINIR SEGÚN PROVEEDORES]", { x: rx + 0.25, y: 6.1, w: rw - 0.5, h: 0.5, fontSize: 11, bold: true, color: K.lima, flag: K.lima });
}

// =====================================================================
// 8. PART TIME VÉRTICE (F)
// =====================================================================
section("8. Servicios part time de Vértice");
{
  const s = newSlide("PAPEL", "08 · DEDICACIÓN PART TIME · BLOQUE F", "CINCO ÁREAS, HORAS DEFINIDAS");
  table(s, ["ÁREA", "DEDICACIÓN PROPUESTA*", "ENTREGABLES MENSUALES", "PERFIL"], [
    ["Estrategia", "16 h/mes (2 días)", "Comité mensual, plan trimestral, reporte de KPIs y recomendaciones.", "Director/a de estrategia"],
    ["Marca", "24 h/mes en Fase 1 · 16 h/mes después", "Plataforma e identidad en Fase 1. Después, guardianía de marca y piezas clave.", "Director/a de arte y redactor/a"],
    ["Contenidos", "40 h/mes (5 días)", "Calendario mensual, posts de LinkedIn [CANTIDAD A VALIDAR], un caso, newsletter.", "Redactor/a y diseñador/a"],
    ["Performance", "16 h/mes (2 días)", "Campañas pagas en LinkedIn, optimización de la landing y reporte.", "Especialista en performance"],
    ["Prospector", "24 h/mes (3 días)", "Perfil de cliente ideal, mensajes, secuencias y revisión semanal de leads.", "Estratega de growth B2B"],
  ], { x: M, y: 1.95, w: CW, colW: [1.8, 2.9, 5.0, 2.633], fontSize: 12.5, boldFirst: true });
  T(s, "* Propuesta inicial de Vértice, ajustable tras el kickoff. Las horas se informan en el reporte mensual.", { x: M, y: 6.35, w: CW, h: 0.4, fontSize: 11.5, color: K.gris });
}
{
  const s = newSlide("PAPEL", "08 · PAQUETES Y CONDICIONES", "TRES PAQUETES PARA ACOMPAÑAR CADA FASE");
  table(s, ["PAQUETE", "ÁREAS INCLUIDAS", "HORAS/MES (SUMA POR ÁREA)", "PRECIO MENSUAL (EQUIPO COMERCIAL)"], [
    ["Despegue", "Estrategia · Marca · Contenidos (base, 24 h)", "64 h", "[MONTO A DEFINIR]"],
    ["Crecimiento", "Estrategia · Marca · Contenidos · Performance", "88 h", "[MONTO A DEFINIR]"],
    [{ text: "Integral (recomendado)", options: { bold: true } }, "Las cinco áreas, incluido Prospector", "112 h", "[MONTO A DEFINIR]"],
  ], { x: M, y: 1.95, w: CW, colW: [2.4, 4.6, 2.3, 3.033], fontSize: 12, boldFirst: true, hl: (r) => (r === 2 ? K.lima : null) });
  const cw = (CW - 0.3) / 2;
  box(s, M, 3.95, cw, 2.9, K.blanco, "condiciones");
  kick(s, "CONDICIONES", M + 0.25, 4.1, cw - 0.5);
  T(s, bullets([
    "Plazo mínimo de contratación [A DEFINIR].",
    "Facturación mensual. Moneda y mecanismo de ajuste [A DEFINIR].",
    "Horas no acumulables entre meses [A CONFIRMAR].",
    "Fuera de alcance: pauta, producción audiovisual y licencias de terceros.",
  ], { fontSize: 12 }), { x: M + 0.25, y: 4.42, w: cw - 0.5, h: 2.35, fontSize: 12 });
  const x2 = M + cw + 0.3;
  box(s, x2, 3.95, cw, 2.9, K.carbon, "supuestos-parttime");
  kick(s, "SUPUESTOS", x2 + 0.25, 4.1, cw - 0.5, K.lima);
  T(s, bullets([
    "Un interlocutor único por parte de Move 37.",
    "Aprobaciones del Grupo en un plazo acordado [A DEFINIR].",
    "Acceso a la información de proyectos necesaria para los casos.",
    "Integral se recomienda porque Prospector depende de la estrategia y los contenidos.",
  ], { fontSize: 12, color: K.blanco }, K.lima), { x: x2 + 0.25, y: 4.42, w: cw - 0.5, h: 2.35, fontSize: 12, color: K.blanco });
}

// =====================================================================
// 9. CRONOGRAMA
// =====================================================================
section("9. Cronograma general");
{
  const s = newSlide("PAPEL", "09 · CRONOGRAMA GENERAL", "DOCE MESES EN SEIS FASES");
  const lx = M, lw = 3.3, gx = M + lw + 0.1, gw = W - M - gx, mw = gw / 12;
  for (let m = 0; m < 12; m++) {
    T(s, "M" + (m + 1), { x: gx + m * mw, y: 1.95, w: mw, h: 0.25, fontSize: 9, color: K.gris, align: "center", charSpacing: 1 });
    if (m > 0) s.addShape(pres.shapes.LINE, { objectName: "gantt-guia-" + m, x: gx + m * mw, y: 2.25, w: 0, h: 4.05, line: { color: LINEA, width: 0.75 } });
  }
  const ph = [
    ["F0 · Validación y gobierno", 0, 1, "hub", "ENTENDER"],
    ["F1 · Marca y oferta", 0, 3, "lens", "TRANSFORMAR"],
    ["F2 · Lanzamiento (90 días)", 3, 6, "spark", "CONECTAR"],
    ["F3 · Prospector MVP y piloto", 3, 7, "lens", "TRANSFORMAR"],
    ["F4 · Ventas piloto, línea A", 5, 9, "spark", "CONECTAR"],
    ["F5 · Optimización y línea B", 8, 12, "aon", "IMPACTAR"],
  ];
  ph.forEach((p, i) => {
    const y = 2.35 + i * 0.66;
    T(s, p[0], { x: lx, y: y + 0.05, w: lw, h: 0.4, fontSize: 12.5, bold: true, valign: "middle" });
    const opt = { objectName: "gantt-barra-" + i, x: gx + p[1] * mw + 0.03, y, w: (p[2] - p[1]) * mw - 0.06, h: 0.5, fill: { color: CAPS[p[3]] }, rectRadius: 0.25, line: p[3] === "spark" ? { color: "000000", width: 0.75 } : { type: "none" } };
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, opt);
    const narrow = opt.w < 1.4;
    const lbl = { x: narrow ? opt.x + opt.w + 0.12 : opt.x + 0.15, y, w: narrow ? 1.6 : opt.w - 0.3, h: 0.5, fontSize: 10, bold: true, color: K.negro, valign: "middle", charSpacing: 1.5 };
    T(s, p[4], lbl);
  });
  T(s, "Fases según la metodología CoCreate de Vértice: Entender (Data/Discovery) · Transformar (Strategy/Creativity) · Conectar (Management/Content) · Impactar (Visualization/Optimization). Duraciones propuestas, no comprometidas: dependen de la aprobación del Grupo en F0, la disponibilidad del equipo de Move 37 y el dictamen legal sobre Prospector.", { x: M, y: 6.35, w: CW, h: 0.6, fontSize: 10.5, color: K.gris });
}

// =====================================================================
// 10. SUPUESTOS, RIESGOS Y PRÓXIMOS PASOS
// =====================================================================
section("10. Supuestos, riesgos y próximos pasos");
{
  const s = newSlide("PAPEL", "10 · RIESGOS", "LO QUE PUEDE SALIR MAL Y CÓMO LO EVITAMOS");
  table(s, ["RIESGO", "PROB.", "IMPACTO", "MITIGACIÓN"], [
    ["Conflicto entre la demanda interna del Grupo y la comercial", "Alta", "Alto", "Cupo de capacidad comercial acordado y gobierno de prioridades en F0."],
    ["Las aseguradoras no le compran a un proveedor de un grupo competidor", "Media", "Alto", "Marca independiente, políticas de confidencialidad y separación operativa demostrables."],
    ["El nombre Move 37 no resulta registrable", "Media", "Medio", "Búsqueda de anterioridades en F0 y alternativas de naming listas."],
    ["Prospector incumple la normativa de datos", "Baja con controles", "Alto", "Dictamen legal previo, baja en cada mensaje, fuentes auditadas."],
    ["Se publica información confidencial del Grupo", "Baja", "Alto", "Anonimización y aprobación escrita de cada caso."],
    ["Precios sin base de costos", "Media", "Medio", "Costeo con el CFO antes de publicar precios."],
    ["Bajo rendimiento de LinkedIn en algún segmento", "Media", "Medio", "Validación temprana y canales alternativos (eventos, cámaras, prensa sectorial)."],
  ], { x: M, y: 1.95, w: CW, colW: [4.2, 1.5, 1.1, 5.533], fontSize: 11, boldFirst: true });
}
{
  const s = newSlide("PAPEL", "10 · SUPUESTOS Y PRÓXIMOS PASOS", "QUÉ NECESITAMOS PARA ARRANCAR");
  box(s, M, 1.95, 5.2, 4.9, K.blanco, "supuestos");
  kick(s, "SUPUESTOS DE ESTA PROPUESTA", M + 0.25, 2.12, 4.7);
  T(s, bullets([
    "El Grupo aprueba explorar la comercialización de Move 37.",
    "Move 37 puede destinar capacidad a clientes externos [DATO A CONFIRMAR].",
    "Hay acceso al inventario de los más de 40 proyectos.",
    "Cifras de mercado, precios y metas se completan en F0.",
    "Toda aplicación de la marca Paraná requiere aprobación del Grupo.",
  ], { fontSize: 12.5 }), { x: M + 0.25, y: 2.45, w: 4.7, h: 4.3, fontSize: 12.5 });
  const steps = [
    ["Aprobación de la Fase 0", "Dirección del Grupo"],
    ["Taller de marca con las autoridades", "CEO y Director Comercial · Vértice"],
    ["Búsqueda de anterioridades del nombre", "Asesoría de marcas"],
    ["Inventario y clasificación de proyectos", "Move 37"],
    ["Dictamen legal sobre Prospector", "Asesoría legal"],
    ["Costeo y definición de precios", "CFO · equipo comercial de Vértice"],
  ];
  const rx = 6.0, rw = W - M - rx;
  kick(s, "PRÓXIMOS PASOS · RESPONSABLE SUGERIDO", rx, 1.95, rw);
  steps.forEach((p, i) => {
    const y = 2.3 + i * 0.75;
    s.addShape(pres.shapes.OVAL, { objectName: "paso-num-" + (i + 1), x: rx, y, w: 0.5, h: 0.5, fill: { color: K.rojo }, line: { type: "none" } });
    T(s, String(i + 1), { x: rx, y, w: 0.5, h: 0.5, fontSize: 14, bold: true, color: K.negro, align: "center", valign: "middle" });
    T(s, p[0], { x: rx + 0.7, y: y - 0.02, w: rw - 0.7, h: 0.3, fontSize: 13.5, bold: true });
    T(s, p[1], { x: rx + 0.7, y: y + 0.28, w: rw - 0.7, h: 0.3, fontSize: 11.5, color: K.gris });
  });
}

// =====================================================================
// ANEXO
// =====================================================================
section("Anexo");
{
  const s = newSlide("PAPEL", "ANEXO · DATOS A CONFIRMAR", "LISTA CONSOLIDADA PARA LA FASE 0");
  table(s, ["#", "DATO", "BLOQUE", "RESPONSABLE SUGERIDO"], [
    ["1", "Tamaño del mercado de aseguradoras y productores y su gasto en tecnología", "B", "Vértice (investigación) · fuente SSN"],
    ["2", "Gasto en soluciones de IA en otras industrias", "B", "Vértice (investigación)"],
    ["3", "Relevamiento de competidores por categoría", "B", "Vértice"],
    ["4", "Tamaño de la red de productores del Grupo", "B", "Dirección Comercial del Grupo"],
    ["5", "Disponibilidad registral y usos de \"Move 37\"", "A", "Asesoría de marcas"],
    ["6", "Aprobación del uso de la marca Paraná en la firma de respaldo", "A", "Dirección del Grupo"],
    ["7", "Inventario de proyectos, resultados y nivel de confidencialidad", "C", "Move 37"],
    ["8", "Capacidad disponible y costo hora del equipo de Move 37", "C · E", "Move 37 · CFO"],
    ["9", "Precios por nivel y paquetes part time", "C · F", "Equipo comercial de Vértice · CFO"],
    ["10", "Metas de KPIs y presupuesto de pauta", "D", "Vértice · Move 37"],
    ["11", "Dictamen sobre Ley 25.326, inscripción de la base y fuentes", "E", "Asesoría legal"],
  ], { x: M, y: 1.95, w: CW, colW: [0.5, 6.6, 1.1, 4.133], fontSize: 11 });
}

// =====================================================================
// CIERRE
// =====================================================================
section("Cierre");
{
  const s = pres.addSlide({ masterName: "ROJO", sectionTitle: curSection });
  s.addText("VÉRTICE  ·  PROPUESTA PARA MOVE 37", { placeholder: "kicker", charSpacing: 2 });
  T(s, "GRACIAS", { x: M, y: 1.7, w: CW, h: 2.4, fontSize: 150, bold: true, color: K.blanco, fontFace: "+mj-lt" });
  T(s, "Proponemos una reunión de trabajo para revisar esta propuesta y aprobar la Fase 0.", { x: M, y: 4.4, w: 8, h: 0.8, fontSize: 18, color: K.negro });
  outline(s, M, 5.5, 5.9, 0.95, K.negro, "caja-contacto");
  T(s, [{ text: "Contacto Vértice: ", options: { bold: true } }, { text: "[DATO A CONFIRMAR: nombre, correo y teléfono]" }], { x: M + 0.2, y: 5.62, w: 5.5, h: 0.7, fontSize: 12.5, color: K.negro, flag: K.negro });
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("OK", OUT);
})().catch((e) => { console.error(e); process.exit(1); });
