#!/usr/bin/env python3
"""Déplace des fichiers ou dossiers du workspace ET met à jour tous les liens.

Usage :
  python3 scripts/move-doc.py <ancien> <nouveau>
  python3 scripts/move-doc.py --batch deplacements.tsv   # une ligne "ancien<TAB>nouveau"
  ajouter --dry-run pour voir sans rien modifier

Liens gérés dans les .md / .mdc :
  * chemins écrits depuis la racine (ex. `07_outputs/reports/x.md`) ;
  * liens Markdown relatifs [texte](../x.md), y compris depuis un fichier déplacé ;
  * chemins relatifs entre backticks (`../x.md`).
Les fichiers suivis par Git sont déplacés avec `git mv` (historique conservé).
"""
import os, re, subprocess, sys
from urllib.parse import unquote, quote

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
os.chdir(ROOT)

def norm(p):
    p = os.path.normpath(p.strip().rstrip("/"))
    return "" if p == "." else p

def load_moves(argv):
    if argv and argv[0] == "--batch":
        moves = []
        for line in open(argv[1], encoding="utf-8"):
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            a, b = line.split("\t")
            moves.append((norm(a), norm(b)))
        return moves
    if len(argv) != 2:
        sys.exit(__doc__)
    return [(norm(argv[0]), norm(argv[1]))]

def mapper(moves):
    ordered = sorted(moves, key=lambda m: -len(m[0]))
    def f(path):
        path = norm(path)
        for a, b in ordered:
            if path == a:
                return b
            if path.startswith(a + "/"):
                return b + path[len(a):]
        return path
    return f

LINK = re.compile(r"\]\(([^)\s]+)\)")
TICK = re.compile(r"`((?:\.\./)+[^`\s]+)`")

def rewrite(text, old_file, new_file, mp, root_moves):
    old_dir, new_dir = os.path.dirname(old_file), os.path.dirname(new_file)
    def repl(m):
        raw = m.group(1)
        if re.match(r"^[a-z]+:", raw) or raw.startswith("#") or raw.startswith("/"):
            return m.group(0)
        path, _, anchor = raw.partition("#")
        encoded = "%" in path
        target = norm(os.path.join(old_dir, unquote(path)))
        new_target = mp(target)
        if not os.path.exists(target) and new_target == target:
            return m.group(0)
        if new_target == target and old_dir == new_dir:
            return m.group(0)
        rel = os.path.relpath(new_target, new_dir or ".")
        if encoded or " " in rel:
            rel = quote(rel, safe="/-_.~")
        return "](" + rel + ("#" + anchor if anchor else "") + ")"
    text = LINK.sub(repl, text)
    def repl_tick(m):  # `../chemin/relatif` entre backticks
        raw = m.group(1)
        path, _, anchor = raw.partition("#")
        target = norm(os.path.join(old_dir, path))
        new_target = mp(target)
        if new_target == target and old_dir == new_dir:
            return m.group(0)
        if not os.path.exists(target) and new_target == target:
            return m.group(0)
        return "`" + os.path.relpath(new_target, new_dir or ".") + ("#" + anchor if anchor else "") + "`"
    text = TICK.sub(repl_tick, text)
    for a, b in root_moves:  # chemins écrits depuis la racine
        text = re.sub(r"(?<![\w./-])" + re.escape(a) + r"(?=[/`'\")\s,;:]|$)", b, text)
    return text

def tracked(path):
    return subprocess.run(["git", "ls-files", "--error-unmatch", path],
                          capture_output=True).returncode == 0 or \
           bool(subprocess.run(["git", "ls-files", path], capture_output=True, text=True).stdout.strip())

def main():
    argv = sys.argv[1:]
    dry = "--dry-run" in argv
    argv = [a for a in argv if a != "--dry-run"]
    moves = load_moves(argv)
    for a, b in moves:
        if not os.path.exists(a):
            sys.exit(f"introuvable : {a}")
    mp = mapper(moves)
    root_moves = sorted(moves, key=lambda m: -len(m[0]))
    docs = subprocess.check_output(["git", "ls-files", "-co", "--exclude-standard"], text=True).split("\n")
    docs = [d for d in docs if d.endswith((".md", ".mdc")) and os.path.exists(d)]
    changed = 0
    for d in docs:
        src = open(d, encoding="utf-8").read()
        out = rewrite(src, d, mp(d), mp, root_moves)
        if out != src:
            changed += 1
            if dry:
                print(f"liens : {d}")
            else:
                open(d, "w", encoding="utf-8").write(out)
    for a, b in moves:
        print(f"{a}  ->  {b}")
        if dry:
            continue
        os.makedirs(os.path.dirname(b) or ".", exist_ok=True)
        if tracked(a):
            subprocess.check_call(["git", "mv", "-k", a, b])
            if os.path.exists(a):  # fichiers non suivis restés sur place
                os.rename(a, b) if not os.path.exists(b) else None
        else:
            os.rename(a, b)
    print(f"{len(moves)} déplacement(s), {changed} fichier(s) aux liens mis à jour" + (" (simulation)" if dry else ""))

main()
