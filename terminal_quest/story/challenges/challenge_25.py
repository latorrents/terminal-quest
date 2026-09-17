# challenge_25.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from terminal_quest.story.challenges.CompanionMisc import StepTemplateMkdir
from terminal_quest.step_helpers import unblock_cd_commands


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateMkdir):
    story = [
        "Bernard: {{Bb:\"¡Hola! Shhh, no digan ni una palabra.\"}}",

        "{{Bb:\"Sé por qué están aquí. ¡Necesitan un cobertizo!\"",

        "\"Tengo justo lo que buscan:}} {{bb:el-mejor-constructor-de-cobertizos.sh}}{{Bb:.\"}}",

        (
            "\nSe ve muy entusiasmado con la idea. {{lb:Examina}} el utensilio "
            "{{bb:el-mejor-constructor-de-cobertizos.sh}}"
        ),

        "\n{{gb:Usa}} {{ob:TAB}} {{gb:para acelerar la escritura.}}"
    ]

    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"

    hints = [
        "{{rb:Usa}} {{yb:cat}} {{rb:para examinar}} {{bb:el-mejor-constructor-de-cobertizos.sh}}",

        "{{rb:Usa}} {{yb:cat el-mejor-constructor-de-cobertizos.sh}} {{rb:para examinar el utensilio.}}"
    ]

    commands = [
        "cat el-mejor-constructor-de-cobertizos.sh",
        "cat ./el-mejor-constructor-de-cobertizos.sh"
    ]
    companion_speech = "Eleanor: {{Bb:Bernard me asusta un poco...}}"

    def check_command(self, line):
        if line == "cat la-mejor-bocina-del-mundo.sh" or \
                        line == "cat ./la-mejor-bocina-del-mundo.sh":

            self.send_hint(
                (
                    "\n{{rb:¡Estás buscando archivos equivocados! Quieres ver}} "
                    "{{bb:el-mejor-constructor-de-cobertizos.sh}}{{rb:.}}"
                )
            )
        else:
            return StepTemplateMkdir.check_command(self, line)

    def next(self):
        return 25, 2


class Step2(StepTemplateMkdir):
    story = [
        "El utensilio tiene una etiqueta que dice \"mkdir cobertizo\".",
        (
            "Reconoces el comando {{yb:mkdir}}. Fue el que usaste para ayudar a {{bb:Ruth}} "
            "en la granja."
        ),

        (
            "Bernard: {{Bb:\"Este utensilio se llama script. Es increíble. Solo ejecuta el comando "
            "y obtienes un cobertizo nuevo.\"}}"
        ),
        "{{Bb:\"Pruébalo. Úsalo con ./el-mejor-constructor-de-cobertizos.sh\"}}",

        "\n{{gb:Usa}} {{ob:TAB}} {{gb:para acelerar la escritura.}}"
    ]

    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"

    hints = [
        (
            "{{rb:Haz lo que dice Bernard: usa}} {{yb:./el-mejor-constructor-de-cobertizos.sh}} "
            "{{rb:para ejecutar el comando}}"
        )
    ]
    commands = [
        "./el-mejor-constructor-de-cobertizos.sh"
    ]
    companion_speech = \
        "Eleanor: {{Bb:¿No es eso lo mismo que poner}} {{yb:mkdir cobertizo}}{{Bb:?}}"

    def check_command(self, line):
        if line == "./la-mejor-bocina-del-mundo.sh":
            self.send_hint(
                "\n{{rb:Te estás equivocando. Quieres ejecutar}} {{yb:./el-mejor-constructor-de-cobertizos.sh}}"
            )
        else:
            return StepTemplateMkdir.check_command(self, line)

    def next(self):
        return 25, 3


class Step3(StepTemplateMkdir):
    story = [
        "{{lb:Mira alrededor}} para ver si creaste el {{bb:cobertizo}}."
    ]
    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar alrededor.}}"
    ]
    companion_speech = "Eleanor: {{Bb:Ah, ¡mira allí!}}"

    def next(self):
        return 25, 4


class Step4(StepTemplateMkdir):
    story = [
        "¡Funcionó! Puedes ver un nuevo {{bb:cobertizo}}.\n",
        "¿Qué sucede si lo ejecutas otra vez?\n",
        "{{gb:Presiona la flecha hacia}} {{ob:ARRIBA}} {{gb:dos veces para repetir el comando.}}"
    ]

    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"

    hints = [
        "{{rb:Mira lo que pasa cuando ejecutas el comando otra vez.}}",

        (
            "{{rb:Ejecuta el comando otra vez usando}} "
            "{{yb:./el-mejor-constructor-de-cobertizos.sh}} {{rb:para ver qué sucede.}}"
        )
    ]
    commands = [
        "./el-mejor-constructor-de-cobertizos.sh"
    ]
    companion_speech = "Eleanor: {{Bb:No creo que esto funcione...}}"

    def next(self):
        return 25, 5


class Step5(StepTemplateMkdir):
    story = [
        "Error {{yb:mkdir: no se puede crear el directorio «cobertizo»: El archivo ya existe}}",
        "\nBernard: {{Bb:\"Claro que no va a funcionar una segunda vez - ¡ya tienes un cobertizo!\"",

        "\"Estoy trabajando en algo nuevo,}} {{bb:la-mejor-bocina-del-mundo.sh}}{{Bb:.\"}}",

        (
            "{{Bb:\"Puede ser utilizada para avisarle a quien quieras que estás llegando. "
            "Tiene algunos problemitas, pero seguro que pronto los arreglaré.\"}}"
        ),

        (
            "\n{{lb:Examina}} {{bb:la-mejor-bocina-del-mundo.sh}} {{lb:y fíjate si "
            "puedes encontrar el problema.}}\n"
        ),

        "{{gb:Recuerda usar}} {{ob:TAB}}{{gb:!}}"
    ]

    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"
    commands = [
        "cat la-mejor-bocina-del-mundo.sh",
        "cat ./la-mejor-bocina-del-mundo.sh"
    ]

    hints = [
        "{{rb:Usa}} {{yb:cat}} {{rb:para examinar el utensilio.}}",
        "{{rb:Usa}} {{yb:cat la-mejor-bocina-del-mundo.sh}} {{rb:para examinar el utensilio.}}"
    ]

    companion_speech = (
        "Eleanor: {{Bb:Creo que este utensilio está un poco roto.}}"
    )

    def check_command(self, line):
        if line == "cat el-mejor-constructor-de-cobertizos.sh" or \
           line == "cat ./el-mejor-constructor-de-cobertizos.sh":

            self.send_hint(
                (
                    "\n{{rb:Estás examinando el utensilio equivocado. Quieres ver}} "
                    "{{yb:la-mejor-bocina-del-mundo.sh}}"
                )
            )

        else:
            return StepTemplateMkdir.check_command(self, line)

    def next(self):
        return 25, 6


class Step6(StepTemplateMkdir):
    story = [
        "El script dice {{yb:eco \"Piii!\"}}",
        "Tal vez debería decir {{yb:echo \"Piii!\"}} ...",
        "¿Cómo podríamos hacer cambios en este script?",
        "\nBernard: {{Bb:\"Oh, parece que comprendes cuál es el problema.\"}}",
        "Eleanor: {{Bb:\"Si necesitamos ayuda, podemos ir a la biblioteca, está justo aquí afuera.\"}}",
        "\nAntes de irte, {{lb:mira}} en el {{bb:sotano}}."
    ]

    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este/tienda-de-cobertizos"

    commands = [
        "ls sotano",
        "ls sotano/",
        "ls -a sotano",
        "ls -a sotano/",
    ]

    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:para mirar.}}",
        "{{rb:Usa}} {{yb:ls sotano/}} {{rb:para mirar dentro.}}"
    ]

    companion_speech = (
        "Eleanor: {{Bb:OooOOoh, ¿hay caramelos allí adentro?}}"
    )

    def check_command(self, line):
        # Using self._last_user_input because the line param is empty from being blocked.
        if self._last_user_input in self.commands:
            return True
        return StepTemplateMkdir.check_command(self, self._last_user_input)

    def next(self):
        return 25, 7


class Step7(StepTemplateMkdir):
    story = [
        "Bernard: {{Bb:\"Oooh, qué atrevidos. No pueden husmear aquí.\"}}",
        "\n{{lb:Sal}} de la tienda de cobertizos y vuelve a la parte {{bb:este}} del pueblo."
    ]

    start_dir = "~/pueblo/este/tienda-de-cobertizos"
    end_dir = "~/pueblo/este"
    hints = [
        "{{rb:Sal de la tienda de cobertizos usando}} {{yb:cd ..}}"
    ]
    companion_speech = (
        "Eleanor: {{Bb:\"Sí, me gusta la biblioteca. ¡Volvamos al pueblo!\"}}"
    )

    def block_command(self, line):
        if line.startswith("cd"):
            return unblock_cd_commands(line)
        else:
            return StepTemplateMkdir.block_command(self, line)

    def next(self):
        return 26, 1
