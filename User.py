# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

from datetime import datetime
from typing import Union, Dict, List


class OSMUser:
    """
    This class is used to represent a user
    """

    def __init__(self, json_response: Dict[str: Union[object, Dict[str: Union[object, Dict[str: object]]]]]) -> None:
        """
        Based on responses from those API endpoints /api/0.6/user/#id.json or /api/0.6/users.json?users=#id1,#id2
        :param json_response: The json response of each user (e.g. what's in "user" in the single user call)
        :return: None
        """

        self.uid: int = json_response["id"]

        self.display_name: str = json_response["display_name"]
        self.account_created: datetime = datetime.fromisoformat(json_response["account_created"])
        self.description: str = json_response["description"]
        self.pfp_link: str = json_response["img"]["href"] if "img" in json_response.keys() else ""
        self.roles: List = json_response["roles"]

        self.changesets_count: int = json_response["changesets"]["count"]
        self.traces_count: int = json_response["traces"]["count"]
        self.blocks_count: int = json_response["blocks"]["received"]["count"]
        self.blocks_active: int = json_response["blocks"]["received"]["active"]

        self.agreed_contributor_terms: bool = json_response["contributor_terms"]["agreed"]

    def __str__(self) -> str:
        """
        :return: A string corresponding to this object
        """

        return f"<OSMUser object: {self.display_name}, UID={self.uid}, Created on {self.account_created.isoformat()}>"
