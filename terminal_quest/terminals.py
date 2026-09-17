# terminals.py
#
# La terminal con la que juega el jugador. Cada desafío usa una terminal
# que conoce solo los comandos (hechizos) aprendidos hasta ese momento.
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

import getpass
import os
import readline
from cmd import Cmd

from terminal_quest import commands
from terminal_quest.common import fake_home_dir, get_username, SUDO_PASSWORD
from terminal_quest.helpers import get_script_cmd, is_exe, logger
from terminal_quest.location import generate_real_path
from terminal_quest.nano import nano
from terminal_quest.ui import colourize_prompt

# Every command the game knows, to tell the player when they use one too early.
ALL_COMMANDS = ["ls", "cat", "cd", "mv", "echo", "mkdir", "nano", "chmod", "rm", "sudo"]

HELP_WORDS = ["ayuda", "help"]
EXIT_WORDS = ["salir", "exit"]


class GameExit(Exception):
    """Raised when the player wants to leave the game."""


class Terminal(Cmd):
    terminal_commands = []

    def __init__(self, step, location, dirs_to_attempt, client):
        """
        :param step: StepTemplate type
        :param location: PlayerLocation location
        """
        Cmd.__init__(self)
        self.passed = True
        self._step = step
        self.__command_blocked = False
        self._location = location
        self._dirs_to_attempt = dirs_to_attempt
        self._client = client
        self.last_cmd_output = ""

        self._set_prompt()
        self._autocomplete_dash_characters()

    def _set_prompt(self):
        fake_cwd = self._location.get_real_path().replace(fake_home_dir, '~').rstrip('/') or '/'
        dark = getattr(self._client, 'dark', False)
        yellow_part = colourize_prompt(get_username() + "@linux ", 'r' if dark else 'y')
        blue_part = colourize_prompt(fake_cwd + ' $ ', 'r' if dark else 'b')
        self.prompt = yellow_part + blue_part

    def cmdloop(self, intro=None):
        """
        Like Cmd.cmdloop, but Ctrl C doesn't close the game and there are
        commands to ask for help and to exit.
        """
        old_completer = readline.get_completer()
        readline.set_completer(self.complete)
        readline.parse_and_bind("tab: complete")
        try:
            stop = None
            while not stop:
                self._set_prompt()
                try:
                    line = input(self.prompt)
                except KeyboardInterrupt:
                    print("^C")
                    continue
                except EOFError:
                    print("")
                    raise GameExit()

                if self._meta_command(line):
                    continue

                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
        finally:
            readline.set_completer(old_completer)

    def _meta_command(self, line):
        """Commands that are part of the game and not of the story."""
        words = line.split()
        if not words:
            return False
        if words[0] in HELP_WORDS:
            spell = words[1] if len(words) > 1 else None
            self._client.show_spell_help(self.terminal_commands or ["ls"], spell)
            return True
        if words[0] in EXIT_WORDS and len(words) == 1:
            raise GameExit()
        return False

    # Public methods

    def emptyline(self):
        """Do nothing if the user enters an empty line."""
        pass

    def default(self, line):
        command = line.split()[0]
        if command.lower() in ALL_COMMANDS and command != command.lower():
            print("{}: orden no encontrada".format(command))
            self._client.send_hint(
                "\n{{ob:¡Cuidado! ¿Tienes activado el Bloq Mayús?}} {{ob:Los comandos distinguen "
                "mayúsculas de minúsculas: escribe}} {{yb:%s}} {{ob:y no}} {{yb:%s}}{{ob:.}}"
                % (command.lower(), command)
            )
        elif command in ALL_COMMANDS:
            print("{}: orden no encontrada".format(command))
            print("Todavía no has aprendido ese hechizo.")
        else:
            print("{}: orden no encontrada".format(command))

    def precmd(self, line):
        """
        If self._step.block_command returns True, the command is not run.
        """
        line = line.strip()
        self._step.set_last_user_input(line)
        if self._step.block_command(line):
            self._set_command_blocked(True)
            return Cmd.precmd(self, "")
        self._set_command_blocked(False)
        return Cmd.precmd(self, line)

    def onecmd(self, line):
        self.last_cmd_output = ""
        is_script, script = get_script_cmd(line, self._location.get_real_path())
        if is_script:
            commands.run_executable(self._location.get_real_path(), line)
            return None
        if line.startswith("./") or line.startswith("/"):
            self._explain_not_executable(line)
            return None
        self.last_cmd_output = Cmd.onecmd(self, line)
        return self.last_cmd_output

    def _explain_not_executable(self, line):
        path = commands.to_real(self._location.get_real_path(), line.split()[0])
        if os.path.isdir(path):
            print("bash: {}: {}".format(line.split()[0], commands.IS_A_DIRECTORY))
        elif os.path.exists(path):
            print("bash: {}: {}".format(line.split()[0], commands.PERMISSION_DENIED))
        else:
            print("bash: {}: {}".format(line.split()[0], commands.NOT_FOUND))

    def postcmd(self, stop, line):
        return self._step.is_finished_step(line.strip(), self.last_cmd_output)

    def completedefault(self, *ignored):
        text, line, begidx, endidx = ignored
        return self._autocomplete_files(text, line, begidx, endidx, only_exe=True)

    def complete_executable(self, text, line, begidx, endidx):
        return ["./"]

    def completenames(self, text, *ignored):
        return [c + " " for c in self.terminal_commands if c.startswith(text)]

    def complete(self, text, state):
        """Return the next possible completion for 'text'."""
        if state == 0:
            origline = readline.get_line_buffer()
            line = origline.lstrip()
            stripped = len(origline) - len(line)
            begidx = readline.get_begidx() - stripped
            endidx = readline.get_endidx() - stripped
            if begidx > 0:
                cmd, args, foo = self.parseline(line)
                if cmd == '':
                    compfunc = self.completedefault
                else:
                    compfunc = getattr(self, 'complete_' + cmd, self.completedefault)
            elif line.startswith("."):
                compfunc = self.completedefault
            else:
                compfunc = self.completenames
            self.completion_matches = compfunc(text, line, begidx, endidx) or []
        try:
            return self.completion_matches[state]
        except IndexError:
            return None

    def get_command_blocked(self):
        return self.__command_blocked

    # Protected methods

    def _autocomplete_files(self, text, line, begidx, endidx, only_dirs=False, only_exe=False):
        try:
            additional_path = line[:int(begidx)].split(" ")[-1]

            # If we do ls ~/ we need to change the path to be absolute.
            if additional_path.startswith('~'):
                path = additional_path.replace('~', fake_home_dir, 1)
            else:
                path = os.path.join(self._location.get_real_path(), additional_path)

            if not os.path.isdir(path):
                return []

            contents = sorted(os.listdir(path))
            if text == "..":
                completions = [text]
            elif only_dirs:
                completions = [f for f in contents
                               if f.startswith(text) and os.path.isdir(os.path.join(path, f))]
            elif only_exe:
                completions = [f for f in contents
                               if f.startswith(text) and (os.path.isdir(os.path.join(path, f)) or
                                                          is_exe(os.path.join(path, f)))]
            else:
                completions = [f for f in contents if f.startswith(text)]

            if not text.startswith("."):
                completions = [f for f in completions if not f.startswith(".")] or completions

            if len(completions) == 1:
                if os.path.isdir(os.path.join(path, completions[0])):
                    completions = [completions[0] + '/']
                else:
                    completions = [completions[0] + ' ']

            return completions

        except Exception as e:
            logger.debug("Hit Exception in the autocomplete_files function {}".format(e))
            return []

    def _get_real_path(self):
        return self._location.get_real_path()

    def _set_command_blocked(self, blocked):
        self._step.set_command_blocked(blocked)
        self.__command_blocked = blocked

    def _autocomplete_dash_characters(self):
        # So we can autocomplete names with the - character
        readline.set_completer_delims(' \t\n"\'')


class TerminalLs(Terminal):
    terminal_commands = ["ls"]

    def do_ls(self, line):
        return commands.ls(self._location.get_real_path(), line)

    def complete_ls(self, text, line, begidx, endidx):
        return self._autocomplete_files(text, line, begidx, endidx)


class TerminalCat(TerminalLs):
    terminal_commands = ["ls", "cat"]

    def do_cat(self, line):
        commands.cat(self._get_real_path(), line)

    def complete_cat(self, text, line, begidx, endidx):
        return self._autocomplete_files(text, line, begidx, endidx)


class TerminalCd(TerminalCat):
    terminal_commands = ["ls", "cat", "cd"]

    def do_cd(self, line):
        if self.__check_cd(line):
            self._set_command_blocked(False)
            new_path = commands.cd(self._location.get_real_path(), line)
            if new_path and not os.access(new_path, os.X_OK):
                self._set_command_blocked(True)
                print("bash: cd: " + line + ": " + commands.PERMISSION_DENIED)
            elif new_path:
                self._location.set_real_path(new_path)
                self._set_prompt()
        else:
            self._set_command_blocked(True)
            print("¡Buen intento! Pero ese no es el camino que buscas.")

    def complete_cd(self, text, line, begidx, endidx):
        return self._autocomplete_files(text, line, begidx, endidx, only_dirs=True)

    def __check_cd(self, line):
        """
        Returns True if cd brings the user closer to their destination,
        so cd is allowed to run with the user's choice of path.
        """
        from terminal_quest.step_helpers import route_between_paths

        route = route_between_paths(self._location.get_fake_path(), self._location.get_end_dir())

        if not route and self._dirs_to_attempt:
            route = route_between_paths(self._location.get_fake_path(), self._dirs_to_attempt)

        line = line.strip()
        if line:
            if line.startswith("~"):
                new_path = line
            else:
                new_path = os.path.join(self._location.get_fake_path(), line)
        else:
            # If the user didn't enter a path, assume they want to go home
            new_path = '~'

        new_path = os.path.abspath(os.path.expanduser(new_path))
        return new_path in route


class TerminalMv(TerminalCd):
    terminal_commands = ["ls", "cat", "cd", "mv"]

    def do_mv(self, line):
        commands.mv(self._location.get_real_path(), line)

    def complete_mv(self, text, line, begidx, endidx):
        return self._autocomplete_files(text, line, begidx, endidx)


class TerminalEcho(TerminalMv):
    terminal_commands = ["ls", "cat", "cd", "mv", "echo"]

    def do_echo(self, line):
        commands.echo(self._location.get_real_path(), line)


class TerminalMkdir(TerminalEcho):
    terminal_commands = ["ls", "cat", "cd", "mv", "echo", "mkdir"]

    def do_mkdir(self, line):
        commands.mkdir(self._location.get_real_path(), line)


class TerminalNano(TerminalMkdir):
    terminal_commands = ["ls", "cat", "cd", "mv", "echo", "mkdir", "nano"]

    def __init__(self, step, location, dirs_to_attempt, client):
        self._step_nano = step.get_nano_logic()
        TerminalMkdir.__init__(self, step, location, dirs_to_attempt, client)

    def do_nano(self, line):
        self._step_nano.set_nano_running(True)
        self._step_nano.opened_nano(line.strip())
        self._step_nano.set_nano_content(self.read_goal_contents())
        commands.sounds_manager.on_command_run(['nano'] + line.split())

        nano(self._location.get_real_path(), line, self._step_nano, self._client)
        self._step_nano.quit_nano()

    def complete_nano(self, text, line, begidx, endidx):
        return self._autocomplete_files(text, line, begidx, endidx)

    def read_goal_contents(self):
        end_path = generate_real_path(self._step_nano.get_goal_nano_filepath())
        if self._step_nano.get_goal_nano_filepath() and os.path.isfile(end_path):
            with open(end_path, encoding="utf-8", errors="replace") as f:
                return f.read()
        return ""


class TerminalChmod(TerminalNano):
    terminal_commands = ["ls", "cat", "cd", "mv", "echo", "mkdir", "nano", "chmod"]

    def do_chmod(self, line):
        commands.chmod(self._location.get_real_path(), line)

    def complete_chmod(self, text, line, begidx, endidx):
        return self._autocomplete_files(text, line, begidx, endidx)


class TerminalRm(TerminalChmod):
    terminal_commands = ["ls", "cat", "cd", "mv", "echo", "mkdir", "nano", "chmod", "rm"]

    def do_rm(self, line):
        commands.rm(self._location.get_real_path(), line)

    def complete_rm(self, text, line, begidx, endidx):
        return self._autocomplete_files(text, line, begidx, endidx)


class TerminalSudo(TerminalRm):
    terminal_commands = ["ls", "cat", "cd", "mv", "echo", "mkdir", "nano", "chmod", "rm", "sudo"]

    def do_sudo(self, line):
        command = line.split(" ")[0]
        following_line = " ".join(line.split(" ")[1:])

        if command in self.terminal_commands and command != "sudo":
            def success_cb(*cb_args):
                return getattr(self, 'do_{}'.format(command))(*cb_args)
        else:
            def success_cb(*cb_args):
                print("sudo: " + command + ": orden no encontrada")

        return self.__sudo(success_cb, following_line)

    def complete_sudo(self, text, line, begidx, endidx):
        return self._autocomplete_files(text, line, begidx, endidx)

    def __sudo(self, success_cb, *cb_args):
        self._client.send_hint("\n{{gb:Escribe la contraseña. No podrás ver lo que escribes.}}")
        for attempt in range(3):
            try:
                password = getpass.getpass('[sudo] contraseña para {}: '.format(get_username()))
            except (KeyboardInterrupt, EOFError):
                print("")
                self.passed = False
                return

            if password == SUDO_PASSWORD:
                self.passed = True
                return success_cb(*cb_args)

            print("Lo siento, vuelve a intentarlo.")
            if password == "" and attempt < 2:
                self._client.send_hint("\n{{rb:¡No escribiste nada! Tienes que escribir una contraseña.}}")

        self.passed = False
        print("sudo: 3 intentos de contraseña incorrectos")
