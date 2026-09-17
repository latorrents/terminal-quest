# challenge_6.py
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
        "Contémosle a {{bb:Mama}} sobre {{bb:Papa}}. Escribe {{yb:cat Mama}}"
    ]
    start_dir = "~/mi-casa/cocina"
    end_dir = "~/mi-casa/cocina"
    commands = "cat Mama"
    hints = [(
        "{{rb:Para hablar con tu Mamá, escribe}} {{yb:cat Mama}} {{rb:y presiona}} "
        "{{ob:Enter}}{{rb:.}}"
    )]

    def next(self):
        return 6, 2


class Step2(StepTemplateCd):
    story = [
        "{{wb:Mamá:}} {{Bb:\"¿No lo has encontrado? Qué extraño, nunca se va de casa sin avisarme.\"",
        (
            "\"Tal vez se fue a la reunión del pueblo con el Alcalde, aquella de la que "
            "hablaban en las noticias. ¿Por qué no vas a ver? Yo me quedaré por si "
            "regresa.\"}}\n"
        ),
        "Vamos al {{bb:pueblo}}. Para abandonar la casa usa {{yb:cd}} solo."
    ]
    start_dir = "~/mi-casa/cocina"
    end_dir = "~"
    commands = "cd"
    hints = ["{{rb:Escribe}} {{yb:cd}} {{rb:para comenzar el viaje.}}"]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 6, 3


class Step3(StepTemplateCd):
    story = [
        "Estás fuera de la casa y en la larga y ventosa carretera llamada Tilde, o {{bb:~}}",
        "{{lb:Mira alrededor}} otra vez para ver a dónde ir."
    ]
    start_dir = "~"
    end_dir = "~"
    commands = "ls"
    hints = ["{{rb:Escribe}} {{yb:ls}} {{rb:para mirar alrededor.}}"]

    def next(self):
        return 6, 4


class Step4(StepTemplateCd):
    story = [
        "¡Puedes ver el {{bb:pueblo}} a la distancia! {{lb:Ve}} usando {{yb:cd}}."
    ]
    start_dir = "~"
    end_dir = "~/pueblo"
    commands = ["cd pueblo", "cd pueblo/"]
    hints = ["{{rb:Escribe}} {{yb:cd pueblo}} {{rb:para caminar hacia el pueblo.}}"]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 7, 1
