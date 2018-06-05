from lib.app.AApplikation_ import AApplikation_
from lib.conf.conf import conf
from lib.jira.JiraIssues  import JiraIssues
from lib.reader.ADataReader import ADataReader
from lib.ui.IUi import IUi
from lib.writer.ADataWriter import ADataWriter


class CalcApplikation(AApplikation_):
	"""
	@python-version 3.3.5
	@author fhill
	"""


	def __init__(self, data_reader, data_writer, user_interface):
		"""

		:type data_reader: ADataReader
		:type data_writer: ADataWriter
		:type user_interface: IUi
		"""

		super().__init__(data_reader, data_writer, user_interface)




	def postProcessIssues(self, issues):
		# Pour les sous-tâches, on importe les valeurs du parent (tâche) en cas de champ vide:
		self.log.debug('')
		jissues = JiraIssues(issues)
		jissues.copyTaskFieldsToSubtasksWhereEmpty()
		jissues.sortOn(conf['oo']['SORT_ISSUES_ON_FIELD'], conf['oo']['SORT_ISSUES_DIRECTION'])
		return jissues.getIssues()



	def getEndMessageSpecific(self):
		return "\n\n NB: Les données se trouvent dans l'onglet %s" % (conf['oo']['WRITE_ISSUES_IN_SHEET'])



	def _importJiraIssuesForProject(self):
		self.log.debug('')
		try:
			self.sub_importJiraIssuesForProject()#self.__importJiraIssuesForProject()
		# Ici on gère cette exception spécifique à cette classe fille :
		except OSError as e:
			self._handleExceptionSpecific(e, "Erreur lors de la lecture du fichier : \n\n %s" % (e,)  )




	def connectDataReader(self):
		return self.dr.connect()



	def connectDataWriter(self):
		self.log.debug('')
		file = self.ui.getFile()

		return self.dw.connect(file)



	def finished(self):
		# Rien de particulier à faire ici
		pass
