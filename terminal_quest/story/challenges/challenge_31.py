# challenge_31.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.sound import SoundManager
from terminal_quest.terminals import TerminalNano


class StepTemplateNano(StepTemplate):
    TerminalClass = TerminalNano


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateNano):
    story = [
        "Has llegado a la {{bb:tienda-de-cobertizos}}. {{lb:Mira alrededor.}}"
    ]
    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]

    def next(self):
        return 31, 2


class Step2(StepTemplateNano):
    story = [
        "Mmm, no ves a {{bb:Bernard}} por ningún lado.",

        "¿A dónde habrá ido?\n",

        "¿Tal vez está en el {{bb:sotano}}? {{lb:Vayamos}} ahí abajo."
    ]
    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este/tienda-de-cobertizos/sotano"
    hints = [
        "{{rb:Ve al sótano con}} {{yb:cd sotano}}"
    ]

    def check_command(self, line):
        if line == "cat Sombrero-de-Bernard":
            self.send_hint("\n¿Ese es el sombrero de Bernard? Qué raro que lo haya dejado...")
        else:
            return StepTemplateNano.check_command(self, line)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 31, 3


class Step3(StepTemplateNano):
    story = [
        "Bajas al sótano de {{bb:Bernard}}. {{lb:Mira alrededor.}}"
    ]
    start_dir = "~/pueblo/este/tienda-de-cobertizos/sotano"
    end_dir = "~/pueblo/este/tienda-de-cobertizos/sotano"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Mira alrededor con}} {{yb:ls}}{{rb:.}}"
    ]

    def _run_at_start(self):
        sound_manager = SoundManager()
        sound_manager.play_sound('steps')

    def next(self):
        return 31, 4


class Step4(StepTemplateNano):
    story = [
        "Ves lo que parece ser otro script y un par de diarios.",
        "",
        "¿Los {{lb:examinamos}}?"
    ]
    start_dir = "~/pueblo/este/tienda-de-cobertizos/sotano"
    end_dir = "~/pueblo/este/tienda-de-cobertizos/sotano"
    commands = [
        "cat diario-de-bernard-1",
        "cat diario-de-bernard-2",
        "cat fotocopiadora.sh"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cat}} {{rb:para examinar los objetos alrededor tuyo.}}"
    ]

    def check_command(self, line):
        if line in self.commands:
            self.commands.remove(line)

            if not self.commands:
                text = "\n{{gb:Presiona}} {{ob:Enter}} {{gb:para continuar.}}"
                self.send_hint(text)
            else:
                text = "\n{{gb:¡Bien hecho! Examina algún objeto más.}}"
                self.send_hint(text)

        elif not line and not self.commands:
            return True

        else:
            return StepTemplateNano.check_command(self, line)

    def next(self):
        return 32, 1
