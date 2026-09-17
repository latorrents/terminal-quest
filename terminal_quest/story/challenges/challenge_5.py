# challenge_5.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from terminal_quest.step import StepTemplate
from terminal_quest.step_helpers import unblock_commands_with_cd_hint
from terminal_quest.terminals import TerminalCd


class StepTemplateCd(StepTemplate):
    TerminalClass = TerminalCd


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):
    story = [
        (
            "{{wb:Mama:}} {{Bb:\"Hola dormilón, el desayuno está casi listo. ¿Puedes ir a "
            "avisarle a tu Papá? Creo que está en el}} {{bb:jardin}}{{Bb:.\"}}\n"
        ),
        "Vamos a buscar a tu {{bb:Papa}} en el {{bb:jardin}}.",
        "Primero necesitamos {{lb:abandonar}} la {{bb:cocina}} usando {{yb:cd ..}}\n"
    ]
    start_dir = "~/mi-casa/cocina"
    end_dir = "~/mi-casa"
    commands = ["cd ..", "cd ../"]
    hints = ["{{rb:Para abandonar la cocina escribe}} {{yb:cd ..}}"]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 5, 2


class Step2(StepTemplateCd):
    story = [
        "Estás nuevamente en la sala de tu casa.\n",
        "¿Puedes ver tu {{bb:jardin}}? {{lb:Mira alrededor}}.\n"
    ]
    start_dir = "~/mi-casa"
    end_dir = "~/mi-casa"
    commands = "ls"
    hints = ["{{rb:Escribe}} {{yb:ls}} {{rb:para mirar alrededor tuyo.}}"]

    def next(self):
        return 5, 3


class Step3(StepTemplateCd):
    story = [
        "Ves las puertas al {{bb:jardin}}, {{bb:cocina}}, {{bb:mi-cuarto}} y el {{bb:cuarto-de-papas}}.",
        "{{lb:Ve}} hacia el {{bb:jardin}}.\n"
    ]
    start_dir = "~/mi-casa"
    end_dir = "~/mi-casa/jardin"
    commands = ["cd jardin", "cd jardin/"]
    hints = ["{{rb:Escribe}} {{yb:cd jardin}} {{rb:para ir hacia el jardin.}}"]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 5, 4


class Step4(StepTemplateCd):
    story = [
        "Usa {{yb:ls}} para {{lb:buscar}} en el {{bb:jardin}} a tu {{bb:Papa}}.\n"
    ]
    start_dir = "~/mi-casa/jardin"
    end_dir = "~/mi-casa/jardin"
    commands = "ls"
    hints = ["{{rb:Para buscar a tu Papá, escribe}} {{yb:ls}} {{rb:y presiona}} {{ob:Enter}}{{rb:.}}"]

    def next(self):
        return 5, 5


class Step5(StepTemplateCd):
    story = [
        "El {{bb:jardin}} se ve muy lindo en esta época del año.",
        "Hmmm...pero no podemos verlo en ninguna parte.",
        "Tal vez está en el {{bb:invernadero}}.",
        "\n{{lb:Ve}} dentro del {{bb:invernadero}}.\n"
    ]
    start_dir = "~/mi-casa/jardin"
    end_dir = "~/mi-casa/jardin/invernadero"
    commands = ["cd invernadero", "cd invernadero/"]
    hints = ["{{rb:Para ir al invernadero, escribe}} {{yb:cd invernadero}}"]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 5, 6


class Step6(StepTemplateCd):
    story = [
        "¿Está allí? {{lb:Mira alrededor}} con {{yb:ls}} para averiguarlo.\n"
    ]
    start_dir = "~/mi-casa/jardin/invernadero"
    end_dir = "~/mi-casa/jardin/invernadero"
    commands = "ls"
    hints = ["{{rb:Escribe}} {{yb:ls}} {{rb:para buscar a tu Papá.}}"]

    def next(self):
        return 5, 7


class Step7(StepTemplateCd):
    story = [
        "Tu {{bb:Papa}} ha estado muy ocupado, hay muchos vegetales aquí.",
        "Hmmmm. No está aquí. Pero hay algo extraño.\n",
        "Ves una {{bb:nota}} en el suelo. Usa {{yb:cat nota}} para {{lb:leer}} lo que dice.\n"
    ]
    start_dir = "~/mi-casa/jardin/invernadero"
    end_dir = "~/mi-casa/jardin/invernadero"
    commands = "cat nota"
    hints = ["{{rb:Escribe}} {{yb:cat nota}} {{rb:¡para ver lo que dice la nota!}}"]

    def next(self):
        return 5, 8


class Step8(StepTemplateCd):
    story = [
        "¿Eh? Qué extraño.",
        "Pero volver es muy fácil. Solo escribe {{yb:cd ..}} para regresar por donde viniste.\n"
    ]
    start_dir = "~/mi-casa/jardin/invernadero"
    end_dir = "~/mi-casa/jardin"
    commands = ["cd ..", "cd ../"]
    hints = ["{{rb:Escribe}} {{yb:cd ..}} {{rb:para volver al jardín.}}"]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 5, 9


class Step9(StepTemplateCd):
    story = [
        "Estás nuevamente en el jardín. Usa {{yb:cd ..}} otra vez para {{lb:volver}} a la casa.\n",
        (
            "{{gb:Consejo: Presiona la flecha hacia}} {{ob:ARRIBA}} {{gb:para ver tus "
            "comandos previos.}}\n"
        )
    ]
    start_dir = "~/mi-casa/jardin"
    end_dir = "~/mi-casa"
    commands = ["cd ..", "cd ../"]
    hints = ["{{rb:Escribe}} {{yb:cd ..}} {{rb:para volver a la casa.}}"]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 5, 10


class Step10(StepTemplateCd):
    story = [
        "Ahora {{lb:ve}} otra vez a la {{bb:cocina}} con {{bb:Mama}}.\n"
    ]
    start_dir = "~/mi-casa"
    end_dir = "~/mi-casa/cocina"
    commands = ["cd cocina", "cd cocina/"]
    hints = ["{{rb:Escribe}} {{yb:cd cocina}} {{rb:para volver a la cocina.}}"]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 6, 1
