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
        "Estás en un claro. {{lb:Mira alrededor.}}",
    ]
    start_dir = "~/bosque/claro"
    end_dir = "~/bosque/claro"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Mira alrededor del claro con}} {{yb:ls}}"
    ]

    file_list = [
        {
            "path": "~/bosque/cueva/letrero",
            "permissions": 0o644,
            "type": "file",
            "contents": get_story_file("sign_cave")
        },

        {
            "path": "~/bosque/cueva/cuarto-oscuro",
            "permissions": 0o300,
            "type": "directory"
        },
        {
            "path": "~/bosque/cueva/cuarto-oscuro/letrero",
            "permissions": 0o644,
            "type": "file",
            "contents": get_story_file("x-sign")
        },

        {
            "path": "~/bosque/cueva/jaula",
            "permissions": 0o500,
            "type": "directory"
        },
        {
            "path": "~/bosque/cueva/jaula/pajaro",
            "permissions": 0o644,
            "type": "file",
            "contents": get_story_file("pajaro")
        },
        {
            "path": "~/bosque/cueva/jaula/letrero",
            "permissions": 0o644,
            "type": "file",
            "contents": get_story_file("r-sign")
        },

        {
            "path": "~/bosque/cueva/cuarto-cerrado/",
            "permissions": 0o600,
            "type": "directory"
        },
        {
            "path": "~/bosque/cueva/cuarto-cerrado/encendedor",
            "permissions": 0o644,
            "type": "file",
            "contents": get_story_file("encendedor")
        },
        {
            "path": "~/bosque/cueva/cuarto-cerrado/letrero",
            "permissions": 0o644,
            "type": "file",
            "contents": get_story_file("w-sign"),
        }
    ]

    def next(self):
        return 33, 2


class Step2(StepTemplateNano):
    story = [
        "Hay una casa en el claro. {{lb:Mira}} dentro de la {{lb:casa}}, o intenta {{lb:entrar}}.",
    ]
    start_dir = "~/bosque/claro"
    end_dir = "~/bosque/claro"
    dirs_to_attempt = "~/bosque/claro/casa"
    commands = [
        "ls casa",
        "ls casa/",
        "ls -a casa",
        "ls -a casa/",
        "cd casa",
        "cd casa/"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls casa/}} {{rb:para mirar dentro de la casa.}}"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 33, 3


class Step3(StepTemplateNano):
    story = [
        "Mmm, parece que no puedes mirar adentro.",
        "Está cerrada de la misma forma que la {{bb:seccion-privada}} de la biblioteca.",
        "Tal vez haya una pista por aquí cerca.",
        "",
        "{{lb:Investiga}} la zona y fíjate si encuentras alguna pista."
    ]
    start_dir = "~/bosque/claro"

    # This should be an array of allowed directories you can end up in.
    # Perhaps an empty array means it doesn't matter where you end up.
    end_dir = "~/bosque/claro"

    hints = [
        "{{rb:Hay un cartel en el claro.}} {{lb:Examínalo}}{{rb:.}}",
        "{{rb:Examina ese cartel con}} {{yb:cat cartel}}{{rb:.}}"
    ]

    commands = [
        "cat cartel"
    ]

    # Perhaps a nice data structure could be if the list of commands were
    # paired with appropriate hints?
    paired_hints = {
        "ls": "Intenta examinar cada objeto con {{lb:cat}}."
    }

    def next(self):
        return 33, 4


class Step4(StepTemplateNano):
    story = [
        "Bien, el cartel tiene una instrucción. Vamos a probarla."
    ]

    # It would be good if we could pass the current dir across and this would
    # simply be the default?
    start_dir = "~/bosque/claro"
    end_dir = "~/bosque/claro"

    hints = [
        "{{rb:Usa}} {{yb:echo toc toc}} {{rb:para tocar la puerta.}}"
    ]

    commands = [
        "echo knock knock",
        "echo toc toc",
        "echo Toc toc",
        "echo Toc Toc"
    ]

    def next(self):
        return 33, 5



class Step5(StepTemplateNano):
    story = [
        "Escuchas una voz grave del otro lado de la puerta.",
        "",
        "Espadachin:",
        "{{Bb:Si me tienes, quieres compartirme.",
        "Si me compartes, ya no me tienes.",
        "¿Qué soy?}}",
        "",
        "{{yb:1. ¿Qué?}}",
        "{{yb:2. No sé}}"
    ]

    start_dir = "~/bosque/claro"
    end_dir = "~/bosque/claro"

    def next(self):
        if self._last_user_input.lower() in [
                "secret", "echo secret",
                "secreto", "echo secreto", "un secreto", "echo un secreto"
        ]:
            return 33, 6
        else:
            return 33, 8


class Step6(StepTemplateNano):
    story = [
        "Espadachin: {{Bb:...¿Completaste el desafío de la cueva?",
        "Muy bien, aquí tienes otro. Abre la puerta de mi casa.}}"
    ]
    start_dir = "~/bosque/claro"
    end_dir = "~/bosque/claro"

    def next(self):
        return 33, 7


class Step7(StepTemplateNano):
    story = [
        "Espadachin: {{Bb:Lo suponía. Tienes que completar los desafíos}} {{lb:de la cueva del bosque}}",
        "{{Bb:Vuelve cuando hayas terminado.}}"
    ]
    start_dir = "~/bosque/claro"
    end_dir = "~/bosque/cueva"
    hints = [
        "Espadachin: {{Bb:¡Ve a la}} {{bb:~/bosque/cueva}} {{Bb:y deja de merodear frente a mi casa!}}",
        "",
        "{{rb:Ve a}} {{bb:~/bosque/cueva}}"
    ]

    def check_command(self, line):
        if line in ["echo knock knock", "echo toc toc", "echo Toc toc", "echo Toc Toc"]:
            self.send_hint("Espadachin: {{Bb:Ve a buscar la respuesta. No te quedes ahí parado.}}")
            return
        return StepTemplateNano.check_command(self, line)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 33, 8


class Step8(StepTemplateNano):
    story = [
        "Espadachin: {{Bb:¡Esa no es la respuesta! Encuentra la respuesta}} {{lb:en la cueva del bosque.}}"
    ]
    start_dir = "~/bosque/claro"
    end_dir = "~/bosque/cueva"
    hints = [
        "Espadachin: {{Bb:¡Ve a la}} {{bb:~/bosque/cueva}} {{Bb:y deja de merodear frente a mi casa!}}",
        "{{rb:Ve a}} {{bb:~/bosque/cueva}}"
    ]

    def check_command(self, line):
        if line in ["echo knock knock", "echo toc toc", "echo Toc toc", "echo Toc Toc"]:
            self.send_hint("Espadachin: {{Bb:Ve a buscar la respuesta. No te quedes ahí adivinando.}}")
            return
        return StepTemplateNano.check_command(self, line)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 33, 9


class Step9(StepTemplateNano):
    story = [
        "{{lb:Entras despacio a la cueva. Huele a humedad.}}",
        "{{Bb:Mira alrededor.}}"
    ]
    start_dir = "~/bosque/cueva"
    end_dir = "~/bosque/cueva"
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]

    def next(self):
        return 34, 1
