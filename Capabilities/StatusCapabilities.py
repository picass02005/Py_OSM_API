# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

import json
from typing import Dict


class StatusCapabilities:
    """
    This class represent the status part of OSM capabilities
    """

    def __init__(self) -> None:
        self.database: str = "offline"
        self.api: str = "offline"
        self.gpx: str = "offline"

    def to_dict(self) -> Dict[str, str]:
        """
        Return values as a dict
        :return: The dict containing all values
        """

        return {
            "database": self.database,
            "api": self.api,
            "gpx": self.gpx
        }

    def __str__(self) -> str:
        """
        Return values as a json string
        :return: The json string containing all values
        """
        return json.dumps(self.to_dict())
