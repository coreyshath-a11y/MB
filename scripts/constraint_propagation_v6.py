#!/usr/bin/env python3
"""
Constraint propagation v6 - uses ALL confirmed + cascade + DELHI hypothesis.
Tries to find NEW unique fits by adding DELHI at 114A and tracing new constraints.
"""

print("=" * 70)
print("CONSTRAINT PROPAGATION v6")
print("All confirmed placements + CASCADE + DELHI + DAKAR")
print("=" * 70)

# Complete grid from CROSSWORD_GRID_DIGITIZED.md
# Format: (entry, row, col, direction, length)
entries_data = """
1A 0 0 A 7   1D 0 0 D 4   2D 0 1 D 4   3D 0 2 D 4   4D 0 3 D 5
5A 0 9 A 6   5D 0 5 D 7   6D 0 6 D 7   7A 0 17 A 8   7D 0 9 D 8
8D 0 10 D 8   9D 0 11 D 3   10D 0 12 D 8   11D 0 17 D 7   12D 0 18 D 6
13D 0 19 D 4   14D 0 20 D 3   15D 0 21 D 4   16D 0 22 D 3   17D 0 23 D 9
18D 0 24 D 9   19D 2 8 D 15   20A 1 0 A 7   21D 1 8 D 3   22A 1 9 A 6
23D 1 14 D 3   24D 1 16 D 6   25A 2 0 A 16   26D 2 17 D 6   27A 2 18 A 7
28A 3 0 A 4   28D 3 0 D 6   29D 3 5 D 9   30D 3 10 D 3   31A 3 11 A 3
32D 3 13 D 6   33D 3 15 D 9   34D 3 20 D 4   35A 3 21 A 4   36A 4 7 A 4
37D 4 10 D 5   38D 4 11 D 9   39A 4 12 A 9   40D 4 20 D 4   41A 4 21 A 4
42A 5 0 A 4   42D 5 0 D 4   43D 5 4 D 4   44A 5 5 A 3   45D 5 5 D 3
46D 5 11 D 6   47A 5 13 A 4   48D 5 13 D 8   49D 5 18 D 4   50A 6 0 A 16
51D 6 17 D 9   52A 6 18 A 7   53D 6 13 D 7   54A 7 0 A 7   54D 7 0 D 9
55D 7 4 D 8   56D 7 7 D 6   58A 7 8 A 4   59D 7 12 D 4   60A 7 13 A 4
61A 7 17 A 4   62D 7 17 D 6   63D 7 18 D 4   64A 7 22 A 3   64D 7 22 D 9
65D 8 3 D 9   66A 8 10 A 4   66D 8 10 D 6   67D 8 12 D 9   68A 8 14 A 2
69D 8 14 D 6   70A 8 18 A 4   70D 8 18 D 5   71D 8 21 D 6   72A 9 0 A 3
73A 9 11 A 14   74D 9 14 D 6   75D 9 15 D 5   76A 9 16 A 9   78D 9 24 D 15
79A 10 0 A 4   79D 10 0 D 4   80A 10 10 A 6   80D 10 10 D 6   81A 10 17 A 4
81D 10 17 D 8   82D 10 20 D 6   83A 10 22 A 3   84A 11 0 A 5   84D 11 0 D 3
85A 11 6 A 5   86D 11 8 D 3   87D 11 9 D 5   88A 11 12 A 5   89D 11 12 D 3
90A 11 18 A 3   90D 11 18 D 7   91A 11 22 A 3   91D 11 22 D 6   92A 12 0 A 6
92D 12 0 D 4   93D 12 6 D 4   94A 12 7 A 11   95D 12 11 D 7   96D 12 17 D 5
97A 12 18 A 7   98A 13 0 A 4   99A 13 4 A 3   99D 13 4 D 4   100D 13 7 D 4
101D 13 14 D 4   102A 13 8 A 5   103A 13 14 A 5   104D 13 18 D 7   105A 13 20 A 5
106A 14 0 A 4   106D 14 0 D 4   107D 14 3 D 5   108D 14 4 D 4   109A 14 9 A 6
110D 14 13 D 6   111A 14 17 A 3   112D 14 17 D 6   113D 14 20 D 5   114A 15 0 A 14
115D 15 3 D 5   116D 15 8 D 3   117A 15 16 A 6   118D 15 16 D 8   119A 16 0 A 4
119D 16 0 D 3   120A 16 5 A 4   121A 16 11 A 4   122D 16 14 D 7   123A 16 16 A 5
124D 16 16 D 9   125D 16 17 D 9   126D 16 18 D 9   127A 17 1 A 6   128D 17 3 D 4
129A 17 8 A 4   130D 17 10 D 6   131D 17 12 D 4   132D 17 14 D 3   133D 17 15 D 8
134A 17 19 A 6   135D 17 21 D 8   136A 18 0 A 2   137D 18 7 D 7   138A 18 9 A 16
139D 18 13 D 7   140D 18 15 D 5   141D 19 0 D 6   142D 19 1 D 6   143A 19 2 A 4
143D 19 2 D 5   144D 19 5 D 3   145A 19 6 A 5   146A 19 11 A 3   147D 19 11 D 5
148D 19 14 D 4   149A 20 4 A 9   150D 20 4 D 5   151D 20 6 D 5   152D 20 8 D 5
153A 20 14 A 4   154D 20 14 D 4   155D 20 18 D 5   156A 21 0 A 4   156D 21 0 D 4
157D 21 3 D 4   158A 21 5 A 5   158D 21 5 D 4   159D 21 6 D 4   160D 21 9 D 4
161A 21 11 A 3   162D 21 13 D 4   163D 21 14 D 4   164A 21 15 A 5   165A 22 0 A 8
166D 22 8 D 3   167A 22 9 A 16   168D 22 9 D 3   169D 22 10 D 3   170D 22 11 D 3
171A 23 0 A 8   172D 23 9 D 2   173D 23 15 D 2   174A 24 0 A 8   175A 24 10 A 6
176A 24 17 A 8
"""

# Parse entries
entries = {}
for line in entries_data.strip().split('\n'):
    for part in line.split():
        part = part.strip()
        if not part:
            continue
    # Need to parse the line differently
    parts = line.strip().split()
    i = 0
    while i < len(parts):
        if i + 4 < len(parts):
            name = parts[i]
            row = int(parts[i+1])
            col = int(parts[i+2])
            dirn = parts[i+3]
            length = int(parts[i+4])
            entries[name] = {"row": row, "col": col, "dir": dirn, "len": length}
            i += 5
        else:
            break

# Confirmed placements (all high confidence + cascade HIGH + DELHI)
placements = {
    "36A": "DORA",
    "37D": "ABASH",
    "53D": "ROTUNDA",
    "58A": "PUSH",
    "66A": "HAFT",
    "86D": "ZIP",
    "87D": "TRITE",
    "88A": "ADORN",
    "94A": "CIRCLEABOUT",
    "96D": "TONER",
    "102A": "PINTO",
    "103A": "ACHOO",
    "109A": "TOLEDO",
    "110D": "DENVER",
    "117A": "REGINA",
    "121A": "TONI",
    "123A": "ERASE",
    "167A": "SUPERBOWLSTADIUM",
    "149A": "BEASTLAND",
    # Cascade HIGH confidence
    "133D": "HULAHOOP",
    "153A": "RACE",
    # Cascade MEDIUM
    "151D": "ACCRA",
    "174A": "TEAMSEAS",
    # Hypothetical
    "104D": "ORGANIC",
    "111A": "NRA",
}

# Build letter grid
grid = {}  # (row, col) -> letter
for name, answer in placements.items():
    if name not in entries:
        continue
    e = entries[name]
    for i, ch in enumerate(answer):
        if e["dir"] == "A":
            r, c = e["row"], e["col"] + i
        else:
            r, c = e["row"] + i, e["col"]
        if (r, c) in grid and grid[(r, c)] != ch:
            print(f"  CONFLICT at ({r},{c}): {grid[(r,c)]} vs {ch} from {name}[{i}]")
        grid[(r, c)] = ch

# DELHI hypothesis: add at 114A pos 8-12
# 114A at (15, 0) len 14 across, DELHI at positions 8-12
delhi = "DELHI"
for i, ch in enumerate(delhi):
    pos = 8 + i
    r, c = 15, 0 + pos  # 114A is across starting at col 0
    if (r, c) in grid:
        if grid[(r, c)] != ch:
            print(f"  DELHI CONFLICT at ({r},{c}): {grid[(r,c)]} vs {ch}")
        else:
            print(f"  DELHI confirms ({r},{c}) = {ch}")
    else:
        grid[(r, c)] = ch
        print(f"  DELHI places ({r},{c}) = {ch}")

# DAKAR at 50A pos 9-13
# 50A at (6, 0) len 16 across
dakar = "DAKAR"
for i, ch in enumerate(dakar):
    pos = 9 + i
    r, c = 6, 0 + pos
    if (r, c) in grid:
        if grid[(r, c)] != ch:
            print(f"  DAKAR CONFLICT at ({r},{c}): {grid[(r,c)]} vs {ch}")
        else:
            print(f"  DAKAR confirms ({r},{c}) = {ch}")
    else:
        grid[(r, c)] = ch
        print(f"  DAKAR places ({r},{c}) = {ch}")

print(f"\nTotal cells filled: {len(grid)}")

# Now extract patterns for ALL unfilled entries
print(f"\n{'='*70}")
print("ENTRY PATTERNS (with 3+ known letters)")
print(f"{'='*70}")

# Read answer bank
import subprocess

# Get all confirmed answers
all_answers = set()
answer_lines = """EVERY CHALLENGE LEADS TOWARDS LOCATION NAME SOMEWHERE AROUND WORLD
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
ACCRA GHANA""".strip()

for line in answer_lines.split('\n'):
    for word in line.split():
        all_answers.add(word)

# Check each unfilled entry
interesting = []
for name, e in sorted(entries.items()):
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

    if name in placements:
        continue  # Skip already placed

    pat_str = ''.join(pattern)
    if known_count >= 2:
        # Check which answers fit
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

        if known_count >= 3 or len(fits) <= 3:
            interesting.append((name, e["len"], pat_str, known_count, fits))
            status = "UNIQUE!" if len(fits) == 1 else f"{len(fits)} fits"
            print(f"  {name} (len {e['len']}): {pat_str} ({known_count} known) → {status}: {fits[:5]}")

# Show unique fits
print(f"\n{'='*70}")
print("UNIQUE FITS (only 1 answer matches)")
print(f"{'='*70}")

new_placements = {}
for name, length, pat, known, fits in interesting:
    if len(fits) == 1:
        answer = fits[0]
        print(f"  {name} = {answer} (pattern: {pat})")
        new_placements[name] = answer

# Trace cascading from new placements
if new_placements:
    print(f"\n{'='*70}")
    print("CASCADING FROM NEW UNIQUE FITS")
    print(f"{'='*70}")

    for name, answer in new_placements.items():
        e = entries[name]
        print(f"\n  {name} = {answer}:")
        for i, ch in enumerate(answer):
            if e["dir"] == "A":
                r, c = e["row"], e["col"] + i
            else:
                r, c = e["row"] + i, e["col"]

            if (r, c) not in grid:
                grid[(r, c)] = ch
                # Find crossing entries
                for other_name, other_e in entries.items():
                    if other_name == name:
                        continue
                    for j in range(other_e["len"]):
                        if other_e["dir"] == "A":
                            or_r, or_c = other_e["row"], other_e["col"] + j
                        else:
                            or_r, or_c = other_e["row"] + j, other_e["col"]
                        if (or_r, or_c) == (r, c):
                            print(f"    ({r},{c})={ch} → {other_name}[{j}] = {ch}")

# Zero fits analysis
print(f"\n{'='*70}")
print("ZERO FITS (no answer in bank matches pattern)")
print(f"{'='*70}")
for name, length, pat, known, fits in interesting:
    if len(fits) == 0 and known >= 3:
        print(f"  {name} (len {length}): {pat} ({known} known) → ZERO FITS")

# Check what DAKAR + DELHI give us at specific entries
print(f"\n{'='*70}")
print("NEW CONSTRAINTS FROM DAKAR (50A pos 9-13) + DELHI (114A pos 8-12)")
print(f"{'='*70}")

# 50A: DAKAR at pos 9-13 means cols 9-13 of row 6 = D,A,K,A,R
# Down entries crossing at these positions:
dakar_crosses = {
    "7D": (6, 9, 6),    # 7D at (0,9) down, row 6 = pos 6
    "8D": (6, 10, 6),   # 8D at (0,10) down, row 6 = pos 6
    # Actually need to check which down entries cross
}

print("\n  DAKAR crosses (col 9-13, row 6):")
for col in range(9, 14):
    letter = dakar[col - 9]
    # Find which down entry crosses at (6, col)
    for dname, de in entries.items():
        if de["dir"] != "D":
            continue
        if de["col"] != col:
            continue
        if de["row"] <= 6 <= de["row"] + de["len"] - 1:
            pos_in_down = 6 - de["row"]
            print(f"    ({6},{col})={letter} → {dname}[{pos_in_down}]")

print("\n  DELHI crosses (col 8-12, row 15):")
for col in range(8, 13):
    letter = delhi[col - 8]
    for dname, de in entries.items():
        if de["dir"] != "D":
            continue
        if de["col"] != col:
            continue
        if de["row"] <= 15 <= de["row"] + de["len"] - 1:
            pos_in_down = 15 - de["row"]
            existing = grid.get((15, col))
            new = "NEW" if existing is None or existing != letter else "confirmed"
            print(f"    ({15},{col})={letter} → {dname}[{pos_in_down}] ({new})")

# Update grid visualization
print(f"\n{'='*70}")
print("UPDATED GRID (with DELHI + DAKAR)")
print(f"{'='*70}")
for row in range(25):
    line = f"R{row:2d} |"
    for col in range(25):
        if (row, col) in grid:
            line += grid[(row, col)]
        else:
            # Check if black cell
            line += '.'
    line += '|'
    print(line)
