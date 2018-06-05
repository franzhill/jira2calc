import logging
import os
from configparser import ConfigParser




class Configuration():
	"""
	@python-version 3.3.5
	@author fhill
	"""

	def __init__(self, *args):
		"""

		:param args: list of files to load configuration from, in reverse order of precedence (i.e. configuration values
		             in last file override the same values defined in files before)
		"""
		# Pour utiliser le logger commun à tout le projet:
		# logger = logging.getLogger("main")
		# Pour utiliser un logger spécifique à ce fichier : (le définir aussi dans le fichier de conf des logs, si différent du logger root)
		logger = logging.getLogger(__name__)

		self.setLogger(logger)

		if (len(args) == 0):
			raise Exception("No configuration file passed to class Configuration. Please provide at least one.")

		self.log.info("Loading config files in this order: %s" %(args,))
		self.conf = ConfigParser()
		self.conf.read(args, "utf-8")

		#for f in args:
		#	self.log.debug("Loading conf file : " + f)
		#	if os.path.exists(f):
		#		self.log.debug("Found conf file : " + f)
		#		self.conf.read(f)
		#	else:
		#		self.log.debug("Did NOT find conf file : %s . Skipping ..." % (f, ))

		self.log.debug("self.conf['jira']['REST_BASE_URL'] = " + self.conf['jira']['REST_BASE_URL'] )
		for k,v in self.conf['jira'].items():
			self.log.debug("%s = %s" % (k, v,))





	# ---------------------------------------------------------------------------
	# Public
	# ---------------------------------------------------------------------------

	def setLogger(self, logger):
		"""
		 Pour injecter un logger spécifique.
		 Sinon, un logger par défaut sera mis en place (voir __init__)

		:type logger: logging.Logger
		"""
		self.log = logger


	def getConf(self):
		return self.conf


	def __getitem__(self, item):
		return self.conf[item]