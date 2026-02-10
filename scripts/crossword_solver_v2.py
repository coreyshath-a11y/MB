#!/usr/bin/env python3
"""
Crossword Solver v2 - Enhanced with backtracking for multi-candidate slots
Tests all 4 length-11 candidates at 94A and propagates constraints.
"""

# ============================================================
# GRID STRUCTURE (from CROSSWORD_GRID_DIGITIZED.md)
# ============================================================

GRID_SIZE = 25

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

ALL_ENTRIES = {}
for num, row, col, length in ACROSS:
    ALL_ENTRIES[f"{num}A"] = ('A', row, col, length)
for num, row, col, length in DOWN:
    ALL_ENTRIES[f"{num}D"] = ('D', row, col, length)

# ============================================================
# ANSWERS (only those with matching grid lengths)
# ============================================================

# All confirmed answers with sources
ALL_ANSWERS_RAW = {
    # P1 (H2O words)
    "ACHOO": (5, "P1"), "TYPHOON": (7, "P1"), "SCHOOL": (6, "P1"),
    "HOODWINK": (8, "P1"), "OHSHOOT": (7, "P1"), "OHIOAN": (6, "P1"),
    "HULAHOOP": (8, "P1"), "HOODIE": (6, "P1"), "HOOVERDAM": (9, "P1"),
    "DHOW": (4, "P1"), "ROBINHOOD": (9, "P1"), "WAHOO": (5, "P1"),
    # P3 (Beach)
    "HAFT": (4, "P3"), "DITHERING": (9, "P3"), "HOWITZERS": (9, "P3"),
    "SCENARIO": (8, "P3"), "ABASH": (5, "P3"), "NEUROTIC": (8, "P3"),
    "HEARTED": (7, "P3"), "HIGHHEELS": (9, "P3"), "SCREENER": (8, "P3"),
    "INTRODUCTIONS": (13, "P3"), "MATTER": (6, "P3"), "OPERA": (5, "P3"),
    "ALLUSIONS": (9, "P3"), "RESISTIVE": (9, "P3"), "ABSOLUTE": (8, "P3"),
    "ERASE": (5, "P3"), "TEAMSEAS": (8, "P3"), "TRITE": (5, "P3"), "MUSTERS": (7, "P3"),
    # P8 (Pyramids) - only lengths that exist in grid (3-9, 11)
    "RAD": (3, "P8"), "EAR": (3, "P8"), "ION": (3, "P8"), "EON": (3, "P8"),
    "DORA": (4, "P8"), "RACE": (4, "P8"), "TONI": (4, "P8"), "NOTE": (4, "P8"),
    "ADORN": (5, "P8"), "LECAR": (5, "P8"), "PINTO": (5, "P8"), "TONER": (5, "P8"),
    "ECLAIR": (6, "P8"), "OPTION": (6, "P8"), "ORIENT": (6, "P8"),
    "ROTUNDA": (7, "P8"), "CALIBER": (7, "P8"), "PORTION": (7, "P8"), "INUTERO": (7, "P8"),
    "DURATION": (8, "P8"), "CARBLITE": (8, "P8"), "POSITRON": (8, "P8"), "ROUTINES": (8, "P8"),
    "INUNDATOR": (9, "P8"), "CABRIOLET": (9, "P8"), "RATPOISON": (9, "P8"), "OUTLINERS": (9, "P8"),
    "TURNONADIME": (11, "P8"), "CIRCLEABOUT": (11, "P8"), "OUTFORASPIN": (11, "P8"), "REVOLUTIONS": (11, "P8"),
    # P9 (Circle)
    "ZIP": (3, "P9"), "CHAIRS": (6, "P9"), "QUORUMS": (7, "P9"),
    "FLAMINGO": (8, "P9"), "PUSH": (4, "P9"), "CONVEX": (6, "P9"), "HIRPLED": (7, "P9"),
    # Video
    "CASHTENT": (8, "VIDEO"),
    # P4 cities (likely entries)
    "TORONTO": (7, "P4"), "REGINA": (6, "P4"), "OWENSBORO": (9, "P4"),
    "TOLEDO": (6, "P4"), "ROSWELL": (7, "P4"), "DRESDEN": (7, "P4"),
    "TEMPE": (5, "P4"), "WARSAW": (6, "P4"), "SANJUAN": (7, "P4"),
    "ADELAIDE": (8, "P4"), "DENVER": (6, "P4"), "SEVILLE": (7, "P4"),
    "OTTAWA": (6, "P4"), "ANNAPOLIS": (9, "P4"), "AUBURN": (6, "P4"),
    "DOVER": (5, "P4"), "ROCHESTER": (9, "P4"), "ORLANDO": (7, "P4"), "WOODWAY": (7, "P4"),
}

# Filter to only answers that have matching grid entry lengths
valid_lengths = set()
for key, (d, r, c, l) in ALL_ENTRIES.items():
    valid_lengths.add(l)

ALL_ANSWERS = {}
excluded = []
for word, (length, src) in ALL_ANSWERS_RAW.items():
    if length in valid_lengths:
        ALL_ANSWERS[word] = (length, src)
    else:
        excluded.append((word, length, src))

print(f"Valid grid lengths: {sorted(valid_lengths)}")
print(f"Total answers with valid lengths: {len(ALL_ANSWERS)}")
print(f"EXCLUDED (no matching grid slots):")
for word, length, src in sorted(excluded, key=lambda x: -x[1]):
    print(f"  {word:20s} len={length:2d} ({src})")

# ============================================================
# HELPERS
# ============================================================

def get_cells(direction, row, col, length):
    if direction == 'A':
        return [(row, col + i) for i in range(length)]
    else:
        return [(row + i, col) for i in range(length)]

cell_to_across = {}
cell_to_down = {}
for num, row, col, length in ACROSS:
    key = f"{num}A"
    for i in range(length):
        cell_to_across[(row, col+i)] = (key, i)
for num, row, col, length in DOWN:
    key = f"{num}D"
    for i in range(length):
        cell_to_down[(row+i, col)] = (key, i)

def solve_with_seed(seed_entry, seed_word, all_answers):
    """Place seed_word at seed_entry, then propagate constraints. Returns (placements, grid)."""
    grid = {}
    placements = {}
    available_answers = dict(all_answers)

    def place_word(entry_key, word):
        d, row, col, length = ALL_ENTRIES[entry_key]
        if len(word) != length:
            return False
        cells = get_cells(d, row, col, length)
        for i, (r, c) in enumerate(cells):
            if (r, c) in grid and grid[(r, c)] != word[i]:
                return False
        for i, (r, c) in enumerate(cells):
            grid[(r, c)] = word[i]
        placements[entry_key] = word
        if word in available_answers:
            del available_answers[word]
        return True

    def check_word_at_entry(word, entry_key):
        d, row, col, length = ALL_ENTRIES[entry_key]
        if len(word) != length:
            return False
        cells = get_cells(d, row, col, length)
        for i, (r, c) in enumerate(cells):
            if (r, c) in grid and grid[(r, c)] != word[i]:
                return False
        return True

    # Place seed
    if not place_word(seed_entry, seed_word):
        return placements, grid

    # Iterative constraint propagation
    changed = True
    while changed:
        changed = False
        unplaced_entries = {k: ALL_ENTRIES[k] for k in ALL_ENTRIES if k not in placements}

        # For each unplaced entry, find fitting answers
        for entry_key in sorted(unplaced_entries.keys()):
            d, row, col, length = unplaced_entries[entry_key]
            fitting = [w for w, (wl, _) in available_answers.items()
                      if wl == length and check_word_at_entry(w, entry_key)]
            if len(fitting) == 1:
                if place_word(entry_key, fitting[0]):
                    changed = True

        # For each unplaced answer, find fitting entries
        for word in list(available_answers.keys()):
            wlen, _ = available_answers[word]
            fitting_entries = [k for k in unplaced_entries
                             if ALL_ENTRIES[k][3] == wlen and check_word_at_entry(word, k)]
            if len(fitting_entries) == 1:
                if place_word(fitting_entries[0], word):
                    changed = True

    return placements, grid

# ============================================================
# TEST ALL 4 LENGTH-11 CANDIDATES AT 94A
# ============================================================

print(f"\n{'='*60}")
print("TESTING ALL 4 LENGTH-11 CANDIDATES AT 94A")
print(f"{'='*60}")

candidates_11 = ["TURNONADIME", "CIRCLEABOUT", "OUTFORASPIN", "REVOLUTIONS"]
best_result = None
best_count = 0

for candidate in candidates_11:
    answers_copy = {w: info for w, info in ALL_ANSWERS.items() if w != candidate or w == candidate}
    placements, grid = solve_with_seed("94A", candidate, ALL_ANSWERS)
    count = len(placements)
    print(f"\n--- 94A = {candidate} ---")
    print(f"  Total placed: {count}")
    for k in sorted(placements.keys(), key=lambda x: int(x[:-1])):
        d, r, c, l = ALL_ENTRIES[k]
        print(f"    {k:6s} = {placements[k]:20s} at ({r:2d},{c:2d})")

    if count > best_count:
        best_count = count
        best_result = (candidate, placements, grid)

# ============================================================
# BEST RESULT
# ============================================================

print(f"\n{'='*60}")
print(f"BEST: 94A = {best_result[0]} with {best_count} placements")
print(f"{'='*60}")

placements = best_result[1]
grid = best_result[2]

# Print the best grid
print(f"\n=== BEST GRID STATE ===")
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
# AMBIGUOUS ENTRIES ANALYSIS
# ============================================================

print(f"\n=== MULTI-CANDIDATE ANALYSIS ===")
print("Entries where multiple known answers fit (considering grid constraints):")

unplaced_entries = {k: ALL_ENTRIES[k] for k in ALL_ENTRIES if k not in placements}
available = {w: info for w, info in ALL_ANSWERS.items() if w not in placements.values()}

def check_word_grid(word, entry_key, grid):
    d, row, col, length = ALL_ENTRIES[entry_key]
    if len(word) != length:
        return False
    cells = get_cells(d, row, col, length)
    for i, (r, c) in enumerate(cells):
        if (r, c) in grid and grid[(r, c)] != word[i]:
            return False
    return True

# Group by entry - which answers could go where
entry_candidates = {}
for entry_key in sorted(unplaced_entries.keys()):
    d, row, col, length = ALL_ENTRIES[entry_key]
    fitting = [(w, src) for w, (wl, src) in available.items()
               if wl == length and check_word_grid(w, entry_key, grid)]
    if fitting:
        entry_candidates[entry_key] = fitting

# Show entries with few candidates (most constrained)
for entry_key in sorted(entry_candidates.keys(), key=lambda k: len(entry_candidates[k])):
    cands = entry_candidates[entry_key]
    if len(cands) <= 5:
        d, r, c, l = ALL_ENTRIES[entry_key]
        words = [f"{w}({s})" for w, s in cands]
        print(f"  {entry_key:6s} (len={l}, at ({r},{c})): {', '.join(words)}")

# ============================================================
# THEME ENTRIES - WHAT FITS?
# ============================================================

print(f"\n=== THEME ENTRY CANDIDATES ===")
print("These are the longest entries that could contain hidden location names.")
print("167A asks: 'What this puzzle commemorates in eleven hidden words in the theme entries'")

theme_nums = [25, 50, 73, 114, 138, 167]  # Across theme entries
for num in theme_nums:
    key = f"{num}A"
    d, r, c, l = ALL_ENTRIES[key]
    print(f"\n  {key}: Length {l} at row {r}, cols {c}-{c+l-1}")
    if key in placements:
        print(f"    PLACED: {placements[key]}")
    else:
        # What partial letters do we know from crossings?
        cells = get_cells('A', r, c, l)
        partial = ""
        known_count = 0
        for i, (cr, cc) in enumerate(cells):
            if (cr, cc) in grid:
                partial += grid[(cr, cc)]
                known_count += 1
            else:
                partial += "."
        print(f"    Partial: {partial} ({known_count}/{l} known)")

# Also check down theme entries
for num_d in [19, 78]:
    key = f"{num_d}D"
    d, r, c, l = ALL_ENTRIES[key]
    print(f"\n  {key}: Length {l} at col {c}, rows {r}-{r+l-1}")
    cells = get_cells('D', r, c, l)
    partial = ""
    known_count = 0
    for i, (cr, cc) in enumerate(cells):
        if (cr, cc) in grid:
            partial += grid[(cr, cc)]
            known_count += 1
        else:
            partial += "."
    print(f"    Partial: {partial} ({known_count}/{l} known)")

# ============================================================
# STATISTICS
# ============================================================

print(f"\n=== FINAL STATISTICS ===")
print(f"Entries placed: {len(placements)} / 176")
placed_by_source = {}
for word in placements.values():
    if word in ALL_ANSWERS_RAW:
        src = ALL_ANSWERS_RAW[word][1]
    else:
        src = "UNKNOWN"
    placed_by_source[src] = placed_by_source.get(src, 0) + 1
for src in sorted(placed_by_source.keys()):
    print(f"  {src}: {placed_by_source[src]} placed")

print(f"\nAnswers that CANNOT fit in grid (wrong length):")
print(f"  Length 2 (no slots): RA, ER, OI, NO")
print(f"  Length 10 (no slots): TRADEUNION, ORBICULATE, STAINPROOF, RESOLUTION, WILMINGTON, SACRAMENTO")
print(f"  Length 11 (only 1 slot): 3 of 4 P8 answers excluded")
print(f"  Length 13 (no slots): INTRODUCTIONS, CONTRADICTION")
print(f"  TOTAL EXCLUDED: ~15 answers")
print(f"  -> These may be CLUES rather than ANSWERS, or entries in a different puzzle structure")
