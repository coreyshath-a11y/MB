#!/usr/bin/env python3
"""
Comprehensive Crossword Solver
Places ALL confirmed answers into the 25x25 grid using constraint propagation.
"""

# ============================================================
# GRID SETUP
# ============================================================

GRID_SIZE = 25

# Black cells
BLACK = {
    (0,7),(0,8),(0,15),(0,16),
    (1,7),(1,15),(1,16),
    (2,16),
    (3,4),(3,10),(3,14),(3,20),
    (4,4),(4,5),(4,6),(4,11),(4,21),
    (5,4),(5,8),(5,13),(5,18),(5,19),
    (6,16),(6,23),(6,24),
    (7,7),(7,12),(7,17),(7,24),
    (8,3),(8,9),(8,14),(8,15),(8,20),
    (9,0),(9,1),(9,2),(9,9),(9,10),
    (10,0),(10,4),(10,8),(10,9),(10,16),(10,21),
    (11,5),(11,11),(11,17),(11,21),
    (12,6),(12,18),
    (13,3),(13,7),(13,13),(13,19),
    (14,3),(14,8),(14,15),(14,16),(14,20),(14,24),
    (15,14),(15,15),(15,22),(15,23),(15,24),
    (16,4),(16,9),(16,10),(16,15),(16,21),
    (17,0),(17,7),(17,12),(17,17),
    (18,0),(18,1),(18,8),
    (19,5),(19,6),(19,11),(19,16),(19,20),
    (20,3),(20,13),(20,18),(20,19),(20,20),
    (21,4),(21,10),(21,14),(21,20),
    (22,8),
    (23,8),(23,9),(23,17),
    (24,8),(24,9),(24,16),(24,17),
}

# All entries: (number, direction, row, col, length)
ENTRIES = [
    # ACROSS
    (1,'A',0,0,7), (8,'A',0,9,6), (14,'A',0,17,8),
    (22,'A',1,0,7), (23,'A',1,8,7), (24,'A',1,17,8),
    (25,'A',2,0,16), (28,'A',2,17,8),
    (29,'A',3,0,4), (30,'A',3,5,5), (31,'A',3,11,3), (32,'A',3,15,5), (34,'A',3,21,4),
    (35,'A',4,0,4), (36,'A',4,7,4), (38,'A',4,12,9), (41,'A',4,22,3),
    (42,'A',5,0,4), (43,'A',5,5,3), (45,'A',5,9,4), (47,'A',5,14,4), (48,'A',5,20,5),
    (50,'A',6,0,16), (54,'A',6,17,6),
    (57,'A',7,0,7), (58,'A',7,8,4), (59,'A',7,13,4), (61,'A',7,18,6),
    (63,'A',8,0,3), (64,'A',8,4,5), (66,'A',8,10,4), (68,'A',8,16,4), (70,'A',8,21,4),
    (72,'A',9,3,6), (73,'A',9,11,14),
    (77,'A',10,1,3), (79,'A',10,5,3), (80,'A',10,10,6), (81,'A',10,17,4), (82,'A',10,22,3),
    (83,'A',11,0,5), (85,'A',11,6,5), (88,'A',11,12,5), (90,'A',11,18,3), (91,'A',11,22,3),
    (92,'A',12,0,6), (94,'A',12,7,11), (97,'A',12,19,6),
    (99,'A',13,0,3), (100,'A',13,4,3), (102,'A',13,8,5), (103,'A',13,14,5), (105,'A',13,20,5),
    (106,'A',14,0,3), (107,'A',14,4,4), (109,'A',14,9,6), (111,'A',14,17,3), (113,'A',14,21,3),
    (114,'A',15,0,14), (117,'A',15,16,6),
    (119,'A',16,0,4), (120,'A',16,5,4), (121,'A',16,11,4), (123,'A',16,16,5), (124,'A',16,22,3),
    (127,'A',17,1,6), (129,'A',17,8,4), (132,'A',17,13,4), (134,'A',17,18,7),
    (136,'A',18,2,6), (138,'A',18,9,16),
    (141,'A',19,0,5), (143,'A',19,7,4), (145,'A',19,12,4), (146,'A',19,17,3), (147,'A',19,21,4),
    (148,'A',20,0,3), (149,'A',20,4,9), (153,'A',20,14,4), (155,'A',20,21,4),
    (156,'A',21,0,4), (158,'A',21,5,5), (159,'A',21,11,3), (161,'A',21,15,5), (164,'A',21,21,4),
    (165,'A',22,0,8), (167,'A',22,9,16),
    (171,'A',23,0,8), (172,'A',23,10,7), (173,'A',23,18,7),
    (174,'A',24,0,8), (175,'A',24,10,6), (176,'A',24,18,7),
    # DOWN
    (1,'D',0,0,9), (2,'D',0,1,9), (3,'D',0,2,9), (4,'D',0,3,8), (5,'D',0,4,3), (6,'D',0,5,4), (7,'D',0,6,4),
    (8,'D',0,9,8), (9,'D',0,10,3), (10,'D',0,11,4), (11,'D',0,12,7), (12,'D',0,13,5), (13,'D',0,14,3),
    (14,'D',0,17,7), (15,'D',0,18,5), (16,'D',0,19,5), (17,'D',0,20,3), (18,'D',0,21,4), (19,'D',0,22,15), (20,'D',0,23,6), (21,'D',0,24,6),
    (23,'D',1,8,4), (26,'D',2,7,5), (27,'D',2,15,6), (33,'D',3,16,3),
    (37,'D',4,10,5), (39,'D',4,14,4), (40,'D',4,20,4),
    (43,'D',5,5,6), (44,'D',5,6,7), (46,'D',5,11,6), (49,'D',5,21,5),
    (51,'D',6,4,4), (52,'D',6,8,4), (53,'D',6,13,7), (55,'D',6,18,6), (56,'D',6,19,7),
    (60,'D',7,16,3), (62,'D',7,23,8),
    (65,'D',8,7,5), (67,'D',8,12,9), (69,'D',8,17,3), (71,'D',8,24,6),
    (72,'D',9,3,4), (74,'D',9,14,6), (75,'D',9,15,5), (76,'D',9,20,5),
    (77,'D',10,1,8), (78,'D',10,2,15), (80,'D',10,10,6), (83,'D',11,0,6), (84,'D',11,4,5),
    (86,'D',11,8,3), (87,'D',11,9,5), (89,'D',11,16,3), (93,'D',12,5,7), (95,'D',12,11,7), (96,'D',12,17,5), (98,'D',12,21,4),
    (101,'D',13,6,6), (104,'D',13,18,7), (108,'D',14,7,3), (110,'D',14,13,6), (112,'D',14,19,6),
    (115,'D',15,3,5), (116,'D',15,8,3), (117,'D',15,16,4), (118,'D',15,20,4),
    (122,'D',16,14,5), (124,'D',16,22,9), (125,'D',16,23,9), (126,'D',16,24,9),
    (128,'D',17,4,4), (130,'D',17,9,6), (131,'D',17,10,4), (133,'D',17,15,8), (135,'D',17,21,8),
    (137,'D',18,7,7), (139,'D',18,12,7), (140,'D',18,17,5),
    (141,'D',19,0,6), (142,'D',19,1,6), (144,'D',19,8,3),
    (150,'D',20,5,5), (151,'D',20,6,5), (152,'D',20,11,5), (154,'D',20,16,4),
    (157,'D',21,3,4), (160,'D',21,13,4), (162,'D',21,18,4), (163,'D',21,19,4),
    (166,'D',22,4,3), (168,'D',22,10,3), (169,'D',22,14,3), (170,'D',22,20,3),
]

# Build entry lookup
entry_map = {}  # (num, dir) -> (row, col, length)
for num, d, r, c, l in ENTRIES:
    entry_map[(num, d)] = (r, c, l)

# Build cell-to-entries lookup
cell_entries = {}  # (row, col) -> [(entry_key, position_in_entry)]
for num, d, r, c, l in ENTRIES:
    for i in range(l):
        if d == 'A':
            cell = (r, c + i)
        else:
            cell = (r + i, c)
        if cell not in cell_entries:
            cell_entries[cell] = []
        cell_entries[cell].append(((num, d), i))

# ============================================================
# GRID STATE
# ============================================================

grid = [[None]*25 for _ in range(25)]
for r, c in BLACK:
    grid[r][c] = '#'

def set_cell(r, c, letter):
    if grid[r][c] is not None and grid[r][c] != letter and grid[r][c] != '#':
        return False  # Conflict
    grid[r][c] = letter
    return True

def get_entry_cells(num, d, r, c, l):
    """Return list of (row, col) for an entry"""
    if d == 'A':
        return [(r, c + i) for i in range(l)]
    else:
        return [(r + i, c) for i in range(l)]

def place_word(word, num, d, r, c, l):
    """Place a word in the grid. Returns True if successful."""
    cells = get_entry_cells(num, d, r, c, l)
    for i, (cr, cc) in enumerate(cells):
        if grid[cr][cc] is not None and grid[cr][cc] != word[i] and grid[cr][cc] != '#':
            return False
    for i, (cr, cc) in enumerate(cells):
        grid[cr][cc] = word[i]
    return True

def get_entry_state(num, d, r, c, l):
    """Get current letters in an entry (None for empty)"""
    cells = get_entry_cells(num, d, r, c, l)
    return [grid[cr][cc] for cr, cc in cells]

def word_fits(word, state):
    """Check if a word fits the current entry state"""
    if len(word) != len(state):
        return False
    for w, s in zip(word, state):
        if s is not None and s != '#' and s != w:
            return False
    return True

# ============================================================
# CONFIRMED ANSWERS DATABASE
# ============================================================

# Already placed (from previous solver)
PLACED = {
    (36, 'A'): 'DORA',
    (37, 'D'): 'ABASH',
    (53, 'D'): 'ROTUNDA',
    (58, 'A'): 'PUSH',
    (66, 'A'): 'HAFT',
    (86, 'D'): 'ZIP',
    (87, 'D'): 'TRITE',
    (88, 'A'): 'ADORN',
    (94, 'A'): 'CIRCLEABOUT',
    (102, 'A'): 'PINTO',
    (109, 'A'): 'TOLEDO',
    (110, 'D'): 'DENVER',
    (121, 'A'): 'TONI',
}

# All confirmed answers grouped by length
ANSWERS_BY_LENGTH = {
    3: ['RAD', 'EAR', 'ION', 'EON', 'ZIP'],
    4: ['DHOW', 'HAFT', 'DORA', 'RACE', 'TONI', 'NOTE', 'PUSH'],
    5: ['ACHOO', 'ABASH', 'OPERA', 'ERASE', 'TRITE', 'ADORN', 'LECAR', 'PINTO', 'TONER',
        'ACCRA', 'DOVER', 'TEMPE'],
    6: ['SCHOOL', 'OHIOAN', 'HOODIE', 'MATTER', 'ECLAIR', 'OPTION', 'ORIENT', 'CHAIRS', 'CONVEX',
        'TOLEDO', 'DENVER', 'REGINA', 'AUBURN', 'OTTAWA'],
    7: ['TYPHOON', 'HEARTED', 'MUSTERS', 'ROTUNDA', 'CALIBER', 'PORTION', 'INUTERO',
        'QUORUMS', 'HIRPLED', 'TORONTO', 'ROSWELL', 'DRESDEN', 'SEVILLE', 'ORLANDO', 'WOODWAY'],
    8: ['HOODWINK', 'HULAHOOP', 'SCENARIO', 'NEUROTIC', 'SCREENER', 'ABSOLUTE', 'TEAMSEAS',
        'DURATION', 'CARBLITE', 'POSITRON', 'ROUTINES', 'CASHTENT', 'FLAMINGO', 'ADELAIDE'],
    9: ['HOOVERDAM', 'ROBINHOOD', 'DITHERING', 'HOWITZERS', 'HIGHHEELS', 'ALLUSIONS', 'RESISTIVE',
        'INUNDATOR', 'CABRIOLET', 'RATPOISON', 'OUTLINERS', 'OWENSBORO', 'ANNAPOLIS', 'ROCHESTER'],
    11: ['CIRCLEABOUT', 'TURNONADIME', 'OUTFORASPIN', 'REVOLUTIONS'],
}

# P9 answers (less certain)
P9_ANSWERS = ['ZIP', 'CHAIRS', 'QUORUMS', 'FLAMINGO', 'PUSH', 'CONVEX', 'HIRPLED']

# P4 cities (definitive)
P4_CITIES = ['TORONTO', 'REGINA', 'OWENSBORO', 'TOLEDO', 'ROSWELL', 'DRESDEN',
             'TEMPE', 'WARSAW', 'ADELAIDE', 'DENVER', 'SEVILLE', 'OTTAWA',
             'ANNAPOLIS', 'AUBURN', 'DOVER', 'ROCHESTER', 'ORLANDO', 'WOODWAY']
# Note: WILMINGTON(10) and SACRAMENTO(10) excluded - no 10-letter slots
# Note: SANJUAN is 7 if no space, or needs to be SAN JUAN as two words - unclear

# ============================================================
# PLACE ALREADY-CONFIRMED ENTRIES
# ============================================================

print("=" * 70)
print("PLACING CONFIRMED ENTRIES")
print("=" * 70)

for (num, d), word in PLACED.items():
    r, c, l = entry_map[(num, d)]
    ok = place_word(word, num, d, r, c, l)
    print(f"  {num}{d}: {word} at ({r},{c}) len={l} → {'OK' if ok else 'CONFLICT!'}")

# ============================================================
# TRY TO PLACE REMAINING ANSWERS
# ============================================================

print("\n" + "=" * 70)
print("TRYING TO PLACE REMAINING ANSWERS")
print("=" * 70)

placed_entries = set(PLACED.keys())
newly_placed = {}

def try_place_answer(word):
    """Try to find unique placement for a word"""
    candidates = []
    for num, d, r, c, l in ENTRIES:
        if (num, d) in placed_entries:
            continue
        if l != len(word):
            continue
        state = get_entry_state(num, d, r, c, l)
        if word_fits(word, state):
            # Check how many letters are constrained (more = better match)
            constrained = sum(1 for s in state if s is not None)
            candidates.append(((num, d), r, c, l, constrained))
    return candidates

# First pass: find answers with unique placements or heavy constraints
all_answers = set()
for length, words in ANSWERS_BY_LENGTH.items():
    for w in words:
        all_answers.add(w)

# Remove already placed
already_placed_words = set(PLACED.values())

changes = True
iteration = 0
while changes:
    changes = False
    iteration += 1
    print(f"\n--- Iteration {iteration} ---")

    # For each unplaced answer, find candidate slots
    for length in sorted(ANSWERS_BY_LENGTH.keys()):
        for word in ANSWERS_BY_LENGTH[length]:
            if word in already_placed_words:
                continue

            candidates = try_place_answer(word)

            # Filter: only keep candidates where word has at least 1 constrained letter matching
            strong_candidates = [c for c in candidates if c[4] > 0]

            if len(strong_candidates) == 1:
                # Unique strong placement
                (num, d), r, c, l, constrained = strong_candidates[0]
                ok = place_word(word, num, d, r, c, l)
                if ok:
                    placed_entries.add((num, d))
                    already_placed_words.add(word)
                    newly_placed[(num, d)] = word
                    print(f"  PLACED {num}{d}: {word} ({constrained} constraints)")
                    changes = True
            elif len(candidates) == 1 and candidates[0][4] == 0:
                # Only one slot of this length... but no constraints
                # Still useful info
                pass

    # Also check: for each unfilled entry, how many answers fit?
    for num, d, r, c, l in ENTRIES:
        if (num, d) in placed_entries:
            continue
        state = get_entry_state(num, d, r, c, l)
        constrained = sum(1 for s in state if s is not None)
        if constrained == 0:
            continue

        fitting = []
        for word in ANSWERS_BY_LENGTH.get(l, []):
            if word in already_placed_words:
                continue
            if word_fits(word, state):
                fitting.append(word)

        if len(fitting) == 1:
            word = fitting[0]
            ok = place_word(word, num, d, r, c, l)
            if ok:
                placed_entries.add((num, d))
                already_placed_words.add(word)
                newly_placed[(num, d)] = word
                print(f"  PLACED {num}{d}: {word} (only answer fitting {constrained} constraints)")
                changes = True
        elif len(fitting) == 0 and constrained > 0:
            state_str = ''.join(s if s else '.' for s in state)
            # print(f"  WARNING: {num}{d} len={l} state={state_str} - NO answers fit!")

# ============================================================
# REPORT: What fits where?
# ============================================================

print("\n" + "=" * 70)
print("CANDIDATE ANALYSIS FOR UNFILLED ENTRIES WITH CONSTRAINTS")
print("=" * 70)

for num, d, r, c, l in ENTRIES:
    if (num, d) in placed_entries:
        continue
    state = get_entry_state(num, d, r, c, l)
    constrained = sum(1 for s in state if s is not None)
    if constrained == 0:
        continue

    state_str = ''.join(s if s else '.' for s in state)
    fitting = []
    for word in ANSWERS_BY_LENGTH.get(l, []):
        if word in already_placed_words:
            continue
        if word_fits(word, state):
            fitting.append(word)

    if fitting:
        print(f"  {num}{d} len={l} [{state_str}]: {fitting}")
    else:
        print(f"  {num}{d} len={l} [{state_str}]: NO confirmed answers fit")

# ============================================================
# PRINT GRID STATE
# ============================================================

print("\n" + "=" * 70)
print("CURRENT GRID STATE")
print("=" * 70)

print("     0123456789012345678901234")
for r in range(25):
    row_str = ""
    for c in range(25):
        if (r, c) in BLACK:
            row_str += "#"
        elif grid[r][c] is not None:
            row_str += grid[r][c]
        else:
            row_str += "."
    print(f"R{r:2d} |{row_str}")

# ============================================================
# THEME ENTRY STATUS
# ============================================================

print("\n" + "=" * 70)
print("THEME ENTRY STATUS")
print("=" * 70)

theme_entries = [
    (25, 'A'), (50, 'A'), (73, 'A'), (94, 'A'), (114, 'A'), (138, 'A'), (167, 'A'),
    (19, 'D'), (78, 'D'),
]

for num, d in theme_entries:
    r, c, l = entry_map[(num, d)]
    state = get_entry_state(num, d, r, c, l)
    state_str = ''.join(s if s else '.' for s in state)
    known = sum(1 for s in state if s is not None)
    print(f"  {num}{d} (len={l}): {state_str}  [{known}/{l} known]")

# ============================================================
# SUMMARY
# ============================================================

total_placed = len(placed_entries)
total_new = len(newly_placed)
print(f"\n{'='*70}")
print(f"SUMMARY: {total_placed} entries placed ({total_new} new this run)")
print(f"{'='*70}")
print(f"\nNewly placed:")
for (num, d), word in sorted(newly_placed.items()):
    print(f"  {num}{d}: {word}")

# Show crossing analysis for theme entries
print(f"\n{'='*70}")
print("CROSSING ENTRIES FOR THEME ENTRIES")
print(f"{'='*70}")

for theme_num, theme_d in theme_entries:
    r, c, l = entry_map[(theme_num, theme_d)]
    if (theme_num, theme_d) in placed_entries:
        continue
    print(f"\n  {theme_num}{theme_d} (len={l}, starts at ({r},{c})):")
    cells = get_entry_cells(theme_num, theme_d, r, c, l)
    for i, (cr, cc) in enumerate(cells):
        crossing = []
        for (entry_key, pos) in cell_entries.get((cr, cc), []):
            if entry_key != (theme_num, theme_d):
                crossing.append((entry_key, pos))
        if grid[cr][cc] is not None:
            print(f"    pos {i:2d} ({cr},{cc}): '{grid[cr][cc]}' ← ", end="")
        else:
            print(f"    pos {i:2d} ({cr},{cc}): '.'  ← ", end="")
        for (ek, ep) in crossing:
            word = PLACED.get(ek) or newly_placed.get(ek)
            if word:
                print(f"{ek[0]}{ek[1]}[{ep}]='{word[ep]}' ", end="")
            else:
                er, ec, el = entry_map[ek]
                st = get_entry_state(ek[0], ek[1], er, ec, el)
                st_str = ''.join(s if s else '.' for s in st)
                print(f"{ek[0]}{ek[1]}(len={el},state={st_str}) ", end="")
        print()
