---
name: audit
description: Auditer les rendus d'un brief (dépôts GitHub des apprenants contre une grille) ou l'activité GitHub de la classe, produire un rapport avec un bloc Résumé et mettre à jour les fiches et alertes.
argument-hint: "<brief> | activite | <apprenant> <brief>"
---

# /audit

## 1. Cadrer l'audit

- `<brief>` : audit de livraison de toute la classe sur ce brief.
- `activite` : point sur les commits et branches récents de la classe (qui avance, qui est à l'arrêt).
- `<apprenant> <brief>` : audit individuel (souvent avant un débrief).

Lire `CURRENT.md`, le brief audité (exigences, livrables, critères de performance), le registre apprenants (colonne GitHub) et le dernier audit du même objet s'il existe.

## 2. Collecter

- Dépôts : depuis le registre. Lien manquant → le chercher dans les traces de rendu ; sinon « non rendu ou lien à collecter » (ne pas deviner un compte).
- Pour chaque dépôt : branche par défaut et branches, date et contenu des derniers commits, structure, README, exécution si possible (installer et lancer ; noter si impossible).
- Accès : `gh` ou `git clone` en HTTPS ; dépôt privé ou inaccessible → le noter, ne pas bloquer l'audit.

## 3. Évaluer

Grille dérivée des critères de performance du brief (poids et observables explicites dans le rapport). Score par apprenant **et** constats qualitatifs. Nommer l'axe de chaque verdict (production, risque IA, rythme) : un audit de dépôt ne dit rien de l'appropriation orale, il peut seulement la mettre « à challenger ». Respecter la section 5 d'`AGENTS.md`.

## 4. Écrire

`<dossier du sprint>/rapports/audits/audit-<objet>-AAAA-MM-JJ.md` (modèle `.pilotage/modeles/audit.md`), **`## Résumé` en tête** (≤ 10 lignes, verdict par apprenant), puis grille, détail par apprenant avec preuves (lien de commit, fichier).

## 5. Propager

- Fiches : ligne d'état du sprint en cours remplacée, lien vers l'audit.
- Registre : comptes GitHub découverts.
- Alertes : non-rendus, chutes, risques IA forts ; proposer les débriefs prioritaires.
- `python3 scripts/maj-fiches.py`.

## 6. Finir

`bash scripts/check-organisation.sh`, commits séparés (`audit:` puis `fiches:`). Réponse : le Résumé, et les débriefs proposés.
