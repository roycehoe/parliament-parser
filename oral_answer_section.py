from enum import Enum, auto
import re


def is_oral_answer_title(text: str) -> bool:
    pattern = r"\*\*[A-Z\s]+\*\*"
    return bool(re.search(pattern, text))


def is_oral_answer_subtitle(text: str) -> bool:
    pattern = r"(?m)^\*\*(?=.*[a-z])[^*]+\*\*$"
    return bool(re.search(pattern, text))


def is_question(text: str) -> bool:
    return text[0].isnumeric()


def is_answer(text: str) -> bool:
    return text[:2] == "**"


def is_blank_line(text: str) -> bool:
    return text.strip() == ""


class OralAnswerLineType(Enum):
    TITLE = auto()
    SUBTITLE = auto()
    BLANK = auto()
    QUESTION = auto()
    ANSWER = auto()
    CONTD_TEXT = auto()


def get_oral_answer_line_type(text: str) -> OralAnswerLineType:
    if is_blank_line(text):
        return OralAnswerLineType.BLANK
    if is_oral_answer_title(text):
        return OralAnswerLineType.TITLE
    if is_oral_answer_subtitle(text):
        return OralAnswerLineType.SUBTITLE
    if is_question(text):
        return OralAnswerLineType.QUESTION
    if is_answer(text):
        return OralAnswerLineType.ANSWER
    return OralAnswerLineType.CONTD_TEXT


line_label_mapping = {}


with open("oral_answer_section.md") as file:
    for i, t in enumerate(file):
        line_label_mapping[i] = get_oral_answer_line_type(t)


print(line_label_mapping)
