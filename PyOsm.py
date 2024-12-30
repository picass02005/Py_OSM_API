# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

import json
import sys
from typing import Tuple, Iterable
from urllib.parse import quote

import aiohttp

from Cogs.OSM.Py_OSM_API.BoundingBox import OSMBoundingBox
from Cogs.OSM.Py_OSM_API.Note import OSMNote
from User import OSMUser

"""
HOW TO FIND YOUR USER ID
Log in into your OSM account and you will be able to get it on https://api.openstreetmap.org/api/0.6/user/details.json
It should be under {'users': {'id': YOUR_USER_ID}}
"""


class PyOSM:
    def __init__(self):
        self._capabilities = {
            'area': 0,
            'note_area': 0,
            'changesets': {
                'maximum_elements': 0,
                'default_query_limit': 0,
                'maximum_query_limit': 0
            },
            'notes': {
                'default_query_limit': 0,
                'maximum_query_limit': 0,
                'area': 0
            },
            'timeout': 0,
            'status': {
                'database': "offline",
                'api': "offline",
                'gpx': "offline"
            }
        }

    async def update_capabilities(self) -> bool:
        """
        Updates api rates dictionary
        :return: True if it managed to update api rates
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.openstreetmap.org/api/0.6/capabilities.json") as resp:
                if resp.status == 200:
                    data = json.loads(await resp.text())

                    self._capabilities.update({
                        'area': data['api']['area']['maximum'],
                        'note_area': data['api']['note_area']['maximum'],
                        'changesets': data['api']['changesets'],
                        'notes': data['api']['notes'],
                        'timeout': data['api']['timeout']['seconds'],
                        'status': data['api']['status']
                    })

                else:
                    sys.stderr.write(f"WARNING: Couldn't fetch OSM API rates: {resp.status} {await resp.text()}")
                    return False

    @staticmethod
    async def get_uid_with_changeset(display_name: str) -> int:
        """
        Following method is a hack used to get a user UID from one of their changeset
        This doesn't work if someone never made any changeset
        :param display_name: The display name of the user you want to fetch
        :return: If UID is found, return its value; else it will return -1
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://api.openstreetmap.org/api/0.6/changesets.json?limit=1&display_name={quote(display_name)}"
            ) as resp:
                if resp.status == 200:
                    data = json.loads(await resp.text())

                    if len(data['changesets']) == 0:
                        return -1

                    return data['changesets'][0]["uid"]



                else:
                    sys.stderr.write(f"WARNING: Couldn't fetch OSM UID from display_name: {resp.status} "
                                     f"{await resp.text()}")
                    return -1

    @staticmethod
    async def fetch_user_info(uid: int) -> OSMUser | None:
        """
        Fetch a user using its UID
        :param uid: The user's UID
        :return: Inititalized OSMUser if successfull, else None
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.openstreetmap.org/api/0.6/user/{uid}.json") as resp:
                if resp.status == 200:
                    data = json.loads(await resp.text())

                    return OSMUser(data["user"])

                else:
                    sys.stderr.write(f"WARNING: Couldn't fetch user informations: {resp.status} {await resp.text()}")
                    return None

    @staticmethod
    async def fetch_users_info(uid: Iterable[int]) -> Tuple[OSMUser, ...] | None:
        """
        Fetch multiple user using their UID
        :param uid: Every UID we want to get information on
        :return: Inititalized OSMUsers in a tuple if successfull, else None
        """

        uid_str = ','.join([str(i) for i in uid])

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.openstreetmap.org/api/0.6/users.json?users={uid_str}") as resp:
                if resp.status == 200:
                    data = json.loads(await resp.text())

                    return tuple([OSMUser(i["user"]) for i in data["users"]])

                else:
                    sys.stderr.write(f"WARNING: Couldn't fetch user informations: {resp.status} {await resp.text()}")
                    return None

    async def fetch_notes_by_bbox(self, bbox: OSMBoundingBox, limit: int = 100, closed: int = 7) -> Tuple[OSMNote, ...]:
        """
        Fetch notes respecting the following arguments
        :param bbox: Coordinates for the area to retrieve the notes from. Must not be overlaping the date line
        :param limit: Number of entries returned at max
        :param closed: Number of days a note needs to be closed to be excluded (0 means only open notes are returned,
        negative means all notes)
        :return: A tuple of OSM Notes
        """

        # ===== Data check ===== #

        if bbox.cross_date_line():
            raise ValueError("The bounding box crosses date line")

        for i in bbox.get_size():
            if i > self._capabilities['note_area']:
                raise ValueError(f"Bounding box is too big: must be under {self._capabilities['note_area'] * 100} "
                                 f"square degrees")

        if limit > self._capabilities['notes']['maximum_query_limit']:
            raise ValueError(f"Limit is too big: must be under {self._capabilities['notes']['maximum_query_limit']}")

        # ========== #

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://api.openstreetmap.org/api/0.6/notes.json?bbox={bbox}&limit={limit}&closed={closed}"
            ) as resp:
                if resp.status == 200:
                    data = json.loads(await resp.text())

                    if len(data['features']) == 0:
                        return ()

                    return tuple([OSMNote(i) for i in data['features']])



                else:
                    sys.stderr.write(f"WARNING: Couldn't fetch OSM notes: {resp.status} {await resp.text()}")
                    return ()

    @staticmethod
    async def fetch_note_by_id(note_id: int) -> OSMNote | None:
        """
        Fetch a note by its internal id
        :param note_id: The note we want to fetch
        :return: The note object or None if something went wrong
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.openstreetmap.org/api/0.6/notes/{note_id}.json") as resp:
                if resp.status == 200:
                    data = json.loads(await resp.text())

                    return OSMNote(data)


                else:
                    sys.stderr.write(f"WARNING: Couldn't fetch OSM note: {resp.status} {await resp.text()}")
                    return None


async def osm_builder() -> PyOSM:
    pyosm = PyOSM()
    await pyosm.update_capabilities()

    return pyosm


"""async def test():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.openstreetmap.org/api/0.6/changesets?display_name=Chepycou") as response:
            text = await response.text()

    with open("OSMTest.xml", 'w') as f:
        f.write(text)"""

"""
[
/api/0.6/notes/search
]

/api/0.6/changesets
/api/0.6/changeset/#id?include_discussion=true
"""

# TODO: Readme / doc
