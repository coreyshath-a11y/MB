#!/usr/bin/env python3
"""
Parse entry positions from CROSSWORD_GRID_DIGITIZED.md to build accurate entry data.
This replaces the error-prone hand-coded entry data.
"""

import re

# Read the grid file
with open('/home/user/MB/analysis/CROSSWORD_GRID_DIGITIZED.md') as f:
    content = f.read()

# Parse ACROSS entries
across_entries = {}
in_across = False
in_down = False
for line in content.split('\n'):
    if '## ACROSS ENTRIES' in line:
        in_across = True
        in_down = False
        continue
    if '## DOWN ENTRIES' in line:
        in_across = False
        in_down = True
        continue
    if in_across or in_down:
        m = re.match(r'\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|', line)
        if m:
            num = int(m.group(1))
            row = int(m.group(2))
            col = int(m.group(3))
            length = int(m.group(4))
            direction = 'A' if in_across else 'D'
            key = f"{num}{direction}"
            if in_across:
                across_entries[key] = {"row": row, "col": col, "len": length, "dir": "A"}
            else:
                across_entries[key] = {"row": row, "col": col, "len": length, "dir": "D"}

entries = across_entries

print(f"Parsed {len(entries)} entries ({sum(1 for k in entries if k.endswith('A'))} across, "
      f"{sum(1 for k in entries if k.endswith('D'))} down)")

# Confirmed placements
placements = {
    "36A": "DORA", "37D": "ABASH", "53D": "ROTUNDA", "58A": "PUSH",
    "66A": "HAFT", "86D": "ZIP", "87D": "TRITE", "88A": "ADORN",
    "94A": "CIRCLEABOUT", "96D": "TONER", "102A": "PINTO", "103A": "ACHOO",
    "109A": "TOLEDO", "110D": "DENVER", "117A": "REGINA", "121A": "TONI",
    "123A": "ERASE", "167A": "SUPERBOWLSTADIUM", "149A": "BEASTLAND",
    "133D": "HULAHOOP", "153A": "RACE", "151D": "ACCRA", "174A": "TEAMSEAS",
    "104D": "ORGANIC", "111A": "NRA",
}

# Build grid
grid = {}
for name, answer in placements.items():
    if name not in entries:
        print(f"WARNING: {name} not found in parsed entries!")
        continue
    e = entries[name]
    for i, ch in enumerate(answer):
        if e["dir"] == "A":
            r, c = e["row"], e["col"] + i
        else:
            r, c = e["row"] + i, e["col"]
        if (r, c) in grid and grid[(r, c)] != ch:
            print(f"CONFLICT at ({r},{c}): {grid[(r,c)]} vs {ch} from {name}[{i}]")
        grid[(r, c)] = ch

# Add DELHI at 114A pos 8-12
e114 = entries["114A"]
for i, ch in enumerate("DELHI"):
    r, c = e114["row"], e114["col"] + 8 + i
    if (r, c) in grid and grid[(r, c)] != ch:
        print(f"DELHI CONFLICT at ({r},{c}): {grid[(r,c)]} vs {ch}")
    else:
        grid[(r, c)] = ch

# Add DAKAR at 50A pos 9-13
e50 = entries["50A"]
for i, ch in enumerate("DAKAR"):
    r, c = e50["row"], e50["col"] + 9 + i
    if (r, c) in grid and grid[(r, c)] != ch:
        print(f"DAKAR CONFLICT at ({r},{c}): {grid[(r,c)]} vs {ch}")
    else:
        grid[(r, c)] = ch

print(f"\nTotal cells filled: {len(grid)}")

# Answer bank
all_answers = set()
answer_text = """EVERY CHALLENGE LEADS TOWARDS LOCATION NAME SOMEWHERE AROUND WORLD
DORA ABASH ROTUNDA PUSH HAFT ZIP TRITE ADORN CIRCLEABOUT TONER PINTO ACHOO TOLEDO DENVER REGINA TONI ERASE
HULAHOOP RACE ACCRA TEAMSEAS ORGANIC NRA
SUPERBOWLSTADIUM BEASTLAND
RA EAR ION NOTE LECAR ECLAIR CALIBER CARBLITE CABRIOLET ORBICULATE TURNONADIME
ER RACE TONI ADORN AROUND ROTUNDA DURATION INUNDATOR TRADEUNION CIRCLEABOUT
OI PINTO OPTION PORTION POSITRON RATPOISON STAINPROOF OUTFORASPIN
NO NOTE EON TONER ORIENT INUTERO ROUTINES OUTLINERS RESOLUTION REVOLUTIONS
ACHOO REDO CELLO HULAHOOP BANJO SKYSCRAPER TIPTOE HOODIE IGLOO BAGUETTE MUSTERS LOLLIPOP LATTE
INTRODUCTIONS CONTRADICTION
DOMAIN CASHTENT
ROSWELL WICHITA DURHAM PUEBLO TOLEDO DENVER ANCHORAGE SACRAMENTO WILMINGTON SPRINGFIELD
TULSA RENO REGINA MACON SITKA BOISE ALBANY BUFFALO LINCOLN PROVO TACOMA
ERASE ADORN TRITE HAFT ABASH LEADS ACHOO PINTO PUSH EVERY DORA TONER RACE ZIP
ACCRA GHANA"""
for line in answer_text.strip().split('\n'):
    for word in line.split():
        all_answers.add(word)

# Extract patterns for all entries
print(f"\n{'='*70}")
print("CORRECTLY PARSED ENTRY PATTERNS")
print(f"{'='*70}")

unique_fits = []
zero_fits = []
multi_fits = []

for name in sorted(entries.keys(), key=lambda x: (int(x[:-1]), x[-1])):
    if name in placements:
        continue  # Skip placed entries

    e = entries[name]
    pattern = []
    known_count = 0
    for i in range(e["len"]):
        if e["dir"] == "A":
            r, c = e["row"], e["col"] + i
        else:
            r, c = e["row"] + i, e["col"]
        if (r, c) in grid:
            pattern.append(grid[(r, c)])
            known_count += 1
        else:
            pattern.append('?')

    pat_str = ''.join(pattern)

    if known_count >= 2:
        fits = []
        for answer in all_answers:
            if len(answer) == e["len"]:
                match = True
                for i, ch in enumerate(pat_str):
                    if ch != '?' and ch != answer[i]:
                        match = False
                        break
                if match:
                    fits.append(answer)

        if len(fits) == 1:
            unique_fits.append((name, e["len"], pat_str, known_count, fits[0]))
        elif len(fits) == 0 and known_count >= 3:
            zero_fits.append((name, e["len"], pat_str, known_count))
        elif len(fits) <= 5 and known_count >= 2:
            multi_fits.append((name, e["len"], pat_str, known_count, fits))

print(f"\n--- UNIQUE FITS ---")
for name, length, pat, known, answer in unique_fits:
    print(f"  {name} (len {length}): {pat} → {answer}")

print(f"\n--- ZERO FITS (3+ known, no bank answer matches) ---")
for name, length, pat, known in zero_fits:
    print(f"  {name} (len {length}): {pat} ({known} known)")

print(f"\n--- FEW FITS (2-5 matches) ---")
for name, length, pat, known, fits in multi_fits:
    print(f"  {name} (len {length}): {pat} → {fits}")

# Now check the specific entries we were worried about
print(f"\n{'='*70}")
print("VERIFICATION: Key entries")
print(f"{'='*70}")

for check in ["140D", "133D", "145A", "146A", "141D", "142D", "137D"]:
    if check in entries:
        e = entries[check]
        pattern = []
        for i in range(e["len"]):
            if e["dir"] == "A":
                r, c = e["row"], e["col"] + i
            else:
                r, c = e["row"] + i, e["col"]
            pattern.append(grid.get((r, c), '?'))
        print(f"  {check} at ({e['row']},{e['col']}) len {e['len']}: {''.join(pattern)}")

# Print grid
print(f"\n{'='*70}")
print("GRID VISUALIZATION")
print(f"{'='*70}")

# Parse black cells
black_cells = set()
grid_map_section = False
for line in content.split('\n'):
    if 'R 0 |' in line and not grid_map_section:
        grid_map_section = True
    if grid_map_section and line.startswith('R'):
        m = re.match(r'R\s*(\d+)\s*\|(.+)\|', line)
        if m:
            row = int(m.group(1))
            chars = m.group(2)
            for col, ch in enumerate(chars):
                if ch == '#':
                    black_cells.add((row, col))
            if row == 24:
                grid_map_section = False

for row in range(25):
    line = f"R{row:2d} |"
    for col in range(25):
        if (row, col) in grid:
            line += grid[(row, col)]
        elif (row, col) in black_cells:
            line += '#'
        else:
            line += '.'
    line += '|'
    print(line)

# Check circled cells
print(f"\n{'='*70}")
print("CIRCLED CELL VALUES")
print(f"{'='*70}")

circled = [
    (0, 12), (2, 4), (3, 8), (3, 24), (4, 19), (10, 12),
    (11, 2), (11, 22), (13, 0), (18, 7), (19, 17), (20, 2),
    (22, 11), (22, 18), (22, 24), (24, 20),
]

code = []
for i, (r, c) in enumerate(circled):
    letter = grid.get((r, c), '?')
    code.append(letter)
    print(f"  Cell {i+1}: ({r},{c}) = {letter}")

print(f"\n  Final code: {''.join(code)}")
