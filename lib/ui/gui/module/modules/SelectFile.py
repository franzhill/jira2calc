import logging
import tkinter as tk
from tkinter.filedialog import askopenfilename

from lib.ui.gui.module.AModule import AModule



class SelectFile(AModule):
	"""
	"Module" comprenant tous les éléments graphiques permettant la sélection par l'utilisateur d'un fichier Calc

	@python-version 3.3.5
	@author fhill
	"""


	def __init__(self, master, app):
		"""
		:param master: la fenêtre graphique (Tk) parente
		:type  master: tk.Tk
		:param app: l'application dans laquelle évolue ce module
		:type  app: AApplikation_
		"""
		super().__init__()

		self.master = master
		self.app    = app

		self.label    = tk.Label(self.master, text="Fichier calc : ", bg='grey')
		# Valeur cible finale du module
		self.value    = tk.StringVar()              # variable miroir du champ Ã©dition du Filename
		# Input (permet dà l'utilisateur de sélectionner son fichier)
		self.selector = tk.Entry (self.master, textvariable=self.value, width=100)  # width = 100 car
		self.browser  = tk.Button(self.master, text='Parcourir ...', command=self.cbkSelectFile)


	# ---------------------------------------------------------------------------
	# Public
	# ---------------------------------------------------------------------------


	def getElements(self):
		"""
		 Renvoie les différents éléments du module afin qu'ils puissent être positionnés par le niveau supérieur
		"""
		elems = dict()
		elems['selector'] = self.selector
		elems['label'   ] = self.label
		elems['browser' ] = self.browser
		return elems



	def getValue(self):
		"""
		Renvoie la valeur (finale) du module, suite à input par l'utilisateur
		"""
		return self.value.get()



	# ---------------------------------------------------------------------------
	# Private
	# ---------------------------------------------------------------------------


	def cbkSelectFile(self, *args):
		self.log.debug('')
		filepath = askopenfilename(title="Ouvrir un fichier Calc", filetypes=[('Calc files', '.ods'), ('all files', '.*')])
		self.value.set(filepath)
		self.log.debug("self.value=" + self.value.get())


