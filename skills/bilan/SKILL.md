---
name: bilan
description: Clôturer une phase (Warm-Up ou sprint) - écrire son BILAN, fermer les alertes, mettre à jour les fiches, archiver l'historique de CURRENT dans le journal et préparer CURRENT pour la phase suivante.
argument-hint: "[phase]"
---

# /bilan

Par défaut : la phase en cours dans `CURRENT.md`. Vérifier que les audits des briefs de la phase existent ; s'il en manque, le signaler et demander si on clôture quand même.

## 1. Lire

README et cadrage de la phase, blocs `## Résumé` de ses audits, débriefs (`05_promotion/suivi/<phase>/`), fiches, alertes, décisions de la phase dans l'INDEX.

## 2. Écrire le BILAN

`<dossier de la phase>/BILAN.md` (modèle `.pilotage/modeles/bilan.md`), une page :

- **Résumé** : résultats, compétences travaillées et niveau atteint par la classe, points ouverts ;
- **Par apprenant** : une ligne de lecture à l'entrée de la phase suivante, axe nommé (section 5 d'`AGENTS.md`) ;
- points reportés à la phase suivante ;
- alertes closes avec la phase ;
- liens vers briefs, cadrage, audits, décisions.

Une fois le BILAN écrit, la phase est **close** : les agents ne liront plus que ce fichier.

## 3. Propager

1. Fiches : ligne de la phase figée en une phrase, prochaine action pour la phase suivante.
2. `06_pilotage/alertes.md` : retirer les alertes résolues (elles sont dans le BILAN).
3. Historique de `CURRENT.md` → `06_pilotage/journal/AAAA-MM.md` (ajout en tête), puis réécrire `CURRENT.md` pour la phase suivante.
4. Décisions de la phase : statut « appliquée » dans l'INDEX quand c'est le cas.
5. Proposer un poster ou un visuel KPI de fin de phase dans `07_outputs/posters/` si le formateur le souhaite.

## 4. Finir

`python3 scripts/maj-fiches.py`, `bash scripts/check-organisation.sh`, commits séparés (`bilan:`, `fiches:`, `pilotage: current et journal`). Suggérer `/cadrage sprint <N+1>` si le sprint suivant n'est pas cadré.
