import os
from PySide import QtGui
from ui.fenetrePrincipale import Ui_fenetrePrincipale
import notesManager as nm
import utils as utl

class CreateurDeNote(QtGui.QWidget, Ui_fenetrePrincipale):
	def __init__(self):
		super(CreateurDeNote, self).__init__()

		self.setupUi(self)
		self.recupererNotes()
		self.setupConnections()
		self.show()

	def setupConnections(self):
		self.btn_creerNote.clicked.connect(self.creerNote)
		self.lw_listeDeNotes.itemClicked.connect(self.afficherLaNote)
		self.btn_mettreAJourNote.clicked.connect(self.mettreAJourLaNote)
		self.btn_supprimerNote.clicked.connect(self.supprimerNote)

	def creerNote(self):
		nomDeLaNote, ok = QtGui.QInputDialog.getText(self, 'Creer une note', 'Entrez le nom de la note: ')
		if not ok:
			return

		nm.creerNote(nomDeLaNote)
		self.recupererNotes()

	def recupererNoteSelectionnee(self):
		notesSelectionnees = self.lw_listeDeNotes.selectedItems()
		if not notesSelectionnees:
			return

		nomDeLaNote = notesSelectionnees[-1].text()
		cheminDeLaNote = os.path.join(utl.DATA_FOLDER, nomDeLaNote + '.txt')

		return nomDeLaNote, cheminDeLaNote

	def afficherLaNote(self):
		"""
		Fonction qui affiche le contenu de la note selectionnee
		"""

		# On recupere le nom et le chemin de la note
		nomDeLaNote, cheminDeLaNote = self.recupererNoteSelectionnee()
		
		# On recupere le contenu de la note
		contenuDeLaNote = nm.recupererContenuNote(nomDeLaNote)
		
		# On affiche le contenu de la note dans le QTextEdit
		self.te_contenuDeLaNote.setText(contenuDeLaNote)

	def mettreAJourLaNote(self):
		"""
		Fonction pour mettre a jour le contenu de la note
		"""

		# On recupere le nom et le chemin de la note
		nomDeLaNote, cheminDeLaNote = self.recupererNoteSelectionnee()
		# On recupere le nouveau contenu de la note avec la fonction 'toPlainText'
		contenuDeLaNote = self.te_contenuDeLaNote.toPlainText()
		# On met a jour la note avec la meme fonction que celle utilisee pour creer une note
		nm.creerNote(nomDeLaNote, contenuDeLaNote)

	def supprimerNote(self):
		nomDeLaNote, cheminDeLaNote = self.recupererNoteSelectionnee()
		nm.supprimerNote(nomDeLaNote)
		self.recupererNotes()

	def recupererNotes(self):
		self.lw_listeDeNotes.clear()
		notes = nm.recupererLesNotes()
		self.lw_listeDeNotes.addItems(notes)

app = QtGui.QApplication([])
nc = CreateurDeNote()
app.exec_()
