from enum import StrEnum, auto
from typing import Iterable


class Section(StrEnum):
    META = auto()
    ATTENDANCE = auto()
    TRANSCRIPT = auto()


def is_start_of_attendance(text: str) -> bool:
    return "PRESENT:" in text


def is_start_of_transcript(text: str) -> bool:
    return (
        "ORAL ANSWER TO QUESTION" in text
        or "ORAL ANSWERS TO QUESTIONS" in text
        or "[MR SPEAKER IN THE CHAIR]" in text
        or "[Mr Speaker in the Chair]" in text
        or "PRESIDENT'S ADDRESS" in text
    )


def get_next_section(section: Section) -> Section:
    if section == Section.META:
        return Section.ATTENDANCE
    return Section.TRANSCRIPT


def get_section_tagged_lines(
    lines: list[str],
) -> Iterable[tuple[str, Section]]:
    section_tags: list[Section] = []

    current_section = Section.META
    for line in lines:
        if is_start_of_attendance(line):
            current_section = Section.ATTENDANCE
        if is_start_of_transcript(line):
            current_section = Section.TRANSCRIPT
        section_tags.append(current_section)

    return zip(lines, section_tags)


def get_section_tagged_handsard(
    parsed_handsard_data, line_number_to_handsard_data_index
):
    result = {}
    section_tagged_handsard = get_section_tagged_lines(parsed_handsard_data)
    for index, (_, section) in enumerate(section_tagged_handsard):
        result[index] = {
            **line_number_to_handsard_data_index[index],
            "section": section,
        }
    return result
