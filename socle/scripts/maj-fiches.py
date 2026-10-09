#!/usr/bin/env python3
"""Régénère la section « Documents » des fiches apprenants (05_promotion/apprenants/fiches/).

Chaque fiche déclare, en commentaires HTML :
  <!-- motifs: regex -->        mots qui désignent l'apprenant dans les textes
  <!-- fichiers: mot1,mot2 -->  mots présents dans le NOM des documents qui lui sont dédiés
La section entre <!-- AUTO:liens --> et <!-- /AUTO:liens --> est réécrite ; le reste n'est jamais touché.

Usage : python3 scripts/maj-fiches.py           (met à jour)
        python3 scripts/maj-fiches.py --check   (code 1 si une fiche n'est pas à jour)
"""
import os, re, subprocess, sys

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
os.chdir(ROOT)
FICHES = "05_promotion/apprenants/fiches"
START, END = "<!-- AUTO:liens", "<!-- /AUTO:liens -->"

def phase_of(p):
    if p.startswith("01_warmup/") or "/suivi/warmup/" in p: return "Warm-Up"
    m = re.search(r"sprint-0(\d)", p)
    return f"Sprint {m.group(1)}" if m else "Transverse"

def docs():
    out = subprocess.check_output(["git", "-c", "core.quotepath=false", "ls-files", "-co", "--exclude-standard"], text=True).split("\n")
    keep = []
    for p in out:
        if not p.endswith(".md") or not os.path.exists(p): continue
        if re.match(r"^(01_warmup/rapports/audits|02_sprints/[^/]+/rapports/audits|05_promotion/suivi)/", p) and not p.endswith("README.md"):
            keep.append(p)
    return sorted(keep)

def label(p):
    b = os.path.basename(p)[:-3]
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", b)

CLASSE = 10  # un document qui cite au moins 10 apprenants est un document « de classe »

def build(fiche_path, text, corpus, classe=frozenset()):
    motifs = re.search(r"<!-- motifs: (.+?) -->", text)
    fichiers = re.search(r"<!-- fichiers: (.+?) -->", text)
    if not motifs: return text
    rx = re.compile(motifs.group(1))
    toks = [t.strip().lower() for t in fichiers.group(1).split(",")] if fichiers else []
    here = os.path.dirname(fiche_path)
    dedies, mentions = [], {}
    for p, content in corpus:
        name = os.path.basename(p).lower()
        if toks and any(t in name for t in toks):
            dedies.append(p)
        elif p not in classe and rx.search(content):
            mentions.setdefault(phase_of(p), []).append(p)
    lines = [START + " — généré par scripts/maj-fiches.py, ne pas éditer à la main -->", ""]
    lines.append("**Documents dédiés**" + ("" if dedies else " : aucun"))
    for p in dedies:
        lines.append(f"- [{label(p)}]({os.path.relpath(p, here)}) · {phase_of(p)}")
    lines.append("")
    lines.append("**Mentionné dans** (hors documents de classe, qui citent toute la promo : voir les `BILAN.md` et `rapports/audits/`)")
    for ph in ["Warm-Up", "Sprint 1", "Sprint 2", "Sprint 3", "Sprint 4", "Sprint 5", "Sprint 6", "Transverse"]:
        if ph in mentions:
            links = ", ".join(f"[{label(p)}]({os.path.relpath(p, here)})" for p in mentions[ph])
            lines.append(f"- {ph} : {links}")
    lines += ["", END]
    block = "\n".join(lines)
    if START in text and END in text:
        return re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block, text, flags=re.S)
    return text.rstrip() + "\n\n## Documents\n\n" + block + "\n"

def main():
    check = "--check" in sys.argv
    corpus = [(p, open(p, encoding="utf-8").read()) for p in docs()]
    fiches = [os.path.join(FICHES, f) for f in sorted(os.listdir(FICHES))] if os.path.isdir(FICHES) else []
    motifs = []
    for f in fiches:
        m = re.search(r"<!-- motifs: (.+?) -->", open(f, encoding="utf-8").read()) if f.endswith(".md") else None
        if m: motifs.append(re.compile(m.group(1)))
    classe = frozenset(p for p, c in corpus if sum(1 for rx in motifs if rx.search(c)) >= CLASSE)
    stale = []
    for f in sorted(os.listdir(FICHES)) if os.path.isdir(FICHES) else []:
        if not f.endswith(".md") or f == "README.md": continue
        path = os.path.join(FICHES, f)
        src = open(path, encoding="utf-8").read()
        out = build(path, src, corpus, classe)
        if out != src:
            stale.append(path)
            if not check:
                open(path, "w", encoding="utf-8").write(out)
    if check:
        for s in stale: print(f"fiche à régénérer : {s}")
        sys.exit(1 if stale else 0)
    print(f"{len(stale)} fiche(s) mise(s) à jour")

main()
