# menu.py
#
# El menú inicial: continuar, empezar de nuevo o elegir un capítulo.
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

from terminal_quest import titles
from terminal_quest.common import MAX_CHALLENGE
from terminal_quest.progress import get_level

LOGO = r"""
 _____                   _             _    ___                  _   
|_   _|__ _ __ _ __ ___ (_)_ __   __ _| |  / _ \ _   _  ___  ___| |_ 
  | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | | | | | | | | |/ _ \/ __| __|
  | |  __/ |  | | | | | | | | | | (_| | | | |_| | |_| |  __/\__ \ |_ 
  |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|_|  \__\_\\__,_|\___||___/\__|
"""


def last_unlocked_challenge():
    return min(get_level() + 1, MAX_CHALLENGE)


def ask(ui, question, valid):
    while True:
        try:
            answer = input(question).strip().lower()
        except KeyboardInterrupt:
            print("")
            continue
        if answer in valid:
            return answer
        ui.print_text("{{rb:Escribe una de estas opciones:}} " + ", ".join("{{yb:%s}}" % v for v in valid))


def challenge_title(number):
    return titles.challenges.get(number, {}).get('title', '')


def show(ui):
    """
    Returns:
        int: the challenge to start from, or None to exit.
    """
    ui.clear()
    ui.print_art(LOGO, colour='g')
    ui.print_text("{{yb:        Una aventura para aprender a usar la terminal de Linux}}\n")

    level = get_level()
    if level == 0:
        ui.print_text("  {{yb:1}}  Empezar la aventura")
        ui.print_text("  {{yb:2}}  Salir\n")
        answer = ask(ui, "¿Qué quieres hacer? ", ["1", "2"])
        return 0 if answer == "1" else None

    if level >= MAX_CHALLENGE:
        ui.print_text("  {{gb:¡Ya terminaste Terminal Quest! Puedes volver a jugar cualquier desafío.}}\n")
        next_challenge = None
    else:
        next_challenge = last_unlocked_challenge()
        ui.print_text("  {{yb:1}}  Continuar: desafío %d, %s" % (next_challenge, challenge_title(next_challenge)))
    ui.print_text("  {{yb:2}}  Elegir un capítulo")
    ui.print_text("  {{yb:3}}  Empezar desde el principio")
    ui.print_text("  {{yb:4}}  Salir\n")

    options = ["1", "2", "3", "4"] if next_challenge else ["2", "3", "4"]
    answer = ask(ui, "¿Qué quieres hacer? ", options)
    if answer == "1":
        return next_challenge
    if answer == "2":
        return choose_challenge(ui)
    if answer == "3":
        return 0
    return None


def choose_challenge(ui):
    unlocked = last_unlocked_challenge()

    ui.print_text("\n{{lb:CAPÍTULOS}}")
    available = []
    for number, chapter in sorted(titles.chapters.items()):
        if chapter['start_challenge'] <= unlocked:
            available.append(str(number))
            ui.print_text("  {{yb:%d}}  %s" % (number, chapter['title']))
        else:
            ui.print_text("  {{wn:%d  %s (bloqueado)}}" % (number, chapter['title']))
    chapter = titles.chapters[int(ask(ui, "\nElige un capítulo: ", available))]

    ui.print_text("\n{{lb:DESAFÍOS}}")
    available = []
    for number in range(chapter['start_challenge'], chapter['end_challenge'] + 1):
        if number <= unlocked:
            available.append(str(number))
            ui.print_text("  {{yb:%2d}}  %s" % (number, challenge_title(number)))
        else:
            ui.print_text("  {{wn:%2d  %s (bloqueado)}}" % (number, challenge_title(number)))
    return int(ask(ui, "\nElige un desafío: ", available))
