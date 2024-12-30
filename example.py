# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

import asyncio
from datetime import datetime

from Cogs.OSM.Py_OSM_API import OSMSort, OSMOrder
from Cogs.OSM.Py_OSM_API.BoundingBox import OSMBoundingBox
from Cogs.OSM.Py_OSM_API.PyOsm import osm_builder


async def main():
    py_osm = await osm_builder()

    print(py_osm._capabilities)

    print(await py_osm.get_uid_with_changeset("Chepycou"))  # 14112053
    print(await py_osm.fetch_user_info(14112053))

    for i in await py_osm.fetch_users_info([14112053, 1]):
        print(i)

    print("=====")

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

    print("=====")

    for i in await py_osm.fetch_notes_by_search(
            limit=5,
            closed=-1,
            query="Missing path",
            user_name="Chepycou",
            user_id=14112053,
            bbox=OSMBoundingBox(1.4645, 43.56968, 1.4696, 43.57408),
            before=datetime.fromisoformat("2022-06-01"),
            after=datetime.fromisoformat("2022-05-01"),
            sort=OSMSort.CREATED_AT,
            # order="newest"
            order=OSMOrder.NEWEST
    ):
        print(i)
        print([str(j) for j in i.comments])



asyncio.run(main())
