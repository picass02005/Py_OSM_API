# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

import asyncio

from Cogs.OSM.Py_OSM_API.BoundingBox import OSMBoundingBox
from Cogs.OSM.Py_OSM_API.PyOsm import osm_builder


async def main():
    py_osm = await osm_builder()

    print(py_osm._capabilities)

    print(await py_osm.get_uid_with_changeset("Chepycou"))  # 14112053
    print(await py_osm.fetch_user_info(14112053))

    for i in await py_osm.fetch_users_info([14112053, 1]):
        print(i)

    for i in await py_osm.fetch_notes_by_bbox(
            OSMBoundingBox(1.4645, 43.56968, 1.4696, 43.57408),
            50,
            7
    ):
        print(i)
        print([str(j) for j in i.comments])

    print("=====")
    print((note := await py_osm.fetch_note_by_id(3514775)))
    print([str(j) for j in note.comments])



asyncio.run(main())
