import logging
import tkinter as tk
import sys
from lib.tools import *
import pprint as pp

from lib.ui.gui.module.AModule import AModule


# @todo pê mettre cette conf ailleurs ou mieux la gérer
optionAllProjectsLbl = "*** Tous les projets ***"
optionAllProjectsVal = -1



class SelectProject(AModule):
	"""
	"Module" comprenant tous les éléments graphiques permettant la sélection par l'utilisateur d'un projet Jira

	Les options sont des couples de valeurs : {nom projet, id projet}
	L'idée étant que l'utilisateur sélectionne un nom de projet, et que ce soit sont id qui soit manipulé par le programme.
	A voir à l'usage s'il est désirable de faire ainsi. On pourrait pê sinon manipuler seulement le nom du projet
	(voir si cela pose pb ou non dans les appels Jira, et aussi répondre à la question : comment traiter le cas où l'on
	veut tous les projets)

	@see http://stackoverflow.com/questions/18380766/assigning-variables-using-choices-in-tkinter-dropdown-menu-python-2-7

	@todo valeur par défaut à sauvegarder et charger depuis une config ou fichier de preférences
	@todo faire en sorte que les options soient toujours présentées dans le même ordre

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


		# Valeurs proposées dans le sélecteur :
		self.selectorOptionsPrj      = self._getSelectorOptionsPrj()
		self.selectorOptionsDefault  = {optionAllProjectsLbl: optionAllProjectsVal}
		self.selectorOptions         = self.selectorOptionsPrj.copy() ; self.selectorOptions.update(self.selectorOptionsDefault)  # concat des 2 précédentes
		self.log.debug("self.selectorOptions     =" + pp.pformat(self.selectorOptions))

		# Valeur cible intermédiaire du module (résultat de la sélection par l'utilisateur):
		self.selectorInputValue      = tk.StringVar()
		# Valeur cible finale du module  (pas forcément ce que l'utilisateur voit à l'interface):
		self.selectorInputValueFinal = ''

		# Initialisation des valeurs cibles avec les valeurs par défaut (au cas où l'utilisateur ne fasse pas de choix)
		self.selectorInputValue.set(next (iter (self.selectorOptionsDefault.keys())) )  # devrait être == "Tous les projets" (ou quel que soit le texte choisi)
		self.selectorInputValueFinal = self.selectorOptionsDefault[self.selectorInputValue.get()]

		self.log.debug("self.selectorInputValue     =" +     self.selectorInputValue.get())
		self.log.debug("self.selectorInputValueFinal=" + str(self.selectorInputValueFinal ))

		# Création du widget "option menu"
		#                             (fenêtre mère, valeur à peupler,  valeur par défaut, valeurs des autres options, callback )
		#self.selector  = tk.OptionMenu(self.master, self.selectorInputValue, /*self.selectorOptionsDefault*/, *self.selectorOptions, command=self.cbkSelectProject)
		self.selector = tk.OptionMenu(self.master, self.selectorInputValue, *self.selectorOptions, command = self._cbkSelectProject)

		self.label = tk.Label(self.master, text="Projet : ", bg='grey')



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
		return elems



	def getValue(self):
		"""
		Renvoie la valeur (finale) du module, suite à input par l'utilisateur
		"""

		# On renvoit l'id du projet sélectionné
		#return self.selectorInputValueFinal

		# On renvoit le nom du projet sélectionné
		if self.selectorInputValueFinal == optionAllProjectsVal:  # sauf dans le cas où l'on veut tous les projets à ce moment on renvoit un code spécifique
			return optionAllProjectsVal
		return self.selectorInputValue.get()



	def isValueAll(self, val):
		"""
		Note de conception: il s'agit d'encapsulation... C'est à ce module de dire si val correspond au code pour "tous les projets"
		:param val: une valeur retournée par getValue()
		:return: boolean
		"""
		return val == optionAllProjectsVal


	# ---------------------------------------------------------------------------
	# Private
	# ---------------------------------------------------------------------------

	def _getSelectorOptionsPrj(self):
		"""
		Récupère la liste des projets de Jira
		"""
		jira_projects = self.app.jr.getProjects()

		# Dictionnaire de projets  [nom, id]
		options = dict()
		for p in jira_projects:
			options[p.name] = p.id

		self.log.debug("options=\n" + pp.pformat(options))
		return options



	def _cbkSelectProject(self, *args):
		self.log.debug('')

		# Valeur finale que l'on veut récupérer
		self.selectorInputValueFinal = self.selectorOptions[self.selectorInputValue.get()]
		self.log.debug("User chose project: %s, the id of which is: %s" % (self.selectorInputValue.get(), self.selectorInputValueFinal))


