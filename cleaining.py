import re


def remove_spaces(original_text: str) -> str:
    return original_text.replace("&nbsp;", "")


def remove_column_text(original_text: str) -> str:
    pattern = r"<br><br><font size=\"1\"><b>Column: \d+</b></font><br><br>"
    return re.sub(pattern, "", original_text)
