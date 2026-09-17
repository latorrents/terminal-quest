#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.terminals import TerminalNano


class StepTemplateNano(StepTemplate):
    TerminalClass = TerminalNano


class Step1(StepTemplateNano):
    story = [
        "Basta de dar vueltas. Es hora de encontrar al Espadachin.",
        "Clara dijo que estaba en el bosque justo al lado de la {{lb:Carretera Ventosa}} {{yb:~}}.",
        "Usa {{yb:cd}} para ir allí ahora."
    ]
    start_dir = "~/pueblo/este/tienda-de-cobertizos/sotano"
    end_dir = "~"
    hints = [
        "{{rb:Usa}} {{yb:cd}} {{rb:solo para volver a la Carretera Ventosa ~}}"
    ]

    file_list = [
        {
            "path": "~/bosque/claro/casa",
            "permissions": 0o000,
            "type": "directory"
        },
        {
            "path": "~/bosque/claro/cartel",
            "permissions": 0o644,
            "type": "file",
            "contents": get_story_file("cartel")
        },
        {
            "path": "~/bosque/claro/casa/Espadachin",
            "contents": get_story_file("swordmaster")
        }
    ]

    # Maybe this could be reduced to an argument in the class.
    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 32, 2


class Step2(StepTemplateNano):
    story = [
        "{{lb:Mira alrededor}} para ver dónde está el bosque."
    ]
    start_dir = "~"
    end_dir = "~"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Mira alrededor usando}} {{yb:ls}}"
    ]

    def next(self):
        return 32, 3


class Step3(StepTemplateNano):
    story = [
        "Ves el {{bb:bosque}} a lo lejos, un montón de árboles oscuros e inhóspitos.",
        "{{lb:Entra al bosque}}."
    ]
    start_dir = "~"
    end_dir = "~/bosque"
    hints = [
        "{{rb:Usa}} {{yb:cd bosque/}} {{rb:para ir al bosque.}}"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 32, 4


# Should they use ls -a to find something hidden?
class Step4(StepTemplateNano):
    story = [
        "{{lb:Mira alrededor}} para ver a dónde ir ahora."
    ]
    start_dir = "~/bosque"
    end_dir = "~/bosque"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Mira alrededor usando}} {{yb:ls}}"
    ]

    def next(self):
        return 32, 5


class Step5(StepTemplateNano):
    story = [
        "Ves un {{bb:claro}} que te recuerda a un jardín.",
        "{{lb:Entra al}} {{bb:claro}}{{lb:.}}"
    ]
    start_dir = "~/bosque"
    end_dir = "~/bosque/claro"
    commands = [
        "cd claro/",
        "cd claro"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cd claro/}} {{rb:para entrar al claro.}}"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 33, 1



