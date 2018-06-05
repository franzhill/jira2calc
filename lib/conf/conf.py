
from lib.tools.Configuration import Configuration
import socket


# Les différents fichiers de conf "en superposition" (le dernier l'emporte) :
confs = ['conf/conf.ini'      ,
         'conf/conf.prod.ini' ,
         'conf/conf.perso.ini',
        ]

# Détecte si l'on se trouve dans un environnement précis et le cas échéant ajoute un fichier de conf dédié :
#print("socket.gethostname() = " + socket.gethostname())
if (socket.gethostname() == "ACER"):
	confs.append('conf/conf.fhi_home.ini')
import pprint
#print(pprint.pformat(confs))

conf = Configuration(*confs)


