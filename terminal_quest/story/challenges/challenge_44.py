#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.location import generate_real_path
from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file
from terminal_quest.file_tree import modify_permissions
from terminal_quest.helpers import has_write_permissions, has_read_permissions, has_execute_permissions
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.terminals import TerminalRm


class StepTemplateRm(StepTemplate):
    TerminalClass = TerminalRm


class Step1(StepTemplateRm):
    story = [
        "¡Guau! Destruiste la nota.",
        "",
        "Es hora de encontrar a ese conejo y ponerle fin a esta locura.",
        "{{lb:Ve al lugar donde conociste al conejo.}}"
    ]
    start_dir = "~/pueblo/este/biblioteca/seccion-privada"
    end_dir = "~/bosque/matorral"

    hints = [
        "",
        "{{lb:Conociste al conejo en el}} {{bb:~/bosque/matorral}}",
        "{{rb:Usa}} {{yb:cd ~/bosque/matorral}}"
    ]
    dark_theme = True

    file_list = [
        {
            "path": "~/pueblo/este/biblioteca/madriguera/Espadachin",
            "contents": get_story_file("swordmaster"),
            "permissions": 0o644,
            "type": "file"
        }
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 44, 2


class Step2(StepTemplateRm):
    story = [
        "{{lb:Mira alrededor.}}"
    ]
    start_dir = "~/bosque/matorral"
    end_dir = "~/bosque/matorral"
    commands = [
        "ls",
        "ls .",
        "ls ./",
        "ls -a",
        "ls -a .",
        "ls -a ./"
    ]

    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]
    dark_theme = True

    def next(self):
        return 44, 3


class Step3(StepTemplateRm):
    story = [
        "Estás afuera de la madriguera. Tiene una gran roca delante.",
        "Intenta {{lb:entrar.}}"
    ]
    start_dir = "~/bosque/matorral"
    end_dir = "~/bosque/matorral"
    dirs_to_attempt = "~/bosque/matorral/madriguera"

    commands = [
        "cd madriguera",
        "cd madriguera/"
    ]

    hints = [
        "{{rb:Usa}} {{yb:cd madriguera}} {{rb:para entrar en la madriguera.}}"
    ]
    dark_theme = True

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 44, 4


class Step4(StepTemplateRm):
    story = [
        "No puedes pasar la roca.",
        "La {{bb:madriguera}} está completamente bloqueada.",
        "",
        "{{lb:Desbloquéala.}}",
        "Usa el mismo comando que usaste para desbloquear la {{bb:seccion-privada}}."
    ]
    start_dir = "~/bosque/matorral"
    end_dir = "~/bosque/matorral"

    hints = [
        "{{rb:Usa}} {{yb:chmod +rwx madriguera/}}"
    ]
    dark_theme = True

    def check_command(self, line):
        dir = generate_real_path("~/bosque/matorral/madriguera")
        if has_write_permissions(dir) and has_read_permissions(dir) and has_execute_permissions(dir):
            return True
        self.send_stored_hint()

    def next(self):
        return 44, 5


class Step5(StepTemplateRm):
    story = [
        "Empujas la roca. Con algo de esfuerzo, se mueve lentamente a un lado. Sale luz por la grieta.",
        "{{lb:Entra en la}} {{bb:madriguera}}{{lb:.}}"
    ]
    start_dir = "~/bosque/matorral"
    end_dir = "~/bosque/matorral/madriguera"

    commands = [
        "cd madriguera",
        "cd madriguera/"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cd madriguera}} {{rb:para entrar en la madriguera.}}"
    ]
    dark_theme = True

    file_list = [
        {
            "path": "~/bosque/matorral/madriguera/campana",
            "type": "file",
            "contents": get_story_file("campana"),
            "permissions": 0o644
        },
        {
            "path": "~/bosque/matorral/madriguera/Conejo",
            "type": "file",
            "contents": get_story_file("Conejo"),
            "permissions": 0o644
        },
        {
            "path": "~/bosque/matorral/madriguera/jaula/Mama",
            "type": "file",
            "contents": get_story_file("Mama"),
            "permissions": 0o644
        },
        {
            "path": "~/bosque/matorral/madriguera/jaula/Papa",
            "type": "file",
            "contents": get_story_file("Papa"),
            "permissions": 0o644
        },
        {
            "path": "~/bosque/matorral/madriguera/jaula/perro",
            "type": "file",
            "contents": get_story_file("perro"),
            "permissions": 0o644
        },
        {
            "path": "~/bosque/matorral/madriguera/jaula/Edith",
            "type": "file",
            "contents": get_story_file("Edith"),
            "permissions": 0o644
        },
        {
            "path": "~/bosque/matorral/madriguera/jaula/Edward",
            "type": "file",
            "contents": get_story_file("Edward"),
            "permissions": 0o644
        },
        {
            "path": "~/bosque/matorral/madriguera/jaula/hombre-enojado",
            "type": "file",
            "contents": get_story_file("grumpy-man-fixed"),
            "permissions": 0o644
        },
        {
            "path": "~/bosque/matorral/madriguera/jaula/Alcalde",
            "type": "file",
            "contents": get_story_file("Alcalde"),
            "permissions": 0o644
        },
        {
            "path": "~/bosque/matorral/madriguera/jaula/chica",
            "type": "file",
            "contents": get_story_file("chica"),
            "permissions": 0o644
        },
        {
            "path": "~/bosque/matorral/madriguera/jaula/chico",
            "type": "file",
            "contents": get_story_file("chico"),
            "permissions": 0o644
        },
        {
            "path": "~/bosque/matorral/madriguera/jaula/Espadachin",
            "contents": get_story_file("swordmaster-without-sword"),
            "type": "file",
            "permissions": 0o644
        },
        {
            "path": "~/bosque/matorral/madriguera/jaula/Bernard",
            "contents": get_story_file("Bernard")
        },
        {
            "path": "~/bosque/matorral/madriguera/cofre/nota-rota",
            "contents": get_story_file("nota-rota")
        },
        {
            "path": "~/bosque/matorral/madriguera/cofre/pergamino",
            "contents": get_story_file("pergamino")
        }
    ]

    def _run_after_text(self):
        modify_permissions("~/bosque/matorral/madriguera/jaula", 0o500)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 45, 1
