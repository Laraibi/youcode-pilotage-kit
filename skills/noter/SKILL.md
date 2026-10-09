---
name: noter
description: Capter n'importe quelle information de la formation (présence, observation, rendu, débrief, décision, info administrative, CSV, capture, liste de liens), à n'importe quel moment, puis la propager aux fiches, au registre, aux alertes et à CURRENT. Sans argument, trie la boîte inbox/.
argument-hint: "<texte, fichier, capture ou CSV> | (vide pour trier inbox/)"
---

# /noter

Point d'entrée unique pour tout ce qui arrive au fil de l'eau : en classe, hors classe, pendant un débrief, le soir depuis le téléphone. Le formateur ne range rien ; la commande s'en charge.

## 1. Rassembler

- Avec argument : le texte collé, le fichier ou la capture fournis.
- Sans argument : tous les fichiers de `inbox/` (sauf `README.md`), du plus ancien au plus récent.

## 2. Comprendre

Pour chaque morceau d'information :

1. **Type** : présence · observation de séance · rendu (lien GitHub, dépôt) · débrief · décision ou validation · info administrative · import (CSV YouCode, Simplonline, liste).
2. **Apprenants concernés** : les reconnaître via `05_promotion/apprenants/registre-apprenants.md` (nom, surnom, pseudo GitHub, nom plateforme). Un nom inconnu : le signaler, ne pas deviner. Un nouveau surnom ou pseudo confirmé : l'ajouter au registre.
3. **Moment** : date et heure de l'événement (pas de la saisie), phase concernée.
4. **Sensibilité** : justificatif médical, téléphone, adresse, situation personnelle → `_confidentiel/` uniquement, avec une mention neutre ailleurs (« absence justifiée »).

Si une information est ambiguë au point de changer où elle va, poser **une** question courte ; sinon avancer.

## 3. Ranger la trace

Une trace datée par événement, selon `06_pilotage/organisation-documentaire.md` :

- présence → `05_promotion/suivi/presences/AAAA-MM-JJ-presences-<objet>.md` ;
- observation, débrief court → `05_promotion/suivi/<phase>/AAAA-MM-JJ-<objet>.md` (modèle `.pilotage/modeles/note.md`) ;
- rendu → compléter la colonne GitHub du registre ; lien de dépôt noté dans la fiche ;
- import CSV → `07_outputs/imports/<source>-AAAA-MM-JJ.csv` + mise à jour du registre ; données personnelles retirées vers `_confidentiel/` ;
- validation d'une proposition de `/cadrage` → appliquer l'étape « Valider » de `/cadrage`.

Plusieurs informations sur un même événement : un seul fichier. Une note de deux lignes sur un apprenant peut aller directement dans sa fiche sans fichier séparé.

## 4. Propager

- **Fiche** de chaque apprenant concerné : remplacer la ligne d'état touchée (pas empiler), lier la trace.
- **Alertes** (`06_pilotage/alertes.md`) : ouvrir, faire évoluer ou fermer, en nommant l'axe (production, appropriation orale, risque IA, rythme, administratif) ; respecter la section 5 d'`AGENTS.md`.
- **`CURRENT.md`** : seulement si l'information change une priorité ou le programme de la semaine.
- **Décision** : si la note tranche quelque chose de durable, fichier daté + ligne dans l'INDEX.
- `python3 scripts/maj-fiches.py` pour régénérer les liens des fiches.

## 5. Finir

Vider de `inbox/` ce qui a été traité. `bash scripts/check-organisation.sh`, puis commits atomiques (`suivi:`, `fiche:`, `alerte:`, `decision:`).
Réponse en 3 lignes maximum : ce qui a été noté, où c'est allé, ce qui reste à confirmer.
