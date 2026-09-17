# challenge_2.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from terminal_quest.step import StepTemplate
from terminal_quest.progress import save_app_state_variable
from terminal_quest.helpers import wrap_in_box
from terminal_quest.terminals import TerminalCat


class StepCat(StepTemplate):
    TerminalClass = TerminalCat


# ----------------------------------------------------------------------------------------


class Step1(StepCat):
    story = [
        "Increíble, ahora puedes ver los objetos a tu alrededor. ",
        "Allí está tu {{bb:cama}}, tu {{bb:despertador}}... ",
        "¡Euuughh...apaga ese {{bb:despertador}}, por favor! \n",
    ]

    story += wrap_in_box([
        "{{gb:Nuevo Poder}}: para {{lb:examinar}} objetos, escribe",
        "{{yb:cat}} y el nombre del objeto.",
    ])

    story += [
        "Usa {{yb:cat despertador}} para {{lb:examinar}} el {{bb:despertador}}."
    ]

    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"
    commands = "cat despertador"
    highlighted_commands = ['cat']
    hints = ["{{rb:Escribe}} {{yb:cat despertador}} {{rb:para investigar el despertador.}}"]

    def next(self):
        return 2, 2


class Step2(StepCat):
    story = [
        "Ok - está apagado. Mejor vístete...\n",

        "Escribe {{yb:ls armario/}} para {{lb:mirar dentro}} de tu {{bb:armario}}.\n"
    ]
    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"
    commands = ["ls armario", "ls armario/"]
    hints = [
        "{{rb:Escribe}} {{yb:ls armario/}} {{rb:para buscar ropa para ponerte.}}"
    ]

    def next(self):
        return 2, 3


class Step3(StepCat):
    story = [
        "¡Mira esa {{bb:camiseta}}!\n",
        "{{lb:Examina}} la {{bb:camiseta}} con {{yb:cat armario/camiseta}} para ver cómo te sienta.\n"
    ]
    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"
    commands = "cat armario/camiseta"
    hints = [
        "{{rb:Escribe}} {{yb:cat armario/camiseta}} {{rb:para averiguar cómo se ve.}}"
    ]

    def next(self):
        return 2, 4


class Step4(StepCat):
    story = [
        "¡Se ve bien! Póntela y busca algo más.\n",
        "{{lb:Examina}} la {{bb:falda}} o los {{bb:pantalones}}.\n"
    ]
    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"
    commands = [
        "cat armario/falda",
        "cat armario/pantalones"
    ]
    hints = [
        (
            "{{rb:Escribe}} {{yb:cat armario/pantalones}} {{rb:o}} {{yb:cat armario/falda}} "
            "{{rb:para vestirte.}}"
        )
    ]
    checked_outside_wardrobe = False

    def check_command(self, line):
        if line == self.commands[0]:
            save_app_state_variable('terminal-quest', 'outfit', 'falda')
        elif line == self.commands[1]:
            save_app_state_variable('terminal-quest', 'outfit', 'pantalones')
        elif not self.checked_outside_wardrobe and (line == "cat pantalones" or line == "cat falda"):
            self.send_hint("\n{{rb:Necesitas mirar dentro de tu}} {{bb:armario}} {{rb:para ver ese objeto.}}")
            self.checked_outside_wardrobe = True

        return StepCat.check_command(self, line)

    def next(self):
        return 2, 5


class Step5(StepCat):
    story = [
        "¡Genial, ya casi estás listo para la aventura!\n",
        "Finalmente, échale un vistazo a esa {{bb:gorra}}.\n"
    ]
    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"
    commands = [
        "cat armario/gorra"
    ]
    hints = [
        "{{rb:Escribe}} {{yb:cat armario/gorra}} {{rb:para}} {{lb:examinar}} {{rb:la gorra.}}"
    ]

    last_step = True

    def next(self):
        return 3, 1
