import tkinter as tk

from lib.ui.gui.AGui import AGui
from lib.ui.gui.module import modules



class CalcGui(AGui):
	"""
	@python-version 3.3.5
	@author fhill
	"""


#	def __init__(self, app):
#		super().__init__(app)



	def _getWindowTitle(self):
		"""
		TODO passer en paramètre au super() constructeur plutôt
		"""
		return "Import JIRA dans Calc"



	def _createModules(self):
		self.createModuleSelectProject()
		self._createModuleSelectFile()
		self.createModuleImport()



	def _createModuleSelectFile(self):
		frame_file = tk.Frame(self.windowRootFrame, bg='grey')
		frame_file.pack(padx=5, pady=5, side="top")

		self.modules['file'] = modules.SelectFile(frame_file, self)
		self.modules['file'].getElements()['label'   ].grid(row=0, column=1, padx=5, pady=5)
		self.modules['file'].getElements()['selector'].grid(row=0, column=2, padx=5, pady=5)
		self.modules['file'].getElements()['browser' ].grid(row=1, column=1, padx=5, pady=5)



	def getFile(self):
		return self.modules["file"].getValue()