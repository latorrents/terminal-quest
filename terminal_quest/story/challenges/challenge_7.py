# challenge_7.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.terminals import TerminalCd


class StepTemplateCd(StepTemplate):
    TerminalClass = TerminalCd


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):
    story = [
        "{{lb:Mira alrededor}} para ver qué está pasando."
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo"
    commands = "ls"
    hints = ["{{rb:Para mirar a tu alrededor usa}} {{yb:ls}}"]

    def next(self):
        return 7, 2


class Step2(StepTemplateCd):
    story = [
        (
            "Wow, hay mucha gente aquí. Encuentra al {{bb:Alcalde}} y {{lb:escucha}} lo que "
            "tiene para decir."
        )
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo"
    commands = "cat Alcalde"
    hints = ["{{rb:Escribe:}} {{yb:cat Alcalde}}"]

    def next(self):
        return 7, 3


class Step3(StepTemplateCd):
    story = [
        (
            "{{wb:Alcalde:}} {{Bb:\"¡Mantengan la calma, por favor! Tenemos a los mejores "
            "buscando a los desaparecidos, y esperamos encontrar una explicación pronto.\"}}\n"
        ),
        "Algo extraño está pasando. Mejor fíjate que todos estén bien.",
        "Escribe {{yb:cat}} para fijarte en las personas."
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo"

    # Use functions here
    command = ""
    all_commands = {
        "cat hombre-enojado": "{{wb:Hombre:}} {{Bb:\"¡Ayuda! No sé qué me está pasando. Escuché sonar una campana, y ahora mis piernas se sienten muy raras.\"}}",
        "cat chica": "{{wb:Chica:}} {{Bb:\"¿Puedes ayudarme? No encuentro a mi amiga Amy por ningún lado. Si la ves, ¿me avisas?\"}}",
        "cat chico": "{{wb:Chico:}} {{Bb:\"¿Pongo? ¿Pongo? ¿Alguien ha visto a mi perro Pongo? Nunca antes se había escapado...\"}}"
    }

    last_step = True

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
        self.hints = [
            "{{rb:Usa}} {{yb:%s}} {{rb:para avanzar.}}" % list(self.all_commands.keys())[0]
        ]

        end_dir_validated = self.get_fake_path() == self.end_dir

        # if the validation is included
        if (line in self.all_commands.keys()) and end_dir_validated:
            # Print hint from person
            hint = "\n" + self.all_commands[line]

            self.all_commands.pop(line, None)

            if len(self.all_commands) == 1:
                hint += "\n{{gb:¡Bien hecho! Fíjate en 1 persona más.}}"
            elif len(self.all_commands) > 0:
                hint += "\n{{gb:¡Bien hecho! Fíjate en %d personas más.}}" % len(self.all_commands)
            else:
                hint += "\n{{gb:Presiona}} {{ob:Enter}} {{gb:para continuar.}}"

            self.send_hint(hint)

        else:
            self.send_stored_hint()

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def next(self):
        return 8, 1
