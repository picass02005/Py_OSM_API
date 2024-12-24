import json
import sys

import aiohttp


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
