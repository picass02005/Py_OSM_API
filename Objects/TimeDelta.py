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

    def check_data_validity(self, optional_before: bool = True, optional_after: bool = True) -> bool:
        """
        Check if before and after are valid regarding time
        :param optional_before: Set to False if you need before value
        :param optional_after: Set to False if you need after value
        :return: True if data is valid
        """

        if (self.before is None and not optional_before) or (self.after is None and not optional_after):
            return False

        elif self.before is not None and self.after is not None:
            if self.before <= self.after:
                return True

            else:
                return False

        else:
            return True
