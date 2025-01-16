# OSMBoundingBox documentation

---

## Table of content

1. [General description](#GeneralDescriptionLink)
2. [OSMBoundingBox](#OSMBoundingBoxLink)
    1. [Creating a bounding box](#CreateBboxLink)
    2. [Get area size](#GetAreaSizeLink)
    3. [Check data](#CheckDataLink)
    4. [Cross date line](#CrossDateLineLink)
    5. [String conversion](#StringConversionLink)

---

<a name="GeneralDescriptionLink"></a>

## 1. General description

A bounding box (usually shortened to bbox) is an area defined by two longitudes and two latitudes, where:

- Latitude is a float between -90.0 and 90.0
- Longitude is a float between -180.0 and 180.0

Bounding box are often used through the API, especially to search elements within an area.<br>
For more specific information, you can check
the [official Open Street Map documentation](https://wiki.openstreetmap.org/wiki/Bounding_box).

---

<a name="OSMBoundingBoxLink"></a>

## 2. OSMBoundingBox

<a name="CreateBboxLink"></a>

### 2.1. Creating a bounding box

To create a bounding box, you need to specify 4 values representing longitudes and latitudes limiting the bounding box (
in Decimal Degrees):

- Left (or minimum longitude)
- Bottom (or minimum latitude)
- Right (or maximum longitude)
- Top (or maximum latitude)

Each of thoses values are float respecting those rules:

- For left and right:
    - Between -180 and 180
    - Left must be smaller than right
- For bottom and top:
    - Between -90 and 90
    - Bottom must be smaller than top

Once you have those values, you have to create an instance of bounding box with them.<br>
For example, this is a bounding box corresponding to Paris, France.

````python
bbox = OSMBoundingBox(
    left=2.251854,
    bottom=48.814777,
    right=2.416649,
    top=48.901741
)
````

<a name="GetAreaSizeLink"></a>

### 2.2. Get area size

This method is used to get the area of your bounding box. Its value is returned in square degrees.

As example, the area of the bounding box defined above is 0.014 degrees squared.<br>
To get it, you can run the following code:

````python
area = bbox.get_area()
````

<a name="CheckDataLink"></a>

### 2.3. Check data

This method check data integrity according to the rules defined in [2.1. Creating a bounding box](#CreateBboxLink).<br>
It returns a boolean (``True`` if values are valid, elsewise ``False``).

````python
bbox.check_data()
````

<a name="CrossDateLineLink"></a>

### 2.4. Cross date line

This method checks if a bounding box is crossing date line.<br>
This is useful for some API calls which does not work properly if your bounding box crosses it.

<u>Note:</u> It is not 100% accurate: this only check if your bounding box cross the 0° longitude line.

The following example return if a bounding box crosses this line:

````python
bbox.cross_date_line()
````

<a name="StringConversionLink"></a>

### 2.5. String conversion

Open Street Map uses a representation of bounding box in the format ``left,bottom,right,top``.<br>
Naturally, when converting this value into a string, it returns it with the same format.

You can convert a bounding box into a string with standard python method:

````python
str(bbox)
````
