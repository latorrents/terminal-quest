# animation.py
#
# Animaciones de arte ASCII (el conejo, el pájaro, los fuegos artificiales...)
# dibujadas con curses.
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

import curses
import random
import shutil
import time

from terminal_quest.common import get_story_file
from terminal_quest.helpers import logger


class Animation:
    def __init__(self, filename):
        self.__screen = None
        self.__path = get_story_file(filename)

    def play_across_screen(self, cycles=1, start_direction='left-to-right', speed=10):
        return self.__play(lambda: self.__run_animation_across_screen(cycles, start_direction, speed))

    def play_finite(self, cycles=1):
        return self.__play(lambda: self.__run_animation(cycles))

    def __play(self, run):
        status = 1  # everything went wrong
        try:
            self.__init_curses()
            status = run()
        except Exception as e:
            logger.debug('Animation failed: {}'.format(e))
        finally:
            self.__shutdown_curses()
        return status

    def __init_curses(self):
        self.__screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.__screen.keypad(True)
        try:
            curses.curs_set(0)
        except curses.error:
            pass
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
        self.__screen.clear()
        self.__screen.refresh()

    def __shutdown_curses(self):
        if self.__screen is None:
            return
        try:
            curses.curs_set(1)
        except curses.error:
            pass
        self.__screen.keypad(False)
        self.__screen.clear()
        self.__screen.refresh()
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        self.__screen = None

    def __run_animation(self, max_cycles):
        frames = self.load_animation()
        ascii_h = animation_height(frames)
        w, h = get_width_height_of_terminal()

        frame = 0
        cycles = 0
        while True:
            for n in range(ascii_h):
                self.draw_fn(n, 0, " " * (w - 1))

            self.draw_frame(frames[frame], 0, 0)
            frame += 1
            if frame >= len(frames):
                frame = 0
                cycles += 1
                if cycles == max_cycles:
                    break

            self.__screen.refresh()
            time.sleep(0.15)

        return 0

    def __run_animation_across_screen(self, max_cycles, start_direction, speed):
        frames = self.load_animation()
        ascii_w = animation_width(frames)
        ascii_h = animation_height(frames)
        w, h = get_width_height_of_terminal()
        cx = w // 2

        if start_direction == "left-to-right":
            startx = -ascii_w
            offset_diff = speed
        else:
            startx = w
            offset_diff = -speed

        starty = randint(0, h - ascii_h - 1)

        frame = 0
        cycle = 0
        offsetx = 0
        while True:
            for n in range(ascii_h):
                self.draw_fn(starty + n, 0, " " * (w - 1))

            self.draw_frame(frames[frame], startx + offsetx, starty)
            frame = (frame + 1) % len(frames)
            offsetx += offset_diff

            if max_cycles == 0 and startx + offsetx >= (cx - ascii_w // 2):
                time.sleep(0.5)
                break
            # invert the direction
            elif startx + offsetx > w or startx + offsetx < -ascii_w:
                offset_diff = -offset_diff
                starty = randint(0, h - ascii_h - 1)
                cycle += 1
                if cycle >= max_cycles:
                    break

            self.__screen.refresh()
            time.sleep(0.15)

        return 0

    def load_animation(self):
        """
        Loads an ASCII art animation. Each frame is delimited by a line
        consisting only of '---'.
        """
        frames = []
        frame = []
        with open(self.__path, encoding='utf-8') as f:
            for line in f:
                line = line.rstrip("\n")
                if line == "---":
                    frames.append(frame)
                    frame = []
                else:
                    frame.append(line)
        if frame:
            frames.append(frame)
        return frames

    def draw_fn(self, y, x, msg):
        h, w = self.__screen.getmaxyx()
        if 0 <= y < h and x < w:
            try:
                self.__screen.addstr(y, x, msg[:max(0, w - x - 1)])
            except curses.error:
                pass

    def draw_frame(self, frame, x, y):
        """Draw a single frame from the [x, y] coordinates, clipping at the edges."""
        w, h = get_width_height_of_terminal()
        for n, line in enumerate(frame):
            clipped = line
            draw_x = x
            if draw_x < 0:
                clipped = clipped[-draw_x:]
                draw_x = 0
            clipped = clipped[:max(0, w - draw_x - 1)]
            if clipped:
                self.draw_fn(y + n, draw_x, clipped)


def get_width_height_of_terminal():
    size = shutil.get_terminal_size((80, 24))
    return size.columns, size.lines


def randint(a, b):
    return a if a >= b else random.randint(a, b)


def animation_width(animation):
    return max((len(line) for frame in animation for line in frame), default=0)


def animation_height(animation):
    return max((len(frame) for frame in animation), default=0)
