from PySide6 import QtGui, QtWidgets
import filemanager as fm

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note")
        self.setMinimumSize(550, 300)
        self.setMaximumSize(825, 450)
        self.setWindowIcon(QtGui.QIcon('C:/Users/timol/OneDrive/Documents/GitHub/Note/data/icon.ico'))
        self._components()
        self.load()
        print('OK')

    def _components(self):

        # --- Create components ---
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.left_layout = QtWidgets.QVBoxLayout(self)
        self.right_layout = QtWidgets.QVBoxLayout(self)

        self.lw_note_list = QtWidgets.QListWidget()
        self.btn_create_note = QtWidgets.QPushButton("New")
        self.btn_delete_note = QtWidgets.QPushButton("Delete")
        self.btn_save_note = QtWidgets.QPushButton("Save")
        self.le_note_title = QtWidgets.QLabel()
        self.te_note_content = QtWidgets.QTextEdit()

        # --- Add components ---
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.left_layout.addWidget(self.lw_note_list)
        self.left_layout.addWidget(self.btn_create_note)
        self.left_layout.addWidget(self.btn_delete_note)
        
        self.right_layout.addWidget(self.le_note_title)
        self.right_layout.addWidget(self.te_note_content)
        self.right_layout.addWidget(self.btn_save_note)

        # --- Components settings ---
        self.lw_note_list.itemClicked.connect(self.openNote)
        self.btn_save_note.clicked.connect(self.saveNote)
        self.btn_delete_note.clicked.connect(self.removeNote)
        self.btn_create_note.clicked.connect(self.createNote)
        self.te_note_content.setPlaceholderText("This is my note.")
        self.te_note_content.textChanged.connect(self.func)
    
    def func(self):
        self.te_note_content.setDisabled(False)

    def load(self):
        dict_notes = fm.dictNotes()
        note_id = 0
        for i in dict_notes:
                while not str(note_id) in dict_notes:
                    note_id += 1
                self.lw_note_list.addItem(dict_notes[str(note_id)]["title"])
                note_id += 1

    def openNote(self):
        dict_note = fm.dictNotes()
        self.le_note_title.setText(fm.dictNotes()[fm.getIdWithTitle(self.lw_note_list.currentItem().text())]["title"])
        self.te_note_content.setText(dict_note[fm.getIdWithTitle(self.lw_note_list.currentItem().text())]["content"])
        self.btn_save_note.setDisabled(True)

    def createNote(self):
        
        self.saveNote()
        all_json_ids = list(fm.dictNotes().keys()) 

        if all_json_ids == []:
            id_new_note = 0
        else:
            id_new_note = all_json_ids[-1]
            id_new_note = int(id_new_note) + 1
            
        note_title = QtWidgets.QInputDialog.getText(self, ' ', 'Enter the title of the note:')
        note_title = str(list(note_title)[0])
        if note_title == "":
            return 0
        fm.createNote(str(id_new_note), note_title, "")
        self.lw_note_list.addItem(note_title)

        if self.le_note_title.text() == False:
            dict_note = fm.dictNotes()
            self.le_note_title.setText(note_title)
            self.te_note_content.setText("")
        

    def saveNote(self):
        note_id = fm.getIdWithTitle(self.le_note_title.text())
        note_title = self.le_note_title.text()
        note_content = self.te_note_content.toPlainText()
        fm.updateNote(note_id, note_title, note_content)

    def removeNote(self):

        try:
            fm.deleteNote(self.lw_note_list.currentItem().text())
            for item in self.lw_note_list.selectedItems():
                self.lw_note_list.takeItem(self.lw_note_list.row(item))

            self.le_note_title.clear()
            self.te_note_content.clear()

        except AttributeError:
            return

app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec()