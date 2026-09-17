# challenge_29.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os

from terminal_quest.story.challenges.CompanionMisc import StepTemplateNano
from terminal_quest.helpers import record_user_interaction


story_replies = {
    "echo 1": [
        {
            "user": "\"¿Por qué la sección privada de la biblioteca está cerrada?\"",
            "clara": \
                (
                    "Clara: {{Bb:\"Contiene información peligrosa.\"\n\"...Lo siento, no debería hablar "
                    "mucho más. El director de la biblioteca se preocupa mucho por que nadie entre "
                    "allí. Él es el único que puede cerrar y abrir la sección.\"}}"
                )
        },
        {
            "user": "\"¿Cómo la cerró?\"",
            "clara": \
                (
                    "Clara: {{Bb:\"No lo sé, es un cerrojo muy especial. Pero creo que aprendió los secretos del "
                    "cerrojo de un espadachín enmascarado que vive fuera del pueblo.\"}}"
                )
        },
        {
            "user": "\"¿Dónde puedo encontrar a ese espadachín enmascarado?\"",
            "clara": \
                (
                    "Clara: {{Bb:\"Él dijo que el}} "
                    "{{bb:espadachín enmascarado}} {{Bb:vivía en el bosque.\"}}"
                    "\n{{Bb:\"Supongo que se refería al bosque que está justo al lado de la}} "
                    "{{lb:Carretera Ventosa}}{{Bb:. El que está "
                    "cerca de la granja y de aquella extraña casa solitaria fuera del pueblo.\"}}"
                )
        }
    ],

    "echo 2": [
        {
            "user": "\"¿Por qué te escondes aquí abajo?\"",
            "clara": \
                (
                    "Clara: {{Bb:\"Escuché un timbre sonar y vi cómo alguien desaparecía delante de "
                    "mí. Estaba tan asustada que corrí, y encontré esta}} {{bb:.bodega}}{{Bb:.\"}}"
                )
        },
        {
            "user": "\"¿Tienes algún pariente en el pueblo?\"",
            "clara": \
                (
                    "Clara: {{Bb:\"Tengo dos hijos, un}} {{bb:chico}} {{Bb:y una}} "
                    "{{bb:chica}}{{Bb:. Espero que se encuentren bien.\"}}"
                )
        },
        {
            "user": "\"¿Por qué está tan vacía la biblioteca?\"",
            "clara": \
                (
                    "Clara: {{Bb:\"Hace tiempo empezamos a cobrar multas por "
                    "devolver tarde los libros...\"}}"
                )
        }
    ],

    "echo 3": [
        {
            "user": "\"¿Conoces a alguien más en el pueblo?\"",
            "clara": \
                (
                    "Clara: {{Bb:\"Hay un hombre en quien no confío, el dueño de la}} "
                    "{{bb:tienda-de-cobertizos}}{{Bb:. Creo que su nombre es}} {{bb:Bernard}}{{Bb:.\"}}"
                )
        },
        {
            "user": "\"¿Por qué no te gusta Bernard?\"",
            "clara": \
                (
                    "Clara: {{Bb:\"Hace utensilios muy simples y cobra una fortuna por "
                    "ellos.}}\n{{Bb:Su padre era un hombre muy inteligente y pasaba mucho tiempo en la "
                    "biblioteca leyendo comandos. Se convirtió en un exitoso hombre de negocios.\"}}"
                )
        },
        {
            "user": "\"¿Qué le pasó al papá de Bernard?\"",
            "clara": \
                (
                    "Clara: {{Bb:\"Nadie lo sabe con seguridad, desapareció un día. Todos asumieron que "
                    "había muerto. Lo vi abandonar la biblioteca el día que desapareció, se fue muy "
                    "apurado. Parecía estar muy asustado.\"}}"
                )
        }
    ]
}


# Generate the story from the step number
def create_story(step):
    print_text = ""

    if step > 1:
        print_text = "{{yb:%s}}" % story_replies["echo 1"][step - 2]["user"]

    story = [
        story_replies["echo 1"][step - 2]["clara"],
        "\n{{yb:1: %s}}" % story_replies["echo 1"][step - 1]["user"],
        "{{yb:2: %s}}" % story_replies["echo 2"][0]["user"],
        "{{yb:3: %s}}" % story_replies["echo 3"][0]["user"]
    ]

    return print_text, story


# Want to eliminate the story that the user has already seen
def pop_story(user_input):
    # if the user_input is echo 1, echo 2 or echo 3
    if user_input in story_replies:
        reply = story_replies[user_input][0]
        story_replies[user_input].remove(reply)
        return reply


class StepNanoStory(StepTemplateNano):
    commands = [
        "echo 1"
    ]

    start_dir = "~/pueblo/este/restaurante/.bodega"
    end_dir = "~/pueblo/este/restaurante/.bodega"
    hints = [
        (
            "{{rb:Habla con Clara usando}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:o}} "
            "{{yb:echo 3}}{{rb:.}}"
        )
    ]
    step_number = None


    def story_check_command(self, line, echo_hit):
        # If self.last_user_input equal to "echo 1" or "echo 3"
        if line in story_replies:

            if line == "echo 1":
                return True

            else:
                if echo_hit[line]:
                    echo_hit[line] = False
                    reply = pop_story(line)["clara"]
                    self.send_hint("\n\n" + reply)

                    # Record that the user got optional info
                    # Replace spaces with underscores
                    user_input = "_".join(line.split(" "))
                    state_name = "clara_%s" % user_input
                    record_user_interaction(self, state_name)
                else:
                    self.send_hint(
                        "\n{{rb:Ya le has preguntado eso a Clara. Pregúntale otra cosa.}}"
                    )

        else:
            return StepTemplateNano.check_command(self, line)


# ----------------------------------------------------------------------------------------


class Step1(StepNanoStory):
    story = [
        "Clara: {{Bb:\"¿Qué? ¿Quién eres?\"}}",

        (
            "\nEleanor: {{Bb:\"¡Hola! Soy Eleanor, y aquí tenemos a mi amigo}} "
            "{{gb:%s}}{{Bb:.}} {{Bb:¡Te reconozco! ¡Solías trabajar en la biblioteca!\"}}"
        )\
        % os.environ["LOGNAME"],

        "\nClara: {{Bb:\"...¡ah, Eleanor! Sí, me acuerdo de ti, solías venir casi todos los días.\"}}",

        # Options
        "\n{{yb:1: \"¿Por qué la sección privada de la biblioteca está cerrada?\"}}",
        "{{yb:2: \"¿Por qué te escondes aquí abajo?\"}}",
        "{{yb:3: \"¿Conoces a alguien más en el pueblo?\"}}",

        "\nUsa {{yb:echo}} para hacerle una pregunta a {{bb:Clara}}."
    ]

    companion_speech = "Eleanor: {{Bb:\"Ya no estoy asustada, me cae bien Clara.\"}}"

    def _run_at_start(self):
        self.echo_hit = {
            "echo 2": True,
            "echo 3": True
        }

    def check_command(self, last_user_input):
        return self.story_check_command(last_user_input, self.echo_hit)

    def next(self):
        return 29, 2


class Step2(StepNanoStory):
    companion_speech = "Eleanor: {{Bb:\"¿Qué es aquello tan peligroso que se oculta en la seccion-privada?\"}}"

    def _run_at_start(self):
        self.echo_hit = {
            "echo 2": True,
            "echo 3": True
        }

        self.print_text = [create_story(2)[0]]
        self.story = create_story(2)[1]

    def check_command(self, last_user_input):
        return self.story_check_command(last_user_input, self.echo_hit)

    def next(self):
        return 29, 3


class Step3(StepNanoStory):
    companion_speech = "Eleanor: {{Bb:\"¿Quieres descubrir algo tan peligroso?\"}}"

    def _run_at_start(self):
        self.echo_hit = {
            "echo 2": True,
            "echo 3": True
        }

        self.print_text = [create_story(3)[0]]
        self.story = create_story(3)[1]

    def check_command(self, last_user_input):
        return self.story_check_command(last_user_input, self.echo_hit)

    def next(self):
        return 29, 4


class Step4(StepNanoStory):
    last_step = True

    print_text = "{{yb:\"¿Dónde puedo encontrar a ese espadachín enmascarado?\"}}",
    story = [
        (
            "Clara: {{Bb:\"Él dijo que el}} "
            "{{bb:espadachín enmascarado}} {{Bb:vivía en el bosque.\"}}"
        ),

        (
            "{{Bb:\"Supongo que se refería al bosque que está justo al lado de la}} "
            "{{lb:Carretera Ventosa}}{{Bb:. El que está cerca de la granja y de aquella "
            "extraña casa solitaria fuera del pueblo.\"}}"
        ),

        "\n{{gb:Presiona}} {{ob:Enter}} {{gb:para continuar.}}"
    ]

    companion_speech = "Eleanor: {{Bb:\"¿¿Un espadachín enmascarado??\"}}"

    commands = []

    def next(self):
        return 30, 1
