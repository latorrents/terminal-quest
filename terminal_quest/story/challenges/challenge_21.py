# challenge_21.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.step_helpers import unblock_cd_commands, unblock_commands_with_mkdir_hint, unblock_commands
from terminal_quest.terminals import TerminalMkdir


class StepTemplateMkdir(StepTemplate):
    TerminalClass = TerminalMkdir


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        "{{gb:¡Guau! Construiste un iglú. Ahora tienes el poder mkdir.}}",
        "",
        "Ruth: {{Bb:\"¡Qué increíble! ¡Por favor, ayúdame a construir un refugio!",
        (
            "Podemos construirlo en el}} {{bb:granero}}{{Bb:, así será más fácil meter "
            "a los animales.\"}}"
        ),
        "\n{{lb:Ve}} al {{bb:granero}}."
    ]
    start_dir = "~/granja/taller"
    end_dir = "~/granja/granero"
    deleted_items = [
        "~/granja/taller/Ruth"
    ]
    file_list = [
        {"path": "~/granja/granero/Ruth"}
    ]

    path_hints = {
        "~/granja/taller": {
            "blocked": "\n{{rb:Usa}} {{yb:cd ..}} {{rb:para volver.}}"
        },
        "~/granja": {
            "not_blocked": "\n{{gb:Has salido. Ahora ve al}} {{bb:granero}}{{gb:.}}",
            "blocked": "\n{{rb:Usa}} {{yb:cd granero}} {{rb:para ir al granero.}}"
        }
    }

    def check_command(self, line):
        if self.get_fake_path() == self.end_dir:
            return True
        elif "cd" in line and not self.get_command_blocked():
            hint = self.path_hints[self.get_fake_path()]["not_blocked"]
        else:
            hint = self.path_hints[self.get_fake_path()]["blocked"]

        self.send_hint(hint)

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 21, 2


class Step2(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:\"Tu iglú quedó genial, pero cualquiera podría encontrarlo.\"}}",
        "{{Bb:\"¿Se puede construir algo oculto?\"}}",
        "",
        "{{yb:1: \"Si lo llamamos}} {{bb:refugio-oculto}}{{yb:, quedará oculto.\"}}",
        "{{yb:2: \"Si pones un . al comienzo del nombre, queda oculto.\"}}",
        "{{yb:3: \"Es imposible hacer un refugio oculto.\"}}\n",
        "Usa {{yb:echo}} para decirle a {{bb:Ruth}} cómo hacer un refugio oculto."
    ]
    start_dir = "~/granja/granero"
    end_dir = "~/granja/granero"
    commands = [
        "echo 1",
        "echo 2",
        "echo 3"
    ]
    hints = [
        (
            "Ruth: {{Bb:\"Tendrás que hablar más claro, no entiendo nada de lo que estás "
            "diciendo.\"}}"
        ),
        (
            "{{rb:Usa}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:o}} {{yb:echo 3}} {{rb:para "
            "responderle a Ruth.}}"
        )
    ]

    def _run_at_start(self):
        self.__next_step = 4

    def check_command(self, line):
        if line == "echo 1":
            self.__next_step = 3
            return True
        elif line == "echo 2":
            self.__next_step = 6
            return True
        elif line == "echo 3":
            hint = (
                "\nRuth: {{Bb:\"¿...En serio? ¿Estás seguro de lo que estás diciendo?\"}}"
            )
            self.send_hint(hint)
        else:
            self.send_stored_hint()

    def next(self):
        return 21, self.__next_step


# First fork - try making a hidden shelter
class Step3(StepTemplateMkdir):
    print_text = [
        "{{yb:\"Si lo llamamos}} {{bb:refugio-oculto}}{{yb:, quedará oculto.\"}}"
    ]
    story = [
        (
            "Ruth: {{Bb:\"¿Entonces si lo llamamos}} {{bb:refugio-oculto}} {{Bb:quedará "
            "oculto? Bueno, intentémoslo.\"}}\n"
        ),
        "Intenta {{lb:construir}} un refugio llamado {{bb:refugio-oculto}}."
    ]
    start_dir = "~/granja/granero"
    end_dir = "~/granja/granero"
    commands = [
        "mkdir refugio-oculto",
    ]
    hints = [
        "{{rb:Necesitas construir un refugio llamado}} {{yb:refugio-oculto}}{{rb:.}}",
        "{{rb:Usa el comando}} {{yb:mkdir refugio-oculto}} {{rb:para construir el refugio.}}"
    ]

    def check_command(self, line):
        if line == "mkdir .refugio-oculto":
            hint = (
                (
                    "\nRuth: {{Bb:\"Dijiste que debería llamarse}} {{bb:refugio-oculto}}{{Bb:, no}} "
                    "{{lb:.refugio-oculto}}{{Bb:.\"}}\n{{yb:Presiona la flecha ARRIBA para volver "
                    "al comando anterior y editarlo.}}"
                )
            )
            self.send_hint(hint)
        else:
            return StepTemplateMkdir.check_command(self, line)

    def block_command(self, line):
        return unblock_commands_with_mkdir_hint(line, self.commands)

    def next(self):
        return 21, 4


class Step4(StepTemplateMkdir):
    story = [
        "{{lb:Mira alrededor}} para ver si quedó bien oculto."
    ]
    start_dir = "~/granja/granero"
    end_dir = "~/granja/granero"
    commands = [
        "ls"
    ]
    hints = [
        "{{rb:Mira alrededor con}} {{yb:ls}}{{rb:.}}"
    ]
    ls_a_hint = True

    def check_command(self, line):
        if line == "ls -a" and self.ls_a_hint:
            hint = (
                (
                    "\n{{gb:¡Estás cerca!}} {{ob:Pero para comprobar si ocultaste el "
                    "refugio, no necesitas mirar alrededor}} {{yb:tan de cerca}}{{ob:.}}"
                )
            )
            self.send_hint(hint)
            self.ls_a_hint = False
        else:
            return StepTemplateMkdir.check_command(self, line)

    def next(self):
        return 21, 5


class Step5(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:\"¡Hiciste un}} {{bb:refugio-oculto}}{{Bb:!\"}}",
        "{{Bb:\"...El problema es que yo también puedo verlo. Creo que no funcionó.",
        "¿De qué otra manera puedes construir algo oculto?\"}}",
        "\n{{yb:1: \"Si pones un . delante del nombre, queda oculto.\"}}",
        "{{yb:2: \"Te equivocas. No puedes ver el refugio-oculto, está oculto.\"}}\n",
        "Usa {{yb:echo}} para hablarle a {{bb:Ruth}}.",
    ]
    start_dir = "~/granja/granero"
    end_dir = "~/granja/granero"
    commands = [
        "echo 1"
    ]
    hints = [
        "Ruth: {{Bb:\"Tienes que hablar más claro. No te entiendo.\"}}",
        "{{rb:Usa}} {{yb:echo 1}} {{rb:o}} {{yb:echo 2}} {{rb:para responder.}}"
    ]

    def check_command(self, line):
        if line == "echo 1":
            return True

        elif line == "echo 2":
            hint = (
                "\nRuth: {{Bb:...." +\
                "Cuidado, chico, no soy tonta. Ese refugio no está oculto.\n" +\
                "¿Cómo hago uno que sí lo esté?}}"
            )
            self.send_hint(hint)

        else:
            self.send_stored_hint()

    def next(self):
        return 21, 6


###########################################
# Second fork

class Step6(StepTemplateMkdir):
    print_text = [
        "{{yb:\"Si pones un . delante del nombre, queda oculto.\"}}"
    ]
    story = [
        "Ruth: {{Bb:\"Si llamas al refugio}} {{bb:.refugio}}{{Bb:, ¿estará oculto? ¡Probemos!\"}}\n",
        "{{lb:Construye}} un refugio llamado {{bb:.refugio}}"
    ]
    start_dir = "~/granja/granero"
    end_dir = "~/granja/granero"

    hints = [
        (
            "{{rb:Construye el}} {{bb:.refugio}} {{rb:usando}} {{yb:mkdir .refugio}}{{rb: - "
            "¡no olvides el punto!}}"
        )
    ]
    commands = [
        "mkdir .refugio"
    ]

    def block_command(self, line):
        return unblock_commands_with_mkdir_hint(line, self.commands)

    def next(self):
        return 21, 7


class Step7(StepTemplateMkdir):
    story = [
        "Fíjate si realmente está oculto. Usa {{yb:ls}} para ver si se puede ver."
    ]

    start_dir = "~/granja/granero"
    end_dir = "~/granja/granero"

    commands = [
        "ls"
    ]

    hints = [
        "{{rb:Usa}} {{yb:ls}}{{rb:, no ls -a, para ver si tu refugio está oculto.}}"
    ]

    def next(self):
        return 21, 8


class Step8(StepTemplateMkdir):
    story = [
        "{{gb:Bien, no se ve en el granero.}}\n",
        "¡Ahora mira alrededor con {{yb:ls -a}} para verificar que realmente existe!"
    ]
    start_dir = "~/granja/granero"
    end_dir = "~/granja/granero"
    commands = [
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls -a}} {{rb:para mirar alrededor.}}"
    ]

    def next(self):
        return 21, 9


class Step9(StepTemplateMkdir):
    story = [
        "{{gb:¡Funcionó! Creaste algo oculto con éxito.}}",
        "\nRuth: {{Bb:\"¿Lo lograste? ¡Increíble!\"",
        (
            "\"...lástima que yo no pueda verlo... ¿puedes meterme a mí y a los animales "
            "adentro, por favor?\"}}\n"
        ),
        "{{lb:Mueve}} a todos dentro del {{bb:.refugio}} uno por uno.\n"
    ]
    start_dir = "~/granja/granero"
    end_dir = "~/granja/granero"
    all_commands = [
        "mv Trotter .refugio/",
        "mv Trotter .refugio",
        "mv Daisy .refugio/",
        "mv Daisy .refugio",
        "mv Cobweb .refugio/",
        "mv Cobweb .refugio",
        "mv Ruth .refugio/",
        "mv Ruth .refugio"
    ]

    def block_command(self, line):
        return unblock_commands(line, self.all_commands)

    def check_command(self, line):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if line == 'ls' or line == "ls -a":
            hint = "\n{{gb:Mira a tu alrededor.}}"
            self.send_hint(hint)
            return False

        # check through list of commands
        self.hints = [
            "{{rb:Usa}} {{yb:%s}} {{rb:para avanzar}}" % (self.all_commands[0],)
        ]

        end_dir_validated = self.get_fake_path() == self.end_dir

        # if the validation is included
        if line in self.all_commands and end_dir_validated:

            # Remove both elements, with a slash and without a slash
            if line[-1] == "/":
                self.all_commands.remove(line)
                self.all_commands.remove(line[:-1])
            else:
                self.all_commands.remove(line)
                self.all_commands.remove(line + "/")

            if len(self.all_commands) == 1:
                hint = (
                    "\n{{gb:¡Bien hecho! Mueve a alguien más al}} {{yb:.refugio}}"
                )
            elif len(self.all_commands) > 0:
                hint = "\n{{gb:¡Bien hecho! Mueve a %s más.}}"\
                    % str(len(self.all_commands) // 2)
            else:
                hint = "\n{{gb:Presiona}} {{ob:Enter}} {{gb:para continuar}}"

            self.send_hint(hint)

        else:
            self.send_hint("\n" + self.hints[0])

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def next(self):
        return 21, 10


class Step10(StepTemplateMkdir):
    story = [
        "{{lb:Ve}} dentro del {{bb:.refugio}} junto con {{bb:Ruth}} y los animales."
    ]
    start_dir = "~/granja/granero"
    end_dir = "~/granja/granero/.refugio"
    hints = [
        "{{rb:Escribe}} {{yb:cd .refugio}} {{rb:para ir dentro del}} {{bb:.refugio}}{{rb:.}}"
    ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 21, 11


class Step11(StepTemplateMkdir):
    story = [
        "{{lb:Mira alrededor}} para fijarte si moviste a todos."
    ]
    start_dir = "~/granja/granero/.refugio"
    end_dir = "~/granja/granero/.refugio"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Mira alrededor usando}} {{yb:ls}}{{rb:.}}"
    ]

    def next(self):
        return 22, 1
