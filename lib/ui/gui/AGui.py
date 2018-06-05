import logging
import tkinter as tk
from abc import ABCMeta, abstractmethod
from tkinter import messagebox

from lib.ui.IUi import IUi
from lib.ui.gui.module import modules


class AGui(IUi, metaclass=ABCMeta):
	"""
	Définit les éléments communs d'une interface graphique
	(abstraite : les instanciations concrètes pourront être par exemple une GUI pour s'interfacer avec Pentaho, ou Calc etc.
	selon le script que l'utilisateur aura lancé)

	@python-version 3.3.5
	@author fhill
	"""

	def __init__(self):
		"""

		"""

		# Pour utiliser le logger commun à tout le projet:
		# logger = logging.getLogger("main")
		# Pour utiliser un logger spécifique à ce fichier : (le définir aussi dans le fichier de conf des logs, si différent du logger root)
		logger = logging.getLogger(__name__)
		self.setLogger(logger)

		self.windowRoot      = tk.Tk()
		self.windowRootFrame = tk.Frame(self.windowRoot)
		self.modules         = dict()


	# ---------------------------------------------------------------------------
	# Public
	# ---------------------------------------------------------------------------

	def setLogger(self, logger):
		"""
		 Pour injecter un logger spécifique.
		 Sinon, un logger par défaut sera mis en place (voir __init__)

		:type logger: logging.Logger
		"""
		self.log = logger



	def initialize(self, app):
		self.app = app
		self._createLayout()
		self.log.debug("FIRING AFTER....")
		self.windowRootFrame.after(1000, self.initialize_) # delay is in ms



	def initialize_(self):
		#try:
			self.log.debug('')
			for i,m in self.modules.items():
				self.log.debug("i,m = %s, %s" % (str(i), str(m)))

				try:
					m.initialize()          # intialise le module, si une initialisation est prévue,
				except AttributeError:    # sinon rien
					pass
	#	except Exception as e:
	#		self._handleException(e)




	def run(self):
		self.windowRootFrame.mainloop()




	def _createLayout(self):
		'''
		Positionne les différents widgets graphiques dans la fenêtre
		:return:
		'''
		self.log.debug('')

		self.windowRootFrame.pack(padx=5, pady=5)
		self.windowRoot.title(self._getWindowTitle())
		self._createModules()



	@abstractmethod
	def _getWindowTitle(self):
		pass



	@abstractmethod
	def _createModules(self):
		"""
		Dans l'implémentantation de cette fonction dans une classe fille CF,
		appeler simplement sub_importJiraIssuesForProject dans un try: ... except:
		Cela permettra d'y gérer les exception propres à cettte classe CF.
		:return:
		"""
		pass





	def createModuleSelectProject(self):
		self.log.debug('')

		# On peut choisir de positionner les éléments du module "InputProject" directement dans cette feneêtre...
		in_line_or_in_frame = "in_frame"  # "in_frame"
		if in_line_or_in_frame == "in_line":
			self.modules["project"] = modules.SelectProject(self.windowRootFrame, self.app)
			self.modules["project"].getElements()["selector"].grid(row=0, column=1, padx=5, pady=5)
			self.modules["project"].getElements()["label"   ].grid(row=0, column=0, padx=5, pady=5)

		# ...ou alors de les packager dans une frame:
		else:
			frame_proj = tk.Frame(self.windowRootFrame, bg='grey', relief='raised', borderwidth=1)
			frame_proj.pack(padx=5, pady=5, side="top",  fill='both')

			self.modules["project"] = modules.SelectProject(frame_proj, self.app)
			self.modules["project"].getElements()["label"   ].pack(padx=5, pady=5, side="left")  # grid(row=0, column=0, padx=5, pady=5)
			self.modules["project"].getElements()["selector"].pack(padx=5, pady=5, side="left")  # grid(row=0, column=1, padx=5, pady=5)



	def createModuleImport(self):

		# Bouton d'import
		# ----------------

		frame_import = tk.Frame(self.windowRootFrame)
		frame_import.pack(padx=5, pady=5, side="top")

		# Idem: on peut choisir de positionner les élements suivants à même la fenêtre, ou les envelopper d'une frame
		self.modules["import"] = modules.ActionImport(frame_import, self)
		self.modules["import"].getElements()["button"].pack(padx=5, pady=5, side="right")  #grid(row=1, column=3, padx=5, pady=5)






	def importJiraIssuesForProject(self):
		"""
		Appelé par : callback du bouton "Importer"
		:return:
		"""
		self.app.importJiraIssuesForProject()




	def getProject(self):
		return self.modules["project"].getValue()




	def error(self, msg):
		messagebox.showerror('Erreur', msg)


	def info(self, msg):
		messagebox.showinfo('Information', msg)