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
BASE = 'https://verticestudios.com'
SITE_NAME = 'Vértice Content Marketing Studio'
DATES = {'effie-jurado-2026': '2026-10-01', 'highlights-octubre': '2026-11-11', 'streaming-marcas': '2026-08-05', 'auren-plus': '2026-06-01', 'ferrini-cuestion-de-piel': '2026-05-01', 'dato': '2026-11-11'}
OG_IMG = {'effie-jurado-2026': 'blog-effie.jpg', 'streaming-marcas': 'blog-streaming.jpg', 'auren-plus': 'blog-auren.jpg', 'ferrini-cuestion-de-piel': 'blog-ferrini.jpg',
          'highlights-octubre': 'assets/video/highlights-adlatina.jpg', 'dato': 'og-home.jpg'}
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

def page(title, desc, body, extra_css='', head=''):
    return ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>%s</title>\n<link rel="icon" href="../favicon.ico" sizes="any">\n<link rel="icon" type="image/png" sizes="32x32" href="../favicon-32.png">\n<link rel="apple-touch-icon" href="../apple-touch-icon.png">\n<meta name="description" content="%s">\n%s<style>%s%s</style>\n</head>\n<body>\n%s\n</body>\n</html>\n') % (
        html.escape(title), html.escape(desc, quote=True), head, CSS, extra_css, body)

NAV = ('<header class="nav"><a href="../index.html" aria-label="Vértice, inicio"><img src="../assets/img/logo-blanco.png" alt="Vértice"></a>'
       '<a class="back" href="index.html">← <span class="x">Todas las </span>notas</a>' + SOC + '<a class="btn btn-l" href="' + CAL + '" target="_blank" rel="noopener">Hablemos <i>→</i></a></header>')
FOOT = ('<footer class="dk"><div class="wrap"><a href="../index.html" aria-label="Vértice, inicio"><img src="../assets/img/logo-blanco.png" alt="Vértice"></a>' + SOC + WA +
        '<p class="nx">Strategy that inspires. Creativity that performs.</p><p class="nx">© 2026 Vértice Content Marketing Studio</p></div></footer>')

def seo(path, title, desc, image, typ='article', ld=None, noindex=False):
    url = BASE + path
    q = lambda t: html.escape(t, quote=True)
    out = ['<link rel="canonical" href="%s">' % url]
    if noindex: out.append('<meta name="robots" content="noindex, follow">')
    out += ['<meta name="theme-color" content="#f10a09">',
            '<meta property="og:type" content="%s">' % typ, '<meta property="og:site_name" content="%s">' % SITE_NAME, '<meta property="og:locale" content="es_AR">',
            '<meta property="og:title" content="%s">' % q(title), '<meta property="og:description" content="%s">' % q(desc), '<meta property="og:url" content="%s">' % url,
            '<meta property="og:image" content="%s/%s">' % (BASE, image),
            '<meta name="twitter:card" content="summary_large_image">', '<meta name="twitter:title" content="%s">' % q(title), '<meta name="twitter:description" content="%s">' % q(desc), '<meta name="twitter:image" content="%s/%s">' % (BASE, image)]
    if ld: out.append('<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False))
    return '\n'.join(out) + '\n'

def note_head(n):
    path = '/blog/%s.html' % n['slug']; img = OG_IMG[n['slug']]
    ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': n['title'], 'description': n['desc'], 'datePublished': DATES[n['slug']], 'dateModified': DATES[n['slug']],
          'url': BASE + path, 'mainEntityOfPage': BASE + path, 'image': '%s/%s' % (BASE, img), 'inLanguage': 'es-AR',
          'author': {'@type': 'Person', 'name': 'Hernán Sampó', 'url': BASE + '/'},
          'publisher': {'@type': 'Organization', 'name': SITE_NAME, 'url': BASE, 'logo': {'@type': 'ImageObject', 'url': BASE + '/logo-rojo.png'}}}
    return seo(path, n['title'] + ' | Vértice', n['desc'], img, 'article', ld, noindex=bool(n.get('dato')))

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
    return page(n['title'] + ' | Vértice', n['desc'], body, head=note_head(n))

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
    return page(n['title'] + ' | Vértice', n['desc'], body, head=note_head(n))

def reel_page():
    body = (NAV.replace('<a class="back" href="index.html">← <span class="x">Todas las </span>notas</a>', '<a class="back" href="../index.html">← <span class="x">Volver al </span>sitio</a>') + '<main>' +
            hero('Reel de agencia', 'Vertice Studios', 'Strategy that inspires. Creativity that performs.') +
            '<section class="paper"><div class="wrap"><figure class="single" style="margin-top:calc(-1 * clamp(56px,7vw,100px))"><video id="reel" controls playsinline preload="auto" poster="../assets/video/reel.jpg" src="../assets/video/reel.mp4" aria-label="Reel de Vértice"></video></figure>' +
            cta_box('¿Hablamos?', 'Contanos qué necesita tu marca y armamos el recorrido juntos.', 'Hablemos →') + '</div></section></main>' + FOOT +
            '<script>(function(){var v=document.getElementById("reel");if(!v)return;try{var p=v.play();if(p&&p.catch)p.catch(function(){})}catch(e){}})();</script>')
    d = 'Reel de Vértice Content Marketing Studio: estrategia, creatividad y contenido que funciona.'
    return page('VERTICE STUDIOS', d, body, head=seo('/blog/reel.html', 'VERTICE STUDIOS', d, 'assets/video/reel.jpg', 'website'))

def dato_page(n):
    body = (NAV + '<main>' + hero('Dato · [Fecha]', 'El dato que cambia <br>cómo planificamos') + '<section class="paper"><div class="wrap">' +
            '<div class="col" style="margin-top:0"><p class="fig">[00]%</p><p class="lead">[Una cifra con fuente y qué hacer con ella el lunes.]</p>'
            '<h2>[Qué dice el dato]</h2><p>[Texto editorial de la nota: de dónde sale la cifra, qué significa para las marcas y cómo cambia la forma de planificar. Dos o tres párrafos.]</p>'
            '<h2>[Qué hacer el lunes]</h2><p>[Una recomendación concreta y accionable.]</p><p class="src">Fuente: [Fuente de la cifra]</p></div>' +
            cta_box('¿Querés que tu estrategia de contenidos dé resultados medibles?', 'Contanos qué querés mover y armamos el recorrido juntos.', 'Hablemos →') + related(n) + '</div></section></main>' + FOOT)
    return page(n['title'] + ' | Vértice', n['desc'], body, head=note_head(n))

def index_page():
    body = (NAV.replace('<a class="back" href="index.html">← <span class="x">Todas las </span>notas</a>', '<a class="back" href="../index.html#vlog">← <span class="x">Volver al </span>sitio</a>') + '<main>' +
            hero('Noticias de Vértice', 'Vlog', 'Clientes nuevos, premios, festivales, research y datos. Un episodio por novedad, contado por el equipo, y la nota para leerla con calma.') +
            '<section class="paper"><div class="wrap"><div class="cards" style="margin-top:clamp(40px,5vw,64px)">%s</div></div></section></main>' % ''.join(card(n) for n in NOTES) + FOOT)
    d = 'Noticias de Vértice Content Marketing Studio: clientes, premios, lanzamientos y datos de la industria.'
    ld = {'@context': 'https://schema.org', '@type': 'Blog', 'name': 'Vlog de Vértice', 'url': BASE + '/blog/', 'inLanguage': 'es-AR', 'publisher': {'@type': 'Organization', 'name': SITE_NAME, 'url': BASE}}
    return page('Vlog | Vértice', d, body, head=seo('/blog/', 'Vlog | Vértice', d, 'og-home.jpg', 'website', ld))

# ---------- Descargas ----------
# Para sumar una presentación: copiar el PDF a descargas/files/, la portada a assets/descargas/ y agregar un item acá.
DOWNLOADS = [
    {'id': 'servicios', 'title': 'Presentación de servicios', 'tag': 'Presentación · 2026', 'file': 'descargas/files/vertice-presentacion-de-servicios-2026.pdf',
     'cover': 'assets/descargas/servicios-portada.jpg', 'info': 'PDF · 9 páginas · 2,2 MB',
     'desc': 'Qué hacemos y cómo trabajamos: estrategia, creatividad, producción, live streaming, contenido con IA y datos, en una sola presentación.'},
]
DL_CSS = r'''
.dl-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(340px,100%),1fr));gap:clamp(20px,2.6vw,40px);margin-top:calc(-1 * clamp(56px,7vw,100px))}
.dl{background:var(--blanco);border-radius:8px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 30px 80px -40px rgba(0,0,0,.45)}
.dl .m{aspect-ratio:16/9;background:var(--negro)}.dl .m img{display:block;width:100%;height:100%;object-fit:cover}
.dl .b{display:flex;flex-direction:column;gap:12px;padding:clamp(20px,2.2vw,30px);flex:1}
.dl .k{color:var(--rojo-texto);font-size:10px}
.dl h2{font-family:var(--display);font-weight:600;text-transform:uppercase;line-height:.96;font-size:clamp(34px,3.4vw,48px);text-wrap:balance}
.dl p{color:var(--gris-texto);font-size:16px;line-height:1.5}
.dl .f{display:flex;flex-wrap:wrap;gap:12px 18px;align-items:center;margin-top:auto;padding-top:10px}.dl .f span{font-size:10px;color:var(--gris-texto)}
.soon{margin-top:clamp(28px,3vw,44px);font-size:15px;color:var(--gris-texto)}
dialog.fm{border:0;padding:0;border-radius:12px;width:min(560px,calc(100vw - 24px));max-height:calc(100dvh - 24px);background:var(--papel);color:#111;overflow:auto;margin:auto}
dialog.fm::backdrop{background:rgba(0,0,0,.72)}
.fm .in{padding:clamp(24px,4vw,40px);display:flex;flex-direction:column;gap:16px;position:relative}
.fm .x{position:absolute;right:14px;top:14px;width:40px;height:40px;border-radius:999px;border:0;background:var(--negro);color:var(--blanco);font-size:18px;cursor:pointer}.fm .x:hover{background:var(--rojo)}
.fm h2{font-family:var(--display);font-weight:600;text-transform:uppercase;color:var(--rojo-texto);font-size:clamp(34px,5vw,48px);line-height:.96;padding-right:44px}
.fm .lede{font-size:16px;line-height:1.5;color:var(--gris-texto)}
.fm label{display:flex;flex-direction:column;gap:6px;font-family:var(--ext);text-transform:uppercase;letter-spacing:.14em;font-size:10px}
.fm input[type=text],.fm input[type=email]{font:inherit;font-family:var(--body);text-transform:none;letter-spacing:0;font-size:16px;min-height:48px;padding:0 14px;border:1.5px solid var(--negro);border-radius:8px;background:var(--blanco);color:#111}
.fm input:focus-visible{outline:2px solid var(--rojo);outline-offset:1px}
.fm .row{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media (max-width:520px){.fm .row{grid-template-columns:1fr}}
.fm .ck{flex-direction:row;align-items:flex-start;gap:10px;text-transform:none;letter-spacing:0;font-family:var(--body);font-size:13px;line-height:1.4;color:var(--gris-texto)}
.fm .ck input{margin-top:2px;width:18px;height:18px;accent-color:var(--rojo);flex:none}
.fm .hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.fm button.btn{border:0;cursor:pointer;font-size:12px;align-self:flex-start}.fm button.btn[disabled]{opacity:.6;cursor:wait}
.fm .err{color:var(--rojo-texto);font-size:14px;line-height:1.4}.fm .err a{font-weight:700}
.fm .ok{display:none;flex-direction:column;gap:16px}.fm.done .ok{display:flex}.fm.done form,.fm.done .lede,.fm.done .ttl{display:none}
.fm .ok p{font-size:16px;line-height:1.5}.fm .ok a.btn{align-self:flex-start}
'''

def dl_form(d):
    return ('<dialog class="fm" id="fm" aria-labelledby="fm-t"><div class="in"><button class="x" type="button" aria-label="Cerrar" data-close>✕</button>'
            '<p class="nx" style="color:var(--rojo-texto);font-size:10px">Descarga gratuita</p><h2 id="fm-t" class="ttl">Dejanos tus datos y descargá</h2>'
            '<p class="lede">Completá el formulario y la descarga empieza sola. Así sabemos a quién le sirve y podemos mandarte lo que viene.</p>'
            '<form name="descargas" method="POST" action="/descargas/gracias.html" data-netlify="true" netlify-honeypot="bot-field">'
            '<input type="hidden" name="form-name" value="descargas"><input type="hidden" name="archivo" id="fm-a" value="">'
            '<p class="hp"><label>No completar <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>'
            '<div class="row"><label>Nombre y apellido<input type="text" name="nombre" required autocomplete="name"></label>'
            '<label>Email de trabajo<input type="email" name="email" required autocomplete="email"></label></div>'
            '<div class="row" style="margin-top:14px"><label>Empresa<input type="text" name="empresa" required autocomplete="organization"></label>'
            '<label>Cargo<input type="text" name="cargo" autocomplete="organization-title"></label></div>'
            '<label class="ck" style="margin-top:14px"><input type="checkbox" name="consentimiento" value="si" required><span>Acepto que Vértice use estos datos para enviarme el material y contactarme. Puedo pedir la baja cuando quiera.</span></label>'
            '<p class="err" id="fm-e" role="alert" hidden></p>'
            '<button class="btn btn-k" type="submit" style="margin-top:14px"><span>Descargar</span> <i>↓</i></button></form>'
            '<div class="ok" role="status"><h2>¡Listo! Ya es tuyo</h2><p>La descarga empezó. Si no arrancó, usá este botón.</p>'
            '<a class="btn btn-k" id="fm-l" href="#" download>Descargar de nuevo <i>↓</i></a>'
            '<p>¿Querés ver cómo lo aplicamos a tu marca? <a href="%s" target="_blank" rel="noopener">Agendá una charla</a>.</p></div></div></dialog>') % CAL

DL_JS = r'''(function(){
var dlg=document.getElementById("fm"),f=dlg.querySelector("form"),err=document.getElementById("fm-e"),btn=f.querySelector("button[type=submit]"),cur=null;
function open(b){cur={t:b.dataset.title,f:b.dataset.file};document.getElementById("fm-a").value=cur.t;dlg.classList.remove("done");err.hidden=true;btn.disabled=false;document.getElementById("fm-t").textContent="Dejanos tus datos y descargá";
 if(dlg.showModal)dlg.showModal();else dlg.setAttribute("open","")}
document.querySelectorAll("[data-dl]").forEach(function(b){b.addEventListener("click",function(){open(b)})});
dlg.querySelectorAll("[data-close]").forEach(function(b){b.addEventListener("click",function(){dlg.close()})});
dlg.addEventListener("click",function(e){if(e.target===dlg)dlg.close()});
function go(){var a=document.getElementById("fm-l");a.href=cur.f;a.setAttribute("download",cur.f.split("/").pop());dlg.classList.add("done");a.click()}
f.addEventListener("submit",function(e){e.preventDefault();if(!cur)return;err.hidden=true;btn.disabled=true;
 var body=new URLSearchParams(new FormData(f)).toString();
 fetch("/",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:body}).then(function(r){if(!r.ok)throw new Error(r.status);go()}).catch(function(){
  btn.disabled=false;err.hidden=false;err.innerHTML="No pudimos enviar el formulario. Probá de nuevo o escribinos por <a href=\"%s\" target=\"_blank\" rel=\"noopener\">WhatsApp</a>."})});
})();''' % WA_URL

def dl_card(d):
    return ('<article class="dl"><div class="m"><img src="../%s" alt="Portada: %s" loading="lazy"></div><div class="b"><span class="nx k">%s</span><h2>%s</h2><p>%s</p>'
            '<div class="f"><button class="btn btn-k" type="button" data-dl data-title="%s" data-file="../%s">Descargar <i>↓</i></button><span class="nx">%s</span></div></div></article>') % (
        d['cover'], html.escape(d['title'], quote=True), html.escape(d['tag']), html.escape(d['title']), html.escape(d['desc']), html.escape(d['title'], quote=True), d['file'], html.escape(d['info']))

def descargas_page():
    body = (NAV.replace('<a class="back" href="index.html">← <span class="x">Todas las </span>notas</a>', '<a class="back" href="../index.html">← <span class="x">Volver al </span>sitio</a>') + '<main>' +
            hero('Material de Vértice', 'Descargas', 'Presentaciones y guías para llevarte. Dejás tus datos y la descarga empieza sola.') +
            '<section class="paper"><div class="wrap"><div class="dl-grid">%s</div><p class="soon">Vamos sumando material nuevo. Escribinos si buscás algo en particular.</p></div></section></main>' % ''.join(dl_card(d) for d in DOWNLOADS) +
            ''.join([dl_form(DOWNLOADS[0])]) + FOOT + '<script>' + DL_JS + '</script>')
    d = 'Descargá las presentaciones de Vértice Content Marketing Studio: servicios, casos y material para marcas y agencias.'
    return page('Descargas | Vértice', d, body, extra_css=DL_CSS, head=seo('/descargas/', 'Descargas | Vértice', d, DOWNLOADS[0]['cover'], 'website'))

def gracias_page():
    body = (NAV.replace('<a class="back" href="index.html">← <span class="x">Todas las </span>notas</a>', '<a class="back" href="../index.html">← <span class="x">Volver al </span>sitio</a>') + '<main>' +
            hero('Gracias', 'Recibimos tus datos', 'Si la descarga no empezó, volvé a Descargas y probá de nuevo.') +
            '<section class="paper"><div class="wrap"><p style="margin-top:32px"><a class="btn btn-k" href="index.html">Ir a Descargas <i>→</i></a></p></div></section></main>' + FOOT)
    return page('Gracias | Vértice', 'Gracias por tu interés en Vértice.', body, head=seo('/descargas/gracias.html', 'Gracias | Vértice', 'Gracias', 'og-home.jpg', 'website', noindex=True))

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
    os.makedirs(os.path.join(ROOT, 'descargas'), exist_ok=True)
    open(os.path.join(ROOT, 'descargas', 'index.html'), 'w').write(descargas_page())
    open(os.path.join(ROOT, 'descargas', 'gracias.html'), 'w').write(gracias_page())
    urls = [('/', '2026-11-11'), ('/blog/', '2026-11-11'), ('/blog/reel.html', '2026-11-11'), ('/descargas/', '2026-11-13')] + [('/blog/%s.html' % n['slug'], DATES[n['slug']]) for n in NOTES if not n.get('dato')]
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (BASE, u, d) for u, d in urls) + '</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nDisallow: /descargas/files/\nDisallow: /descargas/gracias.html\n\nSitemap: %s/sitemap.xml\n' % BASE)
    p = os.path.join(ROOT, 'index.html'); s = open(p).read()
    s = re.sub(r'<!--VLOG-->.*?<!--/VLOG-->', lambda m: '<!--VLOG-->\n      ' + home_cards() + '\n      <!--/VLOG-->', s, flags=re.S)
    open(p, 'w').write(s)
    print('ok', len(NOTES), 'notas')
