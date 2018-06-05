import logging
import pprint
import traceback
from abc import ABCMeta, abstractmethod

from lib.jira.JiraIssue     import JiraIssue
from lib.reader.ADataReader import ADataReader
from lib.ui.IUi import IUi
from lib.writer.ADataWriter import ADataWriter


class AApplikation_(metaclass=ABCMeta):
	"""
	TODO rename Application

	@python-version 3.3.5
	@author fhill
	"""

	def __init__(self, data_reader, data_writer, user_interface):
		"""

		:type data_reader: ADataReader
		:type data_writer: ADataWriter
		:type ui: IUi
		"""

		# Pour utiliser le logger commun à tout le projet:
		# logger = logging.getLogger("main")
		# Pour utiliser un logger spécifique à ce fichier : (le définir aussi dans le fichier de conf des logs, si différent du logger root)
		logger = logging.getLogger(__name__)
		self.setLogger(logger)

		self.dr      = data_reader
		self.dw      = data_writer
		self.ui      = user_interface

		# Maintenant qu'on utilise la factory, l'initialisation est faite extérieurement
		# self.ui.initialize(self)



	# ---------------------------------------------------------------------------
	# Public
	# ---------------------------------------------------------------------------

	def setLogger(self, logger):
		"""
		 Pour injecter un logger spécifique.
		 Sinon, un logger par défaut sera mis en place (voir __init__)

		:type logger: logging.Logger
		:return:
		"""
		self.log = logger



	def initializeUi(self):
		try:
			self.ui.initialize(self)
		except Exception as e:
			self._handleException(e)



	def initializeDr(self):
		try:
			self.dr.initialize(self)
		except Exception as e:
			self._handleException(e)



	def run(self):
		try:
			self.ui.run()
		except Exception as e:
			self._handleException(e)



	def importJiraIssuesForProject(self):
		try:
			# Gère les cas d'exception spécifiques aux implémentations
			self._importJiraIssuesForProject()

		# On gère le cas d'exception général
		except Exception as e:
			self._handleException(e)



	@abstractmethod
	def _importJiraIssuesForProject(self):
		"""
		A implémenter dans les classes filles : tout simplement appeler sub_importJiraIssuesForProject()
		mais en gérant les cas d'exception spécifiques à l'implémentation fille, si besoin

		:return:
		"""
		pass



	def sub_importJiraIssuesForProject(self):
		self.log.debug('')

		prj  = self.ui.getProject()
		self.log.info("Importing JIRA issues from project [%s]" % (str(prj),))

		prj_name_display = "Tous les projets" if prj == -1 else prj

		## La possibilité de choisir "tous les projets" a été désactivée...
		# if self.modules["project"].isValueAll(prj):
		#	self.log.debug("Getting issues for ALL projects...")
		#	issues = self.dr.getIssuesAll()
		# else:

		self.log.debug("Getting issues for project: " + prj)
		self.connectDataReader()
		issues = self.dr.readIssues(prj)
		issues = self.postProcessIssues(issues)
		self.log.debug("issues=\n" + pprint.pformat(issues))

		self.log.info("Writing issues to destination...")
		self.connectDataWriter()
		self.dw.erase()             # On efface tout avant

		if not issues:
			msg = "Aucune issue JIRA trouvée pour le projet %s" % (prj_name_display,)
			self.log.info(msg)
			self.ui.info(msg)

		else:
			nb_issues_written = self.dw.writeIssues(issues)

			msg = "Import terminé. [%s] tâches Jira importées pour le projet [%s]" % (nb_issues_written, prj_name_display,)

			msg += ("\n\n" + self.dw.getReportMsg()       )   if  self.dw.getReportMsg()       else ''
			msg += ("\n\n" + self.getEndMessageSpecific() )   if  self.getEndMessageSpecific() else ''

			self.log.info(msg)
			self.ui.info(msg)

		self.finished()



	@abstractmethod
	def postProcessIssues(self, issues):
		"""

		:param issues:
		:return:
		:rtype: list[JiraIssue]
		"""
		pass



	@abstractmethod
	def connectDataWriter(self):
		pass



	@abstractmethod
	def connectDataReader(self):
		pass




	@abstractmethod
	def getEndMessageSpecific(self):
		"""

		:return:
		:rtype: str
		"""
		pass



	@abstractmethod
	def finished(self):
		pass



	def _handleException(self, e):
		self.log.error("!!! Une erreur s'est produite : \n" + str(e) + "\n\n" + "[TRACEBACK:] \n" + traceback.format_exc())
		# NDP : autre manière d'afficher le traceback:
		# log.error('Erreur à cause de ...', exc_info=True)

		msg = "Une erreur générale s'est produite : \n\n %s" % (e,)

		self.ui.error(msg)



	def _handleExceptionSpecific(self, e, msg=None):
		"""
		@todo maybe merge with _handleException
		"""
		self.log.error("!!! Une erreur s'est produite : \n" + str(e) + "\n\n" + "[TRACEBACK:] \n" + traceback.format_exc())

		self.ui.error(msg)