# house.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# Copyright (C) 2026 David Latorre <david@latorredev.com> (adaptación standalone en Python 3)
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from .garden import garden
from .kitchen import kitchen
from .my_room import my_room
from .parents_room import parents_room

my_house = {
    "name": "mi-casa",
    "children": [
        my_room, kitchen, parents_room, garden
    ]
}
