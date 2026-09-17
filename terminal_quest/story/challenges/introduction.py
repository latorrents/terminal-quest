# introduction.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os
from terminal_quest.terminals import Terminal
from terminal_quest.step import StepTemplate


class StepTemplateLs(StepTemplate):
    TerminalClass = Terminal


class Step1(StepTemplateLs):
    story = [
        "Hola {}.".format("{{yb:" + os.environ['LOGNAME'] + "}}"),
        "Bienvenido a la Terminal.",
        "Un mundo salvaje y maravilloso donde las palabras tienen poder. Estas palabras se llaman comandos.",
        "¿Quieres nuevos poderes? Presiona {{gb:Enter}} para comenzar."
    ]
    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"

    def next(self):
        return 1, 1
