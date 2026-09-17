# kitchen.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#


from terminal_quest.common import get_story_file


basket = {
    "name": "canasta",
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 13,
            "step": 5
        },
        {
            "challenge": 14,
            "step": 4,
            "exists": False
        }
    ],
    "children": [
        {
            "name": "botella-vacia",
            "contents": get_story_file("botella-vacia")
        }
    ]
}

kitchen = {
    "name": "cocina",
    "children": [
        basket,
        {
            "name": "banana",
            "contents": get_story_file("banana"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1
                },
                {
                    "challenge": 14,
                    "step": 3,
                    "exists": False
                }
            ]
        },
        {
            "name": "pastel",
            "contents": get_story_file("pastel"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                },
                {
                    "challenge": 14,
                    "step": 3,
                    "exists": False
                }
            ]
        },
        {
            "name": "croissant",
            "contents": get_story_file("croissant"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1
                },
                {
                    "challenge": 14,
                    "step": 3,
                    "exists": False
                }
            ]
        },
        {
            "name": "uvas",
            "contents": get_story_file("uvas")
        },
        {
            "name": "leche",
            "contents": get_story_file("leche")
        },
        {
            "name": "tarta",
            "contents": get_story_file("tarta")
        },
        {
            "name": "sandwich",
            "contents": get_story_file("sandwich")
        },
        {
            "name": "periodico",
            "contents": get_story_file("periodico")
        },
        {
            "name": "horno",
            "contents": get_story_file("horno")
        },
        {
            "name": "mesa",
            "contents": get_story_file("mesa")
        },
        {
            "name": "nota",
            "contents": get_story_file("note_kitchen"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 8,
                    "step": 1
                },
                {
                    "challenge": 10,
                    "step": 1
                }
            ]
        },
        {
            "name": "Mama",
            "contents": get_story_file("Mama"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1
                },
                {
                    "challenge": 8,
                    "step": 1,
                    "exists": False
                }
            ]
        }

    ]
}