# hidden_shelter.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from terminal_quest.common import get_story_file

eleanor_hidden_shelter = {
    "name": "Eleanor",
    "contents": get_story_file("Eleanor"),
    "challenges": [
        {
            "challenge": 10,
            "step": 1
        },
        {
            "challenge": 11,
            "step": 6,
            "exists": False
        },
        {
            "challenge": 12,
            "step": 1
        },
        {
            "challenge": 23,
            "step": 4,
            "exists": False
        }
    ]
}

dog_hidden_shelter = {
    "name": "perro",
    "contents": get_story_file("perro"),
    "challenges": [
        {
            "challenge": 10,
            "step": 1
        },
        {
            "challenge": 11,
            "step": 6,
            "exists": False
        },
        {
            "challenge": 12,
            "step": 2
        },
        {
            "challenge": 22,
            "step": 2,
            "exists": False
        }
    ]
}


edith_hidden_shelter = {
    "name": "Edith",
    "contents": get_story_file("Edith"),
    "challenges": [
        {
            "challenge": 10,
            "step": 1
        },
        {
            "challenge": 22,
            "step": 4,
            "exists": False
        }
    ]
}


edward_hidden_shelter = {
    "name": "Edward",
    "contents": get_story_file("Edward"),
    "challenges": [
        {
            "challenge": 10,
            "step": 1
        },
        {
            "challenge": 22,
            "step": 4,
            "exists": False
        }
    ]
}


apple_hidden_shelter = {
    "name": "manzana",
    "contents": get_story_file("manzana"),
    "challenges": [
        {
            "challenge": 10,
            "step": 1
        },
        {
            "challenge": 11,
            "step": 5,
            "exists": False
        },
        {
            "challenge": 11,
            "step": 6
        },
        {
            "challenge": 23,
            "step": 1,
            "exists": False
        }
    ]
}


apple_basket = {
    "name": "manzana",
    "contents": get_story_file("manzana"),
    "challenges": [
        {
            "challenge": 11,
            "step": 5,
            "exists": False
        },
        {
            "challenge": 11,
            "step": 6
        },
        {
            "challenge": 23,
            "step": 1,
            "exists": False
        }
    ]
}


kitchen_food_challenges = [
    {
        "challenge": 0,
        "step": 1,
        "exists": False
    },
    {
        "challenge": 14,
        "step": 6
    },
    {
        "challenge": 23,
        "step": 1,
        "exists": False
    }
]


basket_hidden_shelter = {
    "name": "canasta",
    "type": "directory",
    "challenges": [
        {
            "challenge": 10,
            "step": 1
        },
        {
            "challenge": 13,
            "step": 2,
            "exists": False
        },
        {
            "challenge": 14,
            "step": 6
        }
    ],
    "children": [
        apple_basket,
        {
            "name": "banana",
            "contents": get_story_file("banana"),
            "challenges": kitchen_food_challenges
        },
        {
            "name": "pastel",
            "contents": get_story_file("pastel"),
            "challenges": kitchen_food_challenges
        },
        {
            "name": "croissant",
            "contents": get_story_file("croissant"),
            "challenges": kitchen_food_challenges
        }
    ]
}


tiny_chest = {
    "name": ".cofrecito",
    "children": [
        {
            "name": "MV",
            "contents": get_story_file("MV")
        }
    ],
    "challenges": [
        {
            "challenge": 10,
            "step": 1
        }
    ]
}


hidden_shelter = {
    "name": ".refugio-oculto",
    "children": [
        basket_hidden_shelter,
        tiny_chest,
        apple_hidden_shelter,
        dog_hidden_shelter,
        edith_hidden_shelter,
        eleanor_hidden_shelter,
        edward_hidden_shelter
    ],
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 10,
            "step": 1
        }
    ]
}
