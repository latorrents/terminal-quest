#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file
from terminal_quest.file_tree import modify_permissions
from terminal_quest.helpers import wrap_in_box
from terminal_quest.terminals import TerminalChmod
from terminal_quest.terminals import TerminalRm


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class StepTemplateRm(StepTemplate):
    TerminalClass = TerminalRm


REPLY_PRINT_TEXT = "{{yb:Un conejo vino y robó el comando delante de mí.}}"


class Step1(StepTemplateChmod):
    story = [
        "Estás solo en la biblioteca. El Conejo ha robado el comando.",
        "Crece la sensación de que algo terrible va a pasar. Entonces, el Espadachin entra corriendo en la sala.",
        "",
        "Espadachin: {{Bb:\"¿Qué has hecho?\"}}",
        "",
        "{{yb:1:}} " + REPLY_PRINT_TEXT,
        "{{yb:2: Nada.}}"
    ]
    start_dir = "~/pueblo/este/biblioteca/seccion-privada"
    end_dir = "~/pueblo/este/biblioteca/seccion-privada"
    file_list = [
        {
            "path": "~/pueblo/este/biblioteca/seccion-privada/Espadachin",
            "contents": get_story_file("swordmaster"),
            "permissions": 0o644,
            "type": "file"
        }
    ]
    commands = [
        "echo 1",
        "echo 2"
    ]
    hints = [
        "Espadachin: {{Bb:\"¡Habla con}} {{lb:echo}} {{Bb:y dímelo!\"}}"
    ]
    dark_theme = True

    def _run_at_start(self):
        modify_permissions("~/bosque/matorral/madriguera", 0o000)

    def next(self):
        if self._last_user_input == "echo 2":
            return 43, 100
        else:
            return 43, 2


class Step100(StepTemplateChmod):
    story = [
        "Espadachin: {{rb:\"¡BASTA!\"}}",
        "{{Bb:\"Dime}} {{rb:la verdad.\"}}",
        "{{Bb:\"Necesitas mi ayuda para arreglar esto....\"}}",
        "",
        "{{yb:1:}} " + REPLY_PRINT_TEXT,
        "{{yb:2: Nada.}}"
    ]
    commands = [
        "echo 1"
    ]
    start_dir = "~/pueblo/este/biblioteca/seccion-privada"
    end_dir = "~/pueblo/este/biblioteca/seccion-privada"

    hints = [
        "{{rb:Dile la verdad al Espadachin usando}} {{yb:echo 1}}"
    ]
    dark_theme = True

    def check_command(self, last_user_input):
        if last_user_input == "echo 2":
            self.send_hint(
                "Espadachin: {{Bb:\"Los dos sabemos que eso no es verdad....\"}}"
            )
            return
        return StepTemplateChmod.check_command(self, last_user_input)

    def next(self):
        return 43, 2


class Step2(StepTemplateChmod):
    print_text = [REPLY_PRINT_TEXT]
    story = [
        "Espadachin: {{Bb:\"¿Un Conejo? A decir verdad, a menudo veo un conejo blanco en un matorral cerca de mi casa.\"}}",
        "{{Bb:\"Pero siempre pareció tan inocente, nunca me hubiera imaginado que pudiera hacer algo así.\"}}",
        "{{Bb:\"¿Qué habrá cambiado? Quizás...mmm...la campana...\"}}",
        "{{Bb:\"Debemos eliminar el origen del problema. Te enseñaré cómo.\"}}",
        "",
        "{{pb:Din. Don.}}",
        "",
        "Oíste una campana. {{lb:Mira alrededor.}}"
    ]
    start_dir = "~/pueblo/este/biblioteca/seccion-privada"
    end_dir = "~/pueblo/este/biblioteca/seccion-privada"
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]
    hints = [
        "{{rb:Mira alrededor con}} {{yb:ls}}"
    ]
    file_list = [
        {
            "path": "~/pueblo/este/biblioteca/seccion-privada/espada",
            "contents": get_story_file("RM-sword"),
            "type": "file",
            "permissions": 0o644
        }
    ]
    dark_theme = True

    deleted_items = ["~/pueblo/este/biblioteca/seccion-privada/Espadachin"]

    def next(self):
        return 43, 3


class Step3(StepTemplateChmod):
    story = [
        "El Espadachin se ha ido.",
        "",
        "Dejó algo atrás. Parece la {{lb:espada}} que siempre lleva consigo.",
        "{{lb:Examínala}}."
    ]
    start_dir = "~/pueblo/este/biblioteca/seccion-privada"
    end_dir = "~/pueblo/este/biblioteca/seccion-privada"
    commands = [
        "cat espada"
    ]
    dark_theme = True

    hints = [
        "{{rb:Usa}} {{yb:cat espada}} {{rb:para examinarla.}}"
    ]

    def next(self):
        return 43, 4


class Step4(StepTemplateRm):
    story = [
        "Tiene un comando grabado.",
        "....{{lb:rm}}...?\n"
    ]

    story += wrap_in_box([
        "{{gb:Nuevo Poder:}} Usa {{yb:rm}} para",
        " {{lb:eliminar un objeto}}."
    ])

    story += [
        "Usa {{yb:rm nota}} para probar el comando con la nota.",
        "Pero ten cuidado....parece peligroso."
    ]
    start_dir = "~/pueblo/este/biblioteca/seccion-privada"
    end_dir = "~/pueblo/este/biblioteca/seccion-privada"
    commands = [
        "rm nota"
    ]
    highlighted_commands = ["rm"]

    hints = [
        "",
        "{{rb:Usa el comando}} {{yb:rm nota}}"
    ]
    dark_theme = True

    def next(self):
        return 43, 5


class Step5(StepTemplateRm):
    story = [
        "{{lb:Mira alrededor.}}"
    ]
    start_dir = "~/pueblo/este/biblioteca/seccion-privada"
    end_dir = "~/pueblo/este/biblioteca/seccion-privada"
    commands = [
        "ls"
    ]

    hints = [
        "{{rb:Usa el comando}} {{yb:ls}}"
    ]
    dark_theme = True

    def next(self):
        return 44, 1
