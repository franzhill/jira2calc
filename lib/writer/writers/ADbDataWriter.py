from abc import ABCMeta
import psycopg2

from lib.db_connector.exceptions import *
from lib.oo.import_oo_libs   import *
from lib.tools.tools         import *
from lib.writer.ADataWriter import ADataWriter
from lib.db_connector.db_connectors.PostgresqlConnector import PostgresqlConnector




class ADbDataWriter(ADataWriter,  metaclass=ABCMeta):
	"""
	Abstract DbDataWriter

	Ecrit des issues JIRA dans une BD (Postgresql)
	Les éléments de connexion à la BD sont implémentés.
	Mais la fonction d'écriture ne l'est pas

	TODO on pourrait factoriser avec ADbDataReader

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
		self.log.debug('')

		self.db_connector.connect()

		# Pour compatibilité historique:
		#self.conn = self.db_connector.conn
		#self.cur  = self.db_connector.cur



	def erase(self):
		self.log.debug('')
	# TODO maybe - Pour l'instant comme on drop et on recrée la table à chaque fois, pas utils



	def setParams(self, params):
		self.db_connector.setParams(params)



	def _writeInTable(self, issues, table_name):
		"""
		Ecrit des issues  en BD dans une table

		:type issues: list[JiraIssue]
		:type table_name: str
		:return: nb of rows inserted
		:rtype: int
		"""
		self.log.debug('')

		create_table = True  # 		if conf.conf['db']['ISSUE_TABLE_CREATE']:  # TODO mettre en conf, mettre en UI ...
		if (create_table):
			self._createTable(table_name)

		# 1. On récupère les noms des champs de la table "issue" :
		# (on aurait pu le faire à partir du fichier schema de création de cette table mais cela aurait
		#  nécéssité un parsing compliqué de la requête de création
		#  => la solution la plus simple est de faire une requête à la DB)

		# ATTENTION ! Psycopg ne propose apparemment pas de construction de requête avec échappement en ce qui concerne
		# le nom des tables
		# => être sûr de la provenance de la valeur que nous prenons
		# Proposons quand même une validation :

		# Requête ...
		self.db_connector.securityCheckTableName(table_name)
		self.db_connector.execute('select * from %s LIMIT 1' % table_name)

		# d'où la liste des champs de la table :
		table_fields = [description[0] for description in self.db_connector.cur.description]

		# ... et la liste des champs de la classe JiraIssue :
		issue_fields = table_fields  # Le mécanisme actuel impose l'identité des champs en DB et dans le modèle JiraIssue

		# 2. On insère ...

		sql_template = "INSERT into %s ( %s ) VALUES ( %s ) " % \
									 (table_name,
										', '.join(table_fields),
										', '.join(["%s"] * len(table_fields))
										)

		log.debug("sql_template=" + sql_template)

		nb_inserted_rows = 0
		for iss in issues:
			#fields = [getFieldVal(iss, field, case_insensitive=True) for field in issue_fields]
			#log.debug("fields=" + pprint.pformat(fields))
			# cur.execute(sql_template, [ str(vars(iss)[field]) for field in issue_fields])

			self.db_connector.execute(sql_template, [getFieldVal(iss, field, case_insensitive=True, raise_excp_if_not_found=True) for field in issue_fields])


			# TODO approche pas forcément optimale (à vérifier) - Pê mieux si on pouvait passer toutes les requêtes
			#        INSERT à execute en une seule fois/

			nb_inserted_rows += self.db_connector.cur.rowcount

		# Make the changes to the database persistent
		self.db_connector.commit()

		self.log.debug("Insertion complete : %d rows inserted" % (nb_inserted_rows,))
		return nb_inserted_rows



	def finished(self):
		# On a tout fini => on ferme tout proprement
		self.log.debug('')
		self.db_connector.finished()







	# ---------------------------------------------------------------------------
	# Privé
	# ---------------------------------------------------------------------------


	def _createTable(self, table_name):
		"""
		Crée une table en BD
		Va chercher le script de création de la table dans un fichier de conf nommé avec le nom de cette table.

		:param table_name:
		:type table_name: str
		:return:
		"""
		self.log.debug('Creating table : ' + table_name)
		self.db_connector.securityCheckTableName(table_name)

		with open('conf/db.sql.create_table.%s.sql' % (table_name,), 'r') as f:
			sql = f.read()  # .replace('\n', ' ')
		self.log.debug("sql=" + sql)
		sql = removeCommentsFromSql(sql)
		self.log.debug("sql=" + sql)
		sql = sql.replace('\n', ' ')
		self.log.debug("sql=" + sql)

		self.db_connector.execute(sql)
		# Make the changes to the database persistent
		# NB  possible improvement: calls to commit could be grouped
		self.db_connector.commit()




