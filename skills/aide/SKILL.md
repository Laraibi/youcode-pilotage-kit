---
name: aide
description: Afficher les commandes du kit de pilotage et suggérer la prochaine action selon le moment de la formation. Avec un nom de commande, expliquer ce qu'elle lit, ce qu'elle écrit, avec des exemples.
argument-hint: "[commande]"
---

# /aide

Lecture seule : cette commande ne modifie aucun fichier.

## Sans argument

1. Afficher le tableau, une ligne par commande :

| Commande | Quand | En une phrase |
| --- | --- | --- |
| `/noter` | N'importe quand | Je dépose une info (texte, capture, CSV), elle va au bon endroit et met à jour les fiches. |
| `/cadrage` | Avant un sprint, chaque fin de semaine, à la demande | Options argumentées pour un sprint, une semaine (veilles, workshops, lives) ou une activité, puis décision. |
| `/brief` | Après un cadrage de sprint validé | Brief apprenant stateless + version plateforme. |
| `/audit` | Pendant un brief | Rendus et activité GitHub, verdict par apprenant, fiches à jour. |
| `/debrief` | Point individuel, oral | Verdict par compétence, plan d'action, fiche et alertes. |
| `/point` | N'importe quand | Question libre sur l'état de la promo, sans rien modifier. |
| `/bilan` | Fin de phase | BILAN, alertes closes, CURRENT pour la phase suivante. |
| `/amorcer` | J0, nouvelle source | Planning, référentiel, legacy, liste apprenants. |
| `/aide <commande>` | | Détail d'une commande. |

2. **Suggérer la prochaine action** (2 lignes maximum), en lisant uniquement `PROMO.md`, `CURRENT.md`, `06_pilotage/alertes.md` et la liste des fichiers de `inbox/`, `00_sources/` et du sprint en cours. Règles, dans l'ordre :
   - promo pas amorcée (`promo.yml` d'exemple, registre vide, pas de `planning-reference.md`) → guider vers `/amorcer`, étape par étape (voir plus bas) ;
   - fichiers en attente dans `inbox/` → `/noter` ;
   - sprint suivant à moins de deux semaines sans cadrage retenu → `/cadrage sprint <N>` ;
   - on est jeudi ou vendredi et la semaine suivante n'a pas de planification → `/cadrage semaine` ;
   - échéance de brief passée sans audit → `/audit` ;
   - alerte 🔴 avec débrief à faire → `/debrief <apprenant>` ;
   - dernier jour de phase → `/bilan`.
   Sinon : « Rien d'urgent ; `/point` pour un état de la promo. »

## Avec une commande en argument

Lire `.claude/skills/<commande>/SKILL.md` et répondre en 10 lignes maximum : à quoi elle sert, ce qu'elle lit, ce qu'elle écrit, ce qu'elle ne fait jamais seule, et 2 ou 3 exemples d'appel réalistes (par exemple `/cadrage semaine`, `/noter absents ce matin : X et Y, Z en retard 10h40`).

## Nouveau formateur (promo non amorcée)

Guider dans cet ordre, une étape à la fois, en vérifiant chacune avant la suivante :

1. Remplir `promo.yml` (nom, parcours, phases avec dates, plateformes, règles de veille), puis relancer l'installeur du kit.
2. Déposer le planning dans `00_sources/planning/` et le référentiel (export xlsx du Google Sheet) dans `00_sources/referentiel/`.
3. Déposer les anciens briefs et veilles dans `00_sources/legacy/`.
4. Mettre la liste nominative (export CSV de la plateforme) dans `_confidentiel/`.
5. Lancer `/amorcer`.
6. Puis `/cadrage sprint 1` (ou `/cadrage semaine` si le sprint est déjà cadré).
7. Pousser le dépôt sur GitHub **en privé** pour pouvoir utiliser `/noter` depuis le téléphone.
