import asyncio

from Cogs.OSM.Py_OSM_API.main import make_py_osm


async def main():
    PyOsm = await make_py_osm()
    print(PyOsm._ApiRates)


asyncio.run(main())
