# chest.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

from terminal_quest.common import get_story_file

chest = {
    "name": "cofre",
    "children": [
        {
            "name": "pergamino",
            "contents": get_story_file("pergamino"),
        },
        {
            "name": "nota-rota",
            "contents": get_story_file("nota-rota")
        }
    ],
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
    ]
}