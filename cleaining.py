import re


def remove_spaces(original_text: str) -> str:
    return original_text.replace("&nbsp;", "")


def remove_column_text(original_text: str) -> str:
    html_column_pattern = r"<br><br><font size=\"1\"><b>Column: \d+</b></font><br><br>"
    column_pattern = r"^Column: \d+"
    return re.sub(f"{html_column_pattern}{column_pattern}", "", original_text)
