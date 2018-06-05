from abc import ABCMeta

import psycopg2

from lib.db_connector.exceptions import *
from lib.jira.JiraIssue import JiraIssue
from lib.oo.import_oo_libs   import *
from lib.reader.ADataReader import ADataReader
from lib.tools.tools         import *
from lib.db_connector.db_connectors.PostgresqlConnector import PostgresqlConnector


class ADbDataReader(ADataReader,  metaclass=ABCMeta):
	"""
	Abstract DbDataReader

	Lit des issues JIRA depuis une BD (Postgresql)
	Les éléments de connexion à la BD sont implémentés.
	Mais la fonction de lecture ne l'est pas

	TODO on pourrait factoriser avec ADbDataWriter

	@python-version 3.3.5
	@author fhill
	"""


	def __init__(self, host, port, user, password, dbname):  # TODO changer en params (dictionnaire)
		super().__init__()

		self.db_connector = PostgresqlConnector(host, port, user, password, dbname)



	# ---------------------------------------------------------------------------
	# Public
	# ---------------------------------------------------------------------------

	def connect(self):
		"""

		:return:
		"""
		self.log.debug('')

		self.db_connector.connect()





	def setParams(self, params):
		self.db_connector.setParams(params)










	def readFromTable(self, table_name):
		"""
		Lit des issues en BD dans une table

		:type table_name: str
		:return:
		:rtype: list[JiraIssue]
		"""
		self.log.debug('')

		# Requête ...
		self.db_connector.securityCheckTableName(table_name)
		self.db_connector.execute('select * from %s' % table_name)

		# d'où la liste des champs de la table :
		table_fields = [description[0] for description in self.db_connector.cur.description]

		issues = []
		for r in self.db_connector.cur:
			self.log.debug("table_fields=" + pprint.pformat(table_fields))
			self.log.debug("list(r)     =" + pprint.pformat(list(r)))
			dic = dict(zip(table_fields, list(r)))
			self.log.debug("dic=" + pprint.pformat(dic))
			iss = JiraIssue(dic=dic)
			self.log.debug("iss=" + pprint.pformat(iss))
			issues.append(iss)

		return issues



	def finished(self):
		# 3. On a tout fini => on ferme tout proprement
		self.db_connector.finished()
