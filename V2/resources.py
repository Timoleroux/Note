default_note = {"0":{"title":"How to use this app ?", "content":"It's a simply app of note. All notes are saves in a json file."}}
default_new_note = {"title":"New note", "content":"This is my new note."}


def LOG(content):
    print(content)

def _countChar(text):
    res = 0
    text = str(text)
    if not text:
        return False
    else:
        for i in text:
            res += 1
        LOG(res)
    return res
