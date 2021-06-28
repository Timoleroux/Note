import json

PATH = "C:/Users/timol/OneDrive/Documents/GitHub/Note/data/data.json"

def add_note_json(content):
    with open(PATH, "w") as f:
        json.dump(content, f, indent=4)

with open(PATH, "r") as f:
    the_list = json.load(f)
    # for i in the_list:
    #     res = the_list

