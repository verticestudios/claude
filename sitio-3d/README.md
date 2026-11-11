# Vértice · propuesta de sitio web 3D

Propuesta de sitio de una página para Vértice Content Marketing Studio, con una escena WebGL (three.js) detrás del contenido.

- `index.html`: página completa (HTML, CSS y JS en un solo archivo).
- `assets/video/`: loops de 6 a 8 s comprimidos (854×480 o 480×854, sin audio) y sus pósters, tomados de la biblioteca de Drive (`02 · Rodajes` y `08 · Trabajos para clientes`).
- `assets/fonts/`, `assets/img/`: tipografías y logos del brand board.
- `assets/vendor/three.min.js`: three.js r128.

## Verlo

Los videos se usan como texturas, así que hay que servir la carpeta por HTTP (no abrir el archivo directo):

```bash
npx serve sitio-3d
```

## Qué hay en la escena

- Cordillera de líneas que fluye en el hero y crece en el cierre.
- Anillo de ocho videos: escultura en duotono rojo·negro en el hero, carrusel que gira con el scroll en el reel. La pieza del frente pasa a color y se abre en un visor.
- Sin WebGL, el reel pasa a una grilla de pósters. Con `prefers-reduced-motion` no hay giro ni reproducción automática.

## Pendiente de confirmar

- Títulos y créditos de cada pieza (salen de los nombres de archivo).
- Permiso de uso con marca de los trabajos para clientes.
- Número de WhatsApp y datos de contacto.
