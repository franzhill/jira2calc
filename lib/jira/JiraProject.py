from lib.tools.JsonReader import *



class JiraProject:
	"""
	 Représentation d'un projet JIRA

	 Comprend tous les champs JIRA nous intéressant pour notre propos
	"""

	def __init__(self, json):

		jr = JsonReader(json, '')

		self.id                    = jr.readSafe('id')
		self.key                   = jr.readSafe('key')
		self.name                  = jr.readSafe('name')
		self.project_type_key      = jr.readSafe('projectTypeKey')
		self.project_category_id   = jr.readSafe('projectCategory','id')
		self.project_category_name = jr.readSafe('projectCategory','name')



	def __repr__(self):
		return str(vars(self))



	def __lt__(self, other):
		"""
		Pour permettre le tri sur une liste de JiraProject
		:return:
		"""
		return self.name < other.name