import re


def remove_html_spaces(original_text: str) -> str:
    return original_text.replace("&nbsp;", "")


def remove_spaces(original_text: str) -> str:
    return original_text.strip()


def remove_column_text(original_text: str) -> str:
    column_pattern = r"Column:\s*\d+"
    return re.sub(f"{column_pattern}", "", original_text)


def remove_page_text(original_text: str) -> str:
    page_text_pattern = r"Page:\s*\d+"
    return re.sub(f"{page_text_pattern}", "", original_text)
