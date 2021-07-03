default_note = {"0":{"title":"How to use this app ?", "content":"It's a simply app of note. All notes are saves in a json file."}}
default_new_note = {"title":"New note", "content":"This is my new note."}


def count_char(text):
    res = 0
    text = str(text)
    if not text:
        return False
    else:
        for i in text:
            res += 1
    return res