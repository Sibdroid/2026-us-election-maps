#!/usr/bin/env python3
"""Sum Jackson / Collins / total votes for Maine's ME-01 and ME-02.

data_ap.txt (tab-separated): name, Jackson, Collins, other, other, total, est. %
cd1.txt: one municipality per line; those are ME-01, everything else is ME-02.
"""
import sys

DATA_FILE = sys.argv[1] if len(sys.argv) > 1 else "data_ap.txt"
CD1_FILE = sys.argv[2] if len(sys.argv) > 2 else "cd1.txt"

# cd1.txt spelling -> data_ap.txt spelling
ALIASES = {"Saint George": "St. George"}


def num(s):
    s = s.strip().replace(",", "")
    return int(s) if s.isdigit() else 0


with open(CD1_FILE, encoding="utf-8") as f:
    cd1 = {ALIASES.get(line.strip(), line.strip()) for line in f if line.strip()}

totals = {
    "ME-01": {"jackson": 0, "collins": 0, "total": 0},
    "ME-02": {"jackson": 0, "collins": 0, "total": 0},
}
seen = set()

with open(DATA_FILE, encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line.strip():
            continue
        parts = line.split("\t")
        name = parts[0].strip()
        seen.add(name)
        district = "ME-01" if name in cd1 else "ME-02"
        totals[district]["jackson"] += num(parts[1])
        totals[district]["collins"] += num(parts[2])
        totals[district]["total"] += num(parts[5])

missing = cd1 - seen
if missing:
    print("WARNING: in cd1.txt but not found in data file:", sorted(missing), file=sys.stderr)

for district, t in totals.items():
    print(f"{district}: Jackson {t['jackson']:,} | Collins {t['collins']:,} | Total {t['total']:,}")
