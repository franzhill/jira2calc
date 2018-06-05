from lib.oo.import_oo_libs   import *
from lib.tools.tools         import *
from lib.writer.writers.ADbDataWriter import ADbDataWriter

# DEPRECATED

class MockDbDataWriter(ADbDataWriter):

	# ---------------------------------------------------------------------------
	# Public
	# ---------------------------------------------------------------------------


	def connect(self, host, user, password, port, dbname):

		self.log.debug('')
		self.log.debug("* Connecting to DB...")

		conn_str  = "dbname=%s user=%s host=%s" % (dbname, user, host)
		conn_str += " port=%s"     % (port,)     if port     else ''
		conn_str += " password=%s" % (password,) if password else ''

		log.debug("conn_str=" + conn_str)

		return



	def erase(self):
		self.log.debug('')
		return



	def writeIssues(self, issues):
		self.log.debug('')
		return



	def getReportMsg(self):
		return "On est dans un mock, donc tout s'est bien passé ;o)"