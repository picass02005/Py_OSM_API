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

---

<a name="InitClassLink"></a>

## 1. How to properly init this class

To initialize properly this class, use the ``py_osm_builder()`` couroutine.

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

# TODO: this part

<a name="FetchNotesBboxLink"></a>

### 5.2. Fetch notes by bounding box

# TODO: this part

<a name="FetchNotesSearch"></a>

### 5.3. Fetch notes by search

# TODO: this part

---

# TODO: changesets