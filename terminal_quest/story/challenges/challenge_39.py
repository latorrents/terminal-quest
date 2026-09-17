#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file, get_username
from terminal_quest.terminals import TerminalChmod


class StepTemplateChmod(StepTemplate):
    TerminalClass = TerminalChmod


class Step1(StepTemplateChmod):
    story = [
        "Ves a un Espadachin Enmascarado que te observa.",
        "{{lb:Escucha}} lo que tiene que decir."
    ]
    start_dir = "~/bosque/claro/casa"
    end_dir = "~/bosque/claro/casa"
    hints = [
        "{{rb:Usa}} {{yb:cat Espadachin}} {{rb:para}} {{lb:escuchar}} {{rb:lo que tiene que decir el Espadachin.}}"
    ]
    commands = [
        "cat Espadachin"
    ]

    def next(self):
        return 39, 2


class Step2(StepTemplateChmod):
    story = [
        "{{wb:Espadachin:}} {{Bb:\"Niño, ¿por qué me buscas?\"}}",
        "",
        "{{yb:1: Quiero abrir la sección privada de la biblioteca.}}",
        "{{yb:2: ¿Quién eres?}}",
        "{{yb:3: ¿Has estado dejándome notas extrañas?}}",
        "",
        "Responde con {{yb:echo 1}}, {{yb:echo 2}} o {{yb:echo 3}}."
    ]
    commands = [
        "echo 1"
    ]
    start_dir = "~/bosque/claro/casa"
    end_dir = "~/bosque/claro/casa"
    extra_hints = {
        "echo 2": "Espadachin: {{Bb:\"Huí del mundo exterior para hacer mi hogar aquí, en este bosque tranquilo. "
                  "Los pocos que me conocen me llaman el Espadachin Enmascarado.\"}}",
        "echo 3": "Espadachin: {{Bb:\"¿Qué notas?\"}}"
    }

    last_step = True

    def check_command(self, line):
        if line in self.extra_hints:
            self.send_hint(self.extra_hints[line])
            return

        return StepTemplateChmod.check_command(self, line)

    def next(self):
        return 39, 3


class Step3(StepTemplateChmod):
    print_text = [
        "{{yb:Quiero abrir la sección privada de la biblioteca.}}"
    ]
    story = [
        "Espadachin: {{Bb:\"Bueno, si abriste el cofre de la}} {{bb:~/bosque/cueva}}"
        "{{Bb:, entonces ya sabes cómo hacerlo.\"}}",
        "{{Bb:\"Una advertencia: lo que hay dentro es poderoso y peligroso a la vez.\"}}",
        "",
        "{{yb:1: ¿Qué hay en la biblioteca que sea tan peligroso?}}",
        "{{yb:2: ¿Por qué vives tan lejos de la gente?}}",
        "{{yb:3: ¿Sabes por qué está desapareciendo la gente?}}"
    ]

    commands = [
        "echo 3"
    ]

    start_dir = "~/bosque/claro/casa"
    end_dir = "~/bosque/claro/casa"
    extra_hints = {
        "echo 1": "Espadachin: {{Bb:\"Un comando que da a quien lo usa un poder tremendo, "
                  "y lo convierte en Super Usuario.\"}}",
        "echo 2": "Espadachin: {{Bb:\"Como soy espadachin, tengo la capacidad de}} {{lb:eliminar}} {{Bb:a otros. "
                  "Eso pone nerviosa a la gente cuando estoy cerca, así que prefiero vivir en el bosque.\"}}"
    }

    def check_command(self, line):
        if line in self.extra_hints:
            self.send_hint(self.extra_hints[line])

        return StepTemplateChmod.check_command(self, line)

    def next(self):
        return 39, 4


class Step4(StepTemplateChmod):
    print_text = [
        "{{yb:¿Sabes por qué está desapareciendo la gente?}}"
    ]
    story = [
        "Espadachin: {{Bb:\"No sabía que la gente estaba desapareciendo. ¿Es por eso que suena esa campana?",
        "Entonces quizás sea bueno que estés aquí.\"",
        "\"Dime, ¿cómo te llamas?\"}}"
    ]
    start_dir = "~/bosque/claro/casa"
    end_dir = "~/bosque/claro/casa"
    commands = [
        "echo " + get_username()
    ]
    hints = [
        "{{rb:Usa}} {{yb:echo " + get_username() + "}} {{rb:para decir tu nombre.}}"
    ]

    def check_command(self, last_user_input):
        if last_user_input.startswith("echo") and last_user_input not in self.commands:
            self.send_hint(
                "Espadachin: {{Bb:\"Qué nombre tan extraño. ¿De verdad te llamas así?\"}}"
            )
        return StepTemplateChmod.check_command(self, last_user_input)

    def next(self):
        return 39, 5


class Step5(StepTemplateChmod):
    story = [
        "Espadachin: {{Bb:\"Eso pensé. Pocos tienen el poder de usar los comandos que usaste antes.",
        "¿Cómo supe tu nombre? Usa}} {{yb:ls -l}} {{Bb:para verlo.\"}}"
    ]
    commands = [
        "ls -l",
        "ls -l .",
        "ls -l ./"
    ]
    start_dir = "~/bosque/claro/casa"
    end_dir = "~/bosque/claro/casa"

    file_list = [
        {
            "contents": get_story_file("note_swordsmaster-house"),
            "path": "~/bosque/claro/casa/nota",
            "permissions": 0o644,
            "type": "file"
        }
    ]

    def next(self):
        return 39, 6


class Step6(StepTemplateChmod):
    story = [
        "Espadachin: {{Bb:\"Tu nombre está escrito en este mundo, para quien sepa dónde mirar.\"}}",
        "{{Bb:\"...\"}}",
        "{{Bb:\"...¿por qué hay una}} {{lb:nota}} {{Bb:en este cuarto?\"}}",
        "{{Bb:\"¿La ves? Usa}} {{lb:cat nota}} {{Bb:para examinarla.\"}}"
    ]
    commands = [
        "cat nota"
    ]

    start_dir = "~/bosque/claro/casa"
    end_dir = "~/bosque/claro/casa"

    def next(self):
        return 40, 1
