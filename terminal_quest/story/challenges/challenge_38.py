#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

# Redo chapter 5 with the swordmaster.

import os

from terminal_quest.step import StepTemplate
from terminal_quest.location import generate_real_path
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.terminals import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        "{{gb:¡Encontraste la respuesta al acertijo del Espadachin!}}",
        "",
        "{{lb:Vuelve al claro del Espadachin.}}"
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/claro"
    hints = [
        "Vuelve al {{bb:~/bosque/claro}}, donde vive el Espadachin.",
        "{{rb:Usa}} {{yb:cd ~/bosque/claro}} {{rb:para volver al claro del Espadachin.}}"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 38, 2


class Step2(StepTemplateChmod):
    story = [
        "Toca a la puerta del Espadachin."
    ]
    start_dir = "~/bosque/claro"
    end_dir = "~/bosque/claro"
    commands = [
        "echo knock knock",
        "echo toc toc",
        "echo Toc toc",
        "echo Toc Toc"
    ]
    hints = [
        "{{rb:Usa}} {{yb:echo toc toc}} {{rb:para tocar a la puerta del Espadachin.}}"
    ]

    def next(self):
        return 38, 3


class Step3(StepTemplateChmod):
    story = [
        "Espadachin:",
        "{{Bb:\"Si me tienes, quieres compartirme.",
        "Si me compartes, ya no me tienes.",
        "¿Qué soy?\"}}",
        "",
        "{{yb:1. Un secreto}}",
        "{{yb:2. No sé}}",
        "",
        "Usa {{lb:echo}} para responder."
    ]
    start_dir = "~/bosque/claro"
    end_dir = "~/bosque/claro"
    commands = [
        "echo 1",
        "echo secret",
        "echo a secret",
        "echo A secret",
        "echo \"secret\"",
        "echo \"a secret\"",
        "echo \"A secret\"",
        "echo secreto",
        "echo Secreto",
        "echo un secreto",
        "echo Un secreto",
        "echo \"secreto\"",
        "echo \"un secreto\"",
        "echo \"Un secreto\""
    ]

    def check_command(self, line):
        if line.startswith("echo ") and line not in self.commands:
            self.send_hint("Espadachin: {{Bb:\"Incorrecto. ¿Terminaste los desafíos de la cueva? "
                           "La respuesta estaba allí.\"}}")
        return StepTemplateChmod.check_command(self, line)

    def next(self):
        path = generate_real_path("~/bosque/claro/casa")
        os.chmod(path, 0o755)
        return 38, 4


class Step4(StepTemplateChmod):
    story = [
        "{{wb:Clonc.}} {{gb:Parece que la puerta se abrió.}}",
        "",
        "{{lb:Entra en la casa.}}"
    ]
    start_dir = "~/bosque/claro"
    end_dir = "~/bosque/claro/casa"
    hints = [
        "{{rb:Usa}} {{yb:cd casa}} {{rb:para entrar.}}"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 38, 5


class Step5(StepTemplateChmod):
    story = [
        "{{lb:Mira alrededor.}}"
    ]
    start_dir = "~/bosque/claro/casa"
    end_dir = "~/bosque/claro/casa"
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]
    commands = [
        "ls"
    ]

    def next(self):
        return 39, 1
