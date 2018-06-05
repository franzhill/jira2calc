from abc import ABCMeta, abstractmethod
# from lib.app.AApplikation_ import AApplikation_   # On ne peut pas ... sinon import circulaire ... pas cool Python de ne pas gérer ça...


class IUi(metaclass=ABCMeta):
	"""
	Interface pour les User Interfaces (UI)  (utilisées dans les applications *Calc* et *Pentaho*)

	@python-version 3.3.5
	@author fhill
	"""



	#	def initialize(self, app: AApplikation_) -> None:   # expérimentation du type hinting -> ne marche pas apparemment
	@abstractmethod
	def initialize(self, app):
		"""
		Il nous faut pouvoir remonter à l'app "mère" pour bien fonctionner
		(entre autres pour les callbacks de l'UI, qui sont gérés côté Applikation (~contrôleur))
		On ne peut pas faire cette liaison dans __init__ (à cause de dépendance circulaire voir classe Factory)

		A appeler le plus tôt possible !!

		:type app: AApplikation_
		:param app: Reference to the owner application - On est obligé de l'avoir
		"""
		pass



	@abstractmethod
	def run(self):
		pass



	@abstractmethod
	def error(self, msg):
		"""

		:type msg: str
		:return:
		"""
		pass



	@abstractmethod
	def info(self, msg):
		"""

		:type msg: str
		:return:
		"""
		pass



	@abstractmethod
	def getProject(self):
		"""

		:return: le nom (JIRA) du projet.
		         Dans les cas de "tous les projets" (là où cette option existe) : soit "ALL", soit -1
		:rtype: str|int
		"""
		pass