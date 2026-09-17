# challenge_15.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.terminals import TerminalMv
from terminal_quest.step_helpers import unblock_commands_with_cd_hint


class StepTemplateMv(StepTemplate):
    TerminalClass = TerminalMv


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMv):
    story = [
        "Tienes la molesta sensación de que se te está pasando algo.",
        "¿Cuál era el comando que te ayudó a encontrar el refugio oculto?\n",
        "Úsalo para {{lb:mirar alrededor más de cerca}}.\n"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls -a}} {{rb:para mirar a tu alrededor más de cerca.}}"
    ]

    story_dict = {
        "CAT, LS, CD, .nota": {
            "path": "~/mi-casa/mi-cuarto/.cofre"
        }
    }

    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "ls -a"
    ]

    def next(self):
        return 15, 2


class Step2(StepTemplateMv):
    story = [
        "¿Qué es eso? Hay un {{bb:.cofrecito}} en una esquina del refugio.",
        "Vamos a {{lb:mirar dentro}} del {{bb:.cofrecito}}."
    ]

    hints = [
        "{{rb:Usa}} {{yb:ls .cofrecito}} {{rb:para mirar dentro}}"
    ]

    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "ls .cofrecito",
        "ls .cofrecito/",
        "ls -a .cofrecito",
        "ls -a .cofrecito/"
    ]

    def next(self):
        return 15, 3


class Step3(StepTemplateMv):
    story = [
        "Ves un pergamino de aspecto especial con un sello que dice {{bb:MV}}.",
        "{{lb:Lee}} lo que dice."
    ]

    hints = [
        "{{rb:Usa}} {{yb:cat .cofrecito/MV}} {{rb:para leer el pergamino}}"
    ]

    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "cat .cofrecito/MV"
    ]

    def next(self):
        return 15, 4


class Step4(StepTemplateMv):
    story = [

        "{{wb:Edward:}} {{Bb:\"Oye, ese es nuestro}} {{bb:.cofrecito}}{{Bb:. Lo usamos para guardar cosas a salvo.",
        "Gracias a ese pergamino MV aprendí a mover objetos con}} {{yb:mv}}{{Bb:.",
        "Seguro que a ti te sirve más. Por favor, tómalo como agradecimiento por salvarnos.\"}}",
        "",
        "\nTal vez deberías volver a {{bb:mi-casa}} para buscar más objetos ocultos.",
        "Para volver rápidamente a casa, usa {{yb:cd ~/mi-casa}}\n"
    ]

    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/mi-casa"
    commands = [
        'cd ~/mi-casa/',
        'cd ~/mi-casa'
    ]
    hints = [
        (
            "{{rb:¡Sin abreviaturas! Usa}} {{yb:cd ~/mi-casa}} {{rb:para volver a tu casa en "
            "un solo paso.}}"
        )
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 15, 5


class Step5(StepTemplateMv):
    story = [
        "¡Veamos si podemos encontrar algo oculto por aquí!",
        "¿Dónde piensas que podremos encontrar cosas ocultas?\n",
        "Intenta {{lb:mirar más de cerca}} en {{bb:mi-cuarto}} primero."
    ]

    start_dir = '~/mi-casa'

    hints = [
        "{{rb:¿Atascado? Mira en}} {{yb:mi-cuarto}}{{rb:.}}",
        (
            "{{rb:Usa}} {{yb:ls -a mi-cuarto}} {{rb:para buscar objetos ocultos en}} "
            "{{lb:mi-cuarto}}{{rb:.}}"
        )
    ]

    def check_output(self, output):
        # Need to check that .chest is shown in the output of the command
        if not output:
            return False

        if '.cofre' in output:
            return True

        return False

    def next(self):
        return 16, 1
