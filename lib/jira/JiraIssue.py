from datetime  import datetime, date
from decimal import *

from lib.conf.conf import conf
from lib.jira.exceptions import *
from lib.tools.JsonReader import *




class JiraIssue:
	"""
	Représentation d'une issue (tâche, demande) JIRA

	Comprend tous les champs JIRA nous intéressant pour notre propos

	Il est pré-supposé qu'il n'y a que 2 niveaux de "parentalité" : des tâches et des sous-tâches (Commandes et Paiements)
	"""


	typeCommande = conf['jira']['ISSUE_TYPE_COMMANDE']
	typePaiement = conf['jira']['ISSUE_TYPE_PAIEMENT']


	def __init__(self, json_=None, dic=None):
		"""
		Initialise à partir de : soit un json issu d'une requête REST vers le serveur JIRA,
		                         soit un dictionnaire Python {attribut_JiraIssue : valeur}
		L'un des 2 paramètres doit être fourni.

		Dans le cas d'une création à partir de dictionnaire : attention, les clés du dictionnaire
		 fourni doivent correspondre à des champs réel de JiraIssue.
		Il n'y a cependant pas de contrôle sur les clés et pas de définition des "champs réels"
		de JiraIssue (=> champs réels = ceux définis dans _initFromJson() ). Toute clé fournie se verra
		convertie en champ de la JiraIssue construite.
		Attention donc, fournir une mauvaise clé pourrait avoir une incidence en aval dans les
		 composants manipulant JiraIssue et s'attendant à trouver les "champs réels"
		Attention aussi, fournir un dictionnaire incomplet pourrait résulter en une JiraIssue ayant
		"des trous".


		:param json_:
		:param dic: Attention, doit aussi contenir la clé : type (= JiraIssue.typeCommande ou JiraIssue.typePaiement)
		:type json_: str|json
		:type dic: dict
		"""
		# Pour utiliser le logger commun à tout le projet:
		#logger = logging.getLogger("main")
		# Pour utiliser un logger spécifique à ce fichier : (le définir aussi dans le fichier de conf des logs, si différent du logger root)
		logger = logging.getLogger(__name__)
		self.setLogger(logger)


		if (json_ and dic):
			raise JiraIssueException("Upon build [%s] request, json and dictionary provided. Unsure which to take. Provide only one.")

		if json_:
			self._initFromJson(json_)
		elif dic:
			self._initFromDict(dic)
		else:
			raise JiraIssueException("Cannot build [%s], must provide a json or a dictionary.")



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



	def asCommande(self):
		"""
		Définit la JiraIssue comme étant une commande.
		Utile dans les cas où l'on reconstitue des JiraIssue "précises" (qualifiées commen étant commande ou paiement)
		à partir de JiraIssues génériques ayant perdu cette distinction.
		:return:
		"""
		self.type                = JiraIssue.typeCommande
		self.montant_cmde        = self.montant
		self.id                  = self.issue_id
		self.date_previ_paiement = self.date_previ_paiement if (hasattr(self, 'date_previ_paiement')) else ''
		self._initCalculated()



	def asPaiement(self):
		"""
		Définit la JiraIssue comme étant une paiement
		Cf asCommande()
		:return:
		"""
		self.type             = JiraIssue.typePaiement
		self.montant_paiement = self.montant
		self.id               = self.issue_id
		self._initCalculated()



	def isTypeCommande(self):
		return self.type == JiraIssue.typeCommande



	def isTypePaiement(self):
		return self.type == JiraIssue.typePaiement



	# ---------------------------------------------------------------------------
	# Privé
	# ---------------------------------------------------------------------------

	def _initFromJson(self, json_):

		jr = JsonReader(json_)

		# Champs extraits de JIRA
		# ------------------------

		self.id                  = jr.readSafe('id')
		self.self                = jr.readSafe('self')
		self.key                 = jr.readSafe('key')
		self.summary             = jr.readSafe('fields', 'summary')
		self.type                = jr.readSafe('fields', 'issuetype', 'name')
		self.subtask             = jr.readSafe('fields', 'issuetype', 'subtask')
		self.entite              = jr.readSafe('fields', 'customfield_10099', 'value') # idem
		self.bureau              = self.entite                                         # alias
		self.marche              = jr.readSafe('fields', 'customfield_10071', 'value') # idem
		self.montant_cmde        = jr.readSafe('fields', 'customfield_10054')          # montant prévu
		self.montant_paiement    = jr.readSafe('fields', 'customfield_10067')          # montant paiement
		self.nom                 = jr.readSafe('fields', 'customfield_10078', 'value')
		self.nom_du_projet       = jr.readSafe('fields', 'customfield_10033', 'value')
		self.creator             = jr.readSafe('fields', 'creator', 'name')
		self.created             = jr.readSafe('fields', 'created')
		self.description         = jr.readSafe('fields', 'description')
		self.project_id          = jr.readSafe('fields', 'project', 'id')
		self.project_name        = jr.readSafe('fields', 'project', 'name')
		self.parent_id           = jr.readSafe('fields', 'parent', 'id')
		self.parent_key          = jr.readSafe('fields', 'parent', 'key')
		self.parent_summary      = jr.readSafe('fields', 'parent', 'fields', 'summary')
		self.status              = jr.readSafe('fields', 'status', 'name')
		self.centre              = jr.readSafe('fields', 'customfield_10016', 'value')
		self.domaine             = jr.readSafe('fields', 'customfield_10011', 'value')
		self.axe                 = jr.readSafe('fields', 'customfield_10041', 'value')
		self.centre              = jr.readSafe('fields', 'customfield_10044', 'value')
		self.browsable_url       = conf['jira']['BROWSER_BASE_URL'] + str(self.key)
		self.contact             = jr.readSafe('fields', 'customfield_10106', 'displayName')

		self._initCalculated()



	def _initFromDict(self, dic):
		"""
		Si 'type' n'est pas indiqué dans le dictionnaire fourni alors il faudra appeler
		 asCommande() ou asPaiement() derrière.

		:param dic: dictionnaire de type {champ_JiraIssue : valeur}
		:type  dic: dict
		:return:
		"""

		# Initialise tous les champs aux valeurs par défaut
		self._initFromJson('{"this":"is a dummy object"}')

		for k,v in dic.items():

			# Conversion de types
			# En effet, dic proviendra vraisemblablement d'une lecture de table, les types renvoyés par la base
			# ne sont pas forcément ceux attendus pour notre JiraIssue (que des strings)
			if    (type(v) in [datetime, date] ):
				self.log.debug("Found field [%s] of type datetime/date, converting to string: [%s]" % (k, v))
				v = v.strftime("%Y-%m-%d")
				self.log.debug("Converted value is: [%s]" % (v,))
			elif (type(v) in [int, Decimal]):
				self.log.debug("Found field [%s] of type int, converting to string: [%s]" % (k, v))
				v = str(v)

			setattr(self, k, v)

		if hasattr(self, 'type'):
			if self.type == JiraIssue.typeCommande:
				self.asCommande()
			elif self.type == JiraIssue.typePaiement:
				self.asPaiement()
			else:
				# Ne pas oublier d'appeler asCommande() or asPaiement() soi-même alors !
				pass
				#raise Exception("Programming Exception, should not happen (type=[%s])" %(self.type,))



	def _initCalculated(self):
		"""
		Initialise les champs "calculés" (i.e. non fournis extérieurement) (autrement dit "redondants")

		:return:
		"""

		# Pour utilisation CALC ou Pentaho/Saiku) :

		try:
			# On suppose qu'il n'y a que 2 niveaux de "parentalité" : des tâches et des sous-tâches
			# Le sort_idx a pour but d'être affiché dans le rapport dans une colonne qui permettra que le tri dessus (ex. dans Calc)
			# fasse apparaître naturellement les lignes "sous-tâches" sous la ligne de la tâche parente.
			# On suppose aussi que les id (Jira) des tâches ont pour format 5 chiffres.
			if self.parent_id:
				self.sort_idx = self.parent_id + '_' + self.id
			else:
				# On suppose donc qu'il s'agit d'une tâche qui n'est pas une sous-tâche
				self.sort_idx = str(self.id) + '_' + '00000'
		except KeyError: pass


		# Pour les insertions dans les tables 'commande' et 'paiement' :

		self.montant                 = self.montant_cmde if self.isTypeCommande() else (self.montant_paiement if self.isTypePaiement() else -1)
		self.issue_id                = self.id


		# Pour Saiku en particulier ... :

		self.c_status                = self.status     if self.isTypeCommande() else None
		self.c_key                   = self.key        if self.isTypeCommande() else None
		self.c_parent_key            = self.parent_key if self.isTypeCommande() else None

		self.p_status                = self.status     if self.isTypePaiement() else None
		self.p_key                   = self.key        if self.isTypePaiement() else None
		self.p_parent_key            = self.parent_key if self.isTypePaiement() else None

		self.date_commande_ymd       = self._convertDateToYmd(self.date_commande)
		self.date_commande_y         = self._convertDateToY  (self.date_commande)
		self.date_commande_m         = self._convertDateToM  (self.date_commande)
		self.date_commande_w         = self._convertDateToW  (self.date_commande)



	# ------------------------------------------------------------------------------
	# Fonctions de prémâchage de données pour Saïku
	# ------------------------------------------------------------------------------

	def _convertDateToYmd(self, date):
		self.log.debug("Current JiraIssue = " + str(self))
		if date:
			self.log.debug("date=" + pprint.pformat(date))
			return datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
		else:
			return None

	def _convertDateToY(self, date):
		if date:
			return datetime.strptime(date, '%Y-%m-%d').strftime('%Y')
		else:
			return None

	def _convertDateToM(self, date):
		if date:
			return datetime.strptime(date, '%Y-%m-%d').strftime('%m')
		else:
			return None

	def _convertDateToW(self, date):
		"""
		Renvoie la semaine
		:param date:
		:return:
		"""
		if date:
			return datetime.strptime(date, '%Y-%m-%d').isocalendar()[1]
		else:
			return None


	def __repr__(self):
		return str(vars(self))
