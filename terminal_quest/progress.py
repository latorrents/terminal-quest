# progress.py
#
# Guarda y carga el progreso del jugador en un archivo JSON.
#
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

import json
import os

from terminal_quest.common import game_dir, progress_file


def _load():
    try:
        with open(progress_file, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _save(data):
    os.makedirs(game_dir, exist_ok=True)
    tmp = progress_file + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, progress_file)


# The app argument is kept so the story code reads like the original.
def load_app_state_variable(app, name):
    return _load().get(name)


def save_app_state_variable(app, name, value):
    data = _load()
    data[name] = value
    _save(data)


def save_app_state_variable_with_dialog(app, name, value):
    save_app_state_variable(app, name, value)


def increment_app_state_variable(app, name, amount):
    data = _load()
    data[name] = data.get(name, 0) + amount
    _save(data)


def get_level():
    return _load().get('level') or 0


def save_level(challenge):
    if challenge > get_level():
        save_app_state_variable('terminal-quest', 'level', challenge)


def reset_progress():
    _save({})
