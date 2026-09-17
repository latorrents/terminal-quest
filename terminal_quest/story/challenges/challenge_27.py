# challenge_27.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.common import get_story_file
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.helpers import wrap_in_box
from terminal_quest.story.challenges.CompanionMisc import StepTemplateMkdir, StepTemplateNano


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        "Te encuentras nuevamente en la tienda de {{bb:Bernard}}.\n",
        "{{lb:Escucha}} lo que {{bb:Bernard}} tiene para decir."
    ]

    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"

    hints = [
        "{{rb:Usa}} {{yb:cat Bernard}} {{rb:para interactuar con Bernard.}}"
    ]

    commands = [
        "cat Bernard"
    ]

    deleted_items = ["~/pueblo/este/biblioteca/Eleanor"]
    file_list = [
        {
            "path": "~/pueblo/este/tienda-de-cobertizos/Eleanor",
            "contents": get_story_file("Eleanor"),
            "type": "file"
        }
    ]
    companion_speech = (
        "Eleanor: {{Bb:\"¡Achís! Este lugar está sucio...*sniff*\"}}"
    )

    def next(self):
        return 27, 2


class Step2(StepTemplateNano):
    story = [
        "Bernard: {{Bb:\"Holaaaaaa. ¿Volvieron para arreglar mi utensilio?\"}}\n ",
    ]
    story += wrap_in_box([
        "{{gb:Nuevo Poder}}: {{yb:nano}} seguido de un",
        "objeto te permite {{lb:editarlo}}",
    ])
    story += [
        "Intenta usar {{yb:nano la-mejor-bocina-del-mundo.sh}} para editarlo.",
    ]

    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"

    commands = [
        "nano la-mejor-bocina-del-mundo.sh"
    ]
    highlighted_commands = ['nano']

    hints = [
        "{{rb:Usa}} {{yb:nano la-mejor-bocina-del-mundo.sh}} {{rb:para editar el utensilio.}}"
    ]

    companion_speech = (
        "Eleanor: {{Bb:Nos enseñaron a escribir en la escuela. No creo que Bernard sea "
        "muy inteligente.}}"
    )

    def _setup_nano(self):
        self._nano.set_goal_nano_save_name("la-mejor-bocina-del-mundo.sh")
        self._nano.set_goal_nano_end_content("echo \"Piii!\"")
        self._nano.set_goal_nano_filepath("~/pueblo/este/tienda-de-cobertizos/la-mejor-bocina-del-mundo.sh")

    def check_command(self, line):
        if line == "cat Eleanor":
            self.send_hint("\n" + self.companion_speech)
        else:
            return self._nano.check_nano_input()

    def check_nano_contents(self):
        return self._nano.check_nano_content_default()

    def next(self):
        return 27, 3


class Step3(StepTemplateNano):
    story = [
        "¡Es hora de poner a prueba tu comando!",
        "Usa {{yb:./la-mejor-bocina-del-mundo.sh}} para ejecutarlo."
    ]

    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"

    commands = [
        "./la-mejor-bocina-del-mundo.sh"
    ]

    companion_speech = "Eleanor: {{Bb:¿Sonará fuerte?}}"
    hints = [
        "{{rb:Usa}} {{yb:./la-mejor-bocina-del-mundo.sh}} {{rb:para ejecutar el comando.}}"
    ]

    def next(self):
        return 27, 4


class Step4(StepTemplateNano):
    # Allow the user to ask all the questions within the same Step?
    story = [
        "{{gb:Felicitaciones, el comando ahora dice \"Piii!\"}}",

        "\nBernard: {{Bb:\"¡El utensilio está funcionando! ¡Fantástico! ¡Muchas gracias!\"}}",

        "\nSe te ocurre que no le has preguntado a {{bb:Bernard}} acerca de él.",

        "¿Qué te gustaría preguntarle?",

        "\n{{yb:1: \"¿Cómo creaste tus utensilios?\"}}",

        "{{yb:2: \"¿Cuál será el próximo utensilio que crearás?\"}}",

        "{{yb:3: \"¿Te esconderás ahora?\"}}",

        "{{yb:4: \"¿Qué hay en el sótano?\"}}",

        "\nUsa {{yb:echo}} para hacerle la pregunta."
    ]

    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"
    hints = [
        (
            "{{rb:Usa}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}}{{rb:,}} {{yb:echo 3}} {{rb:o}} "
            "{{yb:echo 4}}"
        )
    ]

    companion_speech = "Eleanor: {{Bb:\"Yo tengo una pregunta: ¿tendrá caramelos en el sótano?\"}}"

    commands = [
        "echo 2"
    ]

    def check_command(self, line):
        if line == "echo 1":
            text = (
                "\nBernard: {{Bb:\"Ah, secreto profesional. *guiño*\"}}"
            )
            self.send_hint(text)
        elif line == "echo 3":
            text = (
                "\nBernard: {{Bb:\"Er, ¿qué? No, no estaba planeando hacerlo. ¿Por qué debería hacer eso?\"}}"
            )
            self.send_hint(text)
        elif line == "echo 4":
            text = (
                "\nBernard: {{Bb:\"Oh ho ho ho, eso no te interesa.\"}}"
            )
            self.send_hint(text)
        else:
            return StepTemplateNano.check_command(self, line)

    def next(self):
        return 27, 5


class Step5(StepTemplateNano):
    print_text = [
        "{{yb:\"¿Cuál será el próximo utensilio que crearás?\"}}"
    ]

    story = [
        (
            "Bernard: {{Bb:\"Quisiera saber cómo es que cierran la}} {{bb:seccion-privada}} {{Bb:"
            "de la}} {{bb:biblioteca}}{{Bb:, y luego crear una llave para abrirla.\"}}"
        ),

        (
            "\nEleanor: {{Bb:\"Me imagino que la}} {{bb:bibliotecaria}} {{Bb:es quien cierra la "
            "sección privada.\"}}"
        ),

        "{{Bb:\"¿Tal vez puede decirnos cómo lo hace? Deberíamos buscarla.\"}}",

        "\n{{lb:Sal}} de la {{bb:tienda-de-cobertizos}}."
    ]

    hints = [
        "{{rb:Usa}} {{yb:cd ..}} {{rb:para}} {{lb:volver}} {{rb:al pueblo.}}"
    ]
    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este"
    companion_speech = \
        (
            "Eleanor: {{Bb:\"¿Qué crees que esconde la seccion-privada?}}\n{{Bb:Tal vez Bernard "
            "no debería saberlo...\"}}"
        )

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 28, 1
