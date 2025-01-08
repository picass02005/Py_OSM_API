# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

from datetime import datetime
from typing import Dict

from .BoundingBox import OSMBoundingBox
from .ChangesetTags import OSMChangesetTags

type _json_types = None | str | float | int | bool


class OSMChangeset:
    """
    This class is used to represent a changeset
    """

    def __init__(self, json_response: Dict[str, _json_types | Dict[str, _json_types]]) -> None:
        """
        :param json_response: The json response returned by API corresponding to a changeset
        :return: None
        """

        self.id: int = json_response["id"]
        self.comments_count: int = json_response["comments_count"]
        self.changes_count: int = json_response["changes_count"]
        self.uid: int = json_response["uid"]

        self.open: bool = json_response["open"]

        self.created_at: datetime = datetime.fromisoformat(json_response["created_at"])

        if "closed_at" in json_response.keys():
            self.closed_at: datetime = datetime.fromisoformat(json_response["closed_at"])

        else:
            self.closed_at: datetime = datetime.fromisoformat("1970-01-01T00:00:00Z")

        self.boundingBox: OSMBoundingBox = OSMBoundingBox(
            json_response["min_lon"],
            json_response["min_lat"],
            json_response["max_lon"],
            json_response["max_lat"]
        )

        self.user: str = json_response["user"]

        self.tags: OSMChangesetTags(json_response) = OSMChangesetTags(json_response)

    def __str__(self) -> str:
        """
        Convert this class into a string
        :return: The generated string
        """

        return (f"<OSMChangeset object: id={self.id}, user={self.user}, created_at={self.created_at}, "
                f"tags={str(self.tags)}>")
