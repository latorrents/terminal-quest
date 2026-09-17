# step_helpers.py
#
# Funciones específicas para usar en los desafíos.
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

import os

BLOCKED_MESSAGE = "¡Buen intento! Pero no necesitas ese comando para este desafío"


def line_contains_dangerous_command(line):
    return line[:3] in ["cd ", "mv ", "rm "]


def unblock_commands(line, list_of_commands):
    """Blocks the commands that start with cd, mv or rm unless the command is
    in list_of_commands.
    """
    line = line.strip()
    if line_contains_dangerous_command(line) and \
            line not in list_of_commands and \
            not line == 'mv --help':
        print(BLOCKED_MESSAGE)
        return True


def unblock_commands_with_cd_hint(line, list_of_commands):
    """Unblocks the commands and informs the user."""
    line = line.strip()
    if "cd" in line and line not in list_of_commands:
        print("Estás cerca, pero escribiste un destino inesperado. Intenta ir a otro lugar.")
        return True

    elif line in ["mv ", "rm "] and not line == 'mv --help':
        print(BLOCKED_MESSAGE)
        return True


def unblock_commands_with_mkdir_hint(line, list_of_commands):
    line = line.strip()
    if "mkdir" in line and line not in list_of_commands:
        print("¡Casi lo logras! Pero estás intentando construir algo distinto de lo "
              "esperado. Intenta construir otra cosa.")
        return True

    elif line_contains_dangerous_command(line) and not line == 'mv --help':
        print(BLOCKED_MESSAGE)
        return True


def unblock_cd_commands(line):
    if line.startswith("mkdir") or (line.startswith("mv") and not line.strip() == 'mv --help'):
        print(BLOCKED_MESSAGE)
        return True
    return False


###########################################################################
# The following are used for cd commands in the story


def find_common_parent(path1, path2):
    """
    Find the largest common path between two absolute fake paths,
    e.g. ~/pueblo/.refugio-oculto and ~/granja/granero/.refugio
    """
    dirs1 = path1.split("/")
    dirs2 = path2.split("/")
    common = []
    for a, b in zip(dirs1, dirs2):
        if a != b:
            break
        common.append(a)
    return '/'.join(common)


def route_between_paths(start_path, end_path):
    """
    Returns:
        list of strings: every path you could hit on a direct route from
        start_path to end_path (both absolute fake paths).
    """
    common_path = find_common_parent(start_path, end_path)
    start_dirs = [d for d in start_path[len(common_path):].split("/") if d]
    end_dirs = [d for d in end_path[len(common_path):].split("/") if d]

    dest_paths = []
    current = start_path.split("/")
    for _ in start_dirs:
        current = current[:-1]
        dest_paths.append(os.path.expanduser("/".join(current)))

    current = "/".join(current)
    for d in end_dirs:
        current = os.path.join(current, d)
        dest_paths.append(os.path.expanduser(current))

    return dest_paths
