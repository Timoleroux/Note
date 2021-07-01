from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QWaitCondition, Qt
import os
import json
import default

PATH = "C:/Users/timol/OneDrive/Documents/GitHub/Note/TEST/dataTEST/dataTEST.json"

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note")
        self.setWindowIcon(QtGui.QIcon('C:/Users/timol/OneDrive/Documents/GitHub/Note/data/icon.ico'))
        self.component()
        self.css()
        self.load(True)

    def component(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.left_layout = QtWidgets.QVBoxLayout(self)
        self.right_layout = QtWidgets.QVBoxLayout(self)

        self.list_note = QtWidgets.QListWidget()
        self.btn_open = QtWidgets.QPushButton("Ouvir")
        self.btn_open.clicked.connect(self.note_open)
        self.btn_delete = QtWidgets.QPushButton("Supprimer")
        self.btn_delete.clicked.connect(self.note_remove)

        self.le_title = QtWidgets.QLineEdit()
        self.text_area = QtWidgets.QTextEdit()
        self.btn_save = QtWidgets.QPushButton("Sauvegarder")
        self.btn_save.clicked.connect(self.note_write)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.left_layout.addWidget(self.list_note)
        self.left_layout.addWidget(self.btn_open)
        self.left_layout.addWidget(self.btn_delete)
        self.right_layout.addWidget(self.le_title)
        self.right_layout.addWidget(self.text_area)
        self.right_layout.addWidget(self.btn_save)

    def css(self):
        self.setStyleSheet("""
        background-color: #ffffff;
        """)

    def load(self, is_load):  # load all elements in text_area at the starting (note_load)
        global json_dict

        with open(PATH, "r") as f:
            json_dict = json.load(f)
             
        if not json_dict or bool(json_dict) == False:  # if there isn't note, create the default note 
            with open(PATH, "w") as f:                 # and then update the json_dict
                json.dump(default.note, f, indent=4)
            with open(PATH, "r") as f:
                json_dict = json.load(f)

        if is_load == True:

            note_id = list(json_dict.keys())  # get note ID in a list
            note_id = int(note_id[0])

            for i in json_dict:  # add all the note in text_area
                if str(note_id) in json_dict:
                    self.list_note.addItem(json_dict[str(note_id)]["title"])
                note_id += 1

    def get_id_by_title(self, target_title):
        global note_id

        if target_title != "":

            self.load(False)
            goal = None
            note_id = 0

            while goal != target_title:

                if str(note_id) in json_dict:
                    goal = str(json_dict[str(note_id)]["title"])

                note_id += 1

        note_id -= 1
        note_id = str(note_id)

    def note_open(self):
        self.get_id_by_title(self.list_note.currentItem().text())
        self.le_title.setText(json_dict[note_id]["title"])
        self.text_area.setText(json_dict[note_id]["content"])

# --------------------------------------- HERE ! ---------------------------------------

    def note_write(self): 
        global note_exist
        self.load(False)
        
        def write(title, content):

            is_note_exist = False

            for i in json_dict:
                if title == json_dict[i]["title"]:
                    is_note_exist = True
                    self.list_note.addItem(str(self.le_title.text()))

            if is_note_exist == False:

                json_new = {"title":title, "content":content}
                self.get_nbr_next_note()
                json_dict.update({nbr_next_note:json_new})
                with open(PATH, "w") as f:
                    json.dump(json_dict, f, indent=4)
                
        text_title = str(self.le_title.text())
        text_content = str(self.text_area.toPlainText())
        self.json_write(text_title, text_content)

        if note_exist == False:
            
        elif note_exist == True:
            self.dict_locate(text_title)

    def note_remove(self):
        pass

    def write_in_json(self): 
        pass






    def _get_nbr_next_note(self):
        global nbr_next_note
        nbr_next_note = 0
        for i in json_dict:
            nbr_next_note += 1
        nbr_next_note = str(nbr_next_note)

    # def json_load(self):
    #     global json_dict
    #     with open(PATH, "r") as f:
    #         json_dict = json.load(f)
    #         is_empty = bool(json_dict)  # if json_dict is empty return False
    #     if not json_dict or is_empty == False:  # if json_dict is empty or don't exist
    #         with open(PATH, "w") as f:
    #             json.dump({"0":{"title":"How to use this app ?", "content":"It's a simply app of note. All notes are saves in a json file."}}, f, indent=4)

    #     with open(PATH, "r") as f:
    #         json_dict = json.load(f)

    def _json_write(self, title, content):
        self.json_load()
        global note_exist
        note_exist = False
        for i in json_dict:
            res = json_dict[i]["title"]
            if title == res:
                note_exist = True

        if note_exist == False:
            json_new = {"title":title, "content":content}
            self.get_nbr_next_note()
            json_dict.update({nbr_next_note:json_new})
            with open(PATH, "w") as f:
                json.dump(json_dict, f, indent=4)

    def _dict_locate(self, target): # get the ID of the note with only the title of the note
        if target != "":
            self.json_load()
            global note_id
            locate = None
            note_id = 0
            with open(PATH, "r") as f:
                json_dict = json.load(f)
            while locate != target:
                if str(note_id) in json_dict:
                    locate = str(json_dict[str(note_id)]["title"])
                note_id += 1
            note_id -= 1

    def _json_remove(self):
        self.json_load()
        self.dict_locate(self.list_note.currentItem().text())
        del json_dict[str(note_id)]
        with open(PATH, "w") as f:
                json.dump(json_dict, f, indent=4)

    # def note_load(self):
    #     self.json_load()
    #     first_key = list(json_dict.keys())
    #     first_key = str(first_key[0])
    #     v = int(first_key)
    #     for i in json_dict:
    #         if str(v) in json_dict:
    #             self.list_note.addItem(json_dict[str(v)]["title"])
    #         v += 1

    def _note_write(self):
            resT = str(self.le_title.text())
            resC = str(self.text_area.toPlainText())
            self.json_write(resT, resC)
            if note_exist == False:
                self.list_note.addItem(resT)
            elif note_exist == True:
                self.dict_locate(resT)

    def _note_remove(self):
        self.json_remove()
        list_items = self.list_note.selectedItems()
        for item in list_items:
            self.list_note.takeItem(self.list_note.row(item))

    # def _note_open(self):
    #     self.dict_locate(self.list_note.currentItem().text())
    #     self.le_title.setText(json_dict[str(note_id)]["title"])
    #     self.text_area.setText(json_dict[str(note_id)]["content"])



app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()