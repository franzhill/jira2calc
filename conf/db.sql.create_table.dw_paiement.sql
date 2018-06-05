DROP TABLE IF EXISTS dw_paiement;


--
-- Note concernant le mapping JiraIssue -> table ci-dessous en DB  :
-- Pour l'instant celui-ci est fait de manière simple et sans ORM
-- Pour ce faire, le mécanisme d'insertion de JiraIssue(s) en base nécéssite pour bien fonctionner que :
--  les noms champs de la table ci-dessous correspondent au noms des champs (attributs) de la classe
--  JiraIssue, modulo la 'case' (= peu importe si des majuscules ou des minuscules sont utilisées)
--  (en PostgreSQL le nom des champs est automatiquement "converti" en minuscules  sauf si une syntaxe
--   spéciale est utilisée, ce que nous n'avons ici pas voulu faire pour ne pas compliquer les choses)
--

CREATE TABLE dw_paiement
(
  issue_id              integer NOT NULL,
  description           text,
  creator               text,
  created               timestamp(0) with time zone,
  parent_id             integer,
  status                text,
  browsable_url         text,
  summary               text,
  --montant_prevu       numeric(12,2),
  montant               numeric(12,2),
  key                   text,
  parent_key            text,


  CONSTRAINT dw_paiement_id PRIMARY KEY (issue_id)
)
WITH (
  OIDS=FALSE
);


