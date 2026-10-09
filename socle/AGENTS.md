# AGENTS — règles de travail (Claude, Codex, Cursor, tout agent)

> Fichier **noyau** fourni par le kit de pilotage YouCode (version dans `.pilotage/version`).
> Il est remplacé à chaque mise à jour du kit : ne pas le modifier ici.
> Le contexte et les règles propres à cette promo vivent dans **`PROMO.md`**, qui prévaut en cas de conflit.

Workspace de pilotage pédagogique d'une promo. Le filesystem est la mémoire du projet, pas le chat.
Français par défaut ; termes techniques en anglais.

## 1. Lecture minimale

1. Lire `PROMO.md` (contexte de la promo) et `CURRENT.md` (état du moment). **Ne rien lire d'autre par défaut.**
2. Puis seulement ce que la tâche exige, en passant par les index :
   * sprint → `02_sprints/<sprint>/README.md` (phase close : **seulement** `BILAN.md`) ;
   * apprenant → `05_promotion/apprenants/fiches/<slug>.md`, puis la preuve liée ;
   * identité d'un apprenant (surnom, pseudo GitHub, nom plateforme) → `05_promotion/apprenants/registre-apprenants.md` ;
   * décision → `06_pilotage/decisions/INDEX.md`, puis le fichier utile ;
   * rapport long → lire d'abord le bloc `## Résumé` (30 premières lignes).
3. Brief / sprint / veille / Git pédagogique → `06_pilotage/regles-pedagogiques.md` et `05_promotion/veille/regles-veille.md`.

**Ne pas lire sauf demande explicite** : `00_sources/legacy/**` (passer par sa synthèse `00_sources/legacy/SYNTHESE.md`), `07_outputs/imports/**`, binaires (PDF, XLSX, DOCX, PNG), rapports des phases closes, `06_pilotage/journal/**`. **Ne jamais lire** `_confidentiel/`.

## 2. Commandes du kit

Quand l'utilisateur tape une de ces commandes, ou demande la même chose en clair, suivre le fichier correspondant `.claude/skills/<commande>/SKILL.md` (identique dans `.agents/skills/`).

| Commande | Usage |
| --- | --- |
| `/aide` | Liste des commandes et suggestion de la prochaine selon le moment |
| `/amorcer` | J0 : rassembler et analyser les sources (planning, référentiel, legacy, liste apprenants) |
| `/noter` | Capter n'importe quelle information, n'importe quand, et la propager |
| `/cadrage` | Cadrer un sprint, une semaine (veilles, workshops, lives) ou une activité ponctuelle |
| `/brief` | Rédiger un brief apprenant et sa version plateforme |
| `/audit` | Auditer les rendus et l'activité GitHub |
| `/debrief` | Point individuel, oral, cadrage d'un apprenant |
| `/point` | Question en lecture seule sur l'état de la promo |
| `/bilan` | Clôturer une phase |

## 3. Ranger : un seul endroit par type

Table complète : `06_pilotage/organisation-documentaire.md`. En bref :

* tout ce qui concerne un sprint → `02_sprints/<sprint>/` (`briefs/`, `briefs/plateforme/`, `cadrage/`, `rapports/audits/`, `rapports/preparations/`, `rapports/prompts/`) ; Warm-Up → `01_warmup/` ;
* suivi humain (séances, débriefs, plans d'action) → `05_promotion/suivi/<phase>/` ; état d'un apprenant → sa fiche ;
* décision durable → `06_pilotage/decisions/AAAA-MM-JJ-objet.md` **et** une ligne dans `decisions/INDEX.md` ;
* `07_outputs/` = transversal seulement (posters, pdf, présentations, imports) ;
* note en vrac pas encore triée → `inbox/` (vidée par `/noter`) ;
* données personnelles sensibles → `_confidentiel/` (ignoré par Git) ;
* un document va dans la phase dont il parle, sinon dans la phase en cours ;
* pour déplacer un fichier : `python3 scripts/move-doc.py <ancien> <nouveau>` (met à jour tous les liens) ;
* modèles de documents : `.pilotage/modeles/`.

## 4. Écrire : court, remplacé, lié

* `CURRENT.md` ≤ 10 Ko : on **remplace** l'état, on n'empile pas. L'historique va dans `06_pilotage/journal/AAAA-MM.md`.
* `06_pilotage/alertes.md` : alertes actives uniquement.
* Tout audit commence par `## Résumé` (≤ 10 lignes, verdict par apprenant) et met à jour les fiches apprenants concernées.
* Lier la preuve plutôt que recopier un tableau. Pas de fichiers vides inutiles.
* Ne pas inventer : marquer « à confirmer ». Signaler incohérences, échéances manquantes, compétences oubliées.
* **Proposition ≠ confirmation** : une proposition (veille, cadrage, binôme) reste marquée « à confirmer » ; les registres officiels ne changent qu'après validation explicite du formateur.
* `00_sources/` fait autorité : ne jamais le modifier sans demande explicite.
* Documents destinés aux apprenants (briefs, sujets de veille, workshops) : Markdown, **stateless**, sans pilotage interne, sans faiblesse individuelle ni raison de choix ; compétences techniques `C*` et transversales `CT*` distinguées.

## 5. Lire les profils apprenants sans raccourci

Ne jamais déduire un **profil rouge**, **profil moteur** ou une comparaison globale depuis un seul score de rendu. Toujours nommer l'axe observé avant de classer :

* **production récente** : score, dépôt, retard, non-rendu ;
* **appropriation orale** : capacité à expliquer, modifier, refaire sans aide ;
* **risque IA** : code au-dessus du niveau explicable, traces de génération, dépendance ;
* **rythme / présence** : absences, retards, régularité, relances ;
* **priorité de débrief** : urgence de passage en revue, indépendamment de la validation.

Typologie recommandée :

* **rouge structurel** = appropriation faible + récurrence + risque de validation ;
* **alerte ponctuelle** = chute ou retard sur un livrable récent sans invalider la trajectoire globale ;
* **à challenger** = bon rendu mais appropriation à vérifier ;
* **moteur confirmé** = bon rendu + oral solide + régularité ;
* **cas administratif** = départ, non-rendu, absence ou no-show à tracer.

Interdits de lecture :

* transformer un bon rendu en profil moteur sans oral solide ;
* transformer un mauvais rendu ponctuel en profil rouge global ;
* assimiler deux apprenants sans préciser l'axe de comparaison ;
* confondre « débrief clôturé » avec « compétences validées ».

Quand une fiche contient une note `Lecture agent IA`, elle prévaut pour éviter les raccourcis.

## 6. Fin de tâche et Git

Il n'y a pas de rituel « début / fin de session » : chaque commande termine elle-même son travail.

1. Fichiers rangés selon la table, `CURRENT.md` remplacé si l'état a changé, décision indexée, fiches à jour.
2. `bash scripts/check-organisation.sh` passe.
3. Commits atomiques : un commit = une intention. Vérifier le diff staged ; séparer suivi, audit, décision, brief, cadrage, source, script.
4. Le hook `scripts/hooks/pre-commit` lance le contrôle : corriger plutôt que `--no-verify`. S'il est inactif : `git config core.hooksPath scripts/hooks`.

Clôture d'une phase : voir `/bilan`.
