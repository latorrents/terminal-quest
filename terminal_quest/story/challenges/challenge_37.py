#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.location import generate_real_path
from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file
from terminal_quest.helpers import has_write_permissions, has_read_permissions, has_execute_permissions
from terminal_quest.terminals import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        "¡Encendiste el fuego artificial!",
        "{{gb:Aprendiste todos los comandos chmod.}}",
        "",
        "{{lb:¡Pum!}}",
        "",
        "Algo nuevo cayó delante de ti.",
        "{{lb:Mira alrededor}} para ver qué es."
    ]
    file_list = [
        {
            "path": "~/bosque/cueva/cofre",
            "permissions": 0o000,
            "type": "directory"
        },
        {
            "path": "~/bosque/cueva/cofre/respuesta",
            "type": "file",
            "permissions": 0o644,
            "contents": get_story_file("answer-cave")
        },
        {
            "path": "~/bosque/cueva/cofre/acertijo",
            "type": "file",
            "permissions": 0o644,
            "contents": get_story_file("riddle-cave")
        }
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para ver qué cayó delante de ti.}}"
    ]
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]

    def next(self):
        return 37, 2


class Step2(StepTemplateChmod):
    story = [
        "Hay un {{bb:cofre}} delante de ti.",
        "Está bien amarrado con una gran cadena.",
        "{{lb:Mira dentro del cofre.}}"
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    hints = [
        "{{rb:Usa}} {{yb:ls cofre}} {{rb:para ver dentro del cofre.}}"
    ]
    commands = [
        "ls cofre",
        "ls cofre/"
    ]

    def next(self):
        return 37, 3


class Step3(StepTemplateChmod):
    story = [
        "La cadena no se mueve. No puedes ver dentro ni sacar lo que hay.",
        "",
        "Rompe la cadena.",
        "{{lb:Tendrás que combinar todas las opciones de chmod que acabas de aprender: r, w y x.}}"
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    hints = [
        "{{rb:Usa}} {{yb:chmod +rwx cofre}} {{rb:para abrir el cofre.}}"
    ]

    def check_command(self, line):
        chest = generate_real_path("~/bosque/cueva/cofre")
        if has_write_permissions(chest) and has_read_permissions(chest) and has_execute_permissions(chest):
            return True
        self.send_stored_hint()

    def next(self):
        return 37, 4


class Step4(StepTemplateChmod):
    story = [
        "{{gb:¡Lo abriste!}}",
        "Ahora {{lb:mira dentro}} del cofre."
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"

    commands = [
        "ls cofre",
        "ls cofre/"
    ]

    hints = [
        "{{rb:Usa}} {{yb:ls cofre/}} {{rb:para mirar dentro del cofre.}}"
    ]

    def next(self):
        return 37, 5


class Step5(StepTemplateChmod):
    story = [
        "Ves un acertijo y una respuesta. {{lb:Examínalos.}}"
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "cat cofre/respuesta"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cat cofre/respuesta}} {{rb:para examinar la respuesta del cofre.}}"
    ]

    def check_command(self, last_user_input):
        if last_user_input == "cat cofre/acertijo":
            self.send_hint(
                "{{gb:Parece el acertijo que te hizo el Espadachin.}}"
            )
            return
        return StepTemplateChmod.check_command(self, last_user_input)

    def next(self):
        return 38, 1
