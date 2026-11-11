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

- Hero: cordillera de líneas y una pantalla curva con el reel de agencia; el botón abre el reel completo con sonido.
- Casos: pared curva de siete videos que gira con el scroll. El del centro pasa de duotono a color y se abre en un visor.
- Servicios: índice de filas con los íconos del brand board.
- Vértice CoCreate: ascenso a la cumbre con las cuatro etapas y sus logos.
- Vlog: cuatro notas de ejemplo (video, foto, nota editorial y video vertical con texto).
- Los botones "Hablemos" abren la página de citas.
- Sin WebGL, los casos pasan a una grilla de pósters. Con `prefers-reduced-motion` no hay reproducción automática.

## Pendiente de confirmar

- Títulos y créditos de cada caso (salen de los nombres de archivo).
- Permiso de uso con marca de los trabajos para clientes.
- Contenido real del vlog: las cuatro notas son de ejemplo.
- Ícono de Live streaming: no está en el brand board, se dibujó en el mismo estilo.
