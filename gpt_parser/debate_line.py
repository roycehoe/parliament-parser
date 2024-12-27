PROMPT = """Your task is to read a parliament handsard document. After reading it, you are to attempt to create a JSON representation
of the data within the parliament handsard document. Your output JSON should follow this structure:

JSONOutput:
    line_number: Debate

Debate:
    debate_title:
    MP: MP
    is_question: // boolean

eg. {
    "1": {"debate_title": "title", MP: "name", is_question: False}
    "2": {"debate_title": "title", MP: "name", is_question: False}
}


Do take note of the following rules:
1. The line number represents the zero indexed line number within the handsard document.
2. You are to look through the document sequentially. Once a debate has started, it is assumed that all preceeding lines are part of the same debate unless a new debate has started.
3. You will be provided with a list of debate titles. You can only classify debate titles based on this list of debate titles. 
4. With reference to [4], note that not all lines are part of a debate (for example, the attendance list at the beginning of the document is not a debate). If so, mark the debate_title as null.
5. You will be provided with a list of MP objects. You can only classify MPs based on this list of MP objects. 
6. With reference to [5], note that not all lines have a speaker (for example, the attendance list at the beginning of the document is not a debate). If so, mark the speaker as null.
7. A question is defined as the lines preceeding a debate title, made by the same speaker. Note that a question may span multiple lines. If so, all of the said lines are considered a question. Mark is_question as true if it fulfils this condition.
8. Every line must be labeled.

"""

from openai import OpenAI

from markdown import get_handsard_lines


def _get_prompt(debate_titles, mps):
    return f"""{PROMPT}

```debate_titles
{debate_titles}
```

```mps
{mps}
```

When you finish this representation, reply with a JSON and a JSON only of the created representation. Nothing more. Here is the Markdown file:
"""


def get_debate_lines(openAI_client: OpenAI, debate_titles, mps) -> str:
    handsard_lines = get_handsard_lines("./data/18-07-1957.json")

    stream = openAI_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"{_get_prompt(debate_titles, mps)}{handsard_lines}",
            }
        ],
        response_format={"type": "json_object"},
        max_tokens=16384,
    )
    if gpt_completion := stream.choices[0].message.content:
        return gpt_completion
    raise Exception
