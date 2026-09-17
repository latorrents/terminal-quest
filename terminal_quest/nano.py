# nano.py
#
# Un editor de texto sencillo que imita a GNU nano, escrito con curses.
# Reemplaza al nano modificado que usaba el juego original: en lugar de
# comunicarse por una tubería, avisa directamente a la lógica del desafío.
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

import curses
import os

from terminal_quest.commands import to_real, split_args
from terminal_quest.helpers import strip_formatting

SAVE_PROMPT = "¿Guardar el búfer modificado? (Responder \"No\" DESCARTARÁ los cambios)"
FILENAME_PROMPT = "Nombre del archivo a escribir"

SHORTCUTS = [
    ("^G", "Ayuda"), ("^O", "Guardar"), ("^X", "Salir"),
    ("^K", "Cortar línea"), ("^U", "Pegar"), ("^C", "Cancelar"),
]

HELP_TEXT = [
    "Ayuda de nano",
    "",
    "Escribe normalmente para añadir texto al archivo.",
    "Usa las flechas para mover el cursor.",
    "",
    "Ctrl O  Guardar el archivo",
    "Ctrl X  Salir (si hay cambios, te pregunta si quieres guardarlos)",
    "Ctrl K  Cortar la línea actual",
    "Ctrl U  Pegar la última línea cortada",
    "Ctrl C  Cancelar una pregunta",
    "",
    "Pulsa cualquier tecla para volver.",
]

KEY_CTRL = {chr(ord(c) - 64): c for c in "CGKOUXY"}


def plural(count, singular, plural_text):
    return "{} {}".format(count, singular if count == 1 else plural_text)


class NanoListener:
    """Receives what happens inside the editor. StepNano implements it."""

    def nano_opened(self, filename):
        pass

    def contents_changed(self, text):
        pass

    def prompt_shown(self, prompt, editable=""):
        pass

    def prompt_answered(self, answer):
        pass

    def file_saved(self, filename):
        pass

    def nano_closed(self):
        pass


class Editor:
    def __init__(self, real_loc, filename, listener=None):
        self.real_loc = real_loc
        self.filename = filename
        self.listener = listener or NanoListener()
        self.lines = [""]
        self.cy = 0
        self.cx = 0
        self.top = 0
        self.modified = False
        self.status = ""
        self.hint = ""
        self.cut_buffer = None
        self.screen = None

    # Public

    def set_hint(self, text):
        self.hint = text.strip()
        if self.screen:
            self.draw()

    def run(self):
        self.load()
        curses.wrapper(self.main)

    # File handling

    def load(self):
        if not self.filename:
            return
        path = to_real(self.real_loc, self.filename)
        if os.path.isdir(path):
            self.status = "[ «{}» es un directorio ]".format(self.filename)
            self.filename = ""
        elif os.path.exists(path):
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    text = f.read()
                if text.endswith("\n"):
                    text = text[:-1]
                self.lines = text.split("\n")
                self.status = "[ {} ]".format(plural(len(self.lines), "línea leída", "líneas leídas"))
            except PermissionError:
                self.status = "[ Error al leer {}: Permiso denegado ]".format(self.filename)
        else:
            self.status = "[ Archivo nuevo ]"

    def save(self, filename):
        path = to_real(self.real_loc, filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.lines) + "\n")
        except PermissionError:
            self.status = "[ Error al escribir {}: Permiso denegado ]".format(filename)
            return False
        except OSError as e:
            self.status = "[ Error al escribir {}: {} ]".format(filename, e.strerror)
            return False
        self.filename = filename
        self.modified = False
        self.status = "[ {} ]".format(plural(len(self.lines), "línea escrita", "líneas escritas"))
        self.listener.file_saved(filename)
        return True

    # Drawing

    def main(self, screen):
        self.screen = screen
        curses.raw()
        curses.use_default_colors()
        if curses.has_colors():
            curses.init_pair(1, curses.COLOR_GREEN, -1)
            curses.init_pair(2, curses.COLOR_YELLOW, -1)
        screen.keypad(True)
        self.listener.nano_opened(self.filename)
        self.loop()
        self.listener.nano_closed()
        self.screen = None

    def text_height(self):
        h, _ = self.screen.getmaxyx()
        return max(1, h - 5)

    def safe_addstr(self, y, x, text, attr=0):
        h, w = self.screen.getmaxyx()
        if y < 0 or y >= h or x >= w:
            return
        try:
            self.screen.addstr(y, x, text[:max(0, w - x - 1)], attr)
        except curses.error:
            pass

    def draw(self, prompt=None):
        screen = self.screen
        h, w = screen.getmaxyx()
        screen.erase()

        title = "  GNU nano (Terminal Quest)"
        name = "Archivo: " + self.filename if self.filename else "Nuevo búfer"
        header = title + name.center(max(0, w - len(title) * 2)) + ("Modificado" if self.modified else "")
        self.safe_addstr(0, 0, header.ljust(w), curses.A_REVERSE)

        height = self.text_height()
        if self.cy < self.top:
            self.top = self.cy
        elif self.cy >= self.top + height:
            self.top = self.cy - height + 1

        offset = max(0, self.cx - (w - 2))
        for row in range(height):
            index = self.top + row
            if index >= len(self.lines):
                break
            line = self.lines[index]
            shown = line[offset:] if index == self.cy else line
            self.safe_addstr(row + 1, 0, shown)

        if self.hint:
            hint = strip_formatting(self.hint).replace("\n", " ")
            self.safe_addstr(h - 4, 0, hint, curses.color_pair(2) | curses.A_BOLD)

        if prompt is not None:
            self.safe_addstr(h - 3, 0, prompt.ljust(w), curses.A_REVERSE)
        elif self.status:
            self.safe_addstr(h - 3, max(0, (w - len(self.status)) // 2), self.status, curses.A_REVERSE)

        if prompt is not None and prompt.startswith(SAVE_PROMPT):
            shortcuts = [("S", "Sí"), ("N", "No"), ("^C", "Cancelar")]
        elif prompt is not None:
            shortcuts = [("Enter", "Confirmar"), ("^C", "Cancelar")]
        else:
            shortcuts = SHORTCUTS
        x = 0
        for key, label in shortcuts:
            self.safe_addstr(h - 2, x, key, curses.A_REVERSE)
            self.safe_addstr(h - 2, x + len(key) + 1, label)
            x += len(key) + len(label) + 4

        if prompt is not None:
            screen.move(h - 3, min(len(prompt), w - 1))
        else:
            screen.move(self.cy - self.top + 1, min(self.cx - offset, w - 1))
        screen.refresh()

    # Input

    def read_key(self):
        try:
            return self.screen.get_wch()
        except curses.error:
            return None
        except KeyboardInterrupt:
            return "\x03"

    def loop(self):
        while True:
            self.draw()
            key = self.read_key()
            if key is None:
                continue
            self.status = ""

            if key == "\x18":  # Ctrl X
                if self.exit():
                    return
            elif key == "\x0f":  # Ctrl O
                self.ask_filename_and_save()
            elif key == "\x07":  # Ctrl G
                self.show_help()
            elif key == "\x0b":  # Ctrl K
                self.cut_line()
            elif key == "\x15":  # Ctrl U
                self.paste_line()
            elif key == "\x03":  # Ctrl C
                self.status = "[ línea {}/{}, columna {} ]".format(self.cy + 1, len(self.lines), self.cx + 1)
            else:
                self.handle_edit_key(key)

    def handle_edit_key(self, key):
        line = self.lines[self.cy]
        changed = False

        if key in (curses.KEY_UP,):
            self.cy = max(0, self.cy - 1)
        elif key in (curses.KEY_DOWN,):
            self.cy = min(len(self.lines) - 1, self.cy + 1)
        elif key in (curses.KEY_LEFT,):
            if self.cx > 0:
                self.cx -= 1
            elif self.cy > 0:
                self.cy -= 1
                self.cx = len(self.lines[self.cy])
        elif key in (curses.KEY_RIGHT,):
            if self.cx < len(line):
                self.cx += 1
            elif self.cy < len(self.lines) - 1:
                self.cy += 1
                self.cx = 0
        elif key in (curses.KEY_HOME, "\x01"):
            self.cx = 0
        elif key in (curses.KEY_END, "\x05"):
            self.cx = len(line)
        elif key in (curses.KEY_BACKSPACE, "\x7f", "\x08"):
            if self.cx > 0:
                self.lines[self.cy] = line[:self.cx - 1] + line[self.cx:]
                self.cx -= 1
                changed = True
            elif self.cy > 0:
                self.cx = len(self.lines[self.cy - 1])
                self.lines[self.cy - 1] += line
                del self.lines[self.cy]
                self.cy -= 1
                changed = True
        elif key in (curses.KEY_DC, "\x04"):
            if self.cx < len(line):
                self.lines[self.cy] = line[:self.cx] + line[self.cx + 1:]
                changed = True
            elif self.cy < len(self.lines) - 1:
                self.lines[self.cy] += self.lines.pop(self.cy + 1)
                changed = True
        elif key in ("\n", "\r", curses.KEY_ENTER):
            self.lines[self.cy] = line[:self.cx]
            self.lines.insert(self.cy + 1, line[self.cx:])
            self.cy += 1
            self.cx = 0
            changed = True
        elif key == "\t":
            self.lines[self.cy] = line[:self.cx] + "    " + line[self.cx:]
            self.cx += 4
            changed = True
        elif isinstance(key, str) and key.isprintable():
            self.lines[self.cy] = line[:self.cx] + key + line[self.cx:]
            self.cx += 1
            changed = True

        self.cx = min(self.cx, len(self.lines[self.cy]))
        if changed:
            self.content_changed()

    def content_changed(self):
        self.modified = True
        self.listener.contents_changed("\n".join(self.lines))

    def cut_line(self):
        self.cut_buffer = self.lines[self.cy]
        if len(self.lines) > 1:
            del self.lines[self.cy]
            self.cy = min(self.cy, len(self.lines) - 1)
        else:
            self.lines = [""]
        self.cx = 0
        self.content_changed()

    def paste_line(self):
        if self.cut_buffer is None:
            return
        self.lines.insert(self.cy, self.cut_buffer)
        self.cy += 1
        self.cx = 0
        self.content_changed()

    def show_help(self):
        self.screen.erase()
        for row, text in enumerate(HELP_TEXT):
            self.safe_addstr(row + 1, 2, text, curses.A_BOLD if row == 0 else 0)
        self.screen.refresh()
        self.read_key()

    def ask(self, prompt, editable=None):
        """
        Show a prompt at the bottom. If editable is None the answer is a
        single key (S/N), otherwise the user edits a line of text.
        Returns the answer, or None if cancelled.
        """
        self.listener.prompt_shown(prompt, editable or "")
        while True:
            if editable is None:
                self.draw(prompt + " ")
            else:
                self.draw("{}: {}".format(prompt, editable))
            key = self.read_key()
            if key == "\x03":
                self.status = "[ Cancelado ]"
                self.listener.prompt_answered("cancel")
                return None
            if editable is None:
                if isinstance(key, str) and key.lower() in ("s", "y"):
                    self.listener.prompt_answered("yes")
                    return "yes"
                if isinstance(key, str) and key.lower() == "n":
                    self.listener.prompt_answered("no")
                    return "no"
            else:
                if key in ("\n", "\r", curses.KEY_ENTER):
                    return editable
                if key in (curses.KEY_BACKSPACE, "\x7f", "\x08"):
                    editable = editable[:-1]
                elif isinstance(key, str) and key.isprintable():
                    editable += key
                else:
                    continue
                self.listener.prompt_shown(prompt, editable)

    def ask_filename_and_save(self):
        filename = self.ask(FILENAME_PROMPT, self.filename)
        if filename is None:
            return False
        if not filename.strip():
            self.status = "[ Cancelado ]"
            self.listener.prompt_answered("cancel")
            return False
        return self.save(filename.strip())

    def exit(self):
        if not self.modified:
            return True
        answer = self.ask(SAVE_PROMPT)
        if answer == "no":
            return True
        if answer == "yes":
            return self.ask_filename_and_save()
        return False


def nano(real_loc, line, listener=None, hint_owner=None):
    """
    Open the editor.

    Args:
        real_loc (str): where the player is.
        line (str): what the player typed after nano.
        listener (NanoListener): gets told about what happens in the editor.
        hint_owner: object with a hint_sink attribute (the GameUI), so the hints
            sent while nano is open are shown inside the editor.
    """
    args = split_args(line)
    filename = args[0] if args else ""
    editor = Editor(real_loc, filename, listener)

    previous_sink = None
    if hint_owner is not None:
        previous_sink = hint_owner.hint_sink
        hint_owner.hint_sink = editor.set_hint
    try:
        editor.run()
    finally:
        if hint_owner is not None:
            hint_owner.hint_sink = previous_sink
