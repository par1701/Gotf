# Traspaso del proyecto (creador Cypher en español)

Web: repositorio `par1701/gotf` (GitHub Pages). Archivos publicados en la raíz: `index.html`, `data.json`, `hoja_es.pdf`, `pdf-lib.esm.min.js`.

## Cómo retomar en una sesión nueva

1. Clonar: `git clone https://github.com/par1701/gotf /home/claude/gotf-repo`
2. Enlazar las rutas que usan los scripts:
   ```
   ln -s /home/claude/gotf-repo/fuentes/gotf /home/claude/gotf
   ln -s /home/claude/gotf-repo/fuentes/scripts /home/claude/scripts
   mkdir -p /home/claude/site && cp /home/claude/gotf-repo/{index.html,data.json,hoja_es.pdf,pdf-lib.esm.min.js} /home/claude/site/
   ```
3. Reconstruir datos: `python3 /home/claude/scripts/build.py` (escribe `/home/claude/site/data.json`).
4. Probar: `cd /home/claude/site && python3 -m http.server 8765` y Playwright.
5. Publicar: copiar `site/index.html` y `site/data.json` a la raíz del repo, commit y `git -c push.negotiate=true push`.
6. Para extraer reglas nuevas hace falta adjuntar el PDF del *Cypher Character Rulebook* (2026-06-12). Página del PDF = página del libro + 2.

## Estructura

- `fuentes/gotf/`: datos extraídos y traducidos. `tr/*.json` son las traducciones (focos, tipos, género). `sf_*.json`: ciencia ficción.
- `fuentes/scripts/build.py`: une todo en `data.json`. `trf.py` (`F()`) añade traducciones de focos; `sfput.py` (`put()`) tipos de CF; `reuse.py` reutiliza traducciones idénticas.
- `fuentes/sheet/gen.py`: genera `hoja_es.pdf` (hoja oficial traducida). Necesita la hoja oficial rellenable de Monte Cook Games como `orig.pdf` (no incluida).
- `index.html`: `SETTINGS` define cada ambientación (género, tipos, lista de habilidades, focos sugeridos, textos). `applySetting()` filtra `DALL` en `D`. `GOTF()` activa la capa divina; `AEON()` la de psiones de Æon (`aeForm()`, `aePicks()`, `aeAvail()`, `psiE()`, `aeGuide()`). Sin `#guia` ni `#creador` en la URL se muestra la portada neutra (`renderHome()`), desde la que se elige la ambientación.
- `fuentes/aeon/aptitudes.md`: exportación en Markdown del documento «Æon a Cypher — Aptitudes psíquicas». `fuentes/scripts/aeon.py` saca de él `fuentes/aeon/aeon.json` (Aptitudes como focos con `col` = Modo y `tier` = fila, órdenes, habilidades de género psíquicas, textos de la guía); `build.py` lo añade a `data.json`. Si el documento cambia: exportarlo de nuevo, `python3 fuentes/scripts/aeon.py` y `build.py`.

## Hecho

- Ambientaciones: Gods of the Fall, Fantasía (CCR), Ciencia ficción dura, Space opera, Postapocalipsis.
- 793/793 habilidades de foco traducidas; 25 tipos de fantasía y 17 de CF; habilidades de género de fantasía y CF; especies de fantasía y CF.
- Guardar/cargar, importar/exportar, PDF en la hoja oficial en español, heridas según capacidad, rango por avances, reglas de dominio de GotF, Máquina, no carne automatizada.

## Pendiente

- Æon, fase 2: Modos auxiliares, cambios de poder psi (rangos 1 y 4), opciones de orden de Prometheus Unbound, Terra Firma y Nidavellir, y equipo de Æon.

- Fase 3: superhéroes (7 tipos por rango, cambios de poder, habilidades de origen, Superheroics, adaptar tipos alternativos).
- Fase 4: mundo real (solo personaje núcleo, habilidades del mundo real, habilidad extra en rangos 3 y 6, excepción de armas).
- Restricción por rango de habilidades marcadas con asterisco (ataque, defensa, artillería).
- Convertir 4 focos de GotF sin equivalente: Crafts Unique Objects, Siphons Power, Travels Through Time, Exists in Two Places at Once.
- «raver» sin traducir; concordancia de género en la frase («Soy Bruja»).

## Normas del usuario

Español de España, conciso. Fidelidad estricta al material; reglas del CCR. Nombres en español con el original entre paréntesis. En la frase, el tipo va antes del descriptor. Avisar de límites de tokens y de lo que quede sin hacer.
