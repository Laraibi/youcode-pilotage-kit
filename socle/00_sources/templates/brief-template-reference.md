# Référence de squelette Markdown de brief

## Source

* Source exploitée : corpus des anciens briefs dans `00_sources/legacy/` (synthèse : `00_sources/legacy/SYNTHESE.md`).
* Statut : squelette de brief Markdown dérivé des sections récurrentes observées dans les anciens briefs.
* Objectif : comprendre la structure attendue lorsqu'un brief de l'année est demandé en Markdown.
* Les anciens briefs restent des références historiques et d'inspiration, pas des sources normatives.
* Le planning et le référentiel restent prioritaires pour choisir les compétences ciblées.

## Format cible

Les nouveaux briefs doivent être des fichiers Markdown (`.md`), placés dans `02_sprints/<sprint>/briefs/` (versions de saisie plateforme dans `briefs/plateforme/`).

## Structure Markdown attendue

| Section | Statut | Contenu attendu | Source du choix |
| ------- | ------ | --------------- | --------------- |
| Titre | Obligatoire | Nom du brief, sprint et thème principal | Récurrent dans tous les briefs historiques. |
| Métadonnées pédagogiques | Obligatoire | Sprint, période, durée, modalité de travail, technologies, livrables principaux | Déduit des anciens briefs et nécessaire au pilotage. |
| Compétences visées | Obligatoire | Séparer clairement compétences techniques `C*` et compétences transversales `CT*`, avec niveaux ciblés | Alignement planning/référentiel. |
| Contexte du projet | Obligatoire | Situation métier courte, concrète, orientée problème | Très récurrent dans les anciens briefs. |
| Objectifs pédagogiques | Obligatoire | Liste de capacités à développer, alignées sur les compétences ciblées | Très récurrent dans les anciens briefs. |
| Cahier des charges fonctionnel | Obligatoire selon le brief | Fonctionnalités attendues, souvent par rôle, module ou parcours utilisateur | Récurrent dans les briefs applicatifs. |
| Contraintes techniques | Obligatoire | Stack, architecture, règles techniques, qualité minimale | Très récurrent dans les anciens briefs. |
| Modalités pédagogiques | Obligatoire | Individuel/binôme/squad, suivi, organisation, jalons | Récurrent dans les anciens briefs. |
| Modalités d'évaluation | Obligatoire | Déroulé, soutenance, démonstration, points observés | Récurrent dans les anciens briefs. |
| Livrables attendus | Obligatoire | Dépôt GitHub, README, application/API, documentation, exports ou déploiement selon le sprint | Très récurrent dans les anciens briefs. |
| Critères de performance | Obligatoire | Critères courts, observables et évaluables | Très récurrent dans les anciens briefs. |
| Bonus | Optionnel | Extensions proposées sans brouiller le niveau attendu | Présent dans plusieurs briefs historiques. |
| Ressources | Optionnel | Documentation, liens ou supports si fournis par les sources | À utiliser seulement si les sources existent. |

## Règles d'alignement

* Ne pas générer de brief HTML.
* Ne pas convertir les anciens HTML en nouveaux briefs.
* Générer les nouveaux briefs en Markdown.
* Toujours distinguer les compétences techniques `C*` des compétences transversales `CT*` (numérotation selon le référentiel de la promo).
* Les compétences visées d'un brief doivent venir du planning, de `referentiel-reference.md` et de `progression-referentiel.md`.
* Les anciens briefs servent à retrouver le squelette, le ton pédagogique, les types de sections et les exigences fréquentes.
* Si une compétence, un niveau ou une modalité n'est pas dans les sources, marquer `À confirmer`.

## Points à confirmer

* Un template Markdown officiel peut encore être fourni plus tard.
* Les champs exacts attendus par l'équipe pédagogique doivent rester ajustables.
* La structure ci-dessus est une référence opérationnelle issue du legacy, pas une norme externe.
