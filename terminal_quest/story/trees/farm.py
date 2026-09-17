# farm.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#


from terminal_quest.common import get_story_file

shelter = {
    "name": ".refugio",
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 21,
            "step": 7
        }
    ],
    "children": [
        {
            "name": "Cobweb",
            "contents": get_story_file("Cobweb"),
            "challenges": [
                {
                    "challenge": 21,
                    "step": 10
                }
            ]
        },
        {
            "name": "Trotter",
            "contents": get_story_file("Trotter"),
            "challenges": [
                {
                    "challenge": 21,
                    "step": 10
                }
            ]
        },
        {
            "name": "Daisy",
            "contents": get_story_file("Daisy"),
            "challenges": [
                {
                    "challenge": 21,
                    "step": 10
                }
            ]
        },
        {
            "name": "Ruth",
            "contents": get_story_file("Ruth"),
            "challenges": [
                {
                    "challenge": 21,
                    "step": 10
                }
            ]
        }
    ]
}


farm = {
    "name": "granja",
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 17,
            "step": 1
        }
    ],
    "children": [
        {
            "name": "granero",
            "challenges": [
                {
                    "challenge": 17,
                    "step": 1
                }
            ],
            "children": [
                shelter,
                {
                    "name": "Cobweb",
                    "contents": get_story_file("Cobweb"),
                    "challenges": [
                        {
                            "challenge": 21,
                            "step": 10
                        }
                    ]
                },
                {
                    "name": "Trotter",
                    "contents": get_story_file("Trotter"),
                    "challenges": [
                        {
                            "challenge": 21,
                            "step": 10
                        }
                    ]
                },
                {
                    "name": "Daisy",
                    "contents": get_story_file("Daisy"),
                    "challenges": [
                        {
                            "challenge": 21,
                            "step": 10
                        }
                    ]
                },
                {
                    "name": "Ruth",
                    "contents": get_story_file("Ruth"),
                    "challenges": [
                        {
                            "challenge": 21,
                            "step": 10
                        }
                    ]
                }
            ]
        },
        {
            "name": "casa-de-campo",
            "children": [
                {
                    "name": "cama",
                    "contents": get_story_file("bed_farmhouse")
                }
            ]
        },
        {
            "name": "taller",
            "children": [
                {
                    "name": "MKDIR",
                    "contents": get_story_file("MKDIR")
                },
                {
                    "name": "llave-inglesa",
                    "contents": get_story_file("llave-inglesa")
                },
                {
                    "name": "martillo",
                    "contents": get_story_file("martillo")
                },
                {
                    "name": "serrucho",
                    "contents": get_story_file("serrucho")
                },
                {
                    "name": "cinta-metrica",
                    "contents": get_story_file("cinta-metrica")
                },
                {
                    "name": "iglu",
                    "type": "directory",
                    "challenges": [
                        {
                            "challenge": 0,
                            "step": 1,
                            "exists": False
                        },
                        {
                            "challenge": 20,
                            "step": 5
                        }
                    ]
                }
            ]
        }
    ]
}
