# challenge_12.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


# Change this import statement, need to decide how to group the terminals
# together
import os
from terminal_quest.step import StepTemplate
from terminal_quest.terminals import TerminalMv
from terminal_quest.common import tq_file_system
from terminal_quest.step_helpers import unblock_commands


class StepTemplateMv(StepTemplate):
    TerminalClass = TerminalMv


# ----------------------------------------------------------------------------------------


# Thanks you for saving the little girl
class Step1(StepTemplateMv):
    story = [
        "{{wb:Edith:}} {{Bb:\"¡Gracias por salvarla!\"}}",
        "{{wb:Eleanor:}} {{Bb:\"¡Perrito!\"}}",
        (
            "{{wb:Edith:}} {{Bb:\"¿Puedes salvar a su perro también? Me preocupa que algo malo "
            "le suceda si se queda afuera.\"}}\n"
        )
    ]
    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "mv ../perro .",
        "mv ../perro ./",
        "mv ~/pueblo/perro ~/pueblo/.refugio-oculto",
        "mv ~/pueblo/perro ~/pueblo/.refugio-oculto/",
        "mv ~/pueblo/perro .",
        "mv ~/pueblo/perro ./",
        "mv ../perro ~/pueblo/.refugio-oculto",
        "mv ../perro ~/pueblo/.refugio-oculto/",
    ]
    hints = [
        "{{rb:Usa el comando}} {{yb:mv ../perro ./}} {{rb:para rescatar al perro.}}"
    ]
    dog_file = os.path.join(tq_file_system, 'pueblo/.refugio-oculto/perro')

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 12, 2


# Save both the dog and the little girl
class Step2(StepTemplateMv):
    story = [
        "{{wb:Eleanor:}} {{Bb:\"¡Yay, Perrito!\"}}",
        "{{wb:Perro:}} {{Bb:\"¡Ruff!\"}}",
        "{{wb:Edith:}} {{Bb:\"Muchas gracias por hacer que vuelvan.",
        "Me equivoqué contigo. ¡Eres un héroe!\"}}\n",
        "{{lb:Escucha a todos}} y fíjate si hay algo más que puedas hacer para ayudarlos.\n"
    ]
    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = "cat Edward"
    all_commands = {
        "cat Edith": "\n{{wb:Edith:}} {{Bb:\"¡Muchas gracias! Eleanor, ¡no vuelvas a salir - me has asustado!\"}}",

        "cat Eleanor": "\n{{wb:Eleanor:}} {{Bb:\"¿Dónde piensas que se habrá llevado la campana a los demás?\"}}",

        "cat perro": "\n{{wb:Perro:}} {{Bb:\"¡Guau! ¡Guau Guau!\"}}"
    }
    hints = [
        "{{gb:Parece que Edward tiene algo para decir. Escucha a Edward con}} {{yb:cat Edward}}"
    ]

    def check_command(self, line):
        line = line.strip()
        if line in self.all_commands.keys():
            hint = self.all_commands[line]
            self.send_hint(hint)
            return
        return StepTemplateMv.check_command(self, line)

    def next(self):
        return 13, 1
