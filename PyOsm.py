# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

import json
import sys
from typing import Tuple, Iterable, Optional, Literal
from urllib.parse import quote

import aiohttp

from .Capabilities import OSMCapabilities
from .Enums import OSMOrder
from .Enums import OSMSort
from .Enums import OSMStatus
from .Objects import OSMBoundingBox
from .Objects import OSMChangeset
from .Objects import OSMNote
from .Objects import OSMTimeDelta
from .Objects import OSMUser

"""
HOW TO FIND YOUR USER ID
Log in into your OSM account and you will be able to get it on https://api.openstreetmap.org/api/0.6/user/details.json
It should be under {'user': {'id': YOUR_USER_ID}}
"""


class PyOSM:
    def __init__(self):
        self.capabilities: OSMCapabilities = OSMCapabilities()

    async def update_capabilities(self) -> bool:
        """
        Updates api rates dictionary

        :return: True if it managed to update api rates
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.openstreetmap.org/api/0.6/capabilities.json") as resp:
                if resp.status == 200:
                    data = json.loads(await resp.text())

                    self.capabilities.update_from_api(data)

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

        if not bbox.check_data():
            raise ValueError("Bounding box invalid: for more information, check Documentation/OSMBoundingBox.md")

        if bbox.cross_date_line():
            raise ValueError("The bounding box crosses date line")

        if bbox.get_area() > self.capabilities.notes.area:
            raise ValueError(f"Bounding box is too big: must be under {self.capabilities.notes.area} square degrees")

        if limit > self.capabilities.notes.maximum_query_limit:
            raise ValueError(f"Limit is too big: must be under {self.capabilities.notes.maximum_query_limit}")

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
            during: Optional[OSMTimeDelta] = None,
            sort: Optional[Literal[OSMSort.CREATED_AT, OSMSort.UPDATED_AT]] = None,
            order: Optional[Literal[OSMOrder.NEWEST, OSMOrder.OLDEST]] = None
    ) -> Tuple[OSMNote, ...]:
        """
        Fetch all notes matching to defined criteria.
        For more information: https://wiki.openstreetmap.org/wiki/API_v0.6#Search_for_notes:_GET_/api/0.6/notes/search

        :param limit: Maximum number of results. Must be under self.capabilities.notes.maximum_query_limit
        :param closed: Maximum number of days a note has been closed for. If 0, return only open notes; if negative, return all notes
        :param query: Text search query, matching either note text or comments
        :param user_name: Search for notes which the given user interacted with
        :param user_id: Same than user_name but with user ID. If both option provided, user_name takes priority
        :param bbox: Coordinates for the area to retrieve the notes from. Must be under self._capability['note_area'] degrees
        :param during: Keep only notes which were created at or updated at (defined in sort) in this timedelta. Before value is optional
        :param sort: Define what type of values we use for during. Valid values are defined in OSMSort
        :param order: Used to sort by newest or oldest. Valid values are defined in OSMOrder

        :return: A tuple containing all notes matching search criterias
        :except ValueError: If any parameters is invalid.
        """

        # ===== Parameters check ===== #

        if not 0 <= limit <= self.capabilities.notes.maximum_query_limit:
            raise ValueError(f"Invalid limit: must be a positive below {self.capabilities.notes.maximum_query_limit}")

        if bbox is not None:
            if not bbox.check_data():
                raise ValueError("Bounding box invalid: for more information, check Documentation/OSMBoundingBox.md")

            if bbox.get_area() > self.capabilities.notes.area:
                raise ValueError(f"Bounding box must be under {self.capabilities.notes.area} square degrees")

        if during is not None:
            if not during.check_data_validity(optional_after=False):
                raise ValueError("Before value is older than after value or you forgot to set after value")

        if sort not in OSMSort and sort is not None:
            raise ValueError(f"{sort} is an invalid value for sort parameter. Valid values are defined in OSMSort")

        if order not in OSMOrder and order is not None:
            raise ValueError(f"{order} is an invalid value for order parameter. Valid values are defined in OSMOrder")

        if during is not None and sort is None:
            ValueError("You must specify sort if during is defined")

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

        if during is not None:
            if during.before is not None:
                url += f"&to={quote(during.before.isoformat())}"

            if during.after is not None:
                url += f"&from={quote(during.after.isoformat())}"

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

    async def fetch_changesets_by_search(
            self,
            limit: int = 100,
            user_name: Optional[str] = None,
            user_id: Optional[int] = None,
            bbox: Optional[OSMBoundingBox] = None,
            created_timedelta: Optional[OSMTimeDelta] = None,
            closed_timedelta: Optional[OSMTimeDelta] = None,
            by_ids: Optional[Iterable[int]] = None,
            status: Literal[OSMStatus.OPEN, OSMStatus.CLOSED, OSMStatus.OPEN_AND_CLOSED] = OSMStatus.OPEN_AND_CLOSED,
            order: Optional[Literal[OSMOrder.NEWEST, OSMOrder.OLDEST]] = None
    ) -> Tuple[OSMChangeset, ...]:

        """
        Fetch all changesets matching to defined criteria.
        For more information: https://wiki.openstreetmap.org/wiki/API_v0.6#Query:_GET_/api/0.6/changesets
        Note: this method doesn't return comments, please use self.fetch_changesets_by_id for this purpose

        :param limit: Maximum number of results. Must be under self.capabilities.changesets.maximum_query_limit
        :param user_name: Search for notes which the given user interacted with
        :param user_id: Same than user_name but with user ID. If both option provided, user_name takes priority
        :param bbox: Changesets must be within this bounding box to be returned
        :param created_timedelta: Return changesets created during this timedelta. Note: You can set only before or before AND after but can't just set after
        :param closed_timedelta: Return changesets created during this timedelta. Note: You can set only before or before AND after but can't just set after
        :param by_ids: Return only changesets with those ID
        :param status: Decides if you want to get only open or closed changesets. Default value is both of them
        :param order: Define in which order to return changesets

        :return: Tuple containing all changesets validating those conditions
        :except ValueError: If any parameter have invalid values. Please refer to the attached message
        """

        # ===== Parameters check =====

        if not 0 <= limit <= self.capabilities.changesets.maximum_query_limit:
            raise ValueError(
                f"Invalid limit: must be a positive below {self.capabilities.changesets.maximum_query_limit}"
            )

        if user_name is not None and user_id is not None:
            raise ValueError("You can only specify a user name or a user ID, but not both")

        if bbox is not None:
            if not bbox.check_data():
                raise ValueError("Bounding box invalid: for more information, check Documentation/OSMBoundingBox.md")

        if created_timedelta is not None:
            if created_timedelta.before is None:
                raise ValueError("You never defined a before datetime for created_timedelta")

            if not created_timedelta.check_data_validity(optional_before=False):
                raise ValueError(f"Created_timedelta is invalid: before datetime is older than after datetime")

        if closed_timedelta is not None:
            if closed_timedelta.before is None:
                raise ValueError("You never defined a before datetime for closed_timedelta")

            if not closed_timedelta.check_data_validity(optional_before=False):
                raise ValueError(f"Closed_timedelta is invalid: before datetime is older than after datetime")

        if status not in OSMStatus:
            raise ValueError(f"{status} is an invalid value for sort parameter. Valid values are defined in OSMStatus")

        if order not in OSMOrder and order is not None:
            raise ValueError(f"{order} is an invalid value for sort parameter. Valid values are defined in OSMOrder")

        # ===== Build URL =====

        url = f"https://api.openstreetmap.org/api/0.6/changesets.json?limit={limit}"

        if user_name:
            url += f"&display_name={quote(user_name)}"

        if user_id:
            url += f"&user={user_id}"

        if bbox is not None:
            url += f"&bbox={bbox}"

        if created_timedelta is not None:
            url += f"&from={created_timedelta.before.isoformat()}"

            if created_timedelta.after is not None:
                url += f"&to={created_timedelta.after.isoformat()}"

        if closed_timedelta is not None:
            url += f"&time={created_timedelta.before.isoformat()}"

            if closed_timedelta.after is not None:
                url += f",{created_timedelta.after.isoformat()}"

        if by_ids is not None:
            url += f"&changesets={','.join([str(i) for i in by_ids])}"

        match status:
            case OSMStatus.OPEN | "o" | "open":
                url += "&open=true"
            case OSMStatus.CLOSED | "c" | "closed":
                url += "&closed=true"

            # Do nothing if status is open and closed

        if order is not None:
            url += f"&order={order.value if isinstance(order, OSMOrder) else order}"

        # ========== #

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = json.loads(await resp.text())

                    if len(data['changesets']) == 0:
                        return ()

                    return tuple([OSMChangeset(i) for i in data['changesets']])

                else:
                    sys.stderr.write(f"WARNING: Couldn't fetch OSM changesets: {resp.status} {await resp.text()}\n")
                    return ()

    @staticmethod
    async def fetch_changesets_by_id(changeset_id: int, include_discussion: bool = False) -> OSMChangeset | None:
        """
        Fetch a changeset by its ID
        :param changeset_id: The changeset ID to fetch from
        :param include_discussion: If set to True, will also fetch this changeset comments
        :return: The fetched changeset, or None if any issue happened
        """

        url = f"https://api.openstreetmap.org/api/0.6/changeset/{changeset_id}.json"

        if include_discussion:
            url += "?include_discussion=true"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = json.loads(await resp.text())

                    if len(data['changeset']) == 0:
                        sys.stderr.write(f"WARNING: Couldn't fetch OSM changesets: data invalid\n")
                        return None

                    return OSMChangeset(data['changeset'])

                else:
                    sys.stderr.write(f"WARNING: Couldn't fetch OSM changesets: {resp.status} {await resp.text()}\n")
                    return None



async def py_osm_builder() -> PyOSM:
    pyosm = PyOSM()
    await pyosm.update_capabilities()

    return pyosm
