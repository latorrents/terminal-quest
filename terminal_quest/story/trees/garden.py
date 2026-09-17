# garden.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

from terminal_quest.common import get_story_file

greenhouse = {
    "name": "invernadero",
    "children": [
        {
            "name": "zanahorias",
            "contents": get_story_file("zanahorias")
        },
        {
            "name": "calabaza",
            "contents": get_story_file("calabaza")
        },
        {
            "name": "tomate",
            "contents": get_story_file("tomate")
        },
        {
            "name": "cebolla",
            "contents": get_story_file("cebolla")
        },
        {
            "name": "Papa",
            "contents": get_story_file("Papa"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1
                },
                {
                    "challenge": 4,
                    "step": 3,
                    "exists": False
                }
            ]
        },
        {
            "name": "nota",
            "contents": get_story_file("note_greenhouse"),
            "challenges":
                [
                    {
                        "challenge": 4,
                        "step": 3
                    }
                ]
        }
    ]
}
garden = {
    "name": "jardin",
    "children": [
        {
            "name": "banco",
            "contents": get_story_file("banco")
        },
        {
            "name": "flores",
            "contents": get_story_file("flores")
        },
        {
            "name": "cerca",
            "contents": get_story_file("cerca")
        },
        greenhouse
    ]
}