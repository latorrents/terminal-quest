# commands.py
#
# Los comandos de la terminal, escritos en Python para que el juego no
# dependa de ningún programa externo. Imitan a los comandos reales de Linux
# con mensajes en español.
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

import glob
import grp
import os
import pwd
import shlex
import shutil
import stat
import time

from terminal_quest.common import fake_home_dir
from terminal_quest.sound import SoundManager
from terminal_quest.ui import colourize

sounds_manager = SoundManager()

NOT_FOUND = "No existe el archivo o el directorio"
PERMISSION_DENIED = "Permiso denegado"
IS_A_DIRECTORY = "Es un directorio"
NOT_A_DIRECTORY = "No es un directorio"
FILE_EXISTS = "El archivo ya existe"


def split_args(line):
    """Split the line into arguments, respecting quotes when possible."""
    line = line.strip()
    if not line:
        return []
    try:
        return shlex.split(line)
    except ValueError:
        return line.split()


def to_real(real_loc, path):
    """Turn a path typed by the player into a real path on disk."""
    if path == "~" or path.startswith("~/"):
        path = fake_home_dir + path[1:]
    return os.path.normpath(os.path.join(real_loc, path))


def to_fake(path):
    return path.replace(fake_home_dir, "~")


def expand_globs(real_loc, args):
    """Expand * and ? like the shell does."""
    expanded = []
    for arg in args:
        if any(c in arg for c in "*?[") and not arg.startswith("-"):
            matches = sorted(glob.glob(to_real(real_loc, arg)))
            if matches:
                for match in matches:
                    expanded.append(os.path.relpath(match, real_loc) if not arg.startswith("~")
                                    else to_fake(match))
                continue
        expanded.append(arg)
    return expanded


def split_flags(args):
    flags = ""
    others = []
    for arg in args:
        if arg.startswith("-") and len(arg) > 1 and not arg.startswith("--"):
            flags += arg[1:]
        else:
            others.append(arg)
    return flags, others


def path_error(path):
    """
    Returns None if the path can be reached, otherwise the error message
    (the path doesn't exist, or a folder on the way can't be entered).
    """
    try:
        os.lstat(path)
        return None
    except PermissionError:
        return PERMISSION_DENIED
    except OSError:
        return NOT_FOUND


def colour_file_dir(path, name):
    """Colourize the files and directories consistently."""
    if os.path.isdir(path):
        return colourize("{{bb:%s}}" % name)
    if os.path.isfile(path) and os.access(path, os.X_OK):
        return colourize("{{gb:%s}}" % name)
    return name


def sort_key(name):
    return name.lstrip(".").lower()


def permission_string(mode):
    kind = "d" if stat.S_ISDIR(mode) else "-"
    chars = ""
    for who in (stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR,
                stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
                stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH):
        chars += "rwxrwxrwx"[len(chars)] if mode & who else "-"
    return kind + chars


def long_line(path, name):
    info = os.lstat(path)
    try:
        user = pwd.getpwuid(info.st_uid).pw_name
    except KeyError:
        user = str(info.st_uid)
    try:
        group = grp.getgrgid(info.st_gid).gr_name
    except KeyError:
        group = str(info.st_gid)
    date = time.strftime("%d %b %H:%M", time.localtime(info.st_mtime))
    return "{} {} {} {} {:>5} {} {}".format(
        permission_string(info.st_mode), info.st_nlink, user, group, info.st_size, date,
        colour_file_dir(path, name)
    )


###########################################################################
# ls


def ls(real_loc, line, has_access=True):
    """
    Prints the coloured output of ls.

    Returns:
        str: the names shown, separated by spaces (used by the challenges).
    """
    if not has_access:
        print("ls: no se puede abrir el directorio {}: {}".format(line, PERMISSION_DENIED))
        return

    flags, targets = split_flags(expand_globs(real_loc, split_args(line)))
    show_all = "a" in flags
    long_format = "l" in flags
    one_per_line = "1" in flags

    if not targets:
        targets = ["."]

    output_names = []
    printed_something = False
    for index, target in enumerate(targets):
        path = to_real(real_loc, target)

        error = path_error(path)
        if error:
            print("ls: no se puede acceder a '{}': {}".format(target, error))
            continue

        if not os.path.isdir(path):
            output_names.append(target)
            print(long_line(path, target) if long_format else colour_file_dir(path, target))
            continue

        try:
            names = os.listdir(path)
        except PermissionError:
            print("ls: no se puede abrir el directorio '{}': {}".format(target, PERMISSION_DENIED))
            continue

        if show_all:
            names += [".", ".."]
        else:
            names = [n for n in names if not n.startswith(".")]
        names.sort(key=sort_key)
        output_names += names

        if len(targets) > 1:
            if printed_something:
                print("")
            print("{}:".format(target))

        if long_format:
            for name in names:
                try:
                    print(long_line(os.path.join(path, name), name))
                except PermissionError:
                    print("?????????? ? ? ? ? ? {}".format(name))
        elif names:
            separator = "\n" if one_per_line else "  "
            print(separator.join(colour_file_dir(os.path.join(path, n), n) for n in names))
        printed_something = True

    return " ".join(output_names)


###########################################################################
# cat


def cat(real_loc, line):
    args = split_args(line)
    if not args:
        print("cat: falta el nombre del archivo que quieres examinar")
        return False

    success = True
    for arg in expand_globs(real_loc, args):
        path = to_real(real_loc, arg)
        error = path_error(path)
        if error:
            print("cat: {}: {}".format(arg, error))
            success = False
        elif os.path.isdir(path):
            print("cat: {}: {}".format(arg, IS_A_DIRECTORY))
            success = False
        else:
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    contents = f.read()
            except PermissionError:
                print("cat: {}: {}".format(arg, PERMISSION_DENIED))
                success = False
                continue
            print(colourize(contents))
            sounds_manager.on_command_run(["cat", arg])
    return success


###########################################################################
# cd


def cd(real_path, line, has_access=True):
    """
    Returns:
        str: the new real path (the same one if the path doesn't exist).
    """
    if not has_access:
        print("bash: cd: {}: {}".format(line, PERMISSION_DENIED))
        return

    line = line.strip()
    if not line or line == "~":
        new_path = fake_home_dir
    else:
        new_path = to_real(real_path, line)
        error = path_error(new_path)
        if error or not os.path.isdir(new_path):
            print("bash: cd: {}: {}".format(line, error or NOT_A_DIRECTORY))
            new_path = real_path

    return new_path.rstrip("/") or "/"


###########################################################################
# mv


MV_HELP = """Uso: mv ORIGEN DESTINO
  o:  mv ORIGEN... DIRECTORIO
Cambia el nombre de ORIGEN a DESTINO, o mueve ORIGEN(es) a DIRECTORIO.

Ejemplos:
  mv manzana canasta/     mueve la manzana dentro de la canasta
  mv manzana pera         cambia el nombre de manzana a pera
  mv canasta/* ./         mueve todo lo que hay en la canasta aquí"""


def mv(real_loc, line):
    args = split_args(line)
    if "--help" in args:
        print(MV_HELP)
        return True

    flags, args = split_flags(expand_globs(real_loc, args))
    if len(args) < 2:
        if not args:
            print("mv: falta un archivo como argumento")
        else:
            print("mv: falta el archivo de destino después de '{}'".format(args[0]))
        return False

    sources, destination = args[:-1], args[-1]
    dest_path = to_real(real_loc, destination)

    if len(sources) > 1 and not os.path.isdir(dest_path):
        print("mv: el destino '{}' no es un directorio".format(destination))
        return False

    success = True
    for source in sources:
        src_path = to_real(real_loc, source)
        error = path_error(src_path)
        if error:
            print("mv: no se puede efectuar 'stat' sobre '{}': {}".format(source, error))
            success = False
            continue

        target = dest_path
        if os.path.isdir(dest_path):
            target = os.path.join(dest_path, os.path.basename(src_path))

        if os.path.abspath(target) == os.path.abspath(src_path):
            print("mv: '{}' y '{}' son el mismo archivo".format(source, destination))
            success = False
            continue

        try:
            if os.path.isdir(target) and not os.path.isdir(src_path):
                print("mv: no se puede sobrescribir el directorio '{}' con un archivo".format(to_fake(target)))
                success = False
                continue
            os.replace(src_path, target)
        except PermissionError:
            print("mv: no se puede mover '{}' a '{}': {}".format(source, destination, PERMISSION_DENIED))
            success = False
            continue
        except OSError as e:
            print("mv: no se puede mover '{}' a '{}': {}".format(source, destination, e.strerror))
            success = False
            continue

        sounds_manager.on_command_run(["mv", source, destination])
    return success


###########################################################################
# echo


def echo(real_loc, line):
    words = split_args(line)
    text = " ".join(words)
    if words and words[0] == "-n":
        text = " ".join(words[1:])
    print(text)
    return text


###########################################################################
# mkdir


def mkdir(real_loc, line):
    flags, args = split_flags(split_args(line))
    if not args:
        print("mkdir: falta el nombre de la carpeta que quieres crear")
        return False

    success = True
    for arg in args:
        path = to_real(real_loc, arg)
        try:
            if "p" in flags:
                os.makedirs(path, exist_ok=True)
            else:
                os.mkdir(path)
        except FileExistsError:
            print("mkdir: no se puede crear el directorio «{}»: {}".format(arg, FILE_EXISTS))
            success = False
        except FileNotFoundError:
            print("mkdir: no se puede crear el directorio «{}»: {}".format(arg, NOT_FOUND))
            success = False
        except PermissionError:
            print("mkdir: no se puede crear el directorio «{}»: {}".format(arg, PERMISSION_DENIED))
            success = False
        else:
            sounds_manager.on_command_run(["mkdir", arg])
    return success


###########################################################################
# chmod


PERMISSION_BITS = {
    "r": (stat.S_IRUSR, stat.S_IRGRP, stat.S_IROTH),
    "w": (stat.S_IWUSR, stat.S_IWGRP, stat.S_IWOTH),
    "x": (stat.S_IXUSR, stat.S_IXGRP, stat.S_IXOTH),
}
WHO_INDEX = {"u": 0, "g": 1, "o": 2}


def new_mode(mode, spec):
    """
    Apply a symbolic (u+x, +rw, a-w, ...) or octal (755) mode to mode.
    Returns None if the spec is not valid.
    """
    if spec.isdigit() and all(c in "01234567" for c in spec):
        return int(spec, 8)

    umask = os.umask(0)
    os.umask(umask)

    for clause in spec.split(","):
        who = ""
        i = 0
        while i < len(clause) and clause[i] in "ugoa":
            who += clause[i]
            i += 1
        if i >= len(clause) or clause[i] not in "+-=":
            return None
        operator = clause[i]
        perms = clause[i + 1:]
        if any(p not in "rwx" for p in perms):
            return None

        bits = 0
        for p in perms:
            for index, bit in enumerate(PERMISSION_BITS[p]):
                if not who or "a" in who or any(WHO_INDEX[w] == index for w in who if w in WHO_INDEX):
                    bits |= bit
        if not who:
            # Like the real chmod, without "who" the umask is respected
            bits &= ~umask

        if operator == "+":
            mode |= bits
        elif operator == "-":
            mode &= ~bits
        else:
            mode = (mode & ~0o777) | bits
    return mode


def chmod(real_loc, line):
    args = split_args(line)
    if not args:
        print("chmod: falta un operando")
        return False
    if len(args) == 1:
        print("chmod: falta un operando después de «{}»".format(args[0]))
        return False

    spec, files = args[0], expand_globs(real_loc, args[1:])
    success = True
    for name in files:
        path = to_real(real_loc, name)
        error = path_error(path)
        if error:
            print("chmod: no se puede acceder a '{}': {}".format(name, error))
            success = False
            continue
        mode = new_mode(os.stat(path).st_mode & 0o777, spec)
        if mode is None:
            print("chmod: modo inválido: «{}»".format(spec))
            return False
        try:
            os.chmod(path, mode)
        except PermissionError:
            print("chmod: cambiando los permisos de '{}': {}".format(name, PERMISSION_DENIED))
            success = False
    return success


###########################################################################
# rm


def rm(real_loc, line):
    flags, args = split_flags(expand_globs(real_loc, split_args(line)))
    recursive = "r" in flags or "R" in flags
    force = "f" in flags
    if not args:
        if not force:
            print("rm: falta un operando")
        return False

    success = True
    for name in args:
        path = to_real(real_loc, name)
        error = path_error(path)
        if error:
            if not force or error == PERMISSION_DENIED:
                print("rm: no se puede borrar '{}': {}".format(name, error))
                success = False
            continue
        try:
            if os.path.isdir(path) and not os.path.islink(path):
                if not recursive:
                    print("rm: no se puede borrar '{}': {}".format(name, IS_A_DIRECTORY))
                    success = False
                    continue
                shutil.rmtree(path)
            else:
                os.remove(path)
        except PermissionError:
            print("rm: no se puede borrar '{}': {}".format(name, PERMISSION_DENIED))
            success = False
    return success


###########################################################################
# cp (only used by the scripts inside the game)


def cp(real_loc, line):
    flags, args = split_flags(expand_globs(real_loc, split_args(line)))
    if len(args) < 2:
        print("cp: falta un archivo como argumento")
        return False
    sources, destination = args[:-1], to_real(real_loc, args[-1])
    success = True
    for source in sources:
        src_path = to_real(real_loc, source)
        try:
            if os.path.isdir(src_path):
                target = destination
                if os.path.isdir(destination):
                    target = os.path.join(destination, os.path.basename(src_path))
                shutil.copytree(src_path, target)
            else:
                shutil.copy(src_path, destination)
        except FileNotFoundError:
            print("cp: no se puede efectuar 'stat' sobre '{}': {}".format(source, NOT_FOUND))
            success = False
        except PermissionError:
            print("cp: no se puede copiar '{}': {}".format(source, PERMISSION_DENIED))
            success = False
        except shutil.SameFileError:
            print("cp: '{}' y '{}' son el mismo archivo".format(source, args[-1]))
            success = False
    return success


###########################################################################
# Running scripts (./script.sh)


def run_executable(real_path, line):
    """
    Runs a script from the game world. The scripts are interpreted line by
    line with the commands above, so no real shell is needed.
    """
    from terminal_quest.animation import Animation

    args = split_args(line)
    script = to_real(real_path, args[0])
    script_name = os.path.basename(script)

    try:
        with open(script, encoding="utf-8") as f:
            script_lines = f.read().splitlines()
    except PermissionError:
        print("bash: {}: {}".format(args[0], PERMISSION_DENIED))
        return
    except OSError:
        print("bash: {}: {}".format(args[0], NOT_FOUND))
        return

    builtins = {"echo": echo, "mkdir": mkdir, "cp": cp, "ls": ls, "cat": cat,
                "mv": mv, "rm": rm, "chmod": chmod}

    for number, script_line in enumerate(script_lines, start=1):
        script_line = script_line.strip()
        if not script_line or script_line.startswith("#"):
            continue
        command, _, rest = script_line.partition(" ")
        if command == "animacion":
            Animation(rest.strip()).play_finite(cycles=1)
        elif command in builtins:
            builtins[command](real_path, rest)
        else:
            print("{}: línea {}: {}: orden no encontrada".format(script_name, number, command))

    sounds_manager.on_command_run([script_name])
