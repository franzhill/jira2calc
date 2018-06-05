from lib.ui.IUiPentaho import IUiPentaho
from lib.ui.gui.AGui import AGui
from lib.ui.gui.module import modules


class PentahoDwToDsGui(AGui, IUiPentaho):
	"""
	@python-version 3.3.5
	@author fhill
	"""



	def _getWindowTitle(self):
		"""
		TODO passer en paramètre au super() constructeur plutôt
		"""
		return "Alimentation des Data Stores à partir du Data Warehouse"



	def _createModules(self):
		self._createModuleFormDbConnection()
		self.createModuleImport()


	def getProject(self):
		# On peut renvoyer la valeur qu'on veut, elle ne devrait de toute manière pas être utilisée
		return "ALL"


	def _createModuleFormDbConnection(self):
		self.modules['form_db_connect'] = modules.FormDbPgsqlConnect(self.windowRootFrame, self.app)
		self.modules['form_db_connect'].getElements()['form'].pack(padx=5, pady=5, side='top')



	def getDbParamsDest(self):
		return self.modules["form_db_connect"].getValue()


	def getDbParamsSource(self):
		# ici pour l'instant on utilise la même BD que ce soit pour la source ou la destination
		# TODO rendre possible que les BD source et dest soient différentes
		return self.modules["form_db_connect"].getValue()