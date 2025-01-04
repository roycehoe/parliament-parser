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


def get_non_debates_data():
    metadata = json.loads(get_handsard_metadata(client))
    mps = json.loads(get_mps(client))
    attendnace = json.loads(get_mp_attendance(client, mps))

    return {**metadata, **mps, **attendnace}


def get_debates():
    debates_with_titles = json.loads(get_debate_titles(client))
    debates: list[dict] = debates_with_titles["debates"]
    return debates


def main():
    return get_debates()


print(json.dumps(main()))
