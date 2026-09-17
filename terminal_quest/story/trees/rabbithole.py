# rabbithole.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from terminal_quest.common import get_story_file
from .chest import chest


cage = {
    "name": "jaula",
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 44,
            "step": 5,
            "permissions": 0o500
        },
        {
            "challenge": 45,
            "step": 6,
            "permissions": 0o755
        }
    ],
    "children": [
        {
            "name": "Bernard",
            "contents": get_story_file("Bernard")
        },
        {
            "name": "Edith",
            "contents": get_story_file("Edith")
        },
        {
            "name": "Edward",
            "contents": get_story_file("Edward")
        },
        {
            "name": "perro",
            "contents": get_story_file("perro")
        },
        {
            "name": "Espadachin",
            "contents": get_story_file("swordmaster-without-sword")
        },
        {
            "name": "Papa",
            "contents": get_story_file("Papa")
        },
        {
            "name": "Mama",
            "contents": get_story_file("Mama")
        },
        {
            "name": "hombre-enojado",
            "contents": get_story_file("hombre-enojado")
        },
        {
            "name": "Alcalde",
            "contents": get_story_file("Alcalde")
        },
        {
            "name": "chico",
            "contents": get_story_file("chico")
        },
        {
            "name": "chica",
            "contents": get_story_file("chica")
        }
    ]
}

rabbithole = {
    "name": "madriguera",
    "type": "directory",
    "children": [
        cage,
        chest,
        {
            "name": "Conejo",
            "contents": get_story_file("Conejo"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 44,
                    "step": 5
                }
            ],
        },
        {
            "name": "campana",
            "contents": get_story_file("campana"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 43,
                    "step": 1
                }
            ],
        }
    ],
    "challenges": [
        {
            "challenge": 40,
            "step": 1,
            "permissions": 0o755
        },
        {
            "challenge": 43,
            "step": 1,
            "permissions": 0o000
        },
        {
            "challenge": 44,
            "step": 5,
            "permissions": 0o755
        }
    ]
}
