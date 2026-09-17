# clearing.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from terminal_quest.common import get_story_file

house = {
    "name": "casa",
    "children": [
        {
           "name": "Espadachin",
            "contents": get_story_file("swordmaster"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 32,
                    "step": 1
                },
                {
                    "challenge": 43,
                    "step": 1,
                    "exists": False
                }
            ]
        },
        {
            "name": "nota",
            "contents": get_story_file("note_woods"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 40,
                    "step": 1
                }
            ]
        }
    ],
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 32,
            "step": 1,
            "permissions": 0o000
        },
        {
            "challenge": 33,
            "step": 32,
            "permissions": 0o700,
        }
    ]
}

clearing = {
    "name": "claro",
    "children": [
        house,
        {
            "name": "cartel",
            "contents": get_story_file("cartel")
        }
    ],
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 32,
            "step": 1
        }
    ]
}