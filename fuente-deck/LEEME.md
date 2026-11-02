# Cómo se genera la propuesta

La presentación se arma sobre el template maestro de Vértice (`Vértice — Template Maestro.pptx`), que no está en el repositorio.

1. Copiá el template como `template.pptx` en esta carpeta.
2. `python3 stage.py`: duplica las láminas del template en el orden de la propuesta y descarta el resto (genera `stage.pptx`).
3. `python3 fill.py ../propuesta-move-37-vertice.pptx`: carga el contenido.

Requisitos: `python-pptx`, `lxml` y los scripts de la skill de PowerPoint (rutas en `stage.py`).
