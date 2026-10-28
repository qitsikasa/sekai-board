# SEKAI Board — Práctica 6 · Programación Web I

Sitio fan del juego **Project Sekai: Colorful Stage!** hecho para la Práctica 6 de la clase de Programación Web I. Es una página de noticias y galería de imágenes con tema claro y oscuro.

> Proyecto de fan, sin fines de lucro. Todos los personajes, imágenes y marcas son de Colorful Palette / SEKAI Project.

---

## Páginas

| Página | Qué muestra |
|---|---|
| `web/index.html` | Inicio: evento en curso, noticias, unidades, imágenes recientes y canciones destacadas |
| `web/unidades.html` | Las 6 unidades con su logo y sus integrantes |
| `web/personajes.html` | Los 26 personajes, con filtro por unidad y enlace al booru |
| `web/eventos.html` | Los últimos 12 eventos en orden cronológico |
| `web/booru.html` | Galería de 54 imágenes con buscador por tags, filtros rápidos, visor ampliado y favoritos |

## Tecnologías

- **HTML5** — el base de cada página.
- **Bootstrap 5.3.3** — diseño responsivo (grid, navbar, modal, badges), por CDN.
- **Bootstrap Icons** e **Inter** (Google Fonts) — íconos y tipografía, por CDN.
- **CSS propio** (`web/css/sekai.css`, 265 líneas) — solo ajusta colores de Bootstrap para los dos temas.
- **JavaScript vanilla** (`web/js/sekai.js`, 44 líneas + scripts en cada página) — cambia el tema, pinta las tarjetas del `data.js`, busca y filtra.
- **`web/js/data.js`** (generado) — todo el contenido del sitio: unidades, personajes, eventos, canciones e imágenes.

## Tema claro y oscuro

- El botón ☀️ / 🌙 del menú cambia el tema.
- La elección se guarda en el navegador (`localStorage`) y se mantiene al recargar.
- Si no hay elección guardada, se usa el tema del sistema.

## Estructura del proyecto

```
sekai-board/
├── README.md
├── web/                    ← el sitio
│   ├── index.html
│   ├── unidades.html
│   ├── personajes.html
│   ├── eventos.html
│   ├── booru.html
│   ├── css/sekai.css
│   ├── js/data.js          ← contenido generado (no se edita a mano)
│   ├── js/sekai.js         ← utilidades: tema, fechas, unidades
│   └── tools/gen_data.py   ← script que genera data.js
├── cards_trained/          ← 36 cartas de personajes (galería)
├── songs/                  ← 26 jackets de canciones
├── events/                 ← 12 banners de eventos
├── characters/portraits/   ← 26 retratos
└── logos/                  ← 6 logos de unidades
```

Los assets están recortados: solo están los archivos que el sitio usa (105 archivos, ~17 MB).

## Cómo verlo en local

Desde la raíz del proyecto:

```bash
python3 -m http.server 8000
```

Luego abre <http://localhost:8000/web/index.html>.

(Necesita internet para cargar Bootstrap, los íconos y la fuente por CDN.)

## Cómo se generó `data.js`

El archivo `web/js/data.js` no se escribió a mano. Lo genera el script `web/tools/gen_data.py`:

```bash
python3 web/tools/gen_data.py
```

El script:

1. Lee `manifest.json` (índice de las imágenes descargadas) y las bases de datos oficiales del juego (`cards`, `events`, `musics`, `character2ds` de [sekai-world/sekai-master-db-diff](https://github.com/sekai-world/sekai-master-db-diff)).
2. Cruza los datos: por ejemplo, cada carta obtiene su personaje y su atributo; cada evento obtiene su nombre y sus fechas.
3. Le pone likes a las imágenes con una función de hash, para que siempre salgan los mismos números.
4. Verifica que todas las imágenes referenciadas existan.
5. Escribe `data.js` con la forma `window.SEKAI = { units: [...], characters: [...], events: [...], songs: [...], booru: [...] }`.

Las páginas leen `window.SEKAI` con JavaScript y pintan el contenido.

## Contenido del sitio

- 6 unidades: Leo/need, MORE MORE JUMP!, Vivid BAD SQUAD, Wonderlands × Showtime, 25:00 (Nightcord) y Virtual Singer.
- 26 personajes con retrato y unidad.
- 12 eventos con banner, fechas y tipo.
- 16 canciones destacadas con su jacket.
- 54 imágenes en el booru: cartas, jackets y banners, con tags (`card`, `miku`, `emu`, `cute`…), buscador y favoritos guardados en el navegador.

## Créditos

- Juego, personajes e imágenes: **Project Sekai: Colorful Stage!** de Colorful Palette / Bushiroad / SEKAI Project.
- Datos: [sekai-master-db-diff](https://github.com/sekai-world/sekai-master-db-diff).
- Framework: [Bootstrap 5.3.3](https://getbootstrap.com/).
- Hecho con ayuda de IA para la Práctica 6 — Programación Web I.
