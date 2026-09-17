# challenge_16.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.terminals import TerminalMv


class StepTemplateMv(StepTemplate):
    TerminalClass = TerminalMv


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMv):
    story = [
        "Hay un antiguo {{bb:.cofre}} oculto debajo de tu cama, no recuerdas haberlo visto antes.\n",
        "Entras en {{bb:mi-cuarto}} para mirar más de cerca.\n",
        "{{lb:Mira dentro}} del {{bb:.cofre}} y fíjate qué contiene."
    ]

    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"

    commands = [
        'ls .cofre',
        'ls .cofre/',
        'ls -a .cofre',
        'ls -a .cofre/',
        'ls .cofre/ -a',
        'ls .cofre -a'
    ]

    hints = [
        "{{rb:Usa}} {{yb:ls .cofre}} {{rb:para mirar dentro del .cofre}}"
    ]

    def next(self):
        return 16, 2


class Step2(StepTemplateMv):
    story = [
        (
            "Hay algunos pergaminos, parecidos al que encontraste en el {{bb:.refugio-oculto}}. "
            "Podrían contener comandos más poderosos.\n"
        ),
        "Usa {{yb:cat}} para {{lb:leer}} uno de los pergaminos.\n"
    ]

    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"

    commands = [
        'cat .cofre/LS',
        'cat .cofre/CAT',
        'cat .cofre/CD'
    ]

    hints = [
        "{{rb:Usa}} {{yb:cat .cofre/LS}} {{rb:para leer el pergamino LS.}}"
    ]

    def next(self):
        return 16, 3


class Step3(StepTemplateMv):
    story = [
        "¿Habrá algo más oculto en este {{lb:.cofre}}?",
        "{{lb:Mira más de cerca}} para encontrar otros objetos."
    ]

    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"

    hints = [
        "{{rb:Usa}} {{yb:ls -a .cofre}} {{rb:para encontrar otros objetos ocultos en el cofre.}}"
    ]

    commands = [
        "ls -a .cofre",
        "ls -a .cofre/",
        'ls .cofre/ -a',
        'ls .cofre -a'
    ]

    def next(self):
        return 16, 4


class Step4(StepTemplateMv):
    story = [
        (
            "De repente encuentras una pequeña {{lb:.nota}} manchada y arrugada en la "
            "esquina del {{lb:.cofre}}."
        ),
        "¿Qué dice?\n"
    ]

    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"

    hints = [
        "{{rb:Usa}} {{yb:cat .cofre/.nota}} {{rb:para leer la}} {{lb:.nota}}{{rb:.}}"
    ]

    commands = [
        "cat .cofre/.nota"
    ]

    def next(self):
        return 17, 1
