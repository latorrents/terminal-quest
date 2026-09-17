# controller.py
#
# Lleva al jugador de un paso de la historia al siguiente.
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

import importlib

from terminal_quest.common import tq_file_system
from terminal_quest.file_tree import FileTree
from terminal_quest.progress import save_level
from terminal_quest.story.trees.default_trees import tree


def get_step_class(challenge_number, step_number):
    """Gets the step class for the specified challenge and step."""
    if challenge_number == 0:
        module_name = "terminal_quest.story.challenges.introduction"
        step_class_name = "Step1"
    else:
        module_name = "terminal_quest.story.challenges.challenge_{}".format(challenge_number)
        step_class_name = "Step{}".format(step_number)

    module = importlib.import_module(module_name)
    return getattr(module, step_class_name)


class ChallengeController:

    def __init__(self, ui):
        self.__ui = ui

    def run(self, challenge=1, step=1):
        FileTree(tree, tq_file_system).parse_complete(challenge, step)

        while True:
            step_instance = get_step_class(challenge, step)(self.__ui)
            self.__send_start_challenge_data(step_instance, challenge)
            step_instance.run()
            new_challenge, new_step = step_instance.next()

            if step_instance.is_finished_game():
                save_level(challenge)
                return

            if new_challenge != challenge:
                self.__ui.challenge_completed(challenge)
                if new_challenge > challenge:
                    save_level(challenge)

            challenge, step = new_challenge, new_step

    def __send_start_challenge_data(self, step_instance, challenge_number):
        self.__ui.send_start_challenge_data(
            "\n".join(step_instance.story),
            challenge_number,
            step_instance.TerminalClass.terminal_commands,
            step_instance.highlighted_commands,
            "",
            step_instance.get_print_text()
        )
