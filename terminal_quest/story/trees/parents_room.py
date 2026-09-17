# parents_room.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

from terminal_quest.common import get_story_file

safe = {
    "name": ".caja-fuerte",
    "challenges": [
        {
            "challenge": 17,
            "step": 1
        }
    ],
    "children": [
        {
            "name": "diario-de-mama",
            "contents": get_story_file("diario-de-mama"),
        },
        {
            "name": "ECHO",
            "contents": get_story_file("ECHO"),
        },
        {
            "name": "mapa",
            "contents": get_story_file("mapa"),
        }
    ]
}

parents_room = {
    "name": "cuarto-de-papas",
    "children": [
        {
            "name": "cuadro",
            "contents": get_story_file("cuadro")
        },
        {
            "name": "tele",
            "contents": get_story_file("tele")
        },
        {
            "name": "ventana",
            "contents": get_story_file("ventana")
        },
        {
            "name": "cama",
            "contents": get_story_file("bed_parents-room")
        },
        safe
    ]
}