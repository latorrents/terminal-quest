# challenge_3.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from terminal_quest.step import StepTemplate
from terminal_quest.terminals import TerminalCat


class StepTemplateCat(StepTemplate):
    TerminalClass = TerminalCat


class Step1(StepTemplateCat):
    story = [
        "¡Muy linda! Póntela rápido.",
        "Hay muchas otras cosas interesantes en tu habitación.\n",
        "Vamos a {{lb:mirar}} en tus {{bb:estantes}} usando {{yb:ls}}.\n"
    ]
    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"
    commands = ["ls estantes", "ls estantes/"]
    hints = ["{{rb:Escribe}} {{yb:ls estantes/}} {{rb:para mirar tus libros.}}"]

    def next(self):
        return 3, 2


class Step2(StepTemplateCat):
    story = [
        "¿Sabes que puedes usar la tecla {{ob:TAB}} para acelerar tu escritura?",
        "Inténtalo echándole un vistazo a esa {{bb:historieta}}.\n",
        "{{lb:Examina}} la historieta con {{yb:cat estantes/historieta}}\n",
        "¡Presiona la tecla {{ob:TAB}} antes de que hayas terminado de escribir!\n"
    ]
    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"
    commands = "cat estantes/historieta"
    hints = ["{{rb:Escribe}} {{yb:cat estantes/historieta}} {{rb:para leer la historieta.}}"]

    def next(self):
        return 3, 3


class Step3(StepTemplateCat):
    story = [
        "¿Por qué tiene huellas de garras?",
        "Espera un momento, ¿puedes ver eso? Hay una {{bb:nota}} entre tus libros.\n",
        "{{lb:Lee}} la {{bb:nota}} usando {{yb:cat}}.\n"
    ]
    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"
    commands = "cat estantes/nota"
    hints = ["{{rb:Escribe}} {{yb:cat estantes/nota}} {{rb:para leer la nota.}}"]

    def next(self):
        return 4, 1
