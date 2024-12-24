import json
import sys
from urllib.parse import quote

import aiohttp

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
/api/0.6/user/#id
/api/0.6/users?users=#id1,#id2,...,#idn

[
/api/0.6/notes
/api/0.6/notes/#id
/api/0.6/notes/search
]

/api/0.6/changesets
/api/0.6/changeset/#id?include_discussion=true


"""
