# default_trees.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from .farm import farm
from terminal_quest.common import get_story_file
from .my_house import my_house
from .woods import woods
from .town import town


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
            "step": 2
        },
        {
            "challenge": 13,
            "step": 5,
            "exists": False
        },
        {
            "challenge": 14,
            "step": 4
        },
        {
            "challenge": 14,
            "step": 5,
            "exists": False
        }
    ],
    "children": [
        {
            "name": "banana",
            "contents": get_story_file("banana"),
            "challenges": [
                {
                    "challenge": 14,
                    "step": 4
                }
            ]
        },
        {
            "name": "pastel",
            "contents": get_story_file("pastel"),
            "challenges": [
                {
                    "challenge": 14,
                    "step": 4
                }
            ]
        },
        {
            "name": "croissant",
            "contents": get_story_file("croissant"),
            "challenges": [
                {
                    "challenge": 14,
                    "step": 4
                }
            ]
        }
    ]
}


tree = {
    "name": "~",
    "children": [
        my_house,
        town,
        woods,
        farm,
        basket
    ]
}




