from PySide6 import QtGui, QtWidgets
import json
from resources import default_note, default_new_note
from resources import _countChar

PATH = "C:/Users/timol/OneDrive/Documents/GitHub/Note/data/data.json"

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note")
        self.setMinimumSize(550, 300)
        self.setMaximumSize(825, 450)
        self.setWindowIcon(QtGui.QIcon('C:/Users/timol/OneDrive/Documents/GitHub/Note/data/icon.ico'))
        self._createComponents()
        self._addComponents()
        self._componentSettings()
        self._load(True)

    def _createComponents(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.left_layout = QtWidgets.QVBoxLayout(self)
        self.right_layout = QtWidgets.QVBoxLayout(self)

        self.lw_note_list = QtWidgets.QListWidget()
        self.btn_create_note = QtWidgets.QPushButton("New")
        self.btn_delete_note = QtWidgets.QPushButton("Delete")
        self.le_note_title = QtWidgets.QLineEdit()
        self.te_note_content = QtWidgets.QTextEdit()

    def _addComponents(self):
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.left_layout.addWidget(self.lw_note_list)
        self.left_layout.addWidget(self.btn_create_note)
        self.left_layout.addWidget(self.btn_delete_note)
        
        self.right_layout.addWidget(self.le_note_title)
        self.right_layout.addWidget(self.te_note_content)

    def _componentSettings(self):
        self.lw_note_list.itemClicked.connect(self._openNote)
        self.le_note_title.textChanged.connect(self._saveNote)
        self.te_note_content.textChanged.connect(self._saveNote)
        self.btn_delete_note.clicked.connect(self._removeNote)
        self.btn_create_note.clicked.connect(self._createNote)
        self.le_note_title.setMaxLength(35)
        self.le_note_title.setDisabled(True)
        self.te_note_content.setDisabled(True)
        self.btn_delete_note.setDisabled(True)
        self.le_note_title.setPlaceholderText("Title")
        self.te_note_content.setPlaceholderText("This is the content of my note")

    def _load(self, is_load):
        global json_dict

        with open(PATH, "r") as f:
            json_dict = json.load(f)
             
        if not json_dict or bool(json_dict) == False:  # if there isn't note, create one
            with open(PATH, "w") as f:
                json.dump(default_note, f, indent=4)
            with open(PATH, "r") as f:
                json_dict = json.load(f)

        if is_load == True:
            note_id = 0

            for i in json_dict:
                while not str(note_id) in json_dict:
                    note_id += 1

                self.lw_note_list.addItem(json_dict[str(note_id)]["title"])
                note_id += 1

    def _getIdWithTitle(self, target_title):
        global note_id

        if target_title != "":

            self._load(False)
            goal = None
            note_id = 0

            while goal != target_title:

                if str(note_id) in json_dict:
                    goal = str(json_dict[str(note_id)]["title"])

                note_id += 1
        note_id -= 1
        note_id = str(note_id)

    def _openNote(self):
        global disable_save_func

        self.le_note_title.setDisabled(False)
        self.te_note_content.setDisabled(False)
        self.btn_delete_note.setDisabled(False)
        disable_save_func = True
        self._getIdWithTitle(self.lw_note_list.currentItem().text())
        self.le_note_title.setText(json_dict[note_id]["title"])
        self.te_note_content.setText(json_dict[note_id]["content"])
        disable_save_func = False

    def _createNote(self):
        self._load(False)
        
        json_keys_list = list(json_dict.keys()) # get all the ID of the notes
        id_new_note = json_keys_list[-1]  # get the last ID
        id_new_note = int(id_new_note)
        id_new_note += 1  # get the next ID 

        json_dict.update({id_new_note:default_new_note})  # add the new note the json_dict

        with open(PATH, "w") as f:
            json.dump(json_dict, f, indent=4)  # add the note in the json file
               
        self.lw_note_list.addItem(default_new_note["title"]) # add the title in the list_note
         
        new_content = self.te_note_content.toPlainText()
        try:
            json_dict.update({note_id:{"title":self.le_note_title.text(), "content":new_content}})
        except:
            print("ERROR")

        with open(PATH, "w") as f:
            json.dump(json_dict, f, indent=4)

    def _saveNote(self):
        new_title = self.le_note_title.text()
        new_content = self.te_note_content.toPlainText()
        
        if _countChar(new_title) >= 1 and disable_save_func == False:
            self._load(False)
            json_dict.update({note_id:{"title":new_title, "content":new_content}})

            with open(PATH, "w") as f:
                json.dump(json_dict, f, indent=4)

            self.lw_note_list.clear()
            self._load(True)

    def _removeNote(self):
        self._load(False)
        self._getIdWithTitle(self.lw_note_list.currentItem().text())

        del json_dict[note_id]  # delete the note
        with open(PATH, "w") as f:
                json.dump(json_dict, f, indent=4)  # update the json file

        list_items = self.lw_note_list.selectedItems()
        for item in list_items:
            self.lw_note_list.takeItem(self.lw_note_list.row(item))  # remove the note title in the list_note

        self.le_note_title.clear()
        self.te_note_content.clear()
        self.le_note_title.setDisabled(True)
        self.te_note_content.setDisabled(True)
        self.btn_delete_note.setDisabled(True)
        self.lw_note_list.selectionModel().clear()

app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec()