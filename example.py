# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

import asyncio
from datetime import datetime

from Enums import OSMOrder
from Enums import OSMSort
from Objects import OSMBoundingBox
from Objects import OSMTimeDelta
from PyOsm import py_osm_builder


# In this example, imports are referencing to the classes directly because of its location
# For your project you should import everything from Py_OSM_API
# from Py_OSM_API import *


async def main():
    py_osm = await py_osm_builder()  # Builds properly an instance of PyOSM

    # This bounding box is located around Paris and will be used through this example for some API calls
    paris_bbox = OSMBoundingBox(left=2.251854, bottom=48.814777, right=2.416649, top=48.901741)

    print("===== CAPABILITIES =====")

    # For more information about capabilities, please refer to documentation/OSMCapabilities_class.md

    print(py_osm.capabilities)  # Prints all capabilities (like max limit on some api calls, ...)
    print(py_osm.capabilities.notes.area)  # Print the maximum area in square degrees you can use when using a bounding
    # box in notes API calls

    print("\n===== USERS =====")

    # For more information about user object, please refer to documentation/OSMUser_class.md

    print("Fetch UID from user name")

    uid = await py_osm.get_uid_with_changeset("Chepycou")  # Get the UID of user named "Chepycou"
    print(uid)  # prints "14112053" which is Chepycou's user ID

    # Information about one user

    print("\nFetch one user's information")

    user = await py_osm.fetch_user_info(14112053)  # Fetch full information about this user
    print(user)  # Prints global information about him:
    # <OSMUser object: Chepycou, UID=14112053, Created on 2021-09-14T20:01:00+00:00>

    print(user.changesets_count)  # Prints how much changesets he made (3297 when typing this)

    # Information about multiple users

    print("\nFetch multiples users' information")

    users = await py_osm.fetch_users_info([1, 14112053])  # Fetch both users with UID 1 and 14112053

    for i in users:
        print(i)  # Prints general information about them
        # <OSMUser object: Steve, UID=1, Created on 2005-09-13T15:32:57+00:00>
        # <OSMUser object: Chepycou, UID=14112053, Created on 2021-09-14T20:01:00+00:00>

    print("\n===== NOTES =====")

    # For more information about note object, please refer to documentation/OSMNote_OSMNoteComment_class.md

    print("Fetch one note by its ID")

    note = await py_osm.fetch_note_by_id(4482167)  # Fetch the note with ID = 4482167
    print(note)  # Prints general information about this note
    print(note.geometry)  # Print the geometry representing the coordinates of this note
    # {'type': 'Point', 'coordinates': [1.5089116, 43.5814462]}

    for i in note.comments:
        print(i)  # Print comments made on this note. As I'm writing this, it returns the following:
        # <OSMNoteComment object: Chepycou, UID=14112053, Commented on 2024-10-17T08:22:50, "Missing a building here\nIl manque un bâtiment ici"\nOSM snapshot date: 2024-10-01T00:16:33Z\nPOI has no name\nPOI types: landuse-meadow\n #organicmaps android>
        # <OSMNoteComment object: Chepycou, UID=14112053, Commented on 2024-10-17T08:31:30, Added main building but not the rest of the place\nle bâtiment principal a été ajouté mais il reste tout le reste>

    print("\nFetch multiples notes within a bounding box")

    notes = await py_osm.fetch_notes_by_bbox(
        bbox=paris_bbox,
        limit=3,
        closed=0
    )  # Fetch 3 notes max which are in Paris and are currently opened

    for i in notes:
        print(i)  # As when I'm writing this script, the output is:
        # <OSMNote object: 4611638, Statuts=open, Created on 2025-02-02T17:22:09, 1 comments>
        # <OSMNote object: 4610037, Statuts=open, Created on 2025-02-01T10:28:56, 2 comments>
        # <OSMNote object: 4585076, Statuts=open, Created on 2025-01-11T14:05:38, 6 comments>

    print("\nFetch multiples notes corresponding to some criteria")

    # For documentation about each argument possible, please refer to documentation/PyOSM_class.md, section 5.3.

    notes = await py_osm.fetch_notes_by_search(
        limit=3,
        user_name="Chepycou",
        during=OSMTimeDelta(before=datetime.fromisoformat("2024-09-01"), after=datetime.fromisoformat("2024-09-30")),
        sort=OSMSort.CREATED_AT.value
    )

    for i in notes:
        print(i)
        # <OSMNote object: 4456204, Statuts=open, Created on 2024-09-28T14:47:32, 1 comments>
        # <OSMNote object: 4455755, Statuts=open, Created on 2024-09-28T10:04:05, 1 comments>
        # <OSMNote object: 4439924, Statuts=open, Created on 2024-09-17T13:19:29, 1 comments>

    print("\n===== CHANGESETS =====")

    # For more information about changeset object, please refer to
    # documentation/OSMChangeset_OSMChangesetComment_OSMChangesetTags_class.md

    print("Fetch a changeset by its ID")

    changeset = await py_osm.fetch_changeset_by_id(
        160518131,
        include_discussion=True
    )  # Fetch the changeset with ID = 160518131 with its discussion

    print(changeset)  # Prints general information about this changeset
    # <OSMChangeset object: id=160518131, user=Loren Maxwell, created_at=2024-12-22 22:58:12+00:00, tags=<OSMChangesetTags: {"comment": "Added border_type=state", "created_by": "JOSM/1.5 (19253 en)"}>>

    print(changeset.tags)  # Prints this changeset tags
    # <OSMChangesetTags: {"comment": "Added border_type=state", "created_by": "JOSM/1.5 (19253 en)"}>

    print(changeset.comments[0])  # Prints this changeset first comment general information
    # <OSMChangesetComment object: Tatti Barletta, UID=6693292, Commented on 2024-12-23T08:12:33+00:00, Please take a look at the wiki page: https://wiki.openstreetmap.org/wiki/Key:border_type\nIt makes no sense setting border_type.>

    print(changeset.comments[0].date)  # Prints the first comment post ID
    # 2024-12-23 08:12:33+00:00

    print("\nFetch multiple changesets corresponding to some criteria")

    # For documentation about each argument possible, please refer to documentation/PyOSM_class.md, section 6.2.

    changesets = await py_osm.fetch_changesets_by_search(
        limit=3,
        user_name="Chepycou",
        created_timedelta=OSMTimeDelta(
            before=datetime.fromisoformat("2025-01-01"),
            after=datetime.fromisoformat("2025-02-01")
        ),
        order=OSMOrder.NEWEST
    )  # This will get the 3 most recent changesets made by Chepycou created in january 2025

    for i in changesets:
        print(i)  # Print the basic information about those changesets
        # <OSMChangeset object: id=161890648, user=Chepycou, created_at=2025-01-29 10:08:40+00:00, tags=<OSMChangesetTags: {"comment": "Updated a kindergarten", "created_by": "Organic Maps android 2024.11.27-12-FDroid", "custom_tags": {"bundle_id": "app.organicmaps"}}>>
        # <OSMChangeset object: id=161713430, user=Chepycou, created_at=2025-01-24 13:53:31+00:00, tags=<OSMChangesetTags: {"comment": "Survey if places still exist", "created_by": "StreetComplete_ee 60.0", "source": "survey", "locale": "fr", "custom_tags": {"StreetComplete:quest_type": "CheckShopExistence"}}>>
        # <OSMChangeset object: id=161514672, user=Chepycou, created_at=2025-01-19 07:38:34+00:00, tags=<OSMChangesetTags: {"comment": "Edit element", "created_by": "StreetComplete_ee 60.0", "source": "survey", "locale": "fr", "custom_tags": {"StreetComplete:quest_type": "TagEdit"}}>>


asyncio.run(main())