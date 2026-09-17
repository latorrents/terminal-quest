#!/usr/bin/env python
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.animation import Animation
from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file, get_username
from terminal_quest.helpers import wrap_in_box
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.terminals import TerminalSudo
from terminal_quest.terminals import TerminalRm


class StepTemplateRm(StepTemplate):
    TerminalClass = TerminalRm


class StepTemplateSudo(StepTemplate):
    TerminalClass = TerminalSudo


class Step1(StepTemplateRm):
    story = [
        "{{gb:¡Brillante! Salvaste a todos los aldeanos.}}",
        "Estás solo con el Conejo y la campana. El Conejo se da vuelta furioso y empieza a correr hacia ti.",
        "",
        "Es hora de terminar con esto. {{lb:Elimina la campana.}}"
    ]

    start_dir = "~/bosque/matorral/madriguera"
    end_dir = "~/bosque/matorral/madriguera"
    commands = [
        "rm campana"
    ]
    hints = [
        "{{rb:Usa}} {{yb:rm campana}} {{rb:para eliminar la campana.}}"
    ]
    dark_theme = True

    def block_command(self, line):
        if line == "rm Conejo":
            print("¡El conejo esquivó el ataque!")
            return True
        return StepTemplateRm.block_command(self, line)

    def check_command(self, line):
        if self.get_last_user_input() == "rm Conejo":
            self.send_hint(
                "{{lb:¡El conejo esquivó el ataque!}} {{rb:Elimina la campana con}} {{yb:rm campana}}"
            )
            return

        return StepTemplateRm.check_command(self, line)

    def next(self):
        Animation("gong-being-removed").play_finite(1)
        self.send_normal_theme()
        Animation("rabbit-blinking").play_finite(1)
        return 46, 2


class Step2(StepTemplateRm):
    story = [
        "El conejo se detiene. La furia de sus ojos se desvanece y en su lugar aparece la confusión.",
        "",
        "El Espadachin entra corriendo en la {{bb:madriguera}}.",
        "",
        "Espadachin: {{Bb:\"¡Lo lograste! El conejo está libre de la campana maldita, ¡y salvaste a todos!\"}}",
        "",
        "{{Bb:\"¿Ya miraste dentro del}} {{bb:cofre}} {{Bb:que robó el conejo? Está justo aquí.\"}}"
    ]
    start_dir = "~/bosque/matorral/madriguera"
    end_dir = "~/bosque/matorral/madriguera"
    commands = [
        "cat cofre/pergamino"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cat cofre/pergamino}} {{rb:para examinar el contenido.}}"
    ]
    deleted_items = [
        "~/bosque/matorral/madriguera/Conejo"
    ]

    file_list = [
        {
            "path": "~/bosque/matorral/madriguera/Espadachin",
            "contents": get_story_file("swordmaster-without-sword")
        },
        {
            "path": "~/bosque/matorral/madriguera/Conejo",
            "contents": get_story_file("Rabbit-cute")
        }
    ]

    def check_command(self, line):
        if line == "cat cofre/nota-rota":
            return False
        return StepTemplateRm.check_command(self, line)

    def next(self):
        return 46, 3


class Step3(StepTemplateSudo):
    story = wrap_in_box([
        "{{gb:Nuevo Poder:}} Usa {{yb:sudo}} para",
        " {{lb:convertirte en Super Usuario.}}"
    ])
    story += [
        "Pruébalo. Usa {{yb:sudo ls}} para mirar alrededor.",
        "Te pedirá una contraseña.",
        "",
        "Espadachin: {{Bb:El Conejo no pudo adivinar la contraseña.}}",
        "{{Bb:¿Puedes descubrirla tú?}}",
        "",
        "Consejo: La contraseña será invisible para mantenerla en secreto. Parecerá que no escribiste nada, así que ten cuidado."
    ]
    commands = [
        "sudo ls",
        "sudo ls .",
        "sudo ls ./"
    ]
    start_dir = "~/bosque/matorral/madriguera"
    end_dir = "~/bosque/matorral/madriguera"
    hints = [
        "{{rb:¡Inténtalo de nuevo! Usa}} {{yb:sudo ls}}{{rb:. La contraseña predeterminada es}} {{yb:password}}"
        "{{rb:. Si cambiaste la contraseña, prueba con esa.}}"
    ]

    def next(self):
        return 46, 4


class Step4(StepTemplateSudo):
    story = [
        "Espadachin: {{Bb:\"Vaya, sí que tienes talento. Quizás no notaste el cambio, pero ¡te convertiste en "
        "Super Usuario por un instante!}}",
        "{{Bb:Conocer este comando te da el poder de hacer cosas cuando todo lo demás falla.\"}}",
        "",
        "{{gb:¡Bien hecho, aprendiste el poder de}} {{yb:sudo}}{{gb:!}}",
        "",
        "Espadachin: {{Bb:\"Deberías convertirte en Super Usuario y}} {{lb:eliminar}} {{Bb:este cofre para que no vuelva a caer en manos enemigas.}}",
        "{{Bb:Para borrar el cofre entero, usa}} {{yb:sudo rm -r cofre/}}{{Bb:. La opción -r se usa para directorios.\"}}"
    ]
    commands = [
        "sudo rm -r cofre",
        "sudo rm -r cofre/"
    ]
    start_dir = "~/bosque/matorral/madriguera"
    end_dir = "~/bosque/matorral/madriguera"
    hints = [
        "{{rb:Usa}} {{yb:sudo rm -r cofre}} {{rb:para eliminar el cofre y su contenido.}}"
    ]

    def next(self):
        return 46, 5


class Step5(StepTemplateSudo):
    story = [
        "Espadachin: {{Bb:\"¡Bien hecho!\"}}",
        "{{Bb:\"Volvamos al}} {{bb:~/pueblo}}{{Bb:. ¡Todos querrán darte las gracias!\"}}"
    ]

    start_dir = "~/bosque/matorral/madriguera"
    end_dir = "~/pueblo"
    file_list = [
        {
            "path": "~/pueblo/Ruth",
            "contents": get_story_file("Ruth")
        },
        {
            "path": "~/pueblo/Clara",
            "contents": get_story_file("Clara")
        },
        {
            "path": "~/pueblo/Eleanor",
            "contents": get_story_file("Eleanor")
        }
    ]

    def block_command(self, last_user_input):
        return unblock_cd_commands(last_user_input)

    def next(self):
        return 46, 6


class Step6(StepTemplateSudo):
    story = [
        "La gente del pueblo te aclama mientras entras al pueblo.",
        "{{lb:Mira alrededor.}}"
    ]
    commands = [
        "ls"
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo"

    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]

    file_list = [
        {
            "path": "~/pueblo/Conejo",
            "contents": get_story_file("Rabbit-cute")
        },
        {
            "path": "~/pueblo/Espadachin",
            "contents": get_story_file("swordmaster-without-sword")
        }
    ]

    deleted_items = [
        "~/bosque/matorral/madriguera/Conejo",
        "~/bosque/matorral/madriguera/Espadachin"
    ]

    def next(self):
        return 46, 7


class Step7(StepTemplateSudo):
    story = [
        "Ves a tu Mama, a tu Papa y a todos los que conociste en tu aventura. Te rodean en la calle "
        "aplaudiendo y festejando.",
        "{{lb:Habla con todos.}}"
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo"

    hints = [
        ""
    ]

    all_commands = {
        "cat Mama": "Mama: {{Bb:\"¡Salvaste Folderton! ¡Eres un héroe!\"}}",
        "cat Papa": "Papa: {{Bb:\"Estoy muy orgulloso de ti, " + get_username() + ".\"}}",
        "cat Alcalde": "Alcalde: {{Bb:\"Ahora que eres Super Usuario, siempre debes recordar:\n"
                       " 1. Respeta la privacidad de los demás.\n"
                       " 2. Piensa antes de escribir.\n"
                       " 3. Un gran poder conlleva una gran responsabilidad.\"}}"
    }

    other_commands = {
        "cat hombre-enojado": "hombre-enojado: {{Bb:\"Ruth me contó cómo la ayudaste a esconderse a ella y a nuestros animales. "
                            "¡Gracias!}}",
        "cat Ruth": "Ruth: {{Bb:\"Si alguna vez pasas por la granja, ¡te invitamos un vaso de leche!\"}}",
        "cat chico": "chico: {{Bb:\"¡Mamá está a salvo!\"}}",
        "cat chica": "chica: {{Bb:\"Encontramos a Mamá. Me alegra mucho que esté a salvo.\"}}",
        "cat Edith": "Edith: {{Bb:\"¡Me alegra tanto que Eleanor esté a salvo! Gracias por salvarnos a Edward y a mí.\"}}",
        "cat Edward": "Edward: {{Bb:\"Ahora que todo esto terminó, podemos volver a nuestra casa y dejar de vivir "
                        "escondidos.\"}}",
        "cat Eleanor": "Eleanor: {{Bb:\"¡Encontraste a mis papás! Sabía que estarían bien.\"}}",
        "cat perro": "perro: {{Bb:\"¡Guau guau!\"}}",
        "cat Bernard": "Bernard: {{Bb:\"¿Quién es ese Espadachin Enmascarado? Me resulta extrañamente familiar.\"}}",
        "cat Clara": (
            "Clara: {{Bb:\"Eleanor me ayudó a ser valiente, ¡pero estoy tan feliz de que encontraras a mis hijos}} {{bb:chica}} {{Bb:y}} "
            "{{bb:chico}}{{Bb:! ¡Gracias, " + get_username() + "!\"}}"
        ),
        "cat Espadachin": "Espadachin: {{Bb:\"Lo hiciste bien. Eres sin duda alguien a quien hay que tener en cuenta. "
                             "Sigue entrenando y serás todavía más poderoso.\"}}",
        "cat Conejo": "Conejo: {{Bb:....}}"
    }

    def check_command(self, line):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if line == 'ls':
            hint = "\n{{gb:Mira a tu alrededor.}}"
            self.send_hint(hint)
            return False
        elif line in self.other_commands:
            hint = "\n" + self.other_commands[line]
            self.send_hint(hint)
            return False

        # check through list of commands
        self.hints = [
            "{{rb:Usa}} {{yb:%s}} {{rb:para avanzar.}}" % list(self.all_commands.keys())[0]
        ]

        end_dir_validated = self.get_fake_path() == self.end_dir

        if (line in self.all_commands.keys()) and end_dir_validated:
            hint = "\n" + self.all_commands[line]
            self.all_commands.pop(line, None)

            if len(self.all_commands) == 0:
                hint += "\n\n{{gb:Presiona}} {{ob:Enter}} {{gb:para continuar.}}"

            self.send_hint(hint)
        else:
            self.send_stored_hint()

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def next(self):
        from terminal_quest.progress import save_app_state_variable_with_dialog
        save_app_state_variable_with_dialog('terminal-quest', 'finished', 'challenge_46')
        self._is_finished = True
        self.exit()
        return -1, -1
