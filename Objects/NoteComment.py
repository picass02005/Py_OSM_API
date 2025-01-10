# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

from datetime import datetime
from typing import Dict


class OSMNoteComment:
    """
    This class is used to represent a note comment
    """

    # noinspection PyTypeChecker
    def __init__(self, json_response: Dict[str, object]) -> None:
        """
        :param json_response: The json response of one note comment
        """

        self.date: datetime = datetime.strptime(json_response['date'], "%Y-%m-%d %H:%M:%S UTC")
        self.action: str = json_response['action']
        self.text: str = json_response['text']
        self.html: str = json_response['html']

        self.uid: int = json_response["uid"] if "uid" in json_response.keys() else -1
        self.user: str = json_response["user"] if "user" in json_response.keys() else ""
        self.user_url: str = json_response["user_url"] if "user_url" in json_response.keys() else ""

    def __str__(self) -> str:
        """
        :return: A string corresponding to this object
        """

        return f"<OSMNoteComment object: {self.user}, UID={self.uid}, Commented on {self.date.isoformat()}, {self.text}>"
