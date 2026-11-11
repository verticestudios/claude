#!/usr/bin/env python3
"""Genera las páginas del Vlog (blog/*.html) y las tarjetas del Vlog de la home (index.html).

Uso, desde la carpeta sitio-3d:  python3 blog/build.py
El contenido de las cuatro notas migradas está en blog/notes.json (texto de verticestudios.com).
Para sumar una nota: agregarla a NOTES (y a notes.json si es una nota de texto) y volver a correr el script.
"""
import json, re, html, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CAL = 'https://calendar.app.google/fQACh8Sen125STmX6'
IG = 'https://www.instagram.com/vertice.estudios/'
LI = 'https://www.linkedin.com/company/vertice-content-marketing/'
NJ = json.load(open(os.path.join(HERE, 'notes.json')))

# Orden de más nueva a más vieja. 'img' es la imagen de la tarjeta; 'cover' la de la portada de la nota.
NOTES = [
    dict(slug='highlights-octubre', date='Noviembre 2026', tag='Lanzamiento · Contenido', video=True, img='../video/highlights-adlatina', cover_alt='Highlights de Octubre para Adlatina y Marketers',
         title='Los highlights de Octubre para Adlatina y Marketers',
         desc='Lanzamos los highlights de Octubre para Adlatina y Marketers by Adlatina: lo más importante del mes para la industria, en video.'),
    dict(slug='effie-jurado-2026', src='effie-jurado-2026', date='Octubre 2026', tag='Reconocimiento · Industria', img='effie-jurado', cover='effie', cover_alt='Premios Effie Argentina'),
    dict(slug='dato', date='[Fecha]', tag='Dato', dato=True, img=None, cover_alt='',
         title='El dato que cambia cómo planificamos',
         desc='Una cifra con fuente y qué hacer con ella el lunes. Nota editorial, sin video.'),
    dict(slug='streaming-marcas', src='streaming-marcas', date='Agosto 2026', tag='Nuevos servicios · Producción', img='streaming', cover='streaming', cover_alt='Producción de streaming en vivo'),
    dict(slug='auren-plus', src='auren-plus', date='Junio 2026', tag='Producción · Branding', img='auren', cover='auren', cover_alt='Línea Auren+ de Laboratorios Ferrini'),
    dict(slug='ferrini-cuestion-de-piel', src='ferrini-cuestion-de-piel', date='Mayo 2026', tag='Creatividad · Campaña', img='ferrini', cover='ferrini', cover_alt='Sapolán Ferrini: es cuestión de piel'),
]
SHORT = {
    'effie-jurado-2026': 'Hernán Sampó integra el jurado de los Effie Argentina 2026',
    'streaming-marcas': 'Vértice lanza su servicio de streaming en vivo para marcas',
    'auren-plus': 'Vértice produce el lanzamiento visual de Auren+',
    'ferrini-cuestion-de-piel': '«Es cuestión de piel»: el concepto para Sapolán Ferrini',
}
for n in NOTES:
    if 'src' in n:
        d = NJ[n['src']]
        n['title'] = html.unescape(re.sub(r'<[^>]+>', '', d['title'])).replace('  ', ' ')
        n['desc'] = d['ogdesc']
        n['data'] = d
    n['href'] = n['slug'] + '.html'
    n['short'] = SHORT.get(n['slug'], n['title'])
    n['dshort'] = re.split(r'(?<=[.!?])\s', n['desc'])[0] if n['slug'] != 'highlights-octubre' else n['desc']

def img_url(n, up=''):
    return '%sassets/%s' % (up, ('blog/%s.jpg' % n['img']) if not n['img'].startswith('../') else n['img'][3:] + '.jpg')

SOC = ('<span class="soc"><a href="%s" target="_blank" rel="noopener" aria-label="Instagram de Vértice"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"></rect><circle cx="12" cy="12" r="4"></circle><circle cx="17.3" cy="6.7" r=".6"></circle></svg></a>'
       '<a href="%s" target="_blank" rel="noopener" aria-label="LinkedIn de Vértice"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="3"></rect><path d="M8 10.5V16M8 7.8v.01M12 16v-5.5M12 13a2.6 2.6 0 0 1 5.2 0V16"></path></svg></a></span>') % (IG, LI)

WA_URL = 'https://wa.me/5491123442635'
WA = ('<a class="btn btn-l wa" href="' + WA_URL + '" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3.5 20.5l1.3-4.3A8.5 8.5 0 1 1 8 19.2z"></path>'
      '<path d="M9 8.5c0 3.5 3 6.5 6.5 6.5l1-1.5-2-1-1 .8a4.5 4.5 0 0 1-2-2l.8-1-1-2z"></path></svg>WhatsApp</a>')

CSS = r'''
:root{--rojo:#f10a09;--rojo-texto:#c60807;--negro:#000;--carbon:#131313;--blanco:#fff;--papel:#f2f2f0;--lima:#d7fe51;--gris-texto:#4a4a4a;--gris-claro:#ababab;--linea:#e0e0dc;
--display:"Tusker Grotesk","Bebas Neue","Arial Narrow",sans-serif;--ext:"Nimbus Sans Extended","Helvetica Neue",Arial,sans-serif;--body:"Helvetica Neue",Helvetica,Arial,sans-serif;
--gl:max(clamp(16px,5.5vw,80px),env(safe-area-inset-left,0px));--gr:max(clamp(16px,5.5vw,80px),env(safe-area-inset-right,0px));--ease:cubic-bezier(.2,.7,.2,1);color-scheme:light}
@font-face{font-family:"Tusker Grotesk";src:url("../assets/fonts/TuskerGrotesk-6600Semibold.ttf") format("truetype");font-weight:600;font-display:swap}
@font-face{font-family:"Tusker Grotesk";src:url("../assets/fonts/TuskerGrotesk-4500Medium.ttf") format("truetype");font-weight:500;font-display:swap}
@font-face{font-family:"Nimbus Sans Extended";src:url("../assets/fonts/NimbusSansExtendedD.otf") format("opentype");font-weight:400;font-display:swap}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--papel);color:#111;font-family:var(--body);font-size:16px;line-height:1.5;overflow-x:hidden}
a{color:inherit}h1,h2,h3,p,ul,dl,dd,figure{margin:0}ul{padding:0;list-style:none}
:focus-visible{outline:2px solid var(--negro);outline-offset:3px}.dk :focus-visible,.nav :focus-visible{outline-color:var(--lima)}
.tg{font-family:var(--display);font-weight:600;text-transform:uppercase;line-height:.92;text-wrap:balance}
.tm{font-family:var(--display);font-weight:500;text-transform:uppercase;line-height:1}
.nx{font-family:var(--ext);text-transform:uppercase;letter-spacing:.16em;font-size:12px;line-height:1.5}
.wrap{padding-left:var(--gl);padding-right:var(--gr);max-width:1400px;margin-inline:auto}
.rule{display:block;height:4px;background:linear-gradient(currentColor,currentColor) left center/12px 4px no-repeat,linear-gradient(currentColor,currentColor) right center/12px 4px no-repeat,linear-gradient(currentColor,currentColor) center/100% 1px no-repeat}
.btn{display:inline-flex;align-items:center;gap:12px;min-height:48px;padding:0 24px;border-radius:999px;font-family:var(--ext);text-transform:uppercase;letter-spacing:.16em;font-size:12px;text-decoration:none;white-space:nowrap;transition:background .35s var(--ease),color .35s var(--ease)}
.btn i{font-style:normal;transition:transform .35s var(--ease)}.btn:hover i{transform:translateX(5px)}
.btn-l{background:var(--lima);color:var(--negro)}.btn-l:hover{background:var(--blanco)}
.btn-k{background:var(--negro);color:var(--blanco)}.btn-k:hover{background:var(--blanco);color:var(--negro)}
.nav{position:fixed;z-index:20;top:calc(14px + env(safe-area-inset-top,0px));left:var(--gl);right:var(--gr);display:flex;align-items:center;gap:20px;height:56px;padding:0 8px 0 22px;background:var(--negro);color:var(--blanco);border-radius:999px;box-shadow:0 0 0 1px rgba(255,255,255,.14);max-width:1240px;margin-inline:auto}
.nav img{height:22px;width:auto;display:block}.nav .back{margin-left:auto;font-family:var(--ext);text-transform:uppercase;letter-spacing:.16em;font-size:11px;text-decoration:none;padding:12px 0}.nav .back:hover{color:var(--lima)}
.nav .btn{min-height:40px;padding:0 18px;font-size:11px}
.soc{display:flex;gap:6px}.soc a{width:36px;height:36px;border-radius:999px;display:grid;place-items:center;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.35);transition:background .3s var(--ease),color .3s var(--ease),box-shadow .3s var(--ease)}
.soc a:hover{background:var(--lima);color:var(--negro);box-shadow:none}.soc svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}.soc circle[r=".6"]{fill:currentColor}
@media (max-width:640px){.nav{gap:10px;padding-left:16px}.nav .soc,.nav .back .x{display:none}.nav .back{white-space:nowrap}}
.hero{background:var(--rojo);color:var(--negro);padding-block:clamp(120px,14vw,190px) clamp(80px,9vw,130px)}
.hero .nx.k{margin-bottom:22px;display:flex;flex-direction:column;gap:12px;max-width:640px}
.hero h1{color:var(--blanco);font-size:clamp(40px,7vw,120px);max-width:15em}
.hero .sub{margin-top:26px;font-size:clamp(17px,1.6vw,22px);font-weight:500;max-width:28em;line-height:1.35}
.paper{padding-bottom:clamp(64px,8vw,120px)}
.cover{position:relative;overflow:hidden;aspect-ratio:16/9;background:var(--negro);border-radius:8px;margin-top:calc(-1 * clamp(56px,7vw,100px));box-shadow:0 30px 80px -30px rgba(0,0,0,.5);max-width:100%}
.cover::before{content:"";position:absolute;inset:-30px;background:var(--img) center/cover;filter:blur(30px) saturate(1.15)}
.cover img{position:relative;display:block;width:100%;height:100%;object-fit:contain}
.meta{display:flex;flex-wrap:wrap;gap:18px 56px;padding:26px 0;border-bottom:1px solid var(--negro)}
.meta div{display:flex;flex-direction:column;gap:6px;min-width:0}.meta dt{font-family:var(--ext);text-transform:uppercase;letter-spacing:.16em;font-size:10px;color:var(--rojo-texto)}
.meta dd{font-family:var(--display);font-weight:500;text-transform:uppercase;font-size:24px;line-height:1}
.col{max-width:740px;margin-top:clamp(36px,5vw,64px)}
.lead{font-size:clamp(20px,2vw,26px);line-height:1.4;font-weight:500;color:#111}
.col h2{font-family:var(--display);font-weight:600;text-transform:uppercase;color:var(--rojo-texto);font-size:clamp(34px,4vw,52px);line-height:.98;margin:clamp(40px,5vw,64px) 0 16px;text-wrap:balance}
.col p{font-size:18px;line-height:1.65;color:#222;margin-top:16px}.col .lead{margin-top:0}
.col strong{color:#000}
.col ul{display:flex;flex-direction:column;gap:10px;margin-top:20px}.col li{padding-left:26px;position:relative;font-size:18px;line-height:1.55;color:#222}
.col li::before{content:"";position:absolute;left:0;top:.6em;width:10px;height:10px;border-radius:50%;background:var(--rojo)}
.col .concept{font-family:var(--display);font-weight:600;text-transform:uppercase;color:var(--rojo);font-size:clamp(56px,8vw,120px);line-height:.9;margin:clamp(8px,2vw,24px) 0 0;text-wrap:balance}
.col .portrait{margin-top:28px;max-width:360px;border-radius:8px;overflow:hidden}.col .portrait img{display:block;width:100%;height:auto}
.cta{margin-top:clamp(56px,7vw,96px);background:var(--rojo);border-radius:8px;padding:clamp(28px,4vw,56px);display:flex;flex-direction:column;gap:18px;align-items:flex-start}
.cta h3{font-family:var(--display);font-weight:600;text-transform:uppercase;color:var(--blanco);font-size:clamp(34px,4.6vw,68px);line-height:.95;max-width:16em;text-wrap:balance}
.cta p{font-size:18px;line-height:1.5;max-width:34em;font-weight:500}
.more-h{margin-top:clamp(56px,7vw,96px);display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap}
.more-h h2{font-family:var(--display);font-weight:600;text-transform:uppercase;color:var(--rojo-texto);font-size:clamp(40px,5vw,72px);line-height:.95}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(300px,100%),1fr));gap:clamp(20px,2.4vw,36px);margin-top:28px}
.card{position:relative;display:flex;flex-direction:column;gap:12px;min-width:0}
.card .m{position:relative;aspect-ratio:4/3;border-radius:8px;overflow:hidden;background:var(--negro)}.card .m img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .6s var(--ease)}
.card:hover .m img{transform:scale(1.04)}
.card .tag{position:absolute;left:12px;top:12px;background:var(--negro);color:var(--blanco);padding:6px 10px;border-radius:6px;font-size:10px}
.card .k{color:var(--rojo-texto);font-size:10px}
.card h3{font-family:var(--display);font-weight:600;text-transform:uppercase;line-height:.98;font-size:clamp(26px,2.3vw,34px);text-wrap:balance}
.card p{color:var(--gris-texto);font-size:15px;line-height:1.5}
.card a{position:static;text-decoration:none}.card a::after{content:"";position:absolute;inset:0}
.card .go{font-family:var(--ext);text-transform:uppercase;letter-spacing:.16em;font-size:11px;margin-top:auto;padding-top:4px}
.card:hover .go{color:var(--rojo-texto)}
.vids{display:grid;grid-template-columns:minmax(0,1.9fr) minmax(0,.8fr);gap:clamp(16px,2.4vw,32px);align-items:start;margin-top:clamp(36px,5vw,64px)}
.vid{display:flex;flex-direction:column;gap:12px;min-width:0}.vid video{display:block;width:100%;background:#000;border-radius:8px}
.vid .h{aspect-ratio:16/9;object-fit:cover}.vid .v{aspect-ratio:9/16;object-fit:cover}.vid .nx{color:var(--rojo-texto);font-size:10px}
@media (max-width:760px){.vids{grid-template-columns:1fr}.vid .v{max-width:340px}}
footer{background:var(--negro);color:var(--blanco);padding-block:26px calc(26px + env(safe-area-inset-bottom,0px))}
footer .wrap{display:flex;flex-wrap:wrap;gap:14px 32px;justify-content:space-between;align-items:center}footer img{height:20px;width:auto;display:block}footer p{font-size:10px;color:var(--gris-claro)}
.wa{min-height:40px;padding:0 18px;font-size:11px;gap:10px}.wa svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.card .m.fig{display:grid;place-items:center;background:var(--negro)}
.card .m.fig b{font-family:var(--display);font-weight:600;font-size:clamp(84px,9vw,140px);line-height:.86;color:var(--rojo)}
.col .fig{font-family:var(--display);font-weight:600;font-size:clamp(100px,16vw,220px);line-height:.86;color:var(--rojo);margin-top:clamp(8px,2vw,24px)}
.mod{margin-top:clamp(40px,5vw,72px);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,340px);gap:clamp(20px,3vw,48px);align-items:center;background:var(--negro);color:var(--blanco);border-radius:8px;padding:clamp(24px,3vw,44px)}
.mod h2{font-family:var(--display);font-weight:600;text-transform:uppercase;color:var(--blanco);font-size:clamp(34px,4vw,56px);line-height:.98;margin:0 0 14px;text-wrap:balance}
.mod p{color:var(--gris-claro);font-size:17px;line-height:1.6;margin:0}.mod .nx{color:var(--lima);font-size:10px;margin-bottom:14px;display:block}
.mod video{display:block;width:100%;aspect-ratio:9/16;object-fit:cover;background:#000;border-radius:8px}
@media (max-width:760px){.mod{grid-template-columns:1fr}.mod video{max-width:340px}}
.src{margin-top:28px;font-size:14px;color:var(--gris-texto)}.src a{text-underline-offset:3px}
.single{display:block;margin-top:clamp(36px,5vw,64px)}.single video{display:block;width:100%;aspect-ratio:16/9;background:#000;border-radius:8px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.card .m img{transition:none}}
'''

def page(title, desc, body, extra_css=''):
    return ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n<style>%s%s</style>\n</head>\n<body>\n%s\n</body>\n</html>\n') % (
        html.escape(title), html.escape(desc, quote=True), CSS, extra_css, body)

NAV = ('<header class="nav"><a href="../index.html" aria-label="Vértice, inicio"><img src="../assets/img/logo-blanco.png" alt="Vértice"></a>'
       '<a class="back" href="index.html">← <span class="x">Todas las </span>notas</a>' + SOC + '<a class="btn btn-l" href="' + CAL + '" target="_blank" rel="noopener">Hablemos <i>→</i></a></header>')
FOOT = ('<footer class="dk"><div class="wrap"><a href="../index.html" aria-label="Vértice, inicio"><img src="../assets/img/logo-blanco.png" alt="Vértice"></a>' + SOC + WA +
        '<p class="nx">Strategy that inspires. Creativity that performs.</p><p class="nx">© 2026 Vértice Content Marketing Studio</p></div></footer>')

def card(n):
    if n.get('dato'):
        return ('<article class="card"><div class="m fig"><b>[00]%%</b></div><span class="nx k">%s · %s</span><h3><a href="%s">%s</a></h3><p>%s</p><span class="go">Leer la nota →</span></article>') % (
            html.escape(n['tag']), n['date'], n['href'], html.escape(n['title']), html.escape(n['desc']))
    tag = '<span class="nx tag">Video</span>' if n.get('video') else ''
    return ('<article class="card"><div class="m"><img src="%s" alt="" loading="lazy"%s>%s</div><span class="nx k">%s · %s</span><h3><a href="%s">%s</a></h3><p>%s</p><span class="go">%s →</span></article>') % (
        img_url(n, '../'), ' style="object-position:50%% 35%%"' if n['slug'].startswith('ferrini') else '', tag, html.escape(n['tag']), n['date'], n['href'], html.escape(n['short']), html.escape(n['dshort']),
        'Ver episodio' if n.get('video') else 'Leer la nota')

def related(cur):
    others = [n for n in NOTES if n['slug'] != cur['slug'] and not n.get('dato')][:3]
    return '<div class="more-h"><h2>Más notas</h2><a class="btn btn-k" href="index.html">Todas las notas <i>→</i></a></div><div class="cards">%s</div>' % ''.join(card(n) for n in others)

def cta_box(h3, p, btn):
    return '<aside class="cta"><h3>%s</h3><p>%s</p><a class="btn btn-k" href="%s" target="_blank" rel="noopener">%s</a></aside>' % (html.escape(h3), html.escape(p), CAL, html.escape(btn))

def hero(tag, title, sub=''):
    return '<section class="hero"><div class="wrap"><p class="nx k"><span class="rule"></span>%s</p><h1 class="tg">%s</h1>%s</div></section>' % (html.escape(tag), title, ('<p class="sub">%s</p>' % html.escape(sub)) if sub else '')

def cover(n):
    u = 'assets/blog/%s.jpg' % n['cover'] if 'cover' in n else 'assets/video/highlights-adlatina.jpg'
    return '<figure class="cover" style="--img:url(../%s)"><img src="../%s" alt="%s"></figure>' % (u, u, html.escape(n['cover_alt']))

def meta(items):
    return '<dl class="meta">%s</dl>' % ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (html.escape(k), html.escape(v)) for k, v in items)

def note_page(n):
    d = n['data']
    parts = []
    for b in d['body']:
        if b['tag'] == 'h2': parts.append('<h2>%s</h2>' % b['html'])
        elif b['tag'] == 'p': parts.append('<p>%s</p>' % b['html'])
        elif b['tag'] == 'ul': parts.append('<ul>%s</ul>' % b['html'].strip())
        elif b['cls'] == 'art-concept': parts.append('<p class="concept">%s</p>' % b['html'])
        elif b['tag'] == 'img': parts.append('<figure class="portrait"><img src="../assets/blog/effie-jurado.jpg" alt="Hernán Sampó, jurado de los Effie Awards Argentina 2026"></figure>')
    body = (NAV + '<main>' + hero(d['badge'], d['title']) + '<section class="paper"><div class="wrap">' + cover(n) + meta(d['meta']) +
            '<div class="col"><p class="lead">%s</p>%s</div>' % (d['lead'], ''.join(parts)) +
            cta_box(d['cta']['h3'], d['cta']['p'], 'Hablemos →') + related(n) + '</div></section></main>' + FOOT)
    return page(n['title'] + ' | Vértice', n['desc'], body)

def highlights_page(n):
    body = (NAV + '<main>' + hero('Lanzamiento · Contenido', 'Los highlights de Octubre para <br>Adlatina y Marketers', 'Lanzamos los highlights de Octubre para Adlatina y Marketers by Adlatina.') +
            '<section class="paper"><div class="wrap">'
            '<figure class="single" style="margin-top:calc(-1 * clamp(56px,7vw,100px))"><video controls playsinline preload="metadata" poster="../assets/video/highlights-adlatina.jpg" src="../assets/video/highlights-adlatina.mp4" aria-label="Highlights de Octubre, Adlatina"></video></figure>' +
            meta([('Publicado', n['date']), ('Medios', 'Adlatina · Marketers by Adlatina'), ('Formato', 'Video, episodio mensual')]) +
            '<div class="col"><p class="lead">Lanzamos los highlights de Octubre para Adlatina y Marketers by Adlatina: dos episodios que reúnen en video lo más importante del mes para la industria publicitaria y del marketing. Es el episodio más largo desde que el formato nació, en agosto, porque octubre estuvo plagado de novedades.</p>'
            '<h2>Un mes cargado de novedades</h2>'
            '<p>Del lado de Adlatina, el episodio reúne <strong>la despedida de Messi y la polémica de Sancor Seguros que derivó de ella</strong>, la ceremonia de Effie Latam, que entregó los galardones a los ganadores en la última semana de octubre en Cartagena de Indias, y el lanzamiento de nuevas agencias como Flint Latam y Lip 156.</p>'
            '<h2>Dos miradas, dos episodios</h2>'
            '<p>Cada medio cuenta su mes. Martina Caraboni comparte los highlights de Adlatina y Martina Varela los de Marketers by Adlatina, que destaca <strong>a los latinos presentes en el top 10 de CMO de Cannes Lions</strong>, el anuncio de las Leading Women Ecuador y la derrota de Amazon frente a Alibaba como el anunciante más grande en el Index Report, entre otras novedades.</p>'
            '<h2>Dónde verlo</h2>'
            '<p>Ambos episodios están disponibles en todas las redes sociales de Adlatina y de Marketers, y también en Adlatina TV.</p>'
            '<p class="src">Fuente: <a href="https://www.adlatina.com/publicidad/llegan-los-highlights-de-octubre" target="_blank" rel="noopener">Adlatina, «Llegan los highlights de octubre»</a>, 4 de noviembre de 2026.</p></div>'
            '<section class="mod" aria-label="Episodio de Marketers en vertical"><div><span class="nx">Episodio vertical · 9:16</span><h2>Marketers by Adlatina, en vertical</h2><p>El mismo mes, contado para la pantalla del celular. Mirá el episodio de Marketers en formato vertical.</p></div>'
            '<video controls playsinline preload="metadata" poster="../assets/video/highlights-marketers.jpg" src="../assets/video/highlights-marketers.mp4" aria-label="Marketers by Adlatina, vertical"></video></section>' +
            cta_box('¿Querés un contenido así para tu marca?', 'Contanos qué querés mover y armamos el recorrido juntos.', 'Hablemos →') + related(n) + '</div></section></main>' + FOOT)
    return page(n['title'] + ' | Vértice', n['desc'], body)

def reel_page():
    body = (NAV.replace('<a class="back" href="index.html">← <span class="x">Todas las </span>notas</a>', '<a class="back" href="../index.html">← <span class="x">Volver al </span>sitio</a>') + '<main>' +
            hero('Reel de agencia', 'Reel 26', 'Strategy that inspires. Creativity that performs.') +
            '<section class="paper"><div class="wrap"><figure class="single" style="margin-top:calc(-1 * clamp(56px,7vw,100px))"><video id="reel" controls playsinline preload="auto" poster="../assets/video/reel.jpg" src="../assets/video/reel.mp4" aria-label="Reel de Vértice"></video></figure>' +
            cta_box('¿Hablamos?', 'Contanos qué necesita tu marca y armamos el recorrido juntos.', 'Hablemos →') + '</div></section></main>' + FOOT +
            '<script>(function(){var v=document.getElementById("reel");if(!v)return;try{var p=v.play();if(p&&p.catch)p.catch(function(){})}catch(e){}})();</script>')
    return page('Reel 26 | Vértice', 'Reel de Vértice Content Marketing Studio.', body)

def dato_page(n):
    body = (NAV + '<main>' + hero('Dato · [Fecha]', 'El dato que cambia <br>cómo planificamos') + '<section class="paper"><div class="wrap">' +
            '<div class="col" style="margin-top:0"><p class="fig">[00]%</p><p class="lead">[Una cifra con fuente y qué hacer con ella el lunes.]</p>'
            '<h2>[Qué dice el dato]</h2><p>[Texto editorial de la nota: de dónde sale la cifra, qué significa para las marcas y cómo cambia la forma de planificar. Dos o tres párrafos.]</p>'
            '<h2>[Qué hacer el lunes]</h2><p>[Una recomendación concreta y accionable.]</p><p class="src">Fuente: [Fuente de la cifra]</p></div>' +
            cta_box('¿Querés que tu estrategia de contenidos dé resultados medibles?', 'Contanos qué querés mover y armamos el recorrido juntos.', 'Hablemos →') + related(n) + '</div></section></main>' + FOOT)
    return page(n['title'] + ' | Vértice', n['desc'], body)

def index_page():
    body = (NAV.replace('<a class="back" href="index.html">← <span class="x">Todas las </span>notas</a>', '<a class="back" href="../index.html#vlog">← <span class="x">Volver al </span>sitio</a>') + '<main>' +
            hero('Noticias de Vértice', 'Vlog', 'Clientes nuevos, premios, festivales, research y datos. Un episodio por novedad, contado por el equipo, y la nota para leerla con calma.') +
            '<section class="paper"><div class="wrap"><div class="cards" style="margin-top:clamp(40px,5vw,64px)">%s</div></div></section></main>' % ''.join(card(n) for n in NOTES) + FOOT)
    return page('Vlog | Vértice', 'Noticias de Vértice Content Marketing Studio.', body)

def home_cards():
    def media_img(n, aspect_cls=''):
        return '<img src="%s" alt="%s" loading="lazy"%s>' % (img_url(n), html.escape(n['cover_alt']), ' style="object-position:50% 35%"' if n['slug'].startswith('ferrini') else '')
    h = {n['slug']: n for n in NOTES}
    a = h['highlights-octubre']
    out = ['<article class="nw nw-a"><div class="media"><video src="assets/video/vlog-festival.mp4" poster="assets/video/vlog-festival.jpg" muted loop playsinline preload="none" data-auto aria-label="Adlatina Highlights, adelanto"></video><span class="nx tag"><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 1.5l7 4.5-7 4.5z"></path></svg>Video · Episodio</span></div>'
           '<span class="nx meta">%s · %s</span><h3>%s</h3><p>%s</p><a class="more" href="blog/%s">Ver episodio →</a></article>' % (a['tag'], a['date'], html.escape(a['title']), html.escape(a['desc']), a['href'])]
    e = h['effie-jurado-2026']
    out.append('<article class="nw nw-b"><div class="media">%s<span class="nx tag">Nota · Foto</span></div><span class="nx meta">%s · %s</span><h3>%s</h3><p>%s</p><a class="more" href="blog/%s">Leer la nota →</a></article>' % (media_img(e), e['tag'], e['date'], html.escape(e['short']), html.escape(e['dshort']), e['href']))
    d = h['dato']
    out.append('<article class="nw nw-s nw-c"><span class="nx meta">%s · %s</span><p class="fig">[00]%%</p><h3>%s</h3><p>%s</p><a class="more" href="blog/%s">Leer la nota →</a></article>' % (d['tag'], d['date'], html.escape(d['title']), html.escape(d['desc']), d['href']))
    for s_ in ['streaming-marcas', 'auren-plus', 'ferrini-cuestion-de-piel']:
        n = h[s_]
        out.append('<article class="nw nw-s"><div class="media">%s<span class="nx tag">Nota</span></div><span class="nx meta">%s · %s</span><h3>%s</h3><p>%s</p><a class="more" href="blog/%s">Leer la nota →</a></article>' % (media_img(n), n['tag'], n['date'], html.escape(n['short']), html.escape(n['dshort']), n['href']))
    return '\n      '.join(out)

if __name__ == '__main__':
    for n in NOTES:
        open(os.path.join(HERE, n['href']), 'w').write(highlights_page(n) if n.get('video') else dato_page(n) if n.get('dato') else note_page(n))
    open(os.path.join(HERE, 'reel.html'), 'w').write(reel_page())
    open(os.path.join(HERE, 'index.html'), 'w').write(index_page())
    p = os.path.join(ROOT, 'index.html'); s = open(p).read()
    s = re.sub(r'<!--VLOG-->.*?<!--/VLOG-->', lambda m: '<!--VLOG-->\n      ' + home_cards() + '\n      <!--/VLOG-->', s, flags=re.S)
    open(p, 'w').write(s)
    print('ok', len(NOTES), 'notas')
