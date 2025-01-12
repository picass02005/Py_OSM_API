# OSMCapabilities documentation

---

## Table of content

1. [OSMCapabilities](#OSMCapabilitiesLink)
2. [ChangesetCapabilities](#ChangesetCapabilitiesLink)
3. [NoteCapabilities](#NoteCapabilitiesLink)
4. [StatusCapabilities](#StatusCapabilitiesLink)
5. [Convertions](#ConvertionsLink)
6. [Update capabilities](#UpdateCapabilitiesLink)

---

<a name="OSMCapabilitiesLink"></a>

## 1. OSMCapabilities

This read-only class is used to access information about Open Street Map capabilities.<br>
This class have the following attributes defined in it:

````python
area: float
timeout: int

changesets: ChangesetCapabilities
notes: NoteCapabilities
status: StatusCapabilities
````

- area: Maximum area in square degrees which can be queried by API calls
- timeout: Time you must wait in case you get rate limited by the API

---

<a name="ChangesetCapabilitiesLink"></a>

## 2. ChangesetCapabilities

This class have 3 values

- maximum_elements: Maximum number of combined nodes, way and relations that can be containes in a changeset
- default_query_limit: Default limit in number of changesets returned.
- maximum_query_limit: Maximum limit in number of changesets returned

---

<a name="NoteCapabilitiesLink"></a>

## 3. NoteCapabilities

This class have 3 values

- area: Maximum area you can get at one time when you fetch notes
- default_query_limit: Same as in ChangesetCapabilities but for notes
- maximum_query_limit: Same as in ChangesetCapabilities but for notes

---

<a name="StatusCapabilitiesLink"></a>

## 4. StatusCapabilities

This class have 3 values showing which services are ``online``, ``readonly`` or ``offline``

- database
- api
- gpx

---

<a name="ConvertionsLink"></a>

## 5. Convertions

``OSMCapabilities``, ``ChangesetCapabilities``, ``NoteCapabilities`` and ``StatusCapabilities`` have a `to_dict()`
function to convert their values into a dictionary.<br>
``OSMCapabilities`` also have a string convertion using ``str(py_osm.capabilities)``.

---

<a name="UpdateCapabilitiesLink"></a>

## 6. Update capabilities

To update capabilities, you can use ``await py_osm.update_capabilities``<br>
Note: all default_query_limit values are directly hard coded in PyOSM function call
