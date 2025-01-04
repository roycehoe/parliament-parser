PROMPT = """Your task is to read a parliament handsard document. After reading it, you are to attempt to create a JSON representation
of the data within the parliament handsard document. Your output JSON should look like this:

JSONOutput:
    parliament_no:
    sitting_no:
    volume_no:
    sitting_no:
    sitting_date:
    volume:

When you finish this representation, reply with a JSON and a JSON only of the created representation. Nothing more. Here is the Markdown file:
"""

import json
from openai import OpenAI

from markdown import get_handsard_lines


def get_handsard_metadata(openAI_client: OpenAI, file_path: str) -> dict:
    handsard_lines = get_handsard_lines(file_path)

    stream = openAI_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"{PROMPT}{handsard_lines}"}],
        response_format={"type": "json_object"},
        max_tokens=16384,
    )
    if gpt_completion := stream.choices[0].message.content:
        return json.loads(gpt_completion)
    raise Exception
