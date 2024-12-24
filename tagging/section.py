from enum import StrEnum, auto


class Section(StrEnum):
    META = auto()
    ATTENDANCE = auto()
    TRANSCRIPT = auto()


def is_start_of_attendance(text: str) -> bool:
    return text == "PRESENT:   "


def is_start_of_transcript(text: str) -> bool:
    return text == "#### [Mr Speaker in the Chair]"


def get_next_section(section: Section) -> Section:
    if section == Section.META:
        return Section.ATTENDANCE
    return Section.TRANSCRIPT


def get_section_tagged_handsard(handsard_data: list[str]) -> zip[tuple[str, Section]]:
    section_tags: list[Section] = []

    current_section = Section.META
    for line in handsard_data:
        if is_start_of_attendance(line):
            current_section = Section.ATTENDANCE
        if is_start_of_transcript(line):
            current_section = Section.TRANSCRIPT
        section_tags.append(current_section)

    return zip(handsard_data, section_tags)
