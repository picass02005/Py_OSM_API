# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

import json
from typing import Dict, List

from .ChangesetCapabilites import ChangesetCapabilities
from .NoteCapabilities import NoteCapabilities
from .StatusCapabilities import StatusCapabilities


class OSMCapabilities:
    """
    This class represent OSM capabilities. You must update it at least once from API before using its values.
    """

    def __init__(self) -> None:
        self.area: float = 0
        self.timeout: int = 0

        self.changesets: ChangesetCapabilities = ChangesetCapabilities()
        self.notes: NoteCapabilities = NoteCapabilities()
        self.status: StatusCapabilities = StatusCapabilities()

    def to_dict(self) -> Dict[str, float | int | Dict[str, str | int]]:
        """
        Return values as a dict
        :return: The dict containing all values
        """

        return {
            "area": self.area,
            "timeout": self.timeout,
            "changesets": self.changesets.to_dict(),
            "notes": self.notes.to_dict(),
            "status": self.status.to_dict()
        }

    def update_from_api(
            self,
            json_values: Dict[str, str | Dict[str, Dict[str, str | float | int | List[Dict[str, str]]]]]
    ) -> None:
        """
        Update every value recursively from json response from OSM api
        :param json_values: The OSM api response in json
        :return: None
        """

        self.area = json_values["api"]["area"]["maximum"]
        self.timeout = json_values["api"]["timeout"]["seconds"]

        self.changesets.maximum_elements = json_values["api"]["changesets"]["maximum_elements"]
        self.changesets.maximum_query_limit = json_values["api"]["changesets"]["maximum_query_limit"]
        self.changesets.default_query_limit = json_values["api"]["changesets"]["default_query_limit"]

        self.notes.area = json_values["api"]["note_area"]["maximum"]
        self.notes.maximum_query_limit = json_values["api"]["notes"]["maximum_query_limit"]
        self.notes.default_query_limit = json_values["api"]["notes"]["default_query_limit"]

        self.status.database = json_values["api"]["status"]["database"]
        self.status.api = json_values["api"]["status"]["api"]
        self.status.gpx = json_values["api"]["status"]["gpx"]

    def __str__(self) -> str:
        """
        Return values as a json string
        :return: The json string containing all values
        """
        return json.dumps(self.to_dict())
