import json

import html2text

from cleaining import (
    remove_column_text,
    remove_html_spaces,
    remove_page_text,
    remove_spaces,
)


def get_handsard_lines(path: str) -> list[str]:
    h = html2text.HTML2Text(bodywidth=0)
    with open(path) as file:
        parliament_data = json.load(file)
        parliament_html_full_content = parliament_data.get("htmlFullContent")
        parliament_html_full_content = remove_html_spaces(parliament_html_full_content)
        parliament_html_full_content = remove_column_text(parliament_html_full_content)
        parliament_html_full_content = remove_page_text(parliament_html_full_content)
    md_file = h.handle(parliament_html_full_content)
    return [remove_spaces(line) for line in md_file.split("\n")]
