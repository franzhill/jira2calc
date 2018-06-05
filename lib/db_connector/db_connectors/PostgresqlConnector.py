import psycopg2
from lib.db_connector.ADbConnector import ADbConnector
from lib.db_connector.exceptions import *
from lib.tools.tools import *



class PostgresqlConnector(ADbConnector):
	"""
	@python-version 3.3.5
	@author fhill
	"""

	def __init__(self, host, port, user, password, dbname, schema = "public"):
		"""
		"""
		super().__init__()

		self.host     = host
		self.port     = port
		self.user     = user
		self.password = password
		self.dbname   = dbname
		self.schema   = schema

		self.conn     = None
		self.cur      = None



	def setParams(self, params):
		self.log.debug('')
		self.log.debug('params=' + pprint.pformat(params))
		if safeReadDict(params, 'host'    , None) is not None: self.host      = safeReadDict(params, 'host'    , None)
		if safeReadDict(params, 'port'    , None) is not None: self.port      = safeReadDict(params, 'port'    , None)
		if safeReadDict(params, 'user'    , None) is not None: self.user      = safeReadDict(params, 'user'    , None)
		if safeReadDict(params, 'password', None) is not None: self.password  = safeReadDict(params, 'password', None)
		if safeReadDict(params, 'dbname'  , None) is not None: self.dbname    = safeReadDict(params, 'dbname'  , None)
		if safeReadDict(params, 'schema'  , None) is not None: self.schema    = safeReadDict(params, 'schema'  , None)



	def connect(self):
		self.log.debug('')
		self.log.debug("* Connecting to DB...")

		if (not self.dbname or not self.host or not self.user):
			raise DbConnectionException("One or more of the following: dbname, host, user - are not specified.")


		conn_str  = "dbname=%s user=%s host=%s" % (self.dbname, self.user, self.host)
		conn_str += " port=%s"     % (self.port,)     if self.port     else ''
		conn_str += " password=%s" % (self.password,) if self.password else ''

		self.log.debug("conn_str=" + conn_str)

		try:
			self.conn = psycopg2.connect(conn_str)

			# Open a cursor to perform database operations
			self.cur  = self.conn.cursor()

			# Connect to schema if specified
			# TODO ne marchera pas si on a pas d'abord accès au schema public
			# => utiliser le mode URI pour se connecter
			#  http://stackoverflow.com/questions/4168689/is-it-possible-to-specify-schema-when-connecting-to-postgres-with-jdbc
			#  ch. 31.1.1.2 de https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS
			self.log.debug("self.schema=" + self.schema)
			self.securityCheckTableName(self.schema)  # Le formalisme pour le nom du schema est le même que pour une table
			if self.schema is not None:
				self.log.debug("Connecting to schema [%s]" % (self.schema, ))
				self.cur.execute("SET search_path TO " +  self.schema)
				# Temporise pour attendre que le schema soit positionné côté BD
				# http://stackoverflow.com/questions/32812463/setting-schema-for-all-queries-of-a-connection-in-psycopg2-getting-race-conditi
				import time; time.sleep(0.2)

		except Exception as e:
			msg = "Erreur lors de la connection à la BD."
			raise DbConnectionException(msg, e)

		self.log.debug("* Connection succesful !")



	def execute(self, *args):
		self.log.debug('')
		self.log.debug("args=" + pprint.pformat(args))
		return self.cur.execute(*args)



	def commit(self):
		return self.conn.commit()



	def finished(self):
		# 3. On a tout fini => on ferme tout proprement
		self.log.debug('')
		self.cur.close()
		self.conn.close()



	def securityCheckTableName(self, table_name):
		"""
		Vérifie que le nom de la table passé est bien un nom de table SQL acceptable et est exempt
		 de tentative d'injection SQL ou autre chaîne non désirée

		:param table_name:
		:type table_name: str
		:return:
		"""
		if not isSingleWord(table_name):
			raise Exception("For security, only accepting table/schema/... names that are a single word. Table/schema/... name was: [%s]" % table_name)
		return True
