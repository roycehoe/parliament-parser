import json

import html2text

from cleaining import remove_column_text, remove_spaces
from tagging.attendance import get_attendance_line_type
from tagging.section import Section, get_section_tagged_handsard
from tagging.transcript import get_transcript_line_type

PATH = "test.json"


def get_parsed_handsard_data(path: str) -> list[str]:
    h = html2text.HTML2Text(bodywidth=0)
    with open(path) as file:
        parliament_data = json.load(file)
        parliament_html_full_content = parliament_data.get("htmlFullContent")
        parliament_html_full_content = remove_spaces(parliament_html_full_content)
        parliament_html_full_content = remove_column_text(parliament_html_full_content)
    md_file = h.handle(parliament_html_full_content)
    return md_file.split("\n")


def main(path):
    parsed_handsard_data = get_parsed_handsard_data(path)
    section_tagged_handsard = get_section_tagged_handsard(parsed_handsard_data)
    line_number_to_handsard_data_index = {}

    for index, text in enumerate(parsed_handsard_data):
        line_number_to_handsard_data_index[index] = {}
        line_number_to_handsard_data_index[index]["text"] = text

    for index, (_, section) in enumerate(section_tagged_handsard):
        line_number_to_handsard_data_index[index]["section"] = section

    for index, text in enumerate(parsed_handsard_data):
        line_number_to_handsard_data_index[index]["attendance_type"] = (
            get_attendance_line_type(text)
            if line_number_to_handsard_data_index[index]["section"]
            == Section.ATTENDANCE
            else None
        )

    for index, text in enumerate(parsed_handsard_data):
        line_number_to_handsard_data_index[index]["transcript_type"] = (
            get_transcript_line_type(text)
            if line_number_to_handsard_data_index[index]["section"]
            == Section.TRANSCRIPT
            else None
        )
    return line_number_to_handsard_data_index


print(json.dumps(main("./data/03-03-2005.json")))
