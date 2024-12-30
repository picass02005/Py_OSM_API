# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

from enum import Enum


class OSMSort(Enum):
    """
    This enum contains the valid values for sort parameter used by some API calls
    """

    CREATED_AT: str = "created_at"
    UPDATED_AT: str = "updated_at"
