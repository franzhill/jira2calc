from abc import ABCMeta, abstractmethod
import logging


class ADbConnector( metaclass=ABCMeta):
	"""
	Classe abstraite, voir classes filles concrètes pour les usages

	@python-version 3.3.5
	@author fhill
	"""

	def __init__(self):

		# Pour utiliser le logger commun à tout le projet:
		#logger = logging.getLogger("main")
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



	def setParams(self, **kwargs):
		"""
		Pour définir les paramètres (ou les changer) dynamiquement
		Spécifier les arguments qui doivent redéfinir les paramètres par défaut
		(i.e. positionnés dans le constructeur) par clé
		:return:
		"""



	@abstractmethod
	def connect(self):
		pass



	@abstractmethod
	def execute(self, *args):
		"""

		:param args: selon les implémentations la signature de la fonction peut varier
		:return:
		"""
		pass


	@abstractmethod
	def commit(self):
		pass



	@abstractmethod
	def finished(self):
		pass