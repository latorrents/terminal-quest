# Terminal Quest

Una aventura de texto para que niñas y niños aprendan a usar la terminal de Linux.
Despiertas en tu casa, el pueblo de Folderton tiene problemas, y para ayudar tendrás
que aprender "hechizos": `ls`, `cat`, `cd`, `mv`, `echo`, `mkdir`, `nano`, `chmod`,
`rm` y `sudo`.

## Guía rápida (si ya sabes usar la terminal)

```
git clone https://github.com/latorrents/terminal-quest.git
cd terminal-quest
python3 jugar.py
```

Si nunca has usado una terminal, sigue la guía paso a paso de abajo. No necesitas saber
nada de programación.

---

## Guía paso a paso

### Paso 1: Revisa que tu computadora sirva

Necesitas:

- **Una computadora con Linux o macOS.** En Windows funciona dentro de WSL (mira la
  sección [¿Y si tengo Windows?](#y-si-tengo-windows)).
- **Python 3, versión 3.8 o más nueva.** Es un programa gratuito. Casi todos los Linux y
  los Mac recientes ya lo traen instalado.
- **Unos 10 MB de espacio libre.**
- **Opcional: parlantes o audífonos** para escuchar los sonidos.

No hace falta internet para jugar, solo para descargar el juego la primera vez.

### Paso 2: Abre la terminal

La terminal es una ventana donde se escriben órdenes con el teclado.

- **Linux (Ubuntu, Fedora, Linux Mint...):** pulsa a la vez `Ctrl` + `Alt` + `T`.
  Si no se abre nada, busca "Terminal" en el menú de aplicaciones.
- **macOS:** pulsa `Cmd` + `Espacio`, escribe `Terminal` y pulsa `Enter`.

Verás una ventana con un texto parecido a `tunombre@tucomputadora:~$` y un cursor
parpadeando. Ahí es donde vas a escribir.

> **Consejo:** en todas las instrucciones, escribe el comando **exactamente igual** y
> luego pulsa la tecla `Enter` para ejecutarlo.

### Paso 3: Comprueba que tienes Python

Escribe esto en la terminal y pulsa `Enter`:

```
python3 --version
```

- Si aparece algo como `Python 3.12.3` (cualquier número desde **3.8** en adelante),
  ¡perfecto! Salta al **Paso 4**.
- Si aparece `command not found`, `orden no encontrada` o un número menor que 3.8,
  instala Python así:

  **Ubuntu, Debian o Linux Mint:**
  ```
  sudo apt update
  sudo apt install python3
  ```

  **Fedora:**
  ```
  sudo dnf install python3
  ```

  **macOS:** al escribir `python3 --version` el Mac suele ofrecer instalar las
  "herramientas de línea de comandos"; pulsa **Instalar** y espera a que termine.
  Si no aparece esa ventana, descarga Python desde
  [python.org/downloads](https://www.python.org/downloads/) e instálalo como cualquier
  otro programa.

  > Cuando escribas tu contraseña después de `sudo` **no verás nada en la pantalla**,
  > ni siquiera asteriscos. Es normal: escríbela y pulsa `Enter`.

  Después vuelve a escribir `python3 --version` para confirmar que ya funciona.

### Paso 4: Descarga el juego

Elige **una** de estas dos formas.

**Forma A: con git (recomendada)**

```
git clone https://github.com/latorrents/terminal-quest.git
```

Si te dice que `git` no existe, instálalo con `sudo apt install git` (Ubuntu/Debian/Mint),
`sudo dnf install git` (Fedora) o `xcode-select --install` (macOS), y vuelve a intentarlo.

**Forma B: sin git, descargando un ZIP**

1. Entra en [github.com/latorrents/terminal-quest](https://github.com/latorrents/terminal-quest).
2. Pulsa el botón verde **Code** y luego **Download ZIP**.
3. Abre la carpeta de Descargas y descomprime el archivo (clic derecho →
   **Extraer aquí** o doble clic en macOS).
4. Cambia el nombre de la carpeta `terminal-quest-master` (o `terminal-quest-main`)
   a `terminal-quest` y muévela a tu carpeta personal.

### Paso 5: Entra en la carpeta del juego

```
cd terminal-quest
```

Para comprobar que estás en el lugar correcto, escribe `ls`. Debes ver, entre otros,
`jugar.py` y `README.md`.

> ¿Dice `No existe el archivo o el directorio`? Seguramente la carpeta quedó en otro
> sitio. Si la dejaste en Descargas, prueba con `cd ~/Descargas/terminal-quest`
> (o `cd ~/Downloads/terminal-quest` si tu sistema está en inglés).

### Paso 6: ¡A jugar!

```
python3 jugar.py
```

Aparecerá el título **Terminal Quest** y un menú. Escribe `1` y pulsa `Enter` para
empezar la aventura.

> **Consejo:** agranda la ventana de la terminal (o ponla en pantalla completa) para
> que los dibujos se vean bien.

### Paso 7: Volver a jugar otro día

El juego **guarda tu progreso automáticamente**. La próxima vez solo tienes que abrir
la terminal y escribir:

```
cd terminal-quest
python3 jugar.py
```

En el menú elige **Continuar** para seguir donde lo dejaste.

---

## Cómo se juega

El juego te cuenta una historia y te pide que escribas comandos para avanzar. Si no
sabes qué hacer, lee la última pista en color: casi siempre te dice qué escribir.

| Quiero...                                   | Escribo o pulso                     |
|---------------------------------------------|-------------------------------------|
| Ver los hechizos (comandos) que conozco     | `ayuda`                             |
| Saber cómo funciona un hechizo              | `ayuda ls` (o el hechizo que sea)   |
| Que el texto aparezca de golpe              | cualquier tecla mientras se escribe |
| Completar un nombre largo                   | `Tab`                               |
| Repetir un comando que ya escribí           | flecha `↑` (arriba)                 |
| Guardar y salir                             | `salir` (o `Ctrl` + `D`)            |

Dentro del editor **nano** (aparece más adelante en la historia):

| Quiero...                     | Pulso                        |
|-------------------------------|------------------------------|
| Salir                         | `Ctrl` + `X`                 |
| Guardar los cambios al salir  | `S` y luego `Enter`          |
| Salir sin guardar             | `N`                          |
| Cancelar una pregunta         | `Ctrl` + `C`                 |

> **La contraseña de `sudo` dentro del juego es `password`.** No es la contraseña de tu
> computadora: es solo parte de la historia.

### Opciones para adultos

Se pueden añadir opciones al arrancar:

```
python3 jugar.py                 # menú: continuar, elegir capítulo o empezar de nuevo
python3 jugar.py 12              # empezar directamente en el desafío 12
python3 jugar.py 27 2            # empezar en el paso 2 del desafío 27
python3 jugar.py --rapido        # mostrar el texto sin efecto de máquina de escribir
python3 jugar.py --sin-sonido    # jugar sin sonidos
python3 jugar.py --help          # ver todas las opciones
```

---

## ¿Es seguro para mi computadora?

Sí. El juego **no ejecuta comandos reales del sistema**: `ls`, `cd`, `rm`, `sudo` y los
demás son imitaciones escritas en Python que solo funcionan dentro del mundo del juego.
Aunque el jugador escriba `rm` o `sudo`, no se toca nada fuera de la carpeta del juego
ni se usa tu contraseña real.

Todo lo que crea el juego queda en una carpeta oculta, `~/.terminal-quest/`:

- `mundo/` son las carpetas y archivos que explora el jugador. Se vuelve a crear en
  cada partida.
- `progreso.json` guarda el último desafío superado.

Para **borrar el progreso y empezar de cero**, cierra el juego y escribe:

```
rm -rf ~/.terminal-quest
```

Para **desinstalar el juego por completo**, borra también la carpeta que descargaste:

```
rm -rf ~/.terminal-quest ~/terminal-quest
```

(cambia `~/terminal-quest` por la ruta donde lo hayas guardado).

---

## Problemas frecuentes

**`python3: command not found` / `orden no encontrada`**
Python no está instalado. Vuelve al [Paso 3](#paso-3-comprueba-que-tienes-python).

**`can't open file 'jugar.py': No such file or directory`**
No estás dentro de la carpeta del juego. Vuelve al
[Paso 5](#paso-5-entra-en-la-carpeta-del-juego).

**`Terminal Quest necesita ejecutarse en una terminal.`**
Lo abriste con doble clic o desde un editor. Ábrelo desde la terminal con
`python3 jugar.py`.

**No se oye nada**
Los sonidos son opcionales y necesitan un reproductor del sistema (`paplay`, `pw-play`,
`aplay` o `afplay`). La mayoría de los Linux con escritorio y todos los Mac ya lo traen.
Si no lo tienes, el juego funciona igual, pero en silencio. Revisa también el volumen.

**Los dibujos se ven cortados o desordenados**
Agranda la ventana de la terminal (al menos 100 columnas de ancho) o reduce el tamaño
de letra con `Ctrl` + `-`.

**Los colores o las tildes se ven raros**
Usa la terminal que viene con tu sistema. Casi todas las modernas funcionan bien.

**El texto va muy lento**
Pulsa cualquier tecla para que aparezca de golpe, o arranca con
`python3 jugar.py --rapido`.

**Me quedé atascado en un desafío**
Lee la pista de color que aparece después de cada intento y escribe `ayuda`. Si aun así
no avanzas, escribe `salir`, vuelve a entrar y elige **Elegir un capítulo** para repetir
el desafío desde el principio.

### ¿Y si tengo Windows?

El juego necesita funciones de terminal que Windows no trae, pero puedes usar
**WSL** (Linux dentro de Windows), que es gratis y oficial de Microsoft:

1. Abre el menú Inicio, escribe `PowerShell`, haz clic derecho y elige
   **Ejecutar como administrador**.
2. Escribe `wsl --install` y pulsa `Enter`.
3. Reinicia la computadora cuando termine.
4. Abre **Ubuntu** desde el menú Inicio; la primera vez te pedirá crear un usuario y
   una contraseña.
5. En esa ventana de Ubuntu, sigue esta guía desde el
   [Paso 3](#paso-3-comprueba-que-tienes-python) como si tuvieras Linux.

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
