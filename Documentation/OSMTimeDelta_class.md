# OSMTimeDelta documentation

---

## Table of content

1. [General description](#GeneralDescriptionLink)
2. [OSMTimeDelta](#OSMTimeDeltaLink)
    1. [Create a time delta](#CreateTimeDeltaLink)
    2. [Check data validity](#CheckDataLink)

---

<a name="GeneralDescriptionLink"></a>

## 1. General description

Some API calls can search element based on a time span.<br>
This class is used to represent a time span.<br>
Some API call can work with only a single value. This is specified in their respective documentation.

---

<a name="OSMTimeDeltaLink"></a>

## 2. OSMTimeDelta

This class works with standard [datetime.datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime)
objects.<br>
``Before`` value must takes place before ``after`` timewise.<br>
Before and after can both be ``None`` if undefined.

<a name="CreateTimeDeltaLink"></a>

### 2.1. Create a time delta

The following code shows you 3 time delta:

1. Defined with before and after
2. Defined with only before
3. Defined with only after

````python
# ===== 1 ===== #

time_delta = OSMTimeDelta(
    before=datetime(year=2025, month=1, day=2, hour=3, minute=4, second=5),
    after=datetime(year=2025, month=1, day=3, hour=0, minute=0, second=0)
)

# ===== 2 ===== #

time_delta = OSMTimeDelta(before=datetime(year=2025, month=1, day=2, hour=3, minute=4, second=5))

# ===== 3 ===== #

time_delta = OSMTimeDelta(after=datetime(year=2025, month=1, day=3, hour=0, minute=0, second=0))
````

<u>Tips:</u> you can create a datetime object from [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format like this:

````python
datetime.fromisoformat("2025-01-02T03:04:05Z")
# Equivalent to datetime(year=2025, month=1, day=2, hour=3, minute=4, second=5)
````

<a name="CheckDataLink"></a>

### 2.2. Check data validity

This method is used to check if before and after datetime are valid (e.g. they're defined if not optional, and before <
after).

It takes 2 boolean arguments representing if before or after values are optional:

- optional_before (default: ``True``)
- optional_after (default: ``True``)

It returns a bolean indicating if defined values are valid or not.

````python
time_delta.check_data_validity()  # Check with before and after as optional values

time_delta.check_data_validity(optional_before=False)  # Here, before is required
time_delta.check_data_validity(optional_after=False)  # Here, after is required

# This will have both before and after value as required
time_delta.check_data_validity(optional_before=False, optional_after=False)
````