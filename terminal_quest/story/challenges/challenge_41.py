#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.terminals import TerminalChmod
from terminal_quest.step_helpers import unblock_cd_commands


GO_TO_THE_LIBRARY = [
    "¿El Conejo quiere saber dónde se guarda el comando de Super Usuario?",
    "....",
    "Vamos a la {{bb:~/pueblo/este/biblioteca}}.",
    "Parece que el Conejo te seguirá."
]

RABBITS_ARE_QUIET = [
    "Conejo: {{Bb:...}}",
    "",
    "Parece que el Conejo no habla mucho.",
    "Eso es bastante normal en los conejos."
]

RABBIT_BLOCKING_RABBITHOLE = "El Conejo está delante de la madriguera y no te deja pasar."


class TerminalRabbit(TerminalChmod):
    def _autocomplete_files(self, text, line, begidx, endidx, only_dirs=False, only_exe=False):
        completions = TerminalChmod._autocomplete_files(self, text, line, begidx, endidx, only_dirs, only_exe)
        if "jaula/" in completions or "Mama" in completions:
            print("\n" + RABBIT_BLOCKING_RABBITHOLE)
            return []
        else:
            return completions


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod

    def block_command(self, line):
        if "madriguera" in line and ("ls" in line or "cat" in line):
            print(RABBIT_BLOCKING_RABBITHOLE)
            return True
        else:
            return StepTemplate.block_command(self, line)


# Same as the towns people, and the last challenge?
class Step1(StepTemplateChmod):
    story = [
        "Ves un Conejo, un trozo de papel y una madriguera.",
        "Este Conejo te resulta algo conocido...",
        "{{lb:Escucha}} al Conejo."
    ]
    start_dir = "~/bosque/matorral"
    end_dir = "~/bosque/matorral"
    hints = [
        "{{rb:Usa}} {{yb:cat Conejo}} {{rb:para escuchar al Conejo.}}"
    ]

    read_note = False
    commands = [
        "cat Conejo"
    ]

    def check_command(self, line):
        if line == "cat nota":
            self.read_note = True

        return StepTemplateChmod.check_command(self, line)

    def next(self):
        if self.read_note:
            return 41, 4
        else:
            return 41, 2


class Step2(StepTemplateChmod):
    story = RABBITS_ARE_QUIET + ["", "{{lb:Examina}} la nota."]
    start_dir = "~/bosque/matorral"
    end_dir = "~/bosque/matorral"
    commands = [
        "cat nota"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cat nota}} {{rb:para examinar la nota.}}"
    ]

    def next(self):
        return 41, 3


class Step3(StepTemplateChmod):
    story = GO_TO_THE_LIBRARY
    start_dir = "~/bosque/matorral"
    end_dir = "~/pueblo/este/biblioteca"
    hints = [
        "{{rb:Usa}} {{yb:cd ~/pueblo/este/biblioteca}} {{rb:para ir a la biblioteca.}}"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 42, 1


class Step4(StepTemplateChmod):
    story = RABBITS_ARE_QUIET + [""] + GO_TO_THE_LIBRARY
    start_dir = "~/bosque/matorral"
    end_dir = "~/pueblo/este/biblioteca"
    hints = [
        "{{rb:¿Será el mismo lugar del que habló el Espadachin?}}",
        "{{rb:Usa}} {{yb:cd ~/pueblo/este/biblioteca}} {{rb:para ir a la biblioteca.}}"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 42, 1
