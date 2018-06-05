"""
 Cf main_jira_to_calc

 Cette déclinaison est un exemple (expérimental) de script montrant la versatilité possible de
 lutilisation des briques sous-jacentes.

 But : fournir un script permettant de pouvoir spécifier dynamiquement n'importe quel reader
 (source d'issues Jira) et n'importe quel writer (destination d'issues Jira), qqch de la sorte :
  > python mon_script_generique.py mon_projet_jira params_source params_dest

 Pour l'instant (2017.02.01), la combinaison source=serveur Jira et dest=Calc fonctionne, mais
 seulement en ligne de commande:
  > python main_generique.py  "Mon_Projet_Jira" "{\"type\" : \"jira\", \"host\":\"http://localhost:8080/rest/api/2/\", \"user\":\"fhill\", \"password\": \"***\"}" "{\"type\" : \"calc\", \"host\":\"localhost\", \"port\":\"2002\"}"

 L'écriture de fichiers json en ligne de commande étant fastidieuse, bien entendu il faudrait pouvoir
 lire ces configs depuis des fichiers (et fournir en paramètre ceux-ci plutôt) (=> à faire un jour ;o) )

 @author fhill
 @since 2017.02.02
 @python-version 3.3.5

"""


import argparse
import sys
import json

from lib.app.ApplikationFactory import ApplikationFactory
from lib.conf.conf import conf
from lib.conf.conf_log import log
from lib.reader.readers.JiraDataReader import JiraDataReader
from lib.ui.clui.cluis.PentahoClui import PentahoClui
from lib.ui.gui.guis.PentahoGui import PentahoGui
from lib.writer.writers.OoDataWriter import OoDataWriter
from lib.writer.writers.DwDbDataWriter import DwDbDataWriter
from lib.writer.writers.DsDbDataWriter import DsDbDataWriter
from lib.reader.readers.DwDbDataReader import DwDbDataReader
from lib.reader.readers.DwDbDataReader import DwDbDataReader
from lib.ui.clui.cluis.GenericClui import GenericClui



help_desc = """
Lit des tâches Jira depuis une BD ou un serveur JIRA ou un fichier Calc et les écrit dans Jira ou une BD ou dans Calc

Expérimental.

Uniquement en mode CLI (pas de GUI pour l'instant).

Certaines sources et destinations ne sont pas en l'état encore supportées :
  source : Calc, BD (Data Source)
  destinations : Jira




"""\
	#.format({'name': sys.argv[0]})

parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('project',
                       help="""
Projet Jira que l'on veut importer. Dans certaines configurations, cette donnée n'a pas de sens et sera ignorée.
Pour tous les projets : "ALL"
""")

parser.add_argument('source_params',
                       help="""
Paramètres de la source des tâches Jira, au format Json.
Doit contenir les clés nécessaires à la connexion à la source de données.
Ex:
{ "type"    : "jira",  (ou "calc" ou "bd")
  "subtype" ; "dw"  ou "ds"  (data warehouse ou data store)
  "file"    : "...",   (dans le cas de calc)
  "server"  : "...",   (dans le cas de bd)
  "dbname"  : "..."    (dans le cas de bd)
  "user"    : "...",   (dans le cas de bd, jira...)
  "password": "...",
  "hostname": "...",
  "port"    : "...",
  ...
}"""
                     )
parser.add_argument('dest_params',
                       help="""
Même que pour source_params""")

args = parser.parse_args()

source_params = json.loads(args.source_params)
#source_params = json.loads(args.source_params.content.decode("utf-8"))
dest_params   = json.loads(args.dest_params)

if source_params['type'] == 'jira':
	dr = JiraDataReader(source_params['host'],
	                    source_params['user'],
	                    source_params['password'],
	                    )
elif source_params['type'] == 'bd' and source_params['subtype'] == 'dw':
	dr = DwDbDataReader(source_params['host'],
	                    source_params['port'],
	                    source_params['user'],
	                    source_params['password'],
	                    source_params['dbname'],
	                    )
else:
	raise Exception("Type de source non supporté.")


if dest_params['type'] == 'calc':
	dw = OoDataWriter  (    dest_params['host'],
	                    int(dest_params['port']),
	                    )
elif dest_params['type'] == 'bd' and dest_params['subtype'] == 'ds':
	dw = DsDbDataWriter(dest_params['host'],
	                    int(dest_params['port']),
	                    dest_params['user'],
	                    dest_params['password'],
	                    dest_params['dbname'],
	                    )
elif dest_params['type'] == 'bd' and dest_params['subtype'] == 'dw':
	dw = DwDbDataWriter(dest_params['host'],
	                    int(dest_params['port']),
	                    dest_params['user'],
	                    dest_params['password'],
	                    dest_params['dbname'],
	                    )
else:
	raise Exception("Type de destination non supporté.")

ui = GenericClui(args)

app_fact = ApplikationFactory()
app_fact.setType(dest_params['type'])   # TODO utiliser un type générique
app_fact.setUi(ui)
app_fact.setDr(dr)
app_fact.setDw(dw)
app = app_fact.make()
app.run()
