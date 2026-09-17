# helpers.py
#
# Funciones de ayuda usadas en todo el juego.
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

import logging
import os
import re

from terminal_quest.common import story_files_dir, game_dir, log_file
from terminal_quest.progress import (
    load_app_state_variable, save_app_state_variable, increment_app_state_variable
)

FORMATTING_BEGIN = re.compile(r"{{\w+:")
FORMATTING_END = re.compile(r"}}")

logger = logging.getLogger('terminal_quest')
logger.addHandler(logging.NullHandler())


def enable_log():
    os.makedirs(game_dir, exist_ok=True)
    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def get_script_cmd(string, real_path):
    """
    Checks whether the command the user typed is an executable file.

    Returns:
        tuple (bool, str): whether it is a valid executable, and its real path.
    """
    string = string.split(" ")[0]
    if string.startswith("./"):
        script = os.path.join(real_path, string[2:])
    elif string.startswith("/"):
        script = string
    else:
        script = os.path.join(real_path, string)

    # directories are executable, so exclude directories
    is_script = os.path.exists(script) and not os.path.isdir(script) and is_exe(script)
    return is_script, script


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def record_user_interaction(instance, base_name):
    """
    Store some user actions, so we know if the user did the optional side quests.
    """
    class_instance = instance.__class__.__name__
    challenge_number = instance.__module__.split("_")[-1]
    profile_var_name = "{} {} {}".format(base_name, challenge_number, class_instance)

    if not load_app_state_variable("terminal-quest", profile_var_name):
        save_app_state_variable("terminal-quest", profile_var_name, True)
        increment_app_state_variable("terminal-quest", "{} total".format(base_name), 1)


def get_ascii_art(name):
    """Load an ASCII art file from the story files."""
    try:
        with open(os.path.join(story_files_dir, name), encoding='utf-8') as f:
            return f.read()
    except OSError as e:
        logger.error('Could not load file {} - [{}]'.format(name, e))
        return name


def strip_formatting(string):
    """
    Remove formatting in strings, e.g. strip_formatting('{{gb:Foo}}') => 'Foo'
    """
    string = FORMATTING_BEGIN.sub("", string)
    return FORMATTING_END.sub("", string)


def wrap_in_box(lines):
    """Wrap lines in an ascii box"""
    max_characters = max(len(strip_formatting(line)) for line in lines)
    outer_line = " {} ".format("-" * (max_characters + 2))

    def format_line(line):
        num_padding = max_characters - len(strip_formatting(line))
        return "| {} |".format(line + (" " * num_padding))

    return [outer_line] + [format_line(line) for line in lines] + [outer_line + "\n"]


def is_executable(path):
    return os.path.isfile(path) and has_execute_permissions(path)


def has_read_permissions(path):
    return os.access(path, os.R_OK)


def has_write_permissions(path):
    return os.access(path, os.W_OK)


def has_execute_permissions(path):
    return os.access(path, os.X_OK)
