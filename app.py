from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QWaitCondition, Qt
import os
import json
from resources import default_note, default_new_note
from resources import count_char    

PATH = "C:/Users/timol/OneDrive/Documents/GitHub/Note/data/data.json"

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note")
        self.setMinimumSize(550, 300)
        self.setMaximumSize(825, 450)
        self.setWindowIcon(QtGui.QIcon('C:/Users/timol/OneDrive/Documents/GitHub/Note/data/icon.ico'))
        self.component()
        self.load(True)

    def component(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.left_layout = QtWidgets.QVBoxLayout(self)
        self.right_layout = QtWidgets.QVBoxLayout(self)

        self.list_note = QtWidgets.QListWidget()
        self.list_note.itemClicked.connect(self.note_open)
        self.btn_delete = QtWidgets.QPushButton("Supprimer")
        self.btn_delete.clicked.connect(self.note_remove)
        self.label_title = QtWidgets.QLabel("Title:")
        self.le_title = QtWidgets.QLineEdit()
        self.le_title.textChanged.connect(self.note_save)
        self.le_title.setMaxLength(35)
        self.le_title.setDisabled(True)
        self.label_content = QtWidgets.QLabel("Content:")
        self.text_area = QtWidgets.QTextEdit()
        self.text_area.textChanged.connect(self.note_save)
        self.text_area.setDisabled(True)
        self.btn_save = QtWidgets.QPushButton("Nouveau")
        self.btn_save.clicked.connect(self.note_write)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.left_layout.addWidget(self.list_note)
        self.left_layout.addWidget(self.btn_save)
        self.left_layout.addWidget(self.btn_delete)
        self.right_layout.addWidget(self.label_title)
        self.right_layout.addWidget(self.le_title)
        self.right_layout.addWidget(self.label_content)
        self.right_layout.addWidget(self.text_area)

    def load(self, is_load):  # load all elements in text_area at the starting (note_load)
        global json_dict

        with open(PATH, "r") as f:
            json_dict = json.load(f)
             
        if not json_dict or bool(json_dict) == False:  # if there isn't note, create the default note 
            with open(PATH, "w") as f:                 # and then update the json_dict
                json.dump(default_note, f, indent=4)
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
        global disable_save_func
        self.le_title.setDisabled(False)
        self.text_area.setDisabled(False)
        disable_save_func = True
        self.get_id_by_title(self.list_note.currentItem().text())
        self.le_title.setText(json_dict[note_id]["title"])
        self.text_area.setText(json_dict[note_id]["content"])
        disable_save_func = False
        

    def note_write(self):
        self.load(False)
        
        json_keys_list = list(json_dict.keys()) # get all the ID of the notes
        id_new_note = json_keys_list[-1]  # get the last ID
        id_new_note = int(id_new_note)
        id_new_note += 1  # get the next ID 

        json_dict.update({id_new_note:default_new_note})  # add the new note the json_dict

        with open(PATH, "w") as f:
            json.dump(json_dict, f, indent=4)  # add the note in the json file
               
        self.list_note.addItem(default_new_note["title"]) # add the title in the list_note
         
        new_content = self.text_area.toPlainText()
        json_dict.update({note_id:{"title":self.le_title.text(), "content":new_content}})

        with open(PATH, "w") as f:
            json.dump(json_dict, f, indent=4)


    def note_save(self):
        new_title = self.le_title.text()
        new_content = self.text_area.toPlainText()
        
        if count_char(new_title) >= 1 and disable_save_func == False:
            self.load(False)
            json_dict.update({note_id:{"title":new_title, "content":new_content}})

            with open(PATH, "w") as f:
                json.dump(json_dict, f, indent=4)

            self.list_note.clear()
            self.load(True)

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