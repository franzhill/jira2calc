# -*- coding: utf-8 -*-
"""
 Ce programme
  - lance LibreOffice en mode serveur
  - va chercher les (des) issues (tâches) dans un projet Jira
  - les écrit (injecte) dans un document LibreOffice


 @author fhill
 @since 2016.12 - 2017.01
 @python-version 3.3.5


 Notes
  OO  = OpenOffice (~LibreOffice)
"""


from lib.conf.conf_log import log
from lib.app.ApplikationFactory import ApplikationFactory
from lib.conf.conf import conf
from lib.reader.readers.JiraDataReader import JiraDataReader
from lib.ui.gui.guis.CalcGui import CalcGui
from lib.writer.writers.OoDataWriter import OoDataWriter

# ----------------------------------------------
# Main
# ----------------------------------------------

dr = JiraDataReader (conf['jira']['REST_BASE_URL'],
                     conf['jira']['REST_USERNAME'],
                     conf['jira']['REST_PASSWORD']
                    )

dw = OoDataWriter   (    conf['oo']['SERVER_HOST'],
                     int(conf['oo']['SERVER_PORT'])
                    )

ui = CalcGui()



app_fact = ApplikationFactory()
app_fact.setType('calc')
app_fact.setDr(dr)
app_fact.setDw(dw)
app_fact.setUi(ui)
app = app_fact.make()
app.run()



