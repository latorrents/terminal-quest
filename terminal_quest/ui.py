# ui.py
#
# Muestra la historia, las pistas y los hechizos en la terminal.
#
# El texto usa un pequeño formato de colores: "{{XY:texto}}" donde X es el
# color y Y es "b" (negrita) o "n" (normal). Por ejemplo "{{yb:ls}}".
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

import os
import re
import select
import shutil
import sys
import termios
import time
import tty

from terminal_quest.common import get_username
from terminal_quest.helpers import get_ascii_art, strip_formatting
from terminal_quest.sound import SoundManager
from terminal_quest import titles

# 256-colour codes, close to the colours of the original storybook.
COLOURS = {
    'r': 167,  # red
    'g': 112,  # green
    'G': 191,  # light green
    'b': 74,   # blue
    'y': 220,  # yellow
    'o': 208,  # orange
    'w': 255,  # white
    'l': 147,  # lilac
    'c': 51,   # cyan
    'p': 177,  # purple
    'P': 212,  # pink
    'B': 158,  # light blue
}

RESET = "\033[0m"
MARKUP = re.compile(r"{{(\w+):(.*?)}}", re.S)
MAX_WIDTH = 100

NEWLINE_SLEEP = 0.06
CHAR_SLEEP = 0.012


def ansi_style(attr):
    codes = []
    if attr and attr[0] in COLOURS:
        codes.append("38;5;%d" % COLOURS[attr[0]])
    if len(attr) > 1 and attr[1] == 'b':
        codes.append("1")
    return "\033[%sm" % ";".join(codes) if codes else ""


def parse(string):
    """
    Split a formatted string into (text, ansi_style) segments.
    """
    segments = []
    pos = 0
    for match in MARKUP.finditer(string):
        if match.start() > pos:
            segments.append((string[pos:match.start()], ""))
        segments.append((match.group(2), ansi_style(match.group(1))))
        pos = match.end()
    if pos < len(string):
        segments.append((string[pos:], ""))
    return segments


def colourize(string):
    return "".join(style + text + (RESET if style else "") for text, style in parse(string))


def colourize_prompt(string, colour, bold=True):
    """Colourize text for the readline prompt (non printing chars are wrapped)."""
    style = ansi_style(colour + ('b' if bold else 'n'))
    return "\001%s\002%s\001%s\002" % (style, string, RESET)


def terminal_width():
    return min(shutil.get_terminal_size((80, 24)).columns, MAX_WIDTH) - 1


def wrap(string, width=None):
    """
    Insert newlines so the text wraps nicely at word boundaries,
    ignoring the formatting marks when measuring words.
    """
    width = width or terminal_width()
    wrapped_lines = []
    for line in string.split("\n"):
        if len(strip_formatting(line)) <= width:
            wrapped_lines.append(line)
            continue
        current = None
        current_len = 0
        for word in line.split(" "):
            word_len = len(strip_formatting(word))
            if current is None:
                current, current_len = word, word_len
            elif current_len + 1 + word_len > width and current_len:
                wrapped_lines.append(current)
                current, current_len = word, word_len
            else:
                current += " " + word
                current_len += 1 + word_len
        wrapped_lines.append(current)
    return "\n".join(wrapped_lines)


class KeyWatcher:
    """Detect key presses while the text is being typed, so it can be skipped."""

    def __enter__(self):
        self.fd = None
        if sys.stdin.isatty():
            self.fd = sys.stdin.fileno()
            self.old = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
        return self

    def pressed(self):
        if self.fd is None:
            return False
        ready, _, _ = select.select([self.fd], [], [], 0)
        if ready:
            os.read(self.fd, 1024)
            return True
        return False

    def __exit__(self, *args):
        if self.fd is not None:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old)


class GameUI:
    """
    Everything the story shows to the player goes through this class.
    It replaces the storybook window and the spellbook of the original game.
    """

    def __init__(self, typing=True):
        self.typing = typing and sys.stdout.isatty() and not os.environ.get('TQ_RAPIDO')
        self.dark = False
        self.sound = SoundManager()
        self.hint_sink = None
        self.__last_challenge = None
        self.__known_spells = []
        self.__help_shown = False

    # Output helpers

    def write(self, text):
        sys.stdout.write(text)
        sys.stdout.flush()

    def print_text(self, string):
        self.write(colourize(wrap(string)) + "\n")

    def print_art(self, string, colour=None):
        """Print ASCII art as it is, without wrapping it."""
        for line in string.splitlines():
            self.write(colourize("{{%sb:%s}}" % (colour, line) if colour and line else line) + "\n")

    def type_text(self, string):
        """Print formatted text with a typing effect. Pressing a key skips it."""
        string = wrap(string)
        plain = strip_formatting(string)
        sound_positions = {}
        for key_words, sound_name in self.sound.story_text_sound.items():
            index = plain.find(key_words)
            if index != -1:
                sound_positions[index] = sound_name

        if not self.typing:
            for sound_name in sound_positions.values():
                self.sound.play_sound(sound_name)
            self.write(colourize(string) + "\n")
            return

        position = 0
        skip = False
        with KeyWatcher() as keys:
            for text, style in parse(string):
                self.write(style)
                for char in text:
                    if position in sound_positions:
                        self.sound.play_sound(sound_positions[position])
                    position += 1
                    self.write(char)
                    if not skip:
                        skip = keys.pressed()
                        time.sleep(NEWLINE_SLEEP if char == "\n" else CHAR_SLEEP)
                if style:
                    self.write(RESET)
        self.write("\n")

    # Messages sent by the story

    def send_hint(self, string):
        if not string or not string.strip():
            return
        if self.hint_sink:
            self.hint_sink(string)
        else:
            self.type_text(string)

    send_text = send_hint

    def send_start_challenge_data(self, story, challenge, spells, highlighted, xp="", print_text=""):
        challenge = int(challenge)
        if challenge != self.__last_challenge:
            self.print_challenge_title(challenge)
            self.__last_challenge = challenge
        else:
            self.write("\n")

        if print_text:
            self.print_text(print_text + "\n")

        self.type_text(story)
        self.show_spells(spells, highlighted)

    def print_challenge_title(self, challenge):
        if challenge == 0:
            text = "INTRODUCCIÓN"
        else:
            title = titles.challenges.get(challenge, {}).get('title', '')
            text = "DESAFÍO {}: {}".format(challenge, title) if title else "DESAFÍO {}".format(challenge)

        colour = 'r' if self.dark else 'o'
        border = "═" * (len(text) + 4)
        self.write("\n")
        self.print_text("{{%sb:╔%s╗}}" % (colour, border))
        self.print_text("{{%sb:║  %s  ║}}" % (colour, text))
        self.print_text("{{%sb:╚%s╝}}" % (colour, border))
        self.write("\n")

    def show_spells(self, spells, highlighted):
        if isinstance(highlighted, str):
            highlighted = [highlighted]
        spells = list(spells or [])
        if spells == self.__known_spells and not highlighted:
            return

        new_spells = [s for s in spells if s not in self.__known_spells]
        self.__known_spells = spells
        if not spells:
            return

        parts = []
        for spell in spells:
            if spell in highlighted or spell in new_spells and self.__help_shown:
                parts.append("{{gb:%s ✦}}" % spell)
            else:
                parts.append("{{yb:%s}}" % spell)

        self.write("\n")
        self.print_text("{{lb:Tus hechizos:}} " + "  ".join(parts))
        if not self.__help_shown:
            self.print_text("{{ln:Escribe}} {{yb:ayuda}} {{ln:para ver qué hace cada hechizo.}}")
            self.__help_shown = True
        self.write("\n")

    def show_spell_help(self, spells, spell=None):
        if spell:
            if spell not in spells:
                self.print_text("{{rb:Todavía no conoces el hechizo}} {{yb:%s}}{{rb:.}}" % spell)
                return
            self.print_art(get_ascii_art(spell + "_tooltip"))
            return

        self.print_text("\n{{lb:Hechizos que conoces:}} " + "  ".join("{{yb:%s}}" % s for s in spells))
        self.print_text("{{ln:Escribe}} {{yb:ayuda <hechizo>}} {{ln:para saber más, por ejemplo}} "
                        "{{yb:ayuda %s}}{{ln:.}}" % spells[-1])
        self.print_text("{{ln:Escribe}} {{yb:salir}} {{ln:para guardar y salir del juego.}}\n")

    def set_dark_theme(self):
        self.dark = True

    def set_normal_theme(self):
        self.dark = False

    def finish_if_server_ready(self, other_condition):
        return other_condition

    def challenge_completed(self, challenge):
        if challenge > 0:
            self.print_text("\n{{gb:✔ ¡Desafío %d superado!}}" % challenge)

    def exit(self):
        self.print_banner("finished_terminal_quest")

    def print_banner(self, filename):
        lines = get_ascii_art(filename).splitlines()
        self.write("\n")
        for line in lines:
            self.write(colourize("{{yb:%s}}" % line) + "\n")
            if self.typing:
                time.sleep(0.15)
        self.write("\n")

    @staticmethod
    def clear():
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def greeting_name():
    return get_username()
