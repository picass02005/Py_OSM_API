# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

import json
from typing import Dict


class ChangesetCapabilities:
    """
    This class represent the changesets part of OSM capabilities
    """

    def __init__(self) -> None:
        self.maximum_elements: int = 0
        self.default_query_limit: int = 0
        self.maximum_query_limit: int = 0

    def to_dict(self) -> Dict[str, int]:
        """
        Return values as a dict
        :return: The dict containing all values
        """

        return {
            "maximum_elements": self.maximum_elements,
            "default_query_limit": self.default_query_limit,
            "maximum_query_limit": self.maximum_query_limit
        }

    def __str__(self) -> str:
        """
        Return values as a json string
        :return: The json string containing all values
        """
        return json.dumps(self.to_dict())
