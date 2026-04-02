#!/usr/bin/env python3
"""
Brute-force test of ALL FOUR 94A candidates and their cascading effects.
Grid: 25x25 crossword.
94A is at row 12, cols 7-17 (11 letters).
"""

import re
from collections import defaultdict

# ── Answer bank by length ──────────────────────────────────────────────
answers = {
    3: ['RAD', 'EAR', 'ION', 'EON', 'ZIP'],
    4: ['DHOW', 'HAFT', 'DORA', 'RACE', 'TONI', 'NOTE', 'PUSH'],
    5: ['ACHOO', 'WAHOO', 'ABASH', 'OPERA', 'ERASE', 'TRITE', 'ADORN', 'LECAR', 'PINTO', 'TONER', 'ACCRA', 'WORLD'],
    6: ['SCHOOL', 'OHIOAN', 'HOODIE', 'MATTER', 'ECLAIR', 'OPTION', 'ORIENT', 'CHAIRS', 'CONVEX', 'TOLEDO', 'REGINA', 'AUBURN', 'DENVER', 'OTTAWA', 'DOVER'],  # DOVER is len 5, fix below
    7: ['TYPHOON', 'OHSHOOT', 'HEARTED', 'MUSTERS', 'ROTUNDA', 'CALIBER', 'PORTION', 'INUTERO', 'QUORUMS', 'HIRPLED', 'TORONTO', 'ROSWELL', 'DRESDEN', 'ORLANDO', 'WOODWAY', 'SANJUAN'],
    8: ['HOODWINK', 'HULAHOOP', 'SCENARIO', 'NEUROTIC', 'SCREENER', 'ABSOLUTE', 'TEAMSEAS', 'DURATION', 'CARBLITE', 'POSITRON', 'ROUTINES', 'FLAMINGO', 'CASHTENT', 'ADELAIDE'],
    9: ['HOOVERDAM', 'ROBINHOOD', 'DITHERING', 'HOWITZERS', 'HIGHHEELS', 'ALLUSIONS', 'RESISTIVE', 'INUNDATOR', 'CABRIOLET', 'RATPOISON', 'OUTLINERS', 'BEASTLAND', 'OWENSBORO', 'ANNAPOLIS', 'ROCHESTER'],
    11: ['TURNONADIME', 'CIRCLEABOUT', 'OUTFORASPIN', 'REVOLUTIONS'],
    16: ['SUPERBOWLSTADIUM'],  # for 167A
}

# Fix: DOVER is 5 letters, not 6
if 'DOVER' in answers[6]:
    answers[6].remove('DOVER')
    answers[5].append('DOVER')

# ── All across entries: (num, row, start_col, length) ──────────────────
across_entries = [
    (1,0,0,7),(8,0,9,6),(14,0,17,8),(22,1,0,7),(23,1,8,7),(24,1,17,8),
    (25,2,0,16),(28,2,17,8),(29,3,0,4),(30,3,5,5),(31,3,11,3),(32,3,15,5),
    (34,3,21,4),(35,4,0,4),(36,4,7,4),(38,4,12,9),(41,4,22,3),(42,5,0,4),
    (43,5,5,3),(45,5,9,4),(47,5,14,4),(48,5,20,5),(50,6,0,16),(54,6,17,6),
    (57,7,0,7),(58,7,8,4),(59,7,13,4),(61,7,18,6),(63,8,0,3),(64,8,4,5),
    (66,8,10,4),(68,8,16,4),(70,8,21,4),(72,9,3,6),(73,9,11,14),(77,10,1,3),
    (79,10,5,3),(80,10,10,6),(81,10,17,4),(82,10,22,3),(83,11,0,5),(85,11,6,5),
    (88,11,12,5),(90,11,18,3),(91,11,22,3),(92,12,0,6),(94,12,7,11),(97,12,19,6),
    (99,13,0,3),(100,13,4,3),(102,13,8,5),(103,13,14,5),(105,13,20,5),
    (106,14,0,3),(107,14,4,4),(109,14,9,6),(111,14,17,3),(113,14,21,3),
    (114,15,0,14),(117,15,16,6),(119,16,0,4),(120,16,5,4),(121,16,11,4),
    (123,16,16,5),(124,16,22,3),(127,17,1,6),(129,17,8,4),(132,17,13,4),
    (134,17,18,7),(136,18,2,6),(138,18,9,16),(141,19,0,5),(143,19,7,4),
    (145,19,12,4),(146,19,17,3),(147,19,21,4),(148,20,0,3),(149,20,4,9),
    (153,20,14,4),(155,20,21,4),(156,21,0,4),(158,21,5,5),(159,21,11,3),
    (161,21,15,5),(164,21,21,4),(165,22,0,8),(167,22,9,16),(171,23,0,8),
    (172,23,10,7),(173,23,18,7),(174,24,0,8),(175,24,10,6),(176,24,18,7)
]

# ── All down entries: (num, row, col, length) ──────────────────────────
down_entries = [
    (1,0,0,9),(2,0,1,9),(3,0,2,9),(4,0,3,8),(5,0,4,3),(6,0,5,4),(7,0,6,4),
    (8,0,9,8),(9,0,10,3),(10,0,11,4),(11,0,12,7),(12,0,13,5),(13,0,14,3),
    (14,0,17,7),(15,0,18,5),(16,0,19,5),(17,0,20,3),(18,0,21,4),(19,0,22,15),
    (20,0,23,6),(21,0,24,6),(23,1,8,4),(26,2,7,5),(27,2,15,6),(33,3,16,3),
    (37,4,10,5),(39,4,14,4),(40,4,20,4),(43,5,5,6),(44,5,6,7),(46,5,11,6),
    (49,5,21,5),(51,6,4,4),(52,6,8,4),(53,6,13,7),(55,6,18,6),(56,6,19,7),
    (60,7,16,3),(62,7,23,8),(65,8,7,5),(67,8,12,9),(69,8,17,3),(71,8,24,6),
    (72,9,3,4),(74,9,14,6),(75,9,15,5),(76,9,20,5),(77,10,1,8),(78,10,2,15),
    (80,10,10,6),(83,11,0,6),(84,11,4,5),(86,11,8,3),(87,11,9,5),(89,11,16,3),
    (93,12,5,7),(95,12,11,7),(96,12,17,5),(98,12,21,4),(101,13,6,6),
    (104,13,18,7),(108,14,7,3),(110,14,13,6),(112,14,19,6),(115,15,3,5),
    (116,15,8,3),(117,15,16,4),(118,15,20,4),(122,16,14,5),(124,16,22,9),
    (125,16,23,9),(126,16,24,9),(128,17,4,4),(130,17,9,6),(131,17,10,4),
    (133,17,15,8),(135,17,21,8),(137,18,7,7),(139,18,12,7),(140,18,17,5),
    (141,19,0,6),(142,19,1,6),(144,19,8,3),(150,20,5,5),(151,20,6,5),
    (152,20,11,5),(154,20,16,4),(157,21,3,4),(160,21,13,4),(162,21,18,4),
    (163,21,19,4),(166,22,4,3),(168,22,10,3),(169,22,14,3),(170,22,20,3)
]

# ── Build lookup structures ────────────────────────────────────────────
# Map (row, col) -> list of (entry_type, entry_num, entry_length, position_in_entry, start_row, start_col)
cell_to_entries = defaultdict(list)

for (num, row, start_col, length) in across_entries:
    for i in range(length):
        col = start_col + i
        cell_to_entries[(row, col)].append(('A', num, length, i, row, start_col))

for (num, start_row, col, length) in down_entries:
    for i in range(length):
        row = start_row + i
        cell_to_entries[(row, col)].append(('D', num, length, i, start_row, col))

# Entry info lookup: entry_key -> (type, num, length, start_row, start_col)
entry_info = {}
for (num, row, start_col, length) in across_entries:
    entry_info[('A', num)] = (row, start_col, length)
for (num, start_row, col, length) in down_entries:
    entry_info[('D', num)] = (start_row, col, length)

# ── Pre-confirmed placements ──────────────────────────────────────────
pre_confirmed = {
    ('A', 167): 'SUPERBOWLSTADIUM',
    ('A', 149): 'BEASTLAND',
}

# ── Cascade solver ─────────────────────────────────────────────────────
def solve_cascade(candidate_94a, verbose=True):
    """
    Place 94A candidate and pre-confirmed entries, then cascade constraints.
    Returns dict of results.
    """
    # Grid: 25x25, None = unknown
    grid = [[None]*25 for _ in range(25)]

    # Track placed entries
    placed = {}

    def place_entry(etype, num, word):
        """Place a word into the grid for a given entry."""
        start_row, start_col, length = entry_info[(etype, num)]
        if len(word) != length:
            return False
        for i, ch in enumerate(word):
            if etype == 'A':
                r, c = start_row, start_col + i
            else:
                r, c = start_row + i, start_col
            if grid[r][c] is not None and grid[r][c] != ch:
                return False  # conflict
        for i, ch in enumerate(word):
            if etype == 'A':
                r, c = start_row, start_col + i
            else:
                r, c = start_row + i, start_col
            grid[r][c] = ch
        placed[(etype, num)] = word
        return True

    def get_entry_pattern(etype, num):
        """Get current pattern for an entry (with . for unknown)."""
        start_row, start_col, length = entry_info[(etype, num)]
        pattern = []
        for i in range(length):
            if etype == 'A':
                r, c = start_row, start_col + i
            else:
                r, c = start_row + i, start_col
            ch = grid[r][c]
            pattern.append(ch if ch else '.')
        return ''.join(pattern)

    def match_answers(pattern, length):
        """Find answers matching a pattern from our bank."""
        if length not in answers:
            return []
        regex = re.compile('^' + pattern + '$')
        return [a for a in answers[length] if regex.match(a)]

    # Place pre-confirmed
    for (etype, num), word in pre_confirmed.items():
        place_entry(etype, num, word)

    # Place 94A candidate
    place_entry('A', 94, candidate_94a)

    # Iterative cascade: keep trying to place unique fits
    max_iterations = 50
    iteration = 0
    newly_placed = True

    cascade_log = []
    cascade_log.append(f"Placed 94A = {candidate_94a}")
    cascade_log.append(f"Placed 167A = SUPERBOWLSTADIUM")
    cascade_log.append(f"Placed 149A = BEASTLAND")

    while newly_placed and iteration < max_iterations:
        newly_placed = False
        iteration += 1

        # Check all entries
        all_entry_keys = list(entry_info.keys())
        for key in all_entry_keys:
            if key in placed:
                continue
            etype, num = key
            start_row, start_col, length = entry_info[key]
            pattern = get_entry_pattern(etype, num)

            if '.' not in pattern:
                # Fully filled by crossings
                placed[key] = pattern
                cascade_log.append(f"  Iter {iteration}: {etype}{num} fully filled = {pattern}")
                newly_placed = True
                continue

            if pattern == '.' * length:
                continue  # no constraints

            matches = match_answers(pattern, length)
            if len(matches) == 1:
                word = matches[0]
                if place_entry(etype, num, word):
                    cascade_log.append(f"  Iter {iteration}: {etype}{num} unique fit '{pattern}' -> {word}")
                    newly_placed = True
                elif verbose:
                    cascade_log.append(f"  Iter {iteration}: {etype}{num} CONFLICT trying {word} for '{pattern}'")

    # ── Gather stats ──────────────────────────────────────────────────
    unique_fits = 0
    impossible_fits = 0
    multi_fits = 0
    unconstrained = 0
    constrained_entries = []
    impossible_entries = []
    multi_entries = []

    for key in sorted(entry_info.keys(), key=lambda k: (k[0], k[1])):
        if key in placed:
            continue
        etype, num = key
        start_row, start_col, length = entry_info[key]
        pattern = get_entry_pattern(etype, num)

        if pattern == '.' * length:
            unconstrained += 1
            continue

        matches = match_answers(pattern, length)
        if len(matches) == 0:
            impossible_fits += 1
            impossible_entries.append((etype, num, length, pattern))
        elif len(matches) == 1:
            unique_fits += 1  # should have been placed; maybe conflict
            constrained_entries.append((etype, num, length, pattern, matches))
        else:
            multi_fits += 1
            multi_entries.append((etype, num, length, pattern, matches))

    return {
        'candidate': candidate_94a,
        'placed': dict(placed),
        'cascade_log': cascade_log,
        'unique_fits_remaining': unique_fits,
        'impossible_fits': impossible_fits,
        'multi_fits': multi_fits,
        'unconstrained': unconstrained,
        'impossible_entries': impossible_entries,
        'multi_entries': multi_entries,
        'constrained_entries': constrained_entries,
        'grid': [row[:] for row in grid],
    }


# ── Run all four candidates ────────────────────────────────────────────
candidates = ['CIRCLEABOUT', 'TURNONADIME', 'OUTFORASPIN', 'REVOLUTIONS']

results = []
for cand in candidates:
    res = solve_cascade(cand)
    results.append(res)

# ── Print detailed results for each ───────────────────────────────────
for res in results:
    print("=" * 80)
    print(f"  94A = {res['candidate']}")
    print("=" * 80)

    print("\n--- Cascade Log ---")
    for line in res['cascade_log']:
        print(line)

    print(f"\n--- Summary ---")
    print(f"  Total placed entries: {len(res['placed'])}")
    print(f"  Unique fits remaining (could not place, conflict?): {res['unique_fits_remaining']}")
    print(f"  Impossible fits (0 matches from bank): {res['impossible_fits']}")
    print(f"  Multi-match (2+ matches): {res['multi_fits']}")
    print(f"  Unconstrained (all dots): {res['unconstrained']}")

    print(f"\n--- All Placed Entries ---")
    for key in sorted(res['placed'].keys(), key=lambda k: (k[0], k[1])):
        etype, num = key
        word = res['placed'][key]
        print(f"  {etype}{num:>4} = {word}")

    if res['impossible_entries']:
        print(f"\n--- Impossible Entries (0 matches) ---")
        for etype, num, length, pattern in res['impossible_entries']:
            print(f"  {etype}{num:>4} (len {length}): pattern '{pattern}'")

    if res['multi_entries']:
        print(f"\n--- Multi-Match Entries ---")
        for etype, num, length, pattern, matches in res['multi_entries']:
            print(f"  {etype}{num:>4} (len {length}): pattern '{pattern}' -> {matches}")

    if res['constrained_entries']:
        print(f"\n--- Unplaced Unique Fits (conflict?) ---")
        for etype, num, length, pattern, matches in res['constrained_entries']:
            print(f"  {etype}{num:>4} (len {length}): pattern '{pattern}' -> {matches}")

    print()

# ── Comparison Table ───────────────────────────────────────────────────
print("\n" + "=" * 80)
print("  COMPARISON TABLE")
print("=" * 80)

header = f"{'Candidate':<16} {'Placed':>7} {'Impossible':>11} {'Multi':>6} {'Uncons.':>8}"
print(header)
print("-" * len(header))
for res in results:
    print(f"{res['candidate']:<16} {len(res['placed']):>7} {res['impossible_fits']:>11} {res['multi_fits']:>6} {res['unconstrained']:>8}")

# ── Show crossing details for 94A ─────────────────────────────────────
print("\n" + "=" * 80)
print("  CROSSING DETAILS FOR 94A (row 12, cols 7-17)")
print("=" * 80)

crossing_downs = [
    (65, 8, 7, 5, 4, "last letter"),
    (86, 11, 8, 3, 1, "middle"),
    (87, 11, 9, 5, 1, "pos 1"),
    (80, 10, 10, 6, 2, "pos 2"),
    (95, 12, 11, 7, 0, "first letter"),
    (67, 8, 12, 9, 4, "pos 4"),
    (53, 6, 13, 7, 6, "last letter"),
    (74, 9, 14, 6, 3, "pos 3"),
    (75, 9, 15, 5, 3, "pos 3"),
    (89, 11, 16, 3, 1, "middle"),
    (96, 12, 17, 5, 0, "first letter"),
]

print(f"\n{'Col':<5} {'Down#':<7} {'Len':<5} {'Pos':<6} ", end="")
for cand in candidates:
    print(f"  {cand[:6]:<8}", end="")
print()
print("-" * (5+7+5+6 + len(candidates)*10))

for dnum, drow, dcol, dlen, pos, desc in crossing_downs:
    col_offset = dcol - 7  # position within 94A (0-10)
    print(f"{dcol:<5} {dnum:<4}D  {dlen:<5} [{pos}]{desc:<6}", end="")
    for cand in candidates:
        letter = cand[col_offset]
        print(f"  {letter:<8}", end="")
    print()

# ── Show what each candidate forces in crossing downs ──────────────────
print("\n" + "=" * 80)
print("  FORCED LETTERS IN CROSSING DOWNS + MATCHING ANSWERS")
print("=" * 80)

for cand in candidates:
    print(f"\n--- {cand} ---")
    # Reset grid for this candidate
    r = solve_cascade(cand, verbose=False)
    for dnum, drow, dcol, dlen, pos, desc in crossing_downs:
        col_offset = dcol - 7
        forced_letter = cand[col_offset]
        pattern = r['placed'].get(('D', dnum))
        if pattern:
            print(f"  {dnum}D: PLACED = {pattern}")
        else:
            # Get pattern from grid
            start_row, start_col, length = entry_info[('D', dnum)]
            pat_chars = []
            for i in range(length):
                ch = r['grid'][start_row + i][start_col]
                pat_chars.append(ch if ch else '.')
            pat = ''.join(pat_chars)
            matches = []
            if length in answers:
                regex = re.compile('^' + pat + '$')
                matches = [a for a in answers[length] if regex.match(a)]
            status = f"matches={matches}" if matches else "NO MATCH IN BANK"
            if pat == '.' * length:
                status = "(unconstrained)"
            print(f"  {dnum}D (len {length}): pos[{pos}]={forced_letter}, pattern='{pat}' {status}")

# ── Final Verdict ──────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("  FINAL VERDICT")
print("=" * 80)

best = min(results, key=lambda r: (r['impossible_fits'], -len(r['placed'])))
print(f"\nBest candidate: {best['candidate']}")
print(f"  Placed {len(best['placed'])} entries with {best['impossible_fits']} impossible fits")

# Rank all
ranked = sorted(results, key=lambda r: (r['impossible_fits'], -len(r['placed'])))
print("\nRanking (fewest impossible, most placed):")
for i, r in enumerate(ranked):
    print(f"  {i+1}. {r['candidate']:<16}  placed={len(r['placed']):>3}  impossible={r['impossible_fits']:>2}  multi={r['multi_fits']:>2}")
