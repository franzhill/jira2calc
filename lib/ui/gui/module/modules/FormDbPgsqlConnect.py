import logging
import tkinter as tk

from lib.app.AApplikation_ import AApplikation_
from lib.conf.conf import conf
from lib.ui.gui.module.AModule import AModule


class FormDbPgsqlConnect(AModule):
	"""
	"Module" comprenant tous les éléments graphiques permettant à l'utilisateur de se connecter à la BD

	@python-version 3.3.5
	@author fhill
	"""

	def __init__(self, master, app):
		"""
		:param master: la fenêtre graphique (Tk) parente
		:type  master: tk.Tk
		:param app: l'application dans laquelle évolue ce module
		:type  app: AApplikation_
		"""
		super().__init__()

		self.master = master
		self.app    = app


		# Inputs and their default vals
		import collections

		input_lbls       = collections.OrderedDict()
		input_defaults   = dict()
		self.input_vars  = dict()

		input_lbls      ['user'     ] = 'User'
		input_lbls      ['host'     ] = 'Host'
		input_lbls      ['password' ] = 'Password'
		input_lbls      ['port'     ] = 'Port'
		input_lbls      ['dbname'   ] = 'DbName'
		input_lbls      ['schema'   ] = 'Schema'

		input_defaults  ['host'     ] = conf['db']['HOST']
		input_defaults  ['user'     ] = conf['db']['USER']
		input_defaults  ['password' ] = conf['db']['PASSWORD'] if conf['db']['PASSWORD']     else ''
		input_defaults  ['port'     ] = conf['db']['PORT']     if conf['db']['PORT']         else ''
		input_defaults  ['dbname'   ] = conf['db']['DBNAME']
		input_defaults  ['schema'   ] = conf['db']['SCHEMA']

		self.input_vars ['user'     ] = tk.StringVar()
		self.input_vars ['host'     ] = tk.StringVar()
		self.input_vars ['password' ] = tk.StringVar()
		self.input_vars ['port'     ] = tk.StringVar()
		self.input_vars ['dbname'   ] = tk.StringVar()
		self.input_vars ['schema'   ] = tk.StringVar()


		self.frame_form = tk.Frame(self.master, bg='grey')
		#self.frame_form.pack(padx=5, pady=5, side="top")

		for k,v in input_lbls.items():
			frame_row = tk.Frame(self.frame_form)

			label = tk.Label(frame_row, width=15, text=v, anchor='w')
			entry = tk.Entry(frame_row, textvariable=self.input_vars[k] )
			self.input_vars[k].set(input_defaults[k])

			frame_row.pack(side="top", fill="x", padx=5, pady=5)
			label.pack(side="left")
			entry.pack(side="right", expand="yes", fill="x")




	# ---------------------------------------------------------------------------
	# Public
	# ---------------------------------------------------------------------------

	def getElements(self):
		elems = dict()
		elems['form'] = self.frame_form
		return elems


	def getValue(self):
		"""
		Renvoie la valeur (finale) du module, suite à input par l'utilisateur
		"""
		return \
		{
			'user'     : self.input_vars['user'    ].get(),
			'host'     : self.input_vars['host'    ].get(),
			'password' : self.input_vars['password'].get(),
			'port'     : self.input_vars['port'    ].get(),
			'dbname'   : self.input_vars['dbname'  ].get(),
			'schema'   : self.input_vars['schema'  ].get(),
		}
