import argparse
import pprint

from lib.ui.IUi import IUi
from lib.ui.IUiPentaho import IUiPentaho


class PentahoClui(IUi, IUiPentaho):
	"""
	Command Line User Interface

	@python-version 3.3.5
	@author fhill
	"""


	def __init__(self, parser = None):
		"""

		:param parser: parser d'options et d'arguments de ligne de commande, s'il existe déjà avant
		:type parser: ArgumentParser
		"""
		if not parser:
			parser = argparse.ArgumentParser()

		parser.add_argument('project'   ,       default="ALL", help="Projet (voir si nécéssaire ? TODO)")
		parser.add_argument('host'      ,       default=None,  help="Host de la BD utilisée par Pentaho")
		parser.add_argument('dbname'    ,       default=None,  help="Nom de la BD utilisée par Pentaho")
		parser.add_argument('user'      ,       default=None,  help="Utilisateur utilisé pour se connecter à la BD")
		parser.add_argument('--password', '-w', default=None,  help="Mot de passe de l'utilisateur" )
		parser.add_argument('--port'    , '-p', default=None,  help="Port spécifique à utiliser pour se connecter à la BD")
		parser.add_argument('--schema'  , '-s', default=None,  help="Schema spécifique à utiliser pour se connecter. Sinon le schema par défaut est pris")



		self.args = parser.parse_args()
		print(pprint.pformat(self.args))





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



	def getDbParamsDest(self):
		return \
		{
			'user'     : self.args.user,
			'host'     : self.args.host,
			'password' : self.args.password,
			'port'     : self.args.port,
			'dbname'   : self.args.dbname,
			'schema'   : self.args.schema,
		}


	def getDbParamsSource(self):
		# ici pour l'instant on utilise la même BD que ce soit pour la source ou la destination
		# TODO rendre possible que les BD source et dest soient différentes
		return \
		{
			'user'     : self.args.user,
			'host'     : self.args.host,
			'password' : self.args.password,
			'port'     : self.args.port,
			'dbname'   : self.args.dbname,
			'schema'   : self.args.schema,
		}
