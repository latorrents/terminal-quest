# main.py
#
# Arranca Terminal Quest.
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

import argparse
import locale
import os
import sys

from terminal_quest import menu
from terminal_quest.common import MAX_CHALLENGE, game_dir, tq_file_system
from terminal_quest.controller import ChallengeController, get_step_class
from terminal_quest.file_tree import revert_to_default_permissions
from terminal_quest.helpers import enable_log, logger
from terminal_quest.sound import SoundManager
from terminal_quest.terminals import GameExit
from terminal_quest.ui import GameUI


def parse_args():
    parser = argparse.ArgumentParser(
        prog="jugar.py",
        description="Terminal Quest: una aventura de texto para aprender a usar la terminal de Linux."
    )
    parser.add_argument("desafio", nargs="?", type=int,
                        help="empezar directamente en este desafío (0 a %d)" % MAX_CHALLENGE)
    parser.add_argument("paso", nargs="?", type=int, default=1, help="paso del desafío (por defecto 1)")
    parser.add_argument("--rapido", action="store_true", help="mostrar el texto sin efecto de escritura")
    parser.add_argument("--sin-sonido", action="store_true", help="no reproducir sonidos")
    parser.add_argument("--registro", action="store_true",
                        help="guardar un registro de depuración en ~/.terminal-quest/registro.log")
    return parser.parse_args()


def main():
    locale.setlocale(locale.LC_ALL, "")
    args = parse_args()

    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("Terminal Quest necesita ejecutarse en una terminal.")
        sys.exit(1)

    os.makedirs(game_dir, exist_ok=True)
    if args.registro:
        enable_log()
    if args.sin_sonido:
        SoundManager.enabled = False

    ui = GameUI(typing=not args.rapido)

    try:
        if args.desafio is not None:
            challenge = args.desafio
            if not 0 <= challenge <= MAX_CHALLENGE:
                sys.exit("El desafío debe estar entre 0 y %d." % MAX_CHALLENGE)
            try:
                get_step_class(challenge, args.paso)
            except AttributeError:
                sys.exit("El desafío %d no tiene un paso %d." % (challenge, args.paso))
            step = args.paso
        else:
            challenge = menu.show(ui)
            step = 1
            if challenge is None:
                return

        ui.clear()
        ChallengeController(ui).run(challenge, step)
        ui.print_text("\n{{gb:¡Gracias por jugar a Terminal Quest!}}\n")

    except (GameExit, KeyboardInterrupt):
        ui.print_text("\n{{yb:¡Hasta pronto! Tu progreso está guardado.}}\n")
    except Exception:
        logger.exception("Unexpected error")
        raise
    finally:
        revert_to_default_permissions(tq_file_system)
