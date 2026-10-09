# Organisation documentaire — référence opérationnelle

Fournie par le kit de pilotage (`.pilotage/version`). Ne pas modifier ici : les adaptations locales vont dans `PROMO.md`.
Contrôle automatique : `scripts/check-organisation.sh` (lancé à chaque commit par le hook Git).

## Principe

Ranger **par phase**, retrouver **par apprenant**, garder les points d'entrée **courts et remplacés**.
Un document va dans la phase dont il parle ; sinon dans la phase en cours à sa date.

## Où ranger quoi

| Je produis… | Emplacement | Nom |
| --- | --- | --- |
| brief apprenant, cahier des charges | `02_sprints/<sprint>/briefs/` | `brief-0N-<sujet>.md` |
| version de saisie plateforme (Simplonline, YouCode…) | `02_sprints/<sprint>/briefs/plateforme/` | `brief-0N-<plateforme>.md` |
| cadrage de sprint | `02_sprints/<sprint>/cadrage/` | `sprintN-cadrage-<theme>.md` |
| support, atelier, exercice, dataset distribuable | `02_sprints/<sprint>/{supports,ateliers,exercices}/` | libre, kebab-case |
| audit de rendus, snapshot, activité GitHub | `02_sprints/<sprint>/rapports/audits/` | `audit-<objet>-AAAA-MM-JJ.md` |
| activités plateforme, check, message Discord, préparation | `02_sprints/<sprint>/rapports/preparations/` | `<type>-<objet>-AAAA-MM-JJ.md` |
| prompt conservé comme trace | `02_sprints/<sprint>/rapports/prompts/` | `prompt-<outil>-<objet>-AAAA-MM-JJ.md` |
| observation de séance, débrief, plan d'action | `05_promotion/suivi/<phase>/` | `AAAA-MM-JJ-<objet>.md` |
| présence isolée | `05_promotion/suivi/presences/` | `AAAA-MM-JJ-presences-*.md` |
| état d'un apprenant | `05_promotion/apprenants/fiches/<slug>.md` | mettre à jour, ne pas dupliquer |
| veille (propositions, registre) | `05_promotion/veille/` | `propositions-<phase>-semaine-0N.md`, `registre-attributions-veille.md` |
| note captée en vrac, pas encore triée | `inbox/` | libre ; vidé par `/noter` |
| squads | `05_promotion/groupes/` | `squads-sprint-0N.md` |
| décision durable | `06_pilotage/decisions/` **+ 1 ligne dans `decisions/INDEX.md`** | `AAAA-MM-JJ-<objet>.md` |
| historique retiré de CURRENT | `06_pilotage/journal/AAAA-MM.md` | ajout en tête |
| poster, PDF transverse, import brut | `07_outputs/{posters,pdf,presentations,imports}/` | `<objet>-AAAA-MM-JJ.<ext>` |
| justificatif, coordonnées, données perso | `_confidentiel/` (hors Git) | libre |
| script d'outillage | `scripts/` | kebab-case |

`<phase>` = `warmup`, `sprint-01`, `sprint-02`… Les phases Warm-Up utilisent `01_warmup/` avec les mêmes sous-dossiers (`briefs/`, `rapports/…`).

## Cycle de vie

| Cycle | Quoi | Lecture par un agent |
| --- | --- | --- |
| Chaud | `CURRENT.md`, README du sprint en cours, `alertes.md`, fiches apprenants | à chaque tâche concernée |
| Tiède | décisions (via `decisions/INDEX.md`), rapports du sprint en cours | à la demande, en lisant d'abord le `## Résumé` |
| Froid | phase close : lire **seulement** son `BILAN.md` ; `00_sources/legacy/`, `07_outputs/imports/`, binaires | uniquement si la tâche l'exige explicitement |

## Règles de taille

* `CURRENT.md` ≤ 10 Ko (bloquant au commit). On remplace l'état ; l'historique va dans `06_pilotage/journal/`.
* Audits : bloc `## Résumé` (≤ 10 lignes) dans les 30 premières lignes.
* Fiche apprenant ≤ 3 Ko : état en 5 lignes + liens.
* Pas de recopie de longs tableaux : lier la preuve.
* Fichier > 5 Mo ou archive `.zip` : à justifier ; supprimer après extraction + synthèse + mention dans le README du dossier.

## Rituel de clôture de phase

1. Écrire `BILAN.md` de la phase (1 page : résultats, compétences, points ouverts, liens).
2. Déplacer l'historique de `CURRENT.md` vers `06_pilotage/journal/` et réécrire `CURRENT.md` pour la phase suivante.
3. Retirer les alertes résolues de `alertes.md` (elles sont dans le bilan).
4. Mettre à jour les fiches apprenants (ligne « état »).
5. `scripts/check-organisation.sh` doit passer.

## Fin de tâche (automatique)

Il n'y a pas de rituel de session à lancer : chaque commande du kit (`/noter`, `/cadrage`, `/audit`…) termine elle-même son travail.

1. Chaque nouveau fichier est au bon endroit selon la table.
2. `CURRENT.md` est **remplacé** (et non allongé) si l'état a changé.
3. Nouvelle décision → ligne dans `decisions/INDEX.md`.
4. Nouvel audit → `## Résumé` en tête + fiches apprenants concernées mises à jour.
5. `bash scripts/check-organisation.sh` passe, puis commits atomiques.
