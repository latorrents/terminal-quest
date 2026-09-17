# CompanionMisc.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

from terminal_quest.step import StepTemplate
from terminal_quest.terminals import TerminalMkdir
from terminal_quest.terminals import TerminalNano

bernard_text = "¡Bernard te impidió mirar dentro del sótano!"


def bernard_autocomplete(completions):
    if "fotocopiadora.sh" in completions:
        print("\n" + bernard_text)
        return []
    else:
        return completions


class TerminalMkdirBernard(TerminalMkdir):
    def _autocomplete_files(self, text, line, begidx, endidx, only_dirs=False, only_exe=False):
        completions = TerminalMkdir._autocomplete_files(self, text, line, begidx, endidx, only_dirs, only_exe)
        return bernard_autocomplete(completions)


class TerminalNanoBernard(TerminalNano):
    def _autocomplete_files(self, text, line, begidx, endidx, only_dirs=False, only_exe=False):
        completions = TerminalNano._autocomplete_files(self, text, line, begidx, endidx, only_dirs, only_exe)
        return bernard_autocomplete(completions)


class StepTemplateEleanorBernard(StepTemplate):
    companion_command = "cat Eleanor"

    def check_command(self, last_user_input):
        spoke = self._companion_speaks(last_user_input)
        if not spoke:
            return self._default_check_command(last_user_input)

    def block_command(self, line):
        if "sotano" in line and ("ls" in line or "cat" in line):
            print(bernard_text)
            return True
        else:
            return StepTemplate.block_command(self, line)


class StepTemplateMkdir(StepTemplateEleanorBernard):
    TerminalClass = TerminalMkdirBernard


class StepTemplateNano(StepTemplateEleanorBernard):
    TerminalClass = TerminalNanoBernard
