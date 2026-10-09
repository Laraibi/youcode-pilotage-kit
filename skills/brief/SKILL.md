---
name: brief
description: Rédiger ou modifier un brief apprenant en Markdown (stateless, compétences C* et CT* explicites) à partir d'un cadrage de sprint validé, puis sa version de saisie pour la plateforme.
argument-hint: "<sprint> <numéro du brief> | modifier <fichier>"
---

# /brief

## 1. Vérifier le préalable

Le cadrage du sprint doit être **retenu** (décision dans l'INDEX). Sinon, le dire et proposer `/cadrage sprint <N>` ; ne rédiger un brief sans cadrage que si le formateur le demande explicitement.

## 2. Lire

`PROMO.md`, `CURRENT.md`, README et cadrage du sprint, `06_pilotage/regles-pedagogiques.md`, `00_sources/templates/brief-template-reference.md`, `00_sources/referentiel/referentiel-reference.md`, `06_pilotage/progression-referentiel.md`, les briefs précédents du sprint (continuité), `00_sources/legacy/SYNTHESE.md` puis seulement les anciens briefs pertinents. Les legacy inspirent ; ils ne font jamais autorité.

## 3. Rédiger

`<dossier du sprint>/briefs/brief-0N-<sujet>.md`, selon le squelette de référence :

- métadonnées (sprint, période, durée, modalité, technologies, livrables) ;
- compétences visées, `C*` et `CT*` distinguées, avec niveaux, issues du référentiel ;
- place du brief dans le projet du sprint : ce qu'il reprend, ce qu'il ajoute, ce qui doit être démontrable ;
- contexte, objectifs, cahier des charges, contraintes techniques, modalités, évaluation, livrables, critères de performance, bonus ;
- workflow Git/GitHub explicite (branches, commits, README, PR si collectif).

**Stateless** : aucune décision interne, retard, faiblesse individuelle, deadline discutée en pilotage ni thématique future non annoncée. Ce qui manque dans les sources : « à confirmer ».

Vérifier que chaque notion nouvelle du brief a une veille, un workshop ou un live coding qui l'annonce avant ; sinon le signaler et proposer `/cadrage semaine`.

## 4. Version plateforme

Pour chaque plateforme de `PROMO.md` où les briefs sont publiés : `<dossier du sprint>/briefs/plateforme/brief-0N-<plateforme>.md`, avec les champs dans l'ordre du formulaire de la plateforme (texte prêt à coller ou à faire saisir par un agent navigateur).

## 5. Finir

README du sprint (ligne du brief), `bash scripts/check-organisation.sh`, commits séparés (`brief:` puis `brief: version plateforme`). Réponse : chemin du brief, compétences couvertes, points à confirmer.
