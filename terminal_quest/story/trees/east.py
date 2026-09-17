# east.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#


from terminal_quest.common import get_story_file
from .shed_shop import shed_shop
from .library import library


restaurant = {
    "name": "restaurante",
    "children": [
        {
            "name": "",
            "children": [
                {
                    "name": ".bodega",
                    "children": [
                        {
                            "name": "Clara",
                            "contents": get_story_file("Clara")
                        },
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
                                    "challenge": 28,
                                    "step": 5
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}

east = {
    "name": "este",
    "children": [
        shed_shop,
        library,
        restaurant
    ],
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 23,
            "step": 1
        }
    ]
}