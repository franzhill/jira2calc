import logging

import requests

from lib.jira.JiraProject   import *
from lib.jira.exceptions    import *
from lib.tools.tools        import *
from lib.conf.conf          import conf

#print ("jira_requets __name__ = " + __name__)
# ======================================================================================================================

class JiraRequestBuilder:

	def __init__(self, url_base, user_name, user_password):
		self.url_base = url_base
		self.user_name = user_name
		self.user_password = user_password

		# verify SSL certificate?
		# Le certif SSL de notre serveur Jira de prod n'est pas bon => ne pas en demander la vérification

		self.verify = conf['jira'].getboolean('REST_VERIFY_CERTIFICATE')

		# Pour utiliser le logger commun à tout le projet:
		#logger = logging.getLogger("main")
		# Pour utiliser un logger spécifique à ce fichier : (le définir aussi dans le fichier de conf des logs, si différent du logger root)
		logger = logging.getLogger(__name__)

		self.setLogger(logger)


	def setLogger(self, logger):
		"""
		 Pour injecter un logger spécifique.
		 Sinon, un logger par défaut sera mis en place (voir __init__)

 		:type logger: logging.Logger
		"""
		self.log    = logger



	def buildRequest(self, url_postfix):
		return JiraRequest(self.url_base + url_postfix, self.user_name, self.user_password, self.verify)


	def __repr__(self):
		return str(vars(self))



# ======================================================================================================================

class JiraRequest:

	def __init__(self, url, user_name, user_password, verify):
		self.url = url
		self.user_name = user_name
		self.user_password = user_password
		self.verify = verify

		# Pour utiliser le logger commun à tout le projet:
		#logger = logging.getLogger("main")
		# Pour utiliser un logger spécifique à ce fichier : (le définir aussi dans le fichier de conf des logs, si différent du logger root)
		logger = logging.getLogger(__name__)

		self.setLogger(logger)
		self.log.debug("Finished building JiraRequest")


	def setLogger(self, logger):
		"""
		 Pour injecter un logger spécifique.
		 Sinon, un logger par défaut sera mis en place (voir __init__)

		:type logger: logging.Logger
		"""
		self.log    = logger


	def addParams(self, params):
		"""
		Only call once! Careful, this is not enforced
		:param params: in the format {'name1': value1, 'name2': value2})
		:return:
		"""
		# Add trailing / if necessary:
		if not self.url.endswith('/'):
			self.url += '/'
		self.url += '?' + urllib.parse.urlencode(params)


	def execute(self):
		"""
		Execute as GET (Only GET is supported)

		:return: parsed json
		"""
		self.log.debug("")
		self.log.debug("Verify = " + str(self.verify))

		try:

			## Suite à des problèmes (connexion SSL devenue impossible) tentative de débuguer (2017.04.04) :
			## s'agit-il de la version du cipher utilisée ? -> via curl on constate que c'est :
			##   SSL connection using TLSv1.0 / AES256-SHA
			## qui est utilisé.

			#import requests.packages.urllib3.util.ssl_
			#requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':AES+SHA' + ':AES256+SHA' + ':SHA+AES' + ':SHA+AES256' + ':AES256-SHA'
			#print("requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = " + requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS)

			## Visiblement ça ne change rien ...

			r = requests.get(self.url, auth=(self.user_name, self.user_password), verify=self.verify)

			# For successful API call, response code will be 200 (OK)
			if r.ok:
				self.log.debug("Request successful...")

				# Loading response data into a dictionary variable
				# Notes:
				#   - json.loads(String) takes a Json structure and converts into a python data structure (dict or list, depending on JSON)
				parsed_json = json.loads(r.content.decode("utf-8"))
				return parsed_json

			# If response code is not ok, print the resulting http error code with description
			else:
				self.log.debug("Request UNsuccessful...")
				#dump(r)
				self.log.debug(r.raw)
				r.raise_for_status()

		except Exception as e:
			msg = """
			Erreur lors de la requête suivante :
			  url  = %s
			  user = %s
			""" %  (self.url, self.user_name, )
			#print("**********ERROR : " + msg)
			raise JiraRequestException(msg, e)




	def getUrl(self):
		return self.url


	def __repr__(self):
		return str(vars(self))





