# Vértice · propuesta de sitio web 3D

Propuesta de sitio de una página para Vértice Content Marketing Studio, con una escena WebGL (three.js) detrás del contenido.

- `index.html`: página completa (HTML, CSS y JS en un solo archivo).
- `assets/video/`: loops comprimidos sin audio y sus pósters, más `reel.mp4` (reel de agencia completo, con audio), tomados de la biblioteca de Drive (`02 · Rodajes` y `08 · Trabajos para clientes`).
- `assets/fonts/`, `assets/img/`: tipografías y logos del brand board.
- `assets/vendor/three.min.js`: three.js r128.

## Verlo

Los videos se usan como texturas, así que hay que servir la carpeta por HTTP (no abrir el archivo directo):

```bash
npx serve sitio-3d
```

## Qué hay en la página

- Hero: cordillera de líneas (isolíneas sobre un relieve que tapa lo de atrás). El reel de agencia se abre con el botón "Ver el reel con sonido".
- Marcas: slider de logos de clientes en negro (`assets/img/clients/`).
- Casos: pared curva de siete videos que gira con el scroll, con un párrafo por caso (editable en `data-d` de cada botón).
- Servicios: índice de filas con los íconos del brand board.
- Vértice CoCreate: ascenso a la cumbre que se anima etapa por etapa desde Entender; al pasar el mouse por una etapa se abre su ficha con logo.
- Reel: `blog/reel.html` (el botón "Ver el reel con sonido" del hero).
- Vlog: seis notas en páginas aparte (`blog/`): los highlights de Octubre (video 16:9 y módulo vertical 9:16, redactada sobre el artículo de Adlatina), el módulo Dato (placeholder) y cuatro notas migradas de verticestudios.com. `python3 blog/build.py` regenera las páginas y las tarjetas del Vlog de la home a partir de `blog/notes.json`.
- Redes de Vértice en el header y el footer. Los botones "Hablemos" abren la página de citas.
- Sin WebGL, los casos pasan a una grilla de pósters. Con `prefers-reduced-motion` no hay reproducción ni animación automática.

## Pendiente de confirmar

- Títulos y créditos de cada caso (salen de los nombres de archivo).
- Permiso de uso con marca de los trabajos para clientes.
- Los párrafos de los casos son una propuesta redactada: validar datos y cifras (por ejemplo +9% en ventas de Vecinos Felices y +3M de impactos de Di María × Coca-Cola, tomados del texto en pantalla de cada video).
- Nombre del evento del After Movie, que quedó como marcador entre corchetes.
- Que los videos de highlights usados (Adlatina y Marketers) sean los de Octubre: los archivos de la carpeta parecen de agosto.
- Los párrafos de los casos son una propuesta redactada: validar datos y cifras.
- Ícono de Live streaming: no está en el brand board, se dibujó en el mismo estilo.

## Netlify

- `netlify.toml` y `_redirects` quedan dentro de la carpeta. Si se sube arrastrando la carpeta, Netlify aplica `_redirects`; si se conecta el repo (publish directory `sitio-3d`), aplica `netlify.toml`.
- Redirects: `/blog/<nota>` sirve `/blog/<nota>.html` (las notas de la web anterior siguen funcionando) y `/noticias` lleva a `/blog/`.
- Favicon: `favicon.ico`, `favicon-32.png`, `favicon-192.png` y `apple-touch-icon.png` en la raíz, a partir del isotipo.
- Casos: los clips tienen audio; el botón de sonido de la sección activa el del caso del centro y "Ver caso" lo abre con sonido.

## SEO

- La home y cada página tienen título, descripción, canonical, Open Graph y Twitter Card; las notas llevan datos estructurados Article y la home Organization y WebSite.
- `sitemap.xml` y `robots.txt` se generan con `python3 blog/build.py`.
- Se conservan las URLs de imágenes de la web anterior (`blog-*.jpg`, `logo-rojo.png`, `favicon.png`) y las direcciones `/blog/<nota>.html`.
- Las notas anteriores que aún no se migraron (`equipo-estrategia`, `el-album`, `emergencias-ihsa`) redirigen a `/blog/` con 301; cuando se migren, quitar la regla en `netlify.toml` y `_redirects`.
- La nota `dato` es un placeholder: tiene `noindex` y no está en el sitemap.

## Casos agregados: Mayumana 2025 y El Regreso de La Voz Argentina

Salen de "Mayumana 2025.mp4" y "La Voz Argentina El Regreso TELEFE.mp4" (Drive). Los clips son los primeros 8 s de La Voz y los segundos 3 a 11 de Mayumana. Los textos son los que dio el cliente; validar el de La Voz.

## Videos de los casos

- Cada caso tiene un loop corto (`<caso>.mp4`, 6 a 8 s) para la pared 3D y el video completo (`<caso>-full.mp4`, 480p con audio) que abre "Ver caso".
- La Voz: el video original es un episodio de 26 minutos; se publica un fragmento de los primeros 3 minutos. Para ver más, recodificar `lavoz.mp4` con un tramo más largo (pesa unos 3,7 MB por minuto).
- Auren+ (`auren-collage*`): collage de tres columnas verticales con tres momentos distintos del video. El loop usa tres tramos (producto, textura, rostro) y "Ver caso" abre el video completo con las tres columnas desfasadas en el tiempo.
- Caché: no se fuerza caché en `assets/`; si se reemplaza un archivo, conviene cambiarle el nombre.

## Servicios: fichas ampliadas

Al hacer clic en un servicio se abre una ficha (con cierre por ✕, botón Cerrar, Esc o clic afuera). El contenido vive en el arreglo `SVC` de `index.html`.

- Salen de la presentación de servicios y de las notas del blog: Estrategia, Creatividad, Producción, Live streaming, Contenido IA (CEREBRO), Datos y los textos de Web y UGC.
- Propuestos por IA, para validar: viñetas de Social media, UGC, Podcast, Contenido, Eventos, Web y Paid media.
- Se sumó UGC como servicio porque figura en la presentación y no estaba en la web.

## Casos: créditos

Cada caso tiene `data-k` con los créditos (dirección general creativa y dupla de directores) y `data-b` con la marca que va en la primera línea del título.

## Descargas

- Menú superior (y menú mobile con ☰): "Descargas" lleva a `descargas/index.html`. No está en las secciones de la home ni en el footer.
- Cada presentación es un item de `DOWNLOADS` en `blog/build.py`. Para sumar una: copiar el PDF a `descargas/files/`, la portada a `assets/descargas/`, agregar el item y correr `python3 blog/build.py`.
- Al apretar "Descargar" se abre el formulario (nombre, email, empresa, cargo, consentimiento). Se envía por Netlify Forms (formulario `descargas`) y, si salió bien, la descarga empieza sola; queda un botón por si el navegador la bloquea. Si falla el envío, no se descarga y se ofrece WhatsApp.
- Netlify: tras publicar, en Forms → `descargas` → Settings & notifications, activar el aviso por email. Los contactos quedan en Forms → Submissions (exportables a CSV).
- Importante: es una "puerta blanda". El PDF es un archivo público (`/descargas/files/…`): está fuera del sitemap y con Disallow en robots.txt, pero quien tenga la URL puede bajarlo sin formulario. Para protegerlo de verdad haría falta una Netlify Function que entregue un link firmado.
- `descargas/gracias.html` es noindex (fallback si el navegador envía el formulario sin JS).
