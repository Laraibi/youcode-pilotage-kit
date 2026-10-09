---
name: point
description: Répondre en lecture seule à une question sur l'état de la promo - programme du jour, situation d'un apprenant, qui est en alerte, état de la classe sur un brief, prochaines échéances. Ne modifie aucun fichier.
argument-hint: "<question libre>"
---

# /point

**Lecture seule** : ne créer, modifier ni commiter aucun fichier. Si la réponse révèle quelque chose à corriger ou à noter, le proposer à la fin (« à noter avec `/noter` ? ») sans le faire.

## Lire le minimum

| Question | Lire |
| --- | --- |
| « Qu'est-ce que j'ai aujourd'hui / cette semaine ? » | `CURRENT.md` (tableau de la semaine), propositions de veille en cours, jours fériés |
| « Où en est <apprenant> ? » | registre (identité) → sa fiche → la dernière preuve liée si nécessaire |
| « Qui est en alerte ? » | `06_pilotage/alertes.md` |
| « État de la classe sur le brief N » | bloc `## Résumé` du dernier audit de ce brief, fiches au besoin |
| « Qu'avait-on décidé sur X ? » | `06_pilotage/decisions/INDEX.md` → la décision |
| « Où en est le sprint ? » | README du sprint, `CURRENT.md` |

Sans question : un état en 5 lignes (phase, brief en cours, programme du jour, alertes 🔴, prochaine échéance).

## Répondre

Court, en citant la source de chaque affirmation (chemin du fichier, date de mise à jour). Signaler si l'information est ancienne (fiche ou `CURRENT.md` de plus de 7 jours). Respecter la section 5 d'`AGENTS.md` : nommer l'axe avant tout jugement sur un apprenant.
