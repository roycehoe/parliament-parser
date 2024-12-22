import re


def is_oral_answer_title(text: str) -> bool:
    pattern = r"\*\*[A-Z\s]+\*\*"
    return bool(re.search(pattern, text))


oral_answer_start_lines = []
oral_answer_end_lines = []
with open("oral_answers.md") as file:
    for line_number, line_text in enumerate(file):
        if not is_oral_answer_title(line_text):
            continue
        oral_answer_start_lines.append(line_number)

for i in oral_answer_start_lines[1:]:
    oral_answer_end_lines.append(i - 1)
oral_answer_end_lines.append(len(oral_answer_start_lines))

print(list(zip(oral_answer_start_lines, oral_answer_end_lines)))