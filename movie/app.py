from PySide2 import QtWidgets, QtCore
from movie import Movie, get_movies

class App(QtWidgets.QWidget):
    def  __init__(self):
        super().__init__()
        self.setWindowTitle("_Note_")
        self.component()
        self.actions()
        self.populate_movies()

    def component(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.left_layout = QtWidgets.QVBoxLayout(self)
        self.right_layout = QtWidgets.QVBoxLayout(self)

        self.le_noteTitle = QtWidgets.QLineEdit()
        self.te_note = QtWidgets.QTextEdit()
        self.btn_saveNote = QtWidgets.QPushButton("Sauvegarder")
        self.list_note = QtWidgets.QListWidget()
        self.list_note.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.btn_removeNote = QtWidgets.QPushButton("Supprimer")

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        self.right_layout.addWidget(self.le_noteTitle)
        self.right_layout.addWidget(self.te_note)
        self.right_layout.addWidget(self.btn_saveNote)
        self.left_layout.addWidget(self.list_note)
        self.left_layout.addWidget(self.btn_removeNote)

    def actions(self):
        self.btn_saveNote.clicked.connect(self.add_movie)
        self.le_noteTitle.returnPressed.connect(self.add_movie)
        self.btn_removeNote.clicked.connect(self.remove_movie)

    def populate_movies(self):
        self.list_note.clear()
        movies = get_movies()
        for movie in movies:
            lw_item = QtWidgets.QListWidgetItem(movie.title)
            lw_item.setData(QtCore.Qt.UserRole, movie)
            self.list_note.addItem(lw_item)

    def add_movie(self):
        movie_title = self.le_noteTitle.text()
        if not movie_title:
            return False

        movie = Movie(title=movie_title)
        result = movie.add_to_movies()
        if result:
            lw_item = QtWidgets.QListWidgetItem(movie.title)
            lw_item.setData(QtCore.Qt.UserRole, movie)
            self.list_note.addItem(lw_item)
            self.le_noteTitle.setText("")

    def remove_movie(self):
        for selected_item in self.list_note.selectedItems():
            movie = selected_item.data(QtCore.Qt.UserRole)
            movie.remove_from_movies()
            self.list_note.takeItem(self.list_note.row(selected_item))

app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()