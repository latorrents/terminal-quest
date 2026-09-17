#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.helpers import wrap_in_box
from terminal_quest.step_helpers import unblock_commands
from terminal_quest.terminals import TerminalChmod
from terminal_quest.terminals import TerminalNano


class StepTemplateNano(StepTemplate):
    TerminalClass = TerminalNano


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateNano):
    story = [
        "Hay tres puertas que llevan a dos cuartos y a una jaula.",
        "Primero, {{lb:mira dentro del cuarto-oscuro}}."
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "ls cuarto-oscuro",
        "ls cuarto-oscuro/"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls cuarto-oscuro/}} {{rb:para mirar dentro del cuarto-oscuro.}}"
    ]

    def next(self):
        return 34, 2


class Step2(StepTemplateNano):
    story = [
        "El cuarto está totalmente a oscuras y es imposible ver algo adentro.",
        "Ahora, {{lb:mira dentro}} del {{bb:cuarto-cerrado}}"
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
        return 34, 3


class Step3(StepTemplateNano):
    story = [
        "Espiando por una ventana sucia, apenas logras distinguir los objetos de adentro.",
        "{{lb:Examina los objetos de adentro}}."
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "cat cuarto-cerrado/letrero",
        "cat cuarto-cerrado/fuego-artificial"
    ]
    hints = [
        "{{rb:Examina el letrero con}} {{yb:cat cuarto-cerrado/letrero}}"
    ]

    def next(self):
        return 34, 4


class Step4(StepTemplateNano):
    story = [
        "No logras distinguir bien los objetos del cuarto.",
        "¿Tal vez ayudaría si entraras?",
        "Intenta {{lb:entrar}} al {{bb:cuarto-cerrado}}."
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    dirs_to_attempt = "~/bosque/cueva/cuarto-cerrado"
    hints = [
        "{{rb:Entra al cuarto-cerrado con}} {{yb:cd cuarto-cerrado}}"
    ]
    commands = [
        "cd cuarto-cerrado",
        "cd cuarto-cerrado/"
    ]

    def block_command(self, last_user_input):
        return unblock_commands(last_user_input, self.commands)

    def next(self):
        return 34, 5


class Step5(StepTemplateNano):
    story = [
        "La puerta está cerrada, así que no puedes entrar.",
        "Por último, {{lb:mira dentro}} de la {{bb:jaula}}."
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "ls jaula",
        "ls jaula/"
    ]
    hints = [
        "{{rb:Mira dentro de la jaula con}} {{yb:ls jaula}}"
    ]

    def next(self):
        return 34, 6


class Step6(StepTemplateNano):
    story = [
        "Hay un pájaro en la jaula. {{lb:Examina}} el pájaro.",
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "cat jaula/pajaro"
    ]
    hints = [
        "{{rb:Examina el pájaro con}} {{yb:cat jaula/pajaro}}"
    ]

    def next(self):
        return 34, 7


class Step7(StepTemplateNano):
    story = [
        "Pájaro: {{Bb:\"...Estoy...atrapado..\"}}",
        "{{Bb:\"Por favor, ayuda....sácame de aquí.\"}}",
        "",
        "Ayuda al pájaro {{lb:moviendo}} el {{lb:pajaro}} fuera de la {{lb:jaula}}."
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "mv jaula/pajaro .",
        "mv jaula/pajaro ./"
    ]
    hints = [
        "{{rb:Saca el pájaro de la jaula con}} {{yb:mv jaula/pajaro ./}}"
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 34, 8



class Step8(StepTemplateChmod):
    story = [
        "No puedes sacar el {{bb:pajaro}} de la {{bb:jaula}}.",
        "Pájaro: {{Bb:\"...no funcionó....\"}}",
        "{{Bb:\"...busca en el}} {{lb:cuarto-oscuro}} {{Bb:para encontrar ayuda..\"}}",
        "{{Bb:\"..usa}} {{yb:chmod +r cuarto-oscuro}} {{Bb:para encender las luces.\"}}",
        "{{Bb:\"...sácame de aquí...y te ayudaré.\"}}",
        ""
    ]
    story += wrap_in_box([
        "{{gb:Nuevo Poder:}} Usa ",
        "{{yb:chmod +r cuarto-oscuro}} ",
        "para darte permiso de {{lb:leer}} ",
        "el contenido del cuarto-oscuro."
    ])

    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "chmod +r cuarto-oscuro",
        "chmod +r cuarto-oscuro/"
    ]
    highlighted_commands = "chmod"
    hints = [
        "{{rb:Sigue las instrucciones del pájaro y usa}} {{yb:chmod +r cuarto-oscuro}} {{rb:para encender las luces del}} "
        "{{bb:cuarto-oscuro.}}"
    ]

    def next(self):
        return 35, 1
