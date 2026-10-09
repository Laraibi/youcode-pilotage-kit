---
name: debrief
description: Préparer ou consigner un point individuel avec un apprenant (débrief de brief, oral, mise en situation, cadrage individuel, plan d'action), puis mettre à jour sa fiche et les alertes.
argument-hint: "<apprenant> [preparer | <notes du débrief>]"
---

# /debrief

## Préparer (`/debrief <apprenant> preparer`)

Lire la fiche, le dernier audit le concernant (bloc Résumé puis sa section), ses alertes. Produire en conversation (pas de fichier sauf demande) :

- 3 à 5 questions pour vérifier l'appropriation : expliquer, modifier en direct, refaire sans aide ;
- une mini mise en situation courte liée au code rendu ;
- les points de la fiche à confirmer ou infirmer.

Pour une série de débriefs (toute la classe), produire une checklist dans `<dossier du sprint>/rapports/preparations/checklist-debrief-<objet>-AAAA-MM-JJ.md`.

## Consigner (`/debrief <apprenant> <notes>`)

Les notes peuvent être brutes, dictées, partielles.

1. Écrire `05_promotion/suivi/<phase>/AAAA-MM-JJ-debrief-<objet>-<slug>.md` (modèle `.pilotage/modeles/debrief.md`) : contexte, observations, **verdict par compétence** avec preuve, plan d'action avec échéance.
2. Ne pas confondre « débrief clôturé » et « compétences validées » ; nommer l'axe observé (section 5 d'`AGENTS.md`). Si une note `Lecture agent IA` existe dans la fiche, la respecter.
3. Fiche : remplacer la ligne d'état et la prochaine action.
4. Alertes : ouvrir, faire évoluer ou fermer.
5. Si le débrief entraîne une décision (modalité individuelle, rattrapage, changement de binôme) : décision datée + INDEX.

`python3 scripts/maj-fiches.py`, `bash scripts/check-organisation.sh`, commits séparés (`suivi:`, `fiche:`, `decision:`). Réponse : verdict et prochaine action, en 3 lignes.
