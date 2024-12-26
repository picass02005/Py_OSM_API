# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

import asyncio

from Cogs.OSM.Py_OSM_API.BoundingBox import BoundingBox
from Cogs.OSM.Py_OSM_API.PyOsm import osm_builder


async def main():
    PyOsm = await osm_builder()

    print(PyOsm._capabilities)

    print(await PyOsm.get_uid_with_changeset("Chepycou"))  # 14112053
    print(await PyOsm.fetch_user_info(14112053))

    for i in await PyOsm.fetch_users_info([14112053, 1]):
        print(i)

    for i in await PyOsm.fetch_notes_by_box(
            BoundingBox(1.4645, 43.56968, 1.4696, 43.57408),
            50,
            7
    ):
        print(i)
        print([str(j) for j in i.comments])



asyncio.run(main())
