

# ----------------------------------------------
# Configuration de la solution de logging
# ----------------------------------------------

print("*** <CONFIGURING LOGGING SOLUTION> ***")

import logging.config
logging.config.fileConfig('conf/logging.conf')   # Path relatif à ce fichier
log = logging.getLogger("main")

# Test du logger :
log.debug('debug message')
log.info('info message')
log.warning('warning message')
log.error('error message')
log.critical('critical message')

print("*** </CONFIGURING LOGGING SOLUTION> ***")