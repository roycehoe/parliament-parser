PROMPT = """Your task is to read a parliament handsard document. After reading it, you are to attempt to create a JSON representation
of all the data within the parliament handsard document. Your output JSON should look like this:

JSONOutput:
    parliament_no:
    sitting_no:
    volume_no:
    sitting_no:
    sitting_date:
    volume:
    attendance: Attendance
    debates: list[Debate]

MP:
    name:
    role:

Attendance:
    present: list[MP]
    absent: list[MP]

Speech:
    speaker_name: MP
    is_question:
    speech:


Debate:
    topic:
    speeches: Speech


When you finish this representation, reply with a JSON and a JSON only of the created representation. Nothing more. Here is the Markdown file:
"""

from openai import OpenAI
from dotenv import dotenv_values

from main import get_handsard_lines

API_KEY = dotenv_values(".env").get("KEY")


client = OpenAI(api_key=API_KEY)
test = get_handsard_lines("./data/18-07-1957.json")

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": f"{PROMPT}{test}"}],
    max_tokens=16384,
)
print(stream.choices[0].message.content)
