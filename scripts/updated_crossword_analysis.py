#!/usr/bin/env python3
"""
Updated crossword analysis with:
1. All new clues from the Feb 14 crossword update (Hint #6 era)
2. EYJAFJALLAJOKULL as the 16-circled-cell extraction
3. Full constraint propagation with new data
"""

# ===== NEW CLUES from updated crossword (Feb 14, 2026) =====
# Format: entry_number: "clue text"

NEW_CLUES_ACROSS = {
    8:   "Players on T-Swift's 'Mean'",
    24:  "One collapsed in 1980 in Washington",
    30:  "Words heard in Shibuya",
    35:  "Support that's also shaped like an H",
    42:  "Mia in the 'Fifty Shades' series",
    48:  "Cosmetics shop purchase",
    58:  '"___ Ninja" YouTube series',
    64:  "Start of a Supremes song or end of a Christmas song",
    72:  "Tatum franchise",
    80:  "Teammate of Vini and Jude",
    85:  "Guitarist Harrison",
    92:  "Leave quickly",
    100: "Smartphone powerer",
    106: "The Cavaliers",
    113: "Anthony's result vs. Jake",
    120: "One of two women named in Spinderella's trio",
    127: "Sounds in the night",
    136: "Alpine municipality",
    145: "Jungler Moon Hyeon-jun",
    149: "Theatricality",
    158: "Not one's best effort",
    165: "Amount for Team Trees, Team Seas, or Team Water",
    167: "What this puzzle commemorates in eleven hidden words in the theme entries",
    173: "One that hangs out at the swimming hole",
}

NEW_CLUES_DOWN = {
    1:   "Dry comment",
    5:   "T.I. flick",
    9:   "Bring Me the Horizon release",
    14:  "Perry and kin",
    18:  "Driver who won awards for his Ferrari",
    23:  "Some sports league contracts, for short",
    37:  "Takes a hot bath",
    44:  "Was a little too close",
    52:  "Japanese streamer, perhaps",
    60:  "___-12 (conference with two members in 2025)",
    69:  "One who preferred $10,000 sushi to $10 sushi",
    75:  "Host of the Christmas 'Holiday Halftime Party'",
    80:  "Words before doubling a piece",
    87:  "One end of the pencil scale",
    96:  "John B is one",
    108: "Motor oil brand",
    116: "School where they also say 95-Down",
    124: "File productions",
    130: "Some cords",
    137: "Cotton weave",
    142: "Largest European lake",
    152: "Prepare mushrooms",
    162: "Easy as falling off ___",
    169: "NW-based retailer",
}

print("=" * 70)
print("ALL NEW CLUES FROM FEB 14 CROSSWORD UPDATE")
print("=" * 70)
print(f"\nACROSS clues: {len(NEW_CLUES_ACROSS)}")
for num, clue in sorted(NEW_CLUES_ACROSS.items()):
    print(f"  {num:>3}A: {clue}")
print(f"\nDOWN clues: {len(NEW_CLUES_DOWN)}")
for num, clue in sorted(NEW_CLUES_DOWN.items()):
    print(f"  {num:>3}D: {clue}")
print(f"\nTotal new clues: {len(NEW_CLUES_ACROSS) + len(NEW_CLUES_DOWN)}")

# ===== EYJAFJALLAJOKULL extraction verification =====
print("\n" + "=" * 70)
print("EYJAFJALLAJOKULL EXTRACTION VERIFICATION")
print("=" * 70)

extraction = "EYJAFJALLAJOKULL"  # 16 letters (O for ö)
circled_cells = [
    (0, 12),   # Cell 1
    (2, 4),    # Cell 2
    (3, 8),    # Cell 3
    (3, 24),   # Cell 4
    (4, 19),   # Cell 5
    (10, 12),  # Cell 6
    (11, 2),   # Cell 7
    (11, 22),  # Cell 8
    (13, 0),   # Cell 9
    (18, 7),   # Cell 10
    (19, 17),  # Cell 11
    (20, 2),   # Cell 12
    (22, 11),  # Cell 13
    (22, 18),  # Cell 14
    (22, 24),  # Cell 15
    (24, 20),  # Cell 16
]

import re

# Parse entries from grid file
with open('/home/user/MB/analysis/CROSSWORD_GRID_DIGITIZED.md') as f:
    content = f.read()

entries = {}
in_across = False
in_down = False
for line in content.split('\n'):
    if '## ACROSS ENTRIES' in line:
        in_across = True; in_down = False; continue
    if '## DOWN ENTRIES' in line:
        in_across = False; in_down = True; continue
    if '## Entry Length' in line:
        in_down = False; continue
    if in_across or in_down:
        m = re.match(r'\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|', line)
        if m:
            num = int(m.group(1)); row = int(m.group(2)); col = int(m.group(3)); length = int(m.group(4))
            direction = 'A' if in_across else 'D'
            entries[f"{num}{direction}"] = {"row": row, "col": col, "len": length, "dir": direction}

# Map each circled cell to its letter and the entries it belongs to
print("\nCircled cell → Letter → Entry constraints:")
new_constraints = {}
for i, ((r, c), letter) in enumerate(zip(circled_cells, extraction)):
    crossing = []
    for ename, edata in entries.items():
        if edata["dir"] == "A":
            if edata["row"] == r and edata["col"] <= c < edata["col"] + edata["len"]:
                pos = c - edata["col"]
                crossing.append((ename, pos))
        else:
            if edata["col"] == c and edata["row"] <= r < edata["row"] + edata["len"]:
                pos = r - edata["row"]
                crossing.append((ename, pos))

    cross_strs = []
    for ename, pos in crossing:
        cross_strs.append(f"{ename}[{pos}]={letter}")
        if ename not in new_constraints:
            new_constraints[ename] = {}
        new_constraints[ename][pos] = letter

    print(f"  Cell {i+1:2d}: ({r:2d},{c:2d}) = {letter}  →  {', '.join(cross_strs)}")

# ===== Old placements vs new extraction =====
print("\n" + "=" * 70)
print("CONFLICT CHECK: Old SUPERBOWLSTADIUM vs EYJAFJALLAJOKULL")
print("=" * 70)

old_167A = "SUPERBOWLSTADIUM"
new_167A_constraints = new_constraints.get("167A", {})
print(f"\n167A old answer: {old_167A}")
print(f"167A new constraints from extraction: {new_167A_constraints}")
for pos, letter in new_167A_constraints.items():
    old_letter = old_167A[pos] if pos < len(old_167A) else "?"
    match = "MATCH" if old_letter == letter else "CONFLICT!"
    print(f"  Position {pos}: old={old_letter}, new={letter} → {match}")

# ===== Build constraint grid with EYJAFJALLAJOKULL =====
print("\n" + "=" * 70)
print("UPDATED CONSTRAINT GRID (with EYJAFJALLAJOKULL)")
print("=" * 70)

# Known placements (REMOVING SUPERBOWLSTADIUM since it conflicts)
placements = {
    "36A": "DORA", "37D": "ABASH", "53D": "ROTUNDA",
    "66A": "HAFT", "86D": "ZIP", "87D": "TRITE", "88A": "ADORN",
    "94A": "CIRCLEABOUT", "96D": "TONER", "102A": "PINTO", "103A": "ACHOO",
    "109A": "TOLEDO", "110D": "DENVER", "117A": "REGINA", "121A": "TONI",
    "123A": "ERASE",
    # Cascade (keeping high confidence ones but NOT 167A)
    "133D": "HULAHOOP", "153A": "RACE",
}
# Note: REMOVED 167A=SUPERBOWLSTADIUM, 149A=BEASTLAND, 151D=ACCRA,
# 174A=TEAMSEAS, 104D=ORGANIC, 111A=NRA since they cascaded from 167A

grid = {}
for name, answer in placements.items():
    if name not in entries:
        continue
    e = entries[name]
    for i, ch in enumerate(answer):
        if e["dir"] == "A":
            r, c = e["row"], e["col"] + i
        else:
            r, c = e["row"] + i, e["col"]
        grid[(r, c)] = ch

# Add EYJAFJALLAJOKULL constraints
for (r, c), letter in zip(circled_cells, extraction):
    if (r, c) in grid and grid[(r, c)] != letter:
        print(f"  CONFLICT at ({r},{c}): grid has {grid[(r,c)]}, extraction says {letter}")
    grid[(r, c)] = letter

# Add DELHI at 114A pos 8-12
e114 = entries["114A"]
for i, ch in enumerate("DELHI"):
    r, c = e114["row"], e114["col"] + 8 + i
    if (r, c) in grid and grid[(r, c)] != ch:
        print(f"  DELHI CONFLICT at ({r},{c})")
    else:
        grid[(r, c)] = ch

# Add DAKAR at 50A pos 9-13
e50 = entries["50A"]
for i, ch in enumerate("DAKAR"):
    r, c = e50["row"], e50["col"] + 9 + i
    if (r, c) in grid and grid[(r, c)] != ch:
        print(f"  DAKAR CONFLICT at ({r},{c})")
    else:
        grid[(r, c)] = ch

print(f"\nTotal known cells: {len(grid)}")

# ===== Now solve clues with constraints =====
print("\n" + "=" * 70)
print("CLUE SOLVING WITH CONSTRAINTS")
print("=" * 70)

# For each clue, show the pattern from constraints
all_clues = {}
for num, clue in NEW_CLUES_ACROSS.items():
    key = f"{num}A"
    if key in entries:
        all_clues[key] = clue
for num, clue in NEW_CLUES_DOWN.items():
    key = f"{num}D"
    if key in entries:
        all_clues[key] = clue

for name in sorted(all_clues.keys(), key=lambda x: (int(x[:-1]), x[-1])):
    e = entries[name]
    pattern = []
    for i in range(e["len"]):
        if e["dir"] == "A":
            r, c = e["row"], e["col"] + i
        else:
            r, c = e["row"] + i, e["col"]
        pattern.append(grid.get((r, c), '?'))
    pat_str = ''.join(pattern)
    known = sum(1 for c in pat_str if c != '?')
    clue = all_clues[name]
    print(f"\n  {name:6s} (len {e['len']:2d}): {pat_str}  [{known}/{e['len']} known]")
    print(f"         Clue: {clue}")

    # Attempt to solve some clues
    answer = None

    if name == "24A":
        answer = "STHELENS"
        print(f"         >>> ANSWER: {answer} (Mount St. Helens collapsed 1980 in Washington state)")
    elif name == "35A":
        answer = "GOAL" if e["len"] == 4 else None
        if answer:
            print(f"         >>> ANSWER: {answer} (goalpost is H-shaped)")
    elif name == "42A":
        answer = "GREY" if e["len"] == 4 else None
        if answer:
            print(f"         >>> ANSWER: {answer} (Mia Grey in Fifty Shades)")
    elif name == "85A":
        answer = "GEORGE" if e["len"] == 5 else None
        if e["len"] == 5:
            print(f"         >>> CANDIDATE: GEORGE (Harrison, guitarist of The Beatles)")
    elif name == "92A":
        # Leave quickly, 6 letters
        if e["len"] == 6:
            print(f"         >>> CANDIDATES: DEPART, SCURRY, HUSTLE, BOUNCE, HASTEN, DECAMP")
    elif name == "100A":
        # Smartphone powerer
        if e["len"] == 3:
            print(f"         >>> CANDIDATES: APP (powers smartphone features)")
        elif e["len"] == 7:
            print(f"         >>> CANDIDATES: BATTERY, CHARGER")
    elif name == "106A":
        # The Cavaliers (team from Cleveland)
        if e["len"] == 3:
            print(f"         >>> CANDIDATES: NBA, CLE, CAV")
        elif e["len"] == 4:
            print(f"         >>> CANDIDATES: CAVS, OHIO")
    elif name == "113A":
        # Anthony's result vs. Jake
        print(f"         >>> CANDIDATES: Could be boxing match result (Anthony Joshua vs Jake Paul?)")
    elif name == "136A":
        # Alpine municipality, 6 letters, pos 5 = A (from extraction)
        if e["len"] == 6:
            print(f"         >>> Pattern: ?????A → Alpine municipality. CANDIDATES: DAVOSA?")
    elif name == "142D":
        # Largest European lake
        if e["len"] == 6:
            print(f"         >>> ANSWER: LADOGA (Lake Ladoga in Russia, largest European lake)")
    elif name == "149A":
        # Theatricality
        print(f"         >>> CANDIDATES: DRAMA, HISTRIONICS, MELODRAMA")
    elif name == "152D":
        # Prepare mushrooms, 5 letters
        if e["len"] == 5:
            print(f"         >>> CANDIDATES: SAUTE, SLICE, MINCE, CLEAN")
    elif name == "162D":
        # Easy as falling off ___
        if e["len"] == 4:
            print(f"         >>> ANSWER: ALOG (Easy as falling off a log)")
    elif name == "165A":
        # Amount for Team Trees, Team Seas, or Team Water
        if e["len"] == 8:
            print(f"         >>> CANDIDATES: TWENTYMILL? No... Each had different amounts")
            print(f"             Team Trees: $20M, Team Seas: $30M, Team Water: $?M")
    elif name == "169D":
        # NW-based retailer
        if e["len"] == 3:
            print(f"         >>> ANSWER: REI (NW-based outdoor retailer, HQ in Kent, WA)")
    elif name == "1D":
        # Dry comment
        print(f"         >>> CANDIDATES: WIT? QUIP? WISECRACK? BARB?")
    elif name == "5D":
        # T.I. flick, 3 letters, pos 2 = Y
        if e["len"] == 3:
            print(f"         >>> Pattern: ??Y → T.I. movie. CANDIDATES: ATL(no)... T.I. was in 'ATL'(2006)")
    elif name == "9D":
        # Bring Me the Horizon release
        print(f"         >>> CANDIDATES: Album titles: SEMPITERNAL, AMO, THATSTHESPIRIT, POSTUMAN, NEON")
    elif name == "14D":
        # Perry and kin, 7 letters
        if e["len"] == 7:
            print(f"         >>> CANDIDATES: PERRYS? No... 'Perry and kin' = KATY AND... hmm")
            print(f"             Could be PLATYPUS (Perry the Platypus and kin?)")
    elif name == "18D":
        # Driver who won awards for his Ferrari
        if e["len"] == 4:
            print(f"         >>> CANDIDATES: MANN (Michael Mann directed 'Ferrari')")
    elif name == "23D":
        # Some sports league contracts, for short. 4 letters, pos 2 = J
        if e["len"] == 4:
            print(f"         >>> Pattern: ??J? → sports contracts abbreviation")
    elif name == "37D":
        # Takes a hot bath. Already placed as ABASH?
        print(f"         >>> Already placed as: ABASH (from P3). But 'Takes a hot bath' ≠ 'Make embarrassed'")
        print(f"             CONFLICT: ABASH = Make embarrassed (P3 clue), but this clue = Takes a hot bath")
        print(f"             POSSIBLE: P3 clue 'Make embarrassed' → ABASH was assigned to wrong entry")
    elif name == "44D":
        # Was a little too close
        print(f"         >>> CANDIDATES: INTIMATE? NEARDEATH? NARROW?")
    elif name == "52D":
        # Japanese streamer, perhaps
        if e["len"] == 4:
            print(f"         >>> CANDIDATES: KITE (Japanese paper streamer/carp streamer)")
    elif name == "60D":
        # ___-12 (conference with two members in 2025)
        if e["len"] == 3:
            print(f"         >>> ANSWER: BIG (Big 12 conference)")
    elif name == "69D":
        # One who preferred $10,000 sushi to $10 sushi → MrBeast reference!
        print(f"         >>> This is from a MrBeast video! The person who chose expensive sushi")
    elif name == "75D":
        # Host of Christmas Holiday Halftime Party
        print(f"         >>> CANDIDATES: This could be a MrBeast reference or TV host")
    elif name == "80D":
        # Words before doubling a piece
        if e["len"] == 4:
            print(f"         >>> CANDIDATES: IDARE (I dare you, before doubling in backgammon?)")
    elif name == "87D":
        # One end of the pencil scale → already TRITE? No...
        # Pencil scale goes from 9H (hardest) to 9B (softest)
        print(f"         >>> Pencil hardness scale: H to B. One end = HARD or SOFT")
        print(f"             Already placed: TRITE at 87D. But 'One end of pencil scale' ≠ 'Burnt or hackneyed'")
    elif name == "96D":
        # John B is one
        print(f"         >>> John B from Outer Banks. He's a POGUEE(POGUE)?")
    elif name == "108D":
        # Motor oil brand
        print(f"         >>> CANDIDATES: STP, PENNZOIL, VALVOLINE, MOBIL, CASTROL")
    elif name == "116D":
        # School where they also say 95-Down
        print(f"         >>> This is a self-referential clue! Need to know 95D first")
    elif name == "124D":
        # File productions
        if e["len"] == 9:
            print(f"         >>> CANDIDATES: SAWDUST? No... FILINGS? SHAVINGS? DOCUMENTS?")
    elif name == "130D":
        # Some cords, 6 letters
        if e["len"] == 6:
            print(f"         >>> CANDIDATES: CABLES, ROPINGS, SINEWS, TWINES")
    elif name == "137D":
        # Cotton weave, 7 letters
        if e["len"] == 7:
            print(f"         >>> Pattern starts with A (from extraction)")
            print(f"             CANDIDATES: AERTEX? No... CAMBRIC? No starts with A...")
    elif name == "173A":
        # One that hangs out at the swimming hole
        if e["len"] == 7:
            print(f"         >>> CANDIDATES: TADPOLE? T-A-D-P-O-L-E = 7 letters!")

# ===== Check if SUPERBOWLSTADIUM is truly wrong =====
print("\n" + "=" * 70)
print("167A ANALYSIS: What fits ??K??????U?????L?")
print("=" * 70)

# 167A: 16 letters, K at pos 2, U at pos 9, L at pos 15
# Clue: "What this puzzle commemorates in eleven hidden words in the theme entries"
print("\n167A pattern: ??K??????U?????L")
print("Clue: What this puzzle commemorates in eleven hidden words in the theme entries")
print("\nIf the 11 hidden words are VOLCANO names (since answer = Eyjafjallajökull):")
print("  The puzzle commemorates VOLCANIC SOMETHING")
print("  VOLCANICERUPTION = 16 but V-O-L-C-A-N-I-C-E-R-U-P-T-I-O-N → pos 2=L, 9=R, 15=N ✗")
print("  What 16-letter word/phrase has K@2, U@9, L@15?")

# Try some options
candidates_167 = [
    "ICKENNAMEVOLCANO",  # guess
    "OAKENHILLSVOLCAL",  # nonsense
]

# Let's think about what "the puzzle commemorates"
# The MrBeast puzzle commemorates... Super Bowl? No, that gives SUPERBOWLSTADIUM which conflicts.
# What about volcano-related events?
# 2010 eruption of Eyjafjallajökull disrupted flights worldwide
# The puzzle might commemorate LOCATIONS/PLACES

# Actually, maybe we should just look for 16-letter words/phrases with these constraints
print("\n  Need community data or more crossings to determine 167A")

# ===== Check what new extraction tells us about 167A =====
print("\n  If 167A starts at col 9, row 22:")
print(f"  167A constraints from extraction:")
print(f"    pos  2 (col 11) = K")
print(f"    pos  9 (col 18) = U")
print(f"    pos 15 (col 24) = L")
print(f"  Other constraints from crossings at non-circled cells would help narrow this")

# ===== CRITICAL: Does 87D = TRITE still work? =====
# 87D starts at (11,9), goes down 5 cells to (15,9)
# Extraction gives NO constraints directly on 87D
# But let's verify: 87D clue is "One end of the pencil scale"
# 87D placed as TRITE from P3 ("Burnt or hackneyed")
# Pencil scale: H (hard) to B (soft), or 9H to 9B
# TRITE doesn't match "One end of the pencil scale"!
print("\n" + "=" * 70)
print("CONFLICT CHECK: P3 ANSWER ASSIGNMENTS")
print("=" * 70)
print("\n87D was placed as TRITE (from P3 clue 'Burnt or hackneyed')")
print("But new clue for 87D is 'One end of the pencil scale'")
print("Pencil scale: 9H (hardest) to 9B (softest)")
print("TRITE ≠ 'One end of the pencil scale'")
print("→ TRITE might go in a DIFFERENT entry, not 87D!")
print()
print("37D was placed as ABASH (from P3 clue 'Make embarrassed')")
print("But new clue for 37D is 'Takes a hot bath'")
print("→ ABASH (5 letters) ≠ 'Takes a hot bath'")
print("→ 'Takes a hot bath' = SOAKS? BATHS? STEAMS?")
print("→ ABASH might go in a DIFFERENT entry!")
print()
print("CRITICAL INSIGHT: P3 clues are NOT the crossword clues!")
print("P3 provides crossword ANSWERS, but we don't know which entry each goes to!")
print("We were WRONG to assume P3 answer #5 = 37D, P3 answer #18 = 87D, etc.")

# ===== SIMILARLY check 58A =====
print("\n58A was placed as PUSH (from P9)")
print("New clue for 58A is '___ Ninja YouTube series'")
print("PUSH Ninja? Not a real YouTube series.")
print("→ PUSH probably goes in a DIFFERENT entry!")
print()
print("This means many of our 'confirmed' placements may be WRONG!")
print("We need to re-match P3/P8/P9 answers to entries using the NEW clues.")
