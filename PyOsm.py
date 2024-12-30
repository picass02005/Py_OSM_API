# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

import json
import sys
from datetime import datetime
from typing import Tuple, Iterable, Optional, Literal
from urllib.parse import quote

import aiohttp

from .BoundingBox import OSMBoundingBox
from .Enums import OSMSort, OSMOrder
from .Note import OSMNote
from .User import OSMUser

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
                    sys.stderr.write(f"WARNING: Couldn't fetch OSM API rates: {resp.status} {await resp.text()}\n")
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
                                     f"{await resp.text()}\n")
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
                    sys.stderr.write(f"WARNING: Couldn't fetch user informations: {resp.status} {await resp.text()}\n")
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
                    sys.stderr.write(f"WARNING: Couldn't fetch user informations: {resp.status} {await resp.text()}\n")
                    return None

    async def fetch_notes_by_bbox(self, bbox: OSMBoundingBox, limit: int = 100, closed: int = 7) -> Tuple[OSMNote, ...]:
        """
        Fetch notes located in a defined bounding box

        :param bbox: Coordinates for the area to retrieve the notes from. Must not be overlaping the date line
        :param limit: Number of entries returned at max
        :param closed: Number of days a note needs to be closed to be excluded (0 means only open notes are returned, negative means all notes)
        :return: A tuple of OSM Notes

        :except ValueError: Raises this exception if the parameters are invalid (e.g. bounding box crosses date line, is too big or if limit is too high)
        """

        # ===== Parameters checks ===== #

        if bbox.cross_date_line():
            raise ValueError("The bounding box crosses date line")

        if bbox.get_area() > self._capabilities['note_area']:
            raise ValueError(f"Bounding box is too big: must be under {self._capabilities['note_area']} square degrees")

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
                    sys.stderr.write(f"WARNING: Couldn't fetch OSM notes: {resp.status} {await resp.text()}\n")
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
                    sys.stderr.write(f"WARNING: Couldn't fetch OSM note: {resp.status} {await resp.text()}\n")
                    return None

    async def fetch_notes_by_search(
            self,
            limit: int = 100,
            closed: int = 7,
            query: Optional[str] = None,
            user_name: Optional[str] = None,
            user_id: Optional[int] = None,
            bbox: Optional[OSMBoundingBox] = None,
            before: Optional[datetime] = None,
            after: Optional[datetime] = None,
            sort: Optional[Literal[OSMSort.CREATED_AT, OSMSort.UPDATED_AT]] = None,
            order: Optional[Literal[OSMOrder.NEWEST, OSMOrder.OLDEST]] = None
    ) -> Tuple[OSMNote, ...]:
        """
        Fetch all notes matching to defined criteria.
        For more information: https://wiki.openstreetmap.org/wiki/API_v0.6#Search_for_notes:_GET_/api/0.6/notes/search

        :param limit: Maximum number of results. Must be under self._capabilities['notes']['maximum_query_limit']
        :param closed: Maximum number of days a note has been closed for. If 0, return only open notes; if negative, return all notes
        :param query: Text search query, matching either note text or comments
        :param user_name: Search for notes which the given user interacted with
        :param user_id: Same than user_name but with user ID. If both option provided, user_name takes priority
        :param bbox: Coordinates for the area to retrieve the notes from. Must be under self._capability['note_area'] degrees
        :param before: Keep notes where created_at or updated_at (defined in sort) is before this value
        :param after: Keep notes where created_at or updated_at (defined in sort) is after this value
        :param sort: Define what type of values we use for before and after. Valid values are defined in OSMSort
        :param order: Used to sort by newest or oldest. Valid values are defined in OSMOrder

        :return: A tuple containing all notes matching search criterias
        :except ValueError: If any parameters is invalid.
        """

        # ===== Parameters check ===== #

        if not 0 <= limit <= self._capabilities['notes']['maximum_query_limit']:
            raise ValueError(f"Invalid limit: must be a positive below "
                             f"{self._capabilities['notes']['maximum_query_limit']}")

        if bbox is not None:
            if bbox.get_area() > self._capabilities['note_area']:
                raise ValueError(f"Bounding box is too big: must be under {self._capabilities['note_area']} square "
                                 f"degrees")

        if after is not None and before is not None:
            if after > before:
                raise ValueError("Before value is older than after value. You probably swapped them")

        if sort not in OSMSort and sort is not None:
            raise ValueError(f"{sort} is an invalid value for sort parameter. Valid values are defined in OSMSort")

        if order not in OSMOrder and order is not None:
            raise ValueError(f"{order} is an invalid value for order parameter. Valid values are defined in OSMOrder")

        if (before is not None or after is not None) and sort is None:
            ValueError("You must specify sort if before or after is defined")

        # ===== Build URL ===== #

        url = f"https://api.openstreetmap.org/api/0.6/notes/search.json?limit={limit}&closed={quote(str(closed))}"

        if query:
            url += f"&q={quote(query)}"

        if user_name:
            url += f"&display_name={quote(user_name)}"

        if user_id:
            url += f"&user={user_id}"

        if bbox:
            url += f"&bbox={bbox}"

        if before:
            url += f"&to={quote(before.isoformat())}"

        if after:
            url += f"&from={quote(after.isoformat())}"

        if sort:
            url += f"&sort={sort.value if isinstance(sort, OSMSort) else sort}"

        if order:
            url += f"&order={order.value if isinstance(order, OSMOrder) else order}"

        # ========== #

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = json.loads(await resp.text())

                    if len(data['features']) == 0:
                        return ()

                    return tuple([OSMNote(i) for i in data['features']])

                else:
                    sys.stderr.write(f"WARNING: Couldn't fetch OSM notes: {resp.status} {await resp.text()}\n")
                    return ()


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
/api/0.6/changesets
/api/0.6/changeset/#id?include_discussion=true
"""

# TODO: Readme / doc
# TODO: Change self._capabilities to enum
