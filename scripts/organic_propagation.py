#!/usr/bin/env python3
"""
Test ORGANIC hypothesis for 104D and propagate constraints to find new placements.
Also try expanded dictionary matching for all partially constrained entries.
"""

import subprocess
import re

# ============================================================
# Grid state from 17 confirmed placements
# ============================================================

GRID_SIZE = 25
grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Black cells
BLACK_CELLS = [
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
    (21,4),(21,10),(21,14),(21,20),(22,8),(23,8),(23,9),(23,17),
    (24,8),(24,9),(24,16),(24,17),
]
for r, c in BLACK_CELLS:
    grid[r][c] = '#'

# Placed entries
PLACED = [
    ('36A', 4, 7, 'DORA'),
    ('37D', 4, 10, 'ABASH'),
    ('53D', 6, 13, 'ROTUNDA'),
    ('58A', 7, 8, 'PUSH'),
    ('66A', 8, 10, 'HAFT'),
    ('86D', 11, 8, 'ZIP'),
    ('87D', 11, 9, 'TRITE'),
    ('88A', 11, 12, 'ADORN'),
    ('94A', 12, 7, 'CIRCLEABOUT'),
    ('96D', 12, 17, 'TONER'),
    ('102A', 13, 8, 'PINTO'),
    ('103A', 13, 14, 'ACHOO'),
    ('109A', 14, 9, 'TOLEDO'),
    ('110D', 14, 13, 'DENVER'),
    ('117A', 15, 16, 'REGINA'),
    ('121A', 16, 11, 'TONI'),
    ('123A', 16, 16, 'ERASE'),
]

def place_word(row, col, word, direction):
    for i, ch in enumerate(word):
        if direction.endswith('A'):
            grid[row][col + i] = ch
        else:
            grid[row + i][col] = ch

for name, row, col, word in PLACED:
    direction = 'A' if 'A' in name else 'D'
    place_word(row, col, word, direction)

# ============================================================
# ALL ENTRIES with positions
# ============================================================

# Format: (name, row, col, length, direction)
ACROSS_ENTRIES = [
    ('1A',0,0,7),('8A',0,9,6),('14A',0,17,8),('22A',1,0,7),('23A',1,8,7),
    ('24A',1,17,8),('25A',2,0,16),('28A',2,17,8),('29A',3,0,4),('30A',3,5,5),
    ('31A',3,11,3),('32A',3,15,5),('34A',3,21,4),('35A',4,0,4),('36A',4,7,4),
    ('38A',4,12,9),('41A',4,22,3),('42A',5,0,4),('43A',5,5,3),('45A',5,9,4),
    ('47A',5,14,4),('48A',5,20,5),('50A',6,0,16),('54A',6,17,6),('57A',7,0,7),
    ('58A',7,8,4),('59A',7,13,4),('61A',7,18,6),('63A',8,0,3),('64A',8,4,5),
    ('66A',8,10,4),('68A',8,16,4),('70A',8,21,4),('72A',9,3,6),('73A',9,11,14),
    ('77A',10,1,3),('79A',10,5,3),('80A',10,10,6),('81A',10,17,4),('82A',10,22,3),
    ('83A',11,0,5),('85A',11,6,5),('88A',11,12,5),('90A',11,18,3),('91A',11,22,3),
    ('92A',12,0,6),('94A',12,7,11),('97A',12,19,6),('99A',13,0,3),('100A',13,4,3),
    ('102A',13,8,5),('103A',13,14,5),('105A',13,20,5),('106A',14,0,3),('107A',14,4,4),
    ('109A',14,9,6),('111A',14,17,3),('113A',14,21,3),('114A',15,0,14),('117A',15,16,6),
    ('119A',16,0,4),('120A',16,5,4),('121A',16,11,4),('123A',16,16,5),('124A',16,22,3),
    ('127A',17,1,6),('129A',17,8,4),('132A',17,13,4),('134A',17,18,7),('136A',18,2,6),
    ('138A',18,9,16),('141A',19,0,5),('143A',19,7,4),('145A',19,12,4),('146A',19,17,3),
    ('147A',19,21,4),('148A',20,0,3),('149A',20,4,9),('153A',20,14,4),('155A',20,21,4),
    ('156A',21,0,4),('158A',21,5,5),('159A',21,11,3),('161A',21,15,5),('164A',21,21,4),
    ('165A',22,0,8),('167A',22,9,16),('171A',23,0,8),('172A',23,10,7),('173A',23,18,7),
    ('174A',24,0,8),('175A',24,10,6),('176A',24,18,7),
]

DOWN_ENTRIES = [
    ('1D',0,0,9),('2D',0,1,9),('3D',0,2,9),('4D',0,3,8),('5D',0,4,3),
    ('6D',0,5,4),('7D',0,6,4),('8D',0,9,8),('9D',0,10,3),('10D',0,11,4),
    ('11D',0,12,7),('12D',0,13,5),('13D',0,14,3),('14D',0,17,7),('15D',0,18,5),
    ('16D',0,19,5),('17D',0,20,3),('18D',0,21,4),('19D',0,22,15),('20D',0,23,6),
    ('21D',0,24,6),('23D',1,8,4),('26D',2,7,5),('27D',2,15,6),('33D',3,16,3),
    ('37D',4,10,5),('39D',4,14,4),('40D',4,20,4),('43D',5,5,6),('44D',5,6,7),
    ('46D',5,11,6),('49D',5,21,5),('51D',6,4,4),('52D',6,8,4),('53D',6,13,7),
    ('55D',6,18,6),('56D',6,19,7),('60D',7,16,3),('62D',7,23,8),('65D',8,7,5),
    ('67D',8,12,9),('69D',8,17,3),('71D',8,24,6),('72D',9,3,4),('74D',9,14,6),
    ('75D',9,15,5),('76D',9,20,5),('77D',10,1,8),('78D',10,2,15),('80D',10,10,6),
    ('83D',11,0,6),('84D',11,4,5),('86D',11,8,3),('87D',11,9,5),('89D',11,16,3),
    ('93D',12,5,7),('95D',12,11,7),('96D',12,17,5),('98D',12,21,4),('101D',13,6,6),
    ('104D',13,18,7),('108D',14,7,3),('110D',14,13,6),('112D',14,19,6),('115D',15,3,5),
    ('116D',15,8,3),('117D',15,16,4),('118D',15,20,4),('122D',16,14,5),('124D',16,22,9),
    ('125D',16,23,9),('126D',16,24,9),('128D',17,4,4),('130D',17,9,6),('131D',17,10,4),
    ('133D',17,15,8),('135D',17,21,8),('137D',18,7,7),('139D',18,12,7),('140D',18,17,5),
    ('141D',19,0,6),('142D',19,1,6),('144D',19,8,3),('150D',20,5,5),('151D',20,6,5),
    ('152D',20,11,5),('154D',20,16,4),('157D',21,3,4),('160D',21,13,4),('162D',21,18,4),
    ('163D',21,19,4),('166D',22,4,3),('168D',22,10,3),('169D',22,14,3),('170D',22,20,3),
]

ALL_ENTRIES = [(n, r, c, l, 'A') for n, r, c, l in ACROSS_ENTRIES] + \
              [(n, r, c, l, 'D') for n, r, c, l in DOWN_ENTRIES]

def get_pattern(row, col, length, direction):
    """Get current letter pattern for an entry."""
    pattern = []
    for i in range(length):
        if direction == 'A':
            ch = grid[row][col + i]
        else:
            ch = grid[row + i][col]
        pattern.append(ch)
    return ''.join(pattern)

# ============================================================
# ORGANIC HYPOTHESIS
# ============================================================

print("=" * 80)
print("ORGANIC HYPOTHESIS FOR 104D")
print("=" * 80)

# 104D: row=13, col=18, length=7, direction=D
# Current pattern from grid
pattern_104d = get_pattern(13, 18, 7, 'D')
print(f"\n104D current pattern: {pattern_104d}")

# Place ORGANIC tentatively
organic = "ORGANIC"
print(f"\nIf 104D = {organic}:")
temp_grid = [row[:] for row in grid]  # Deep copy
for i, ch in enumerate(organic):
    temp_grid[13 + i][18] = ch

# Check all entries crossing 104D
crossing_entries = []
for name, row, col, length, direction in ALL_ENTRIES:
    if direction == 'A':
        if col <= 18 < col + length:
            entry_row = row
            if 13 <= entry_row <= 19:
                pos_in_entry = 18 - col
                pos_in_organic = entry_row - 13
                letter = organic[pos_in_organic]
                pattern = get_pattern(row, col, length, 'A')
                new_pattern = list(pattern)
                new_pattern[pos_in_entry] = letter
                new_pattern = ''.join(new_pattern)
                print(f"  {name} (len={length}): pos {pos_in_entry} = {letter}")
                print(f"    Before: {pattern}")
                print(f"    After:  {new_pattern}")
                crossing_entries.append((name, row, col, length, direction, new_pattern))

# Check dictionary matches for the crossing patterns
print(f"\nDictionary matches for crossing entries:")
for name, row, col, length, direction, pattern in crossing_entries:
    # Build regex pattern
    regex = '^' + pattern.replace('.', '[a-z]') + '$'
    result = subprocess.run(['grep', '-i', '-E', regex, '/usr/share/dict/words'],
                          capture_output=True, text=True)
    words = [w.strip() for w in result.stdout.strip().split('\n') if w.strip()]
    words = [w for w in words if len(w) == length]
    if words:
        print(f"  {name} ({pattern}): {len(words)} matches → {words[:10]}")
    else:
        print(f"  {name} ({pattern}): 0 matches")

# ============================================================
# Now propagate ORGANIC and try to match known answers
# ============================================================

print(f"\n{'='*80}")
print("PROPAGATION FROM ORGANIC")
print(f"{'='*80}")

# Known answers by length
KNOWN_ANSWERS = {
    3: ['RAD', 'EAR', 'ION', 'EON', 'ZIP', 'NRA'],  # NRA is a guess for 111A
    4: ['DHOW', 'HAFT', 'DORA', 'RACE', 'TONI', 'NOTE', 'PUSH'],
    5: ['ACHOO', 'WAHOO', 'ABASH', 'OPERA', 'ERASE', 'TRITE', 'ADORN', 'LECAR', 'PINTO', 'TONER', 'WORLD', 'ACCRA'],
    6: ['SCHOOL', 'OHIOAN', 'HOODIE', 'MATTER', 'ECLAIR', 'OPTION', 'ORIENT', 'CHAIRS', 'CONVEX',
        'TOLEDO', 'REGINA', 'DENVER', 'TEMPE', 'WARSAW', 'AUBURN', 'DOVER', 'OTTAWA'],  # some cities
    7: ['TYPHOON', 'OHSHOOT', 'HEARTED', 'MUSTERS', 'ROTUNDA', 'CALIBER', 'PORTION', 'INUTERO', 'QUORUMS', 'HIRPLED',
        'TORONTO', 'ROSWELL', 'DRESDEN', 'SEVILLE', 'ORLANDO', 'WOODWAY', 'SANJUAN'],
    8: ['HOODWINK', 'HULAHOOP', 'SCENARIO', 'NEUROTIC', 'SCREENER', 'ABSOLUTE', 'TEAMSEAS',
        'DURATION', 'CARBLITE', 'POSITRON', 'ROUTINES', 'FLAMINGO', 'CASHTENT', 'ADELAIDE'],
    9: ['HOOVERDAM', 'ROBINHOOD', 'DITHERING', 'HOWITZERS', 'HIGHHEELS', 'ALLUSIONS', 'RESISTIVE',
        'INUNDATOR', 'CABRIOLET', 'RATPOISON', 'OUTLINERS', 'OWENSBORO', 'ANNAPOLIS', 'ROCHESTER'],
}

# If ORGANIC placed, check 111A specifically
# 111A: row=14, col=17, length=3, direction=A
# After ORGANIC: col 17 = ?, col 18 = N (ORGANIC[5] at row 14+1=15... wait)
# Actually 104D is at row 13, col 18, going DOWN. So:
# row 13, col 18 = O
# row 14, col 18 = R
# row 15, col 18 = G
# row 16, col 18 = A
# row 17, col 18 = N
# row 18, col 18 = I
# row 19, col 18 = C

# 111A is at row 14, col 17, length 3. Grid:
# row 14, col 17 = temp_grid[14][17]
# row 14, col 18 = R (from ORGANIC[1])
# row 14, col 19 = temp_grid[14][19]

# Current grid at row 14: ...#....#TOLEDO##...#...#
# col 17 = temp_grid[14][17] (from 96D)
# 96D = TONER at row 12, col 17, length 5 down → rows 12-16
# row 14, col 17 = TONER[2] = N
# So 111A = N, R, ?

# What about col 19?
# 112D starts at row 14, col 19, length 6
# row 14, col 19 = temp_grid[14][19] = ? (first letter of 112D)
# From ORGANIC: nothing at col 19
# From ERASE (123A at row 16, col 16, len 5): row 16, cols 16-20 = E,R,A,S,E
# row 16, col 19 = S → 112D at row 14, col 19, len 6 → 112D[2] when at row 16...
# 112D goes rows 14-19 at col 19. row 16 = 112D[2] = 'S'
# Wait, ERASE is at row 16, cols 16-20: E(16),R(17),A(18),S(19),E(20)
# So grid[16][19] = S. 112D starts at row 14, col 19. 112D[2] = grid[16][19] = S

# From ORGANIC: row 19, col 18 = C → doesn't affect col 19

print(f"\n111A pattern: N R ? (if ORGANIC)")
print(f"  Most likely: NRA (common crossword entry)")

# Check what patterns we get for all entries near ORGANIC
print(f"\nAll affected entries from ORGANIC placement:")
for name, row, col, length, direction in ALL_ENTRIES:
    pattern = get_pattern(row, col, length, direction)
    # Now overlay ORGANIC
    new_pattern = list(pattern)
    changed = False
    for i in range(7):
        org_row = 13 + i
        org_col = 18
        if direction == 'A':
            if row == org_row and col <= org_col < col + length:
                pos = org_col - col
                if new_pattern[pos] == '.':
                    new_pattern[pos] = organic[i]
                    changed = True
        else:
            if col == org_col and row <= org_row < row + length:
                pos = org_row - row
                if new_pattern[pos] == '.':
                    new_pattern[pos] = organic[i]
                    changed = True
    if changed:
        new_pattern = ''.join(new_pattern)
        # Check if any known answer now uniquely fits
        possible = []
        if length in KNOWN_ANSWERS:
            for answer in KNOWN_ANSWERS[length]:
                if len(answer) == length:
                    match = True
                    for j in range(length):
                        if new_pattern[j] != '.' and new_pattern[j] != answer[j]:
                            match = False
                            break
                    if match:
                        possible.append(answer)

        if possible:
            print(f"  {name} (len={length}): {pattern} → {new_pattern}")
            print(f"    Possible answers: {possible}")
            if len(possible) == 1:
                print(f"    *** UNIQUE FIT: {possible[0]} ***")

# ============================================================
# Try NRA for 111A and propagate further
# ============================================================
print(f"\n{'='*80}")
print("CASCADING: ORGANIC → NRA (111A) → further")
print(f"{'='*80}")

# Place ORGANIC and NRA
for i, ch in enumerate(organic):
    grid[13 + i][18] = ch

# NRA at 111A (row 14, col 17, length 3)
# But we already know col 17, row 14 = N (from TONER)
# And col 18, row 14 = R (from ORGANIC)
# So 111A = N, R, A (NRA)
grid[14][19] = 'A'  # NRA's third letter

# Now check what this gives us for 112D
# 112D: row 14, col 19, length 6, DOWN
# row 14 = A (from NRA), row 15 = ?, row 16 = S (from ERASE), row 17-19 = ?
pattern_112d = get_pattern(14, 19, 6, 'D')
print(f"\n112D pattern: {pattern_112d}")

# Check dictionary
regex = '^' + pattern_112d.replace('.', '[a-z]') + '$'
result = subprocess.run(['grep', '-i', '-E', regex, '/usr/share/dict/words'],
                      capture_output=True, text=True)
words = [w.strip() for w in result.stdout.strip().split('\n') if w.strip()]
words = [w for w in words if len(w) == 6]
if words:
    print(f"  Dictionary matches ({len(words)}): {words[:20]}")

# Print updated grid
print(f"\n{'='*80}")
print("UPDATED GRID (with ORGANIC + NRA)")
print(f"{'='*80}")
print(f"     0123456789012345678901234")
for r in range(GRID_SIZE):
    row_str = ''.join(grid[r])
    print(f"R{r:2d} |{row_str}")

# Count placed letters
placed_count = sum(1 for r in range(GRID_SIZE) for c in range(GRID_SIZE)
                   if grid[r][c] not in '.#')
total_white = sum(1 for r in range(GRID_SIZE) for c in range(GRID_SIZE)
                  if grid[r][c] != '#')
print(f"\nPlaced: {placed_count}/{total_white} white cells ({placed_count*100//total_white}%)")

# ============================================================
# Scan ALL partially constrained entries for unique fits
# ============================================================
print(f"\n{'='*80}")
print("SCANNING ALL ENTRIES FOR UNIQUE FITS")
print(f"{'='*80}")

new_placements = []
for name, row, col, length, direction in ALL_ENTRIES:
    pattern = get_pattern(row, col, length, direction)
    if '.' not in pattern:
        continue  # Already complete
    if pattern == '.' * length:
        continue  # No constraints at all

    # Check known answers
    if length in KNOWN_ANSWERS:
        possible = []
        for answer in KNOWN_ANSWERS[length]:
            if len(answer) == length:
                match = True
                for j in range(length):
                    if pattern[j] != '.' and pattern[j] != answer[j]:
                        match = False
                        break
                if match:
                    possible.append(answer)

        if possible and len(possible) <= 3:
            known_count = sum(1 for c in pattern if c != '.')
            print(f"  {name} (len={length}): {pattern} ({known_count} known)")
            print(f"    Candidates: {possible}")
            if len(possible) == 1:
                print(f"    *** UNIQUE FIT: {possible[0]} ***")
                new_placements.append((name, row, col, length, direction, possible[0]))

if new_placements:
    print(f"\n  New unique placements found: {len(new_placements)}")
    for name, row, col, length, direction, answer in new_placements:
        print(f"    {name} = {answer}")
else:
    print(f"\n  No new unique placements found from known answers.")
