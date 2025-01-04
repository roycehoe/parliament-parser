PROMPT = """Your task is to read a parliament handsard document. After reading it, you are to attempt to create a JSON representation
of the data within the parliament handsard document. Your output JSON should look like this:

JSONOutput:
    start_line: 
    end_line: 

eg. {
    start_line: 12
    end_line: 18
}

Each debate will start with a debate title, and optionally, a debate subtitle. Following that would be the debate content. A debate ends when a new debate title, and optionally, a debate subtitle is encountered. Otherwise, a debate ends once the end of the document is reached.

With a given debate title, you are to determine the start line of the debate content and the end line of the debate content.

start_line:
    The starting line of the debate content
    
end_line:
    The ending line of the debate content

You are to give return the absolute line number of the start and end of the debate content. This includes any formatting in the document.
"""

from openai import OpenAI

from markdown import get_handsard_lines_with_line_markers


def _get_prompt(debate_title: dict, debate_titles: list[dict]):
    return f"""{PROMPT}


For context, here are all the debate titles: {debate_titles}

This is the debate title I would like you to extract data from: {debate_title}

When you finish this representation, reply with a JSON and a JSON only of the created representation. Nothing more. Here is the Markdown file:
"""


def get_debate_title_lines(
    openAI_client: OpenAI, debate_title: dict, debate_titles: list[dict]
) -> str:
    handsard_lines = get_handsard_lines_with_line_markers("./data/18-07-1957.json")

    stream = openAI_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"""
{_get_prompt(debate_title, debate_titles)}

```start_of_document
{handsard_lines}
```end_of_document""",
            }
        ],
        response_format={"type": "json_object"},
        max_tokens=16384,
    )
    if gpt_completion := stream.choices[0].message.content:
        return gpt_completion
    raise Exception
