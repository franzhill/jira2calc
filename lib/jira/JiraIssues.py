import copy
import logging

from lib.conf.conf import conf
from lib.jira.JiraIssue import JiraIssue
from lib.tools.tools import *

#print("JiraIssues __name__ = " + __name__ )


class JiraIssues:
	"""
	Classe pour manipuler toutes les issues à la fois

	"""


	def __init__(self, issues):
		"""
		:param issues: liste des issues que cet object va contenir/manipuler
		:type issues: list[JiraIssue]
		"""
		self.issues = issues

		# Pour utiliser le logger commun à tout le projet:
		#logger = logging.getLogger("main")
		# Pour utiliser un logger spécifique à ce fichier : (le définir aussi dans le fichier de conf des logs, si différent du logger root)
		logger = logging.getLogger(__name__)

		self.setLogger(logger)




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



	def getIssues(self):
		"""

		:return: list[JiraIssue]
		"""
		return self.issues



	def copyTaskFieldsToSubtasksWhereEmpty(self):
		"""
			Nota la copie n'est  faite que pour les champs affichés dans Calc

		:return: self, ainsi cette classe est "chainable". Pour récupérer les issues, utiliser getIssues()
		"""
		self.log.debug('')
		issues      = JiraIssues(self.issues)
		issues_d    = issues.convertToDict()
		issues_subs = issues.extractSubTasks()

		for sub in issues_subs:
			self.log.debug('Current subtask = ' + str(sub))

			# Lookup for parent
			try:   # /!\ Le parent n'est pas forcément dans les issues si l'import est partiel par ex. ...
				sub_parent = issues_d[sub.parent_id]
				self.log.debug('  Parent = ' + str(sub_parent))

				# Copy fields from parent where subtask fields are empty
				# !!! It is assumed all fields in JiraIssue are "domain" fields (i.e. have a Jira meaning)
				for k, v in vars(sub).items():

					# Ne faire la copie que pour les champs qu'on affiche dans le Calc au final
					if k in conf['oo']['WRITE_ISSUES_FIELDS']:

						if not v :
							# Set from parent
							self.log.debug("  Copying from parent key = %s, value = %s " % (k, vars(sub_parent)[k],))
							setattr(sub, k, vars(sub_parent)[k])
			except KeyError:
				# ... dans ce cas-là on ne fait rien bien évidemment
				pass

		return self



	def convertToDict(self):
		"""
		Renvoie un dictionnaire des issues, indexé par leur id
		:return:
		"""
		self.log.debug('')

		dict={}
		for i in self.issues:
			dict[i.id] =  i
		return dict


	def extractSubTasks(self):
		"""

		:return: list[JiraIssue]  liste ne contenant que les sous-tâches
		"""
		self.log.debug('')

		list= []
		for i in self.issues:
			self.log.debug('Current issue = ' + str(i))
			if (i.subtask):
				list.append(i)
		return list



	def sortOn(self, field, direction="ASC"):
		"""
		Trie les issues sur le champ fourni (attribut de la classe JiraIssue)

		:param field: string
		:param direction: direction du tri, 'ASC' ou 'DESC'
		:return:
		"""
		direction_accepted_vals =  ['ASC', 'DESC']
		if direction not in direction_accepted_vals:
			direction = direction_accepted_vals[0]
			self.log.warning("Provided unknown direction for sort (%s). Expected one of (%s). Failback direction is to: %s" % (direction, direction_accepted_vals, direction))

		# Fonction lib.tools.tools.getClassProperties() pas "production-ready"
		# => à la place on va faire à la mode Python "it's better to ask for forgiveness..."
		#if field not in getClassProperties(JiraIssue):
		#	self.log.warning("Field provided (%s) does not exist in object JiraIssue. Silently not performing sort.")


		try:
			self.issues.sort(key=lambda obj: getattr(obj, field), reverse=(direction == 'DESC'))
		except AttributeError as e:
			self.log.warning("Sort requested on unknown attribute (%s) for JiraIssue. Silently ignoring, not performing sort." % (field,))
			pass



	def filterCommandes(self):
		"""
			Ne garde que les issues de type commande

			:rtype: list[JiraIssue]
			:return: la liste filtrée
		"""
		ret_issues = []
		for iss in self.issues:
			if iss.isTypeCommande():
				# ON effectue une copie en surface car JiraIssue ne contient pas de listes ou objets
				# (hormis le logger que justement on ne veut pas deep copier car cela pose pb)
				#ret_issues.append(copy.deepcopy(iss))
				ret_issues.append(copy.copy(iss))
		return ret_issues



	def filterPaiements(self):
		"""
			Ne garde que les issues de type commande

			:rtype: list[JiraIssue]
			:return: la liste filtrée
		"""
		ret_issues = []
		for iss in self.issues:
			if iss.isTypePaiement():
				# Cf commentaire filterCommandes
				# ret_issues.append(copy.deepcopy(iss))
				ret_issues.append(copy.copy(iss))
		return ret_issues