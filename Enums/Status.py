# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

from enum import Enum


class OSMStatus(Enum):
    """
    This enum contains the valid values for open / closed statuts parameter used by some API calls
    """

    OPEN: str = "o"
    CLOSED: str = "c"
    OPEN_AND_CLOSED: str = "o&c"
