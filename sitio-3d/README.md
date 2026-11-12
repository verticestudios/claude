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

- `netlify.toml`, `_redirects` y `_headers` quedan dentro de la carpeta. Si se sube arrastrando la carpeta, Netlify aplica `_redirects` y `_headers`; si se conecta el repo (publish directory `sitio-3d`), aplica `netlify.toml`.
- Redirects: `/blog/<nota>` sirve `/blog/<nota>.html` (las notas de la web anterior siguen funcionando) y `/noticias` lleva a `/blog/`.
- Favicon: `favicon.ico`, `favicon-32.png`, `favicon-192.png` y `apple-touch-icon.png` en la raíz, a partir del isotipo.
- Casos: los clips tienen audio; el botón de sonido de la sección activa el del caso del centro y "Ver caso" lo abre con sonido.

## SEO

- La home y cada página tienen título, descripción, canonical, Open Graph y Twitter Card; las notas llevan datos estructurados Article y la home Organization y WebSite.
- `sitemap.xml` y `robots.txt` se generan con `python3 blog/build.py`.
- Se conservan las URLs de imágenes de la web anterior (`blog-*.jpg`, `logo-rojo.png`, `favicon.png`) y las direcciones `/blog/<nota>.html`.
- Las notas anteriores que aún no se migraron (`equipo-estrategia`, `el-album`, `emergencias-ihsa`) redirigen a `/blog/` con 301; cuando se migren, quitar la regla en `netlify.toml` y `_redirects`.
- La nota `dato` es un placeholder: tiene `noindex` y no está en el sitemap.

## Pendiente: caso "El Regreso de La Voz Argentina"

Hay que sumarlo a Casos (Telefe, branded content: una competencia paralela para digital que le daba a los participantes eliminados la chance de volver en las instancias finales). El video está en Drive como "La Voz Argentina El Regreso TELEFE.mp4", pero es privado: hay que compartirlo con "cualquier persona con el enlace" o ponerlo en la carpeta compartida para poder bajarlo.
