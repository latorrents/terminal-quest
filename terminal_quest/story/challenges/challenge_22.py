# challenge_22.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.terminals import TerminalMkdir


class StepTemplateMkdir(StepTemplate):
    TerminalClass = TerminalMkdir


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        "{{gb:¡Bien hecho, parece que ya están todos adentro!}}",
        "\nRuth: {{Bb:\"¡Muchas gracias!\"}}",
        (
            "{{Bb:\"Nos quedaremos aquí dentro para estar seguros. Estoy muy agradecida por "
            "todo lo que has hecho.\"}}"
        ),
        "\nUsa {{yb:cat}} para fijarte si los animales están bien dentro del refugio."
    ]

    start_dir = "~/granja/granero/.refugio"
    end_dir = "~/granja/granero/.refugio"

    commands = [
        "cat Daisy",
        "cat Trotter",
        "cat Cobweb"
    ]
    hints = [
        (
            "{{rb:Usa}} {{yb:cat}} {{rb:para examinar a un animal, por ejemplo}} {{yb:cat "
            "Daisy}}{{rb:.}}"
        )
    ]

    deleted_items = [
        "~/pueblo/.refugio-oculto/canasta",
        "~/pueblo/.refugio-oculto/manzana"
    ]

    def next(self):
        return 22, 2


class Step2(StepTemplateMkdir):
    story = [
        "{{pb:Ding. Dong.}}\n",
        "Ruth: {{Bb:\"¿Qué? ¡Escuché una campana! ¿Qué significa eso?\"}}",
        "¡Rápido! {{lb:Mira alrededor}} y fíjate si falta alguien."
    ]

    start_dir = "~/granja/granero/.refugio"
    end_dir = "~/granja/granero/.refugio"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Mira alrededor con}} {{yb:ls}}{{rb:.}}"
    ]

    deleted_items = [
        "~/pueblo/.refugio-oculto/Edith"
    ]

    def next(self):
        return 22, 3


class Step3(StepTemplateMkdir):

    story = [
        "Parece que todos siguen aquí...",
        "{{pb:Ding. Dong.}}\n",
        "Ruth: {{Bb:\"¡Lo escuché otra vez! ¿Es el sonido que escuchaste cuando desapareció mi marido?\"\n}}",
        "{{lb:Mira alrededor}} una vez más."
    ]

    start_dir = "~/granja/granero/.refugio"
    end_dir = "~/granja/granero/.refugio"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Mira alrededor con}} {{yb:ls}}{{rb:.}}"
    ]
    deleted_items = [
        "~/pueblo/.refugio-oculto/Edward"
    ]

    def next(self):
        return 22, 4


# TODO: FIX THIS STEP
class Step4(StepTemplateMkdir):
    story = [
        (
            "Ruth: {{Bb:\"Todo está bien. Estamos a salvo, todos seguimos aquí. ¿Por qué "
            "sonará esa campana?\"}}"
        ),
        "Tal vez deberíamos investigar ese sonido. ¿A quién más conocemos?",
        "Tal vez deberías volver a ver a la familia del {{bb:.refugio-oculto}} y hablar con ellos.",
        "",
        "Vuelve al {{bb:.refugio-oculto}} usando {{yb:cd}}."
    ]

    start_dir = "~/granja/granero/.refugio"
    end_dir = "~/pueblo/.refugio-oculto"

    hints = [
        (
            "{{rb:Podemos ir directo al}} {{bb:.refugio-oculto}} {{rb:usando}} {{yb:cd "
            "~/pueblo/.refugio-oculto}}"
        )
    ]

    # Remove the dog
    deleted_items = [
        "~/pueblo/.refugio-oculto/perro"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def check_command(self, line):
        # If the command passes, then print a nice hint.
        if line.startswith("cd") and not self.get_command_blocked() and not self.get_fake_path() == self.end_dir:
            hint = "\n{{gb:Sigue así.}}"
            self.send_hint(hint)
        else:
            return StepTemplateMkdir.check_command(self, line)

    def next(self):
        return 22, 5


class Step5(StepTemplateMkdir):
    story = [
        "{{lb:Mira alrededor}}."
    ]

    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]

    def next(self):
        return 23, 1
