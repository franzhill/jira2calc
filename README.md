# jira2calc
POC en Python permettant d'importer des demandes Jira dans LibreOffice Calc ou dans une BD, en vue d'une exploitation "BI"


Le projet présenté ici est un POC développé pour un client en 2017 (toutes les données personnelles/fonctionnelles ont été anonymisées) dont l'objectif est d'aller chercher certaines tâches d'un projet Jira, de réaliser des traitements dessus (transformations, traductions, enrichissement etc.) et de les injecter dans un document tableur LibreOffice Calc (pré-existant ou nouveau), ou vers d'autres destination (DB, décisionnel...), dans le but d'en faire une exploitation BI.

Etant un POC, donc développé rapidement selon une méthodologie agile, le projet présente bien des possibilités d'améliorations. Il a cependant tenu ses promesses en permettant de constater que l'idée fonctionnait plutôt bien, et que la performance (temps de traitement des requêtages, réglages Jira) pouvait s'avérer un goulot d'étrangement et nécéssitait (nécéssiterait) donc une attention particulière.

La solution cible devant ête soit construite en prolongement de ce POC, soit redéveloppée en Java.

Un certain nombre de contraintes liées à l'environnement de dev furent à honorer : version de Python bien particulière, installation via pip compliquées à travers un réseau bridé ... (=> installs manuelles)

Développé en quelques semaines, sans connaissance préalable de Python pour ma part.

Les sources du projet sont ici publiées à des fins de présentation de son auteur.
