import sys
import xml.etree.ElementTree as ET

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
            async with session.get(f"https://api.openstreetmap.org/api/0.6/capabilities") as resp:
                if resp.status == 200:
                    root = ET.fromstring(await resp.text())

                    self._ApiRates.update({
                        'changesets': {key: int(value) for key, value in root.find("api/changesets").attrib.items()},
                        'notes': {key: int(value) for key, value in root.find("api/notes").attrib.items()},
                        'timeout': int(root.find("api/timeout").attrib['seconds'])
                    })

                else:
                    sys.stderr.write("WARNING: Couldn't fetch OSM API rates")
                    return False


async def make_py_osm() -> PyOSM:
    pyosm = PyOSM()
    await pyosm.update_api_rates()

    return pyosm
