# challenge_30.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os

from terminal_quest.common import get_story_file
from terminal_quest.story.challenges.CompanionMisc import StepTemplateEleanorBernard
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.terminals import TerminalNano


# ----------------------------------------------------------------------------------------


class StepNano(StepTemplateEleanorBernard):
    TerminalClass = TerminalNano


class Step1(StepNano):
    story = [
        "{{pb:Ding. Dong.}}\n",
        "\nEleanor: {{Bb:\"¿...qué fue eso?\"}}\n",
        "{{lb:Mira alrededor.}}"
    ]
    start_dir = "~/pueblo/este/restaurante/.bodega"
    end_dir = "~/pueblo/este/restaurante/.bodega"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para asegurarte de que estén todos presentes.}}"
    ]
    deleted_items = [
        "~/pueblo/este/tienda-de-cobertizos/Bernard"
    ]
    file_list = [
        {
            "path": "~/pueblo/este/tienda-de-cobertizos/Sombrero-de-Bernard",
            "contents": get_story_file("bernards-hat")
        }
    ]
    companion_speech = "Eleanor: {{Bb:......}}"

    def next(self):
        return 30, 2


class Step2(StepNano):
    story = [
        "Todos parecen estar aquí. ¿Qué fue ese timbre?",
        "\nParece que {{bb:Clara}} tiene algo para decir. {{lb:Escúchala.}}"
    ]
    commands = [
        "cat Clara"
    ]
    start_dir = "~/pueblo/este/restaurante/.bodega"
    end_dir = "~/pueblo/este/restaurante/.bodega"
    hints = [
        "{{rb:Usa}} {{yb:cat Clara}} {{rb:para escuchar lo que Clara tiene para decir.}}"
    ]
    companion_speech = \
        "Eleanor: {{Bb:\"....Tuve tanto miedo. No quiero salir ahora.\"}}"

    def next(self):
        return 30, 3


class Step3(StepNano):
    story = [
        "Clara: {{Bb:\"¿Van a volver a salir?\"}}",
        (
            "{{Bb:\"}}{{gb:%s}}{{Bb:, parece que sabes cuidarte solo, pero no estoy "
            "tranquila si Eleanor sale.\"}}"
        )\
        % os.environ['LOGNAME'],
        "\n{{Bb:\"}}{{gb:%s}}{{Bb:, ¿dejarías a Eleanor conmigo? Yo la cuidaré.\"}}" % os.environ['LOGNAME'],
        "\n{{yb:1: \"Es una buena idea, cuídala muy bien.\"}}",
        "{{yb:2: \"No, no confío en ti, ella estará más segura conmigo.\"}}",
        "{{yb:3: \"(Pregunta a Eleanor.) ¿Quieres quedarte aquí?\"}}",
        # "{{yb:4: ¿Tienes suficiente comida aquí?}}",
        "\n{{lb:Respóndele a Clara.}}"
    ]
    commands = [
        "echo 1"
    ]
    start_dir = "~/pueblo/este/restaurante/.bodega"
    end_dir = "~/pueblo/este/restaurante/.bodega"
    hints = [
        (
            "{{rb:Usa}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:o}} {{yb:echo 3}} {{rb:para "
            "responderle a Clara.}}"
        )
    ]
    companion_speech = (
        "Eleanor: {{Bb:\"Estaré bien aquí. Me agrada Clara.\"}}"
    )

    def check_command(self, line):
        if line == "echo 2":
            text = (
                (
                    "\nClara: {{Bb:\"Por favor, déjame cuidarla. No creo que sea seguro para ella "
                    "volver a salir.\"}}"
                )
            )
            self.send_hint(text)
        elif line == "echo 3":
            text = "\nEleanor: {{Bb:\"Estaré bien aquí. Me agrada Clara.\"}}"
            self.send_hint(text)
        else:
            return StepNano.check_command(self, line)

    def next(self):
        return 30, 4


class Step4(StepNano):
    story = [
        "Clara: {{Bb:\"¡Gracias!\"}}",
        "Eleanor: {{Bb:\"Cuando encuentres a mis padres, ¿puedes decirles que estoy aquí?\"}}",
        "Clara: {{Bb:\"¿A dónde irás ahora?\"}}",
        (
            "\nVolvamos a ver a {{bb:Bernard}} para saber si ha oído hablar del "
            "{{bb:espadachín enmascarado}}.\n"
        ),
        "{{lb:Dirígete a la}} {{bb:tienda-de-cobertizos}}."
    ]
    start_dir = "~/pueblo/este/restaurante/.bodega"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"

    path_hints = {
        "~/pueblo/este/restaurante/.bodega": {
            "blocked": "\n{{rb:Usa}} {{yb:cd ../}} {{rb:para salir.}}"
        },
        "~/pueblo/este/restaurante": {
            "not_blocked": "\n{{gb:Subiste un nivel. Sigue saliendo.}}",
            "blocked": "\n{{rb:Usa}} {{yb:cd ../}} {{rb:para salir.}}"
        },
        "~/pueblo/este": {
            "not_blocked": "\n{{gb:Ahora dirígete a la}} {{bb:tienda-de-cobertizos}}{{gb:.}}",
            "blocked": "\n{{rb:Usa}} {{yb:cd tienda-de-cobertizos/}}{{rb:.}}"
        }
    }

    def check_command(self, line):
        if self.get_fake_path() == self.end_dir:
            return True
        elif "cd" in line and not self.get_command_blocked():
            hint = self.path_hints[self.get_fake_path()]["not_blocked"]
        else:
            hint = self.path_hints[self.get_fake_path()]["blocked"]

        self.send_hint(hint)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 31, 1
