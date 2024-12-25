from enum import StrEnum, auto
from typing import Iterable


class Section(StrEnum):
    META = auto()
    ATTENDANCE = auto()
    TRANSCRIPT = auto()
    ANNEX = auto()


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


def is_start_of_annex(text: str) -> bool:
    return "Adjourned accordingly at" in text


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
        if is_start_of_annex(line):
            current_section = Section.ANNEX
        section_tags.append(current_section)

    return zip(lines, section_tags)


def get_section_tagged_handsard(handsard_lines_data: list[dict]):
    result = []
    section_tagged_handsard = get_section_tagged_lines(
        [handsard_line_data["text"] for handsard_line_data in handsard_lines_data]
    )
    for index, (_, section) in enumerate(section_tagged_handsard):
        result.append({**handsard_lines_data[index], "section": section})
    return result
