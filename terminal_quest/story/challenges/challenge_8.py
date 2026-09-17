# challenge_8.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file
from terminal_quest.terminals import TerminalCd


class StepTemplateCd(StepTemplate):
    TerminalClass = TerminalCd


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):

    story = [
        "{{pb:Ding. Dong.}}\n",
        "Suena como la campana que escuchaste antes.\n",
        "Usa {{yb:ls}} para {{lb:mirar alrededor}} nuevamente."
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo"
    commands = "ls"
    hints = ["{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"]
    deleted_items = ["~/pueblo/hombre-enojado"]

    def next(self):
        return 8, 2


class Step2(StepTemplateCd):

    story = [
        (
            "{{wb:Chico:}} {{Bb:\"¡Oh no! ¡Ese hombre enojado de piernas raras se ha "
            "ido!}} {{Bb:¿Escuchaste la campana justo antes de que desapareciera?\"}}"
        ),
        "{{wb:Chica:}} {{Bb:\"Estoy asustada...\"}}",
        "\n{{pb:Ding. Dong.}}\n",
        "{{wb:Chica:}} {{Bb:\"¡Oh! ¡La escuché otra vez!\"}}",
        "\n{{lb:Mira alrededor}} para chequear."
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo"
    commands = "ls"
    hints = ["{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"]
    deleted_items = ["~/pueblo/chico"]

    def next(self):
        return 8, 3


class Step3(StepTemplateCd):

    story = [
        (
            "{{wb:Chica:}} {{Bb:\"Espera, había un}} {{bb:chico}} {{Bb:aquí...¿no "
            "es cierto?"
        ),
        "Cada vez que suena esa campana, ¡alguien desaparece!\"}}",
        "{{wb:Alcalde:}} {{Bb:\"¿Tal vez decidieron volver a sus casas...?\"}}",
        "\n{{pb:Ding. Dong.}}\n",
        "{{lb:Mira alrededor.}}"
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo"
    commands = "ls"
    hints = ["{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"]
    deleted_items = ["~/pueblo/chica"]

    def next(self):
        return 8, 4


class Step4(StepTemplateCd):

    story = [
        "Te encuentras solo con el {{bb:Alcalde}}.\n",
        "{{lb:Escucha}} lo que el {{bb:Alcalde}} tiene para decir."
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo"
    commands = "cat Alcalde"
    hints = ["{{rb:Usa}} {{yb:cat Alcalde}} {{rb:para hablarle al Alcalde.}}"]

    def next(self):
        return 8, 5


class Step5(StepTemplateCd):

    story = [
        "{{wb:Alcalde:}} {{Bb:\"Todos...¿han desaparecido?\"\n",
        "\"....Debo irme ahora...\"}}",
        "\n{{pb:Ding. Dong.}}\n"
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo"
    commands = "ls"
    hints = ["{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"]
    deleted_items = ["~/pueblo/Alcalde"]
    file_list = [
        {
            "path": "~/pueblo/nota",
            "contents": get_story_file("note_town"),
            "type": "file"
        }
    ]

    def next(self):
        return 8, 6


class Step6(StepTemplateCd):
    story = [
        "Todos se han ido.",
        "Espera - hay una {{bb:nota}} en el suelo.\n",
        "Usa {{yb:cat}} para leer la {{bb:nota}}."
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo"
    commands = "cat nota"
    hints = ["{{rb:Usa}} {{yb:cat nota}} {{rb:para leer la nota.}}"]

    def next(self):
        return 9, 1
