import json
import os
import random

from constants import PARLIAMENT_SITTINGS, ParliamentSitting
import main

handsard_dates: list[str] = PARLIAMENT_SITTINGS.get(
    ParliamentSitting.LEGISLATIVE_ASSEMBLY_1955_TO_1965, []
)
sampled_handsard_date = random.choices(handsard_dates, k=5)

for index, date in enumerate(sampled_handsard_date):
    with open(f"./sample_output/{date}.json", "w") as f:
        json.dump(main.main(f"./data/{date}.json"), f)
