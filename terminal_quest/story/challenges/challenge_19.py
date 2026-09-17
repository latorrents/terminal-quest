# challenge_18.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os

from terminal_quest.step import StepTemplate
from terminal_quest.terminals import TerminalEcho


class StepTemplateEcho(StepTemplate):
    TerminalClass = TerminalEcho


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateEcho):
    username = os.environ['LOGNAME']
    story = [
        "Ruth: {{Bb:\"¡Me asustaste!\"",
        "\"¿Nos conocemos? Me pareces conocido...\"",
        "\"Espera, ¿no eres el hijo de}} {{bb:Mama}}{{Bb:?\"",
        "\"...¿Y bien? ¿Te comieron la lengua?\"",
        "\"¿No te llamas}} {{yb:%s}}{{Bb:?\"}}" % username,
        "\n{{gb:Responde con}} {{yb:echo si}} {{gb:o}} {{yb:echo no}}{{gb:.}}"
    ]

    # Story has been moved to
    hints = [
        "{{rb:Usa}} {{yb:echo}} {{rb:para responder a su pregunta.}}",
        "{{rb:Responde que sí usando}} {{yb:echo si}}{{rb:.}}"
    ]

    commands = [
        "echo si",
        "echo Si",
        "echo SI",
        "echo sí",
        "echo Sí",
        "echo SÍ",
        "echo yes",
        "echo Yes",
        "echo YES"
    ]

    start_dir = "~/granja/granero"
    end_dir = "~/granja/granero"

    def check_command(self, line):

        if line == "echo no" or line == "echo No" or line == "echo NO":
            hint = (
                "Ruth: {{Bb:\"Ay, no digas tonterías, eres igualito.\"}}"
            )
            self.send_hint(hint)

        return StepTemplateEcho.check_command(self, line)

    def next(self):
        return 19, 2


class Step2(StepTemplateEcho):
    print_text = ["{{yb:\"Sí\"}}"]

    story = [
        "Ruth: {{Bb:\"¡Ah, lo sabía!\"}}",
        "{{Bb:\"¿Vives en la pequeña casa fuera del pueblo?\"}}",
        # TODO: see if this can appear as a block
        # TODO: change the colour of this.
        "{{yb:1: \"Sí\"}}",
        "{{yb:2: \"No\"}}",
        "{{yb:3: \"No lo sé\"}}",
        (
            "\n{{gb:Usa}} {{yb:echo 1}}{{gb:,}} {{yb:echo 2}} {{gb:o}} {{yb:echo 3}} {{gb:para "
            "responder con la opción 1, 2 o 3.}}\n"
        )
    ]

    start_dir = "~/granja/granero"
    end_dir = "~/granja/granero"
    commands = ["echo 1", "echo 2", "echo 3"]
    hints = [
        (
            "{{rb:Usa}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:o}} {{yb:echo 3}} {{rb:para "
            "responderle a Ruth.}}"
        )
    ]

    def check_command(self, line):
        replies = {
            "echo yes": "1",
            "echo si": "1",
            "echo sí": "1",
            "echo no": "2",
            "echo \"i don't know\"": "3",
            "echo i don't know": "3",
            "echo \"no se\"": "3",
            "echo \"no sé\"": "3",
            "echo no se": "3",
            "echo no sé": "3",
            "echo \"no lo se\"": "3",
            "echo \"no lo sé\"": "3",
            "echo no lo se": "3",
            "echo no lo sé": "3"
        }

        if line.lower() in replies:
            hint = [
                "\n{{rb:Si quieres responder \"%s\", usa}} {{yb:echo %s}}" % (line, replies[line.lower()])
            ]
            self.send_hint(hint)
        else:
            return StepTemplateEcho.check_command(self, line)

    def next(self):
        Step3.prev_command = self._last_user_input
        return 19, 3


class Step3(StepTemplateEcho):
    start_dir = "~/granja/granero"
    end_dir = "~/granja/granero"

    commands = [
        "echo 1",
        "echo 2"
    ]
    hints = [
        (
            "Ruth: {{Bb:\"Disculpa, ¿qué dijiste? Sabes usar el comando}} {{lb:echo}}"
            "{{Bb:, ¿verdad?\"}}"
        ),
        (
            "{{rb:Usa}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:o}} {{yb:echo 3}} {{rb:para "
            "responder.}}"
        )
    ]

    def _run_at_start(self):
        if self.prev_command == "echo 1":  # yes
            self.print_text = ["{{yb:\"Sí\"}}"]
            self.story = ["Ruth: {{Bb:\"¡Eso pensé!\"}}"]
        elif self.prev_command == "echo 2":  # no
            self.print_text = ["{{yb:\"No\"}}"]
            self.story = ["Ruth: {{Bb:\"Deja de mentir, te conozco.\"}}"]
        elif self.prev_command == "echo 3":  # I don't know
            self.print_text = ["{{yb:\"No lo sé\"}}"]
            self.story = ["Ruth: {{Bb:\"¿No sabes? Eso es preocupante...\"}}"]

        self.story = self.story + [
            "\n{{Bb:\"¿Vienes caminando desde el pueblo? ¿Viste a mi marido allí?",
            (
                "Es un}} {{bb:hombre-enojado}}{{Bb:, fue al pueblo para esa reunión importante "
                "con el Alcalde.\"}}"
            ),
            "\n{{yb:1: \"Lo siento, desapareció frente a mis ojos.\"}}",
            "{{yb:2: \"No he visto a su marido, pero la gente ha estado desapareciendo en el pueblo.\"}}",
            "{{yb:3: \"No sé nada.\"}}",
            (
                "\nResponde eligiendo una opción con el comando {{yb:echo}} y el número "
                "de la opción.\n"
            )
        ]

    def check_command(self, line):
        if line == "echo 1":
            return True
        elif line == "echo 2":
            hint = ("Ruth: {{Bb:\"Siento que me estás ocultando algo...\"}}")
            self.send_hint(hint)
            return False
        elif line == "echo 3":
            hint = ((
                "Ruth: {{Bb:\"¿En serio? ¿Estás seguro de que no viste a un}} "
                "{{lb:hombre-enojado}}{{Bb: en el pueblo?\"}}"
            ))
            self.send_hint(hint)
            return False

        else:
            self.send_stored_hint()
            return False

    def next(self):
        return 19, 4


class Step4(StepTemplateEcho):
    print_text = [
        "{{yb:\"Lo siento, desapareció frente a mis ojos.\"}}"
    ]
    story = [
        (
            "Ruth: {{Bb:\"¿Desapareció frente a tus ojos? ¡Oh, no! En la radio han dicho que "
            "hay personas desaparecidas... ¿qué debería hacer?\"}}"
        ),
        "\n{{yb:1: \"Algunas personas sobrevivieron escondiéndose.\"}}",
        "{{yb:2: \"Creo que deberías ir a buscar a tu marido.\"}}\n"
    ]

    start_dir = "~/granja/granero"
    end_dir = "~/granja/granero"

    commands = [
        "echo 1",
        "echo 2"
    ]

    hints = [
        "Ruth: {{Bb:\"¿Qué dijiste? No te entendí.\"}}",
        "{{rb:Usa}} {{yb:echo 1}} {{rb:o}} {{yb:echo 2}} {{rb:para responder.}}"
    ]

    def check_command(self, line):
        if line == "echo 1":
            return True
        elif line== "echo 2":
            response = (
                (
                    "Ruth: {{Bb:\"Me da miedo ir y desaparecer yo también.\"\n\"Él podría volver en cualquier "
                    "momento, debería quedarme en casa. ¿Se te ocurre otra idea?\"}}"
                )
            )
            self.send_hint(response)
        else:
            self.send_stored_hint()

    def next(self):
        return 20, 1
