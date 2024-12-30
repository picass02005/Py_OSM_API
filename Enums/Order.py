# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

from enum import Enum


class OSMOrder(Enum):
    """
    This enum contains the valid values for order parameter used by some API calls
    """

    OLDEST: str = "oldest"
    NEWEST: str = "newest"
