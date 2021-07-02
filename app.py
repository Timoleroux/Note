from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QWaitCondition, Qt
import os
import json
import default

PATH = "C:/Users/timol/OneDrive/Documents/GitHub/Note/data/data.json"

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
        self.list_note.itemClicked.connect(self.note_open)
        self.btn_delete = QtWidgets.QPushButton("Supprimer")
        self.btn_delete.clicked.connect(self.note_remove)

        self.le_title = QtWidgets.QLineEdit()
        self.text_area = QtWidgets.QTextEdit()
        self.text_area.textChanged.connect(self.note_save)
        self.btn_save = QtWidgets.QPushButton("Nouveau")
        self.btn_save.clicked.connect(self.note_write)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.left_layout.addWidget(self.list_note)
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

    def note_write(self):
        self.load(False)
        
        def write(title, content):

            is_note_exist = False

            for i in json_dict:  # set if the existing of the note
                if title == json_dict[i]["title"]:
                    is_note_exist = True

            if is_note_exist == False and self.le_title.text():  # if the note don't exist and 
                                                                 # the title isn't empty: create it
                json_keys_list = list(json_dict.keys()) # get all the ID of the notes
                id_new_note = json_keys_list[-1]  # get the last ID
                id_new_note = int(id_new_note)
                id_new_note += 1  # get the next ID 
                new_note = {"title":title, "content":content}  # set the new note

                json_dict.update({id_new_note:new_note})  # add the note the json_dict

                with open(PATH, "w") as f:
                    json.dump(json_dict, f, indent=4)  # add the note in the json file
                
                self.list_note.addItem(title) # add the title in the list_note
            
            elif is_note_exist == True:
                self.get_id_by_title(self.le_title.text())
                new_content = self.text_area.toPlainText()
                json_dict.update({note_id:{"title":self.le_title.text(), "content":new_content}})

                with open(PATH, "w") as f:
                    json.dump(json_dict, f, indent=4)

            text_title = str(self.le_title.text())  # get the title for the write function  
            text_content = str(self.text_area.toPlainText())  # get the content for the write function
            write(text_title, text_content)

    def note_save(self):
        self.get_id_by_title(self.le_title.text())
        new_title = self.le_title.text()
        new_content = self.text_area.toPlainText()
        json_dict.update({note_id:{"title":new_title, "content":new_content}})

        with open(PATH, "w") as f:
            json.dump(json_dict, f, indent=4)


    def note_remove(self):
        self.load(False)
        self.get_id_by_title(self.list_note.currentItem().text())

        del json_dict[note_id]  # delete the note
        with open(PATH, "w") as f:
                json.dump(json_dict, f, indent=4)  # update the json file

        list_items = self.list_note.selectedItems()
        for item in list_items:
            self.list_note.takeItem(self.list_note.row(item))  # remove the note title in the list_note

app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()