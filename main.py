import json
import re

import html2text
from pydantic import BaseModel


def remove_spaces(original_text: str) -> str:
    return original_text.replace("&nbsp;", "")


def remove_column_text(original_text: str) -> str:
    pattern = r"<br><br><font size=\"1\"><b>Column: \d+</b></font><br><br>"
    return re.sub(pattern, "", original_text)


with open("data.json") as file:
    parliament_data = json.load(file)
    parliament_html_full_content = parliament_data.get("htmlFullContent")
    parliament_html_full_content = remove_spaces(parliament_html_full_content)
    parliament_html_full_content = remove_column_text(parliament_html_full_content)

h = html2text.HTML2Text()
print(h.handle(parliament_html_full_content))


"""
# Formatted MD rules

## Section: Oral answers

1. Everything after "#### ORAL ANSWERS TO QUESTIONS" will be part of the oral answers section
2. Each oral answer consists of a question and a list of answers
2. The start of each oral answer section is denoted by a space, a bolded all-caps header, another space, a sub-header, followed by three spaces



"""


# class Speech(BaseModel):
#     speaker: str
#     speech: str


# class Debate(BaseModel):
#     title: str
#     subtitle: str
#     question: Speech
#     oral_answers: list[Speech]
