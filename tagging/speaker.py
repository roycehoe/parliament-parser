import re
from typing import Iterable

from tagging.section import Section


def get_speaker_tagged_lines(
    handsard_data: list[str],
) -> Iterable[tuple[str, str | None]]:
    speaker_tags: list[str | None] = []
    bold_pattern = r"^\*\*(\w.*?)\*\*"
    current_speaker = None

    for line in handsard_data:
        match = re.findall(bold_pattern, line)
        if match:
            # Check if the line consists exclusively of bolded text
            if line.strip() == f"**{match[0]}**":
                current_speaker = None
            else:
                # Remove trailing colon if it exists
                current_speaker = match[0].rstrip(":")
        speaker_tags.append(current_speaker)

    return zip(handsard_data, speaker_tags)


def get_speaker_tagged_handsard(handsard_lines_data: list[dict]):
    result = []
    speaker_tagged_lines = get_speaker_tagged_lines(
        [handsard_line_data["text"] for handsard_line_data in handsard_lines_data]
    )
    for index, (_, spekaer) in enumerate(speaker_tagged_lines):
        if handsard_lines_data[index]["section"] != Section.TRANSCRIPT:
            result.append({**handsard_lines_data[index], "speaker": None})
            continue
        result.append({**handsard_lines_data[index], "speaker": spekaer})

    return result
