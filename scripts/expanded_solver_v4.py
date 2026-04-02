#!/usr/bin/env python3
"""
Expanded Crossword Solver v4
Builds 25x25 grid, places confirmed entries, finds constraint patterns,
and matches against known answer lists to find unique fits.
"""

# ─── Black cells ───
black_cells = set()
black_raw = """
(0,7) (0,8) (0,15) (0,16)
(1,7) (1,15) (1,16)
(2,16)
(3,4) (3,10) (3,14) (3,20)
(4,4) (4,5) (4,6) (4,11) (4,21)
(5,4) (5,8) (5,13) (5,18) (5,19)
(6,16) (6,23) (6,24)
(7,7) (7,12) (7,17) (7,24)
(8,3) (8,9) (8,14) (8,15) (8,20)
(9,0) (9,1) (9,2) (9,9) (9,10)
(10,0) (10,4) (10,8) (10,9) (10,16) (10,21)
(11,5) (11,11) (11,17) (11,21)
(12,6) (12,18)
(13,3) (13,7) (13,13) (13,19)
(14,3) (14,8) (14,15) (14,16) (14,20) (14,24)
(15,14) (15,15) (15,22) (15,23) (15,24)
(16,4) (16,9) (16,10) (16,15) (16,21)
(17,0) (17,7) (17,12) (17,17)
(18,0) (18,1) (18,8)
(19,5) (19,6) (19,11) (19,16) (19,20)
(20,3) (20,13) (20,18) (20,19) (20,20)
(21,4) (21,10) (21,14) (21,20)
(22,8)
(23,8) (23,9) (23,17)
(24,8) (24,9) (24,16) (24,17)
"""
import re
for m in re.finditer(r'\((\d+),(\d+)\)', black_raw):
    black_cells.add((int(m.group(1)), int(m.group(2))))

# ─── Initialize grid ───
grid = [['.' for _ in range(25)] for _ in range(25)]
for r, c in black_cells:
    grid[r][c] = '#'

# ─── Confirmed placements ───
confirmed = {
    '36A': ('DORA', 4, 7, 'across', 4),
    '37D': ('ABASH', 4, 10, 'down', 5),
    '53D': ('ROTUNDA', 6, 13, 'down', 7),
    '58A': ('PUSH', 7, 8, 'across', 4),
    '66A': ('HAFT', 8, 10, 'across', 4),
    '86D': ('ZIP', 11, 8, 'down', 3),
    '87D': ('TRITE', 11, 9, 'down', 5),
    '88A': ('ADORN', 11, 12, 'across', 5),
    '94A': ('CIRCLEABOUT', 12, 7, 'across', 11),
    '96D': ('TONER', 12, 17, 'down', 5),
    '102A': ('PINTO', 13, 8, 'across', 5),
    '103A': ('ACHOO', 13, 14, 'across', 5),
    '109A': ('TOLEDO', 14, 9, 'across', 6),
    '110D': ('DENVER', 14, 13, 'down', 6),
    '117A': ('REGINA', 15, 16, 'across', 6),
    '121A': ('TONI', 16, 11, 'across', 4),
    '123A': ('ERASE', 16, 16, 'across', 5),
    '167A': ('SUPERBOWLSTADIUM', 22, 9, 'across', 16),
    '149A': ('BEASTLAND', 20, 4, 'across', 9),
}

hypothetical = {
    '104D': ('ORGANIC', 13, 18, 'down', 7),
    '111A': ('NRA', 14, 17, 'across', 3),
}

def place_entry(word, row, col, direction, length, uppercase=True):
    """Place a word into the grid."""
    w = word.upper() if uppercase else word.lower()
    for i, ch in enumerate(w):
        if direction == 'across':
            r, c = row, col + i
        else:
            r, c = row + i, col
        if 0 <= r < 25 and 0 <= c < 25:
            if grid[r][c] == '#':
                print(f"  WARNING: placing '{ch}' at ({r},{c}) which is a black cell!")
            elif grid[r][c] not in ('.', ch, ch.upper(), ch.lower()):
                print(f"  CONFLICT at ({r},{c}): grid has '{grid[r][c]}', trying to place '{ch}' from {word}")
            grid[r][c] = ch

# Place confirmed entries (uppercase)
print("=" * 80)
print("PLACING CONFIRMED ENTRIES")
print("=" * 80)
for key, (word, row, col, direction, length) in sorted(confirmed.items(), key=lambda x: x[0]):
    print(f"  {key}: {word} at ({row},{col}) {direction} len={length}")
    place_entry(word, row, col, direction, length, uppercase=True)

# Place hypothetical entries (lowercase)
print("\nPLACING HYPOTHETICAL ENTRIES (lowercase)")
for key, (word, row, col, direction, length) in sorted(hypothetical.items(), key=lambda x: x[0]):
    print(f"  {key}: {word} at ({row},{col}) {direction} len={length}")
    place_entry(word, row, col, direction, length, uppercase=False)

# ─── Print grid ───
print("\n" + "=" * 80)
print("CURRENT GRID STATE")
print("=" * 80)
print("     " + "".join(f"{i%10}" for i in range(25)))
print("     " + "0         1         2    ")
print("     " + "-" * 25)
for r in range(25):
    row_str = ""
    for c in range(25):
        row_str += grid[r][c]
    print(f"R{r:2d} |{row_str}")

# ─── All entries ───
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
    (172,23,10,7),(173,23,18,7),(174,24,0,8),(175,24,10,6),(176,24,18,7),
]

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
    (163,21,19,4),(166,22,4,3),(168,22,10,3),(169,22,14,3),(170,22,20,3),
]

# ─── Known answers by length ───
answers_by_length = {
    3: ['RAD', 'EAR', 'ION', 'EON', 'ZIP'],
    4: ['DHOW', 'HAFT', 'DORA', 'RACE', 'TONI', 'NOTE', 'PUSH'],
    5: ['ACHOO', 'WAHOO', 'ABASH', 'OPERA', 'ERASE', 'TRITE', 'ADORN', 'LECAR',
        'PINTO', 'TONER', 'ACCRA', 'WORLD', 'DOVER', 'TEMPE'],
    6: ['SCHOOL', 'OHIOAN', 'HOODIE', 'MATTER', 'ECLAIR', 'OPTION', 'ORIENT',
        'CHAIRS', 'CONVEX', 'TOLEDO', 'REGINA', 'AUBURN', 'DENVER', 'OTTAWA',
        'WARSAW'],
    7: ['TYPHOON', 'OHSHOOT', 'HEARTED', 'MUSTERS', 'ROTUNDA', 'CALIBER',
        'PORTION', 'INUTERO', 'QUORUMS', 'HIRPLED', 'TORONTO', 'ROSWELL',
        'DRESDEN', 'ORLANDO', 'WOODWAY', 'SANJUAN', 'SEVILLE'],
    8: ['HOODWINK', 'HULAHOOP', 'SCENARIO', 'NEUROTIC', 'SCREENER', 'ABSOLUTE',
        'TEAMSEAS', 'DURATION', 'CARBLITE', 'POSITRON', 'ROUTINES', 'FLAMINGO',
        'CASHTENT', 'ADELAIDE'],
    9: ['HOOVERDAM', 'ROBINHOOD', 'DITHERING', 'HOWITZERS', 'HIGHHEELS',
        'ALLUSIONS', 'RESISTIVE', 'INUNDATOR', 'CABRIOLET', 'RATPOISON',
        'OUTLINERS', 'BEASTLAND', 'OWENSBORO', 'ANNAPOLIS', 'ROCHESTER'],
    11: ['CIRCLEABOUT'],
    14: [],  # theme entries
    15: [],
    16: ['SUPERBOWLSTADIUM'],
}

# P4 cities
p4_cities = ['TORONTO', 'REGINA', 'OWENSBORO', 'TOLEDO', 'ROSWELL', 'DRESDEN',
             'TEMPE', 'WARSAW', 'SANJUAN', 'ADELAIDE', 'DENVER', 'SEVILLE',
             'OTTAWA', 'WILMINGTON', 'SACRAMENTO', 'ANNAPOLIS', 'AUBURN',
             'DOVER', 'ROCHESTER', 'ORLANDO', 'WOODWAY']

# Already placed
already_placed = set()
for key, (word, *_) in confirmed.items():
    already_placed.add(word.upper())
for key, (word, *_) in hypothetical.items():
    already_placed.add(word.upper())


def read_entry(row, col, direction, length):
    """Read current letters from grid for an entry."""
    pattern = ""
    for i in range(length):
        if direction == 'across':
            r, c = row, col + i
        else:
            r, c = row + i, col
        ch = grid[r][c]
        if ch == '.' or ch == '#':
            pattern += '?'
        else:
            pattern += ch.upper()
    return pattern


def matches_pattern(word, pattern):
    """Check if a word matches a constraint pattern (? = wildcard)."""
    if len(word) != len(pattern):
        return False
    for w, p in zip(word, pattern):
        if p != '?' and w.upper() != p.upper():
            return False
    return True


# ─── Build constraint patterns for ALL entries ───
print("\n" + "=" * 80)
print("ALL ENTRY CONSTRAINT PATTERNS")
print("=" * 80)

all_entries = []
for (num, row, col, length) in across_entries:
    all_entries.append((num, row, col, length, 'across'))
for (num, row, col, length) in down_entries:
    all_entries.append((num, row, col, length, 'down'))

all_entries.sort(key=lambda x: (x[0], x[4]))

unique_fits = []
multi_fits = []
no_fits = []

for (num, row, col, length, direction) in all_entries:
    suffix = 'A' if direction == 'across' else 'D'
    label = f"{num}{suffix}"
    pattern = read_entry(row, col, direction, length)
    known_count = sum(1 for ch in pattern if ch != '?')

    # Find matching answers
    candidates = answers_by_length.get(length, [])
    matching = [w for w in candidates if matches_pattern(w, pattern) and w.upper() not in already_placed]

    # Also check P4 cities that match length
    city_matches = [c for c in p4_cities if len(c) == length and matches_pattern(c, pattern) and c.upper() not in already_placed]

    if known_count > 0 or matching or city_matches:
        status = ""
        if pattern.replace('?', '') == '':
            status = "(no constraints)"
        elif '?' not in pattern:
            status = "(FULLY PLACED)"
        elif len(matching) == 1:
            status = f"*** UNIQUE FIT: {matching[0]} ***"
            unique_fits.append((label, pattern, matching[0], length, row, col, direction))
        elif len(matching) == 0 and len(city_matches) == 0 and known_count > 0:
            status = "(constrained but no answer-list match)"

        has_info = known_count > 0 or matching or city_matches
        if has_info:
            line = f"  {label:6s} ({row:2d},{col:2d}) len={length:2d} {direction:6s}: {pattern}"
            if matching:
                line += f"  -> answers: {matching}"
            if city_matches:
                line += f"  -> P4 cities: {city_matches}"
            if status:
                line += f"  {status}"
            print(line)

            if len(matching) == 1:
                pass  # already in unique_fits
            elif len(matching) > 1:
                multi_fits.append((label, pattern, matching, city_matches))

# ─── Summaries ───
print("\n" + "=" * 80)
print("UNIQUE FITS (exactly one answer matches pattern)")
print("=" * 80)
if unique_fits:
    for (label, pattern, answer, length, row, col, direction) in unique_fits:
        print(f"  {label}: {answer} (pattern: {pattern}) at ({row},{col}) {direction}")
else:
    print("  None found.")

print("\n" + "=" * 80)
print("MULTI-FIT ENTRIES (multiple answers match - need more constraints)")
print("=" * 80)
for (label, pattern, answers, cities) in multi_fits:
    print(f"  {label}: pattern={pattern}")
    if answers:
        print(f"       answer matches: {answers}")
    if cities:
        print(f"       P4 city matches: {cities}")

# ─── P4 city placement analysis ───
print("\n" + "=" * 80)
print("P4 CITY PLACEMENT ANALYSIS")
print("=" * 80)
print("Which P4 cities (not already placed) could fit into grid entries?\n")

for city in sorted(p4_cities):
    if city.upper() in already_placed:
        print(f"  {city}: ALREADY PLACED")
        continue
    city_len = len(city)
    possible_placements = []
    for (num, row, col, length, direction) in all_entries:
        if length != city_len:
            continue
        pattern = read_entry(row, col, direction, length)
        if matches_pattern(city, pattern):
            suffix = 'A' if direction == 'across' else 'D'
            label = f"{num}{suffix}"
            known = sum(1 for ch in pattern if ch != '?')
            possible_placements.append((label, pattern, known))
    if possible_placements:
        constrained = [(l, p, k) for l, p, k in possible_placements if k > 0]
        unconstrained = [(l, p, k) for l, p, k in possible_placements if k == 0]
        if constrained:
            for l, p, k in constrained:
                print(f"  {city} ({city_len}): fits {l} (pattern={p}, {k} letters constrained)")
        if unconstrained:
            labels = [l for l, _, _ in unconstrained]
            print(f"  {city} ({city_len}): fits unconstrained: {labels}")
    else:
        print(f"  {city} ({city_len}): NO ENTRY of matching length found")

# ─── Entries crossing SUPERBOWLSTADIUM (167A) ───
print("\n" + "=" * 80)
print("ENTRIES CROSSING SUPERBOWLSTADIUM (167A, row=22, cols=9-24)")
print("=" * 80)
# 167A is at row 22, cols 9-24, word = SUPERBOWLSTADIUM
word_167 = "SUPERBOWLSTADIUM"
for i, ch in enumerate(word_167):
    c = 9 + i
    r = 22
    # Find down entries crossing this cell
    for (num, dr, dc, length) in down_entries:
        if dc == c and dr <= r < dr + length:
            suffix = 'D'
            label = f"{num}{suffix}"
            pos_in_down = r - dr
            pattern = read_entry(dr, dc, 'down', length)
            print(f"  Col {c:2d}: letter '{ch}' (pos {i+1}/16) crosses {label} (len={length}) at pos {pos_in_down+1}/{length}")
            print(f"         {label} pattern: {pattern}")
            # Find matching answers
            candidates = answers_by_length.get(length, [])
            matching = [w for w in candidates if matches_pattern(w, pattern) and w.upper() not in already_placed]
            city_matching = [w for w in p4_cities if len(w) == length and matches_pattern(w, pattern) and w.upper() not in already_placed]
            if matching:
                print(f"         Answer matches: {matching}")
            if city_matching:
                print(f"         P4 city matches: {city_matching}")
            if not matching and not city_matching:
                print(f"         No matches in answer list")

# ─── Entries crossing BEASTLAND (149A) ───
print("\n" + "=" * 80)
print("ENTRIES CROSSING BEASTLAND (149A, row=20, cols=4-12)")
print("=" * 80)
word_149 = "BEASTLAND"
for i, ch in enumerate(word_149):
    c = 4 + i
    r = 20
    for (num, dr, dc, length) in down_entries:
        if dc == c and dr <= r < dr + length:
            suffix = 'D'
            label = f"{num}{suffix}"
            pos_in_down = r - dr
            pattern = read_entry(dr, dc, 'down', length)
            print(f"  Col {c:2d}: letter '{ch}' (pos {i+1}/9) crosses {label} (len={length}) at pos {pos_in_down+1}/{length}")
            print(f"         {label} pattern: {pattern}")
            candidates = answers_by_length.get(length, [])
            matching = [w for w in candidates if matches_pattern(w, pattern) and w.upper() not in already_placed]
            city_matching = [w for w in p4_cities if len(w) == length and matches_pattern(w, pattern) and w.upper() not in already_placed]
            if matching:
                print(f"         Answer matches: {matching}")
            if city_matching:
                print(f"         P4 city matches: {city_matching}")
            if not matching and not city_matching:
                print(f"         No matches in answer list")

# ─── Check ALL constrained entries more carefully ───
print("\n" + "=" * 80)
print("ENTRIES WITH PARTIAL CONSTRAINTS (1+ known letters, not fully placed)")
print("=" * 80)
constrained_entries = []
for (num, row, col, length, direction) in all_entries:
    suffix = 'A' if direction == 'across' else 'D'
    label = f"{num}{suffix}"
    pattern = read_entry(row, col, direction, length)
    known_count = sum(1 for ch in pattern if ch != '?')
    if 0 < known_count < length:
        constrained_entries.append((label, pattern, length, row, col, direction, known_count))

constrained_entries.sort(key=lambda x: -x[6])  # Sort by most constrained first

for (label, pattern, length, row, col, direction, known_count) in constrained_entries:
    candidates = answers_by_length.get(length, [])
    matching = [w for w in candidates if matches_pattern(w, pattern)]
    already = [w for w in matching if w.upper() in already_placed]
    available = [w for w in matching if w.upper() not in already_placed]
    city_matching = [w for w in p4_cities if len(w) == length and matches_pattern(w, pattern)]

    line = f"  {label:6s} len={length:2d} known={known_count:2d}/{length:2d} pattern={pattern}"
    extras = []
    if available:
        extras.append(f"available={available}")
    if already:
        extras.append(f"(already placed: {already})")
    if city_matching:
        extras.append(f"P4 cities={city_matching}")
    if not available and not city_matching:
        extras.append("NO MATCH in lists")
    print(line + "  " + ", ".join(extras))

# ─── Circled cells analysis ───
print("\n" + "=" * 80)
print("CIRCLED CELLS - CURRENT LETTERS")
print("=" * 80)
circled = [
    (0,12), (2,4), (3,8), (3,24), (4,19), (10,12),
    (11,2), (11,22), (13,0), (18,7), (19,17), (20,2),
    (22,11), (22,18), (22,24), (24,20)
]
for r, c in circled:
    ch = grid[r][c]
    display = ch if ch not in ('.', '#') else '?'
    print(f"  ({r:2d},{c:2d}): {display}")

code = ""
for r, c in circled:
    ch = grid[r][c]
    if ch not in ('.', '#'):
        code += ch.upper()
    else:
        code += '?'
print(f"\n  Partial extraction code: {code}")

# ─── Cascade analysis: what if we place unique fits? ───
print("\n" + "=" * 80)
print("CASCADE ANALYSIS: What new constraints would unique fits create?")
print("=" * 80)
if unique_fits:
    for (label, pattern, answer, length, row, col, direction) in unique_fits:
        print(f"\n  If we place {label} = {answer}:")
        # Simulate placement
        for i, ch in enumerate(answer):
            if direction == 'across':
                r, c = row, col + i
            else:
                r, c = row + i, col
            # Find crossing entries
            cross_dir = 'down' if direction == 'across' else 'across'
            entries_to_check = down_entries if cross_dir == 'down' else across_entries
            for (enum, er, ec, elen) in entries_to_check:
                if cross_dir == 'down' and ec == c and er <= r < er + elen:
                    suffix = 'D'
                    cross_label = f"{enum}{suffix}"
                    pos = r - er
                    old_pattern = read_entry(er, ec, 'down', elen)
                    if old_pattern[pos] == '?':
                        new_pattern = old_pattern[:pos] + ch + old_pattern[pos+1:]
                        new_candidates = [w for w in answers_by_length.get(elen, []) if matches_pattern(w, new_pattern) and w.upper() not in already_placed and w.upper() != answer.upper()]
                        new_cities = [w for w in p4_cities if len(w) == elen and matches_pattern(w, new_pattern) and w.upper() not in already_placed and w.upper() != answer.upper()]
                        if new_candidates or new_cities:
                            print(f"    -> {cross_label} gets new constraint at pos {pos+1}: '{ch}' -> pattern {new_pattern}")
                            if new_candidates:
                                print(f"       Answer matches: {new_candidates}")
                            if new_cities:
                                print(f"       P4 city matches: {new_cities}")
                elif cross_dir == 'across' and er == r and ec <= c < ec + elen:
                    suffix = 'A'
                    cross_label = f"{enum}{suffix}"
                    pos = c - ec
                    old_pattern = read_entry(er, ec, 'across', elen)
                    if old_pattern[pos] == '?':
                        new_pattern = old_pattern[:pos] + ch + old_pattern[pos+1:]
                        new_candidates = [w for w in answers_by_length.get(elen, []) if matches_pattern(w, new_pattern) and w.upper() not in already_placed and w.upper() != answer.upper()]
                        new_cities = [w for w in p4_cities if len(w) == elen and matches_pattern(w, new_pattern) and w.upper() not in already_placed and w.upper() != answer.upper()]
                        if new_candidates or new_cities:
                            print(f"    -> {cross_label} gets new constraint at pos {pos+1}: '{ch}' -> pattern {new_pattern}")
                            if new_candidates:
                                print(f"       Answer matches: {new_candidates}")
                            if new_cities:
                                print(f"       P4 city matches: {new_cities}")
else:
    print("  No unique fits to cascade from.")

print("\n" + "=" * 80)
print("DONE")
print("=" * 80)
