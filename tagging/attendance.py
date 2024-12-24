from enum import StrEnum, auto


def is_blank_line(text: str) -> bool:
    return text.strip() == ""


def is_present_marker(text: str) -> bool:
    return text == "PRESENT:   "


def is_absent_header(text: str) -> bool:
    return text == "ABSENT:   "


def is_line_break(text: str) -> bool:
    return text == "* * *"


def is_absent_permission_header(text: str) -> bool:
    return text == "#### PERMISSION TO MEMBERS TO BE ABSENT"


def is_assent_to_bills_passed_header(text: str) -> bool:
    return text == "**ASSENT TO BILLS PASSED**"


class AttendanceLineType(StrEnum):
    BLANK = auto()
    LINE_BREAK = auto()
    PRESENT_HEADER = auto()
    ABSENT_HEADER = auto()
    ABSENT_PERMISSION_HEADER = auto()
    ASSENT_TO_BILLS_PASSED_HEADER = auto()
    TEXT = auto()


def get_attendance_line_type(text: str) -> AttendanceLineType:
    if is_blank_line(text):
        return AttendanceLineType.BLANK
    if is_line_break(text):
        return AttendanceLineType.LINE_BREAK
    if is_present_marker(text):
        return AttendanceLineType.PRESENT_HEADER
    if is_absent_header(text):
        return AttendanceLineType.ABSENT_HEADER
    if is_absent_permission_header(text):
        return AttendanceLineType.ABSENT_PERMISSION_HEADER
    if is_assent_to_bills_passed_header(text):
        return AttendanceLineType.ASSENT_TO_BILLS_PASSED_HEADER
    return AttendanceLineType.TEXT


def get_attendance_tagged_data(
    handsard_attendance_data: list[str],
) -> zip[tuple[str, AttendanceLineType]]:
    attendance_tags: list[AttendanceLineType] = [
        get_attendance_line_type(line) for line in handsard_attendance_data
    ]
    return zip(handsard_attendance_data, attendance_tags)
