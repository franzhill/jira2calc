import pyoo

from pyoo import _IOException

class Desktop(pyoo.Desktop):
	"""
	Surcharge de la classe Desktop de pyoo

	En effet, on veut changer le comportement d'ouverture d'un fichier : voir fonction redéfinie

	@python-version 3.3.5
	@author fhill
	"""


	def _open_url(self, url, extra=()):
		"""
		Si le fichier désigné par l'url est ouvert, alors utiliser la fenêtre
		dans laquelle il est ouvert, plutôt que de l'ouvrir dans une autre fenêtre (et en mode "lecture seule" qui de plus)

		@override
		"""
		try:
			return self._target.loadComponentFromURL(url, '_default', 0, extra)   # la fonction d'origine utilisait '_blank'
		except _IOException as e:             # défini dans l'original ...
			raise IOError(e.Message)
		except Exception as e:                # non défini dans l'original. Or d'autres types d'exception que _IOException peuvent survenir...
			raise IOError(e.Message)            # NB depuis Python > 3 IOError est devenu un alias pour OSError




	#def open_spreadsheet(self, path, as_template=False, as_new=False):
	#	"""
	#
	#	:param path:
	#	:param as_template:
	#	:param as_new: open in a new window if file is already open. If False and file is already open, will move focus to
	#	               the window it's open in, and edition will happen there
	#	:return:
	#	"""
	#	extra = ()
	#	if as_template:
	#		pv = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
	#		pv.Name = 'AsTemplate'
	#		pv.Value = True
	#		extra += (pv,)
	#	# UNO requires absolute paths
	#	url = uno.systemPathToFileUrl(os.path.abspath(path))
	#	document = self._open_url(url, extra)
	#	return SpreadsheetDocument(document)
