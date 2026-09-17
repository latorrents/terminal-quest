# challenge_10.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.step_helpers import unblock_commands_with_cd_hint
from terminal_quest.terminals import TerminalCd


class StepTemplateCd(StepTemplate):
    TerminalClass = TerminalCd


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):
    story = [
        "Estás en tu casa. Parece que estás solo.",
        "Usa {{yb:cat}} para {{lb:examinar}} algunos objetos alrededor tuyo.\n"
    ]
    allowed_commands = [
        "cat banana",
        "cat pastel",
        "cat croissant",
        "cat uvas",
        "cat leche",
        "cat periodico",
        "cat horno",
        "cat tarta",
        "cat sandwich",
        "cat mesa"
    ]
    start_dir = "~/mi-casa/cocina"
    end_dir = "~/mi-casa/cocina"
    counter = 0
    deleted_items = ["~/mi-casa/cocina/nota"]
    file_list = [
        {"path": "~/pueblo/.refugio-oculto/Eleanor"},
        {"path": "~/pueblo/.refugio-oculto/Edward"},
        {"path": "~/pueblo/.refugio-oculto/Edith"},
        {"path": "~/pueblo/.refugio-oculto/manzana"},
        {"path": "~/pueblo/.refugio-oculto/perro"},
        {"path": "~/pueblo/.refugio-oculto/canasta/botella-vacia"},
        {"path": "~/pueblo/.refugio-oculto/.cofrecito/MV"},
    ]
    first_time = True

    def check_command(self, line):

        if line in self.allowed_commands:
            self.counter += 1
            self.allowed_commands.remove(line)
            hint = "{{gb:¡Bien hecho! Solo mira un objeto más.}}"

        else:
            if self.first_time:
                hint = ("{{rb:Usa}} {{yb:cat}} {{rb:para mirar dos de los "
                        "objetos a tu alrededor.}}")
            else:
                hint = "{{rb:Usa el comando}} {{yb:%s}} {{rb:para avanzar.}}" \
                    % self.allowed_commands[0]

        level_up = (self.counter >= 2)

        if not level_up:
            self.send_hint(hint)
            self.first_time = False
        else:
            return level_up

    def next(self):
        return 10, 2


class Step2(StepTemplateCd):
    story = [
        "Pareciera no haber nada aquí más que un montón de comida.",
        "Fíjate si encuentras algo en el {{bb:pueblo}}.\n",
        "Primero, usa {{yb:cd ..}} para {{lb:abandonar}} la {{bb:cocina}}.\n"
    ]
    start_dir = "~/mi-casa/cocina"
    end_dir = "~/pueblo"
    commands = [
        "cd ~/pueblo",
        "cd ~/pueblo/",
        "cd ..",
        "cd ../",
        "cd pueblo",
        "cd pueblo/",
        "cd ../..",
        "cd ../../",
        "cd"
    ]
    num_turns_in_home_dir = 0

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def check_command(self, line):
        if self.get_fake_path() == self.end_dir:
            return True

        hint = ""

        # decide command needed to get to next part of town
        if self.get_fake_path() == '~/mi-casa/cocina' or self.get_fake_path() == '~/mi-casa':

            # If the last command the user used was to get here
            # then congratulate them
            if line == "cd .." or line == 'cd ../':
                hint = ("{{gb:¡Buen trabajo! Ahora repite el último comando usando "
                        "la flecha}} {{ob:ARRIBA}} {{gb:de tu teclado.}}")

            # Otherwise, give them a hint
            else:
                hint = "{{rb:Usa}} {{yb:cd ..}} {{rb:para avanzar hacia el pueblo.}}"

        elif self.get_fake_path() == '~':
            # If they have only just got to the home directory,
            # then they used an appropriate command
            if self.num_turns_in_home_dir == 0:
                hint = "{{gb:¡Genial! Ahora usa}} {{yb:cd pueblo}} {{gb:para ir al pueblo.}}"

            # Otherwise give them a hint
            else:
                hint = "{{rb:Usa}} {{yb:cd pueblo}} {{rb:para entrar al pueblo.}}"

            # So we can keep track of the number of turns they've been in the
            # home directory
            self.num_turns_in_home_dir += 1

        # print the hint
        self.send_hint(hint)

    def next(self):
        return 10, 3


class Step3(StepTemplateCd):
    story = [
        "Usa {{yb:ls}} para {{lb:mirar alrededor}}.\n",
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo"
    commands = "ls"
    hints = ["{{rb:Usa}} {{yb:ls}} {{rb:para mirar tu alrededor en el pueblo.}}"]

    def next(self):
        return 10, 4


class Step4(StepTemplateCd):
    story = [
        "El sitio parece estar desierto.",
        "Sin embargo, pareces escuchar susurros.",
        # TODO make this writing small
        "\n{{wb:?:}} {{Bn:\".....si usan}} {{yb:ls -a}}{{Bn:, nos verán...\"}}",
        "{{wb:?:}} {{Bn:\"..Shhh! ...pueden escuchar....\"}}\n"
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo"
    commands = "ls -a"
    hints = [
        "{{rb:Escuchaste susurros que nombraban}} {{yb:ls -a}}{{rb:, ¡intenta usarlo!}}",
    ]

    def next(self):
        return 10, 5


class Step5(StepTemplateCd):
    story = [
        "Ves un {{bb:.refugio-oculto}} que no has visto antes.\n",
        "{{gb:Algo que empieza con . se encuentra normalmente oculto.\n}}",
        "Parece que los susurros vienen de allí. Intenta entrar.\n"
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "cd .refugio-oculto",
        "cd .refugio-oculto/"
    ]
    hints = [
        "{{rb:Intenta entrar al}} {{lb:.refugio-oculto}} {{rb:usando}} {{yb:cd}}{{rb:.}}",
        "{{rb:Usa el comando}} {{yb:cd .refugio-oculto}} {{rb:para entrar.}}"
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 10, 6


class Step6(StepTemplateCd):
    story = [
        "¿Hay alguien allí? {{lb:Mira alrededor}}.\n"
    ]
    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar a tu alrededor.}}"
    ]

    def next(self):
        return 11, 1
