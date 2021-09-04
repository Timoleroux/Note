import json
PATH = "C:/Users/timol/OneDrive/Documents/GitHub/Note/data/data.json"

def dictNotes():
    with open(PATH, "r") as f:
        return json.load(f)

def getIdWithTitle(target_title):

    with open(PATH, "r") as f:
        json_dict = json.load(f)

    if target_title != "":
        goal = None
        note_id = 0

        while goal != target_title:
            if str(note_id) in json_dict:
                goal = str(json_dict[str(note_id)]["title"])
            note_id += 1
    else:
        return

    note_id -= 1
    return str(note_id)

def createNote(note_id, note_title, note_content):
    json_dict = dictNotes()
    new_note = {note_id:{"title":note_title, "content":note_content}}
    json_dict.update(new_note)
    with open(PATH, "w") as f:
        json.dump(json_dict, f, indent=4)

def updateNote(note_id, note_title, note_content):
    dict_notes = dictNotes()
    dict_notes.update({note_id:{"title":note_title, "content":note_content}})
    with open(PATH, "w") as f:
        json.dump(dict_notes, f, indent=4)

def deleteNote(item):
    dict_notes = dictNotes()
    del dict_notes[getIdWithTitle(item)]
    with open(PATH, "w") as f:
        json.dump(dict_notes, f, indent=4)  # update the json file