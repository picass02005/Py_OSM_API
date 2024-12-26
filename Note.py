# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

from datetime import datetime
from typing import Union, Dict, List

from Cogs.OSM.Py_OSM_API.Comment import OSMComment


class OSMNote:
    """
    This class is used to represent a note
    """

    def __init__(self, json_response: Dict[str: Union[object, Dict[str: Union[object, Dict[str: object]]]]]) -> None:
        """
        Based on responses from this API endpoint /api/0.6/notes.json
        :param json_response: The json response of each note (e.g. what's in "features")
        :return: None
        """

        self.type: str = json_response['type']
        self.geometry: Dict[str: str | List[float]] = json_response['geometry']

        self.id: int = json_response['properties']['id']
        self.url: str = json_response['properties']['url']
        self.comment_url: str = json_response['properties']['comment_url']
        self.close_url: str = json_response['properties']['close_url']
        self.date_created: datetime = datetime.fromisoformat(json_response['properties']['date_created'])
        self.status: str = json_response['properties']['status']

        self.comments: List[OSMComment] = [OSMComment(i) for i in json_response['comments']]

    def __str__(self) -> str:
        """
        :return: A string corresponding to this object
        """

        return f"<OSMNote object: {self.id}, Statuts={self.status}, Created on {self.date_created.isoformat()}>"
