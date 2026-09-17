# challenge_18.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.terminals import TerminalEcho


class StepTemplateEcho(StepTemplate):
    TerminalClass = TerminalEcho


# ----------------------------------------------------------------------------------------

class Step1(StepTemplateEcho):
    story = [
        "¡Guau! ¡Hablaste en voz alta!\n",
        "{{gb:¡Aprendiste el nuevo poder}} {{lb:echo}}{{gb:!}}\n",
        "Tal vez puedas usar este comando para hablar con las personas.",

        "\n¡Ahora vayamos a {{bb:~}} para encontrar la granja!",
        "Escribe {{yb:cd}} solo para volver a la carretera ventosa {{bb:~}}"
    ]

    hints = [
        "{{rb:Usa}} {{yb:cd}} {{rb:solo para volver a}} {{bb:~}}"
    ]

    start_dir = "~/mi-casa/cuarto-de-papas"
    end_dir = "~"

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 18, 2


class Step2(StepTemplateEcho):
    story = [
        (
            "Estás otra vez en la carretera ventosa que es infinita en ambas direcciones. "
            "\n{{lb:Mira alrededor.}}"
        )
    ]
    hints = [
        "{{rb:Mira alrededor con}} {{yb:ls}}{{rb:.}}"
    ]

    commands = [
        "ls",
        "ls -a"
    ]
    start_dir = '~'
    end_dir = '~'

    def next(self):
        return 18, 3


class Step3(StepTemplateEcho):
    story = [
        "A lo lejos, ves una pequeña granja.\n",
        "{{lb:Vayamos}} a la {{bb:granja}}."
    ]

    start_dir = "~"
    end_dir = "~/granja"
    hints = [
        "{{rb:Usa}} {{yb:cd granja}} {{rb:para dirigirte a la granja.}}"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 18, 4


class Step4(StepTemplateEcho):
    story = [
        "Caminas por el sendero hacia la granja.",
        "{{lb:Mira alrededor.}}"
    ]

    commands = "ls"
    start_dir = "~/granja"
    end_dir = "~/granja"
    hints = ["{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"]

    def next(self):
        return 18, 5


class Step5(StepTemplateEcho):
    story = [
        (
            "Estás en la granja, con un {{bb:granero}}, una {{bb:casa-de-campo}} y un gran "
            "{{bb:taller}} a la vista."
        ),
        "El terreno está muy bien cuidado, debe haber gente viviendo aquí.\n",
        "{{lb:Mira alrededor}} y fíjate si encuentras a alguien para hablar."
    ]
    start_dir = "~/granja"
    end_dir = "~/granja"
    counter = 0

    def finished_challenge(self, line):
        output = self.check_output(line)
        if not output:
            # If Ruth not in output, check if command is ls
            self.check_command(line)

        return output

    def output_condition(self, output):
        if 'Ruth' in output:
            return True

        return False

    def check_command(self, line):
        if line == 'ls' or 'ls ' in line:
            self.counter += 1

            if self.counter >= 3:
                self.send_hint("\n{{rb:Usa}} {{yb:ls granero}} {{rb:para mirar dentro del granero.}}")
            if self.counter == 2:
                self.send_hint("\n{{rb:¿Ya miraste dentro del}} {{bb:granero}}{{rb:?}}")
            elif self.counter == 1:
                self.send_hint("\n{{rb:No hay nadie aquí. Busca en otro lugar.}}")

        else:
            self.send_hint("\n{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}")

    def block_command(self, line):
        if "mv" in line:
            return True

    def next(self):
        return 18, 6


class Step6(StepTemplateEcho):

    story = [
        "En el {{bb:granero}}, ves a una mujer atendiendo a unos animales.",
        "{{lb:Camina}} dentro del {{bb:granero}} para poder ver más de cerca."
    ]

    start_dir = "~/granja"
    end_dir = "~/granja/granero"
    hints = [
        "{{rb:Usa}} {{yb:cd granero}} {{rb:para ir al granero.}}"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 18, 7


class Step7(StepTemplateEcho):

    story = [
        "{{lb:Examina}} a todos en el {{bb:granero}} usando el comando {{yb:cat}}."
    ]

    all_commands = {
        "cat Ruth": "Ruth: {{Bb:\"¡Ah! ¿¡Quién eres!?\"}}",
        "cat Cobweb": "Cobweb: {{Bb:\"Iiiiiiih.\"}}",
        "cat Trotter": "Trotter: {{Bb:\"Oink Oink.\"}}",
        "cat Daisy": "Daisy: {{Bb:\"Mooooooooo.\"}}"
    }

    start_dir = "~/granja/granero"
    end_dir = "~/granja/granero"

    hints = [
        "{{rb:Si olvidaste quién está en el granero, usa}} {{yb:ls}} {{rb:para recordarlo.}}"
    ]

    # TODO: move this into step_helper_functions, used a few too many times outside.
    def check_command(self, line):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if line == 'ls':
            hint = "\n{{gb:Mira a tu alrededor.}}"
            self.send_hint(hint)
            return False

        # check through list of commands
        end_dir_validated = self.get_fake_path() == self.end_dir

        # if the validation is included
        if self._last_user_input in self.all_commands.keys() and \
                end_dir_validated:

            # Print hint from person
            hint = "\n" + self.all_commands[self._last_user_input]

            self.all_commands.pop(self._last_user_input, None)

            if len(self.all_commands) == 1:
                hint += "\n{{gb:¡Bien hecho! Examina a alguien más.}}"
            elif len(self.all_commands) > 0:
                hint += "\n{{gb:¡Bien hecho! Examina a %d más.}}" % len(self.all_commands)
            else:
                hint += "\n{{gb:Presiona}} {{ob:Enter}} {{gb:para continuar.}}"

            self.send_hint(hint)

        else:
            if not self.hints:
                self.hints = [
                    "{{rb:Usa}} {{yb:%s}} {{rb:para avanzar.}}" % list(self.all_commands.keys())[0]
                ]
            self.send_stored_hint()
            self.hints.pop()
        return False

    def next(self):
        return 19, 1
