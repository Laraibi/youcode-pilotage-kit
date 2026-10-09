#!/usr/bin/env bash
# Contrôle d'organisation du workspace — compatible bash 3.2 (macOS) et Linux.
# Usage : bash scripts/check-organisation.sh          (contrôle complet)
#         bash scripts/check-organisation.sh --hook   (appelé par le pre-commit : bloque sur erreur)
# Règles : 06_pilotage/organisation-documentaire.md

cd "$(git rev-parse --show-toplevel)" || exit 2
git() { command git -c core.quotepath=false "$@"; }
MODE="${1:-full}"
ERR=0; WARN=0
e() { printf '  \342\234\227 %s\n' "$*"; ERR=$((ERR+1)); }
w() { printf '  ! %s\n' "$*"; WARN=$((WARN+1)); }

# Fichiers concernés : index Git (ce qui sera commité) + fichiers non suivis non ignorés.
LIST=$(mktemp); trap 'rm -f "$LIST"' EXIT
{ git ls-files; git ls-files --others --exclude-standard; } | sort -u > "$LIST"
# Fichiers ajoutés / modifiés dans ce commit (mode hook) ou tous (mode complet)
if [ "$MODE" = "--hook" ]; then
  CHANGED=$(git diff --cached --name-only --diff-filter=AMR)
else
  CHANGED=$(cat "$LIST")
fi

echo "Contrôle d'organisation du workspace"

# 1. CURRENT.md court
if [ -f CURRENT.md ]; then
  size=$(wc -c < CURRENT.md | tr -d ' ')
  [ "$size" -gt 10240 ] && e "CURRENT.md fait $size octets (> 10 Ko) : remplacer l'état, déplacer l'historique dans 06_pilotage/journal/"
  ref=$(grep -m1 -oE '[0-9]{2}/[0-9]{2}/[0-9]{4}' CURRENT.md)
  if [ -n "$ref" ]; then
    age=$(awk -v r="$ref" -v t="$(date +%d/%m/%Y)" 'function days(s,  a){split(s,a,"/");return a[3]*365+a[2]*30.44+a[1]} BEGIN{printf "%d", days(t)-days(r)}')
    [ "$age" -gt 7 ] && w "CURRENT.md daté du $ref (il y a ~$age jours) : vérifier qu'il reflète encore la phase en cours"
  fi
else
  e "CURRENT.md absent"
fi

# 2. Racine propre
while IFS= read -r f; do
  case "$f" in
    */*) top=${f%%/*}
         case "$top" in
           00_sources|01_warmup|02_sprints|03_fil-rouge|04_soutenances|05_promotion|06_pilotage|07_outputs|scripts|inbox|.cursor|.claude|.agents|.pilotage) ;;
           _confidentiel) e "fichier confidentiel suivi par Git : $f" ;;
           *) e "dossier racine non prévu : $f" ;;
         esac ;;
    README.md|INDEX.md|CURRENT.md|AGENTS.md|CLAUDE.md|PROMO.md|promo.yml|.gitignore|.gitattributes|.cursorignore|.cursorindexingignore) ;;
    *) e "fichier à la racine non prévu : $f (voir organisation-documentaire.md)" ;;
  esac
done < "$LIST"

# 3. 07_outputs = transversal uniquement
while IFS= read -r f; do
  case "$f" in
    07_outputs/posters/*|07_outputs/pdf/*|07_outputs/presentations/*|07_outputs/imports/*) ;;
    07_outputs/reports/*/*) e "rapport de phase dans 07_outputs : $f -> 02_sprints/<sprint>/rapports/ ou 01_warmup/rapports/" ;;
    07_outputs/reports/*) ;;
    07_outputs/briefs/*) e "brief dans 07_outputs : $f -> 02_sprints/<sprint>/briefs/plateforme/" ;;
    07_outputs/*) e "emplacement non prévu dans 07_outputs : $f" ;;
  esac
done < "$LIST"

# 4. Données sensibles hors _confidentiel
grep -iE '(justificatif|certificat[_-]|acte[-_ ]?naissance|donnees-administratives|(^|/)\.env$)' "$LIST" | grep -v '^_confidentiel/' | grep -v '\.env\.example$' | while IFS= read -r f; do
  printf '  \342\234\227 donnée sensible suivie : %s -> _confidentiel/\n' "$f"; done
SENS=$(grep -iE '(justificatif|certificat[_-]|acte[-_ ]?naissance|donnees-administratives|(^|/)\.env$)' "$LIST" | grep -v '^_confidentiel/' | grep -vc '\.env\.example$')
ERR=$((ERR+SENS))

# 5. Décisions indexées
if [ -f 06_pilotage/decisions/INDEX.md ]; then
  for f in $(grep -E '^06_pilotage/decisions/[0-9]{4}-.*\.md$' "$LIST"); do
    b=$(basename "$f")
    grep -q "$b" 06_pilotage/decisions/INDEX.md || e "décision non indexée : $b -> ajouter une ligne dans 06_pilotage/decisions/INDEX.md"
  done
else
  e "06_pilotage/decisions/INDEX.md absent"
fi

# 6. Audits avec résumé (phases non closes uniquement)
while IFS= read -r f; do [ -n "$f" ] || continue
  case "$f" in
    */rapports/audits/*.md)
      phase=${f%%/rapports/*}
      [ -f "$phase/BILAN.md" ] && continue
      [ -f "$f" ] && ! head -30 "$f" | grep -q '^## Résumé' && w "audit sans bloc '## Résumé' dans les 30 premières lignes : $f" ;;
  esac
done <<< "$CHANGED"

# 7. Rapports rangés dans les phases closes (ajouts)
if [ "$MODE" = "--hook" ]; then
  for f in $(git diff --cached --name-only --diff-filter=A); do
    case "$f" in
      01_warmup/*|02_sprints/*/*)
        phase=$(echo "$f" | cut -d/ -f1-2); [ "${f%%/*}" = "01_warmup" ] && phase=01_warmup
        [ -f "$phase/BILAN.md" ] && [ "$f" != "$phase/BILAN.md" ] && w "ajout dans une phase close ($phase) : $f — est-ce bien la bonne phase ?" ;;
    esac
  done
fi

# 8. Fiches apprenants courtes
for f in $(grep -E '^05_promotion/apprenants/fiches/.*\.md$' "$LIST"); do
  [ -f "$f" ] || continue
  s=$(wc -c < "$f" | tr -d ' '); [ "$s" -gt 4096 ] && w "fiche longue ($s o) : $f — garder état + liens"
done

# 9. Fichiers lourds / archives
while IFS= read -r f; do
  [ -f "$f" ] || continue
  case "$f" in 00_sources/*) ;; *.zip|*.rar|*.7z) w "archive suivie : $f — extraire, synthétiser, supprimer (organisation-documentaire.md)";; esac
  s=$(wc -c < "$f" | tr -d ' '); [ "$s" -gt 5242880 ] && w "fichier > 5 Mo : $f"
done < "$LIST"

# 10. Liens cassés dans les .md modifiés
while IFS= read -r f; do [ -n "$f" ] || continue
  case "$f" in *.md|*.mdc) ;; *) continue;; esac
  [ -f "$f" ] || continue
  case "$f" in 00_sources/legacy/*|06_pilotage/journal/*) continue;; esac
  # fichiers fournis par le kit : ils citent des chemins créés plus tard par les commandes
  case "$f" in .claude/*|.agents/*|.pilotage/*|.cursor/*|AGENTS.md|00_sources/templates/*|06_pilotage/organisation-documentaire.md|06_pilotage/regles-pedagogiques.md|05_promotion/veille/regles-veille.md) continue;; esac
  # en contrôle complet, les archives (décisions, phases closes) ne sont pas revérifiées
  if [ "$MODE" != "--hook" ]; then
    case "$f" in 06_pilotage/decisions/20*) continue;; esac
    ph=$(echo "$f" | cut -d/ -f1-2); [ "${f%%/*}" = "01_warmup" ] && ph=01_warmup
    [ -f "$ph/BILAN.md" ] && continue
  fi
  d=$(dirname "$f")
  # chemins écrits depuis la racine entre backticks
  for p in $(grep -oE '`0[0-7]_[^` ]+`' "$f" | tr -d '`' | sed 's/#.*//' | sort -u); do
    case "$p" in */*) ;; *) continue;; esac
    case "$p" in */) continue;; esac  # dossier créé à la demande
    case "$p" in *'*'*|*'<'*|*'…'*|*'{'*|*AAAA*|*.zip) continue;; esac
    [ -e "$p" ] || w "lien cassé dans $f : $p"
  done
  # liens Markdown relatifs
  for p in $(grep -oE '\]\([^)# ]+' "$f" | sed 's/^](//' | sort -u); do
    case "$p" in http*|mailto:*|/*|*%*) continue;; esac
    [ -e "$d/$p" ] || w "lien cassé dans $f : $p"
  done
done <<< "$CHANGED"

# 11. Fiches apprenants synchronisées avec les documents
if command -v python3 >/dev/null 2>&1 && [ -d 05_promotion/apprenants/fiches ]; then
  python3 scripts/maj-fiches.py --check >/dev/null 2>&1 || w "fiches apprenants à régénérer : python3 scripts/maj-fiches.py"
fi

# 12. Boîte de dépôt : à trier par /noter
n=$(grep -c '^inbox/' "$LIST" | tr -d ' ')
n=$((n - $(grep -c '^inbox/\(README.md\|.gitkeep\)$' "$LIST" | tr -d ' ')))
[ "$n" -gt 0 ] && w "$n fichier(s) en attente dans inbox/ : lancer /noter pour les trier"

# 13. Hook actif
[ "$(git config core.hooksPath)" = "scripts/hooks" ] || w "hook inactif : lancer 'git config core.hooksPath scripts/hooks'"

echo "Résultat : $ERR erreur(s), $WARN avertissement(s)"
[ "$MODE" = "--hook" ] && [ "$ERR" -gt 0 ] && { echo "Commit bloqué. Corriger (voir 06_pilotage/organisation-documentaire.md)."; exit 1; }
exit 0
