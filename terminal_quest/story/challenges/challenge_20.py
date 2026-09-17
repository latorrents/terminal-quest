# challenge_20.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file
from terminal_quest.terminals import TerminalEcho
from terminal_quest.terminals import TerminalMkdir
from terminal_quest.step_helpers import unblock_commands_with_mkdir_hint, unblock_cd_commands
from terminal_quest.helpers import wrap_in_box


class StepTemplateEcho(StepTemplate):
    TerminalClass = TerminalEcho


class StepTemplateMkdir(StepTemplate):
    TerminalClass = TerminalMkdir


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateEcho):
    print_text = [
        "{{yb:\"Algunas personas sobrevivieron escondiéndose\"}}"
    ]
    story = [
        (
            "Ruth: {{Bb:\"¡Oh! Eso me recuerda que mi marido solía construir refugios "
            "especiales para guardar granos durante el invierno. Creo que usaba una "
            "herramienta especial. Deberíamos buscar dentro del taller para "
            "encontrarla.\"}}"
        ),
        "\nUsa el comando {{lb:cd}} para ir al {{bb:taller}}.\n"
    ]

    start_dir = "~/granja/granero"
    end_dir = "~/granja/taller"
    hints = [
        "{{rb:Ve al taller en un solo paso usando}} {{yb:cd ../taller}}"
    ]

    path_hints = {
        "~/granja/granero": {
            "blocked": "\n{{rb:Usa}} {{yb:cd ..}} {{rb:para volver.}}"
        },
        "~/granja": {
            "not_blocked": "\n{{gb:Saliste, ahora ve al}} {{bb:taller}}{{gb:.}}",
            "blocked": "\n{{rb:Usa}} {{yb:cd taller}} {{rb:para ir a ver las herramientas.}}"
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
        return 20, 2


class Step2(StepTemplateEcho):
    story = [
        "{{bb:Ruth}} te sigue al {{bb:taller}}. Es muy grande y tiene muchas herramientas.\n",
        "Ruth: {{Bb:\"Vamos a}} {{lb:mirar alrededor}} {{Bb:para buscar algo que podría ser útil.\"}}\n"
    ]
    start_dir = "~/granja/taller"
    end_dir = "~/granja/taller"
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]
    commands = [
        "ls",
        "ls -a",
        "ls .",
        "ls ./",
        "ls -a .",
        "ls -a ./"
    ]
    # Move Ruth into toolshed
    file_list = [
        {
            "path": "~/granja/taller/Ruth",
            "contents": get_story_file("Ruth"),
            "type": "file"
        }
    ]
    deleted_items = ["~/granja/granero/Ruth"]

    def next(self):
        return 20, 3


class Step3(StepTemplateEcho):
    story = [
        "Ruth: {{Bb:\"¡Ah, mira! Hay unas instrucciones con la palabra}} {{bb:MKDIR}}{{Bb:.\"}}",
        "{{Bb:\"¿Qué dicen?\"}}",
        "",
        "{{lb:Examina}} las instrucciones de {{bb:MKDIR}}."
    ]
    hints = [
        (
            "Ruth: {{Bb:\"...sabes leer, ¿verdad? Usa}} {{yb:cat}} {{Bb:para "
            "leer cosas.\"}}"
        ),
        "Ruth: {{Bb:\"Qué les enseñan hoy en día a los niños en la escuela...\"}}",
        "{{Bb:\"Solo usa}} {{yb:cat MKDIR}} {{Bb:para leer el papel.\"}}",
        "{{rb:Usa}} {{yb:cat MKDIR}} {{rb:para leerlo.}}"
    ]
    start_dir = "~/granja/taller"
    end_dir = "~/granja/taller"
    commands = [
        "cat MKDIR"
    ]

    def next(self):
        return 20, 4


class Step4(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:\"¿Aquí dice que puedes construir algo usando la palabra}} {{yb:mkdir}}{{Bb:?\"}}",
        "\nIntenta construir un iglú usando {{yb:mkdir iglu}}\n ",
    ]

    story += wrap_in_box([
        "{{gb:Nuevo Poder}}: {{yb:mkdir}} seguido de una palabra",
        "te permite {{lb:construir}} un refugio",
    ])

    hints = [
        "{{rb:Construye un iglú usando}} {{yb:mkdir iglu}}\n"
    ]
    start_dir = "~/granja/taller"
    end_dir = "~/granja/taller"
    commands = [
        "mkdir iglu"
    ]
    highlighted_commands = ['mkdir']

    def block_command(self, line):
        return unblock_commands_with_mkdir_hint(line, self.commands)

    def check_command(self, line):
        if line == "cat MKDIR":
            self.send_hint("\n{{gb:¡Bien hecho!}}")
            return False

        return StepTemplateMkdir.check_command(self, line)

    def next(self):
        return 20, 5


class Step5(StepTemplateMkdir):
    story = [
        "Ahora {{lb:mira alrededor}} para ver qué cambió."
    ]
    start_dir = "~/granja/taller"
    end_dir = "~/granja/taller"
    commands = [
        "ls",
        "ls -a",
        "ls .",
        "ls ./"
    ]
    hints = [
        "{{rb:Mira alrededor usando}} {{yb:ls}}{{rb:.}}"
    ]

    def next(self):
        return 21, 1
