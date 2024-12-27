PROMPT = """Your task is to read a parliament handsard document. After reading it, you are to attempt to create a JSON representation
of the data within the parliament handsard document. Your output JSON should look like this:

JSONOutput:
    debates: list[Debate]

Debate:
    title:
    subtitle: // An optional field. Nil if empty. Typically a bolded and/or bracketed section after the title

Do note that the phrase "ORAL ANSWER TO QUESTION" denotes the start of the debate section of the document. You are to disregard all titles and subtitles before this marker. The phrase itself is not a debate title

When you finish this representation, reply with a JSON and a JSON only of the created representation. Nothing more. Here is the Markdown file:
"""

from openai import OpenAI

from markdown import get_handsard_lines


def get_debate_titles(openAI_client: OpenAI) -> str:
    handsard_lines = get_handsard_lines("./data/18-07-1957.json")

    stream = openAI_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"{PROMPT}{handsard_lines}"}],
        response_format={"type": "json_object"},
        max_tokens=16384,
    )
    if gpt_completion := stream.choices[0].message.content:
        return gpt_completion
    raise Exception
