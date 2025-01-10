# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

from datetime import datetime
from typing import Dict


class OSMChangesetComment:
    """
    This class is used to represent a changeset comment
    """

    def __init__(self, json_response: Dict[str, int | bool | str]) -> None:
        """
        :param json_response: The json response of one changeset comment
        """

        self.comment_id: int = json_response['id']
        self.visible: bool = json_response['visible']

        self.date: datetime = datetime.fromisoformat(json_response['date'])

        self.uid: int = json_response["uid"] if "uid" in json_response.keys() else -1
        self.user: str = json_response["user"] if "user" in json_response.keys() else ""

        self.text: str = json_response["text"]

    def __str__(self) -> str:
        """
        :return: A string corresponding to this object
        """

        return (f"<OSMChangesetComment object: {self.user}, UID={self.uid}, Commented on {self.date.isoformat()}, "
                f"{self.text}>")
