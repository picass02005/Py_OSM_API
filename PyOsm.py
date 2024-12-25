# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

import json
import sys
from typing import Tuple, Iterable
from urllib.parse import quote

import aiohttp

from User import OSMUser

"""
HOW TO FIND YOUR USER ID
Log in into your OSM account and you will be able to get it on https://api.openstreetmap.org/api/0.6/user/details.json
It should be under {'users': {'id': YOUR_USER_ID}}
"""


class PyOSM:
    def __init__(self):
        self._ApiRates = {
            'changesets': {
                'maximum_elements': 0,
                'default_query_limit': 0,
                'maximum_query_limit': 0
            },
            'notes': {
                'default_query_limit': 0,
                'maximum_query_limit': 0
            },
            'timeout': 0
        }

    async def update_api_rates(self) -> bool:
        """
        Updates api rates dictionary
        :return: True if it managed to update api rates
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.openstreetmap.org/api/0.6/capabilities.json") as resp:
                if resp.status == 200:
                    data = json.loads(await resp.text())

                    self._ApiRates.update({
                        'changesets': data['api']['changesets'],
                        'notes': data['api']['notes'],
                        'timeout': data['api']['timeout']['seconds']
                    })

                else:
                    sys.stderr.write("WARNING: Couldn't fetch OSM API rates")
                    return False

    @staticmethod
    async def get_uid_with_changeset(display_name: str) -> int:
        """
        This method will fetch a user's changeset and extract its UID from there
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
                    sys.stderr.write("WARNING: Couldn't fetch OSM UID from display_name")
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
                    sys.stderr.write("WARNING: Couldn't fetch user informations")
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
                    sys.stderr.write("WARNING: Couldn't fetch user informations")
                    return None



async def make_py_osm() -> PyOSM:
    pyosm = PyOSM()
    await pyosm.update_api_rates()

    return pyosm


"""async def test():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.openstreetmap.org/api/0.6/changesets?display_name=Chepycou") as response:
            text = await response.text()

    with open("OSMTest.xml", 'w') as f:
        f.write(text)"""

"""
[
/api/0.6/notes
/api/0.6/notes/#id
/api/0.6/notes/search
]

/api/0.6/changesets
/api/0.6/changeset/#id?include_discussion=true
"""
