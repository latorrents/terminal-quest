# shed-shop.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#


from terminal_quest.common import get_story_file

shed_shop = {
    "name": "tienda-de-cobertizos",
    "children": [
        {
            "name": "Eleanor",
            "contents": get_story_file("Eleanor"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 24,
                    "step": 4
                },
                {
                    "challenge": 26,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 27,
                    "step": 1
                },
                {
                    "challenge": 28,
                    "step": 1,
                    "exists": False
                }
            ]
        },
        {
            "name": "Bernard",
            "contents": get_story_file("Bernard"),
            "challenges": [
                {
                    "challenge": 23,
                    "step": 1
                },
                {
                    "challenge": 30,
                    "step": 1,
                    "exists": False
                }
            ]
        },
        {
            "name": "Sombrero-de-Bernard",
            "contents": get_story_file("bernards-hat"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 30,
                    "step": 1
                }
            ]
        },
        {
            "name": "el-mejor-constructor-de-cobertizos.sh",
            "contents": get_story_file("el-mejor-constructor-de-cobertizos.sh"),
            "challenges": [
                {
                    "challenge": 23,
                    "step": 1,
                    "permissions": 0o755
                }
            ]
        },
        {
            "name": "la-mejor-bocina-del-mundo.sh",
            "contents": get_story_file("best-horn-in-the-world-incorrect.sh"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 23,
                    "step": 1,
                    "permissions": 0o755
                },
                {
                    "challenge": 27,
                    "step": 3,
                    "exists": False
                }
            ]
        },
        {
            "name": "la-mejor-bocina-del-mundo.sh",
            "contents": get_story_file("best-horn-in-the-world-correct.sh"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 27,
                    "step": 3,
                    "permissions": 0o755
                }
            ]
        },
        {
            "name": "sotano",
            "type": "directory",
            "children": [
                {
                    "name": "diario-de-bernard-1",
                    "contents": get_story_file("diario-de-bernard-1"),
                    "challenges": [
                        {
                            "challenge": 23,
                            "step": 1
                        }
                    ]
                },
                {
                    "name": "diario-de-bernard-2",
                    "contents": get_story_file("diario-de-bernard-2"),
                    "challenges": [
                        {
                            "challenge": 23,
                            "step": 1
                        }
                    ]
                },
                {
                    "name": "fotocopiadora.sh",
                    "contents": get_story_file("fotocopiadora.sh"),
                    "permissions": 0o755,
                    "challenges": [
                        {
                            "challenge": 23,
                            "step": 1
                        }
                    ]
                }
            ]
        }
    ]
}
