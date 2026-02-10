#!/usr/bin/env python3
"""
Theme Entry Tracer
Traces ALL crossing constraints through theme entries to deduce hidden location names.
Uses the ORGANIC hypothesis for 104D and other deductions.
"""

# ============================================================
# GRID SETUP (same as comprehensive_solver.py)
# ============================================================

GRID_SIZE = 25
BLACK = {
    (0,7),(0,8),(0,15),(0,16),(1,7),(1,15),(1,16),(2,16),
    (3,4),(3,10),(3,14),(3,20),(4,4),(4,5),(4,6),(4,11),(4,21),
    (5,4),(5,8),(5,13),(5,18),(5,19),(6,16),(6,23),(6,24),
    (7,7),(7,12),(7,17),(7,24),(8,3),(8,9),(8,14),(8,15),(8,20),
    (9,0),(9,1),(9,2),(9,9),(9,10),(10,0),(10,4),(10,8),(10,9),(10,16),(10,21),
    (11,5),(11,11),(11,17),(11,21),(12,6),(12,18),
    (13,3),(13,7),(13,13),(13,19),(14,3),(14,8),(14,15),(14,16),(14,20),(14,24),
    (15,14),(15,15),(15,22),(15,23),(15,24),(16,4),(16,9),(16,10),(16,15),(16,21),
    (17,0),(17,7),(17,12),(17,17),(18,0),(18,1),(18,8),
    (19,5),(19,6),(19,11),(19,16),(19,20),(20,3),(20,13),(20,18),(20,19),(20,20),
    (21,4),(21,10),(21,14),(21,20),(22,8),
    (23,8),(23,9),(23,17),(24,8),(24,9),(24,16),(24,17),
}

grid = {}  # (row, col) -> letter

# All confirmed placements
PLACED = {
    # Original 13
    'DORA': (4, 7, 'A'), 'ABASH': (4, 10, 'D'), 'ROTUNDA': (6, 13, 'D'),
    'PUSH': (7, 8, 'A'), 'HAFT': (8, 10, 'A'), 'ZIP': (11, 8, 'D'),
    'TRITE': (11, 9, 'D'), 'ADORN': (11, 12, 'A'), 'CIRCLEABOUT': (12, 7, 'A'),
    'PINTO': (13, 8, 'A'), 'TOLEDO': (14, 9, 'A'), 'DENVER': (14, 13, 'D'),
    'TONI': (16, 11, 'A'),
    # New placements
    'TONER': (12, 17, 'D'), 'ACHOO': (13, 14, 'A'), 'REGINA': (15, 16, 'A'),
    'ERASE': (16, 16, 'A'),
}

for word, (r, c, d) in PLACED.items():
    for i, letter in enumerate(word):
        if d == 'A':
            grid[(r, c + i)] = letter
        else:
            grid[(r + i, c)] = letter

def get_cell(r, c):
    if (r, c) in BLACK:
        return '#'
    return grid.get((r, c), '.')

# ============================================================
# HYPOTHESIS: 104D = ORGANIC
# ============================================================
print("=" * 70)
print("TESTING HYPOTHESIS: 104D = ORGANIC")
print("=" * 70)

# 104D starts at (13,18), goes DOWN col 18, length 7
hypothesis_104d = "ORGANIC"
for i, letter in enumerate(hypothesis_104d):
    r, c = 13 + i, 18
    existing = get_cell(r, c)
    if existing != '.' and existing != letter:
        print(f"  CONFLICT at ({r},{c}): existing={existing}, need={letter}")
    else:
        if existing == letter:
            print(f"  ({r},{c}) = {letter} ✓ (already confirmed)")
        else:
            print(f"  ({r},{c}) = {letter} (NEW)")
            grid[(r, c)] = letter

# What does this tell us?
print("\nImplications of ORGANIC:")
print(f"  111A[1] = R → 111A = N R ? (starts at (14,17))")
print(f"    → Most likely: NRA (National Rifle Association)")
print(f"  134A[0] = N (starts at (17,18))")
print(f"  138A[9] = I (theme entry position 9!)")
print(f"  146A[1] = C → 146A = ? C ?")

# If 111A = NRA
print("\nIf 111A = NRA:")
nra_word = "NRA"
for i, letter in enumerate(nra_word):
    r, c = 14, 17 + i
    existing = get_cell(r, c)
    if existing == letter:
        print(f"  ({r},{c}) = {letter} ✓")
    elif existing == '.':
        print(f"  ({r},{c}) = {letter} (NEW)")
    else:
        print(f"  ({r},{c}) = {letter} CONFLICT with {existing}!")

# 111A[2] = A → (14,19) = A
# This is also 112D[0]
# So 112D starts with A: A I S ? ? ?
print(f"\n  → 112D = A I S ? ? ? (starts at (14,19), col 19, len 6)")
print(f"    Already have I at pos 1 from REGINA, S at pos 2 from ERASE")

# Check dictionary for AIS???
try:
    with open('/usr/share/dict/words') as f:
        all_words = [line.strip().upper() for line in f if line.strip().isalpha()]
except:
    all_words = []

ais_words = [w for w in all_words if len(w) == 6 and w[:3] == 'AIS']
print(f"    Dictionary 'AIS???' matches: {ais_words}")

# ============================================================
# Trace all theme entries with current knowledge
# ============================================================
print("\n" + "=" * 70)
print("THEME ENTRY STATUS (After ORGANIC hypothesis)")
print("=" * 70)

theme_entries = {
    '25A': (2, 0, 16),   # row 2, cols 0-15
    '50A': (6, 0, 16),   # row 6, cols 0-15
    '73A': (9, 11, 14),  # row 9, cols 11-24
    '94A': (12, 7, 11),  # CIRCLEABOUT (filled)
    '114A': (15, 0, 14), # row 15, cols 0-13
    '138A': (18, 9, 16), # row 18, cols 9-24
    '167A': (22, 9, 16), # row 22, cols 9-24
    '19D': (0, 22, 15),  # col 22, rows 0-14
    '78D': (10, 2, 15),  # col 2, rows 10-24
}

for name, (r, c, l) in theme_entries.items():
    d = 'A' if name.endswith('A') else 'D'
    state = []
    for i in range(l):
        if d == 'A':
            state.append(get_cell(r, c + i))
        else:
            state.append(get_cell(r + i, c))
    state_str = ''.join(state)
    known = sum(1 for s in state if s != '.' and s != '#')
    print(f"  {name} (len={l}): {state_str}  [{known}/{l}]")

# ============================================================
# DAKAR THEORY for 50A
# ============================================================
print("\n" + "=" * 70)
print("DAKAR THEORY: Hidden in 50A positions 9-13")
print("=" * 70)

# 50A currently: ..........A..R..
# If DAKAR at pos 9-13: D A K A R
# 50A would be: .........DAKAR..
# pos 9 = D, pos 10 = A ✓, pos 11 = K, pos 12 = A, pos 13 = R ✓
print("50A with DAKAR: .........DAKAR..")
print("  pos 9 = D → 8D[6] = D")
print("  pos 10 = A ✓ (already confirmed from ABASH)")
print("  pos 11 = K → 46D[1] = K")
print("  pos 12 = A → 11D[6] = A (11D starts at (0,12), len 7)")
print("  pos 13 = R ✓ (already confirmed from ROTUNDA)")

# Check: 46D = ??HA?? → if pos 1 = K: ?KHA??
# This gives us ...KHA... - words matching ?KHA??:
print("\n46D with K at pos 1: ?KHA??")
kha_words = [w for w in all_words if len(w) == 6 and w[1] == 'K' and w[2] == 'H' and w[3] == 'A']
print(f"  Dictionary matches: {kha_words}")

# What about 11D = ?????A? (length 7, A at pos 6)
print("\n11D starts at (0,12), col 12, length 7 = rows 0-6")
print("  If 50A gives pos 12 = A at row 6: 11D[6] = A")
# Also 11D[4] = 66A related? 66A = HAFT at (8,10)... no, that's row 8, col 10-13. (8,12) = F.
# But 11D goes from row 0 to row 6. (8,12) is row 8, beyond 11D.
# So 11D[0] to 11D[6] = (0,12) to (6,12)
# 11D[6] = (6,12) = 50A pos 12

# What we know for 11D:
# (0,12): circled cell! 11D starts here.
# pos 0: (0,12) = 8A[3] (8A at (0,9) len 6: cols 9-14)
# pos 1: (1,12) = 23A[4] (23A at (1,8) len 7: cols 8-14)
# pos 2: (2,12) = 25A[12] (theme entry!)
# pos 3: (3,12) = 31A[1] (31A at (3,11) len 3: cols 11-13)
# pos 4: (4,12) = 38A[0] (38A at (4,12) len 9: starts at col 12)
# pos 5: (5,12) = 45A[3] (45A at (5,9) len 4: cols 9-12... wait. 45A starts at col 9, len 4: cols 9,10,11,12. pos 3 = (5,12))
# pos 6: (6,12) = 50A[12]
print("\n11D positions:")
for i in range(7):
    r2 = i
    c2 = 12
    val = get_cell(r2, c2)
    print(f"  pos {i}: ({r2},{c2}) = '{val}'")

# 8D analysis with DAKAR: 8D[6] = D (from 50A pos 9)
# 8D pattern becomes: ????R?DU
print("\n8D with DAKAR constraint: ????R?DU")
rddu_words = [w for w in all_words if len(w) == 8 and w[4] == 'R' and w[6] == 'D' and w[7] == 'U']
print(f"  Dictionary matches for ????R?DU: {rddu_words}")

# Also check with H2O pattern (P1 answers have H+2O's)
h2o_8letter = [w for w in all_words if len(w) == 8 and w.count('O') >= 2 and 'H' in w]
rddu_h2o = [w for w in h2o_8letter if w[4] == 'R' and w[6] == 'D' and w[7] == 'U']
print(f"  H2O words matching ????R?DU: {rddu_h2o}")

# Without the D constraint (in case DAKAR theory is wrong):
print(f"\n8D original pattern: ????R??U")
ru_words = [w for w in all_words if len(w) == 8 and w[4] == 'R' and w[7] == 'U']
print(f"  Dictionary matches for ????R??U ({len(ru_words)}): {ru_words[:20]}...")

# ============================================================
# Location hiding in theme entries - cross-check
# ============================================================
print("\n" + "=" * 70)
print("LOCATION HIDING CROSS-CHECK")
print("=" * 70)

# The 11 AROUNDWORLD locations need to be hidden in the theme entries
# Theme entries: 25A(16), 50A(16), 73A(14), 94A(11), 114A(14), 138A(16), 167A(16)
# Also: 19D(15), 78D(15) - but these might not be "theme" in the traditional sense
# Total theme letters: 16+16+14+11+14+16+16 = 103 letters in across themes
# With 19D and 78D: 103 + 30 = 133 total

# 94A = CIRCLEABOUT already known. Does it hide a location?
# Possible hidden locations in CIRCLEABOUT:
#   CABO (positions 6-9: A-B-O-U? No, C-A-B-O-U-T has CABO at 5-8 if you read CIRCLEABOUT)
#   Actually: C-I-R-C-L-E-A-B-O-U-T
#   CABO: not consecutive
#   CIRCLE: well it contains CIRCLE
#   BOUT: trivial
#   IRAQ: I-R-A... nope, IRCA not IRAQ
#   LEBA: L-E-B-A? No, E-A-B, not right order
#   Actually looking at it: no standard location is hidden in CIRCLEABOUT consecutively.

print("94A = CIRCLEABOUT - scanning for hidden locations:")
locations_all = [
    'MALI', 'TEHRAN', 'LAGOS', 'SUDAN', 'DUBAI', 'OMAN', 'ADEN', 'WALES', 'WUHAN',
    'GOA', 'JOS', 'QOM', 'NIGER', 'DAKAR', 'DELHI', 'CHAD', 'LIMA', 'PERU', 'ACCRA',
    'GHANA', 'RIYADH', 'CAIRO', 'TOKYO', 'PARIS', 'LONDON', 'TORONTO', 'NAIROBI',
    'MUMBAI', 'SYDNEY', 'BERLIN', 'MOSCOW', 'ROME', 'BAKU', 'DOHA', 'MINSK', 'OSLO',
    'TUNIS', 'RABAT', 'QUITO', 'KABUL', 'DHAKA', 'HANOI', 'SOFIA', 'ABUJA',
    'ADDIS', 'AMMAN', 'ANKARA', 'BOGOTA', 'BRASILIA', 'BUENOS', 'CANBERRA',
    'COLOMBO', 'DAMASCUS', 'DUBLIN', 'HAVANA', 'HELSINKI', 'JAKARTA', 'JERUSALEM',
    'KUALA', 'KUWAIT', 'KYIV', 'LISBON', 'MADRID', 'MANILA', 'MEXICO', 'NAIROBI',
    'NASSAU', 'OTTAWA', 'PANAMA', 'PRAGUE', 'RIYADH', 'SANTIAGO', 'SEOUL',
    'SINGAPORE', 'STOCKHOLM', 'TAIPEI', 'TEHRAN', 'VIENNA', 'WARSAW', 'WELLINGTON',
    'GREENVILLE', 'RALEIGH', 'WICHITA', 'DENVER', 'TOLEDO',
]

for loc in sorted(set(locations_all)):
    theme = "CIRCLEABOUT"
    if loc in theme:
        print(f"  Found '{loc}' in CIRCLEABOUT at position {theme.index(loc)}")

# Check DAKAR in 50A (with current partial)
print("\nChecking if DAKAR can be in 50A: .........DAKAR..")
print("  DAKAR would span positions 9-13. Both known letters match. ✓")

# Which locations could be hidden in each theme entry?
# For this we need more filled letters. Let me compile what we know:

print("\n" + "=" * 70)
print("HYPOTHESIS: 50A contains DAKAR (pos 9-13)")
print("=" * 70)

# If 50A = _ _ _ _ _ _ _ _ _ D A K A R _ _
# We need the full 16-letter answer
# Common theme entry patterns that could contain DAKAR:
# Words/phrases with DAKAR in them:
dakar_containing = [w for w in all_words if 'DAKAR' in w.upper()]
print(f"Dictionary words containing DAKAR: {dakar_containing}")

# More likely: DAKAR spans across natural word boundaries in a multi-word theme answer
# Like "___DAK_AR__" or "___D_AKAR__"
# Actually in crosswords, hidden words are CONSECUTIVE LETTERS in the entry
# So the entry has ...DAKAR... somewhere

# The entry is 16 letters. With DAKAR at positions 9-13:
# _ _ _ _ _ _ _ _ _ D A K A R _ _
# That leaves 11 other letters to form a meaningful phrase

# What about location names that could be in other theme entries?
print("\nScanning all theme entries for potential hidden locations:")
print("(Using current known letters as constraints)")

theme_states = {
    '25A': list('................'),  # 16 letters, 0 known
    '50A': list('..........A..R..'),  # 16 letters, 2 known
    '73A': list('..U...........'),    # 14 letters, 1 known
    '114A': list('.........E...E'),    # 14 letters, 2 known
    '138A': list('....E...........'),  # 16 letters, 1 known + I at pos 9 from ORGANIC
    '167A': list('................'),  # 16 letters, 0 known
}

# Update 138A with ORGANIC hypothesis
theme_states['138A'][9] = 'I'  # from ORGANIC pos 5
print(f"\n138A updated: {''.join(theme_states['138A'])}")

# For each theme entry, check which AROUNDWORLD locations could fit
staircase_locations = {
    1: ['MALI'],           # 4 letters, word[1]=A
    2: ['TEHRAN'],         # 6 letters, word[3]=R (but hiding impossible!)
    3: ['LAGOS'],          # 5 letters, word[3]=O
    4: ['SUDAN', 'DUBAI'], # 5 letters, word[1]=U
    5: ['OMAN'],           # 4 letters, word[3]=N
    6: ['ADEN'],           # 4 letters, word[1]=D
    7: ['WALES', 'WUHAN'], # 5 letters, word[0]=W
    8: ['GOA', 'JOS', 'RIO', 'QOM'], # 3 letters, word[1]=O
    9: ['NIGER', 'DAKAR'], # 5 letters, word[4]=R
    10: ['DELHI'],         # 5 letters, word[2]=L
    11: ['CHAD'],          # 4 letters, word[3]=D
}

print("\nWhich staircase locations could fit in which theme entries?")
for row_num, locs in staircase_locations.items():
    for loc in locs:
        for theme_name, state in theme_states.items():
            entry_str = ''.join(state)
            # Check all possible starting positions
            for start in range(len(state) - len(loc) + 1):
                fits = True
                for i, letter in enumerate(loc):
                    if state[start + i] != '.' and state[start + i] != letter:
                        fits = False
                        break
                if fits:
                    # Show position
                    preview = list(entry_str)
                    for i, letter in enumerate(loc):
                        preview[start + i] = letter.lower()
                    # Mark this as potential
                    print(f"  Row {row_num:2d}: {loc:8s} → {theme_name} pos {start}-{start+len(loc)-1}: {''.join(preview)}")

# ============================================================
# Summary of deductions
# ============================================================
print("\n" + "=" * 70)
print("SUMMARY OF DEDUCTIONS")
print("=" * 70)

print("""
CONFIRMED NEW PLACEMENTS:
  96D = TONER (crossword answer from P8)
  103A = ACHOO (crossword answer from P1)
  117A = REGINA (crossword answer from P4)
  123A = ERASE (crossword answer from P3)

STRONG HYPOTHESES:
  104D = ORGANIC (7 dict matches, all ORGAN-*)
    → 138A pos 9 = I
    → 134A starts with N
    → If 111A = NRA: 112D starts with A

  50A contains DAKAR at positions 9-13
    → 8D[6] = D, 46D[1] = K, 11D[6] = A
    → 8D becomes ????R?DU (very constrained)

THEME ENTRY PROGRESS:
  25A: ................ (0/16)
  50A: ..........A..R.. → with DAKAR: .........DAKAR.. (5/16)
  73A: ..U........... (1/14)
  114A: .........E...E (2/14)
  138A: ....E....I...... (2/16, I from ORGANIC)
  167A: ................ (0/16)

STILL NEED:
  - More crossing letters for 25A, 73A, 114A, 138A, 167A
  - Fill entries in rows 0-3, 17-24 (most unconstrained region)
  - Determine which P4 cities go where
""")
