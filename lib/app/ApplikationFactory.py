from lib.ui.IUi import IUi
from lib.writer.ADataWriter import ADataWriter
from lib.reader.ADataReader import ADataReader
from lib.app.AApplikation_ import AApplikation_
from lib.app.apps.PentahoApplikation import PentahoApplikation
from lib.app.apps.CalcApplikation import CalcApplikation




class ApplikationFactory():
	"""
	Permet de créer des instances de (sous-types concrets de) AApplikation_

	@python-version 3.3.5
	@author fhill
	"""


	typePentaho  = 'pentaho'      # TODO paramétriser
	typePentaho2 = 'bd'           # Alias pour ci-dessus # TODO paramétriser
	typeCalc     = 'calc'         # TODO paramétriser


	def __init(self):
		self.type = None
		self.dr   = None
		self.dw   = None
		self.ui   = None



	def setType(self, type):
		"""
		Définit le type d'application que l'on veut fabriquer

		TODO avoir des types concrets CalcApplikation et PentahoAppplikation n'a plus
		vraiment de sens au vu de l'évoluation actuelle du code
		=> il faudrait avoir une instance concrète d'application
		et pouvoir préciser ses comportements spécifiques de manière interchangeable

		:param type: 'pentaho' ou 'calc'  (case insensitive)  (cf variable de classe définies dans cette classe)
		:type type: str
		:return:
		"""
		lc_type = type.lower()
		if lc_type not in [ApplikationFactory.typePentaho , ApplikationFactory.typePentaho2, ApplikationFactory.typeCalc]:
			raise Exception("Cannot make an application wich is not either a [%s] or a {%s]. Asked for a : [%s]" % (ApplikationFactory.typePentaho, ApplikationFactory.typeCalc, type))
		else:
			self.type = lc_type



	def setUi(self, ui):
		"""
		Spécifie l'interface utilisateur de l'application que l'on veut fabriquer

		:param ui:
		:type ui: IUi
		:return:
		"""
		self.ui = ui



	def setDw(self, dw):
		"""
		Spécifie l' "écriveur" de l'application que l'on veut fabriquer

		:param dw:
		:type dw: ADataWriter
		:return:
		"""
		self.dw = dw



	def setDr(self, dr):
		"""
		Spécifie le "lecteur" de l'application que l'on veut fabriquer

		:param dr:
		:type dr: ADataReader
		:return:
		"""
		self.dr = dr



	def make(self):
		"""
		Fabrique une instance d'application avec les composants spécifiés préalablement avec les fonctions set*()

		:return:
		:rtype: AApplikation_
		"""
		if (not self.type) or (not self.dw) or (not self.ui):
			raise Exception("Type or Data writer or User Interface not or wrongly specified. Cannot make an application.")
		else:
			if   (self.type == ApplikationFactory.typePentaho or self.type == ApplikationFactory.typePentaho2):
				app = PentahoApplikation(self.dr, self.dw, self.ui)
				#app.ui.initialize(app)
				#app.dr.initialize(app)
				app.initializeUi()
				app.initializeDr()
				#app.dw.initialize(app)   TODO
			elif (self.type == ApplikationFactory.typeCalc):
				app = CalcApplikation(self.dr, self.dw, self.ui)
				#app.ui.initialize(app)
				#app.dr.initialize(app)
				app.initializeUi()
				app.initializeDr()
				# app.dw.initialize(app)   TODO
			else:
				# Shouldn't happen ...
				raise Exception("Cannot make an application which is not either a [%s] or a {%s]. Asked for a: [%s]" % (ApplikationFactory.typePentaho, ApplikationFactory.typeCalc, type))

		return app