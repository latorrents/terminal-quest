# challenge_14.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
import os
from terminal_quest.helpers import logger
from terminal_quest.step import StepTemplate
from terminal_quest.terminals import TerminalMv
from terminal_quest.common import fake_home_dir
from terminal_quest.step_helpers import unblock_commands_with_cd_hint, unblock_commands


class StepTemplateMv(StepTemplate):
    TerminalClass = TerminalMv


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMv):
    story = [
        "Vamos a {{lb:mirar alrededor}} para ver si hay comida disponible en la {{bb:cocina}}.\n"
    ]
    start_dir = "~/mi-casa/cocina"
    end_dir = "~/mi-casa/cocina"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para}} {{lb:mirar alrededor}} {{rb:de la cocina.}}"
    ]

    def next(self):
        return 14, 2


# Move three pieces of food into the basket
class Step2(StepTemplateMv):
    story = [
        "{{lb:Mueve}} tres piezas de comida a la {{bb:canasta}}.\n",
        "Puedes mover varios objetos a la vez usando {{yb:mv objeto1 objeto2 objeto3 canasta/}}, por ejemplo: mv banana pastel leche canasta/\n"
    ]
    start_dir = "~/mi-casa/cocina"
    end_dir = "~/mi-casa/cocina"
    passable_items = [
        'banana',
        'pastel',
        'croissant',
        'tarta',
        'uvas',
        'leche',
        'sandwich'
    ]
    unmovable_items = {
        "periodico": "{{rb:Te pidieron comida, ¡no se van a comer el periódico!}}",
        "horno": "{{rb:¡Es un poco pesado para que lo cargues!}}",
        "mesa": "{{rb:¡Es un poco pesado para que lo cargues!}}"
    }
    moved_items = []

    def block_command(self, line):
        if not line:
            return False

        separate_words = line.split(' ')
        should_block = False

        if "cd" in line:
            return True   # block the CD command here
        elif "ls" in line:
            return False  # do not block the LS command

        if separate_words[0] == 'mv' and (separate_words[-1] == 'canasta' or
                                          separate_words[-1] == 'canasta/'):
            for item in separate_words[1:-1]:
                if item not in self.passable_items:
                    if item in self.unmovable_items:
                        self.send_hint(self.unmovable_items[item])
                        return True
                    else:
                        hint = (
                            "{{rb:Estás intentando mover algo que no está aquí.\nIntenta usando}} "
                            "{{yb:mv %s canasta/}}"
                        ) % self.passable_items[0]
                        self.send_hint(hint)
                        return True

        else:
            # print a message in the terminal to show that it failed
            print("¡Si no agregas la palabra canasta al final de tu comando, renombrarás los objetos!")

        return should_block

    def check_command(self, line):
        separate_words = line.split(" ")
        all_items = []

        if separate_words[0] == 'mv' and (separate_words[-1] == 'canasta' or
                                          separate_words[-1] == 'canasta/'):
            for item in separate_words[1:-1]:
                all_items.append(item)

            items_moved = 0
            hint = ''

            for item in all_items:
                try:
                    self.passable_items.remove(item)
                    items_moved += 1
                except ValueError as e:
                    logger.debug("Tried removing item {} from list. User might have"
                                 " made a typo - [{}]".format(item, e))

            if items_moved:
                hint = "{{gb:¡Muy bien! Sigue así.}}"

        else:
            hint = "{{rb:Intenta usando}} {{yb:mv %s canasta/}}" % self.passable_items[0]

        self.send_hint(hint)

    # Check that the basket folder contains the correct number of files?
    def check_output(self, output):
        basket_dir = os.path.join(fake_home_dir, 'mi-casa/cocina/canasta')
        food_files = [
            f for f in os.listdir(basket_dir)
            if os.path.isfile(os.path.join(basket_dir, f))
        ]

        if len(food_files) > 3:
            return True
        else:
            return False

    def next(self):
        return 14, 3


class Step3(StepTemplateMv):
    story = [
        "\nAhora debemos volver al {{bb:.refugio-oculto}} con la {{bb:canasta}}.",
        "{{lb:Mueve}} la {{bb:canasta}} de vuelta a {{bb:~}}.\n"
    ]
    start_dir = "~/mi-casa/cocina"
    end_dir = "~/mi-casa/cocina"
    commands = [
        "mv canasta ~",
        "mv canasta/ ~",
        "mv canasta ~/",
        "mv canasta/ ~/"
    ]
    hints = [
        "{{rb:Usa el comando}} {{yb:mv canasta ~/}} {{rb:para moverla a la carretera ventosa}} {{bb:~}}"
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 14, 4


class Step4(StepTemplateMv):
    story = [
        "Sigue a la {{bb:canasta}} usando {{yb:cd}}.\n"
    ]
    start_dir = "~/mi-casa/cocina"
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
        return 14, 5


class Step5(StepTemplateMv):
    story = [
        "Ahora lleva la {{bb:canasta}} llena de comida a la familia.",
        "{{lb:Mueve}} la {{bb:canasta}} al {{bb:pueblo/.refugio-oculto}}.",
    ]

    start_dir = "~"
    end_dir = "~"
    commands = [
        "mv canasta pueblo/.refugio-oculto",
        "mv canasta/ pueblo/.refugio-oculto",
        "mv canasta pueblo/.refugio-oculto/",
        "mv canasta/ pueblo/.refugio-oculto/",
        "mv canasta ~/pueblo/.refugio-oculto",
        "mv canasta/ ~/pueblo/.refugio-oculto",
        "mv canasta ~/pueblo/.refugio-oculto/",
        "mv canasta/ ~/pueblo/.refugio-oculto/"
    ]
    hints = [
        (
            "{{rb:Usa}} {{yb:mv canasta pueblo/.refugio-oculto/}} {{rb:para llevarle la canasta "
            "a la familia.}}"
        )
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 14, 6


class Step6(StepTemplateMv):
    story = [
        "{{lb:Entra}} al {{bb:pueblo/.refugio-oculto}} usando {{yb:cd}}.\n",
    ]

    start_dir = "~"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "cd pueblo/.refugio-oculto",
        "cd pueblo/.refugio-oculto/",
        "cd ~/pueblo/.refugio-oculto",
        "cd ~/pueblo/.refugio-oculto/"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cd pueblo/.refugio-oculto}} {{rb:para reunirte con la familia.}}",
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 14, 7


class Step7(StepTemplateMv):
    story = [
        "{{wn:Usa}} {{yb:cat}} {{wn:para ver si están contentos con la comida.}}\n"
    ]
    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    hints = [
        "{{rb:Usa}} {{yb:cat}}"
    ]
    allowed_commands = {
        "cat Edith": \
            (
                "\n{{wb:Edith:}} {{Bb:\"Has salvado a mi niña y a mi perro, ahora nos has salvado "
                "de morir de hambre...¿cómo podremos agradecerte?\"}}\n"
            ),
        "cat Eleanor": \
            "\n{{wb:Eleanor:}} {{Bb:\"¡Qué rico! ¿Ves? Te dije que alguien nos ayudaría.\"}}\n",
        "cat Edward": \
            (
                "\n{{wb:Edward:}} {{Bb:\"¡Gracias! Sabía que nos serías de gran ayuda. ¡Eres un "
                "verdadero héroe!\"}}\n"
            ),
        "cat perro": \
            "\n{{wb:Perro:}} {{Bb:\"¡Guau!\"}} {{wn:\nEl perro parece estar muy contento.\n}}"
    }

    def check_command(self, line):
        if not self.allowed_commands:
            return True

        if line in self.allowed_commands.keys():

            hint = self.allowed_commands[line]
            del self.allowed_commands[line]
            num_people = len(self.allowed_commands.keys())

            if num_people == 0:
                hint += "\n{{gb:Presiona}} {{ob:Enter}} {{gb:para continuar.}}"

            # If the hint is not empty
            elif hint:
                if num_people > 1:
                    hint += "\n{{gb:Fíjate en}} {{yb:%d}} {{gb:de los otros}}" % num_people
                else:
                    hint += "\n{{gb:Fíjate en}} {{yb:alguien}} {{gb:más}}"
        else:
            hint = "{{rb:Usa}} {{yb:%s}} {{rb:para avanzar.}}" % list(self.allowed_commands.keys())[0]

        self.send_hint(hint)

    def next(self):
        return 15, 1
