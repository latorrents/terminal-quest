# cave.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#


from terminal_quest.common import get_story_file

dark_room = {
    "name": "cuarto-oscuro",
    "challenges": [
        {
            "challenge": 32,
            "step": 1,
            "permissions": 0o300
        },
        {
            "challenge": 35,
            "step": 1,
            "permissions": 0o700
        }
    ],
    "children": [
        {
            "name": "letrero",
            "contents": get_story_file("x-sign")
        }
    ]
}

cage_room = {
    "name": "jaula",
    "challenges": [
        {
            "challenge": 32,
            "step": 1,
            "permissions": 0o500
        },
        {
            "challenge": 35,
            "step": 6,
            "permissions": 0o700
        }
    ],
    "children": [
        {
            "name": "pajaro",
            "contents": get_story_file("pajaro"),
            "challenges": [
                {
                    "challenge": 36,
                    "step": 1,
                    "exists": False
                }
            ]
        },
        {
            "name": "pergamino",
            "contents": get_story_file("scroll-cage"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 36,
                    "step": 1
                }
            ]
        }
    ]
}

locked_room = {
    "name": "cuarto-cerrado",
    "challenges": [
        {
            "challenge": 32,
            "step": 1,
            "permissions": 0o600
        },
        {
            "challenge": 35,
            "step": 4,
            "permissions": 0o700
        }
    ],
    "children": [
        {
            "name": "fuego-artificial",
            "contents": get_story_file("firework-animation")
        },
        {
            "name": "letrero",
            "contents": get_story_file("w-sign"),
            "challenges": [
                {
                    "challenge": 32,
                    "step": 1
                },
                {
                    "challenge": 33,
                    "step": 23
                }
            ]
        },
        {
            "name": "encendedor",
            "contents": get_story_file("encendedor"),
            "challenges": [
                {
                    "challenge": 32,
                    "step": 1
                },
                {
                    "challenge": 36,
                    "step": 4,
                    "permissions": 0o755
                }
            ]
        }
    ]
}

chest = {
    "name": "cofre",
    "children": [
        {
            "name": "acertijo",
            "contents": get_story_file("riddle-cave")
        },
        {
            "name": "respuesta",
            "contents": get_story_file("answer-cave")
        }
    ],
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 37,
            "step": 2,
            "permissions": 0o000
        },
        {
            "challenge": 37,
            "step": 5,
            "permissions": 0o700
        }
    ]
}

cave = {
    "name": "cueva",
    "children": [
        dark_room,
        cage_room,
        locked_room,
        chest,
        {
            "name": "letrero",
            "contents": get_story_file("sign_cave")
        }
    ]
}