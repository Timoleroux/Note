from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QWaitCondition, Qt
import os
import json

PATH = "C:/Users/timol/OneDrive/Documents/GitHub/Note/data/data.json"
JSON_LIST = ["TEST 1", "TEST 2"]

def add_note_json(content):
    with open(PATH, "w") as f:
        final = KSOn
        json.dump(JSON_LIST, f, indent=4)

def get_note_json():
    with open(PATH, "r") as f:
        the_list = json.load(f)
        for i in the_list:
            res = the_list
            return res

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note")
        self.setWindowIcon(QtGui.QIcon('C:/Users/timol/OneDrive/Documents/GitHub/Note/data/icon.ico'))
        self.component()
        self.css()
        self.get_note()

    def component(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.left_layout = QtWidgets.QVBoxLayout(self)
        self.right_layout = QtWidgets.QVBoxLayout(self)
        self.title = QtWidgets.QLineEdit()
        self.text_area = QtWidgets.QTextEdit()
        self.save = QtWidgets.QPushButton("Sauvegarder")
        self.save.clicked.connect(self.add_note)
        self.delete = QtWidgets.QPushButton("Supprimer")
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

    def add_note(self):
        res = str(self.title.text())
        self.note_list.addItem(res)
        add_note_json(res)

    def get_note(self):
        self.note_list.addItem(str(get_note_json))
        









app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()