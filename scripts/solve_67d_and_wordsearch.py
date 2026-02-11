#!/usr/bin/env python3
"""
Solve 67D (pattern F??AEOE?O) and search grid for hidden location names.
"""

import itertools
import string

# ============================================================
# PART 1: Solve 67D
# ============================================================
# 67D: starts at (8,12), goes down 9 rows to (16,12)
# Pattern: F _ _ A E O E _ O  (positions 0-8)
# Known: pos0=F, pos3=A, pos4=E, pos5=O, pos6=E, pos8=O
# Unknown: pos1, pos2, pos7

print("=" * 60)
print("PART 1: SOLVING 67D")
print("=" * 60)
print()
print("Pattern: F _ _ A E O E _ O")
print("Known letters: F(0), A(3), E(4), O(5), E(6), O(8)")
print("Unknown: positions 1, 2, 7")
print()

# Where do these letters come from?
# (8,12): F  - from 66A or some other across. 66A is at (8,10) len 4, so (8,10-13). pos 2 of 66A = F? HAFT[2] = F. YES! ✓
# (9,12): ?  - in 73A at position 1. 73A starts at (9,11). So (9,12) = 73A[1]
# (10,12): ? - in 80A at position 2. 80A starts at (10,10). So (10,12) = 80A[2]
# (11,12): A - from 88A. 88A = ADORN at (11,12). ADORN[0] = A. ✓
# (12,12): E - from 94A = CIRCLEABOUT at (12,7). Position 5 = E. ✓
# (13,12): O - 102A = PINTO at (13,8). Position 4 = O. ✓
# (14,12): E - 109A = TOLEDO at (14,9). Position 3 = E. ✓
# (15,12): ? - in 114A at position 12. 114A starts at (15,0). So (15,12) = 114A[12]
# (16,12): O - 121A = TONI at (16,11). Position 1 = O. ✓

print("Cross-reference analysis:")
print("  67D[0] = (8,12)  = HAFT[2]     = F ✓")
print("  67D[1] = (9,12)  = 73A[1]      = ? (73A unknown)")
print("  67D[2] = (10,12) = 80A[2]      = ? (80A unknown)")
print("  67D[3] = (11,12) = ADORN[0]    = A ✓")
print("  67D[4] = (12,12) = CIRCLEABOUT[5] = E ✓")
print("  67D[5] = (13,12) = PINTO[4]    = O ✓")
print("  67D[6] = (14,12) = TOLEDO[3]   = E ✓")
print("  67D[7] = (15,12) = 114A[12]    = ? (114A unknown)")
print("  67D[8] = (16,12) = TONI[1]     = O ✓")
print()

# Try all combinations of 3 unknown letters
print("Brute force: trying all 26^3 = 17576 combinations...")
candidates = []
try:
    with open('/usr/share/dict/words', 'r') as f:
        all_words = set(w.strip().upper() for w in f if len(w.strip()) == 9)
except:
    all_words = set()

for c1 in string.ascii_uppercase:
    for c2 in string.ascii_uppercase:
        for c3 in string.ascii_uppercase:
            word = f"F{c1}{c2}AEOE{c3}O"
            if word in all_words:
                candidates.append(word)

print(f"Dictionary matches for F??AEOE?O: {len(candidates)}")
for c in candidates:
    print(f"  {c}")

# Also try compound words / phrases
print()
print("Trying common word patterns:")
# F__AEOE_O could be a compound. Let's look at it differently:
# The pattern FxxAEOExO...
# FIREPROOF? No, wrong pattern
# What if we relax and think of phrases?
# F + ?? + AEOE + ? + O
# FAR AEOEO? No...

# Let's try without dictionary - what patterns make sense?
# Position 1,2,7 unknown
# Could be: FORAEOE?O, FURAEOE?O, etc.
# FO?AEOE?O - like FOCAEOE?O?
# Common F words: FACE, FAKE, FAME, FARE, FATE, FIRE, FIVE, FORE, FREE, FUSE
# F_RAEOE_O? FORAEOEHO?
# F_LAEOE_O? FOLAEOEHO?

# Try splitting: maybe it's two words or a phrase
# F??A + EOE?O
# F??AE + OE?O
print()
print("Pattern analysis:")
print("  If compound: F?? + A + EOE + ?O")
print("  Or: F??A + E + O + E?O")
print("  Substring 'AEOE' is very unusual in English")
print("  Could be a name: FARAEOERO? FORESEEABLE? No, wrong length")
print()

# Since this is Mike Selinker's puzzle, try unusual/creative fills
special_candidates = []
for c1 in string.ascii_uppercase:
    for c2 in string.ascii_uppercase:
        for c3 in string.ascii_uppercase:
            word = f"F{c1}{c2}AEOE{c3}O"
            # Check if any 3-5 letter substrings are common words
            has_words = False
            for i in range(len(word)):
                for j in range(i+3, min(i+6, len(word)+1)):
                    sub = word[i:j]
                    if sub in {'FOR', 'FAR', 'FIN', 'FOE', 'AGE', 'ACE', 'ARE', 'ONE', 'ORE', 'OE', 'THE', 'EON'}:
                        has_words = True
            if has_words:
                special_candidates.append(word)

print(f"Patterns with common subwords: {len(special_candidates)}")
if len(special_candidates) <= 50:
    for c in special_candidates:
        print(f"  {c}")
else:
    print(f"  (too many to list, showing first 20)")
    for c in special_candidates[:20]:
        print(f"  {c}")

# ============================================================
# PART 2: Word Search for Hidden Locations
# ============================================================
print()
print("=" * 60)
print("PART 2: WORD SEARCH FOR HIDDEN LOCATIONS IN GRID")
print("=" * 60)
print()

grid = [
    ".......##......##........",  # R0
    ".......#.......##........",  # R1
    "................#........",  # R2
    "....#.....#...#.....#....",  # R3
    "....###DORA#.........#...",  # R4
    "....#...#.B..#....##.....",  # R5
    "..........A..R..#......##",  # R6
    ".......#PUSH#O...#......#",  # R7
    "...#.....#HAFT##....#....",  # R8
    "###......##..U...........",  # R9
    "#...#...##...N..#....#...",  # R10
    ".....#..ZT.#ADORN#...#...",  # R11
    "......#CIRCLEABOUT#......",  # R12
    "...#...#PINTO#ACHOO#.....",  # R13
    "...#....#TOLEDO##NRA#...#",  # R14
    ".........E...E##REGINA###",  # R15
    "....#....##TONI#ERASE#...",  # R16
    "#......#....#V...#.......",  # R17
    "##......#....E...........",  # R18
    ".....##....#.R..#...#....",  # R19
    "...#BEASTLAND#....###....",  # R20
    "....#.....#...#.....#....",  # R21
    "........#SUPERBOWLSTADIUM",  # R22
    "........##.......#.......",  # R23
    "........##......##.......",  # R24
]

# Location names to search for (comprehensive list)
locations = [
    # Countries
    "CHAD", "CUBA", "FIJI", "IRAN", "IRAQ", "LAOS", "MALI", "OMAN", "PERU", "TOGO",
    "BENIN", "CHILE", "CHINA", "CONGO", "EGYPT", "GABON", "GHANA", "GUAM", "HAITI",
    "INDIA", "ITALY", "JAPAN", "KENYA", "KOREA", "LIBYA", "MALTA", "NAURU", "NEPAL",
    "NIGER", "PALAU", "QATAR", "SAMOA", "SPAIN", "SUDAN", "SYRIA", "TONGA", "WALES",
    "YEMEN", "BELIZE", "BHUTAN", "BRAZIL", "BRUNEI", "CANADA", "CYPRUS", "FRANCE",
    "GAMBIA", "GREECE", "GUINEA", "GUYANA", "ISRAEL", "JORDAN", "KUWAIT", "LATVIA",
    "MALAWI", "MEXICO", "MONACO", "NORWAY", "PANAMA", "POLAND", "RUSSIA", "RWANDA",
    "SERBIA", "SWEDEN", "TURKEY", "TUVALU", "UGANDA", "ZAMBIA",
    # US States
    "OHIO", "IOWA", "UTAH", "IDAHO", "MAINE", "TEXAS", "ALASKA", "HAWAII", "KANSAS",
    "NEVADA", "OREGON",
    # Cities
    "LIMA", "ROME", "OSLO", "BAKU", "DOHA", "SUVA", "ADEN", "ACRE",
    "ACCRA", "DAKAR", "DELHI", "DHAKA", "KABUL", "LAGOS", "MINSK", "NAURU",
    "PARIS", "QUITO", "SEOUL", "TOKYO", "TUNIS",
    "ANKARA", "ATHENS", "BERLIN", "BOGOTA", "BOSTON", "CAIRNS", "DALLAS",
    "DENVER", "DUBLIN", "HAVANA", "LONDON", "MADRID", "MANILA", "MOSCOW",
    "MUMBAI", "NASSAU", "OTTAWA", "PRAGUE", "RIYADH", "SYDNEY", "TEHRAN",
    "VIENNA", "WARSAW", "ZURICH",
    "TORONTO", "ORLANDO", "TOLEDO", "REGINA", "ROSWELL", "DRESDEN", "SEVILLE",
    "AUBURN", "DOVER", "TEMPE", "ADELAIDE",
    # Other relevant locations
    "CABO", "BALI", "MAUI", "NILE", "ALPS", "ASIA", "EAST",
    "WEST", "NORTH", "SOUTH", "LAND", "BOWL", "STAD",
    "LEVI", "LEVIS", "BEAST", "SUPER",
]

def search_grid(grid, word):
    """Search for word in all 8 directions"""
    rows = len(grid)
    cols = len(grid[0])
    results = []
    directions = [
        (0, 1, "right"), (0, -1, "left"),
        (1, 0, "down"), (-1, 0, "up"),
        (1, 1, "diag-DR"), (1, -1, "diag-DL"),
        (-1, 1, "diag-UR"), (-1, -1, "diag-UL")
    ]

    for r in range(rows):
        for c in range(cols):
            for dr, dc, dirname in directions:
                match = True
                cells = []
                for i, ch in enumerate(word):
                    nr, nc = r + dr*i, c + dc*i
                    if 0 <= nr < rows and 0 <= nc < cols:
                        cell = grid[nr][nc]
                        if cell == ch:
                            cells.append((nr, nc))
                        elif cell == '.' or cell == '#':
                            match = False
                            break
                        else:
                            match = False
                            break
                    else:
                        match = False
                        break
                if match and len(cells) == len(word):
                    results.append((word, r, c, dirname, cells))
    return results

print("Searching for location names in the grid (all 8 directions)...")
print()

all_found = []
for loc in locations:
    found = search_grid(grid, loc)
    if found:
        all_found.extend(found)

# Sort by word length (longer = more interesting)
all_found.sort(key=lambda x: -len(x[0]))

print(f"Total matches found: {len(all_found)}")
print()
for word, r, c, direction, cells in all_found:
    print(f"  {word:20s} at ({r},{c}) going {direction:10s} cells: {cells}")

# ============================================================
# PART 3: Theme entry substring analysis
# ============================================================
print()
print("=" * 60)
print("PART 3: LOCATION SUBSTRINGS IN THEME ENTRIES")
print("=" * 60)
print()

theme_entries = {
    '167A': 'SUPERBOWLSTADIUM',
    '94A': 'CIRCLEABOUT',
    '149A': 'BEASTLAND',
}

for entry_id, answer in theme_entries.items():
    print(f"\n{entry_id} = {answer}:")
    found_in = []
    for loc in locations:
        if len(loc) >= 3 and loc in answer:
            idx = answer.index(loc)
            found_in.append((loc, idx, idx + len(loc) - 1))
    if found_in:
        found_in.sort(key=lambda x: -len(x[0]))
        for loc, start, end in found_in:
            print(f"  {loc} at positions {start}-{end}")
    else:
        print("  No location substrings found")

# ============================================================
# PART 4: Binary encoding of grid rows
# ============================================================
print()
print("=" * 60)
print("PART 4: BINARY ENCODING OF GRID ROWS/COLUMNS")
print("=" * 60)
print()

# Black = 1, White = 0
print("Rows as binary (black=1, white=0):")
for i, row in enumerate(grid):
    binary = ''.join('1' if c == '#' else '0' for c in row)
    decimal = int(binary, 2)
    # Try to interpret as ASCII chunks
    print(f"  R{i:2d}: {binary} = {decimal}")

print()
print("Rows as binary (inverted: black=0, white=1):")
for i, row in enumerate(grid):
    binary = ''.join('0' if c == '#' else '1' for c in row)
    decimal = int(binary, 2)
    print(f"  R{i:2d}: {binary} = {decimal}")

# Try reading 8-bit chunks from concatenated binary
print()
print("Concatenated binary (black=1), read as 8-bit ASCII:")
full_binary = ''
for row in grid:
    full_binary += ''.join('1' if c == '#' else '0' for c in row)
print(f"Total bits: {len(full_binary)}")
ascii_result = ''
for i in range(0, len(full_binary) - 7, 8):
    byte = full_binary[i:i+8]
    val = int(byte, 2)
    if 32 <= val <= 126:
        ascii_result += chr(val)
    else:
        ascii_result += '.'
print(f"ASCII (black=1): {ascii_result[:80]}")

# Inverted
full_binary_inv = ''
for row in grid:
    full_binary_inv += ''.join('0' if c == '#' else '1' for c in row)
ascii_result_inv = ''
for i in range(0, len(full_binary_inv) - 7, 8):
    byte = full_binary_inv[i:i+8]
    val = int(byte, 2)
    if 32 <= val <= 126:
        ascii_result_inv += chr(val)
    else:
        ascii_result_inv += '.'
print(f"ASCII (black=0): {ascii_result_inv[:80]}")

# ============================================================
# PART 5: Vault ring as RLE → binary
# ============================================================
print()
print("=" * 60)
print("PART 5: VAULT RING SEQUENCE AS RLE")
print("=" * 60)
print()

vault_ring = [4,1,8,4,1,3,1,8,4,1,1,3,4,4,4,1,2,1,1,4,4,10,1,1,1,2,4,1,1,1,1,3,1,3,1,1,1,1,8,4,3,1,1,1,1,10]
total = sum(vault_ring)
print(f"Vault ring sequence: {vault_ring}")
print(f"Number of values: {len(vault_ring)}")
print(f"Sum of values: {total}")
print(f"Note: 100 = number of black cells, 625 = total grid cells")

# RLE starting with black (1)
binary_b1 = ''
for i, count in enumerate(vault_ring):
    if i % 2 == 0:
        binary_b1 += '1' * count
    else:
        binary_b1 += '0' * count

# RLE starting with white (0)
binary_w1 = ''
for i, count in enumerate(vault_ring):
    if i % 2 == 0:
        binary_w1 += '0' * count
    else:
        binary_w1 += '1' * count

print(f"RLE (start black): {len(binary_b1)} bits = {binary_b1[:80]}...")
print(f"RLE (start white): {len(binary_w1)} bits = {binary_w1[:80]}...")

if total == 100:
    print("\n*** SUM = 100 = number of black cells! ***")
    print("This could encode which cells are black in a specific reading order!")
elif total == 625:
    print("\n*** SUM = 625 = total grid cells! ***")

# Try ASCII decode
for label, binary in [("start-black", binary_b1), ("start-white", binary_w1)]:
    result = ''
    for i in range(0, len(binary) - 7, 8):
        byte = binary[i:i+8]
        val = int(byte, 2)
        if 32 <= val <= 126:
            result += chr(val)
        else:
            result += '.'
    print(f"ASCII ({label}): {result}")

print()
print("DONE!")
