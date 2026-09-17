# challenge_4.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file
from terminal_quest.terminals import TerminalCd
from terminal_quest.step_helpers import unblock_commands_with_cd_hint
from terminal_quest.helpers import wrap_in_box


class StepTemplateCd(StepTemplate):
    TerminalClass = TerminalCd


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):
    story = [
        "¡Qué extraño! No hay tiempo para eso - encontremos a {{bb:Mama}}.\n ",
    ]
    story += wrap_in_box([
        "{{gb:Nuevo Poder}}: {{yb:cd}} te permite {{lb:moverte}}",
        "entre distintos sitios.",
    ])
    story += [
        "Usa el comando {{yb:cd ..}} para {{lb:abandonar}} tu habitación.\n"
    ]

    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa"
    commands = [
        "cd ..",
        "cd ../",
        "cd ~/mi-casa",
        "cd ~/mi-casa/"
    ]
    highlighted_commands = ['cd']
    hints = [
        (
            "{{rb:Escribe}} {{yb:cd ..}} {{rb:para abandonar tu habitación. El}} {{lb:..}} "
            "{{rb:es para salir de allí.}}"
        ),
        "{{rb:Escribe}} {{yb:cd ..}} {{rb:para abandonar tu habitación.}}"
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 4, 2


class Step2(StepTemplateCd):
    story = [
        "Abandonaste {{bb:mi-cuarto}} y estás en la sala de {{bb:mi-casa}}.\n",
        "{{lb:Mira alrededor}} de los diferentes sitios usando {{yb:ls}}.\n"
    ]
    start_dir = "~/mi-casa"
    end_dir = "~/mi-casa"
    commands = "ls"
    hints = ["{{rb:Escribe}} {{yb:ls}} {{rb:y presiona}} {{ob:Enter}}{{rb:.}}"]
    file_list = [
        {
            "path": "~/mi-casa/jardin/invernadero/nota",
            "contents": get_story_file("note_greenhouse"),
            "type": "file"
        }
    ]
    deleted_items = ['~/mi-casa/jardin/invernadero/Papa']

    def next(self):
        return 4, 3


class Step3(StepTemplateCd):
    story = [
        "{{pb:Ding. Dong.}}\n",
        "¿Qué fue eso? ¿Una campana? Eso es un poco extraño.",
        "Ves la puerta de tu {{bb:cocina}}, y escuchas el sonido de alguien cocinando.",
        "¡Parece que alguien está preparando el desayuno!\n",
        "Para {{lb:entrar a la}} {{bb:cocina}}, usa {{yb:cd cocina}}"
    ]
    start_dir = "~/mi-casa"
    end_dir = "~/mi-casa/cocina"
    commands = ["cd cocina", "cd cocina/"]
    hints = ["{{rb:Escribe}} {{yb:cd cocina}} {{rb:y presiona}} {{ob:Enter}}{{rb:.}}"]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 4, 4


class Step4(StepTemplateCd):
    story = [
        "Genial, estás dentro de la {{bb:cocina}}.\n",
        "{{lb:Busca}} a {{bb:Mama}} usando {{yb:ls}}."
    ]
    start_dir = "~/mi-casa/cocina"
    end_dir = "~/mi-casa/cocina"
    commands = "ls"
    hints = ["{{rb:¿No puedes encontrarla? Escribe}} {{yb:ls}} {{rb:y presiona}} {{ob:Enter}}{{rb:.}}"]

    def next(self):
        return 4, 5


class Step5(StepTemplateCd):
    story = [
        "La ves trabajando muy duro entre una nube de vapor.",
        "Vamos a {{lb:escuchar}} lo que {{bb:Mama}} tiene para decir usando {{yb:cat}}."
    ]
    start_dir = "~/mi-casa/cocina"
    end_dir = "~/mi-casa/cocina"
    commands = "cat Mama"
    hints = ["{{rb:¿Atascado? Escribe:}} {{yb:cat Mama}}{{rb:. ¡No olvides la letra mayúscula!}}"]

    def next(self):
        return 5, 1
