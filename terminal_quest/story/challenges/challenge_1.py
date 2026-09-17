# challenge_1.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from terminal_quest.step import StepTemplate
from terminal_quest.terminals import TerminalLs
from terminal_quest.sound import SoundManager
from terminal_quest.helpers import wrap_in_box


class StepLs(StepTemplate):
    TerminalClass = TerminalLs


# ----------------------------------------------------------------------------------------


class Step1(StepLs):
    story = [
        "{{wb:Alarma}}: {{Bb:\"Bip bip bip! Bip bip bip!\"}}",
        "{{wb:Radio}}: {{Bb:\"Buenos días, estas son las noticias de las 9am.\"\n",
        (
            "\"El pueblo de Folderton ha despertado entre extrañas noticias. Hubo varios "
            "reportes de personas desaparecidas y edificios dañados a lo largo del pueblo, "
            "van llegando más novedades mientras hablamos.\""
        ),
        (
            "\n\"El alcalde Hubert ha llamado a una reunión de emergencia en el pueblo, te "
            "mantendremos informado...\"}}\n"
        ),
        "¡Es hora de levantarse, dormilón!\n ",
    ]  # TODO: " \ is a hack in this array to stop word wrap code screwing up and adding new lines in where it shouldn't

    story += wrap_in_box([
        "{{gb:Nuevo Poder:}} Escribe {{yb:ls}} y presiona",
        "{{ob:Enter}} para {{lb:mirar a tu alrededor}}.",
    ])

    start_dir = "~/mi-casa/mi-cuarto"
    end_dir = "~/mi-casa/mi-cuarto"
    commands = "ls"
    highlighted_commands = ["ls"]
    hints = [
        (
            "{{rb:Escribe}} {{yb:ls}} {{rb:y presiona}} {{ob:Enter}} {{rb:para echar un "
            "vistazo alrededor de tu habitación.}}"
        )
    ]

    def _run_at_start(self):
        sound_manager = SoundManager()
        sound_manager.play_sound('despertador')

    def next(self):
        return 2, 1
