#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import time
from threading import Thread

from terminal_quest.animation import Animation
from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.terminals import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        "Ahora, ¿cuál es el cuarto cerrado? {{lb:Mira alrededor}} para recordarlo."
    ]
    start_dir = "~/pueblo/este/biblioteca"
    end_dir = "~/pueblo/este/biblioteca"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]
    file_list = [
        {
            "path": "~/pueblo/este/biblioteca/Conejo",
            "contents": get_story_file("Conejo"),
            "permissions": 0o644,
            "type": "file"
        }
    ]
    deleted_items = [
        "~/bosque/matorral/Conejo",
        "~/bosque/matorral/nota"
    ]

    def next(self):
        return 42, 2


class Step2(StepTemplateChmod):
    story = [
        "Ah, es la {{lb:seccion-privada}}.",
        "El Conejo se ve muy emocionado. Le brillan los ojos.",
        "",
        "Desbloquea la {{lb:seccion-privada}}."
    ]
    start_dir = "~/pueblo/este/biblioteca"
    end_dir = "~/pueblo/este/biblioteca"
    commands = [
        "chmod +rwx seccion-privada",
        "chmod +rwx seccion-privada/",
        "chmod +wxr seccion-privada",
        "chmod +wxr seccion-privada/",
        "chmod +xrw seccion-privada",
        "chmod +xrw seccion-privada/",
        "chmod +rxw seccion-privada",
        "chmod +rxw seccion-privada/",
        "chmod +xwr seccion-privada",
        "chmod +xwr seccion-privada/",
        "chmod +wxr seccion-privada",
        "chmod +wxr seccion-privada/"
    ]

    hints = [
        "{{rb:El comando es}} {{yb:chmod +rwx seccion-privada}} {{rb:para "
        "activar todos los permisos.}}"
    ]

    def next(self):
        return 42, 3


class Step3(StepTemplateChmod):
    story = [
        "¡Genial, la desbloqueaste! {{lb:Entra en la seccion-privada.}}"
    ]
    start_dir = "~/pueblo/este/biblioteca"
    end_dir = "~/pueblo/este/biblioteca/seccion-privada"
    hints = [
        "{{rb:Usa}} {{yb:cd seccion-privada/}} {{rb:para entrar.}}"
    ]
    file_list = [
        {
            "path": "~/pueblo/este/biblioteca/seccion-privada/cofre/pergamino",
            "contents": get_story_file("pergamino"),
            "permissions": 0o644,
            "type": "file"
        },
        {
            "path": "~/pueblo/este/biblioteca/seccion-privada/cofre/nota-rota",
            "contents": get_story_file("nota-rota"),
            "permissions": 0o644,
            "type": "file"
        }
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 42, 4


class Step4(StepTemplateChmod):
    story = [
        "{{lb:Mira alrededor.}}"
    ]
    start_dir = "~/pueblo/este/biblioteca/seccion-privada"
    end_dir = "~/pueblo/este/biblioteca/seccion-privada"
    commands = [
        "ls",
        "ls -a",
        "cat cofre/pergamino",
        "cat cofre/nota-rota",
        "ls cofre",
        "ls cofre/",
        "ls cofre/pergamino",
        "ls cofre/nota-rota"
    ]
    file_list = [
        {
            "path": "~/pueblo/este/biblioteca/seccion-privada/Conejo",
            "contents": get_story_file("Conejo"),
            "permissions": 0o644,
            "type": "file"
        }
    ]
    deleted_items = ["~/pueblo/este/biblioteca/Conejo"]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]

    def block_command(self, line):
        if line == "cat cofre/pergamino":
            self.set_last_user_input(line)
            print("¡El Conejo te arrebató el cofre!")
            return True
        return StepTemplateChmod.block_command(self, line)

    def check_command(self, line):
        if self.get_last_user_input() == "cat cofre/pergamino":
            return True
        return StepTemplateChmod.check_command(self, line)

    def next(self):
        if self.get_last_user_input() == "cat cofre/pergamino":
            return 42, 5
        else:
            return 42, 6


class RabbitTakesChest(StepTemplateChmod):

    start_dir = "~/pueblo/este/biblioteca/seccion-privada"
    end_dir = "~/pueblo/este/biblioteca/seccion-privada"
    deleted_items = [
        "~/pueblo/este/biblioteca/seccion-privada/Conejo",
        "~/pueblo/este/biblioteca/seccion-privada/cofre"
    ]

    def next(self):
        return 42, 7


class Step5(RabbitTakesChest):
    story = [
        "Intentas examinar el contenido del cofre, ¡pero el Conejo te lo arrebata y sale corriendo!"
    ]


class Step6(RabbitTakesChest):
    story = [
        "Ves un {{bb:cofre}}.",
        "Parece que podría contener los poderes que necesitamos.",
        "La emoción del Conejo crece, salta de arriba abajo. ¡De pronto te arrebata el cofre y sale corriendo!",
        "",
        "Presiona Enter para verlo huir."
    ]


class Step7(StepTemplateChmod):
    story = [
        "Una {{bb:nota}} revolotea por el aire. La atrapas. {{lb:Léela}}."
    ]

    start_dir = "~/pueblo/este/biblioteca/seccion-privada"
    end_dir = "~/pueblo/este/biblioteca/seccion-privada"

    commands = [
        "cat nota"
    ]

    hints = [
        "{{rb:Lee la nota con}} {{yb:cat nota}}"
    ]

    file_list = [
        {
            "contents": get_story_file("note_private-section"),
            "path": "~/pueblo/este/biblioteca/seccion-privada/nota"
        }
    ]

    def _run_at_start(self):
        Animation("rabbit-animation").play_across_screen(speed=10)

    def next(self):
        return 42, 8


class Step8(StepTemplateChmod):
    story = [
        "El mundo se estremece... todo se vuelve rojo oscuro",
        "",
        "{{gb:Presiona Enter para continuar.}}"
    ]

    start_dir = "~/pueblo/este/biblioteca/seccion-privada"
    end_dir = "~/pueblo/este/biblioteca/seccion-privada"

    def _run_at_start(self):
        t = Thread(target=self.__timeout_dark_theme)
        t.start()

    def __timeout_dark_theme(self):
        time.sleep(1)
        self.send_dark_theme()

    def next(self):
        return 43, 1

