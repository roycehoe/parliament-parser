from enum import StrEnum, auto
import json

import html2text
from pydantic import BaseModel

from cleaining import remove_column_text, remove_spaces
from tagging.attendance import get_attendance_line_type
from tagging.transcript import get_transcript_line_type


class Section(StrEnum):
    META = auto()
    ATTENDANCE = auto()
    TRANSCRIPT = auto()


def is_start_of_attendance(text: str) -> bool:
    return text == "PRESENT:   "


def is_start_of_transcript(text: str) -> bool:
    return text == "#### [Mr Speaker in the Chair]"


def get_parsed_handsard_data(path: str) -> list[str]:
    h = html2text.HTML2Text(bodywidth=0)
    with open(path) as file:
        parliament_data = json.load(file)
        parliament_html_full_content = parliament_data.get("htmlFullContent")
        parliament_html_full_content = remove_spaces(parliament_html_full_content)
        parliament_html_full_content = remove_column_text(parliament_html_full_content)
    md_file = h.handle(parliament_html_full_content)
    print(md_file)
    return md_file.split("\n")


parsed_handsard_data = get_parsed_handsard_data("test.json")
line_number_to_handsard_data_index = {}

current_section = Section.META
for index, text in enumerate(parsed_handsard_data):
    line_number_to_handsard_data_index[index] = {}

for index, text in enumerate(parsed_handsard_data):
    if is_start_of_attendance(text):
        current_section = Section.ATTENDANCE
    if is_start_of_transcript(text):
        current_section = Section.TRANSCRIPT
    line_number_to_handsard_data_index[index]["section"] = current_section
    line_number_to_handsard_data_index[index]["line_number"] = index
    line_number_to_handsard_data_index[index]["content"] = text

for line_number, handsard_data in line_number_to_handsard_data_index.items():
    if handsard_data["section"] == Section.TRANSCRIPT:
        handsard_data["content_type"] = get_transcript_line_type(
            handsard_data["content"]
        )
        continue
    if handsard_data["section"] == Section.ATTENDANCE:
        handsard_data["content_type"] = get_attendance_line_type(
            handsard_data["content"]
        )
        continue

    handsard_data["content_type"] = None


print(json.dumps(line_number_to_handsard_data_index))


# class Speech(BaseModel):
#     speaker: str
#     speech: str


# class Debate(BaseModel):
#     title: str
#     subtitle: str
#     question: Speech
#     oral_answers: list[Speech]
