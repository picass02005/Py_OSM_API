import asyncio

from Cogs.OSM.Py_OSM_API.main import make_py_osm


async def main():
    PyOsm = await make_py_osm()

    print(await PyOsm.get_uid_with_changeset("Chepycou"))  # 14112053



asyncio.run(main())
