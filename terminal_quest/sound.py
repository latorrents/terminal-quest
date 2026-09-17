# sound.py
#
# Sonidos del juego. Son opcionales: si el sistema no tiene un reproductor
# (paplay, aplay, pw-play o afplay) el juego sigue funcionando en silencio.
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

import os
import shutil
import subprocess

from terminal_quest.common import sounds_dir
from terminal_quest.helpers import logger

PLAYERS = ['paplay', 'pw-play', 'aplay', 'afplay']

# Story code refers to some sounds by their Spanish name.
SOUND_ALIASES = {
    'despertador': 'alarm',
    'campana': 'bell',
    'perro': 'dog',
    'pasos': 'steps',
}


class SoundManager:
    """
    Plays sounds for the commands being run and for the story text being typed.

    The dicts below map a file name in the game world to a sound name.
    """

    enabled = os.environ.get('TQ_SIN_SONIDO') is None
    _player = None

    # for `cat <object>`
    cat_object_sound = {
        'Daisy': 'bull',
        'Cobweb': 'cobweb',
        'perro': 'dog',
        'periodico': 'paper',
        'historieta': 'paper',
        'nota': 'paper',
        '.nota': 'paper',
        'LS': 'paper',
        'CAT': 'paper',
        'CD': 'paper',
        'MV': 'paper',
        'ECHO': 'paper',
        'MKDIR': 'paper',
        'NANO': 'paper',
        'fotocopiadora.sh': 'paper',
        'la-mejor-bocina-del-mundo.sh': 'paper',
        'el-mejor-constructor-de-cobertizos.sh': 'paper',
        'diario-de-bernard-1': 'paper',
        'diario-de-bernard-2': 'paper',
        'diario-de-mama': 'paper',
        'alicia-en-el-pais-de-las-maravillas': 'paper',
        'la-colina-de-watership': 'paper',
        'redwall': 'paper',
        'mapa': 'paper',
        'Trotter': 'trotter'
    }

    # for `mv <object>`
    mv_object_sound = {
        'Daisy': 'bull',
        'perro': 'dog',
        'Cobweb': 'cobweb',
        'Trotter': 'trotter'
    }

    # for `./<script>`
    script_object_sound = {
        'la-mejor-bocina-del-mundo.sh': 'horn',
        'el-mejor-constructor-de-cobertizos.sh': 'mkdir'
    }

    # for story text
    story_text_sound = {
        'Nuevo Poder': 'new_command',
        'Ding. Dong.': 'bell'
    }

    def on_command_run(self, command_args):
        """
        Play the appropriate sound for a command and its arguments,
        e.g. ['cat', 'perro'] or ['./la-mejor-bocina-del-mundo.sh'].
        """
        if not command_args:
            return

        command = command_args[0]
        last_name = command_args[-1].rstrip('/').rsplit('/', 1)[-1]

        if command == 'cat':
            self._play_from(self.cat_object_sound, last_name, background=False)
        elif command == 'mv' and len(command_args) > 1:
            first_name = command_args[1].rstrip('/').rsplit('/', 1)[-1]
            self._play_from(self.mv_object_sound, first_name, background=False)
        elif command == 'mkdir':
            self.play_sound('mkdir')
        elif command == 'nano':
            self.play_sound('paper')
        elif command.endswith('.sh'):
            self._play_from(self.script_object_sound, command.rsplit('/', 1)[-1], background=False)

    def on_typing_story_text(self, story_text):
        """Play the sound for the key words at the beginning of story_text."""
        for key_words, sound_name in self.story_text_sound.items():
            if story_text.startswith(key_words):
                self.play_sound(sound_name)
                break

    def play_sound(self, sound_name, background=True):
        if not SoundManager.enabled:
            return

        sound_name = SOUND_ALIASES.get(sound_name, sound_name)
        sound_path = os.path.join(sounds_dir, sound_name + '.wav')
        player = self._get_player()
        if not player or not os.path.exists(sound_path):
            return

        try:
            process = subprocess.Popen(
                [player, sound_path],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            if not background:
                process.wait(timeout=5)
        except Exception as e:
            logger.debug('Could not play sound {}: {}'.format(sound_name, e))

    def _play_from(self, sounds, name, background):
        if name in sounds:
            self.play_sound(sounds[name], background=background)

    @staticmethod
    def _get_player():
        if SoundManager._player is None:
            SoundManager._player = next((p for p in PLAYERS if shutil.which(p)), '')
        return SoundManager._player
