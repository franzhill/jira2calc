import json
from lib.oo.exceptions  import *
from lib.oo.import_oo_libs import *
from lib.writer.ADataWriter import ADataWriter
from lib.jira.JiraIssue import JiraIssue
import lib.oo.pyoo_override
import pyoo
from lib.tools.tools import *


class OoDataWriter(ADataWriter):
	"""
	Gère l'écriture des issues dans OpenOffice (LibreOffice plus précisement)

	TODO renommer en CalcDataWriter

	@python-version 3.3.5
	@author fhill
	"""

	def __init__(self, host, port):

		super().__init__()

		self.host   = host
		self.port   = port
		self.desktop= None
		self.doc    = None



	# ---------------------------------------------------------------------------
	# Public
	# ---------------------------------------------------------------------------


	def connect(self, file=None):
		"""
		:param file: chemin de fichier dans lequel écrire. Si pas fourni, un nouveau sera ouvert
		"""
		self.log.debug('')

		self.log.debug("* Launching OO server...")
		self._launchOoServer()

		self.log.debug("* Connecting writer to OO server...")
		self._connect()
		self._openSpreadsheet(file)



	def erase(self):
		self.log.debug('')
		self._erase()



	def setParams(self, params):
		if safeReadDict(params, 'host'    , None) is not None: self.host      = safeReadDict(params, 'host'    , None)
		if safeReadDict(params, 'port'    , None) is not None: self.port      = safeReadDict(params, 'port'    , None)



	def writeIssues(self, issues):
		self.log.debug('')
		return self._writeIssues(issues)



	def finished(self):
		# Rien de particulier à faire
		self.log.debug('')
		pass



	def getReportMsg(self):
		# Pas de rapport particulier
		return ''



	# ---------------------------------------------------------------------------
	# Privé
	# ---------------------------------------------------------------------------

	def _launchOoServer(self):
		"""
		Pour les tests
		Lance le process LibreOffice mode serveur en background... (on peut aussi le lancer séparément, "à la main")
		"""

		# Ne marche pas :
		##from subprocess import check_output
		##check_output('"C:\Program Files (x86)\LibreOffice 4\program\soffice" -accept="socket,host=localhost,port=2002;urp;" ', shell=True)

		try:
			import subprocess
			cmd = '"' + conf['path']['PATH_TO_OO_SOFFICE'] + '" -accept="socket,host='+str(self.host)+',port='+str(self.port)+';urp;" '
			self.log.debug("cmd="+cmd)
			subprocess.Popen(cmd)
			import time
			time.sleep(2)
		except Exception as e:
			raise OOException("Erreur lors du lancement de LibreOffice en mode serveur", e)



	def _connect(self):
		"""
		On se connecte à l'instance OO
		(préalablement lancée dans une terminal de commande Windows avec la commande suivante
		  "C:\Program Files (x86)\LibreOffice 4\program\soffice" -accept="socket,host=localhost,port=2002;urp;"
		)

		:return: port on which connection was finally made
		"""
		#print(pyoo)
#		self.log.debug(pyoo)

		try_port = self.port
		nb_tries = 10
		e_ = None

		while ( nb_tries > 0 ):
			try:
				self.desktop = lib.oo.pyoo_override.Desktop(self.host, try_port) #pyoo.Desktop(self.host, self.port)
				self.log.debug("connect() DONE")
				return try_port
			except Exception as e:
				try_port_failed = try_port
				try_port += 1
				nb_tries -= 1
				msg_strategy    = "Will try again on port %s" % (try_port,) if (nb_tries > 0 ) else "Giving up trying other ports, raising error"
				msg             = "Failed to connect to OO on port %s. %s.\n Original cause exception is : %s" % (try_port_failed, msg_strategy, str(e))
				self.log.warning(msg  )
				e_ = e

		# Failed to connect
		raise OOException("Impossible de se connecter à OO sur le port spécifié. Veuillez fermer Libre Office ou modifier le port de connexion dans la configuration.", e_)



	def _openSpreadsheet(self, path=None):
		"""
		Ouvre un document LibreOffice et l'assigne à cette classe comme "docuement courant"

		:param path: full path to spreadsheet e.g. "/path/to/spreadsheet.ods"
		             Si pas fourni, ouvre un (nouveau) document sans nom
		:return:
		"""
		if not path:
			self.doc = self.desktop.create_spreadsheet()
		else:
			self.doc = self.desktop.open_spreadsheet(path)



	def _writeIssues(self, jira_issues, write_header=True):
		"""
		 Stratégie d'écriture "matricielle" plus rapide que l'écriture par cellule )
		:param jira_issues:
		:type jira_issues: list[JiraIssue]
		:return: le nombre de lignes écrites
		"""

		sheet = self._getDestSheet()

		# Liste ordonnée des champs à écrire dans OO
		fields = json.loads(conf['oo']['WRITE_ISSUES_FIELDS'])

		# Header
		if write_header:
			col = 0
			for field in fields:
				#self.log.debug("current field=" + field)
				sheet[0, col].value            = field                      # On peut optimiser ... : inutile d'écrire la ligne de libellés à chaque fois
				sheet[0, col].font_weight      = pyoo.FONT_WEIGHT_BOLD
				sheet[0, col].background_color = 0xbfbfbf
				col += 1

		# Données
		nb_row = len(jira_issues)
		nb_col = len(fields)

		self.log.debug("nb_row, nb_col = %s %s"  % (nb_row, nb_col) )

		matrix = [['init' for i in range(nb_col)] for j in range(nb_row)]   # initialisation de la matrice de données

		row = 0
		col = 0
		for iss in jira_issues:
			for field in fields:
				val = vars(iss)[field]
				self.log.debug("About to set : matrix[%s][%s] = %s" % (row, col, val))
				matrix[row][col] = self._formatVal(val)
				col += 1
			row += 1
			col = 0

		shift = 1 if write_header else 0
		sheet[0+shift:nb_row+shift, 0:nb_col].values = matrix

		return row



	def _getDestSheet(self):
		"""
		Dans le document courant, récupère la feuille dans laquelle écrire les données
		Jira (voir fichier de configuration)
		@todo this could be a attribute of this class rather than a getter
		:return: pyoo.Sheet
		"""
		sheet = self._getSheet(self.doc, conf['oo']['WRITE_ISSUES_IN_SHEET'], conf['oo']['ISSUE_SHEET_POSITION'])
		return sheet



	def _getSheet(self, doc, id, index = None):
		"""
		Fonction d'accès "sécurisée" à un onglet dans le document courant

		Si l'onglet existe, celui-ci est retourné.
		S'il n'existe pas, celui-ci est d'abord créé puis retourné.

		:param doc: document OO (Feuille de calcul)
		:param id: Indentifiant de l'onglet : soit son nom soit son index lorsqu'il existe.
		                         S'il n'existe pas, alors il s'agit de son nom.
		:type id:  str|int
		:param index: Dans le cas d'une création d'onglet, spécifie ou le placer par rapport aux autres.
		              Selon pyoo: "If an optional index argument is not provided then the created sheet is appended at the end"
		:type index: int
		:return:
		:rtype: pyoo.Sheet
		"""

		if index == -1 : index = None

		# Vérifier si l'onglet existe
		# Vilain, mais bon ... à défaut d'avoir une fonction pour en tester l'existence, on tente l'accès et on attrappe l'exception le cas échéant
		# (apparemment c'est la mode dans Python ;o) )
		try:
			sheet = self.doc.sheets[id]
		except KeyError as e:
			self.log.info("Onglet [" + id + "] non détecté. => Création...")
			sheet = self.doc.sheets.create(id, index)
		return sheet



	def _erase(self):
		"""
		Vide la feuille destination des données Jira du document courant
		Pour des raisons techniques il faut spécifier une colonne max et une ligne max : voir fichier de conf
		(en effet il ne semble pas possible de connaître l'étendue des cellules contenant des données)

		:param sheet:
		:return:
		"""
		self.log.debug('')
		sheet = self._getDestSheet()

		return self._eraseSheet_1(sheet)



	def _eraseSheet_1(self, sheet):
		"""
		Implémentation de l'effacement d'une feuille : effacement par application d'une matrice de valeurs (vides),
		avec dimension de la matrice prédéfinie (en conf)
		Bien plus rapide que l'effacement cellule par cellule

		:param sheet:
		:return:
		"""
		self.log.debug('')
		#sheet[0:10, 0].values = "0:10, 0"

		MAX_NB_ROWS=int(conf['oo']['ERASE_UP_TO_ROW'])
		MAX_NB_COLS=int(conf['oo']['ERASE_UP_TO_COL'])

		matrix_erase = [['' for i in range(MAX_NB_COLS)] for j in range(MAX_NB_ROWS)]
		sheet[0:MAX_NB_ROWS, 0:MAX_NB_COLS].values = matrix_erase



	def _formatVal(self, val):
		"""
		Formate la valeur issue de Jira dans le format attendu pour le fichier Calc

		:param val:
		:return:
		"""
		ret_val = ""
		if val is None:
			ret_val = ""
		elif isNumeric(val):
			# remplace , par .
			# On pourrait utiliser un formatage de float, mais pour aller plus vite vu qu'on sait déjà que c'est un float :
			ret_val = str(val).replace('.', ',')
		else:
			ret_val = str(val)

		return ret_val