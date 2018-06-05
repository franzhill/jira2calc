import logging
import tkinter as tk
import sys
from lib.tools.tools import *
import pprint as pp
from lib.app.AApplikation_ import AApplikation_
from lib.ui.gui.module.AModule import AModule



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

		# Initialisation du menu
		# Pour l'instant on initialise avec des valeurs vides.
		# On attendra la création de la fenêtre graphique de l'application pour mettre à jour
		# les options avec les valeurs réelles issues de Jira (requiert une requête REST versd JIRA, qui peut échouer)
		# et ce afin de pouvoir afficher les messages d'erreur dans la fenêtre graphique

		self.label = tk.Label(self.master, text="Projet : ", bg='grey')
		# Valeurs proposées dans le sélecteur :
		self.options      = {"Initializing": 0}

		# Valeur résultante du module (résultat de la sélection par l'utilisateur):
		self.value      = tk.StringVar()
		# Valeur résultante finale du module  (on peut vouloir pour le traitement en interne, 'traduire' la valeur affichée à l'utilisateur):
		self.valueFinal = ''

		# Initialisation des valeurs résultantes
		self.value.set( next ( iter ( self.options.keys() )))
		self.valueFinal = self.options[self.value.get()]

		self.log.debug("self.value     =" + self.value.get())
		self.log.debug("self.valueFinal=" + str(self.valueFinal))

		# Création du widget "option menu"
		#                             (fenêtre mère, valeur à peupler,  valeur par défaut, valeurs des autres options, callback )
		#self.selector  = tk.OptionMenu(self.master, self.selectorInputValue, /*self.selectorOptionsDefault*/, *self.selectorOptions, command=self.cbkSelectProject)
		self.selector = tk.OptionMenu(self.master, self.value, *self.options, command = self._cbkSelectProject)




	# ---------------------------------------------------------------------------
	# Public
	# ---------------------------------------------------------------------------

	def initialize(self):
		'''
		Censé être appelé juste après la création de la fenêtre graphique de l'application
		:return:
		'''
		self.log.debug('')
		return self.update()



	def update(self):
		"""
		Rafraîchit les options affichées dans le menu en allant chercher les projets par une requête Jira
		:return:
		"""
		self.log.debug('')

		# Remise à zéro de la valeur résultante
		self.value.set('')

		# Valeurs proposées dans le sélecteur
		self.options      = self._getOptionsPrj()
		self.log.debug("self.options     =" + pp.pformat(self.options))

		# Mise à jour du menu
		menu = self.selector['menu']
		menu.delete(0, 'end')
		for i,o in sorted(self.options.items()):
			self.log.debug("adding label = " + i)
			menu.add_command(label=i, command=tk._setit(self.value, i))
			#menu.setvar('PY_VAR', i)
		#m.entryconfig(1, label="Horse")

		# Màj des valeurs
		self.value.set(next(iter(self.options.keys())))    # intervenir ici pour positionner une valeur par défaut
		self.valueFinal = self.options[self.value.get()]



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
		return self.value.get()




	# ---------------------------------------------------------------------------
	# Private
	# ---------------------------------------------------------------------------

	def _getOptionsPrj(self):
		"""
		Récupère la liste des projets de Jira
		"""
		self.log.debug('')
		jira_projects = self.app.dr.getProjects(False)
		self.log.debug('After call getProjects')
		# Dictionnaire de projets  [nom, id]
		options = dict()
		for p in jira_projects:
			options[p.name] = p.id

		self.log.debug("options=\n" + pp.pformat(options))
		return options



	def _cbkSelectProject(self, *args):
		self.log.debug('')

		# Valeur finale que l'on veut récupérer
		self.valueFinal = self.options[self.value.get()]
		self.log.debug("User chose project: %s, the id of which is: %s" % (self.value.get(), self.valueFinal))


