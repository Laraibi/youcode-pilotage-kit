---
name: cadrage
description: Cadrer un sprint (thématique, briefs, compétences, modalités), une semaine (veilles, workshops, live coding, quiz) ou une activité ponctuelle (nouvelle notion, workshop, report). Propose des options argumentées, puis écrit la décision une fois validée.
argument-hint: "sprint <N> | semaine [date] | <sujet libre> | valider <fichier>"
---

# /cadrage

Le cadrage décide **comment on avance pédagogiquement** : quand et comment introduire une notion, avec quelle thématique, quelle modalité, quelles activités. Il suit toujours le même mouvement :

**sources → options argumentées → recommandation → points à confirmer → décision datée → propagation**

Le cadrage individuel d'un apprenant n'est pas ici : c'est `/debrief`.

## 1. Choisir l'échelle

| Argument | Échelle | Sortie |
| --- | --- | --- |
| `sprint <N>` | Sprint entier | `<dossier du sprint>/cadrage/sprintN-cadrage-<theme>.md` (modèle `.pilotage/modeles/cadrage-sprint.md`) |
| `semaine [date]` | Semaine à venir (par défaut : la prochaine semaine non planifiée) | `05_promotion/veille/propositions-<phase>-semaine-0N.md` (modèle `.pilotage/modeles/planification-semaine.md`) |
| `<sujet libre>` | Activité ponctuelle : workshop, live coding, report, nouvelle notion, réassignation | proposition courte dans la conversation, puis décision |
| `valider <fichier ou sujet>` | Passage de la proposition à la décision | voir étape 5 |

Sans argument, déduire l'échelle de `CURRENT.md` et du planning : sprint suivant non cadré → `sprint` ; semaine prochaine non planifiée → `semaine` ; sinon demander en une ligne.

## 2. Lire (et rien de plus)

Toujours : `PROMO.md`, `CURRENT.md`, `06_pilotage/alertes.md`, `06_pilotage/decisions/INDEX.md`.

- **Sprint** : `00_sources/planning/`, `00_sources/referentiel/` (version Markdown), `06_pilotage/regles-pedagogiques.md`, le `BILAN.md` du sprint précédent, le README et le cadrage des sprints voisins (continuité), `00_sources/legacy/SYNTHESE.md` puis seulement les legacy du même sprint l'an dernier.
- **Semaine** : `05_promotion/veille/regles-veille.md` + bloc `veilles` de `PROMO.md`, registre des attributions (qui a le moins de passages), README et briefs du sprint (brief en cours **et** suivant : quelles notions nouvelles arrivent ?), jours fériés de la période, fiches des apprenants pressentis comme facilitateurs, absences connues.
- **Ponctuel** : les décisions et fiches directement concernées.

Le pilotage (fiches, alertes, audits) **oriente** les choix (qui facilite quoi, quelle notion consolider), mais ne fuit jamais dans un document destiné aux apprenants.

## 3. Proposer

### Sprint
- Périmètre technique, compétences `C*` / `CT*` visées, hors périmètre.
- 3 options de thématique au minimum, avec points forts, pièges (identité utilisateur, données, périmètre trop large) et une **matrice comparative**.
- Recommandation avec critère de départage, piste écartée.
- Découpage en briefs et en semaines, modalités (individuel → binôme → squad) et conditions de transition, progression d'une techno transverse brief par brief.
- Vue de couverture : chaque compétence couverte ; chaque notion nouvelle reliée à la veille ou au workshop qui l'annonce.
- Garde-fous, bonus autorisés après le socle, **points à confirmer**.

### Semaine
- Veilles : une par jour autorisé, sujet qui **prépare une notion d'un brief à venir** (à défaut, éclaire le brief en cours), binôme varié, priorité aux apprenants ayant le moins de passages, pas de jour férié.
- Workshops : objectif, facilitateur(s), créneau **justifié** (après quelles veilles, avant quel usage dans le brief).
- Live coding : sujet, copilotes.
- Quiz de fin de veille : outil et difficulté progressive.
- Équilibre : garder des blocs longs de production ; ne pas surcharger la semaine.

### Ponctuel
- Objectif pédagogique, prérequis, déroulé progressif, créneau justifié, impact sur le reste de la semaine.

Écrire la proposition avec le statut **pré-validation** / **proposition**, chaque élément incertain marqué « à confirmer ». Terminer par la liste courte des questions à trancher, une ligne chacune, avec la recommandation.

## 4. Ne rien confirmer seul

Tant que le formateur n'a pas validé : ne pas toucher au registre des veilles, au README du sprint, ni à `CURRENT.md`. Commit unique de la proposition (`cadrage: proposition <objet>`).

## 5. Valider

Quand le formateur tranche (ici, ou plus tard via `/noter` : « veille du 12 validée avec X et Y »), pour chaque élément validé :

1. Décision datée `06_pilotage/decisions/AAAA-MM-JJ-<objet>.md` (modèle `.pilotage/modeles/decision.md`) + ligne dans `INDEX.md`.
2. Sprint : statut du cadrage → « retenu », README du sprint (thématique, briefs, modalités).
3. Semaine : registre des attributions (confirmées seulement), tableau « Cette semaine » de `CURRENT.md`.
4. Si une décision en remplace une autre : marquer l'ancienne « remplacée » dans l'INDEX.
5. Proposer l'enchaînement : `/brief` après un cadrage de sprint ; préparation des activités plateforme après un cadrage de semaine.

## 6. Finir

`bash scripts/check-organisation.sh`, puis commits atomiques (cadrage, décision, registre séparés). Réponse finale : ce qui est décidé, ce qui reste à confirmer, la commande suivante suggérée.
