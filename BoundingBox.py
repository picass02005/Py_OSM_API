# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved


class BoundingBox:
    """
    This class is used to represent a bounding box
    For more information, please refer to https://wiki.openstreetmap.org/wiki/Bounding_box
    """

    def __init__(self, left: float, bottom: float, right: float, top: float) -> None:
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top
