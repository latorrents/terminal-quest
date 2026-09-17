# challenge_17.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from terminal_quest.progress import save_app_state_variable, load_app_state_variable

from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file
from terminal_quest.terminals import TerminalMv
from terminal_quest.terminals import TerminalEcho
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.helpers import wrap_in_box


# This is for the challenges that only need ls
class StepTemplateMv(StepTemplate):
    TerminalClass = TerminalMv


# This is for that challenges that need echo
class StepTemplateEcho(StepTemplate):
    TerminalClass = TerminalEcho


# ----------------------------------------------------------------------------------------

class Step1(StepTemplateMv):
    story = [
        (
            "Estás en tu cuarto, frente al {{bb:.cofre}} que contiene todos los comandos "
            "que has aprendido hasta ahora.\n"
        ),
        "¿Tal vez hay algo más oculto en la casa?\n",
        "{{lb:Mira}} el pasillo {{lb:detrás de ti}}. Recuerda: lo que está detrás de ti es {{bb:..}}"
    ]
    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"
    file_list = [
        {"path": "~/granja/granero/Cobweb"},
        {"path": "~/granja/granero/Daisy"},
        {"path": "~/granja/granero/Ruth"},
        {"path": "~/granja/granero/Trotter"},
        {"path": "~/granja/taller/MKDIR"},
        {"path": "~/granja/taller/llave-inglesa"},
        {"path": "~/granja/taller/martillo"},
        {"path": "~/granja/taller/serrucho"},
        {"path": "~/granja/taller/cinta-metrica"},
        {
            "path": "~/granja/casa-de-campo/cama",
            "contents": get_story_file("bed_farmhouse")
        },
        {"path": "~/granja/taller/MKDIR"},
        {"path": "~/mi-casa/cuarto-de-papas/.caja-fuerte/ECHO"},
        {"path": "~/mi-casa/cuarto-de-papas/.caja-fuerte/diario-de-mama"},
        {"path": "~/mi-casa/cuarto-de-papas/.caja-fuerte/mapa"}
    ]
    hints = [
        "{{rb:Mira detrás de ti con}} {{yb:ls ../}}"
    ]
    commands = [
        "ls ..",
        "ls ../"
    ]

    def next(self):
        return 17, 2


class Step2(StepTemplateMv):
    story = [
        "Ves las puertas del {{bb:jardin}}, {{bb:cocina}}, {{bb:mi-cuarto}} y {{bb:cuarto-de-papas}}.",
        "Todavía no hemos revisado el cuarto de tus padres.\n",
        "{{lb:Entra en el}} {{bb:cuarto-de-papas}}."
    ]

    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/cuarto-de-papas"

    path_hints = {
        "~/mi-casa/mi-cuarto": {
            "blocked": "\n{{rb:Usa}} {{yb:cd ..}} {{rb:para volver.}}"
        },
        "~/mi-casa": {
            "not_blocked": "\n{{gb:Ahora ve al}} {{lb:cuarto-de-papas}}{{gb:.}}",
            "blocked": "\n{{rb:Usa}} {{yb:cd cuarto-de-papas}} {{rb:para entrar.}}"
        }
    }

    def check_command(self, line):
        if self._location.get_fake_path() == self.end_dir:
            return True
        elif "cd" in self.get_last_user_input() and not self.get_command_blocked():
            hint = self.path_hints[self._location.get_fake_path()]["not_blocked"]
        else:
            hint = self.path_hints[self._location.get_fake_path()]["blocked"]

        self.send_hint(hint)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        Step3()

    def next(self):
        return 17, 3


class Step3(StepTemplateMv):
    story = [
        "Mira alrededor {{lb:más de cerca}}."
    ]
    start_dir = "~/mi-casa/cuarto-de-papas"
    end_dir = "~/mi-casa/cuarto-de-papas"

    hints = [
        "{{rb:Usa el comando}} {{yb:ls -a}} {{rb:para mirar alrededor más de cerca.}}"
    ]
    commands = [
        "ls -a",
        "ls -a .",
        "ls -a ./"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 17, 4


class Step4(StepTemplateMv):
    story = [
        "¡Hay una {{bb:.caja-fuerte}}!\n",
        "Puede haber algo útil aquí. {{lb:Mira dentro}} de la {{bb:.caja-fuerte}}."
    ]

    commands = [
        "ls .caja-fuerte",
        "ls .caja-fuerte/",
        "ls -a .caja-fuerte",
        "ls -a .caja-fuerte/"
    ]
    start_dir = "~/mi-casa/cuarto-de-papas"
    end_dir = "~/mi-casa/cuarto-de-papas"
    hints = [
        "{{rb:Mira dentro de la}} {{bb:.caja-fuerte}} {{rb:usando}} {{lb:ls}}{{rb:.}}",
        "{{rb:Usa}} {{yb:ls .caja-fuerte}} {{rb:para mirar dentro de la caja fuerte.}}"
    ]

    def next(self):
        return 17, 5


class Step5(StepTemplateMv):
    story = [
        "Encontraste el diario de tu mamá: {{bb:diario-de-mama}}",
        "No deberías leerlo...\n",
        "¿Qué más hay aquí? Vamos a {{lb:examinar}} ese {{bb:mapa}}."
    ]
    start_dir = "~/mi-casa/cuarto-de-papas"
    end_dir = "~/mi-casa/cuarto-de-papas"
    hints = [
        "{{rb:Usa}} {{yb:cat}} {{rb:para leer el}} {{bb:mapa}}{{rb:.}}",
        "{{rb:Usa}} {{yb:cat .caja-fuerte/mapa}} {{rb:para leer el mapa.}}"
    ]

    commands = "cat .caja-fuerte/mapa"

    def check_command(self, line):
        checked_diary = load_app_state_variable("terminal-quest", "checked_mums_diary")
        if line == 'cat .caja-fuerte/diario-de-mama' and not checked_diary:
            self.send_hint("\n{{rb:¡Leíste el diario íntimo de tu mamá!}} {{ob:Tu travesura quedó registrada.}}")
            save_app_state_variable("terminal-quest", "checked_mums_diary", True)
            return False

        return StepTemplateMv.check_command(self, line)

    def next(self):
        return 17, 6


class Step6(StepTemplateMv):
    story = [
        "¿Hay una granja por aquí cerca?",
        "Parece que no está lejos de tu casa, siguiendo la carretera ventosa...\n",
        "¿Qué es esta nota {{bb:ECHO}}? {{lb:Examina}} la nota {{bb:ECHO}}."
    ]

    start_dir = "~/mi-casa/cuarto-de-papas"
    end_dir = "~/mi-casa/cuarto-de-papas"
    commands = "cat .caja-fuerte/ECHO"
    hints = [
        "{{rb:Usa}} {{yb:cat}} {{rb:para leer la nota}} {{bb:ECHO}}{{rb:.}}",
        "{{rb:Usa}} {{yb:cat .caja-fuerte/ECHO}} {{rb:para leer la nota.}}"
    ]

    def next(self):
        return 17, 7


class Step7(StepTemplateEcho):
    story = [
        "La nota dice {{Bb:\"echo hola - te ayudará a decir hola\"}}",
        "Probémoslo. \n",
    ]
    story += wrap_in_box([
        "{{gb:Nuevo Poder}}: {{yb:echo}} seguido de palabras",
        "te permite {{lb:hablar}}",
    ])

    hints = [
        "{{rb:Usa el comando}} {{yb:echo hola}}"
    ]
    commands = [
        "echo hola",
        "echo HOLA",
        "echo Hola",
        "echo hello",
        "echo HELLO",
        "echo Hello"
    ]
    highlighted_commands = ['echo']
    start_dir = "~/mi-casa/cuarto-de-papas"
    end_dir = "~/mi-casa/cuarto-de-papas"

    def next(self):
        return 18, 1
