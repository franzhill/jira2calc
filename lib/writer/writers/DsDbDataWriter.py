from lib.writer.writers.ADbDataWriter import ADbDataWriter
from lib.conf.conf import conf

class DsDbDataWriter(ADbDataWriter):
	"""
	Ecrit dans la partie de la BD qui constitue le "Data Store" (aka "Magasin de données") càd
	les tables dénormalisées pour utilisation par les moteurs de rendu d'hypercube (Saïku)
	 i.e. à l'heure d"écriture dans les tables
	 - issue

	@python-version 3.3.5
	@author fhill
	"""

	tableDsIssue     = conf['db']['DS_ISSUE_TABLE_NAME']
	tableDsCommande  = conf['db']['DS_COMMANDE_TABLE_NAME']



	def writeIssues(self, issues):
		self.log.debug('')
		self.nbRowsInsertedI = self._writeInTable(issues, DsDbDataWriter.tableDsIssue)
		self.nbRowsInsertedC = self._writeInTable(issues, DsDbDataWriter.tableDsCommande)
		self.nbRowsInserted = self.nbRowsInsertedI + self.nbRowsInsertedC

		# TODO maybe ICI éventuellement ajouter les pseudo issues de dates permettant côté Saïku de faire les rapports par mois en (toutes lettres)

		return self.nbRowsInserted



	def getReportMsg(self):
		self.log.debug('')
		msg = "[%s] tâches JIRA insérées dans le Data Store :\n" % (self.nbRowsInserted, )
		msg += "  - [%s] commandes/paiements insérés dans la table [%s] \n" % (self.nbRowsInsertedI, DsDbDataWriter.tableDsIssue,)
		msg += "  - [%s] commandes insérées dans la table [%s] \n"          % (self.nbRowsInsertedC, DsDbDataWriter.tableDsCommande,)

		return msg




