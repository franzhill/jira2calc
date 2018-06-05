from lib.ui.IUi import IUi


class GenericClui(IUi):
	"""
	Command Line User Interface

	@python-version 3.3.5
	@author fhill
	"""


	def __init__(self, args):
		self.args = args


	def initialize(self, app):
		# Ici dans ce cas rien de particulier de plus à faire
		self.app = app



	def run(self):
		self.app.importJiraIssuesForProject()


	def error(self, msg):
		# Print on "Command Line Ouptut" i.e. stdout
		print("ERREUR : " + msg)



	def info(self, msg):
		# Print on "Command Line Ouptut" i.e. stdout
		print("INFO : " + msg)



	def getProject(self):
		return self.args.project



	def getDbParamsSource(self):
		return \
		{
			'user'     : self.args.source_params.user,
			'host'     : self.args.source_params.host,
			'password' : self.args.source_params.password,
			'port'     : self.args.source_params.port,
			'dbname'   : self.args.source_params.dbname,
		}



	def getDbParamsDest(self):
		return \
		{
			#'user'     : self.args.dest_params.user,  #TODO si la clé n'existe pas, pas d'erreur
			'host'     : self.args.dest_params.host,
			#'password' : self.args.dest_params.password, #TODO si la clé n'existe pas, pas d'erreur
			'port'     : int(self.args.dest_params.port),
			#'dbname'   : self.args.dest_params.dbname, #TODO si la clé n'existe pas, pas d'erreur
		}



	def getFile(self):
		# TODO pour l'instant pas supporté:
		return None