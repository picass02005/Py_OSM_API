# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

import math


class OSMBoundingBox:
    """
    This class is used to represent a bounding box
    For more information, please refer to https://wiki.openstreetmap.org/wiki/Bounding_box
    """

    def __init__(self, left: float, bottom: float, right: float, top: float) -> None:
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

    def get_area(self) -> float:
        """
        Get the area size of bounding box in decimal degrees
        :return: The area of bounding box
        """

        return math.fabs(self.left - self.right) * math.fabs(self.top - self.bottom)

    def check_data(self) -> bool:
        """
        Check if current values are valid:
        left <= right and in range [-180, 180]
        bottom <= top and in range [-90, 90]

        :return: True if they are valid
        """

        if -180 <= self.left <= self.right <= 180 and -90 <= self.bottom <= self.top <= 90:
            return True

        else:
            return False

    def cross_date_line(self) -> bool:
        """
        Tells if the bounding box cross dateline
        :return: Boolean
        """

        if 180 >= self.left > 0 > self.right >= -180:
            return True

        else:
            return False

    def __str__(self) -> str:
        """
        :return: The bounding box in the form of left,bottom,right,top
        """

        return f"{self.left},{self.bottom},{self.right},{self.top}"
