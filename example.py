# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

import asyncio
from datetime import datetime

from Cogs.OSM.Py_OSM_API import OSMBoundingBox, OSMStatus, OSMTimeDelta
from Cogs.OSM.Py_OSM_API import OSMSort, OSMOrder
from Cogs.OSM.Py_OSM_API.PyOsm import py_osm_builder


async def main():
    py_osm = await py_osm_builder()

    print(py_osm.capabilities)

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
            during=OSMTimeDelta(datetime.fromisoformat("2022-05-01"), datetime.fromisoformat("2022-06-01")),
            sort=OSMSort.CREATED_AT,
            # order="newest"
            order=OSMOrder.NEWEST
    ):
        print(i)
        print([str(j) for j in i.comments])

    print("==========")

    for i in await py_osm.fetch_changesets_by_search(
            limit=50,
            # user_name="Chepycou",
            user_id=14112053,
            bbox=OSMBoundingBox(1.4645, 43.56968, 1.4696, 43.57408),
            created_timedelta=OSMTimeDelta(datetime.fromisoformat("2024-01-01"), datetime.fromisoformat("2025-01-01")),
            closed_timedelta=OSMTimeDelta(datetime.fromisoformat("2024-01-01"), datetime.fromisoformat("2025-01-01")),
            by_ids=(160803069, 156684643, 156400019),
            status=OSMStatus.CLOSED,
            order=OSMOrder.NEWEST
    ):
        print(i)

    print("=====")

    print(tmp := await py_osm.fetch_changeset_by_id(160518131, include_discussion=True))
    print([str(i) for i in tmp.comments])

    print("=====")

    user_id = await py_osm.get_uid_with_changeset("Chepycou")
    print(user_id)  # 14112053

    user = await py_osm.fetch_user_info(user_id)
    print(user)
    print(user.account_created)  # 2021-09-14 20:01:00+00:00
    print(user.changesets_count)  # 3293 (at the time I write this script)

    print("=====")

    users = await py_osm.fetch_users_info([1, 14112053])
    print(users[0])
    print(users[1])

    print(OSMBoundingBox(left=2.251854, bottom=48.814777, right=2.416649, top=48.901741).get_area())

    print("=====")

    notes = await py_osm.fetch_notes_by_bbox(
        bbox=OSMBoundingBox(left=2.251854, bottom=48.814777, right=2.416649, top=48.901741), limit=2, closed=3)

    for i in notes:
        print(i)

    print("=====")

    notes = await py_osm.fetch_notes_by_search(
        limit=2,
        closed=7,
        query="Sidewalk",
        # user_name="fgouget",  # You can only use user_name or user_id but not both at the same time
        user_id=2678738,
        bbox=OSMBoundingBox(left=2.251854, bottom=48.814777, right=2.416649, top=48.901741),
        during=OSMTimeDelta(before=datetime(year=2025, month=1, day=1), after=datetime(year=2025, month=1, day=31)),
        sort=OSMSort.CREATED_AT,
        order=OSMOrder.OLDEST,
    )

    for i in notes:
        print(i)

    # <OSMNote object: 4589392, Statuts=closed, Created on 2025-01-15T04:24:34, 2 comments>
    # <OSMNote object: 4590107, Statuts=closed, Created on 2025-01-15T18:16:01, 2 comments>

    print("=====")

    a = await py_osm.fetch_changeset_by_id(160518131, include_discussion=True)
    print(a)
    # <OSMChangeset object: id=160518131, user=Loren Maxwell, created_at=2024-12-22 22:58:12+00:00, tags=<OSMChangesetTags: {"custom_tags": {}}>>
    print(a.comments[0])
    # <OSMChangesetComment object: Tatti Barletta, UID=6693292, Commented on 2024-12-23T08:12:33+00:00, Please take a look at the wiki page: https://wiki.openstreetmap.org/wiki/Key:border_type\nIt makes no sense setting border_type.>

    print("=====")

    changesets = await py_osm.fetch_changesets_by_search(
        limit=2,
        # user_name="one way home",  # You can only use user_name or user_id but not both at the same time
        user_id=17131126,
        bbox=OSMBoundingBox(left=2.251854, bottom=48.814777, right=2.416649, top=48.901741),
        created_timedelta=OSMTimeDelta(before=datetime(year=2025, month=1, day=1),
                                       after=datetime(year=2025, month=1, day=31)),
        closed_timedelta=OSMTimeDelta(before=datetime(year=2025, month=2, day=1),
                                      after=datetime(year=2025, month=2, day=28)),
        by_ids=(161944524, 161943177, 161943119),  # Only return changesets in this tuple
        # The oldest one will be ignored because of order and limit values
        status=OSMStatus.CLOSED,
        order=OSMOrder.NEWEST
    )

    for i in changesets:
        print(i)

    # <OSMChangeset object: id=161944524, user=one way home, created_at=2025-01-30 16:32:59+00:00, tags=<OSMChangesetTags: {}>>
    # <OSMChangeset object: id=161943177, user=one way home, created_at=2025-01-30 15:56:25+00:00, tags=<OSMChangesetTags: {}>>


asyncio.run(main())

# TODO: remove
