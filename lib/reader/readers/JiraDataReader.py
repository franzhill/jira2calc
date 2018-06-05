from lib.conf.conf import conf
from lib.jira.JiraIssue     import JiraIssue
from lib.jira.JiraIssueType import JiraIssueType
from lib.jira.jira_requests import *
from lib.reader.ADataReader import ADataReader




class JiraDataReader(ADataReader):
	"""
	@python-version 3.3.5
	@author fhill
	"""

	def __init__(self, url_base, user_name, user_password):
		"""
		TODO pouvoir spécifier le port (e.g. un serveur en local peut très bien répondre sur le 8080 plutôt que le 80)
		:param url_base:
		:param user_name:
		:param user_password:
		"""
		super().__init__()
		self.jrb = JiraRequestBuilder(url_base, user_name, user_password)



	def getProjects(self, sort=True):
		"""
		Effectue une requête REST pour récupérer les projets JIRA

		:param sort: Trie les projets alphabétiquement
		:type  sort: bool
		:rtype: list[JiraProject]
		"""
		self.log.debug('')

		r = self.jrb.buildRequest('project')

		self.log.debug("url=" + r.getUrl())

		parsed_json = r.execute()
		self.log.debug("parsed_json=" + str(parsed_json))
		projects = parsed_json

		# Conversion du JSON au format objet Jira (ici JiraProject)
		jira_projects = []
		for p in projects:
			jira_p = JiraProject(p)
			jira_projects.append(jira_p)

		if sort:
			jira_projects.sort()

		return jira_projects



	def connect(self, *args):
		# Pas besoin de connexion ici, c'est du requêtage REST
		pass



	def getIssues(self, max_nb_issues=-1, max_nb_issues_per_request=99, jql=''):
		"""
		Effectue une (ou plusieurs) requête(s) REST pour récupérer les issues JIRA
		Requête de "plus bas niveau" (permet de spécifier les paramètres techniques)

		:param max_nb_issues:              Aller chercher X issues Jira, -1 pour toutes
		:param max_nb_issues_per_request:  Paramètre technique: aller chercher les issues par lots (requête REST) de tant
		:rtype: list[JiraIssue]
		"""
		self.log.debug('')

		req_max_results = max_nb_issues_per_request
		get_so_many_issues = max_nb_issues

		# Le nombre d'issues renvoyées par requête REST est limité par la proprité JIRA 'jira.search.views.default.max'
		# Cf https://docs.atlassian.com/jira/REST/server/#api/2/search-search
		# Ce paramètre peut être modifié par un admin dans l'interface JIRA.
		# Par défaut i.e. si aucun admin n'y a jamais touché sa valeur est 50
		# Cependant nous allons considérer que nous n'avons pas la main sur ce paramètre => obligé de "paginer"
		# Nous ne savons pas à combien est positionnée cette propriété (par défaut 50) et donc pour tenter de limiter
		# le nb de requêtes total qu'on aura à faire nous allons tenter d'en demander bien plus à la fois.
		# (sachant que "If you specify a value that is higher than this number, your search results will be truncated.")

		continue_pagination = True
		req_page = 1
		req_start_at = 0
		jira_issues = []  # initialisation. Stocke toutes les issues au format JiraIssue

		while (continue_pagination):

			r = self.jrb.buildRequest('search')
			r.addParams({'startAt': req_start_at, 'maxResults': req_max_results, 'jql': jql})

			self.log.debug("url=" + r.getUrl())
			self.log.debug("Currently requesting:")
			self.log.debug(" - page     =" + str(req_page))
			self.log.debug(" - sartAt   =" + str(req_start_at))

			parsed_json = r.execute()

			# Previsoulsy, without the jrb.../
			# url_base = JIRA_REST_BASE_URL + 'search'
			# url = add_get_params(url_base, {'startAt': req_start_at, 'maxResults': req_max_results})
			# r = requests.get(url, auth=(JIRA_REST_USERNAME, JIRA_REST_PASSWORD), verify=False)

			resp_total_nb = parsed_json['total']
			resp_max_results = parsed_json['maxResults']

			self.log.debug("Response:")
			self.log.debug(" - Total nb of issues      = " + str(resp_total_nb))
			self.log.debug(" - Max results per request = " + str(resp_max_results))

			# Toutes nos issues JIRA, encore au format JSON :
			issues = parsed_json['issues']

			# Conversion des issues JIRA au format JSON vers un dictionnaire Python d'objets JiraIssue...

			for issue in issues:
				jira_issue = JiraIssue(issue)
				jira_issues.append(jira_issue)
			# break # pour debug

			# Calculate next params for next request (next page of requests)
			req_page += 1
			req_start_at += resp_max_results
			if (req_start_at > resp_total_nb or (get_so_many_issues != -1 and req_start_at >= get_so_many_issues)):
				continue_pagination = False

			self.log.debug("Next request will be:")
			self.log.debug(" - page     =" + str(req_page))
			self.log.debug(" - sartAt   =" + str(req_start_at))

		return jira_issues



	def getIssuesAll(self):
		"""
		Récupère toutes les issues JIRA

		:rtype: list[JiraIssue]
		"""
		return self.getIssues(conf['jira']['MAX_NB_ISSUES'], conf['jira']['MAX_NB_ISSUES_PER_REQUEST'])



	def readIssues(self, project_name=None):
		"""
		Récupère toutes les issues JIRA pour un projet donné

		:type project_name: str
		:param project_name: le nom du projet
		:rtype: list[JiraIssue]
		"""
		self.log.debug("jql : " + 'project="' + project_name + '"')
		if not project_name:
			return self.getIssuesAll()
		else:
			return self.getIssuesForJql('project="' + project_name + '"')



	def getIssuesForProjectById(self, projet_id):
		"""
		Récupère toutes les issues JIRA pour un projet donné

		@param string projet le nom du projet
		@return list[JiraIssue]
		"""
		self.log.debug("project=" + projet_id)
		return self.getIssuesForJql("project=" + projet_id)



	def getIssuesForType(self, type):
		"""
		Récupère toutes les issues JIRA pour un type donné

		@param string type le nom du type
		@return list[JiraIssue]
		"""
		return self.getIssuesForJql("issuetype=" + type)



	def getIssuesForJql(self, jql):
		"""
		Récupère toutes les issues JIRA correspondant à une requête JQL donnée

		:param jql: la requête JQL
		:type jql: str
		:rtype: list[JiraIssue]
		"""
		return self.getIssues(int(conf['jira']['MAX_NB_ISSUES']), int(conf['jira']['MAX_NB_ISSUES_PER_REQUEST']), jql)



	def getIssueTypes(self):
		"""
		Effectue une requête REST pour récupérer les type d'issues JIRA

		@param
		@param
		@return list[JiraIssueType]
		"""
		self.log.debug("getIssueTypes()...")

		r = self.jrb.buildRequest('issuetype')

		self.log.debug("url=" + r.getUrl())

		parsed_json = r.execute()
		self.log.debug("parsed_json=" + str(parsed_json))
		lj = parsed_json

		# Conversion du JSON au format objet Jira (ici JiraProject)
		list = []
		for i in lj:
			j = JiraIssueType(i)
			list.append(j)

		return list




	def setParams(self, params):
		# TODO maybe
		# Pour l'instant on ne change pas dynamiquement les params de connexion à JIRA
		pass



	def finished(self):
		# Rien de particuler à faire
		pass