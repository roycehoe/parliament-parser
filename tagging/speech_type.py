from enum import StrEnum, auto
import re
from typing import Iterable

from tagging.section import Section
from tagging.transcript import TranscriptLineType


class SpeechType(StrEnum):
    QUESTION = auto()
    ANSWER = auto()


def get_speech_type_tagged_handsard(handsard_lines_data: list[dict]):
    result = []

    current_topic = None
    questioner = None
    answered = False  # Has any speaker (other than the questioner) answered yet?

    for index in range(len(handsard_lines_data)):
        line_data = handsard_lines_data[index]

        # If line is not an actual speech line (eg: blank or something else), skip speech_type logic
        if (
            line_data["title"] is None
            or line_data["speaker"] is None
            or line_data["transcript_tag"]
            not in [
                TranscriptLineType.SPEECH,
                TranscriptLineType.CONTD_TEXT,
            ]
        ):
            result.append({**line_data, "speech_type": None})
            continue

        # --- Check if this is a new topic ---
        if line_data["title"] != current_topic:
            # New topic => new questioner
            current_topic = line_data["title"]
            questioner = line_data["speaker"]
            answered = False
            # The topic initiator is always QUESTION
            result.append({**line_data, "speech_type": SpeechType.QUESTION})
            continue

        # --- Same topic => apply the logic ---
        if line_data["speaker"] == questioner:
            # If no one else has answered yet, keep marking this as QUESTION
            if not answered:
                result.append({**line_data, "speech_type": SpeechType.QUESTION})
            else:
                # Once someone else has answered, the questioner is now effectively responding
                result.append({**line_data, "speech_type": SpeechType.ANSWER})
        else:
            # A different speaker from the questioner => always an ANSWER
            answered = True  # Mark that an answer has occurred
            result.append({**line_data, "speech_type": SpeechType.ANSWER})

    return result
