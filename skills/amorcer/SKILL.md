---
name: amorcer
description: Démarrage d'une promo (J0) ou ajout d'une nouvelle source - rassembler et analyser le planning, le référentiel, les anciens briefs et veilles (legacy) et la liste des apprenants, puis préparer le registre, les fiches et les README de phase.
argument-hint: "[planning | referentiel | legacy | apprenants]"
---

# /amorcer

Rassembler les sources est l'investissement du début : c'est ce qui rend toutes les autres commandes pertinentes. Cette commande le fait **une fois**, proprement, et peut être relancée à chaque nouvelle source.

Avec un argument, ne traiter que cette source. Sans argument, faire l'état des lieux puis traiter ce qui manque, dans l'ordre ci-dessous.

## 0. État des lieux

Lister ce qui est présent dans `00_sources/` et `_confidentiel/` (noms de fichiers seulement pour `_confidentiel/` : ne jamais en lire le contenu ; demander au formateur de coller la liste anonymisée si nécessaire). Dire en une ligne par source : présent, absent, déjà analysé.
Si `promo.yml` contient encore les valeurs d'exemple, le signaler d'abord.

## 1. Planning

Lire le planning déposé (xlsx, export Google Sheets, PDF, image). Produire `00_sources/planning/planning-reference.md` : phases, dates, technologies par sprint, jalons (soutenances, certifications), jours fériés repérés. Vérifier la cohérence avec `promo.yml` et signaler les écarts.

## 2. Référentiel

Lire le référentiel (souvent un xlsx exporté de Google Sheets). Produire `00_sources/referentiel/referentiel-reference.md` au **format standard du kit** :

| Code | Type (`C` technique / `CT` transversale) | Libellé | Niveaux | Critères observables |

puis `06_pilotage/progression-referentiel.md` : quelle compétence à quel sprint, à quel niveau. Ce format commun permettra plus tard de comparer entre promos sans imposer le même référentiel.

## 3. Legacy

Pour les anciens briefs, veilles et plannings (`00_sources/legacy/`) : ne pas convertir, **synthétiser**. Produire `00_sources/legacy/SYNTHESE.md` (≤ 1 page par catégorie) :

- briefs : thématiques par sprint, exigences récurrentes, structure type (enrichir `00_sources/templates/brief-template-reference.md` si utile), pièges connus ;
- veilles : sujets passés par sprint, ce qui a bien ou mal fonctionné ;
- planning : écarts entre l'an dernier et cette année.

Les fichiers legacy restent intacts ; les commandes suivantes passent par la synthèse.

## 4. Apprenants

À partir d'un export CSV (YouCode, Simplonline) ou d'une liste collée :

1. Les coordonnées et données administratives restent dans `_confidentiel/`.
2. Remplir `05_promotion/apprenants/registre-apprenants.md` : slug, nom complet, statut ; surnoms, GitHub, nom plateforme et squad restent « à collecter » s'ils sont inconnus (ils se complètent au fil de l'eau via `/noter` et `/audit`).
3. Créer une fiche par apprenant depuis `.pilotage/modeles/fiche-apprenant.md` dans `05_promotion/apprenants/fiches/<slug>.md` : `motifs` = regex des façons de le nommer (prénom, nom, surnoms), `fichiers` = mots du slug.
4. `python3 scripts/maj-fiches.py`.

## 5. Finir

- Mettre à jour `CURRENT.md` (phase, première semaine, priorités) et le README de la première phase.
- `bash scripts/check-organisation.sh`, puis un commit par source traitée (`source: planning`, `source: referentiel`, `legacy: synthese`, `apprenants: registre et fiches`).
- Réponse : ce qui est prêt, ce qui manque, et la suite logique (en général `/cadrage sprint 1` ou `/cadrage semaine`).
