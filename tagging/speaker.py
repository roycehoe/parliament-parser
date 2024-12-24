import re
from typing import Iterable

from tagging.section import Section


def get_speaker_tagged_lines(
    handsard_data: list[str],
) -> Iterable[tuple[str, str | None]]:
    speaker_tags: list[str | None] = []
    bold_pattern = r"\*\*(.*?)\*\*"
    current_speaker = None

    for line in handsard_data:
        match = re.findall(bold_pattern, line)
        if match:
            current_speaker = match[0]
        speaker_tags.append(current_speaker)

    return zip(handsard_data, speaker_tags)


def get_speaker_tagged_handsard(
    parsed_handsard_data, line_number_to_handsard_data_index
):
    result = {}
    speaker_tagged_lines = get_speaker_tagged_lines(parsed_handsard_data)
    for index, (_, speaker) in enumerate(speaker_tagged_lines):
        result[index] = {
            **line_number_to_handsard_data_index[index],
            "speaker": (
                speaker
                if line_number_to_handsard_data_index[index]["section"]
                == Section.TRANSCRIPT
                else None
            ),
        }
    return result
