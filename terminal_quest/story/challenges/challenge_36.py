#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file
from terminal_quest.step_helpers import unblock_commands
from terminal_quest.terminals import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        "El pájaro dejó caer un {{bb:pergamino}} en la {{bb:jaula}}.",
        "{{lb:Examina}} el pergamino."
    ]

    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "cat jaula/pergamino"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cat jaula/pergamino}} {{rb:para examinar el pergamino.}}"
    ]
    file_list = [
        {
            "path": "~/bosque/cueva/jaula/pergamino",
            "contents": get_story_file("scroll-cage")
        }
    ]
    deleted_items = [
        "~/bosque/cueva/pajaro"
    ]

    def next(self):
        return 36, 2


class Step2(StepTemplateChmod):
    story = [
        "Sigue las instrucciones. Usa {{yb:chmod +x}} en el {{bb:encendedor}} del {{bb:cuarto-cerrado}}."
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "chmod +x cuarto-cerrado/encendedor"
    ]
    hints = [
        "{{rb:Usa}} {{yb:chmod +x cuarto-cerrado/encendedor}} {{rb:para activar el encendedor.}}"
    ]
    highlighted_commands = "chmod"

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 36, 3


class Step3(StepTemplateChmod):
    story = [
        "{{lb:Mira dentro del cuarto-cerrado}} para ver qué le pasó al encendedor."
    ]

    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"

    commands = [
        "ls cuarto-cerrado",
        "ls cuarto-cerrado/"
    ]

    hints = [
        "{{rb:Usa}} {{yb:ls cuarto-cerrado/}} {{rb:para mirar dentro del cuarto-cerrado.}}"
    ]

    def next(self):
        return 36, 4


class Step4(StepTemplateChmod):
    story = [
        "El encendedor se puso {{gb:verde brillante}} cuando lo activaste.",
        "Ahora úsalo con {{yb:./cuarto-cerrado/encendedor}}"
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"

    commands = [
        "./cuarto-cerrado/encendedor"
    ]

    def next(self):
        return 37, 1
