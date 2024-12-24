import json
import os
import random

import main

path = "./data"
dir_list = os.listdir(path)
sampled_handsard_date = random.choices(dir_list, k=5)

for index, date in enumerate(sampled_handsard_date):
    with open(f"./sample_output/{date}", "w") as f:
        json.dump(main.main(f"./data/{date}"), f)
