"""
Placer ces lignes d'import ici permet d'effectuer et d'utiliser les imports de la sorte :

   from lib.gui            import module
   m = module.SelectProject(self, self)      # on appelle directement la classe préfixée par son module

Inconvénient :
  - Pour chaque nouveau fichier ajouté dans le package, il faut ajouter une ligne ici

"""

from .SelectProject import SelectProject
from .SelectFile    import SelectFile
from .ActionImport  import ActionImport
from .FormDbPgsqlConnect import FormDbPgsqlConnect