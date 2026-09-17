# library.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2

from terminal_quest.common import get_story_file


library = {
    "name": "biblioteca",
    "children": [
        {
            "name": "Conejo",
            "type": "file",
            "contents": get_story_file("Conejo"),
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "exists": False
                },
                {
                    "challenge": 42,
                    "step": 1,
                },
                {
                    "challenge": 42,
                    "step": 4,
                    "exists": False
                }
            ]
        },
        {
            "name": "seccion-privada",
            "type": "directory",
            "challenges": [
                {
                    "challenge": 0,
                    "step": 1,
                    "permissions": 0o000
                },
                {
                    "challenge": 42,
                    "step": 3,
                    "permissions": 0o755
                }
            ],
            "children": [
                {
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
                            "challenge": 42,
                            "step": 3
                        },
                        {
                            "challenge": 42,
                            "step": 6,
                            "exists": False
                        }
                    ]
                },
                {
                    "name": "Conejo",
                    "type": "file",
                    "contents": get_story_file("Conejo"),
                    "challenges": [
                        {
                            "challenge": 0,
                            "step": 1,
                            "exists": False
                        },
                        {
                            "challenge": 42,
                            "step": 4
                        },
                        {
                            "challenge": 42,
                            "step": 6,
                            "exists": False
                        }
                    ]
                },
                {
                    "name": "nota",
                    "contents": get_story_file("note_private-section"),
                    "challenges": [
                        {
                            "challenge": 0,
                            "step": 1,
                            "exists": False
                        },
                        {
                            "challenge": 42,
                            "step": 7
                        },
                        {
                            "challenge": 43,
                            "step": 5
                        }
                    ]
                },
                {
                    "name": "espada",
                    "contents": get_story_file("RM-sword"),
                    "challenges": [
                        {
                            "challenge": 0,
                            "step": 1,
                            "exists": False
                        },
                        {
                            "challenge": 43,
                            "step": 2
                        }
                    ]
                }
            ]
        },
        {
            "name": "seccion-publica",
            "children": [
                {
                    "name": "NANO",
                    "contents": get_story_file("NANO")
                }
            ]
        }
    ]
}