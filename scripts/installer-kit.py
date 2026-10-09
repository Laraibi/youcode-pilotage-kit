#!/usr/bin/env python3
"""Installe ou met à jour le kit de pilotage dans le dépôt d'une promo.

Usage :
  python3 <kit>/scripts/installer-kit.py <dossier-promo>             installe ou met à jour
  python3 <kit>/scripts/installer-kit.py <dossier-promo> --dry-run   montre sans rien écrire
  ajouter --adopter pour installer dans un workspace existant qui n'a jamais utilisé le kit

Deux catégories de fichiers :
  * fichiers du KIT : remplacés à chaque mise à jour (AGENTS.md, commandes, scripts, modèles, règles noyau) ;
  * fichiers de la PROMO : créés une seule fois, jamais écrasés (PROMO.md, CURRENT.md, fiches, décisions…).
Compatible Python 3.8+ sans dépendance (PyYAML utilisé s'il est installé).
"""
import os, re, shutil, subprocess, sys
from datetime import date

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOCLE = os.path.join(KIT, "socle")
COMMANDES = ["aide", "amorcer", "noter", "cadrage", "brief", "audit", "debrief", "point", "bilan"]

# Fichiers du kit, remplacés à chaque mise à jour (chemins relatifs au socle)
KIT_FILES = [
    "AGENTS.md", "CLAUDE.md", ".cursor/rules/pilotage.mdc",
    "scripts/check-organisation.sh", "scripts/move-doc.py", "scripts/maj-fiches.py", "scripts/hooks/pre-commit",
    "06_pilotage/organisation-documentaire.md", "06_pilotage/regles-pedagogiques.md",
]
# Fichiers du socle copiés une seule fois (le formateur peut les adapter)
ONCE_FILES = [
    ".gitignore", ".cursorignore", ".claude/settings.json",
    "05_promotion/veille/regles-veille.md", "00_sources/templates/brief-template-reference.md",
]


# ---------- lecture de promo.yml (sous-ensemble YAML) ----------

def _scalar(v):
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        return [_scalar(x) for x in v[1:-1].split(",") if x.strip()]
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def _parse(lines, i, indent):
    """Parse un bloc d'indentation `indent` à partir de la ligne i. Retourne (valeur, i)."""
    if i < len(lines) and lines[i][1].startswith("- "):
        out = []
        while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
            first = lines[i][1][2:]
            if ":" in first and not first.startswith("["):
                # élément de liste = dictionnaire ; ses clés suivantes sont indentées de indent + 2
                lines[i] = (indent + 2, first)
                val, i = _parse(lines, i, indent + 2)
            else:
                val, i = _scalar(first), i + 1
            out.append(val)
        return out, i
    out = {}
    while i < len(lines) and lines[i][0] == indent:
        text = lines[i][1]
        key, _, rest = text.partition(":")
        i += 1
        if rest.strip():
            out[key.strip()] = _scalar(rest)
        elif i < len(lines) and lines[i][0] > indent:
            out[key.strip()], i = _parse(lines, i, lines[i][0])
        else:
            out[key.strip()] = ""
    return out, i


def lire_promo(path):
    text = open(path, encoding="utf-8").read()
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text)
    except ImportError:
        pass
    lines = []
    for raw in text.splitlines():
        s = re.sub(r"\s+#.*$", "", raw) if not raw.lstrip().startswith("#") else ""
        if s.strip():
            lines.append((len(s) - len(s.lstrip()), s.strip()))
    val, _ = _parse(lines, 0, 0)
    return val


# ---------- écriture ----------

class Installeur:
    def __init__(self, cible, dry):
        self.cible, self.dry = cible, dry
        self.crees, self.maj = [], []

    def ecrire(self, rel, contenu, remplacer):
        dest = os.path.join(self.cible, rel)
        existe = os.path.exists(dest)
        if existe and not remplacer:
            return
        if existe and open(dest, encoding="utf-8").read() == contenu:
            return
        (self.maj if existe else self.crees).append(rel)
        if self.dry:
            return
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(contenu)
        if rel.startswith("scripts/") and not rel.endswith(".md"):
            os.chmod(dest, 0o755)

    def copier(self, src, rel, remplacer):
        self.ecrire(rel, open(src, encoding="utf-8").read(), remplacer)


def fmt(d):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})$", str(d))
    return f"{m.group(3)}/{m.group(2)}/{m.group(1)}" if m else str(d)


def liste(v):
    return ", ".join(v) if isinstance(v, list) else str(v or "à confirmer")


def promo_md(p):
    pr = p.get("promo", {})
    v = p.get("veilles", {}) or {}
    phases = "\n".join(
        f"| {ph.get('titre', ph.get('id'))} | {fmt(ph.get('debut'))} → {fmt(ph.get('fin'))} | `{ph.get('dossier')}/` |"
        for ph in p.get("phases", []))
    return f"""# PROMO — {pr.get('nom', 'à confirmer')}

> Fichier **propre à cette promo** : jamais modifié par les mises à jour du kit. Il prévaut sur `AGENTS.md`.
> Généré le {date.today().strftime('%d/%m/%Y')} depuis `promo.yml` ; à enrichir librement.

## Contexte

- Parcours : {pr.get('parcours', 'à confirmer')} · année {pr.get('annee', 'à confirmer')} · {pr.get('campus', '')}
- Formateur : {pr.get('formateur', 'à confirmer')}
- Plateformes de saisie : {liste(p.get('plateformes'))}
- Jours fériés : calendrier `{pr.get('pays_feries', 'à confirmer')}`

## Phases

| Phase | Dates | Dossier |
| --- | --- | --- |
{phases}

## Veilles

{liste(v.get('jours'))} · {v.get('moment', 'matin')} · {v.get('modalite', 'binome')} · {v.get('duree_minutes', 15)} min · quiz : {liste(v.get('quiz'))}.
Ces valeurs prévalent sur `05_promotion/veille/regles-veille.md`.

## Règles locales

Ajouter ici les règles propres à la promo, découvertes en marchant (une ligne chacune, avec la décision liée).

- …
"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry, adopter = "--dry-run" in sys.argv, "--adopter" in sys.argv
    if len(args) != 1:
        sys.exit(__doc__)
    cible = os.path.abspath(args[0])
    os.makedirs(cible, exist_ok=True)
    version = open(os.path.join(KIT, "VERSION"), encoding="utf-8").read().strip()

    yml = os.path.join(cible, "promo.yml")
    if not os.path.exists(yml):
        if not dry:
            shutil.copy(os.path.join(KIT, "promo.example.yml"), yml)
        sys.exit(f"promo.yml créé dans {cible} : remplis-le, puis relance la même commande.")

    marqueur = os.path.join(cible, ".pilotage", "version")
    if os.path.exists(os.path.join(cible, "AGENTS.md")) and not os.path.exists(marqueur) and not adopter:
        sys.exit("Ce dossier a déjà un AGENTS.md qui ne vient pas du kit : relancer avec --adopter "
                 "pour le remplacer par le noyau du kit (sauvegarder d'abord ses règles locales dans PROMO.md).")
    ancienne = open(marqueur).read().strip() if os.path.exists(marqueur) else None

    p = lire_promo(yml)
    ins = Installeur(cible, dry)
    today = date.today().strftime("%d/%m/%Y")

    # 1. Fichiers du kit (remplacés)
    for rel in KIT_FILES:
        ins.copier(os.path.join(SOCLE, rel), rel, True)
    for f in sorted(os.listdir(os.path.join(KIT, "modeles"))):
        ins.copier(os.path.join(KIT, "modeles", f), f".pilotage/modeles/{f}", True)
    for c in COMMANDES:
        src = os.path.join(KIT, "skills", c, "SKILL.md")
        ins.copier(src, f".claude/skills/{c}/SKILL.md", True)
        ins.copier(src, f".agents/skills/{c}/SKILL.md", True)
        ins.ecrire(f".cursor/commands/{c}.md",
                   f"Suis exactement les instructions de `.claude/skills/{c}/SKILL.md`, avec ce que j'ai écrit après la commande comme argument.\n",
                   True)
    ins.ecrire(".pilotage/version", version + "\n", True)

    # 2. Fichiers de la promo (créés une fois)
    for rel in ONCE_FILES:
        ins.copier(os.path.join(SOCLE, rel), rel, False)
    modele = lambda n: open(os.path.join(KIT, "modeles", n), encoding="utf-8").read()
    phases = p.get("phases", []) or []
    premiere = phases[0].get("titre", "") if phases else "à confirmer"
    ins.ecrire("PROMO.md", promo_md(p), False)
    ins.ecrire("CURRENT.md", modele("current.md").replace("{{DATE}}", today).replace("{{PHASE_EN_COURS}}", f"{premiere} (avant démarrage)"), False)
    ins.ecrire("06_pilotage/alertes.md", modele("alertes.md"), False)
    ins.ecrire("06_pilotage/decisions/INDEX.md", modele("decisions-index.md"), False)
    ins.ecrire("05_promotion/apprenants/registre-apprenants.md", modele("registre-apprenants.md"), False)
    ins.ecrire("05_promotion/veille/registre-attributions-veille.md",
               "# Registre des attributions de veille\n\nVeilles **confirmées** uniquement (date, sujet, binôme). Les propositions vivent à côté, dans `propositions-*.md`.\n\n| Date | Sujet | Apprenant(s) | Phase | Décision |\n| --- | --- | --- | --- | --- |\n", False)
    for ph in phases:
        ins.ecrire(f"{ph['dossier']}/README.md",
                   modele("readme-sprint.md").replace("{{TITRE}}", ph.get("titre", ph["id"]))
                   .replace("{{DEBUT}}", fmt(ph.get("debut"))).replace("{{FIN}}", fmt(ph.get("fin"))), False)
    ins.ecrire("00_sources/README.md",
               "# Sources\n\nSources faisant autorité, déposées par le formateur et lues par `/amorcer` :\n\n"
               "- `planning/` : planning officiel (xlsx, export Google Sheets…) ;\n"
               "- `referentiel/` : référentiel de compétences (xlsx) ;\n"
               "- `legacy/` : anciens briefs, veilles, plannings des années précédentes ;\n"
               "- `templates/` : squelettes de documents.\n\nLa liste nominative des apprenants va dans `_confidentiel/`, pas ici.\n", False)
    ins.ecrire("inbox/README.md",
               "# Boîte de dépôt\n\nDépose ici n'importe quoi pendant la journée (capture, CSV, notes en vrac, liens). "
               "`/noter` sans argument trie tout, propage aux fiches et vide la boîte.\n", False)
    ins.ecrire("_confidentiel/README.md",
               "# Confidentiel\n\nHors Git et interdit aux agents : liste nominative avec coordonnées, justificatifs, données administratives.\n", False)
    ins.ecrire("README.md",
               f"# {p.get('promo', {}).get('nom', 'Promo')} — workspace de pilotage\n\n"
               "Point d'entrée : `CURRENT.md` (état du moment) · `PROMO.md` (contexte) · `/aide` (commandes).\n"
               "Généré par le kit de pilotage YouCode ; organisation : `06_pilotage/organisation-documentaire.md`.\n", False)

    # 3. Git
    if not dry:
        if not os.path.isdir(os.path.join(cible, ".git")):
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=cible, check=False)
        subprocess.run(["git", "config", "core.hooksPath", "scripts/hooks"], cwd=cible, check=False)

    titre = "Mise à jour" if ancienne else "Installation"
    print(f"{titre} du kit {ancienne + ' -> ' if ancienne else ''}{version} dans {cible}" + (" (simulation)" if dry else ""))
    print(f"  {len(ins.crees)} fichier(s) créé(s), {len(ins.maj)} fichier(s) du kit mis à jour")
    for r in ins.maj:
        print(f"  ~ {r}")
    if not ancienne:
        print("\nÉtape suivante : dépose tes sources dans 00_sources/ (planning, référentiel, legacy),"
              " la liste nominative dans _confidentiel/, puis lance /amorcer dans ton agent.")


main()
