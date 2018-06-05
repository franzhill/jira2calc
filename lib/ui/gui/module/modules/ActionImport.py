import logging
import tkinter as tk
import sys

from lib.ui.gui.module.AModule import AModule



class ActionImport(AModule):
	"""
  "Module" comprenant tous les éléments graphiques permettant à l'utilisateur d'effectuer l'import
  des issues Jira

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

		self.button = tk.Button(self.master, text='Importer', command=self._cbkButton) #, fg='grey')



	def getElements(self):
		elems = dict()
		elems['button'  ] = self.button
		return elems



	# ---------------------------------------------------------------------------
	# Privé
	# ---------------------------------------------------------------------------

	def _cbkButton(self):
		"""
		:return:
		"""
		self.log.debug('')

		self.app.importJiraIssuesForProject()
