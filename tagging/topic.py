from enum import StrEnum, auto
import re
from typing import Iterable

from pydantic import NonNegativeFloat

from tagging.section import Section
from tagging.transcript import TranscriptLineType


def get_topic_tagged_handsard(handsard_line_data: list[dict]):
    title = None
    subtitle = None

    result = []
    for index in range(len(handsard_line_data)):
        if handsard_line_data[index]["transcript_tag"] == TranscriptLineType.TITLE:
            title = handsard_line_data[index]["raw_text"]
            subtitle = None
            continue
        if handsard_line_data[index]["transcript_tag"] == TranscriptLineType.SUBTITLE:
            subtitle = handsard_line_data[index]["raw_text"]
            continue

        result.append(
            {
                **handsard_line_data[index],
                "title": (
                    title
                    if handsard_line_data[index]["section"] == Section.TRANSCRIPT
                    else None
                ),
                "subtitle": (
                    subtitle
                    if handsard_line_data[index]["section"] == Section.TRANSCRIPT
                    else None
                ),
            }
        )
    return result
