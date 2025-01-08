# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

from datetime import datetime
from typing import Optional


class OSMTimeDelta:
    """
    Represent a before and after couple for some API requet parameters
    """

    def __init__(self, before: Optional[datetime] = None, after: Optional[datetime] = None) -> None:
        """
        Initialize the class with values
        :param before: The before datetime
        :param after: The after datetime
        """

        self.before: None | datetime = before
        self.after: None | datetime = after

    def check_data_validity(self) -> bool:
        """
        Check if before and after are valid regarding time
        :return: True if data is valid
        """

        if self.before is None:
            return False

        elif self.after is None:
            return True

        else:
            if self.before <= self.after:
                return True

            else:
                return False
