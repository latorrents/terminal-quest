#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.location import generate_real_path
from terminal_quest.common import get_username
from terminal_quest.helpers import has_write_permissions
from terminal_quest.step_helpers import unblock_commands
from terminal_quest.terminals import TerminalRm


class StepTemplateRm(StepTemplate):
    TerminalClass = TerminalRm
    dark_theme = True


class StepPeopleInCage(StepTemplateRm):
    commands_done = {
        "cat campana": False,
        "cat Conejo": False
    }

    def check_command(self, line):
        if line in self.commands:
            return StepTemplateRm.check_command(self, line)
        elif line == "cat Conejo":
            self.send_hint("Conejo: {{Bb:...}}\nEl conejo se ve frustrado.")
        elif line == "cat campana":
            self.send_hint("La campana brilla de forma amenazante.")
        elif line.startswith("cat jaula/"):
            self.send_hint(self.cat_people())
        else:
            return StepTemplateRm.check_command(self, line)

    def cat_people(self):
        people = {
            "Mama": "Mama: {{Bb:\"" + get_username() + ", ¡me alegra tanto verte, pero aquí no estás a salvo!\"}}",

            "Papa": "Papa: {{Bb:\"" + get_username() + ", pasó algo rarísimo. ¡Me secuestró un conejo! "
                    "Aunque ahora parece estar actuando todavía más raro.\"}}",

            "hombre-enojado": "hombre-enojado: {{Bb:\"Mis piernas ya están curadas. Espero que mi esposa sepa que estoy bien.\"}}",
            "Alcalde": "Alcalde: {{Bb:\"Cuando salga de aquí, voy a hacer una ley para cazar a todos los conejos.\"}}",
            "chico": "chico: {{Bb:\"¡Extraño a mi mamá!\"}}",
            "chica": "chica: {{Bb:\"No me gusta estar aquí.\"}}",
            "Edith": "Edith: {{Bb:\"¡Tú, " + get_username() + "! ¡Sácanos de aquí!\"}}",
            "Edward": "Edward: {{Bb:\"Edith querida, cálmate...\"}}",
            "perro": "perro: {{Bb:\"¡Guau guau!\"}}",
            "Bernard": "Bernard: {{Bb:\"Después de que te fuiste, oí este sonido\"}}",
            "head-librarian": "bibliotecaria-jefe: {{Bb:\"¿Quién eres?\"}}"
        }
        for person in people:
            if self._last_user_input == "cat jaula/" + person:
                return people[person]

        return ""


class Step1(StepPeopleInCage):
    story = [
        "Estás en la madriguera. {{lb:Mira alrededor.}}"
    ]
    start_dir = "~/bosque/matorral/madriguera"
    end_dir = "~/bosque/matorral/madriguera"

    commands = [
        "ls",
        "ls ./",
        "ls ."
    ]
    hints = [
        "{{rb:Mira alrededor con}} {{yb:ls}}"
    ]

    def next(self):
        return 45, 2


class Step2(StepPeopleInCage):
    story = [
        "Ves al Conejo, pero parece estar distraído.",
        "También hay una jaula y una campana que brilla misteriosamente. Te acercas a escondidas a la jaula.",
        "Espadachin: {{Bb:\"¡Psst! ¡Estamos dentro de la jaula!\"}}",
        "",
        "{{lb:Mira dentro de la jaula.}}"
    ]
    start_dir = "~/bosque/matorral/madriguera"
    end_dir = "~/bosque/matorral/madriguera"
    hints = [
        "{{rb:Usa}} {{yb:ls jaula}} {{rb:para mirar dentro de la jaula.}}"
    ]
    commands = [
        "ls jaula",
        "ls jaula/"
    ]

    def next(self):
        return 45, 3


class Step3(StepPeopleInCage):
    story = [
        "Ves a todas las personas que desaparecieron, muy tristes, dentro de la jaula. ¡Incluidos tu Mama y tu Papa!",
        "Espadachin: {{Bb:\"Oye, escucha. Tengo algo que decirte.\"}}",
        "",
        "Habla con tu Mama y tu Papa. También puedes escuchar a las demás personas atrapadas. "
        "Y cuando estés listo, escucha lo que el Espadachin tiene que decir."
    ]
    start_dir = "~/bosque/matorral/madriguera"
    end_dir = "~/bosque/matorral/madriguera"
    hints = [
        "{{rb:Usa}} {{yb:cat jaula/Espadachin}} {{rb:para escuchar al Espadachin.}}"
    ]
    commands = [
        "cat jaula/Espadachin"
    ]

    def next(self):
        return 45, 4


class Step4(StepPeopleInCage):
    story = [
        "Espadachin: {{Bb:\"Escucha, no tenemos mucho tiempo. Pero creo que es la campana, "
        "está controlando al Conejo. Tiene poderes misteriosos.\"}}",
        "",
        "{{lb:Examina}} la campana."
    ]
    start_dir = "~/bosque/matorral/madriguera"
    end_dir = "~/bosque/matorral/madriguera"
    hints = [
        "{{rb:Usa}} {{yb:cat campana}} {{rb:para examinar la campana.}}"
    ]
    commands = [
        "cat campana"
    ]

    def next(self):
        return 45, 5


class Step5(StepPeopleInCage):
    story = [
        "La campana brilla de forma amenazante.",
        "",
        "Espadachin: {{Bb:\"El Conejo todavía no descubrió cómo usar el poder que robó. Pero pronto lo hará.\"}}",
        "{{Bb:\"Antes de que lo haga, debes sacarnos de esta jaula, sin hacer ruido.\"}}",
        "",
        "{{lb:Tienes que desbloquear la jaula.}}"
    ]
    start_dir = "~/bosque/matorral/madriguera"
    end_dir = "~/bosque/matorral/madriguera"
    hints = [
        "Espadachin: {{Bb:\"Estamos todos atrapados aquí porque se quitaron los permisos de}} {{lb:escritura}}{{Bb:.\"}}",
        "Espadachin: {{Bb:\"Para volver a agregar los permisos de escritura, usa}} {{yb:chmod +w jaula}}{{Bb:\"}}"
    ]

    def check_command(self, line):
        if has_write_permissions(generate_real_path("~/bosque/matorral/madriguera/jaula")):
            return True
        self.send_stored_hint()

    def next(self):
        return 45, 6


class Step6(StepPeopleInCage):
    story = [
        "Espadachin: {{Bb:\"Ahora muévenos al}} {{bb:~/pueblo}}{{Bb:\"}}",
        "{{Bb:\"Para mover a un grupo grande de personas usa el *. Así:}} {{yb:mv jaula/* ~/pueblo}}{{Bb:\"}}"
    ]
    start_dir = "~/bosque/matorral/madriguera"
    end_dir = "~/bosque/matorral/madriguera"
    hints = [
        "{{rb:Usa}} {{yb:mv jaula/* ~/pueblo}} {{rb:para mover a todos los aldeanos al pueblo.}}"
    ]
    commands = [
        "mv jaula/* ~/pueblo",
        "mv jaula/* ~/pueblo/"
    ]

    def block_command(self, line):
        return unblock_commands(line, self.commands)

    def next(self):
        return 45, 7


class Step7(StepTemplateRm):
    story = [
        "{{lb:Mira en ~/pueblo}} para comprobar que moviste a todas las personas a salvo."
    ]
    start_dir = "~/bosque/matorral/madriguera"
    end_dir = "~/bosque/matorral/madriguera"
    commands = [
        "ls ~/pueblo",
        "ls ~/pueblo/"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls ~/pueblo}} {{rb:para comprobar que moviste a todos.}}"
    ]

    def next(self):
        return 46, 1
