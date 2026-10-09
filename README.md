# Kit de pilotage pédagogique YouCode

Un formateur, une promo, un dépôt Git qui sert de mémoire, et des agents (Claude, Codex, Cursor) qui savent où lire, où ranger et quoi mettre à jour.
Le kit livre **la structure et les gestes répétés** d'une promo pilote, sans ses données : chaque formateur crée sa propre instance pour sa promo.

## Ce que contient le kit

| Dossier | Contenu | Dans la promo |
| --- | --- | --- |
| `skills/` | Les 9 commandes, écrites une seule fois | copiées dans `.claude/skills/`, `.agents/skills/` et `.cursor/commands/` |
| `socle/` | `AGENTS.md` noyau, règles, organisation documentaire, scripts, hook Git | copié à la racine |
| `modeles/` | Fiche apprenant, décision, cadrage, planification de semaine, audit, débrief, bilan… | `.pilotage/modeles/` |
| `scripts/installer-kit.py` | Installation et mise à jour | — |
| `promo.example.yml` | Description d'une promo | à copier en `promo.yml` |

## Les commandes

| Commande | Quand | Rôle |
| --- | --- | --- |
| `/aide` | Toujours | Liste des commandes et prochaine action suggérée selon le moment |
| `/amorcer` | J0, nouvelle source | Planning, référentiel, legacy, liste apprenants |
| `/noter` | N'importe quand | Capter une info (texte, capture, CSV) et la propager aux fiches, registre, alertes |
| `/cadrage` | Avant un sprint, chaque semaine, à la demande | Options argumentées puis décision : sprint, semaine (veilles, workshops, lives), activité |
| `/brief` | Après un cadrage validé | Brief apprenant stateless + version plateforme |
| `/audit` | Pendant un brief | Rendus et activité GitHub, verdict, fiches |
| `/debrief` | Point individuel | Verdict par compétence, plan d'action |
| `/point` | N'importe quand | Question en lecture seule |
| `/bilan` | Fin de phase | BILAN, alertes closes, CURRENT suivant |

## Démarrer une promo

Prérequis : `git`, `python3`, un compte Claude, Codex ou Cursor.

```bash
git clone https://github.com/Laraibi/youcode-pilotage-kit.git ~/projects/youcode-pilotage-kit
mkdir ~/projects/ma-promo
python3 ~/projects/youcode-pilotage-kit/scripts/installer-kit.py ~/projects/ma-promo   # crée promo.yml
# remplir ~/projects/ma-promo/promo.yml, puis :
python3 ~/projects/youcode-pilotage-kit/scripts/installer-kit.py ~/projects/ma-promo
```

Ensuite, ouvrir le dossier de la promo dans son agent et taper `/aide` : il guide jusqu'à `/amorcer`.
Pour noter depuis le téléphone, pousser le dépôt de la promo sur GitHub **en privé**.

## Mettre à jour

```bash
git -C ~/projects/youcode-pilotage-kit pull
python3 ~/projects/youcode-pilotage-kit/scripts/installer-kit.py ~/projects/ma-promo
```

Seuls les fichiers du kit sont remplacés (`AGENTS.md`, commandes, scripts, modèles, règles noyau). `PROMO.md`, `CURRENT.md`, les fiches, décisions et tout le contenu de la promo ne sont jamais touchés. Les règles propres à une promo vont dans `PROMO.md`.

## Données personnelles

La liste nominative, les coordonnées et les justificatifs vont dans `_confidentiel/` : ignoré par Git et interdit en lecture aux agents (Claude via `.claude/settings.json`, Cursor via `.cursorignore`, Codex via `AGENTS.md`). Avec un compte personnel, désactiver l'utilisation des conversations pour l'entraînement des modèles.

## Compatibilité des agents

- **Claude Code** (terminal, desktop, web, mobile) : commandes `/noter`, `/cadrage`… disponibles directement via `.claude/skills/`.
- **Codex** : skills lus depuis `.agents/skills/` ; `AGENTS.md` renvoie aussi vers eux.
- **Cursor** : commandes `/` via `.cursor/commands/`, règles via `.cursor/rules/pilotage.mdc`.

Le support exact de Codex et Cursor est à vérifier à chaque version de ces outils ; dans tous les cas, demander « fais un cadrage de semaine » fonctionne grâce à `AGENTS.md`.

## Feuille de route

- [x] 0.1 Squelette : socle, commandes, modèles, installeur
- [ ] Rejouer la promo pilote dans un dépôt neuf généré par le kit
- [ ] Promo d'exemple entièrement fictive
- [ ] Pilote avec 1 ou 2 formateurs
- [ ] Passage à l'échelle : saisie sur les plateformes (YouCode, Simplonline), imports normalisés
