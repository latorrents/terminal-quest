# my_room.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

from terminal_quest.common import get_story_file

shelves = {
    "name": "estantes",
    "children":
        [
            {
                "name": "redwall",
                "contents": get_story_file("redwall")
            },
            {
                "name": "la-colina-de-watership",
                "contents": get_story_file("la-colina-de-watership")
            },
            {
                "name": "alicia-en-el-pais-de-las-maravillas",
                "contents": get_story_file("alicia-en-el-pais-de-las-maravillas")
            },
            {
                "name": "historieta",
                "contents": get_story_file("historieta")
            },
            {
                "name": "nota",
                "contents": get_story_file("note_my-room")
            }
        ]
}

wardrobe = {
    "name": "armario",
    "children": [
        {
            "name": "gorra",
            "contents": get_story_file("gorra")
        },
        {
            "name": "vestido",
            "contents": get_story_file("vestido")
        },
        {
            "name": "sueter",
            "contents": get_story_file("sueter")
        },
        {
            "name": "camisa",
            "contents": get_story_file("camisa")
        },
        {
            "name": "falda",
            "contents": get_story_file("falda")
        },
        {
            "name": "camiseta",
            "contents": get_story_file("camiseta")
        },
        {
            "name": "pantalones",
            "contents": get_story_file("pantalones")
        }
    ]
}

chest = {
    "name": ".cofre",
    "challenges": [
        {
            "challenge": 15,
            "step": 1
        }
    ],
    "children": [
        {
            "name": "CAT",
            "contents": get_story_file("CAT")
        },
        {
            "name": "CD",
            "contents": get_story_file("CD")
        },
        {
            "name": "LS",
            "contents": get_story_file("LS")
        },
        {
            "name": ".nota",
            "contents": get_story_file(".nota")
        }
    ]
}

my_room = {
    "name": "mi-cuarto",
    "children": [
        {
            "name": "despertador",
            "contents": get_story_file("despertador")
        },
        {
            "name": "silla",
            "contents": get_story_file("silla")
        },
        {
            "name": "computadora",
            "contents": get_story_file("computadora")
        },
        {
            "name": "escritorio",
            "contents": get_story_file("escritorio")
        },
        {
            "name": "cama",
            "contents": get_story_file("bed_my-room")
        },
        shelves,
        wardrobe,
        chest
    ]
}