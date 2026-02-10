#!/usr/bin/env python3
"""
Crossword Solver for MrBeast Million Dollar Puzzle Hunt
Places known answers into the 25×25 grid using entry lengths and crossing constraints.
"""

# ============================================================
# GRID STRUCTURE (from CROSSWORD_GRID_DIGITIZED.md)
# ============================================================

GRID_SIZE = 25

# Black cell positions (row, col)
BLACK_CELLS = {
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

# Across entries: (entry_number, row, col, length)
ACROSS = [
    (1, 0, 0, 7), (8, 0, 9, 6), (14, 0, 17, 8),
    (22, 1, 0, 7), (23, 1, 8, 7), (24, 1, 17, 8),
    (25, 2, 0, 16), (28, 2, 17, 8),
    (29, 3, 0, 4), (30, 3, 5, 5), (31, 3, 11, 3), (32, 3, 15, 5), (34, 3, 21, 4),
    (35, 4, 0, 4), (36, 4, 7, 4), (38, 4, 12, 9), (41, 4, 22, 3),
    (42, 5, 0, 4), (43, 5, 5, 3), (45, 5, 9, 4), (47, 5, 14, 4), (48, 5, 20, 5),
    (50, 6, 0, 16), (54, 6, 17, 6),
    (57, 7, 0, 7), (58, 7, 8, 4), (59, 7, 13, 4), (61, 7, 18, 6),
    (63, 8, 0, 3), (64, 8, 4, 5), (66, 8, 10, 4), (68, 8, 16, 4), (70, 8, 21, 4),
    (72, 9, 3, 6), (73, 9, 11, 14),
    (77, 10, 1, 3), (79, 10, 5, 3), (80, 10, 10, 6), (81, 10, 17, 4), (82, 10, 22, 3),
    (83, 11, 0, 5), (85, 11, 6, 5), (88, 11, 12, 5), (90, 11, 18, 3), (91, 11, 22, 3),
    (92, 12, 0, 6), (94, 12, 7, 11), (97, 12, 19, 6),
    (99, 13, 0, 3), (100, 13, 4, 3), (102, 13, 8, 5), (103, 13, 14, 5), (105, 13, 20, 5),
    (106, 14, 0, 3), (107, 14, 4, 4), (109, 14, 9, 6), (111, 14, 17, 3), (113, 14, 21, 3),
    (114, 15, 0, 14), (117, 15, 16, 6),
    (119, 16, 0, 4), (120, 16, 5, 4), (121, 16, 11, 4), (123, 16, 16, 5), (124, 16, 22, 3),
    (127, 17, 1, 6), (129, 17, 8, 4), (132, 17, 13, 4), (134, 17, 18, 7),
    (136, 18, 2, 6), (138, 18, 9, 16),
    (141, 19, 0, 5), (143, 19, 7, 4), (145, 19, 12, 4), (146, 19, 17, 3), (147, 19, 21, 4),
    (148, 20, 0, 3), (149, 20, 4, 9), (153, 20, 14, 4), (155, 20, 21, 4),
    (156, 21, 0, 4), (158, 21, 5, 5), (159, 21, 11, 3), (161, 21, 15, 5), (164, 21, 21, 4),
    (165, 22, 0, 8), (167, 22, 9, 16),
    (171, 23, 0, 8), (172, 23, 10, 7), (173, 23, 18, 7),
    (174, 24, 0, 8), (175, 24, 10, 6), (176, 24, 18, 7),
]

# Down entries: (entry_number, row, col, length)
DOWN = [
    (1, 0, 0, 9), (2, 0, 1, 9), (3, 0, 2, 9), (4, 0, 3, 8), (5, 0, 4, 3), (6, 0, 5, 4), (7, 0, 6, 4),
    (8, 0, 9, 8), (9, 0, 10, 3), (10, 0, 11, 4), (11, 0, 12, 7), (12, 0, 13, 5), (13, 0, 14, 3),
    (14, 0, 17, 7), (15, 0, 18, 5), (16, 0, 19, 5), (17, 0, 20, 3), (18, 0, 21, 4), (19, 0, 22, 15), (20, 0, 23, 6), (21, 0, 24, 6),
    (23, 1, 8, 4), (26, 2, 7, 5), (27, 2, 15, 6),
    (33, 3, 16, 3), (37, 4, 10, 5), (39, 4, 14, 4), (40, 4, 20, 4),
    (43, 5, 5, 6), (44, 5, 6, 7), (46, 5, 11, 6), (49, 5, 21, 5),
    (51, 6, 4, 4), (52, 6, 8, 4), (53, 6, 13, 7), (55, 6, 18, 6), (56, 6, 19, 7),
    (60, 7, 16, 3), (62, 7, 23, 8),
    (65, 8, 7, 5), (67, 8, 12, 9), (69, 8, 17, 3), (71, 8, 24, 6),
    (72, 9, 3, 4), (74, 9, 14, 6), (75, 9, 15, 5), (76, 9, 20, 5),
    (77, 10, 1, 8), (78, 10, 2, 15), (80, 10, 10, 6), (83, 11, 0, 6),
    (84, 11, 4, 5), (86, 11, 8, 3), (87, 11, 9, 5), (89, 11, 16, 3),
    (93, 12, 5, 7), (95, 12, 11, 7), (96, 12, 17, 5), (98, 12, 21, 4),
    (101, 13, 6, 6), (104, 13, 18, 7), (108, 14, 7, 3),
    (110, 14, 13, 6), (112, 14, 19, 6),
    (115, 15, 3, 5), (116, 15, 8, 3), (117, 15, 16, 4), (118, 15, 20, 4),
    (122, 16, 14, 5), (124, 16, 22, 9), (125, 16, 23, 9), (126, 16, 24, 9),
    (128, 17, 4, 4), (130, 17, 9, 6), (131, 17, 10, 4), (133, 17, 15, 8),
    (135, 17, 21, 8), (137, 18, 7, 7), (139, 18, 12, 7), (140, 18, 17, 5),
    (141, 19, 0, 6), (142, 19, 1, 6), (144, 19, 8, 3), (150, 20, 5, 5), (151, 20, 6, 5),
    (152, 20, 11, 5), (154, 20, 16, 4), (157, 21, 3, 4), (160, 21, 13, 4),
    (162, 21, 18, 4), (163, 21, 19, 4), (166, 22, 4, 3), (168, 22, 10, 3),
    (169, 22, 14, 3), (170, 22, 20, 3),
]

# Build lookup: entry_num -> (direction, row, col, length)
ALL_ENTRIES = {}
for num, row, col, length in ACROSS:
    key = f"{num}A"
    ALL_ENTRIES[key] = ('A', row, col, length)
for num, row, col, length in DOWN:
    key = f"{num}D"
    ALL_ENTRIES[key] = ('D', row, col, length)

# ============================================================
# KNOWN ANSWERS (from MASTER_CROSSWORD_ANSWERS.md)
# ============================================================

# P1: H2O words (13 answers, no entry numbers assigned yet)
P1_ANSWERS = {
    "ACHOO": 5, "TYPHOON": 7, "SCHOOL": 6, "HOODWINK": 8, "OHSHOOT": 7,
    "OHIOAN": 6, "HULAHOOP": 8, "HOODIE": 6, "HOOVERDAM": 9, "DHOW": 4,
    "ROBINHOOD": 9, "WAHOO": 5,
    # "HOOPLA": 6, or "VOODOO": 6  -- uncertain
}

# P3: Beach cleanup (19 answers, no entry numbers)
P3_ANSWERS = {
    "HAFT": 4, "DITHERING": 9, "HOWITZERS": 9, "SCENARIO": 8, "ABASH": 5,
    "NEUROTIC": 8, "HEARTED": 7, "HIGHHEELS": 9, "SCREENER": 8,
    "INTRODUCTIONS": 13, "MATTER": 6, "OPERA": 5, "ALLUSIONS": 9,
    "RESISTIVE": 9, "ABSOLUTE": 8, "ERASE": 5, "TEAMSEAS": 8,
    "TRITE": 5, "MUSTERS": 7,
}

# P8: Pyramid entries (39 answers, no entry numbers)
P8_ANSWERS = {
    # A-pyramid (9, excluding AROUND)
    "RA": 2, "RAD": 3, "DORA": 4, "ADORN": 5, "ROTUNDA": 7, "DURATION": 8,
    "INUNDATOR": 9, "TRADEUNION": 10, "TURNONADIME": 11,
    # E-pyramid (10)
    "ER": 2, "EAR": 3, "RACE": 4, "LECAR": 5, "ECLAIR": 6, "CALIBER": 7,
    "CARBLITE": 8, "CABRIOLET": 9, "ORBICULATE": 10, "CIRCLEABOUT": 11,
    # I-pyramid (10)
    "OI": 2, "ION": 3, "TONI": 4, "PINTO": 5, "OPTION": 6, "PORTION": 7,
    "POSITRON": 8, "RATPOISON": 9, "STAINPROOF": 10, "OUTFORASPIN": 11,
    # O-pyramid (10)
    "NO": 2, "EON": 3, "NOTE": 4, "TONER": 5, "ORIENT": 6, "INUTERO": 7,
    "ROUTINES": 8, "OUTLINERS": 9, "RESOLUTION": 10, "REVOLUTIONS": 11,
}

# P9: Circle hidden words (9 answers, lower confidence)
P9_ANSWERS = {
    "ZIP": 3, "CHAIRS": 6, "QUORUMS": 7, "FLAMINGO": 8, "PUSH": 4,
    "CONVEX": 6, "HIRPLED": 7,
    # "OF": 2, "WE": 2  -- too short, excluded
}

# Video puzzle answers
VIDEO_ANSWERS = {
    "CONTRADICTION": 13,  # HIGH confidence
    "CASHTENT": 8,        # MEDIUM
}

# P4: City names (21 cities - likely crossword entries)
P4_CITIES = {
    "TORONTO": 7, "REGINA": 6, "OWENSBORO": 9, "TOLEDO": 6, "ROSWELL": 7,
    "DRESDEN": 7, "TEMPE": 5, "WARSAW": 6, "SANJUAN": 7, "ADELAIDE": 8,
    "DENVER": 6, "SEVILLE": 7, "OTTAWA": 6, "WILMINGTON": 10, "SACRAMENTO": 10,
    "ANNAPOLIS": 9, "AUBURN": 6, "DOVER": 5, "ROCHESTER": 9, "ORLANDO": 7, "WOODWAY": 7,
}

# Combine all answers into one pool
ALL_ANSWERS = {}
for pool_name, pool in [("P1", P1_ANSWERS), ("P3", P3_ANSWERS), ("P8", P8_ANSWERS),
                         ("P9", P9_ANSWERS), ("VIDEO", VIDEO_ANSWERS), ("P4", P4_CITIES)]:
    for word, length in pool.items():
        ALL_ANSWERS[word] = (length, pool_name)

# ============================================================
# BUILD CROSSING MAP
# ============================================================

def get_cells(direction, row, col, length):
    """Return list of (row, col) for an entry."""
    if direction == 'A':
        return [(row, col + i) for i in range(length)]
    else:
        return [(row + i, col) for i in range(length)]

# Build cell -> entry mappings
cell_to_across = {}  # (row,col) -> (entry_key, position_in_entry)
cell_to_down = {}

for num, row, col, length in ACROSS:
    key = f"{num}A"
    for i in range(length):
        cell_to_across[(row, col+i)] = (key, i)

for num, row, col, length in DOWN:
    key = f"{num}D"
    for i in range(length):
        cell_to_down[(row+i, col)] = (key, i)

# Build crossing pairs: for each cell that has both across and down
crossings = []  # (across_key, across_pos, down_key, down_pos)
for cell in cell_to_across:
    if cell in cell_to_down:
        ak, ap = cell_to_across[cell]
        dk, dp = cell_to_down[cell]
        crossings.append((ak, ap, dk, dp))

print(f"Total crossings: {len(crossings)}")

# ============================================================
# MATCH ANSWERS TO ENTRIES BY LENGTH
# ============================================================

# Build length -> entries mapping
length_to_across = {}
length_to_down = {}
length_to_all = {}

for num, row, col, length in ACROSS:
    length_to_across.setdefault(length, []).append(f"{num}A")
    length_to_all.setdefault(length, []).append(f"{num}A")

for num, row, col, length in DOWN:
    length_to_down.setdefault(length, []).append(f"{num}D")
    length_to_all.setdefault(length, []).append(f"{num}D")

print("\n=== ENTRY LENGTH DISTRIBUTION ===")
for l in sorted(length_to_all.keys()):
    entries = length_to_all[l]
    print(f"  Length {l:2d}: {len(entries)} entries -> {', '.join(entries)}")

# Match each answer to possible entries by length
print("\n=== ANSWER TO POSSIBLE ENTRIES ===")
answer_candidates = {}
for word, (length, source) in sorted(ALL_ANSWERS.items(), key=lambda x: -x[1][0]):
    possible = length_to_all.get(length, [])
    answer_candidates[word] = possible
    if len(possible) <= 5:
        print(f"  {word:20s} (len={length:2d}, {source:6s}) -> {possible}")

# ============================================================
# UNIQUE LENGTH MATCHES (only one entry of that length)
# ============================================================

print("\n=== UNIQUE LENGTH PLACEMENTS ===")
grid = {}  # (row, col) -> letter
placements = {}  # entry_key -> word

def place_word(entry_key, word):
    """Place a word in the grid. Returns True if consistent, False if conflict."""
    d, row, col, length = ALL_ENTRIES[entry_key]
    if len(word) != length:
        return False
    cells = get_cells(d, row, col, length)
    for i, (r, c) in enumerate(cells):
        if (r, c) in grid:
            if grid[(r, c)] != word[i]:
                return False  # Conflict!
    # No conflicts, place it
    for i, (r, c) in enumerate(cells):
        grid[(r, c)] = word[i]
    placements[entry_key] = word
    return True

# Find unique-length answers
unique_placements = []
for word, possible in answer_candidates.items():
    if len(possible) == 1:
        entry_key = possible[0]
        length = ALL_ANSWERS[word][0]
        _, row, col, elen = ALL_ENTRIES[entry_key]
        if elen == length:
            unique_placements.append((word, entry_key))

for word, entry_key in unique_placements:
    d, row, col, length = ALL_ENTRIES[entry_key]
    ok = place_word(entry_key, word)
    status = "PLACED" if ok else "CONFLICT"
    print(f"  {status}: {word} -> {entry_key} at ({row},{col})")

# ============================================================
# THEME ENTRIES (longest across entries)
# ============================================================

print("\n=== THEME ENTRY ANALYSIS ===")
theme_candidates = [(n, r, c, l) for n, r, c, l in ACROSS if l >= 10]
theme_candidates.sort(key=lambda x: -x[3])

for num, row, col, length in theme_candidates:
    key = f"{num}A"
    print(f"\n  {key}: Length {length} at row {row}, cols {col}-{col+length-1}")
    # Find which answers could fit
    matching = [w for w, (wl, src) in ALL_ANSWERS.items() if wl == length]
    if matching:
        print(f"    Possible answers: {matching}")
    if key in placements:
        placed = placements[key]
        print(f"    PLACED: {placed}")
        # Look for hidden location names
        for loc_len in range(3, length+1):
            for start in range(length - loc_len + 1):
                substring = placed[start:start+loc_len]
                # Check if it's a known city/location
                if substring in P4_CITIES:
                    print(f"    ** HIDDEN LOCATION: {substring} at positions {start}-{start+loc_len-1}")

# Also check down theme entries
theme_down = [(n, r, c, l) for n, r, c, l in DOWN if l >= 10]
for num, row, col, length in sorted(theme_down, key=lambda x: -x[3]):
    key = f"{num}D"
    print(f"\n  {key}: Length {length} at col {col}, rows {row}-{row+length-1}")
    matching = [w for w, (wl, src) in ALL_ANSWERS.items() if wl == length]
    if matching:
        print(f"    Possible answers: {matching}")

# ============================================================
# CROSSING CONSTRAINT PROPAGATION
# ============================================================

print("\n=== CROSSING CONSTRAINT ANALYSIS ===")

# For placed words, check what constraints they impose on crossing entries
for entry_key, word in sorted(placements.items()):
    d, row, col, length = ALL_ENTRIES[entry_key]
    cells = get_cells(d, row, col, length)
    for i, (r, c) in enumerate(cells):
        letter = word[i]
        # Find crossing entry
        if d == 'A' and (r, c) in cell_to_down:
            dk, dp = cell_to_down[(r, c)]
            if dk not in placements:
                _, dr, dc, dl = ALL_ENTRIES[dk]
                # Find answers that could go here with this letter at position dp
                candidates = [w for w, (wl, src) in ALL_ANSWERS.items()
                             if wl == dl and w[dp] == letter and w not in placements.values()]
                if candidates and len(candidates) <= 3:
                    print(f"  {dk} (len={dl}): position {dp}={letter} (from {entry_key}={word}) -> candidates: {candidates}")
        elif d == 'D' and (r, c) in cell_to_across:
            ak, ap = cell_to_across[(r, c)]
            if ak not in placements:
                _, ar, ac, al = ALL_ENTRIES[ak]
                candidates = [w for w, (wl, src) in ALL_ANSWERS.items()
                             if wl == al and w[ap] == letter and w not in placements.values()]
                if candidates and len(candidates) <= 3:
                    print(f"  {ak} (len={al}): position {ap}={letter} (from {entry_key}={word}) -> candidates: {candidates}")

# ============================================================
# MULTI-CANDIDATE LENGTH MATCHING WITH CROSSING
# ============================================================

print("\n=== CONSTRAINT-BASED PLACEMENT (multi-candidate) ===")

# For each unplaced answer, find which entries it could fit considering crossings
def check_word_at_entry(word, entry_key):
    """Check if word is consistent with all currently placed grid letters."""
    d, row, col, length = ALL_ENTRIES[entry_key]
    if len(word) != length:
        return False
    cells = get_cells(d, row, col, length)
    for i, (r, c) in enumerate(cells):
        if (r, c) in grid and grid[(r, c)] != word[i]:
            return False
    return True

unplaced_answers = {w: info for w, info in ALL_ANSWERS.items()
                    if w not in [placements[k] for k in placements]}
unplaced_entries = {k: ALL_ENTRIES[k] for k in ALL_ENTRIES if k not in placements}

# Try to narrow down placements
new_placements = True
iteration = 0
while new_placements:
    iteration += 1
    new_placements = False
    print(f"\n--- Iteration {iteration} ---")

    # For each unplaced entry, find which unplaced answers fit
    for entry_key in sorted(unplaced_entries.keys()):
        d, row, col, length = unplaced_entries[entry_key]
        fitting = []
        for word, (wlen, src) in unplaced_answers.items():
            if wlen == length and check_word_at_entry(word, entry_key):
                fitting.append(word)

        if len(fitting) == 1:
            word = fitting[0]
            ok = place_word(entry_key, word)
            if ok:
                print(f"  PLACED (sole fit): {word} -> {entry_key}")
                del unplaced_entries[entry_key]
                del unplaced_answers[word]
                new_placements = True

    # For each unplaced answer, find which unplaced entries it could go in
    for word in list(unplaced_answers.keys()):
        wlen, src = unplaced_answers[word]
        fitting_entries = []
        for entry_key in unplaced_entries:
            d, row, col, length = unplaced_entries[entry_key]
            if length == wlen and check_word_at_entry(word, entry_key):
                fitting_entries.append(entry_key)

        if len(fitting_entries) == 1:
            entry_key = fitting_entries[0]
            ok = place_word(entry_key, word)
            if ok:
                print(f"  PLACED (sole slot): {word} -> {entry_key}")
                del unplaced_entries[entry_key]
                del unplaced_answers[word]
                new_placements = True

# ============================================================
# RESULTS SUMMARY
# ============================================================

print(f"\n{'='*60}")
print(f"PLACEMENT RESULTS")
print(f"{'='*60}")
print(f"Total placed: {len(placements)} / 176")
print(f"Unplaced answers remaining: {len(unplaced_answers)}")
print(f"Unfilled entries remaining: {len(unplaced_entries)}")

print(f"\n=== PLACED ENTRIES ===")
for key in sorted(placements.keys(), key=lambda k: int(k[:-1])):
    word = placements[key]
    d, row, col, length = ALL_ENTRIES[key]
    print(f"  {key:6s}: {word:20s} at ({row:2d},{col:2d}) len={length}")

print(f"\n=== REMAINING UNPLACED ANSWERS ===")
for word in sorted(unplaced_answers.keys()):
    wlen, src = unplaced_answers[word]
    possible_entries = [k for k in unplaced_entries if ALL_ENTRIES[k][3] == wlen]
    n_possible = len(possible_entries)
    consistent = [k for k in possible_entries if check_word_at_entry(word, k)]
    print(f"  {word:20s} (len={wlen:2d}, {src:6s}) -> {len(consistent)} possible entries" +
          (f": {consistent}" if len(consistent) <= 5 else ""))

# ============================================================
# PRINT FILLED GRID
# ============================================================

print(f"\n=== CURRENT GRID STATE ===")
print("     " + "".join(f"{i%10}" for i in range(25)))
for r in range(25):
    row_str = f"R{r:2d}| "
    for c in range(25):
        if (r, c) in BLACK_CELLS:
            row_str += "#"
        elif (r, c) in grid:
            row_str += grid[(r, c)]
        else:
            row_str += "."
    print(row_str)

# ============================================================
# HIDDEN LOCATION ANALYSIS
# ============================================================

print(f"\n=== HIDDEN LOCATION NAME SEARCH ===")
print("The 9-word sentence says: EVERY CHALLENGE LEADS TOWARDS LOCATION NAME SOMEWHERE AROUND WORLD")
print("167 Across: 'What this puzzle commemorates in eleven hidden words in the theme entries'")
print("\nSearching placed theme entries for hidden location names...")

# Known world locations to search for (subset)
LOCATIONS = [
    # Major cities & countries
    "ACCRA", "TOKYO", "LONDON", "PARIS", "ROME", "BERLIN", "CAIRO", "LIMA", "OSLO",
    "ADEN", "BALI", "FIJI", "GUAM", "IRAN", "IRAQ", "LAOS", "MALI", "OMAN", "PERU",
    "CUBA", "CHAD", "TOGO", "NIGER", "NEPAL", "QATAR", "KOREA", "CHINA", "JAPAN",
    "INDIA", "SPAIN", "ITALY", "FRANCE", "BRAZIL", "CHILE", "NAURU", "PALAU", "SAMOA",
    "TONGA", "KENYA", "GHANA", "BENIN", "GABON", "SUDAN", "LIBYA", "SYRIA", "YEMEN",
    "ARUBA", "HAITI", "BELIZE",
    # Cities from P4
    "TORONTO", "REGINA", "TOLEDO", "ROSWELL", "DRESDEN", "TEMPE", "WARSAW",
    "DENVER", "SEVILLE", "OTTAWA", "DOVER", "ORLANDO", "AUBURN",
    # More locations
    "TAIPEI", "SEOUL", "DHAKA", "HANOI", "MANILA", "BOGOTA", "QUITO", "DAKAR",
    "RABAT", "TUNIS", "MINSK", "SOFIA", "PRAGUE", "VIENNA", "LISBON", "DUBLIN",
    "ATHENS", "MOSCOW", "CAIRO", "RIYADH", "DOHA", "MUSCAT", "KABUL", "TEHRAN",
    "LAGOS", "ABUJA", "CAPE", "NICE", "LYON", "BONN",
]

for entry_key, word in sorted(placements.items(), key=lambda x: -ALL_ENTRIES[x[0]][3]):
    d, row, col, length = ALL_ENTRIES[entry_key]
    if length >= 8:  # Only check longer entries
        found = []
        for loc in LOCATIONS:
            if loc in word:
                found.append(loc)
        if found:
            print(f"  {entry_key} = {word}: FOUND {found}")

# Also check for locations spanning across adjacent theme entries
print("\nAlso searching all filled rows for hidden location names...")
for r in range(25):
    row_letters = ""
    for c in range(25):
        if (r, c) in grid:
            row_letters += grid[(r, c)]
        elif (r, c) in BLACK_CELLS:
            row_letters += " "
        else:
            row_letters += "?"
    for loc in LOCATIONS:
        if loc in row_letters:
            print(f"  Row {r}: Found '{loc}' in '{row_letters.strip()}'")

print("\n=== P4 CITY PLACEMENT ANALYSIS ===")
print("P4 cities are likely crossword entries (location names as answers)")
for city, clen in sorted(P4_CITIES.items()):
    possible = [k for k in ALL_ENTRIES if ALL_ENTRIES[k][3] == clen and k not in placements]
    consistent = [k for k in possible if check_word_at_entry(city, k)]
    if consistent:
        print(f"  {city:12s} (len={clen}) could go at: {consistent}")
    elif not possible:
        print(f"  {city:12s} (len={clen}) -> NO entries of this length left!")
    else:
        print(f"  {city:12s} (len={clen}) -> {len(possible)} entries of right length, {len(consistent)} consistent with grid")
