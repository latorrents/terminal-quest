# challenge_26.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from terminal_quest.story.challenges.CompanionMisc import StepTemplateMkdir
from terminal_quest.common import get_story_file
from terminal_quest.step_helpers import unblock_cd_commands


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        (
            "Estás otra vez en el pueblo. {{bb:Eleanor}} agita su mano y apunta a un edificio "
            "ubicado a la distancia."
        ),
        "\n{{lb:Mira alrededor}} para ver a dónde apunta {{bb:Eleanor}}."
    ]

    start_dir = "~/pueblo/este"
    end_dir = "~/pueblo/este"

    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]

    commands = [
        "ls",
        "ls -a"
    ]

    deleted_items = ["~/pueblo/este/tienda-de-cobertizos/Eleanor"]
    file_list = [
        {
            "path": "~/pueblo/este/Eleanor",
            "contents": get_story_file("Eleanor"),
            "type": "file"
        }
    ]
    companion_speech = "Eleanor: {{Bb:¡La biblioteca está por allí!}}"

    def next(self):
        return 26, 2


class Step2(StepTemplateMkdir):
    story = [
        "Ves la {{bb:biblioteca}} más adelante.",
        (
            "Eleanor: {{Bb:\"¡Allí está! ¡La}} {{bb:biblioteca}} {{Bb:está justo allí! Vayamos}} "
            "{{lb:dentro.}}{{Bb:\"}}"
        )
    ]

    start_dir = "~/pueblo/este"
    end_dir = "~/pueblo/este/biblioteca"

    hints = [
        "{{rb:Usa}} {{yb:cd biblioteca}} {{rb:para entrar a la biblioteca.}}"
    ]
    companion_speech = "Eleanor: {{Bb:¡Me encanta la biblioteca! ¡Entremos!}}"

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 26, 3


class Step3(StepTemplateMkdir):
    story = [
        "{{bb:Eleanor}} entra a la {{bb:biblioteca}} y tú la sigues.\n",
        "{{lb:Mira alrededor}} de la {{bb:biblioteca}}."
    ]

    start_dir = "~/pueblo/este/biblioteca"
    end_dir = "~/pueblo/este/biblioteca"

    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]
    commands = [
        "ls",
        "ls -a"
    ]
    deleted_items = ["~/pueblo/este/Eleanor"]
    file_list = [
        {
            "path": "~/pueblo/este/biblioteca/Eleanor",
            "contents": get_story_file("Eleanor")
        }
    ]
    companion_speech = "Eleanor: {{Bb:Hay mucho eco-o-o-o-o..}}"

    def next(self):
        return 26, 4


class Step4(StepTemplateMkdir):
    story = [
        (
            "Te encuentras en un pasillo que conduce a dos puertas, cada una con un cartel. "
            "Uno dice {{bb:seccion-publica}}, y el otro {{bb:seccion-privada}}.\n"
        ),

        "Eleanor: {{Bb:\"Solía haber una bibliotecaria aquí.",

        "Me regañaba si me veía intentando entrar a la}} {{bb:seccion-privada}}.",

        "{{Bb:¿Qué crees que haya allí adentro? Intentemos}} {{lb:mirar adentro}}{{Bb:.\"}}"
    ]

    start_dir = "~/pueblo/este/biblioteca"
    end_dir = "~/pueblo/este/biblioteca"

    commands = [
        "ls seccion-privada/",
        "ls seccion-privada"
    ]

    hints = [
        (
            "{{rb:Usa}} {{yb:ls seccion-privada/}} {{rb:para mirar dentro de la "
            "sección privada de la biblioteca.}}"
        )
    ]
    companion_speech = "Eleanor: {{Bb:¿Qué habrá en la seccion-privada?}}"

    def next(self):
        return 26, 5


class Step5(StepTemplateMkdir):

    story = [
        (
            "Eleanor: {{Bb:\"Me imagino que la seccion-privada está cerrada para quienes "
            "vienen de afuera...\""
        ),

        "\"Fijémonos si podemos encontrar algo en la}} {{bb:seccion-publica.}}{{Bb:\"}}",

        "\nUsa {{lb:ls}} para mirar en la {{bb:seccion-publica}}."
    ]

    start_dir = "~/pueblo/este/biblioteca"
    end_dir = "~/pueblo/este/biblioteca"
    commands = [
        "ls seccion-publica",
        "ls seccion-publica/",
        "ls -a seccion-publica",
        "ls -a seccion-publica/"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar dentro de la seccion-publica.}}",
        "{{rb:Usa}} {{yb:ls seccion-publica}} {{rb:para mirar dentro de la seccion-publica.}}"
    ]
    companion_speech = "Eleanor: {{Bb:¿Qué crees que habrá en la seccion-publica?}}"

    def next(self):
        return 26, 6


class Step6(StepTemplateMkdir):
    story = [
        "Eleanor: {{Bb:\"Guau, desaparecieron todos los comandos.",
        "¿Será que la gente los ha estado robando?\"\n}}",

        "{{Bb:\"¿Qué es ese papel}} {{lb:NANO}}{{Bb:?\"}}\n",
        "{{Bb:\"Vamos a}} {{lb:examinar}} {{Bb:el papel.\"}}"
    ]
    start_dir = "~/pueblo/este/biblioteca"
    end_dir = "~/pueblo/este/biblioteca"
    commands = [
        "cat seccion-publica/NANO"
    ]
    hints = [
        "{{rb:Examina el papel con}} {{yb:cat seccion-publica/NANO}}"
    ]
    companion_speech = (
        (
            "Eleanor: {{Bb:Seguro la biblioteca cobra multas por devolver "
            "tarde los libros.}}"
        )
    )

    def next(self):
        return 26, 7


class Step7(StepTemplateMkdir):
    story = [
        "Eleanor: {{Bb:\"¿Entonces nano te permite editar archivos?}}",

        (
            "{{Bb:¿Tal vez podríamos usarlo para arreglar el script}} "
            "{{yb:la-mejor-bocina-del-mundo.sh}}{{Bb:?\"}}\n"
        ),

        "{{Bb:\"Volvamos}} {{lb:otra vez}} {{Bb:a la}} {{bb:tienda-de-cobertizos}}{{Bb:.\"}}"
    ]
    start_dir = "~/pueblo/este/biblioteca"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"
    companion_speech = (
        "Eleanor: {{Bb:¿...tenemos que ir y ver al horripilante Bernard otra vez?}}"
    )

    path_hints = {
        "~/pueblo/este/biblioteca": {
            "blocked": "\n{{rb:Usa}} {{yb:cd ../}} {{rb:para salir.}}"
        },
        "~/pueblo/este": {
            "not_blocked": "\n{{gb:Ahora dirígete a la}} {{bb:tienda-de-cobertizos}}{{gb:.}}",
            "blocked": "\n{{rb:Usa}} {{yb:cd tienda-de-cobertizos/}} {{rb:para ir a la tienda de cobertizos.}}"
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
        return 27, 1
