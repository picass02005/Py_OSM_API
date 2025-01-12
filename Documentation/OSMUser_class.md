# OSMUser documentation

---

## Table of content

1. [OSMUser](#OSMUserLink)
    1. [UID](#UIDLink)
    2. [Display Name](#DisplayNameLink)
    3. [Account Created](#AccountCreatedLink)
    4. [Description](#DescriptionLink)
    5. [Profile picture link](#PfpLink)
    6. [Roles](#RolesLink)
    7. [Changesets Count](#ChangesetsCountLink)
    8. [Traces Count](#TracesCountLink)
    9. [Blocks Count](#BlocksCountLink)
    10. [Blocks Active](#BlocksActiveLink)
    11. [Agreed Contributor Terms](#AgreedContributorTermsLink)
2. [String Conversion](#StringConversionLink)

---

<a name="OSMUserLink"></a>

## 1. OSMUser

This class represents an Open Street Map user.<br>
This is a read-only class generated by some API calls containing serveral attributes.

<a name="UIDLink"></a>

### 1.1. UID

````python
user.uid
````

This attribute is an integer containing the UID of this user.

<a name="DisplayNameLink"></a>

### 1.2. Display Name

````python
user.display_name
````

This attribute is a string containing the username of this user.

<a name="AccountCreatedLink"></a>

### 1.3. Account Created

````python
user.account_created
````

This attribute is a [datetime.datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime) object
containing the creation date of this user.

<a name="DescriptionLink"></a>

### 1.4. Description

````python
user.description
````

This attribute is a string containing the description of this user.

<a name="PfpLink"></a>

### 1.5. Profile picture link

````python
user.pfp_link
````

This attribute is a string containing a link to this user profile picture.

<a name="RolesLink"></a>

### 1.6. Roles

````python
user.roles
````

This attribute is a list of string containing all roles a user may have (``moderator``, ``administrator``, ...).

<a name="ChangesetsCountLink"></a>

### 1.7. Changesets Count

````python
user.changesets_count
````

This attribute is an integer containing the number of changesets this user have ever made.

<a name="TracesCountLink"></a>

### 1.8. Traces Count

````python
user.traces_count
````

This attribute is an integer containing the number of traces this user have ever made.

<a name="BlocksCountLink"></a>

### 1.9. Blocks Count

````python
user.blocks_count
````

This attribute is an integer containing the number of blocks this user have ever made.

<a name="BlocksActiveLink"></a>

### 1.10. Blocks Active

````python
user.blocks_active
````

This attribute is an integer containing the number of active blocks this user have.

<a name="AgreedContributorTermsLink"></a>

### 1.11. Agreed Contributor Terms

````python
user.agreed_contributor_terms
````

This attribute is a boolean indicating if the user have agreed to contributor terms.

---

<a name="StringConversionLink"></a>

## 2. String Conversion

To convert this class into a string, you can use standard python method.

````python
str(user)  # <OSMUser object: USERNAME, UID=XXX, Created on CREATION_DATE_IN_ISO_8601>
````