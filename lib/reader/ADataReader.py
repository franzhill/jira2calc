from abc import ABCMeta, abstractmethod
import logging


class ADataReader( metaclass=ABCMeta):
	"""
	Classe abstraite
	L'objet concret permettra la lecture d'issues JIRA à partir d'une source (ex : Jira directement, en BD etc.)

	@python-version 3.3.5
	@author fhill
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
		Connexion à la destination d'où on doit lire les issues

		:param args: en fonction de l'implémentation, la signature est amenée à être spécifique
		"""
		pass



	@abstractmethod
	def readIssues(self, project_name):
		"""

		Pour des raisons historiques cette fonction se nomme ainsi
		mais idéalement maintenant qu'elle est abstraite devrait plutôt s'appeler qqch comme
		readIssues(project=None)

		:param project_name: Nom du projet tel que dans Jira
		:type project_name: str
		:rtype: list[JiraIssue]
		:return:
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



	def initialize(self, app):
		"""
		Il nous faut pouvoir remonter à l'app "mère" pour bien fonctionner
		On ne peut pas faire cette liaison dans __init__ (à cause de dépendance circulaire voir classe Factory)

		A appeler le plus tôt possible !!

		TODO voir si l'on a tjs besoin de cette fonction. Je pense qu'on peut supprimer (FHI 2017.02.02)

		:type app: AApplikation_
		:param app: Reference to the owner application - On est obligé de l'avoir pour les callbacks de l'UI, qui sont gérés côté Applikation (~contrôleur)
		"""
		self.app = app



	@abstractmethod
	def getProjects(self, sort=True):
		"""
		Récupère les projets JIRA

		Selon le type d'implémentation concrète de la présente classe abstraite, peut ne pas être pertinent.
		=> Dans ce cas, implémenter avec un "pass"

		:param sort: Trie les projets alphabétiquement
		:type  sort: bool
		:rtype: list[JiraProject]
		"""

