Drop TABLE IF EXISTS ds_issue;

--
-- Note concernant le mapping JiraIssue -> table 'issue' en DB  :
-- Pour l'instant celui-ci est fait de manière simple et sans ORM
-- Pour ce faire, le mécanisme d'insertion de JiraIssue(s) en base nécéssite pour bien fonctionner que :
--  les noms champs de la table ci-dessous correspondent au noms des champs (attributs) de la classe
--  JiraIssue, modulo la case (= peu importe si des majuscules ou des minuscules sont utilisées)
--  (en PostgreSQL le nom des champs est automatiquement "converti" en minuscules  sauf si une syntaxe
--   spéciale est utilisée, ce que nous n'avons ici pas voulu faire pour ne pas compliquer les choses)
--

CREATE TABLE ds_issue
(
	id                    text,   -- idéalement devrait être 'issue_id', mais on colle aux noms donnés dans JiraIssue
	type                  text,
	centre                text,
	domaine               text,
	axe                   text,
	nom                   text,
	nom_du_projet         text,
	summary               text,
	status                text,
	montant_cmde          numeric(12,2),  -- http://stackoverflow.com/questions/15726535/postgresql-which-datatype-should-be-used-for-currency
	montant_paiement      numeric(12,2),
	key                   text,
	parent_key            text,
	sort_idx              text,

	browsable_url         text,

  -- Redondants (dénormalisation spécifique pour cube Saïku):

	c_status              text,
	c_key                 text,
	c_parent_key          text,

	p_status              text,
	p_key                 text,
	p_parent_key          text,

	date_commande         date,

	date_commande_ymd   text,
	date_commande_y     smallint,   -- -32768 to +32767
	date_commande_m     smallint,
	date_commande_w     smallint,



  -- Existent dans JiraIssue, mais non insérés en BD :
  --issue_id integer NOT NULL,
  --description text,
  --creator text,
  --created timestamp(0) with time zone,
  --parent_id integer,
  --status text,


  CONSTRAINT ds_issue_id PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);