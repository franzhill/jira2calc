import logging
import json
import pprint

class JsonReader():
	"""
	A partir d'un object JSON donné, fournit des outils pour aller lire dedans de manière "spécifique"

	@author fhill
	"""

	def __init__(self, json_, none_fallback_value=None):
		"""

		:param json: json as a string, or json as a Python dictionary (aka "parsed json")
		"""

		# Pour utiliser le logger commun à tout le projet:
		# logger = logging.getLogger("main")
		# Pour utiliser un logger spécifique à ce fichier : (le définir aussi dans le fichier de conf des logs, si différent du logger root)
		logger = logging.getLogger(__name__)

		self.setLogger(logger)

		self.jsonDict = json.loads(json_) if isinstance(json_, str) else json_

		self.noneFallbackValue = none_fallback_value


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



	def readSafe(self, *args, **kwargs):
		'''
		Pour lire de manière "relâchée" (i.e. sans levée d'erreur) dans le json lorsqu'on n'est pas sûr de la structure
		i.e. sans avoir à se soucier que les objets et sous-objets existent vraiment.
		Ex :
		   jr = JsonReader(json)
		   jr.readSafe(key1, key2, key3) ira chercher dans le json l'objet suivant :

		      json[key1][key2][key3]

		   et si l'une des clés n'existe pas alors readSafe renverra None (mais pas d'exception)

		L'approche
		  try: val       = json['key1']['key2']['key3']
		  except KeyError: val = None
		ne fonctionne pas, enfin pas toujours, en effet si pour une clé intermédiaire l'objet est explicitement
		déclaré dans le JSON comme NULL alors une Exception de type NonType est levée pour la (tentative de) lecture des clés
		suivantes.


		NB : une valeur null dans le JSON est retranscrite en Python comme None (par json.loads(...) )
		 Ex :
		        ...
		       "customfield_10062": null,
		        ...

		:param args:
		:return:
		'''
		self.log.debug('')
		#print(pprint.pformat(args))

		json_dict_curr       = self.jsonDict
		try:
			none_fallback_value = kwargs['default']
		except KeyError:                              # NDP Même si kwargs est vide, cette erreur est levée => inutile donc de pré-vérifier si kwargs est None
			none_fallback_value = self.noneFallbackValue


		for idx, key in enumerate(args):
			try:
				if not (type(json_dict_curr) is dict):
					return none_fallback_value

				json_dict_curr = json_dict_curr[key]

				if json_dict_curr is None:
					return none_fallback_value

				self.log.debug("key=" + key)
				self.log.debug("json_dict_curr = %s" % (pprint.pformat(json_dict_curr))  )
			except KeyError as e:
				return none_fallback_value

		return json_dict_curr
