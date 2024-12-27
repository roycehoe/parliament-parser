import re
from typing import Iterable

from tagging.section import Section


def get_speaker_tagged_lines(
    handsard_lines_data: list[dict],
) -> Iterable[tuple[str, str | None]]:
    speaker_tags: list[str | None] = []
    bold_pattern = r"^\*\*(\w.*?)\*\*"
    current_speaker = None

    handsard_lines = [
        handsard_line_data["raw_text"] for handsard_line_data in handsard_lines_data
    ]
    handsard_section = [
        handsard_line_data["section"] for handsard_line_data in handsard_lines_data
    ]

    for line, section in zip(handsard_lines, handsard_section):
        if section != Section.TRANSCRIPT:
            speaker_tags.append(None)
            continue
        match = re.match(bold_pattern, line)
        if match:
            # Check if the line consists exclusively of bolded text
            if line.strip() == f"**{match[0]}**":
                current_speaker = None
            else:
                # Remove trailing colon if it exists
                current_speaker = match[0].rstrip(":")
        speaker_tags.append(current_speaker)

    return zip(handsard_lines, speaker_tags)


def get_speaker_tagged_handsard(handsard_lines_data: list[dict]):
    result = []
    speaker_tagged_lines = get_speaker_tagged_lines(handsard_lines_data)
    for index, (_, spekaer) in enumerate(speaker_tagged_lines):
        if handsard_lines_data[index]["section"] != Section.TRANSCRIPT:
            result.append({**handsard_lines_data[index], "speaker": None})
            continue
        result.append({**handsard_lines_data[index], "speaker": spekaer})

    return result
