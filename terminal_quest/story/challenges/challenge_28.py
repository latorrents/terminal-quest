# challenge_28.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.story.challenges.CompanionMisc import StepTemplateNano
from terminal_quest.common import get_story_file
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.sound import SoundManager


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateNano):
    story = [
        "Has vuelto al pueblo. {{bb:Eleanor}} parece más aliviada ahora que está afuera.",
        "¿Dónde puede estar escondiéndose la {{bb:bibliotecaria}}?\n",
        "{{lb:Mira alrededor}} para decidir a dónde ir."
    ]

    start_dir = "~/pueblo/este"
    end_dir = "~/pueblo/este"

    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]

    deleted_items = ["~/pueblo/este/tienda-de-cobertizos/Eleanor"]
    file_list = [
        {
            "path": "~/pueblo/este/Eleanor",
            "contents": get_story_file("Eleanor")
        }
    ]

    commands = [
        "ls",
        "ls -a"
    ]

    companion_speech = "Eleanor: {{Bb:\"Tengo hambre. ¿Ves algún sitio donde podamos comer algo?\"}}"

    def next(self):
        return 28, 2


class Step2(StepTemplateNano):
    story = [
        "Todavía no has ido al {{bb:restaurante}}.\n",
        "{{lb:Entra}} al {{bb:restaurante}}."
    ]

    start_dir = "~/pueblo/este"
    end_dir = "~/pueblo/este/restaurante"

    hints = [
        "{{rb:Usa}} {{yb:cd restaurante}} {{rb:para ir al restaurante.}}"
    ]

    companion_speech = ("Eleanor: {{Bb:Ooh, ¿crees que tendrán un sándwich aquí?}}")

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 28, 3


class Step3(StepTemplateNano):
    story = [
        "Junto con {{bb:Eleanor}} entras al {{bb:restaurante}}.\n",
        "{{lb:Mira alrededor}} {{lb:más de cerca}}."
    ]

    start_dir = "~/pueblo/este/restaurante"
    end_dir = "~/pueblo/este/restaurante"

    hints = [
        "Eleanor: {{Bb:¿Recuerdas cómo me encontraste? Usaste}} {{yb:ls -a}} {{Bb:¿no es cierto?}}"
    ]

    commands = [
        "ls -a"
    ]

    deleted_items = ["~/pueblo/este/Eleanor"]
    file_list = [
        {
            "path": "~/pueblo/este/restaurante/Eleanor",
            "contents": get_story_file("Eleanor"),
            "type": "file"
        }
    ]

    companion_speech = "Eleanor: {{Bb:Está realmente vacío aquí adentro...}}"

    def next(self):
        return 28, 4


class Step4(StepTemplateNano):
    story = [
        "¿Puedes ver la {{bb:.bodega}}?\n",
        "{{lb:Entra}} a la {{bb:.bodega}}."
    ]

    start_dir = "~/pueblo/este/restaurante"
    end_dir = "~/pueblo/este/restaurante/.bodega"

    hints = [
        "{{rb:Entra a la bodega usando}} {{yb:cd .bodega}}{{rb:.}}"
    ]

    companion_speech = "Eleanor: {{Bb:Tengo miedo...¿me tomas de la mano?}}"

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 28, 5


class Step5(StepTemplateNano):
    story = [
        "{{bb:Eleanor}} toma tu mano y los dos bajan a la {{bb:.bodega}}.\n",
        "{{lb:Mira alrededor.}}"
    ]

    start_dir = "~/pueblo/este/restaurante/.bodega"
    end_dir = "~/pueblo/este/restaurante/.bodega"

    hints = [
        "{{rb:Mira alrededor con}} {{yb:ls}}{{rb:.}}"
    ]

    deleted_items = ["~/pueblo/este/restaurante/Eleanor"]
    file_list = [
        {
            "path": "~/pueblo/este/restaurante/.bodega/Eleanor",
            "contents": get_story_file("Eleanor"),
            "type": "file"
        }
    ]
    commands = [
        "ls",
        "ls -a"
    ]

    companion_speech = "Eleanor: {{Bb:\"¿...hay alguien aquí?\"}}"

    def _run_at_start(self):
        sound_manager = SoundManager()
        sound_manager.play_sound('steps')

    def next(self):
        return 28, 6


class Step6(StepTemplateNano):
    story = [
        "Ves a una mujer, {{bb:Clara}}, en la {{bb:.bodega}}.\n",
        "{{lb:Escucha}} lo que tiene para decir."
    ]

    start_dir = "~/pueblo/este/restaurante/.bodega"
    end_dir = "~/pueblo/este/restaurante/.bodega"

    hints = [
        "{{rb:Usa}} {{yb:cat}} {{rb:para escuchar lo que tiene para decir.}}",
        "{{rb:Usa}} {{yb:cat Clara}} {{rb:para escuchar a Clara.}}"
    ]

    commands = [
        "cat Clara"
    ]
    companion_speech = "Eleanor: {{Bb:\"...¡oh! ¡Creo que reconozco a esa mujer!\"}}"

    def next(self):
        return 29, 1
