# challenge_24.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step_helpers import unblock_cd_commands
from terminal_quest.story.challenges.CompanionMisc import StepTemplateMkdir


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        (
            "Caminas por el camino estrecho, con {{bb:Eleanor}} bailando a tu lado, hasta "
            "que llegas a un espacio abierto en la parte {{bb:este}} del pueblo."
        ),
        "\n{{lb:Mira a tu alrededor.}}"
    ]
    commands = [
        "ls",
        "ls -a"
    ]

    start_dir = "~/pueblo/este"
    end_dir = "~/pueblo/este"
    hints = [
        "{{rb:Mira alrededor con}} {{yb:ls}}{{rb:.}}"
    ]
    deleted_items = ["~/pueblo/Eleanor"]
    file_list = [{"path": "~/pueblo/este/Eleanor"}]

    companion_speech = (
        "Eleanor: {{Bb:No veo a mis padres por ninguna parte... pero hay un edificio "
        "extraño allá.}}"
    )

    def next(self):
        return 24, 2


class Step2(StepTemplateMkdir):
    story = [
        "Ves una {{bb:tienda-de-cobertizos}}, una {{bb:biblioteca}} y un {{bb:restaurante}}.",
        "\nEleanor: {{Bb:\"¿Qué es esa tienda-de-cobertizos?\"}}\n",
        "{{Bb:\"¡Vamos}} {{lb:adentro}}{{Bb:!\"}}"
    ]

    start_dir = "~/pueblo/este"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"
    hints = [
        "{{rb:Usa}} {{yb:cd tienda-de-cobertizos}} {{rb:para entrar a la tienda de cobertizos.}}"
    ]

    companion_speech = "Eleanor: {{Bb:¿Crees que venderán caramelos?}}"

    def block_command(self, line):
        return unblock_cd_commands(line)

    def next(self):
        return 24, 3


# Duplicate of Step1, except that self.next is changed
class Step3(StepTemplateMkdir):
    # Have a sign with "the-best-shed-maker-in-town"

    story = [
        "Los dos entran despacio en la {{bb:tienda-de-cobertizos}}.",
        "Aquí dentro está sucio y mucho más oscuro que afuera.",
        "Parece que {{bb:Eleanor}} va a estornudar.",
        "\n{{lb:Mira a tu alrededor.}}"
    ]

    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"
    hints = [
        "{{rb:Mira alrededor con}} {{yb:ls}}{{rb:.}}"
    ]
    commands = [
        "ls",
        "ls -a"
    ]
    deleted_items = ["~/pueblo/este/Eleanor"]
    file_list = [{"path": "~/pueblo/este/tienda-de-cobertizos/Eleanor"}]
    companion_speech = "Eleanor: {{Bb:¡Ah... ah... achís! ¡Qué sucio está aquí dentro!}}"

    def next(self):
        return 24, 4


class Step4(StepTemplateMkdir):

    story = [
        "Ves a un hombre llamado {{bb:Bernard}}, una puerta y algunas herramientas.",
        "\nLas herramientas se muestran en {{gb:verde}} en la terminal.",
        "\n{{lb:Escucha}} lo que {{bb:Bernard}} tiene para decir."
    ]

    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"

    hints = [
        "{{rb:Usa}} {{yb:cat Bernard}} {{rb:para escuchar lo que Bernard tiene para decir.}}"
    ]

    commands = [
        "cat Bernard"
    ]
    companion_speech = "Eleanor: {{Bb:Mi}} {{lb:gato}} {{Bb:siempre me escuchaba muy bien, le contaba todo.}}"

    def next(self):
        return 25, 1
