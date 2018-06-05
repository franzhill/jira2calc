import pprint

from lib.app.AApplikation_ import AApplikation_
from lib.ui.IUi import IUi
from lib.writer.ADataWriter import ADataWriter


class PentahoApplikation(AApplikation_):
	"""
	@python-version 3.3.5
	@author fhill
	"""


	def __init__(self, data_reader, data_writer, user_interface ): # = None):
		"""

		:type data_reader: ADataReader
		:type data_writer: ADataWriter
		:type user_interface: IUi
		"""

		super().__init__(data_reader, data_writer, user_interface)



	def postProcessIssues(self, issues):
		self.log.debug('')
		# On ne fait rien de spécial

		return issues



	def getEndMessageSpecific(self):
		# On ne fait rien de spécial
		return ''



	def _importJiraIssuesForProject(self):
		self.log.debug('')

		# Ici dans le cas Pentaho, pas d'exception spécifique à surveiller
		# => on appelle la sous-fonction et on laisse celle-ci gérer les exceptions
		self.sub_importJiraIssuesForProject()


	def connectDataWriter(self):
		self.log.debug('')

		db_params = self.ui.getDbParamsDest()
		self.log.debug('db_params=' + pprint.pformat(db_params))

		self.dw.setParams(db_params)
		return self.dw.connect()



	def connectDataReader(self):
		self.log.debug('')

		db_params = self.ui.getDbParamsSource()
		self.log.debug('db_params=' + pprint.pformat(db_params))

		self.dr.setParams(db_params)
		return self.dr.connect()



	def finished(self):
		self.log.debug('')
		self.dr.finished()
		self.dw.finished()


