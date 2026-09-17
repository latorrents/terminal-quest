# challenge_23.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.common import get_story_file
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.terminals import TerminalMkdir
from terminal_quest.story.challenges.CompanionMisc import StepTemplateMkdir as StepEleanorMkdir


class StepTemplateMkdir(StepTemplate):
    TerminalClass = TerminalMkdir

# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        "Ves a {{bb:Eleanor}}. Escucha lo que tiene para decir."
    ]
    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "cat Eleanor"
    ]
    hints = [
        "{{rb:Usa}} {{yb:cat Eleanor}} {{rb:para ver lo que tiene para decir.}}"
    ]
    file_list = [
        {"path": "~/pueblo/este/tienda-de-cobertizos/Bernard"},
        {
            "path": "~/pueblo/este/tienda-de-cobertizos/el-mejor-constructor-de-cobertizos.sh",
            "permissions": 0o755
        },
        {
            "path": "~/pueblo/este/tienda-de-cobertizos/la-mejor-bocina-del-mundo.sh",
            "permissions": 0o755,
            "contents": get_story_file("best-horn-in-the-world-incorrect.sh")
        },
        {"path": "~/pueblo/este/tienda-de-cobertizos/sotano/fotocopiadora.sh"},
        {"path": "~/pueblo/este/tienda-de-cobertizos/sotano/diario-de-bernard-1"},
        {"path": "~/pueblo/este/tienda-de-cobertizos/sotano/diario-de-bernard-2"},
        {"path": "~/pueblo/este/biblioteca/seccion-publica/NANO"},
        {
            "path": "~/pueblo/este/biblioteca/seccion-privada",
            "type": "directory",
            "permissions": 0o000
        },
        {"path": "~/pueblo/este/restaurante/.bodega/Clara"}
    ]

    def next(self):
        return 23, 2


class Step2(StepTemplateMkdir):
    story = [
        "Eleanor: {{Bb:\"¡Oh, eres tú! ¿Has visto a mi Mamá y a mi Papá?\"}}",
        "\n{{yb:1: \"Me temo que no. ¿Cuándo los viste por última vez?\"}}",
        "{{yb:2: \"¿No estaban contigo en el refugio-oculto?\"}}",
        "{{yb:3: \"(mientes) Sí, los he visto en el pueblo.\"}}",
        "\nUsa el comando {{yb:echo}} para hablarle a {{bb:Eleanor}}."
    ]

    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo/.refugio-oculto"
    commands = [
        "echo 1",
        "echo 2",
        "echo 3"
    ]

    def check_command(self, line):
        if line in self.commands:
            return True
        elif line.startswith("echo"):
            text = (
                "\nEleanor: {{Bb:\"¿Disculpa? ¿Qué dijiste?\"}}"
            )
        else:
            text = (
                (
                    "\n{{rb:Usa}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:o}} {{yb:echo 3}} {{rb:para "
                    "responder.}}"
                )
            )

        self.send_hint(text)

    def next(self):
        Step3.prev_command = self._last_user_input
        return 23, 3


class Step3(StepEleanorMkdir):
    start_dir = "~/pueblo/.refugio-oculto"
    end_dir = "~/pueblo"

    hints = [
        "{{rb:Usa}} {{yb:cd ..}} {{rb:para ir al pueblo.}}"
    ]

    companion_speech = (
        "Eleanor: {{Bb:¡Sí, vámonos de aventura!}}"
    )

    def _run_at_start(self):
        self.story = []

        if self.prev_command == "echo 1":
            self.print_text = [
                "{{yb:\"Me temo que no. ¿Cuándo los viste por última vez?\"}}"
            ]
            self.story += [
                "Eleanor: {{Bb:\"Hace poco. El perro se escapó otra vez y salieron a buscarlo.\"}}"
            ]

        elif self.prev_command == "echo 2":
            self.print_text = [
                "{{yb:\"¿No estaban contigo en el refugio-oculto?\"}}"
            ]
            self.story += [
                (
                    "Eleanor: {{Bb:\"No, salieron. El perro se escapó otra vez y salieron a buscarlo. "
                    "¿Tal vez se perdieron?\"}}"
                )
            ]

        elif self.prev_command == "echo 3":
            self.print_text = [
                "{{yb:\"(mientes) Sí, los he visto en el pueblo.\"}}"
            ]
            self.story += [
                "Eleanor: {{Bb:\"¡Ah, qué bueno! El perro se escapó y salieron a buscarlo.\"",
                "\"La campana me asustó, pero me alegra que estén bien.\"\n}}"
            ]

        self.story += [
            "{{Bb:\"Vayamos juntos al pueblo a buscarlos. Creo que estaré segura si voy contigo.\"}}",

            (
                "\n{{gb:¡Eleanor se unió a ti como nueva compañera! Puedes fijarte cómo está "
                "en cualquier momento con}} {{yb:cat Eleanor}}{{gb:.}}"
            ),

            "\n{{lb:Sal}} del {{bb:.refugio-oculto}}. No te preocupes, ¡{{bb:Eleanor}} te seguirá!"
        ]

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 23, 4


class Step4(StepEleanorMkdir):
    start_dir = "~/pueblo"
    end_dir = "~/pueblo"
    hints = [
        "Eleanor: {{Bb:¿Olvidaste cómo mirar alrededor? Tienes que usar}} {{yb:ls}}{{Bb:.}}",

        "{{rb:Mira alrededor con}} {{yb:ls}}{{rb:.}}"
    ]
    commands = [
        "ls",
        "ls -a"
    ]
    deleted_items = ["~/pueblo/.refugio-oculto/Eleanor"]
    file_list = [
        {
            "path": "~/pueblo/Eleanor",
            "contents": get_story_file("Eleanor")
        }
    ]

    story = [
        "Eleanor: {{Bb:\"Vayamos a la parte}} {{bb:este}} {{Bb:del pueblo.\"}}",
        "{{Bb:\"¿No la habías visto? ¡Está por allá! Mira a tu alrededor.\"}}",
        "\nUsa {{yb:ls}} para ver lo que {{bb:Eleanor}} está tratando de mostrarte."
    ]

    companion_speech = (
        "\nEleanor: {{Bb:¿Por qué me miras a mí? Deberías mirar para allá.}}"
    )

    def next(self):
        return 23, 5


class Step5(StepEleanorMkdir):
    story = [
        "Miras hacia donde apunta {{bb:Eleanor}}.",
        "Hay un camino estrecho que lleva a otra parte del pueblo.",
        "Debe llevarnos a la parte {{bb:este}}.\n",
        "Eleanor: {{Bb:\"Vamos a ver si encontramos a mis padres.\"}}",
        "\n{{lb:Ve}} a la parte {{bb:este}} del pueblo."
    ]
    start_dir = "~/pueblo"
    end_dir = "~/pueblo/este"

    hints = [
        "{{rb:Usa}} {{lb:cd}} {{rb:para ir a la parte este del pueblo.}}",
        "{{rb:Usa}} {{yb:cd este}}"
    ]

    companion_speech = (
        "\nEleanor: {{Bb:Vayamos a la parte}} {{lb:este}} {{Bb:del pueblo, compañero.}}"
    )

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 24, 1
