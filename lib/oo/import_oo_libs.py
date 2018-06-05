import logging
import os
import subprocess
import sys

from lib.conf.conf import conf

# ======================================================================================================================

# Pour utiliser le logger commun à tout le projet:
#log = logging.getLogger("main")
# Pour utiliser un logger spécifique à ce fichier : (le définir aussi dans le fichier de conf des logs, si différent du logger root)
log = logging.getLogger(__name__)

# ======================================================================================================================


def pre_import_uno():
	"""
	 Importe uno dans python installé "hors LibreOffice"
	 (LibreOffice fournit un python mais pour des raisons de droits manquants (relatif politique client)
	 l'installation de packages/librairies est problématique
	  => nous voulons utiliser un python installé en dehors de LibreOffice
	  => il faut "importer" la librairie uno, fournie par LibreOffice... et ça ne se fait pas comme ça ...

	 FHI 2016.12.28

	 Voir :
	   https://forum.openoffice.org/en/forum/viewtopic.php?f=45&t=36370&p=166783
	"""

	# Python_OO = le python livré avec Open(Libre)Office
	python_oo_executable = conf['path']['PATH_TO_OO_PYTHON']    #2
	python_oo_script     = '-cimport os ;print(os.environ["URE_BOOTSTRAP"]) ;print(os.environ["UNO_PATH"]) ;print(os.environ["PATH"])'                    #3, #4, #5
	path_to_uno          = conf['path']['PATH_TO_UNO']        #6


	# Get the environment variables from OO-Python using subprocess
	process               = subprocess.Popen([python_oo_executable, python_oo_script], stdout=subprocess.PIPE)
	result                = process.communicate()
	print("result=")
	print(result)
	environment_variables = result[0].decode("ascii").split('\r\n')   # Three items in the list, one for each env var
	print("environment_variables=")
	print(environment_variables)

	# En mode debug sous Pycharm, les opérations ci-dessus posent problème et on n'arrive pas à récupérer environment_variables...
	# => on rattrappe artificiellement le coup: ici je remplis avec des valeurs propres à MON environnement de dev [FHI]
	if (conf['run'].getboolean('DEBUG')):
		environment_variables = ['vnd.sun.star.pathname:C:\\Program Files (x86)\\LibreOffice 4\\program\\fundamental.ini',
		                         'C:\\Program Files (x86)\\LibreOffice 4\\program\\',
		                         'C:\\Program Files (x86)\\LibreOffice 4\\URE\\bin;C:\\Program Files (x86)\\LibreOffice 4\\program\\;C:\\Program Files (x86)\\Intel\\iCLS Client\\;C:\\Program Files\\Intel\\iCLS Client\\;C:\\windows\\system32;C:\\windows;C:\\windows\\System32\\Wbem;C:\\windows\\System32\\WindowsPowerShell\\v1.0\\;c:\\wapt;C:\\Program Files (x86)\\Intel\\Intel(R) Management Engine Components\\DAL;C:\\Program Files\\Intel\\Intel(R) Management Engine Components\\DAL;C:\\Program Files (x86)\\Intel\\Intel(R) Management Engine Components\\IPT;C:\\Program Files\\Intel\\Intel(R) Management Engine Components\\IPT;C:\\java\\Python33'
		                         ''
		                        ]


	# Positionne les 2 premières var d'env :
	os.environ['URE_BOOTSTRAP'] = environment_variables[0]          #3
	os.environ['UNO_PATH']      = environment_variables[1]          #4

	# Positionne la 3è var d'env : 
	# merge le PATH de python OO avec le path de la version système de Python :
	new_paths      = environment_variables[2].split(';')
	existing_paths = os.environ['PATH'].split(';')
	for path in new_paths:
		if path not in existing_paths:
			existing_paths.append(path)
	os.environ['PATH'] = ';'.join(existing_paths)       #5

	sys.path.append(path_to_uno)                        #6

	return


def pre_import_pyoo():
	sys.path.append(conf['path']['PATH_TO_PYOO'])
	return







pre_import_uno()
log.debug("Done Importing uno")


pre_import_pyoo()
