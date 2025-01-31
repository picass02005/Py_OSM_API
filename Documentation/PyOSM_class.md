# PyOSM class documentation

---

This is the main class of this whole package.
You need an initialized instance of it to performs API calls.

## Table of content

1. [How to properly init this class](#InitClassLink)
2. [Capabilities](#CapabilitiesLink)
3. [Get user ID](#GetUIDLink)
    1. [By logging into the user's account](#GetUIDLoginLink)
    2. [By using a workaround with changesets search](#GetUIDChangesetLink)
4. [Get user(s) information](#GetUserInfoLink)
    1. [For a single user](#SingleUserInfoLink)
    2. [For multiple users](#MultipleUserInfoLink)
5. [Get note(s)](#GetNotesLink)
    1. [Fetch notes by ID](#FetchNotesIdLink)
    2. [Fetch notes by bounding box](#FetchNotesBboxLink)
    3. [Fetch notes by search](#FetchNotesSearch)
6. [Get changeset(s)](#GetChangesetsLink)
    1. [Fetch changeset by ID](#FetchChangesetsIdLink)
    2. [Fetch changesets by search](#FetchChangesetsSearchLink)

---

<a name="InitClassLink"></a>

## 1. How to properly init this class

To properly initialize this class, use the ``py_osm_builder()`` couroutine.

````python
py_osm = await py_osm_builder()
````

---

<a name="CapabilitiesLink"></a>

## 2. Capabilities

Open street map API have some limits for requests.
In PyOSM, they're located in ``PyOSM.capabilities``.
This variable is an instance of ``OSMCapabilities`` class.<br>
For more information, please check [OSMCapabilities documentation](OSMCapabilities_class.md).

---

<a name="GetUIDLink"></a>

## 3. Get user ID

There are 2 ways to get a user ID in open street map.<br>
The user ID is necessary to perform serveral API requests.

<a name="GetUIDLoginLink"></a>

### 3.1. By logging into the user's account

<u>DISCLAMER:</u> For this method, you need to know the login and password of the account you want.

1. Login into this Open Street Map account
2. Go on [this API url](https://api.openstreetmap.org/api/0.6/user/details.json)
3. Your UID is the value located in ``{'user': {'id': YOUR_USER_ID, ...}, ...}``

<a name="GetUIDChangesetLink"></a>

### 3.2. By using a workaround with changesets search

<u>DISCLAMER:</u> This method need the targeter user to have made at least 1 changeset with his account.

For this method, you can use ``PyOSM.get_uid_with_changeset``.<br>
The following script will print the user ID of Chepycou.

````python
user_id = await py_osm.get_uid_with_changeset("Chepycou")

print(user_id)  # Prints 14112053
````

---

<a name="GetUserInfoLink"></a>

## 4. Get user(s) information

In PyOSM there are 2 ways to get user(s) information.<br>
Both of those ways return information for each user in an `OSMUser` class.<br>
For more information about this class, [look at its documentation](OSMUser_class.md).

<a name="SingleUserInfoLink"></a>

### 4.1. For a single user

For a single user, you can use ``PyOSM.fetch_user_info``.

This function takes as parameter a user_id (in the form of an integer).<br>
It returns a ``OSMUser`` object if it's successfull.<br>
If it failed, returns ``None``.

The following script will get information about user with ID ``14112053``.

````python
user = await py_osm.fetch_user_info(14112053)

print(user)  # <OSMUser object: Chepycou, UID=14112053, Created on 2021-09-14T20:01:00+00:00>
````

<a name="MultipleUserInfoLink"></a>

### 4.2. For multiple users

For multiple users, you can use ``PyOSM.fetch_users_info``.

This function takes as parameter a set of integers (can be any iterable), representing each user ID.<br>
It returns a tuple of ``OSMUser`` object (Note: if it fails to get a user, it is skipped).

The following script will get information about users with ID ``1`` and ```14112053```.

````python
users = await py_osm.fetch_users_info([1, 14112053])

print(users[0])  # <OSMUser object: Steve, UID=1, Created on 2005-09-13T15:32:57+00:00>
print(users[1])  # <OSMUser object: Chepycou, UID=14112053, Created on 2021-09-14T20:01:00+00:00>
````

---

<a name="GetNotesLink"></a>

## 5. Get note(s)

Information about a note are stocked in the read-only ``OSMNote`` class.<br>
For more information about this class, please
check [OSMNote and OSMNoteComment documentation](OSMNote_OSMNoteComment_Class.md).

<a name="FetchNotesIdLink"></a>

### 5.1. Fetch notes by ID

You can get information about a note with its ID. For this, you can use ``py_osm.fetch_note_by_id``.<br>
This function takes as parameter a note_id as a float.<br>
It returns a single [OSMNote](OSMNote_OSMNoteComment_Class.md) object (or ``None`` if not found).

The following script will get information about note with ID ``3177810``:

````python
note = await py_osm.fetch_note_by_id(3177810)

print(note)  # <OSMNote object: 3177810, Statuts=closed, Created on 2022-05-13T16:57:36, 2 comments>

for comment in note.comments:  # Loop through each comments
    print(comment)

# <OSMNoteComment object: Chepycou, UID=14112053, Commented on 2022-05-13T16:57:36, Missing path\nChemin manquant\n\nvia StreetComplete 43.0>
# <OSMNoteComment object: K12230LF, UID=21876225, Commented on 2025-01-13T16:29:15, added>
````

<a name="FetchNotesBboxLink"></a>

### 5.2. Fetch notes by bounding box

You can get notes located in a [bounding box](OSMBoundingBox_class.md) using ``py_osm.fetch_notes_by_bbox``.<br>
This function takes those parameters:

- bbox: The [bounding box](OSMBoundingBox_class.md) delimiting where you want your notes to be in. This have some
  requirements:
    - This can't cross the date line
    - Its area must be under ``py_osm.capabilities.notes.area`` (actual value: 25 square degrees)
- limit: Positive integer corresponding to the maximum number of notes returned by this
    - This is optional, default value is 100 notes
    - Its value must be under ``py_osm.capabilities.notes.maximum_query_limit`` (actual value: 10000)
- closed: Integer, exclude all notes closed for more days than this value, opened notes are always fetched
    - This is optional, default value is 7 days (notes closed for more than 7 days are ignored)
    - If this value is set to ``0``, only returns opened notes
    - If this value is set to ``-1``, return any notes

````python
notes = await py_osm.fetch_notes_by_bbox(
    bbox=OSMBoundingBox(left=2.251854, bottom=48.814777, right=2.416649, top=48.901741),
    limit=2,
    closed=3
)

for i in notes:
    print(i)

# At the time I'm writing this, this script returns those values:
# <OSMNote object: 4517955, Statuts=closed, Created on 2024-11-13T11:21:47, 2 comments>
# <OSMNote object: 4590117, Statuts=open, Created on 2025-01-15T18:30:32, 2 comments>
````

<a name="FetchNotesSearch"></a>

### 5.3. Fetch notes by search

You can also get notes corresponding to some criteria. For this you can use ``py_osm.fetch_notes_by_search``.<br>
For more specific documentation, please check the
official [Open Street Map documentation](https://wiki.openstreetmap.org/wiki/API_v0.6#Search_for_notes:_GET_/api/0.6/notes/search).

Each argument is a criteria, and is optional:

- limit: An integer defining the maximum of OSMNotes returned
    - Default value: 100 OSMNotes
- closed: Integer, exclude all notes closed for more days than this value, opened notes are always fetched
    - Default value: 7 days (notes closed for more than 7 days are ignored)
    - If this value is set to ``0``, only returns opened notes
    - If this value is set to ``-1``, return any notes
- query: A string which, when set, represents keywords to search (either in the note itself or in note comments)
- user_name: A string which, when set, returns only notes made by this user
- user_id: An int which, when set, returns only notes made by this user ID
    - When both user_name and user_id defined, user_id is ignored
- bbox: An [OSMBoundingBox](OSMBoundingBox_class.md) which, when set, will only return notes which are within this
- during: An [OSMTimeDelta](OSMTimeDelta_class.md) which, when set, will perform time related sorting
    - Before argument in this [OSMTimeDelta](OSMTimeDelta_class.md) is optional
    - You need to define ``sort`` for this argument to work
- sort: An [OSMSort](OSMSort_OSMOrder_OSMSatus_class.md) which, when set, will specify if ``during`` is filtering on
  ``creation`` or ``update``
    - You need to define ``during`` for this argument to work
- order: An [OSMOrder](OSMSort_OSMOrder_OSMSatus_class.md) which, when set, will order returned data in order first or
  newer first

Return of this function is a tuple of [OSMNotes](OSMNote_OSMNoteComment_Class.md).

If any parameter is invalid, this will raise a ``TypeError``.

````python
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

# At the time I'm writing this, this script returns those values:
# <OSMNote object: 4589392, Statuts=closed, Created on 2025-01-15T04:24:34, 2 comments>
# <OSMNote object: 4590107, Statuts=closed, Created on 2025-01-15T18:16:01, 2 comments>
````

---

<a name="GetChangesetsLink"></a>

## 6. Get changeset(s)

Information about a changeset are stocked in the read-only ``OSMChangeset`` class.<br>
For more information about this class, please
check [OSMChangeset, OSMChangesetComment and OSMChangesetTags documentation](OSMChangeset_OSMChangesetComment_OSMChangesetTags_class).

<a name="FetchChangesetsIdLink"></a>

### 6.1. Fetch changeset by ID

This function get a changeset by its ID.<br>
This is the only way to retrieve discussions made under a changeset.

This takes as parameter:

- changeset_id: An integer representing the ID of the changeset you want to retrieve
- include_discussion: A boolean telling the API if you also want to retrieve the discussion.<br>
  You should avoid setting it to ``True`` if not needed.

The following code is an example containing multiple comments:

````python
changeset = await py_osm.fetch_changeset_by_id(changeset_id=160518131, include_discussion=True)

print(changeset)
# <OSMChangeset object: id=160518131, user=Loren Maxwell, created_at=2024-12-22 22:58:12+00:00, tags=<OSMChangesetTags: {"custom_tags": {}}>>

print(changeset.comments[0])  # Prints the first comment
# <OSMChangesetComment object: Tatti Barletta, UID=6693292, Commented on 2024-12-23T08:12:33+00:00, Please take a look at the wiki page: https://wiki.openstreetmap.org/wiki/Key:border_type\nIt makes no sense setting border_type.>
````

<a name="FetchChangesetsSearchLink"></a>

### 6.2. Fetch changesets by search
