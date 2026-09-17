# Terminal Quest

Una aventura de texto para que niñas y niños aprendan a usar la terminal de Linux.
Despiertas en tu casa, el pueblo de Folderton tiene problemas, y para ayudar tendrás
que aprender "hechizos": `ls`, `cat`, `cd`, `mv`, `echo`, `mkdir`, `nano`, `chmod`,
`rm` y `sudo`.

## Cómo jugar

Solo necesitas Python 3.8 o más reciente (en Linux o macOS):

```
python3 jugar.py
```

No hace falta instalar nada más. El juego se juega en la terminal y guarda tu progreso
automáticamente.

Dentro del juego:

- `ayuda` muestra los hechizos que conoces, y `ayuda ls` explica uno en particular.
- `salir` (o `Ctrl D`) guarda y sale.
- `Tab` completa nombres de archivos y la flecha ARRIBA repite comandos anteriores.
- Si el texto aparece muy lento, pulsa cualquier tecla para mostrarlo completo.

### Opciones

```
python3 jugar.py                 # menú: continuar, elegir capítulo o empezar de nuevo
python3 jugar.py 12              # empezar directamente en el desafío 12
python3 jugar.py 27 2            # empezar en el paso 2 del desafío 27
python3 jugar.py --rapido        # mostrar el texto sin efecto de máquina de escribir
python3 jugar.py --sin-sonido    # jugar sin sonidos
```

Los sonidos son opcionales: se reproducen si el sistema tiene `paplay`, `pw-play`,
`aplay` o `afplay`. Si no, el juego funciona igual en silencio.

## Dónde se guardan las cosas

Todo queda en `~/.terminal-quest/`:

- `mundo/` es el mundo del juego: carpetas y archivos reales que el jugador explora.
  Se vuelve a crear en cada partida, así que se puede borrar sin problema.
- `progreso.json` guarda el último desafío superado.

Para empezar de cero, borra la carpeta `~/.terminal-quest`.

## Cómo está organizado

```
jugar.py                       punto de entrada
terminal_quest/
  main.py                      argumentos y arranque
  menu.py                      menú inicial
  controller.py                pasa de un paso de la historia al siguiente
  step.py                      plantilla de los pasos y lógica de nano
  terminals.py                 la terminal del jugador (un "hechizo" nuevo por nivel)
  commands.py                  ls, cat, cd, mv, echo, mkdir, chmod, rm... en Python puro
  nano.py                      editor tipo nano hecho con curses
  ui.py                        colores, efecto de escritura, pistas y hechizos
  animation.py                 animaciones de arte ASCII
  sound.py                     sonidos opcionales
  file_tree.py                 crea el mundo en disco
  titles.py                    títulos de capítulos y desafíos
  story/challenges/            los 46 desafíos de la historia
  story/trees/                 cómo es el mundo en cada momento de la historia
  assets/story_files/          arte ASCII, notas, carteles y ayudas de cada hechizo
  assets/sounds/               sonidos (ver ATTRIBUTION)
```

El texto de la historia usa marcas de color como `{{yb:ls}}`: la primera letra es el
color (`r` rojo, `g` verde, `y` amarillo, `b` azul, `o` naranja, `l` lila, `B` celeste,
`w` blanco...) y la segunda es `b` (negrita) o `n` (normal).

Los nombres de archivos y carpetas del mundo no llevan tildes ni ñ (`jardin`, `sotano`),
como es costumbre en Linux, para que sean fáciles de escribir.

## Origen y autoría

Esta es una **adaptación standalone en Python 3** de
[Terminal Quest](https://github.com/KanoComputing/terminal-quest) (paquete `linux-story`),
el juego que Kano Computing Ltd. creó para Kano OS, un sistema que ya no tiene
mantenimiento.

La versión original solo funcionaba dentro de Kano OS: necesitaba GTK, VTE, las
bibliotecas propias de Kano y una versión modificada de nano escrita en C. Esta
adaptación funciona sola en cualquier terminal de Linux o macOS y solo necesita
Python 3.

Adaptación realizada por **David Latorre** ([latorredev.com](https://latorredev.com),
david@latorredev.com) en 2026. Los cambios respecto al original son:

- Reescritura como programa de terminal independiente, sin GTK, VTE ni bibliotecas de Kano.
- Comandos (`ls`, `cat`, `cd`, `mv`, `echo`, `mkdir`, `chmod`, `rm`, `sudo`) y editor
  `nano` reimplementados en Python puro con `curses`.
- Traducción de la historia, los textos y los nombres de archivos al español.
- Nueva estructura del proyecto (`terminal_quest/`), menú inicial, guardado de
  progreso en `~/.terminal-quest/` y opciones de línea de comandos.
- Eliminación del empaquetado para Debian/Kano OS y de las pruebas antiguas.

Este proyecto no está afiliado a Kano Computing Ltd. ni cuenta con su respaldo.
"Kano" y "Terminal Quest" son marcas de sus respectivos propietarios.

## Licencia

```
Terminal Quest
Copyright (C) 2014-2016 Kano Computing Ltd.

Adaptación standalone en Python 3
Copyright (C) 2026 David Latorre <david@latorredev.com>
```

Como obra derivada de un programa publicado bajo la **GNU General Public License
versión 2**, esta adaptación se distribuye bajo esa misma licencia. El texto completo
está en [`LICENSE`](LICENSE).

Este programa es software libre: puedes redistribuirlo y/o modificarlo bajo los
términos de la GNU GPL v2 publicada por la Free Software Foundation. Se distribuye
con la esperanza de que sea útil, pero **SIN NINGUNA GARANTÍA**, ni siquiera la
garantía implícita de COMERCIABILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR.
Consulta la licencia para más detalles.

Si redistribuyes o modificas este juego, debes mantener estos avisos de copyright,
incluir la licencia y publicar el código fuente de tus cambios bajo la GPL v2.

### Contenido de terceros

Los sonidos de `terminal_quest/assets/sounds/` vienen de
[freesound.org](https://freesound.org) y tienen sus propias licencias
(Creative Commons Attribution 3.0 o CC0). Los autores y enlaces de cada sonido
están en [`ATTRIBUTION`](terminal_quest/assets/sounds/ATTRIBUTION), junto a los
textos de licencia `LICENSE-BY` y `LICENSE-CC0`.
