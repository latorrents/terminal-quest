#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from terminal_quest.animation import Animation
from terminal_quest.step import StepTemplate
from terminal_quest.helpers import wrap_in_box
from terminal_quest.step_helpers import unblock_commands
from terminal_quest.terminals import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        "{{lb:Mira dentro}} del cuarto oscuro otra vez."
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "ls cuarto-oscuro",
        "ls ./cuarto-oscuro",
        "ls ./cuarto-oscuro/",
        "ls cuarto-oscuro/",
    ]

    hints = [
        "{{rb:Usa}} {{yb:ls cuarto-oscuro}} {{rb:para mirar dentro del cuarto-oscuro.}}"
    ]

    def next(self):
        return 35, 2


class Step2(StepTemplateChmod):
    story = [
        "Ves un letrero en el {{bb:cuarto-oscuro}}. {{lb:Lee el letrero.}}"
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "cat cuarto-oscuro/letrero"
    ]

    hints = [
        "{{rb:Usa}} {{yb:cat cuarto-oscuro/letrero}} {{rb:para leer el letrero.}}"
    ]

    def next(self):
        return 35, 3


class Step3(StepTemplateChmod):
    story = wrap_in_box([
        "{{gb:Nuevo Poder:}} Usa",
        "{{yb:chmod +x cuarto-cerrado}}",
        "para abrir el cuarto-cerrado."
    ])
    story += [
        "Úsalo en el {{bb:cuarto-cerrado}}."
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    hints = [
        "{{rb:Abre el cuarto-cerrado con}} {{yb:chmod +x cuarto-cerrado}}"
    ]
    commands = [
        "chmod +x cuarto-cerrado",
        "chmod +x cuarto-cerrado/"
    ]
    highlighted_commands = "chmod"

    def next(self):
        return 35, 4


class Step4(StepTemplateChmod):
    story = [
        "Ahora puedes {{lb:examinar}} los objetos del {{bb:cuarto-cerrado}}.",
        "{{lb:Lee el letrero del cuarto-cerrado.}}"
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "cat cuarto-cerrado/letrero"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cat cuarto-cerrado/letrero}} {{rb:para leer el letrero.}}"
    ]

    def check_commmand(self, line):
        if line == "cat cuarto-cerrado/fuego-artificial":
            self.send_hint("Ves un fuego artificial.")
            return

        return StepTemplateChmod.check_command(self, line)

    def next(self):
        return 35, 5


class Step5(StepTemplateChmod):
    story = wrap_in_box([
        "{{gb:Nuevo Poder:}} Escribe",
        "{{yb:chmod +w jaula}}",
        "para dar permiso de escritura",
        "y así abrir la jaula.",
    ])
    story += [
        "¡Pruébalo!"
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "chmod +w jaula",
        "chmod +w jaula/"
    ]
    hints = [
        "{{rb:Usa}} {{yb:chmod +w jaula}} {{rb:para abrir la jaula.}}"
    ]

    def next(self):
        return 35, 6


class Step6(StepTemplateChmod):
    story = [
        "Ahora puedes ayudar al pájaro a escapar de la jaula.",
        "{{lb:Mueve el pájaro fuera de la jaula, a donde estás tú.}}"
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "mv jaula/pajaro .",
        "mv jaula/pajaro ./"
    ]
    hints = [
        "{{rb:Usa}} {{yb:mv jaula/pajaro ./}} {{rb:para sacar al pájaro.}}"
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        Animation("bird-animation").play_across_screen(speed=5)
        return 36, 1
