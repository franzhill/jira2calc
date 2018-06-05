"""
 Cf main_jira_to_calc

 Ce programme charge les tâches (issues) JIRA non pas dans Calc (comme le fait main_jira_to_calc),
 mais dans une BD destinée à être utilisée par Pentaho.
 (plus précisément dans une table qui servira de "data warehouse" (voir main_pentaho_dw_to_ds)

 @author fhill
 @since 2016.12 - 2017.02
 @python-version 3.3.5

 Mode d'emploi:
   Voir l'aide du script dans le code plus bas, ou afficher l'aide:
   > python main_pentaho.py -h


 Exemple : pour envoyer les tâches Jira dans Postgres en ligne de commande:
 > python main_pentaho_dw_to_ds.py  --headless "Mon_Projet_Jira" my_postgres_server db_name user -w password -s schema


"""

import argparse
import sys

from lib.app.ApplikationFactory import ApplikationFactory
from lib.conf.conf import conf
from lib.conf.conf_log import log
from lib.reader.readers.JiraDataReader import JiraDataReader
from lib.ui.clui.cluis.PentahoClui import PentahoClui
from lib.ui.gui.guis.PentahoGui import PentahoGui
from lib.writer.writers.DwDbDataWriter import DwDbDataWriter

# ----------------------------------------------
# Main
# ----------------------------------------------

# 1. Parser d'option et lecture des options données au script

help_desc = """
Importe des tâches Jira dans une BD pour utilisation par Pentaho

Author: fhill
Version: 2016.12 - 2017.01
python-version: 3.3.5

Exemples :
  -Affiche l'aide:
  > python {name} -h

  -Lance l'import des tâches du projet JIRA 'Mon_Projet_Jira' dans la BD spécifiée par les paramètres:
  > python {name} --headless "Mon_Projet_Jira" 10.xxx.xx.xx db_name user

  -Même chose, en spécifiant un mot de passe et un port spécifique:
  > python {name} --headless Mon_Projet_Jira" 10.xxx.xx.xx db_name user -w password -p 8082
""" . format(**{'name' : sys.argv[0]})

parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawDescriptionHelpFormatter)

# Pour l'instant on ne s'intéresse qu'à l'option qui détermine si l'on doit lancer la GUI ou non
parser.add_argument('--headless', '-l', action='store_true', default=False, help="Lance le programme sans GUI, en ligne de commande. Si non spécifé, alors la GUI est lancée et dans ce cas, aucune autre option ou argument n'est prise en compte")

# Utiliser parse_known_args() entraîne le mauvais fonctionnement de l'option -h puisque l'on définit le reste des options plus loin
#args = parser.parse_known_args()
#args = args[0]
#log.debug(pprint.pformat(args))
#if args.headless:
# => on va faire "rudimentaire"  (pas très booo)
#  TODO il faudrait revoir tout ça
#  TODO aussi gérer le niveau de log depuis la ligne de commande (-v, -vv, -vvv)

#print("sys.argv[1:]=" + pprint.pformat(sys.argv[1:]))
if any(option in sys.argv[1:] for option in ["--headless", "-l", "-h", "--help"]):
	log.debug("Headless (no GUI) run of script or display help requested...")
	ui = PentahoClui(parser)
else:
	ui = PentahoGui()


# 2. Construction de l'application

dr = JiraDataReader (conf['jira']['REST_BASE_URL'],
                     conf['jira']['REST_USERNAME'],
                     conf['jira']['REST_PASSWORD']
                    )
dw = DwDbDataWriter (conf['db']['HOST'],
                     conf['db']['PORT'],
                     conf['db']['USER'],
                     conf['db']['PASSWORD'],
                     conf['db']['DBNAME']
                    )


app_fact = ApplikationFactory()
app_fact.setType('pentaho')
app_fact.setUi(ui)
app_fact.setDr(dr)
app_fact.setDw(dw)
app = app_fact.make()
app.run()
