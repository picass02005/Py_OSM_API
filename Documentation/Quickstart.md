# Quickstart

---

## Asyncio introduction

In order to use this package, you need to set an asynchronus execution loop using asyncio.
Asyncio official documentation is available [here](https://docs.python.org/3/library/asyncio.html).<br>
The minimal script required to use this lib is the following:

````python
import asyncio
import
from Py_OSM_API import py_osm_builder  # Builder function for PyOSM class


async def main():  # This will be the main function of your asynchronous execution loop
    py_osm = await py_osm_builder()  # Create an instance of PyOSM class and initialize it properly


asyncio.run(main())  # Used to start the loop, refer to asyncio manual for more information
````

You then have a working instance of PyOSM in the main function.<br>
Every asynchronous calls must be preceded by the keyword ``await``.<br>
An asynchronous function must be defined with the keywords ``async def``.

As an example, the following script will print in the console some information about the user named "Chepycou".

````python
import asyncio
import
from Py_OSM_API import py_osm_builder


async def main():
    py_osm = await py_osm_builder()

    user_id = await py_osm.get_uid_with_changeset("Chepycou")  # Fetch user ID
    print(user_id)  # 14112053

    user = await py_osm.fetch_user_info(user_id)  # Fetch all information about this user
    print(user.account_created)  # 2021-09-14 20:01:00+00:00
    print(user.changesets_count)  # 3293 (at the time I write this script)
````

You now know how to use this API.

For more information about specific parts, I highly encourage you to check the other files located in
the [documentation folder](.).<br>
I also recommend you to check the [main class documentation](PyOSM_class.md).<br>
Never hesitate to check [official Open Street Map API documentation](https://wiki.openstreetmap.org/wiki/API_v0.6).
