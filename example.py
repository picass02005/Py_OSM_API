import asyncio

from Cogs.OSM.Py_OSM_API.PyOsm import make_py_osm


async def main():
    PyOsm = await make_py_osm()

    print(await PyOsm.get_uid_with_changeset("Chepycou"))  # 14112053
    print(await PyOsm.fetch_user_info(14112053))

    for i in await PyOsm.fetch_users_info([14112053, 1]):
        print(i)



asyncio.run(main())
