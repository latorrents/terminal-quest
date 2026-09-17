# step.py
#
# La plantilla de la que heredan todos los pasos de la historia.
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

import os

from terminal_quest.common import get_username
from terminal_quest.file_tree import delete_items, modify_file_tree
from terminal_quest.helpers import record_user_interaction
from terminal_quest.location import PlayerLocation, generate_real_path
from terminal_quest.nano import NanoListener, SAVE_PROMPT, FILENAME_PROMPT
from terminal_quest.step_helpers import unblock_commands


class StepTemplate:
    highlighted_commands = []
    print_text = None
    story = [""]
    start_dir = "~"
    dirs_to_attempt = None
    end_dir = "~"
    commands = ""
    hints = [""]
    output_condition = lambda x, y: False
    deleted_items = None
    file_list = None
    TerminalClass = None
    prev_command = ""
    companion_speech = ""
    companion_command = ""
    dark_theme = False

    def __init__(self, client):
        self._client = client

        # Copy the hints so popping them doesn't change the class
        self.hints = list(self.hints)

        self._run_at_start()
        self.__set_theme()
        self._location = PlayerLocation(self.start_dir, self.end_dir)
        self._nano = StepNano(client, self, self._location)
        self._setup_nano()
        self.__modify_file_system()

        if isinstance(self.hints, str):
            raise Exception("Hint is a string! Make it a list")

        self._last_user_input = ""
        self._is_finished = False
        self.__command_blocked = False
        self._terminal = self.TerminalClass(self, self._location, self.dirs_to_attempt, self._client)

    def __set_theme(self):
        if self.dark_theme:
            self.send_dark_theme()

    def get_nano_logic(self):
        return self._nano

    def _run_at_start(self):
        # Hook to run at start
        pass

    def _setup_nano(self):
        # override and set nano values in here.
        pass

    def __modify_file_system(self):
        delete_items(self.deleted_items)
        modify_file_tree(self.file_list)

    def _run_after_text(self):
        pass

    def run(self):
        self._run_after_text()
        self._terminal.cmdloop()

    def terminal_command_passed(self):
        return self._terminal.passed

    def next(self):
        raise Exception("IStep method not implemented")

    def is_finished_step(self, last_user_input, last_cmd_output):
        return self.check_output(last_cmd_output) or self.check_command(last_user_input)

    def block_command(self, last_user_input):
        # default behaviour
        return unblock_commands(last_user_input, self.commands)

    def check_command(self, last_user_input):
        return self._default_check_command(last_user_input)

    def check_output(self, output):
        if not output or not isinstance(output, str):
            return False
        return self.output_condition(output.strip())

    def set_last_user_input(self, last_user_input):
        self._last_user_input = last_user_input

    def get_last_user_input(self):
        return self._last_user_input

    def get_location(self):
        return self._location

    def is_finished_game(self):
        return self._is_finished

    def _is_at_end_dir(self):
        return self._location.is_at_end_dir()

    def get_fake_path(self):
        return self._location.get_fake_path()

    def _default_check_command(self, last_user_input):
        command_validated = self._validate_check_command(last_user_input)
        end_dir_validated = self._validate_end_dir()
        terminal_command_passed = self.terminal_command_passed()
        passed = command_validated and end_dir_validated and terminal_command_passed
        if not passed:
            self.send_stored_hint()
        return passed

    def _validate_check_command(self, last_user_input):
        if not self.commands:
            return True
        if isinstance(self.commands, str):
            return last_user_input == self.commands
        return last_user_input in self.commands

    def _validate_end_dir(self):
        if not self.end_dir:
            return True
        return self._location.get_fake_path() == self.end_dir

    def send_stored_hint(self):
        self._client.send_hint('\n' + self.hints[0])
        if len(self.hints) > 1:
            self.hints.pop(0)

    def send_hint(self, string):
        if isinstance(string, (list, tuple)):
            string = "\n".join(string)
        self._client.send_hint('\n' + string)

    def send_dark_theme(self):
        self._client.set_dark_theme()

    def send_normal_theme(self):
        self._client.set_normal_theme()

    def get_print_text(self):
        if not self.print_text:
            return ""
        lines = [self.print_text] if isinstance(self.print_text, str) else list(self.print_text)
        return "{{yb:" + get_username() + ":}} " + "\n".join(lines)

    def exit(self):
        self._is_finished = True
        self._client.exit()

    def set_command_blocked(self, blocked):
        self.__command_blocked = blocked

    def get_command_blocked(self):
        return self.__command_blocked

    def _companion_speaks(self, line):
        """
        :param line: last line user typed
        :return: boolean, depending on whether the companion spoke
        """
        if line == self.companion_command and self.companion_speech:
            self.send_hint("\n" + self.companion_speech)
            record_user_interaction(self, "_".join(self.companion_command.split(" ")))
            return True
        return False

    def check_nano_contents(self):
        pass


class StepNano(NanoListener):
    """
    Keeps track of what the player does inside nano, so the story can give
    hints while the editor is open.
    """

    SAVING_NANO_PROMPT = SAVE_PROMPT
    SAVE_FILENAME = FILENAME_PROMPT

    def __init__(self, client, step, location):
        self.__client = client
        self.__step = step
        self.__location = location

        self.__nano_content = ""
        self.__nano_running = False
        self.__last_nano_prompt = ""
        self.__on_filename_screen = False
        self.__save_prompt_showing = False
        self.__last_nano_filename = ""
        self.__editable = ""
        self.__goal_nano_save_name = ""
        self.__goal_nano_end_content = ""
        self.__goal_nano_filepath = ""

    # Getters and setters

    def set_nano_running(self, nano_running):
        self.__nano_running = nano_running

    def get_nano_running(self):
        return self.__nano_running

    def set_last_nano_filename(self, filename):
        self.__last_nano_filename = filename

    def get_last_nano_filename(self):
        return self.__last_nano_filename

    def get_editable(self):
        return self.__editable

    def set_editable(self, editable):
        self.__editable = editable

    def set_nano_content(self, nano_content):
        self.__nano_content = nano_content

    def get_nano_content(self):
        return self.__nano_content

    def set_goal_nano_save_name(self, goal_nano_save_name):
        self.__goal_nano_save_name = goal_nano_save_name

    def get_goal_nano_save_name(self):
        return self.__goal_nano_save_name

    def set_on_filename_screen(self, on_filename_screen):
        self.__on_filename_screen = on_filename_screen

    def get_on_filename_screen(self):
        return self.__on_filename_screen

    def set_save_prompt_showing(self, showing):
        self.__save_prompt_showing = showing

    def get_save_prompt_showing(self):
        return self.__save_prompt_showing

    def set_goal_nano_end_content(self, goal_nano_end_content):
        self.__goal_nano_end_content = goal_nano_end_content

    def get_goal_nano_end_content(self):
        return self.__goal_nano_end_content

    def get_last_prompt(self):
        return self.__last_nano_prompt

    def set_last_prompt(self, last_prompt):
        self.__last_nano_prompt = last_prompt

    def get_goal_nano_filepath(self):
        return self.__goal_nano_filepath

    def set_goal_nano_filepath(self, goal_path):
        self.__goal_nano_filepath = goal_path

    # Checks used by the challenges

    def check_nano_content_default(self):
        goal = self.get_goal_nano_end_content()
        content_ok = self.get_nano_content().strip() == goal

        if not self.get_nano_running():
            return self.get_last_nano_filename() == self.get_goal_nano_save_name()

        elif self.get_on_filename_screen() and content_ok:
            if self.get_editable() == self.get_goal_nano_save_name():
                hint = "\n{{gb:Pulsa}} {{ob:Enter}} {{gb:para confirmar el nombre del archivo.}}"
            else:
                hint = "\n{{gb:Escribe}} {{yb:%s}} {{gb:y pulsa}} {{yb:Enter}}" % self.get_goal_nano_save_name()
            self.send_hint(hint)

        elif self.get_on_filename_screen():
            self.send_hint("\n{{ob:Uy, tu texto no es correcto. Pulsa}} {{yb:Ctrl C}} {{ob:para cancelar.}}")

        elif self.get_save_prompt_showing():
            if content_ok:
                hint = "\n{{gb:Pulsa}} {{ob:S}} {{gb:para confirmar que quieres guardar.}}"
            else:
                hint = "\n{{rb:¡Tu texto no es correcto! Pulsa}} {{yb:N}} {{rb:para salir de nano.}}"
            self.send_hint(hint)

        elif content_ok:
            self.send_hint(
                "\n{{gb:¡Excelente, escribiste}} {{yb:%s}}{{gb:! Ahora pulsa}} {{yb:Ctrl X}} "
                "{{gb:para salir.}}" % goal
            )

        return False

    def check_nano_input(self):
        """Check the saved file has the goal contents, after nano was closed."""
        end_path = generate_real_path(self.get_goal_nano_filepath())

        if os.path.exists(end_path):
            with open(end_path, encoding="utf-8") as f:
                text = f.read()

            if text.strip() == self.get_goal_nano_end_content():
                return True
            self.send_hint(
                "\n{{rb:¡Tu texto no es correcto! Escribe}} {{yb:nano %s}} {{rb:para intentarlo de nuevo.}}"
                % self.get_goal_nano_save_name()
            )
            return False

        self.send_hint(
            "\n{{rb:El archivo}} {{lb:%s}} {{rb:no existe. ¿Guardaste bien tu archivo?}}"
            % self.get_goal_nano_filepath()
        )
        return False

    def get_correct_nano_user_cmd(self):
        return "nano {}".format(self.get_goal_nano_save_name())

    def opened_nano(self, line):
        """
        Called when the user has just opened nano. By default, if there is goal
        text to be written, tell the user what to write and how to exit.
        """
        hint = None
        if not line == self.get_goal_nano_save_name():
            hint = "\n{{rb:¡Uy, abriste el archivo equivocado! Pulsa}} {{yb:Ctrl X}} {{rb:para salir.}}"
        elif self.get_goal_nano_end_content():
            hint = (
                "\n{{gb:¡Abriste nano! Ahora asegúrate de que el archivo diga}} {{yb:%s}}"
                "{{gb:. Si quieres salir, pulsa}} {{yb:Ctrl X}}{{gb:.}}"
            ) % self.get_goal_nano_end_content()
        self.send_hint(hint)

    def send_hint(self, string):
        self.__client.send_hint(string)

    # NanoListener: events coming from the editor

    def contents_changed(self, text):
        self.set_nano_content(text)
        self.set_save_prompt_showing(False)
        self.__step.check_nano_contents()

    def prompt_shown(self, prompt, editable=""):
        self.set_last_prompt(prompt)
        self.set_editable(editable)
        if prompt == self.SAVE_FILENAME:
            self.set_save_prompt_showing(False)
            self.set_on_filename_screen(True)
        elif prompt == self.SAVING_NANO_PROMPT:
            self.set_save_prompt_showing(True)
            self.set_on_filename_screen(False)
        self.__step.check_nano_contents()

    def prompt_answered(self, answer):
        if answer == "cancel":
            self.__cancelled_save()
        self.__step.check_nano_contents()

    def file_saved(self, filename):
        self.set_last_nano_filename(filename)
        self.__cancelled_save()

    def nano_closed(self):
        self.quit_nano()

    def __cancelled_save(self):
        self.set_save_prompt_showing(False)
        self.set_on_filename_screen(False)

    def quit_nano(self):
        self.__cancelled_save()
        self.set_nano_running(False)
