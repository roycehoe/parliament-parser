import json
from openai import OpenAI
from dotenv import dotenv_values

from gpt_parser.attendance import get_mp_attendance
from gpt_parser.debates import get_debates
from gpt_parser.handsard_metadata import get_handsard_metadata
from gpt_parser.mps import get_mps

API_KEY = dotenv_values(".env").get("KEY")
client = OpenAI(api_key=API_KEY)
FILE_PATH = "./data/18-07-1957.json"


def get_non_debates_data():
    metadata = get_handsard_metadata(client, FILE_PATH)
    mps = get_mps(client, FILE_PATH)
    attendnace = get_mp_attendance(client, mps, FILE_PATH)

    return {**metadata, **mps, **attendnace}


def get_debates_data():
    debates_with_titles = get_debates(client, FILE_PATH)
    debates: list[dict] = debates_with_titles["debates"]
    return debates


def main():
    return get_non_debates_data()


print(json.dumps(main()))
