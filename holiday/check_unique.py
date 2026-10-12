"""Fail if any holiday subject, preview text or headline repeats a Thanksgiving one.

    python3 holiday/check_unique.py

Thanksgiving copy: subject/preview tables in HANDOFF.md + headlines in templates/*.html.
Holiday copy: subject/preview table in holiday/PLAN.md + headlines in templates/holiday/*.html.
Compared case- and punctuation-blind. Tro, 2026-10-12: they must never share a subject line.
"""
import glob, html, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def norm(t):
    t = html.unescape(re.sub(r"<[^>]+>", " ", t)).replace("’", "'")
    return re.sub(r"[^a-z0-9$ ]", "", re.sub(r"\s+", " ", t.lower())).strip()

def table_copy(path, subj_col, prev_col):
    out = []
    for line in open(os.path.join(ROOT, path), encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) > max(subj_col, prev_col) and not set(cells[0]) <= set("-") and cells[0] not in ("#", "Email", "Send"):
            out += [("subject", cells[subj_col]), ("preview", cells[prev_col])]
    for m in re.finditer(r'subject "([^"]+)"', open(os.path.join(ROOT, path), encoding="utf-8").read()):
        out.append(("subject", m.group(1)))
    return out

def template_copy(pattern):
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, pattern))):
        s = open(f, encoding="utf-8").read()
        out += [("headline " + os.path.basename(f), h) for h in re.findall(r"<h1[^>]*>(.*?)</h1>", s, re.S)]
        out += [("eyebrow " + os.path.basename(f), h) for h in re.findall(r"letter-spacing:[34]px;text-transform:uppercase[^>]*>(.*?)</p>", s, re.S)]
    return out

handoff = open(os.path.join(ROOT, "HANDOFF.md"), encoding="utf-8").read()
tg_section = handoff.split("## Holiday 2026")[0]
tmp = os.path.join(ROOT, ".tg_tables.tmp")
open(tmp, "w", encoding="utf-8").write(tg_section)
try:
    tg = table_copy(".tg_tables.tmp", 2, 3) + template_copy("templates/*.html")
finally:
    os.remove(tmp)
plan = open(os.path.join(ROOT, "holiday/PLAN.md"), encoding="utf-8").read()
subj_part = plan.split("## Subject lines and preview text")[1]
tmp = os.path.join(ROOT, ".hol_tables.tmp")
open(tmp, "w", encoding="utf-8").write(subj_part)
try:
    hol = table_copy(".hol_tables.tmp", 1, 2) + template_copy("templates/holiday/*.html")
finally:
    os.remove(tmp)

seen = {}
for kind, t in tg:
    if norm(t):
        seen.setdefault(norm(t), (kind, t))
clashes = [(k, t, seen[norm(t)]) for k, t in hol if norm(t) in seen]
for k, t, (tk, tt) in clashes:
    print(f"REPEAT  holiday {k}: {norm(t)!r}  ==  thanksgiving {tk}")
print(f"{len(hol)} holiday lines checked against {len(tg)} Thanksgiving lines: {len(clashes)} repeats")
sys.exit(1 if clashes else 0)
