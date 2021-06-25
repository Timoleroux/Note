import json
import os

CUR_DIR = "C:/Users/timol/OneDrive/Documents/GitHub/Note/data/data.json"
DATA_FILE = os.path.join(CUR_DIR)


def get_movies():
    with open(DATA_FILE, "a") as f:
        json.dump("ccc", f, indent=4)

get_movies()