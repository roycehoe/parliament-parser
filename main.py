import json
from openai import OpenAI
from dotenv import dotenv_values

from gpt_parser.attendance import get_mp_attendance
from gpt_parser.debate_line import get_debate_lines
from gpt_parser.debate_title import get_debate_titles
from gpt_parser.debate_title_lines import get_debate_title_lines
from gpt_parser.handsard_metadata import get_handsard_metadata
from gpt_parser.mps import get_mps

API_KEY = dotenv_values(".env").get("KEY")
client = OpenAI(api_key=API_KEY)


def main():
    # metadata = json.loads(get_handsard_metadata(client))
    # mps = json.loads(get_mps(client))

    # attendnace = json.loads(get_mp_attendance(client, mps))
    debate_titles = json.loads(get_debate_titles(client))
    # return debate_titles
    sample_title = debate_titles["debates"][0]["title"]
    debate_title_lines = json.loads(get_debate_title_lines(client, sample_title, debate_titles))

    # return {**metadata, **mps, **attendnace, **debate_without_speeches}
    # debate_without_speeches = json.loads(get_debate_without_speeches(client))

    # debate_lines = json.loads(get_debate_lines(client, debate_titles, mps))
    # return debate_lines
    return debate_title_lines


print(json.dumps(main()))
