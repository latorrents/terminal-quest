# town.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#


from terminal_quest.common import get_story_file
from .hidden_shelter import hidden_shelter
from .east import east


grumpy_man_hurt = {
    "name": "hombre-enojado",
    "contents": get_story_file("hombre-enojado"),
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

grumpy_man_fixed = {
    "name": "hombre-enojado",
    "contents": get_story_file("grumpy-man-fixed"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 46,
            "step": 1
        }
    ]
}

young_girl = {
    "name": "chica",
    "contents": get_story_file("chica"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1
        },
        {
            "challenge": 8,
            "step": 2,
            "exists": False
        },
        {
            "challenge": 46,
            "step": 1
        }
    ]
}

little_boy = {
    "name": "chico",
    "contents": get_story_file("chico"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1
        },
        {
            "challenge": 8,
            "step": 3,
            "exists": False
        },
        {
            "challenge": 46,
            "step": 1
        }
    ]
}

mayor = {
    "name": "Alcalde",
    "contents": get_story_file("Alcalde"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1
        },
        {
            "challenge": 8,
            "step": 6,
            "exists": False
        },
        {
            "challenge": 46,
            "step": 1
        }
    ]
}

note_town = {
    "name": "nota",
    "contents": get_story_file("note_town"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 8,
            "step": 6
        },
        {
            "challenge": 10,
            "step": 1,
            "exists": False
        }
    ]
}

dog_town = {
    "name": "perro",
    "contents": get_story_file("perro"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 11,
            "step": 6
        },
        {
            "challenge": 12,
            "step": 2,
            "exists": False
        },
        {
            "challenge": 46,
            "step": 1
        }
    ]
}

eleanor_town = {
    "name": "Eleanor",
    "contents": get_story_file("Eleanor"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 11,
            "step": 6
        },
        {
            "challenge": 12,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 46,
            "step": 1
        }
    ]
}


clara = {
    "name": "Clara",
    "contents": get_story_file("Clara"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 46,
            "step": 1
        }
    ]
}

bernard = {
    "name": "Bernard",
    "contents": get_story_file("Bernard"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 46,
            "step": 1
        }
    ]
}

rabbit = {
    "name": "Conejo",
    "contents": get_story_file("Conejo"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 46,
            "step": 1
        }
    ]
}


swordmaster = {
    "name": "Espadachin",
    "contents": get_story_file("swordmaster-without-sword"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 46,
            "step": 1
        }
    ]
}

edith = {
    "name": "Edith",
    "contents": get_story_file("Edith"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 46,
            "step": 1
        }
    ]
}


edward = {
    "name": "Edward",
    "contents": get_story_file("Edward"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 46,
            "step": 1
        }
    ]
}

dad = {
    "name": "Papa",
    "contents": get_story_file("Papa"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 46,
            "step": 1
        }
    ]
}


mum = {
    "name": "Mama",
    "contents": get_story_file("Mama"),
    "challenges": [
        {
            "challenge": 0,
            "step": 1,
            "exists": False
        },
        {
            "challenge": 46,
            "step": 1
        }
    ]
}


town = {
    "name": "pueblo",
    "children": [
        hidden_shelter,
        grumpy_man_hurt,
        grumpy_man_fixed,
        young_girl,
        little_boy,
        note_town,
        mayor,
        east,
        dog_town,
        eleanor_town,
        edith,
        edward,
        swordmaster,
        bernard,
        rabbit,
        dad,
        mum
    ]
}
