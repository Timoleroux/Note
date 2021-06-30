from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QWaitCondition, Qt
import os
import json

PATH = "C:/Users/timol/OneDrive/Documents/GitHub/Note/TEST/dataTEST/dataTEST.json"

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note")
        self.setWindowIcon(QtGui.QIcon('C:/Users/timol/OneDrive/Documents/GitHub/Note/data/icon.ico'))
        self.component()
        self.css()
        self.note_load()

    def component(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.left_layout = QtWidgets.QVBoxLayout(self)
        self.right_layout = QtWidgets.QVBoxLayout(self)
        self.title = QtWidgets.QLineEdit()
        self.text_area = QtWidgets.QTextEdit()
        self.save = QtWidgets.QPushButton("Sauvegarder")
        self.save.clicked.connect(self.note_write)
        self.delete = QtWidgets.QPushButton("Supprimer")
        self.delete.clicked.connect(self.note_remove)
        self.note_list = QtWidgets.QListWidget()

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.right_layout.addWidget(self.title)
        self.right_layout.addWidget(self.text_area)
        self.right_layout.addWidget(self.save)


        self.left_layout.addWidget(self.note_list)
        self.left_layout.addWidget(self.delete)

    def css(self):
        self.setStyleSheet("""
        background-color: #ffffff;
        """)

    def get_nbr_next_note(self):
        global nbr_next_note
        nbr_next_note = 0
        for i in json_dict:
            nbr_next_note += 1
        nbr_next_note = str(nbr_next_note)

    def json_load(self):
        global json_dict
        try:
            with open(PATH, "r") as f:
                json_dict = json.load(f)
            if not json_dict:
                with open(PATH, "w") as f:
                    json.dump({"0":{"title":"How to use this app ?", "content":"It's a simply app of note. All notes are saves in a json file."}}, f, indent=4)
        except:
            with open(PATH, "w") as f:
                json.dump({"0":{"title":"How to use this app ?", "content":"It's a simply app of note. All notes are saves in a json file."}}, f, indent=4)
            with open(PATH, "r") as f:
                json_dict = json.load(f)

    def json_write(self, title, content):
        self.json_load()
        json_new = {"title":title, "content":content}
        self.get_nbr_next_note()
        json_dict.update({nbr_next_note:json_new})
        with open(PATH, "w") as f:
            json.dump(json_dict, f, indent=4)

    def dict_locate(self, target):
        self.json_load()
        global target_number
        locate = None
        target_number = 0
        with open(PATH, "r") as f:
            json_dict = json.load(f)
        while locate != target:
            print(type(target))
            print(type(json_dict))
            locate = json_dict[str(target_number)]["title"] # ERROR : why ?
            target_number += 1
        target_number -= 1
        print(target_number)

    def json_remove(self):
        self.json_load()
        self.dict_locate(self.note_list.currentItem().text())
        del json_dict[str(target_number)]
        with open(PATH, "w") as f:
                json.dump(json_dict, f, indent=4)

    def note_load(self):
        self.json_load()
        first_key = list(json_dict.keys())
        print(first_key)
        first_key = str(first_key[0])
        print(first_key)
        v = int(first_key)
        for i in json_dict:
            self.note_list.addItem(json_dict[str(v)]["title"])
            v += 1

    def note_write(self):
        resT = str(self.title.text())
        resC = str(self.text_area.toPlainText())
        self.note_list.addItem(resT)
        self.json_write(resT, resC)

    def note_remove(self):
        self.json_remove()
        list_items = self.note_list.selectedItems()
        for item in list_items:
            self.note_list.takeItem(self.note_list.row(item))

    def note_display():
        pass

app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()