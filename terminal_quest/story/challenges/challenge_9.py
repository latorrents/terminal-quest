# challenge_9.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file
from terminal_quest.step_helpers import unblock_commands_with_cd_hint
from terminal_quest.terminals import TerminalCd


class StepTemplateCd(StepTemplate):
    TerminalClass = TerminalCd


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):
    story = [
        "¡Oh no! Fíjate si tu {{bb:Mama}} se encuentra bien.\n",
        "Escribe {{yb:cd ..}} para irte del {{bb:pueblo}}."
    ]
    start_dir = "~/pueblo"
    end_dir = "~"
    commands = ["cd ..", "cd ../", "cd"]
    hints = ["{{rb:Usa}} {{yb:cd ..}} {{rb:para emprender el regreso a casa.}}"]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 9, 2


class Step2(StepTemplateCd):
    story = [
        "{{pb:Ding. Dong.}}\n",
        "Escribe {{yb:cd mi-casa/cocina}} para ir directo a la {{bb:cocina}}.\n",
        "{{gb:Presiona}} {{ob:TAB}} {{gb:¡para acelerar tu escritura!}}"
    ]
    start_dir = "~"
    end_dir = "~/mi-casa/cocina"
    commands = ["cd mi-casa/cocina", "cd mi-casa/cocina/"]
    hints = [
        "{{rb:Usa}} {{yb:cd mi-casa/cocina}} {{rb:para ir a la cocina.}}"
    ]
    file_list = [
        {
            "path": "~/mi-casa/cocina/nota",
            "contents": get_story_file("note_kitchen"),
            "type": "file"
        }
    ]
    deleted_items = ['~/mi-casa/cocina/Mama', '~/pueblo/nota']

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 9, 3


class Step3(StepTemplateCd):
    story = [
        "{{lb:Mira alrededor}} para asegurarte de que todo esté bien."
    ]
    start_dir = "~/mi-casa/cocina"
    end_dir = "~/mi-casa/cocina"
    commands = "ls"
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para ver si todo está en su lugar.}}"
    ]

    def next(self):
        return 9, 4


class Step4(StepTemplateCd):
    story = [
        "¡Oh no! ¡{{bb:Mama}} también ha desaparecido!",
        "Espera, allí hay otra {{bb:nota}}.\n",
        "Usa {{yb:cat}} para {{lb:leer}} la {{bb:nota}}."
    ]
    start_dir = "~/mi-casa/cocina"
    end_dir = "~/mi-casa/cocina"
    commands = "cat nota"
    hints = ["{{rb:Usa}} {{yb:cat nota}} {{rb:para leer la nota.}}"]

    def next(self):
        return 10, 1
