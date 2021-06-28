from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QWaitCondition, Qt
import os
import json

PATH = "C:/Users/timol/OneDrive/Documents/GitHub/Note/data/data.json"

def add_note_json(content):
    with open(PATH, "r") as f:
        load_json = json.load(f)  # get the content of the list in the json
    with open(PATH, "w") as f:
        load_json.append(content) # add the content of the () in the list
        json.dump(load_json, f, indent=4) # update the list in the json

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

    def json_load(self):
        global json_list
        try:
            with open(PATH, "r") as f:
                json_list = json.load(f)
        except:
            with open(PATH, "w") as f:
                json.dump(["Ho to use note ?"], f, indent=4)
            with open(PATH, "r") as f:
                json_list = json.load(f)

    def json_write(self, content):
        self.json_load()
        json_list.append(content)
        with open(PATH, "w") as f:
                json.dump(json_list, f, indent=4)

    def json_remove(self):
        self.json_load()
        res = self.note_list.currentItem().text()
        json_list.remove(str(res))
        with open(PATH, "w") as f:
                json.dump(json_list, f, indent=4)

    def note_load(self):
        self.json_load()
        for i in json_list:
            self.note_list.addItem(i)

    def note_write(self):
        res = str(self.title.text())
        self.note_list.addItem(res)
        self.json_write(res)

    def note_remove(self):
        self.json_remove()
        list_items = self.note_list.selectedItems()
        for item in list_items:
            self.note_list.takeItem(self.note_list.row(item))













app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()