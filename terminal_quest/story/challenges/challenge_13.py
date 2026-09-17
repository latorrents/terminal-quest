# challenge_13.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.terminals import TerminalMv
from terminal_quest.step_helpers import unblock_commands_with_cd_hint, unblock_commands


class StepTemplateMv(StepTemplate):
    TerminalClass = TerminalMv


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMv):
    story = [
        "{{wb:Edward:}} {{Bb:\"¡Muchas gracias por salvar a mi niña!",
        "Tengo que pedirte otro favor...",

        (
            "No tenemos comida. ¿Puedes traernos algo? No tuvimos tiempo de agarrar nada "
            "antes de escondernos.\""
        ),

        "\"¿Recuerdas haber visto comida en tus viajes?\"}}",

        (
            "\n...¡ah! ¡Tienes un montón de comida en tu {{bb:cocina}}! Podemos traérsela a "
            "esta familia."
        ),

        (
            "\nEmpieza por {{lb:mover}} la {{bb:canasta}} a {{bb:~}} usando el comando {{yb:mv "
            "canasta ~/}}\n"
        )
    ]
    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "mv canasta ~",
        "mv canasta/ ~",
        "mv canasta ~/",
        "mv canasta/ ~/",
        "mv canasta ../..",
        "mv canasta/ ../..",
        "mv canasta ../../",
        "mv canasta/ ../../"
    ]
    hints = [
        (
            "{{rb:Usa el comando}} {{yb:mv canasta ~/}} {{rb:para mover la}} {{bb:canasta}} "
            "{{rb:a la carretera ventosa}} {{bb:~}}"
        )
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 13, 2


class Step2(StepTemplateMv):
    story = [
        (
            "Ahora sigue a la {{bb:canasta}}. Usa {{yb:cd}} solo para {{lb:ir}} hacia "
            "la carretera ventosa {{bb:~}}.\n"
        )
    ]
    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~"
    commands = [
        "cd",
        "cd ~",
        "cd ~/"
    ]
    hints = [
        "{{rb:Usa el comando}} {{yb:cd}} {{rb:solo para moverte por la carretera ~}}"
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 13, 3


class Step3(StepTemplateMv):
    story = [
        (
            "Estás solo en la carretera. {{lb:Mira alrededor}} con {{yb:ls}} para asegurarte "
            "de que tienes la {{bb:canasta}} contigo.\n"
        )
    ]

    start_dir = "~"
    end_dir = "~"
    commands = [
        "ls"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:solo para mirar alrededor.}}"
    ]

    def next(self):
        return 13, 4


class Step4(StepTemplateMv):
    story = [
        "Tienes la {{bb:canasta}} a tu lado, y ves {{bb:mi-casa}} cerca.",
        "Mueve la {{bb:canasta}} a {{bb:mi-casa/cocina}}.",
        "No olvides usar la tecla {{ob:Tab}} para autocompletar los comandos.\n"
    ]

    start_dir = "~"
    end_dir = "~"
    commands = [
        "mv canasta mi-casa/cocina",
        "mv canasta/ mi-casa/cocina",
        "mv canasta mi-casa/cocina/",
        "mv canasta/ mi-casa/cocina/",
        "mv canasta ~/mi-casa/cocina",
        "mv canasta/ ~/mi-casa/cocina",
        "mv canasta ~/mi-casa/cocina/",
        "mv canasta/ ~/mi-casa/cocina/"
    ]
    hints = [
        (
            "{{rb:Usa}} {{yb:mv canasta mi-casa/cocina/}} {{rb:para mover la canasta hacia "
            "tu cocina.}}"
        ),
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 13, 5


class Step5(StepTemplateMv):
    story = [
        "Ahora {{lb:ve}} a {{bb:mi-casa/cocina}} usando {{yb:cd}}.\n",
    ]

    start_dir = "~"
    end_dir = "~/mi-casa/cocina"
    commands = [
        "cd mi-casa/cocina",
        "cd mi-casa/cocina/",
        "cd ~/mi-casa/cocina",
        "cd ~/mi-casa/cocina/"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cd mi-casa/cocina}} {{rb:para ir a tu cocina.}}",
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 14, 1
