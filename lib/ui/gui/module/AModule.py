import logging
from abc import ABCMeta, abstractmethod




class AModule(metaclass=ABCMeta):
	"""
	Regroupe des composants Tkinter fonctionnellement liés afin de pouvoir les manipuler et les réutiliser comme un tout

	L'idée des modules est de regrouper des éléments graphiques afin qu'ils ne forment qu'un tout qu'on pourra réutiliser
	dans des interfaces différentes.

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



	@abstractmethod
	def getElements(self):
		"""
		 Renvoie les différents éléments du module afin qu'ils puissent être positionnés par le niveau supérieur

		 :return: un dictionnaire de type {'nom_element' : element}
		 :rtype: dict
		"""
		pass



	def getValue(self):
		"""
		Renvoie la valeur (finale) du module, si le module en produit une (suite à input par l'utilisateur par ex.)
		A surcharger dans les classes filles si le module renvoit une valeur finale.

		:rtype: mixed
		"""
		return None