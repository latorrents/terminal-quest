#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.terminals import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        "Espadachin: {{Bb:\"...esto es muy extraño. Dejé la puerta abierta. Quizás alguien... o "
        "algo... se coló mientras hablábamos.\"}}",
        "{{Bb:\"Puede que necesites mi ayuda más adelante. Vuelve si te quedas atascado por falta de conocimiento.\"}}",
        "",
        "Es hora de partir: {{lb:sal}} de la casa del Espadachin."
    ]
    start_dir = "~/bosque/claro/casa"
    end_dir = "~/bosque/claro"

    hints = [
        "{{rb:Sal de la casa con}} {{yb:cd ..}}"
    ]

    file_list = [
        {
            "contents": get_story_file("note_woods"),
            "path": "~/bosque/nota",
            "permissions": 0o644,
            "type": "file"
        },
        {
            "contents": get_story_file("Conejo"),
            "path": "~/bosque/matorral/Conejo",
            "permissions": 0o644,
            "type": "file"
        },
        {
            "path": "~/bosque/matorral/madriguera",
            "permissions": 0o755,
            "type": "directory"
        },
        {
            "contents": get_story_file("note_swordsmaster-clearing"),
            "path": "~/bosque/claro/nota",
            "permissions": 0o644,
            "type": "file"
        },
        {
            "contents": get_story_file("note_rabbithole"),
            "path": "~/bosque/matorral/nota",
            "permissions": 0o644,
            "type": "file"
        }
    ]

    def block_command(self, line):
        unblock_cd_commands(line)

    def next(self):
        return 40, 2


class Step2(StepTemplateChmod):
    story = [
        "{{lb:Mira alrededor}} y busca pistas sobre adónde ir ahora."
    ]

    start_dir = "~/bosque/claro"
    end_dir = "~/bosque/claro"
    commands = [
        "ls",
        "ls -a"
    ]

    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]

    def next(self):
        return 40, 3


class Step3(StepTemplateChmod):
    story = [
        "¡Otra nota! ¿Qué dirá?"
    ]
    start_dir = "~/bosque/claro"
    end_dir = "~/bosque/claro"
    commands = [
        "cat nota"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cat nota}} {{rb:para leer la nota.}}"
    ]

    def next(self):
        return 40, 4


class Step4(StepTemplateChmod):
    story = [
        "Parece que deberíamos salir del claro.",
        "{{lb:Vuelve al bosque.}}"
    ]
    start_dir = "~/bosque/claro"
    end_dir = "~/bosque"

    hints = [
        "{{rb:Vuelve al bosque con}} {{yb:cd ../}}"
    ]

    def block_command(self, line):
        unblock_cd_commands(line)

    def next(self):
        return 40, 5


class Step5(StepTemplateChmod):
    story = [
        "{{lb:Mira alrededor.}}"
    ]
    start_dir = "~/bosque"
    end_dir = "~/bosque"
    commands = [
        "ls",
        "ls -a"
    ]

    # This text is used so much we can probably save it as "default ls hint"
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]

    def next(self):
        return 40, 6


class Step6(StepTemplateChmod):
    story = [
        "¡Hay otra nota! {{lb:Léela.}}"
    ]
    start_dir = "~/bosque"
    end_dir = "~/bosque"
    commands = [
        "cat nota"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cat nota}} {{rb:para examinar la nota.}}"
    ]

    def next(self):
        return 40, 7


class Step7(StepTemplateChmod):
    story = [
        "{{lb:Entremos}} en el matorral."
    ]
    start_dir = "~/bosque"
    end_dir = "~/bosque/matorral"
    hints = [
        "{{rb:Usa}} {{yb:cd matorral}} {{rb:para entrar en el matorral.}}"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 40, 8


class Step8(StepTemplateChmod):
    story = [
        "Te abres paso entre plantas muy tupidas. Los árboles te cubren con su sombra.",
        "{{lb:Mira alrededor.}}"
    ]
    start_dir = "~/bosque/matorral"
    end_dir = "~/bosque/matorral"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]

    def next(self):
        return 41, 1

