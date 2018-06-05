from abc import ABCMeta, abstractmethod


class IUiPentaho(metaclass=ABCMeta):
	"""
	Interface pour les Uner Interfaces (UI) des applications *Pentaho* uniquement

	@python-version 3.3.5
	@author fhill

	"""

	@abstractmethod
	def getDbParamsDest(self):
		"""
		:return: dictionnaire de la forme :
			{
				'user'     : xxxx,
				'host'     : xxxx,
				'password' : xxxx,
				'port'     : xxxx,
				'dbname'   : xxxx,
			}
		:rtype: dict
		"""
		pass



	def getDbParamsSource(self):
		"""
		:return: dictionnaire de la forme :
			{
				'user'     : xxxx,
				'host'     : xxxx,
				'password' : xxxx,
				'port'     : xxxx,
				'dbname'   : xxxx,
			}
		:rtype: dict
		"""
		pass