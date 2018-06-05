"""
 Cf main_jira_to_calc
 Cf main_jira_to_pentaho_dw

 Récupère les tâches (issues) JIRA écrites dans ce qui pour l'instant constitue le
  "Data Warehouse" (aka "Puits de données" i.e. les tables "X" et "Y"),
   et les insère (avec enrichissement) dans ce qui pour l'instant constitue le "Data Store"
   (i.e. la table "taches")


 @author fhill
 @since 2016.12 - 2017.02
 @python-version 3.3.5

  Lancement en ligne de commande :
  > python main_pentaho_dw_to_ds.py --headless "Mon_Projet_Jira" 10.xxx.xx.xx db_name user
  > python main_pentaho_dw_to_ds.py --headless "Mon_Projet_Jira" postgres_server db_name user -w password -s schema




"""

import argparse
import sys

from lib.app.ApplikationFactory import ApplikationFactory
from lib.conf.conf import conf
from lib.conf.conf_log import log
from lib.reader.readers.DwDbDataReader import DwDbDataReader
from lib.ui.clui.cluis.PentahoClui import PentahoClui
from lib.ui.gui.guis.PentahoDwToDsGui import PentahoDwToDsGui
from lib.writer.writers.DsDbDataWriter import DsDbDataWriter


# ----------------------------------------------
# Main
# ----------------------------------------------

# 1. Parser d'option et lecture des options données au script

help_desc = """
	Importe des tâches Jira depuis le Data Warehouse, vers le(s) Data Store(s)

	"Exemples :"
"""

parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawDescriptionHelpFormatter)

# Pour l'instant on ne s'intéresse qu'à l'option qui détermine si l'on doit lancer la GUI ou non
parser.add_argument('--headless', '-l', action='store_true', default=False, help="Lance le programme sans GUI, en ligne de commande. Si non spécifé, alors la GUI est lancée et dans ce cas, aucune autre option ou argument n'est prise en compte")

# Utiliser parse_known_args() entraîne le mauvais fonctionnement de l'option -h puisque l'onn définit le reste des options plus loin
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
	ui = PentahoDwToDsGui()


# 2. Construction de l'application

dr = DwDbDataReader (conf['db']['HOST'],
                     conf['db']['PORT'],
                     conf['db']['USER'],
                     conf['db']['PASSWORD'],
                     conf['db']['DBNAME']
                    )
dw = DsDbDataWriter (conf['db']['HOST'],
                     conf['db']['PORT'],
                     conf['db']['USER'],
                     conf['db']['PASSWORD'],
                     conf['db']['DBNAME']
                    )


app_fact = ApplikationFactory()
app_fact.setType('pentaho')
app_fact.setDr(dr)
app_fact.setDw(dw)
app_fact.setUi(ui)
app = app_fact.make()
app.run()
