from lib.writer.writers.ADbDataWriter import ADbDataWriter
from lib.jira.JiraIssues      import JiraIssues
from lib.conf.conf import conf


class DwDbDataWriter(ADbDataWriter):
	"""
	Ecrit dans la partie de la BD qui constitue le  "Data Warehouse" (aka "Puits) càd
	les tables normalisées au plus proches de Jira.

	@python-version 3.3.5
	@author fhill
	"""

	tableCommande = conf['db']['DW_COMMANDE_TABLE_NAME']
	tablePaiement = conf['db']['DW_PAIEMENT_TABLE_NAME']


	def writeIssues(self, issues):
		self.log.debug('')
		jissues = JiraIssues(issues)

		self.nbRowsInsertedC = self._writeInTable(jissues.filterCommandes(), DwDbDataWriter.tableCommande)
		self.nbRowsInsertedP = self._writeInTable(jissues.filterPaiements(), DwDbDataWriter.tablePaiement)
		self.nbRowsInserted  = self.nbRowsInsertedC + self.nbRowsInsertedP

		return self.nbRowsInserted




	def getReportMsg(self):
		self.log.debug('')
		msg  = "[%s] tâches JIRA insérées dans le Data Warehouse : \n" % (self.nbRowsInserted,)
		msg += "  - [%s] commandes insérées dans la table [%s] \n" % (self.nbRowsInsertedC, DwDbDataWriter.tableCommande,)
		msg += "  - [%s] commandes insérées dans la table [%s] \n" % (self.nbRowsInsertedP, DwDbDataWriter.tablePaiement,)
		return msg

