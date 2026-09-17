# challenge_11.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os
from terminal_quest.step import StepTemplate
from terminal_quest.terminals import TerminalCd
from terminal_quest.terminals import TerminalMv
from terminal_quest.step_helpers import unblock_commands
from terminal_quest.common import tq_file_system, get_story_file
from terminal_quest.helpers import wrap_in_box


class StepTemplateCd(StepTemplate):
    TerminalClass = TerminalCd


class StepTemplateMv(StepTemplate):
    TerminalClass = TerminalMv


# ----------------------------------------------------------------------------------------


# The next few steps should be like the disappearing of people in the town
class Step1(StepTemplateCd):
    story = [
        "Ves un grupo de personas asustadas y un {{bb:perro}}.\n",
        "{{lb:Escucha}} lo que tienen para decir con {{yb:cat}}.\n"
    ]
    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"

    # Use functions here
    all_commands = {
        "cat Edith": "{{wb:Edith:}} {{Bb:\"¡Nos encontraste! Edward, te dije que hablaras en voz baja.\"}}",
        "cat Eleanor": "{{wb:Eleanor:}} {{Bb:\"Mi mami tiene miedo de que la campana nos encuentre si salimos.\"}}",
        "cat Edward": ("{{wb:Edward:}} {{Bb:\"Lo siento, Edith...pero no creo que quiera hacernos daño. "
                       "¿Tal vez pueda ayudarnos?\"}}"),
        "cat perro": "{{wb:Perro:}} {{Bb:\"¡Guau guau!\"}}"
    }

    def check_command(self, line):

        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if line == 'ls':
            hint = "{{gb:Miras a tu alrededor.}}"
            self.send_hint(hint)
            return False

        end_dir_validated = self.get_fake_path() == self.end_dir

        # if the validation is included
        if line in self.all_commands.keys() and end_dir_validated:
            # Print hint from person
            hint = self.all_commands[self._last_user_input]
            self.all_commands.pop(self._last_user_input, None)

            if len(self.all_commands) > 0:
                hint += "\n{{gb:¡Bien hecho! Fíjate en %d más.}}" % len(self.all_commands)
            else:
                hint += "\n{{gb:Presiona}} {{ob:Enter}} {{gb:para continuar.}}"

            self.send_hint(hint)

        else:
            self.send_hint("{{rb:Usa}} {{yb:%s}} {{rb:para avanzar.}}" % list(self.all_commands.keys())[0])

        # Don't pass unless the user has emptied self.all_commands
        return False

    def next(self):
        return 11, 2


class Step2(StepTemplateMv):
    story = [
        "Parece que Edward tiene algo para decirte.\n",
        "{{wb:Edward:}} {{Bb:\"¡Oye! ¿Puedes ayudarme?\"}}",

        "{{Bb:\"He estado intentando mover esta}} {{bb:manzana}} {{Bb:dentro de la}} {{bb:canasta}}{{Bb:.\"}}",

        ("{{Bb:\"Me dijeron que el comando}} {{yb:mv manzana canasta/}} {{Bb:lo lograría, pero no consigo que "
     "funcione. ¿Tienes tú el poder para hacerlo?\"}}\n"),
    ]

    story += wrap_in_box([
        "{{gb:Nuevo Poder}}: para {{lb:mover}} objetos, escribe {{yb:mv}}",
        "y el nombre del objeto.",
    ])

    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "mv manzana canasta",
        "mv manzana canasta/"
    ]
    highlighted_commands = ['mv']
    hints = [
        (
            "{{rb:Usa el comando}} {{yb:mv manzana canasta/}} {{rb:para mover la manzana dentro "
            "de la canasta.}}"
        )
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 11, 3


class Step3(StepTemplateMv):
    story = [
        "Asegúrate de que has podido mover la {{bb:manzana}}. {{lb:Mira alrededor}} para comprobarlo.\n"
    ]
    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]
    file_list = [
        {
            "path": "~/pueblo/.refugio-oculto/canasta/manzana",
            "contents": get_story_file("manzana"),
            "type": "file"
        }
    ]

    def next(self):
        return 11, 4


class Step4(StepTemplateMv):
    story = [
        "{{gb:¡Buen trabajo! La manzana fue movida con éxito.}}\n",
        (
            "{{wn:Ahora asegúrate de que la manzana esté en la}} {{bb:canasta}} {{wn:usando}} "
            "{{yb:ls}}{{wn:.}}\n"
        )
    ]
    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "ls canasta",
        "ls canasta/",
        "ls -a canasta",
        "ls -a canasta/"
    ]
    hints = [
        "{{rb:Usa el comando}} {{yb:ls canasta/}} {{rb:para mirar dentro de la canasta.}}"
    ]

    def next(self):
        return 11, 5


class Step5(StepTemplateMv):
    story = [
        "{{gb:¡Excelente, la manzana está en la canasta!}}",
        "\n{{wb:Edward:}} {{Bb:\"¡Guau, lo lograste!\"}}",
        ("{{Bb:\"¿Puedes también mover la}} {{bb:manzana}} {{Bb:de la}} {{bb:canasta}} "
     "{{Bb:de vuelta aquí?\"}}\n")
    ]
    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "mv canasta/manzana .",
        "mv canasta/manzana ./"
    ]
    hints = [
        (
            "{{rb:Usa el comando}} {{yb:mv canasta/manzana ./}} {{rb:para mover la manzana de la "
            "canasta a tu posición actual}} {{bb:./}}"
        )
    ]

    def block_command(self, line):
        if line == "mv canasta/manzana":
            hint = (
                "{{gb:¡Estás cerca! El comando completo es}} {{yb:mv canasta/manzana ./}} {{gb:- "
                "¡no olvides el punto!}}"
            )
            self.send_hint(hint)
            return True
        else:
            return unblock_commands(line, self.commands)

    def next(self):
        return 11, 6


class Step6(StepTemplateMv):
    story = [
        (
            "{{wb:Edith:}} {{Bb:\"Deberías dejar de jugar con eso, es la última comida que "
            "nos queda.\"}}"
        ),
        "{{Bb:\"¡Ah! ¡El perro se escapó!\"}}",
        "{{wb:Eleanor:}} {{Bb:\"¡Perrito!\"}}",
        "{{wb:Edith:}} {{Bb:\"¡No, querido! ¡No salgas!\"}}",
        "\n{{bb:Eleanor}} sigue a su {{bb:perro}} y sale del {{bb:.refugio-oculto}}.",
        "{{lb:Mira alrededor}} para ver si está.\n"
    ]
    file_list = [
        {"path": "~/pueblo/Eleanor"},
        {"path": "~/pueblo/perro"}
    ]
    deleted_items = [
        '~/pueblo/.refugio-oculto/Eleanor',
        '~/pueblo/.refugio-oculto/perro'
    ]

    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "ls", "ls -a"
    ]
    hints = [
        "{{rb:Mira alrededor usando}} {{yb:ls}} {{rb:para ver si Eleanor está allí.}}"
    ]

    def next(self):
        return 11, 7


class Step7(StepTemplateMv):
    story = [
        "{{wb:Edith:}} {{Bb:\"¡No! ¡Cariño, vuelve!\"}}",
        "{{Bb:\"¡Tú, por favor, salva a mi niña!\"}}\n",

        "Primero, {{lb:mira afuera}} para ver a {{bb:Eleanor}} con {{yb:ls ../}}",
    ]
    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = ""
    commands = [
        "ls ..",
        "ls ../",
        "ls ~/pueblo",
        "ls ~/pueblo/"
    ]
    hints = [
        "{{rb:Mira en el pueblo usando}} {{yb:ls ../}} {{rb:o}} {{yb:ls ~/pueblo/}}"
    ]

    def next(self):
        return 11, 8


class Step8(StepTemplateMv):
    story = [
        "Ahora {{lb:mueve}} a {{bb:Eleanor}} del {{bb:pueblo}} {{bb:..}} a tu posición actual{{bb:.}}\n"
    ]
    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "mv ../Eleanor .",
        "mv ../Eleanor ./",
        "mv ~/pueblo/Eleanor ~/pueblo/.refugio-oculto",
        "mv ~/pueblo/Eleanor ~/pueblo/.refugio-oculto/",
        "mv ~/pueblo/Eleanor .",
        "mv ~/pueblo/Eleanor ./",
        "mv ../Eleanor ~/pueblo/.refugio-oculto",
        "mv ../Eleanor ~/pueblo/.refugio-oculto/",
    ]
    hints = [
        (
            "{{rb:¡Apúrate! Usa}} {{yb:mv ../Eleanor ./}} {{rb:para mover a la niña a un "
            "lugar seguro.}}"
        )
    ]
    girl_file = os.path.join(tq_file_system, '~/pueblo/.refugio-oculto/Eleanor')

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def check_command(self, line):

        if os.path.exists(self.girl_file):
            return True

        else:
            self.send_stored_hint()
            return False

    def next(self):
        return 12, 1
