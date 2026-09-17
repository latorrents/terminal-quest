# common.py
#
# Rutas y constantes compartidas por todo el juego.
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

import getpass
import os

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(PACKAGE_DIR, 'assets')
story_files_dir = os.path.join(ASSETS_DIR, 'story_files')
sounds_dir = os.path.join(ASSETS_DIR, 'sounds')

# Carpeta donde se guardan el mundo del juego y el progreso.
game_dir = os.path.join(os.path.expanduser('~'), '.terminal-quest')

# El mundo de archivos con el que interactúa el jugador.
tq_file_system = os.path.join(game_dir, 'mundo')

# La carpeta que el jugador ve como ~
fake_home_dir = os.path.join(tq_file_system, '~')

progress_file = os.path.join(game_dir, 'progreso.json')
log_file = os.path.join(game_dir, 'registro.log')

MAX_CHALLENGE = 46

# Contraseña de sudo dentro del juego.
SUDO_PASSWORD = 'password'


def get_username():
    try:
        return getpass.getuser()
    except Exception:
        return 'aventurero'


def get_story_file(name):
    return os.path.join(story_files_dir, name)
