# Règles pédagogiques — sprints, briefs, Git

> Fichier fourni par le kit (remplacé à chaque mise à jour). Les adaptations propres à la promo vont dans `PROMO.md`.
> À lire **uniquement** pour une tâche de cadrage, de brief, de sprint ou de Git pédagogique.

## Sources et autorité

- `00_sources/` (planning, référentiel, templates) fait autorité : ne jamais le modifier sans demande explicite.
- Les anciens briefs et anciennes veilles (`00_sources/legacy/`) sont des références d'inspiration, jamais des sources normatives. Passer d'abord par `00_sources/legacy/SYNTHESE.md`.
- Ne pas inventer une information absente des sources : marquer clairement « à confirmer ».
- Toute décision durable est écrite dans `06_pilotage/decisions/` et indexée. Mettre à jour les fichiers de pilotage (README du sprint, `CURRENT.md`, progression) dès qu'une décision touche le planning, un sprint, un brief ou le référentiel.
- Signaler spontanément les incohérences, échéances manquantes, compétences oubliées ou risques détectés.

## Principes de sprint

- Un sprint porte **une seule thématique produit**, alignée avec les technologies et compétences ciblées.
- Les briefs d'un sprint ne sont pas des exercices isolés : ils construisent progressivement le même produit. En fin de sprint, le projet est cohérent, présentable et proche d'une situation professionnelle réelle.
- Progression type des briefs :
  1. socle produit, besoin, interfaces, setup et structure ;
  2. enrichissement métier, interactions, logique applicative ;
  3. consolidation, persistance, intégration, documentation et présentation.
- Les modalités évoluent avec la maturité du groupe (par exemple individuel → binôme → squad) ; chaque transition est justifiée dans le cadrage.
- Une technologie transverse nouvelle (Docker, tests, CI…) s'introduit par paliers, brief par brief, avec une sortie attendue claire.
- Toute notion nouvelle d'un brief doit avoir été annoncée avant son usage : veille, workshop ou live coding (voir `05_promotion/veille/regles-veille.md`).

## Briefs

- Markdown uniquement, selon `00_sources/templates/brief-template-reference.md`.
- Compétences visées explicites, techniques `C*` et transversales `CT*` distinguées, issues du planning et du référentiel.
- **Stateless** et directement distribuable : pas de décision interne, de suivi managérial, de retard, de deadline discutée en pilotage, de thématique future non annoncée, ni de contexte de coordination.
- Chaque brief situe sa place dans le projet global du sprint : ce qu'il reprend, ce qu'il ajoute, ce qui doit être démontrable.

## Git / GitHub pédagogique (à demander dans les briefs)

- `main` représente l'état stable et présentable du projet ;
- branches par brief et par fonctionnalité ;
- commits atomiques, réguliers et explicites ;
- README qui évolue avec le projet ;
- pull requests et revues de code dès que le travail est collectif.

## Git du workspace formateur

- Un commit = une intention. Vérifier le diff staged avant chaque commit.
- Une même date, une même séance ou un même dossier ne justifient pas un commit unique : séparer suivi, audit, veille, décision, brief, cadrage, source, script.
- Nettoyage du working tree : non destructif, commits atomiques, jamais de commit fourre-tout.
