from lib.tools.JsonReader import *


class JiraIssueType:
	"""
	 Représentation d'un type d'issue JIRA

	 Comprend tous les champs nous intéressant pour notre propos
	"""

	def __init__(self, json_):

		jr = JsonReader(json_, '')

		self.id               = jr.readSafe('id')
		self.description      = jr.readSafe('description')
		self.name             = jr.readSafe('name')
		self.subtask          = jr.readSafe('subtask')


	def __repr__(self):
		return str(vars(self))
