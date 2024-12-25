import json

import html2text

from cleaining import (
    remove_column_text,
    remove_html_spaces,
    remove_page_text,
    remove_spaces,
)
from tagging.attendance import get_attendance_line_type, get_attendance_tagged_handsard
from tagging.section import Section, get_section_tagged_handsard
from tagging.speaker import get_speaker_tagged_handsard
from tagging.transcript import get_transcript_line_type, get_transcript_tagged_handsard

PATH = "test.json"


def get_parsed_handsard_data(path: str) -> list[str]:
    h = html2text.HTML2Text(bodywidth=0)
    with open(path) as file:
        parliament_data = json.load(file)
        parliament_html_full_content = parliament_data.get("htmlFullContent")
        parliament_html_full_content = remove_html_spaces(parliament_html_full_content)
        parliament_html_full_content = remove_column_text(parliament_html_full_content)
        parliament_html_full_content = remove_page_text(parliament_html_full_content)
    md_file = h.handle(parliament_html_full_content)
    return [remove_spaces(line) for line in md_file.split("\n")]


def get_line_number_to_handsard_data_index_base(
    parsed_handsard_data: list[str],
) -> dict[int, dict]:
    line_number_to_handsard_data_index = {}

    for index, text in enumerate(parsed_handsard_data):
        line_number_to_handsard_data_index[index] = {}
        line_number_to_handsard_data_index[index]["text"] = text
    return line_number_to_handsard_data_index


def main(path):
    parsed_handsard_data = get_parsed_handsard_data(path)
    handsard_index = get_line_number_to_handsard_data_index_base(parsed_handsard_data)
    handsard_index_with_section_tag = get_section_tagged_handsard(
        parsed_handsard_data, handsard_index
    )
    handsard_index_with_transcript_tag = get_transcript_tagged_handsard(
        parsed_handsard_data, handsard_index_with_section_tag
    )
    handsard_index_with_attendance_tag = get_attendance_tagged_handsard(
        parsed_handsard_data, handsard_index_with_transcript_tag
    )
    handsard_index_with_speaker_tag = get_speaker_tagged_handsard(
        parsed_handsard_data, handsard_index_with_attendance_tag
    )

    return handsard_index_with_speaker_tag


# print(json.dumps(main("./data/03-03-2005.json")))