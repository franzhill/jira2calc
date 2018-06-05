from lib.reader.readers.ADbDataReader import ADbDataReader
from lib.jira.JiraIssues      import JiraIssues
from lib.conf.conf import conf


class DwDbDataReader(ADbDataReader):
	"""
	Lit dans la partie de la BD qui constitue le  "Data Warehouse" (aka "Puits") càd
	les tables normalisées au plus proches de Jira.

	@python-version 3.3.5
	@author fhill
	"""

	tableCommande = conf['db']['DW_COMMANDE_TABLE_NAME']
	tablePaiement = conf['db']['DW_PAIEMENT_TABLE_NAME']



	def readIssues(self, project_name=None):
		"""
		Pour des raisons de compatibilité historique (TODO fix) le paramètre project
		fait partie de la signature de cette fonction, mais il est ici ignoré

		:param project_name: ignoré, ne pas passer
		:return: list[JiraIssue]
		"""
		# TODO optimisation : voir si le DataReader est connecté ou pas encore, si pas, le connecter
		self.log.debug('')

		issues_C = self.readFromTable(DwDbDataReader.tableCommande)
		issues_P = self.readFromTable(DwDbDataReader.tablePaiement)

		for iss in issues_C: iss.asCommande()
		for iss in issues_P: iss.asPaiement()

		self.nbReadC = len(issues_C)
		self.nbReadP = len(issues_P)

		return issues_C + issues_P



	def getProjects(self, sort=True):
		return []



	def getReportMsg(self):
		self.log.debug('')
		msg  = "[%d] tâches JIRA extraites depuis le Data Store : \n" % (self.nbReadC + self.nbReadP, )
		msg += "  - [%s] commandes insérées dans la table [%s] \n" % (self.nbReadC, DwDbDataReader.tableCommande,)
		msg += "  - [%s] commandes insérées dans la table [%s] \n" % (self.nbReadP, DwDbDataReader.tablePaiement,)
		return msg

