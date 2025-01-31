# SPDX-License-Identifier: MIT
# Copyright (C) 2024 picasso2005 <clementduran0@gmail.com> - All Rights Reserved

import json
from typing import Dict, Tuple

type _json_types = None | str | float | int | bool


class OSMChangesetTags:
    """
    This class is used to represet tags on a changeset
    """

    def __init__(self, json_response: Dict[str, _json_types | Dict[str, _json_types]]) -> None:
        """
        :param json_response: The json response returned by API corresponding to a changeset
        :return: None
        """

        self.comment: str = ""
        self.created_by: str = ""
        self.imagery_used: str = ""
        self.source: str = ""
        self.locale: str = ""
        self.host: str = ""
        self.closed_note: str = ""

        self.bot: bool | None = None
        self.review_requested: bool | None = None
        self.ideditor_walkthrough_started: bool | None = None

        self.hashtags: Tuple[str, ...] = ()
        self.ideditor_walkthrough_progress: Tuple[str, ...] = ()

        self.changeset_count: int | None = None

        self.custom_tags: Dict[str, _json_types] = {}

        self._builder(json_response)

    def _builder(self, json_response: Dict[str, _json_types | Dict[str, _json_types]]) -> None:
        """
        Populate values from a json response
        :param json_response: The json response returned by API corresponding to a changeset
        :return: None
        """

        if not "tags" in json_response.items():
            return

        for key, value in json_response["tags"].items():
            match key:
                case "comment":
                    self.comment: str = value
                case "created_by":
                    self.created_by: str = value
                case "imagery_used":
                    self.imagery_used: str = value
                case "source":
                    self.source: str = value
                case "locale":
                    self.locale: str = value
                case "host":
                    self.host: str = value
                case "closed_note":
                    self.closed_note: str = value

                case "bot":
                    match value:
                        case "yes":
                            self.bot: bool = True

                        case "no":
                            self.bot: bool = False
                case "review_requested":
                    match value:
                        case "yes":
                            self.review_requested: bool = True

                        case "no":
                            self.review_requested: bool = False
                case "ideditor:walkthrough_started":
                    match value:
                        case "yes":
                            self.ideditor_walkthrough_started: bool = True

                        case "no":
                            self.ideditor_walkthrough_started: bool = False

                case "hashtags":
                    self.hashtags: Tuple[str, ...] = tuple(value.split(";"))
                case "ideditor:walkthrough_progress":
                    self.ideditor_walkthrough_progress: Tuple[str, ...] = tuple(value.split(";"))

                case "changesets_count":
                    self.changeset_count: int = int(value)

                case _:
                    self.custom_tags.update({key: value})

    def to_dict(self, remove_null_values: bool = False) -> (
            Dict[str, _json_types | Tuple[str, ...] | Dict[str, _json_types]]):

        """
        Return values as a dict
        :param remove_null_values: Set to true to remove null values from generated dict
        :return: The dict containing all values
        """

        to_return = {
            "comment": self.comment,
            "created_by": self.created_by,
            "imagery_used": self.imagery_used,
            "source": self.source,
            "locale": self.locale,
            "host": self.host,
            "closed_note": self.closed_note,
            "bot": self.bot,
            "review_requested": self.review_requested,
            "ideditor_walkthrough_started": self.ideditor_walkthrough_started,
            "hashtags": self.hashtags,
            "ideditor_walkthrough_progress": self.ideditor_walkthrough_progress,
            "changeset_count": self.changeset_count,
            "custom_tags": self.custom_tags,
        }

        if remove_null_values:
            to_rm = []
            for key, value in to_return.items():
                if value == "" or value is None or value == ():
                    to_rm.append(key)

            for i in to_rm:
                to_return.pop(i)

        return to_return

    def __str__(self) -> str:
        """
        Return values as a quasi json string
        :return: The quasi json string containing all values which aren't null
        """
        return f"<OSMChangesetTags: {json.dumps(self.to_dict(remove_null_values=True))}>"
