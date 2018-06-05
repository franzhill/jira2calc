from abc import ABCMeta, abstractmethod
import logging


class ADataWriter( metaclass=ABCMeta):
	"""
	Classe abstraite
	Objet permettant l'écriture d'issues JIRA dans une destination (ex : en BD, dans CALC etc.)
	"""

	def __init__(self):

		# Pour utiliser le logger commun à tout le projet:
		#logger = logging.getLogger("main")
		# Pour utiliser un logger spécifique à ce fichier : (le définir aussi dans le fichier de conf des logs, si différent du logger root)
		logger = logging.getLogger(__name__)

		self.setLogger(logger)


	def setLogger(self, logger):
		"""
		 Pour injecter un logger spécifique.
		 Sinon, un logger par défaut sera mis en place (voir __init__)

		:type logger: logging.Logger
		"""
		self.log = logger



	@abstractmethod
	def setParams(self, params):
		"""
		Pour définir les paramètres (ou les changer) dynamiquement
		Spécifier les arguments qui doivent redéfinir les paramètres par défaut
		(i.e. positionnés dans le constructuer) par clé, dans le dictionnaire

		:param params: dictionnaire de paramètres
		:type params: dict
		:return:
		"""
		pass



	@abstractmethod
	def connect(self, *args):
		"""
		Connexion à la destination devant recevoir les issues

		:param args: en fonction de l'implémentation, la signature est amenée à être spécifique
		"""
		pass



	@abstractmethod
	def writeIssues(self, issues):
		"""
		Ecrit des issues dans la destination (une fois connectée la destination, et les anciennes issues effacées)

		:type issues: list[JiraIssue]
		:return: nombre d'issues insérées
		:rtype: int
		"""
		pass



	@abstractmethod
	def finished(self):
		"""
		Traitements de fin une fois les issues érites
		Peut varier selon les implémentations.
		Ex: pour une écriture en BD, on pourrait vouloir ici committer et fermer la connexion

		:return:
		"""
		pass



	@abstractmethod
	def erase(self):
		"""
		Efface toutes les issues se trouvant
		Peut être appelé avant écriture des issues
		 Tant qu'il n'y a pas de mode "incrémental" d'écriture des issues dans la destination, c'est même le mécanisme
		recommandé (et adopté) que d'effacer à chaque fois avant d'écrire les issues
		"""
		pass



	@abstractmethod
	def getReportMsg(self):
		"""
		Renvoie un message (destiné à affichage à l'utilisteur par ex.)
		présentant un rapport résumé des opérations d'écriture (ce qui a été fait etc., combien de lignes, où etc.)
		Bien évidemment, ne doit être appelé qu'une fois les opérations finies

		:return:
		:rtype: str
		"""
		pass