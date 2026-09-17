# woods.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from .cave import cave
from .clearing import clearing
from .rabbithole import rabbithole
from terminal_quest.common import get_story_file


thicket = {
    "name": "matorral",
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
    ],
    "children": [
        rabbithole,
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
                    "challenge": 40,
                    "step": 1
                },
                {
                    "challenge": 42,
                    "step": 1,
                    "exists": False
                }
            ]
        },
        {
            "name": "nota",
            "contents": get_story_file("note_rabbithole"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 40,
                    "step": 1
                },
                {
                    "challenge": 42,
                    "step": 1,
                    "exists": False
                }
            ]
        }
    ]
}


woods = {
    "name": "bosque",
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
    ],
    "children": [
        clearing,
        cave,
        thicket,
        {
            "contents": get_story_file("note_woods"),
            "name": "nota",
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 41,
                    "step": 2
                }
            ]
        },
    ]
}