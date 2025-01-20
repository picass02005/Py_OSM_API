# OSMSort, OSMOrder and OSMStatus documentation

---

## Table of content

1. [General description](#GeneralDescLink)
2. [OSMOrder](#OSMOrderLink)
    1. [Oldest to newest](#OSMOrderOldLink)
    2. [Newest to oldest](#OSMOrderNewLink)
3. [OSMSort](#OSMSortLink)
    1. [Created at](#OSMSortCreateLink)
    2. [Updated at](#OSMSortUpdateLink)
4. [OSMStatus](#OSMStatusLink)
    1. [Open](#OSMStatusOpenLink)
    2. [Closed](#OSMStatusClosedLink)
    3. [Both open or closed](#OSMStatusOpenClosedLink)

---

<a name="GeneralDescLink"></a>

## 1. General description

Those classes are enums used by some API calls.<br>
When needed, you can pass them as argument by typing ``OSMXxxx.yyyy`` where ``Xxxx`` is the class name, and ``yyyy`` is
the attribute you want.

---

<a name="OSMOrderLink"></a>

## 2. OSMOrder

This represents the order in which you want your bulk search to be returned.

<a name="OSMOrderOldLink"></a>

### 2.1. Oldest to newest

When this is used, returned data will be sorted from older to newer ones.

````python
OSMOrder.OLDEST
````

<a name="OSMOrderNewLink"></a>

### 2.2. Newest to oldest

When this is used, returned data will be sorted from newer to older ones.

````python
OSMOrder.NEWEST
````

---

<a name="OSMSortLink"></a>

## 3. OSMSort

This is used in combination with an [OSMTimeDelta](OSMTimeDelta_class.md) to precise if you want data created or updated
in it.

<a name="OSMSortCreateLink"></a>

### 3.1. Created at

When this is used, this will return data which was created in the defined [OSMTimeDelta](OSMTimeDelta_class.md).

````python
OSMSort.CREATED_AT
````

<a name="OSMSortUpdateLink"></a>

### 3.2. Updated at

When this is used, this will return data which was updated in the defined [OSMTimeDelta](OSMTimeDelta_class.md).

````python
OSMSort.UPDATED_AT
````

---

<a name="OSMStatusLink"></a>

## 4. OSMStatus

This is used to filter returned data by their current status: either opened, closed or both of them.

<a name="OSMStatusOpenLink"></a>

### 4.1. Open

Only returned data which is currently opened.

````python
OSMStatus.OPEN
````

<a name="OSMStatusClosedLink"></a>

### 4.2. Closed

Only returned data which is currently closed.

````python
OSMStatus.CLOSED
````

<a name="OSMStatusOpenClosedLink"></a>

### 4.3. Both open or closed

Return data which is open or closed (e.g. everything).

````python
OSMStatus.OPEN_AND_CLOSED
````
