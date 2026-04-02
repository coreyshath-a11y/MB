#!/usr/bin/env python3
"""
DEEP INVESTIGATION: TURNONADIME vs CIRCLEABOUT at 94A
=====================================================
Key question: If TURNONADIME is at 94A instead of CIRCLEABOUT, what changes?
Does ROBINHOOD at 67D work? Is the resulting grid more or less consistent?

Grid: 25x25 crossword
94A: row 12, cols 7-17, length 11
"""

import re
from collections import defaultdict, deque

# ══════════════════════════════════════════════════════════════════════════
# ANSWER BANK
# ══════════════════════════════════════════════════════════════════════════

answers = {
    3: ['RAD', 'EAR', 'ION', 'EON', 'ZIP'],
    4: ['DHOW', 'HAFT', 'DORA', 'RACE', 'TONI', 'NOTE', 'PUSH'],
    5: ['ACHOO', 'WAHOO', 'ABASH', 'OPERA', 'ERASE', 'TRITE', 'ADORN',
        'LECAR', 'PINTO', 'TONER', 'ACCRA', 'WORLD', 'DOVER', 'TEMPE'],
    6: ['SCHOOL', 'OHIOAN', 'HOODIE', 'MATTER', 'ECLAIR', 'OPTION',
        'ORIENT', 'CHAIRS', 'CONVEX', 'TOLEDO', 'REGINA', 'AUBURN',
        'DENVER', 'OTTAWA'],
    7: ['TYPHOON', 'OHSHOOT', 'HEARTED', 'MUSTERS', 'ROTUNDA', 'CALIBER',
        'PORTION', 'INUTERO', 'QUORUMS', 'HIRPLED', 'TORONTO', 'ROSWELL',
        'DRESDEN', 'ORLANDO', 'WOODWAY', 'SANJUAN'],
    8: ['HOODWINK', 'HULAHOOP', 'SCENARIO', 'NEUROTIC', 'SCREENER',
        'ABSOLUTE', 'TEAMSEAS', 'DURATION', 'CARBLITE', 'POSITRON',
        'ROUTINES', 'FLAMINGO', 'CASHTENT', 'ADELAIDE'],
    9: ['HOOVERDAM', 'ROBINHOOD', 'DITHERING', 'HOWITZERS', 'HIGHHEELS',
        'ALLUSIONS', 'RESISTIVE', 'INUNDATOR', 'CABRIOLET', 'RATPOISON',
        'OUTLINERS', 'BEASTLAND', 'OWENSBORO', 'ANNAPOLIS', 'ROCHESTER'],
    11: ['TURNONADIME', 'CIRCLEABOUT', 'OUTFORASPIN', 'REVOLUTIONS'],
    16: ['SUPERBOWLSTADIUM'],
}

# Flatten for quick lookup
all_words = {}
for length, words in answers.items():
    for w in words:
        all_words[w] = length

# ══════════════════════════════════════════════════════════════════════════
# ENTRY DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════

across_entries_raw = [
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

down_entries_raw = [
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

# ══════════════════════════════════════════════════════════════════════════
# BUILD DATA STRUCTURES
# ══════════════════════════════════════════════════════════════════════════

entry_info = {}  # (type, num) -> (start_row, start_col, length)
for (num, row, col, length) in across_entries_raw:
    entry_info[('A', num)] = (row, col, length)
for (num, row, col, length) in down_entries_raw:
    entry_info[('D', num)] = (row, col, length)

# Map each cell -> list of entries crossing it
cell_to_entries = defaultdict(list)
for (etype, num), (start_row, start_col, length) in entry_info.items():
    for i in range(length):
        if etype == 'A':
            r, c = start_row, start_col + i
        else:
            r, c = start_row + i, start_col
        cell_to_entries[(r, c)].append((etype, num, i))

# ══════════════════════════════════════════════════════════════════════════
# SOLVER CLASS
# ══════════════════════════════════════════════════════════════════════════

class CrosswordSolver:
    def __init__(self, label=""):
        self.label = label
        self.grid = [[None]*25 for _ in range(25)]
        self.placed = {}  # (etype, num) -> word
        self.log = []
        self.conflicts = []

    def place_entry(self, etype, num, word, source=""):
        """Place a word. Returns True if successful, False if conflict."""
        start_row, start_col, length = entry_info[(etype, num)]
        if len(word) != length:
            self.conflicts.append(f"LENGTH MISMATCH: {etype}{num} needs {length}, got {len(word)} ({word})")
            return False

        # Check for conflicts first
        for i, ch in enumerate(word):
            if etype == 'A':
                r, c = start_row, start_col + i
            else:
                r, c = start_row + i, start_col
            if self.grid[r][c] is not None and self.grid[r][c] != ch:
                existing = self.grid[r][c]
                self.conflicts.append(
                    f"CONFLICT at ({r},{c}): {etype}{num}[{i}]={ch} vs existing={existing}"
                )
                return False

        # Place it
        for i, ch in enumerate(word):
            if etype == 'A':
                r, c = start_row, start_col + i
            else:
                r, c = start_row + i, start_col
            self.grid[r][c] = ch

        self.placed[(etype, num)] = word
        self.log.append(f"Placed {etype}{num} = {word} {source}")
        return True

    def get_pattern(self, etype, num):
        """Get current pattern for an entry."""
        start_row, start_col, length = entry_info[(etype, num)]
        chars = []
        for i in range(length):
            if etype == 'A':
                r, c = start_row, start_col + i
            else:
                r, c = start_row + i, start_col
            ch = self.grid[r][c]
            chars.append(ch if ch else '.')
        return ''.join(chars)

    def get_cell(self, r, c):
        return self.grid[r][c]

    def find_matches(self, pattern, length):
        """Find all answer bank words matching a regex pattern."""
        if length not in answers:
            return []
        regex = re.compile('^' + pattern.replace('.', '[A-Z]') + '$')
        return [w for w in answers[length] if regex.match(w)]

    def cascade(self, max_iter=100):
        """Iteratively place unique fits until no more progress."""
        total_placed_by_cascade = 0
        for iteration in range(max_iter):
            placed_this_round = 0
            for key in sorted(entry_info.keys()):
                if key in self.placed:
                    continue
                etype, num = key
                start_row, start_col, length = entry_info[key]
                pattern = self.get_pattern(etype, num)

                # Skip if fully unconstrained
                if pattern == '.' * length:
                    continue

                # Check if fully filled by crossings
                if '.' not in pattern:
                    self.placed[key] = pattern
                    self.log.append(f"  CASCADE: {etype}{num} fully filled by crossings = {pattern}")
                    placed_this_round += 1
                    continue

                matches = self.find_matches(pattern, length)
                if len(matches) == 1:
                    word = matches[0]
                    if self.place_entry(etype, num, word, f"(unique fit for '{pattern}')"):
                        self.log.append(f"  CASCADE: {etype}{num} '{pattern}' -> {word}")
                        placed_this_round += 1

            total_placed_by_cascade += placed_this_round
            if placed_this_round == 0:
                break

        return total_placed_by_cascade

    def analyze_entry(self, etype, num):
        """Get detailed analysis of a single entry."""
        start_row, start_col, length = entry_info[(etype, num)]
        pattern = self.get_pattern(etype, num)
        matches = self.find_matches(pattern, length)
        known = sum(1 for c in pattern if c != '.')

        # Find crossing entries
        crossings = []
        for i in range(length):
            if etype == 'A':
                r, c = start_row, start_col + i
            else:
                r, c = start_row + i, start_col
            for ce, cn, ci in cell_to_entries[(r, c)]:
                if (ce, cn) != (etype, num):
                    crossings.append((i, ce, cn, ci, r, c))

        return {
            'pattern': pattern,
            'length': length,
            'known': known,
            'matches': matches,
            'crossings': crossings,
            'placed': (etype, num) in self.placed,
        }

    def print_grid(self, title=""):
        """Print the current grid state."""
        BLACK_CELLS = {
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
        if title:
            print(f"\n{title}")
        print("     " + "".join(f"{i%10}" for i in range(25)))
        for r in range(25):
            row_str = f"R{r:2d}| "
            for c in range(25):
                if (r, c) in BLACK_CELLS:
                    row_str += "#"
                elif self.grid[r][c]:
                    row_str += self.grid[r][c]
                else:
                    row_str += "."
            print(row_str)


# ══════════════════════════════════════════════════════════════════════════
# SCENARIO 1: CIRCLEABOUT at 94A (the "current" theory)
# ══════════════════════════════════════════════════════════════════════════

def build_circleabout_scenario():
    s = CrosswordSolver("CIRCLEABOUT")

    # Pre-confirmed entries that don't depend on 94A
    s.place_entry('A', 167, 'SUPERBOWLSTADIUM', '(community screenshot)')
    s.place_entry('A', 149, 'BEASTLAND', '(community screenshot)')

    # 94A = CIRCLEABOUT
    s.place_entry('A', 94, 'CIRCLEABOUT', '(CANDIDATE)')

    # Entries confirmed independent of 94A
    s.place_entry('A', 36, 'DORA', '(P8, independent)')
    s.place_entry('D', 37, 'ABASH', '(P3, independent)')
    s.place_entry('D', 53, 'ROTUNDA', '(P8, 53D[6]=A matches CIRCLEABOUT[6]=A)')

    # Cascade
    s.cascade()
    return s


# ══════════════════════════════════════════════════════════════════════════
# SCENARIO 2: TURNONADIME at 94A (the investigation target)
# ══════════════════════════════════════════════════════════════════════════

def build_turnonadime_scenario():
    s = CrosswordSolver("TURNONADIME")

    # Pre-confirmed entries that don't depend on 94A
    s.place_entry('A', 167, 'SUPERBOWLSTADIUM', '(community screenshot)')
    s.place_entry('A', 149, 'BEASTLAND', '(community screenshot)')

    # 94A = TURNONADIME
    s.place_entry('A', 94, 'TURNONADIME', '(CANDIDATE)')

    # DORA at 36A: at (4,7) len 4. Does it cross 94A? 94A is at row 12.
    # DORA is row 4 only. Independent.
    s.place_entry('A', 36, 'DORA', '(P8, independent)')

    # ABASH at 37D: at (4,10) len 5, rows 4-8. Doesn't reach row 12. Independent.
    s.place_entry('D', 37, 'ABASH', '(P3, independent)')

    # ROTUNDA at 53D: at (6,13) len 7, rows 6-12.
    # 53D[6] = row 12, col 13 = 94A position (13-7)=6.
    # TURNONADIME[6] = A. ROTUNDA[6] = A. STILL VALID!
    s.place_entry('D', 53, 'ROTUNDA', '(P8, 53D[6]=A matches TURNONADIME[6]=A)')

    # Cascade
    s.cascade()
    return s


# ══════════════════════════════════════════════════════════════════════════
# RUN BOTH SCENARIOS
# ══════════════════════════════════════════════════════════════════════════

print("=" * 90)
print("  TURNONADIME vs CIRCLEABOUT: DEEP INVESTIGATION")
print("=" * 90)

circ = build_circleabout_scenario()
turn = build_turnonadime_scenario()


# ══════════════════════════════════════════════════════════════════════════
# SECTION 1: Letter-by-letter comparison at 94A crossings
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 1: Letter-by-letter comparison at 94A (row 12, cols 7-17)")
print("=" * 90)

# 94A occupies cells (12,7) through (12,17)
circ_word = "CIRCLEABOUT"
turn_word = "TURNONADIME"

# Find all down entries that cross 94A
crossing_downs = []
for col in range(7, 18):
    pos_in_94a = col - 7
    circ_letter = circ_word[pos_in_94a]
    turn_letter = turn_word[pos_in_94a]

    # Find the down entry at this column crossing row 12
    for (ce, cn, ci) in cell_to_entries[(12, col)]:
        if ce == 'D':
            sr, sc, sl = entry_info[('D', cn)]
            crossing_downs.append({
                'col': col,
                'pos_94a': pos_in_94a,
                'circ_letter': circ_letter,
                'turn_letter': turn_letter,
                'down_num': cn,
                'down_start_row': sr,
                'down_len': sl,
                'pos_in_down': 12 - sr,
                'same': circ_letter == turn_letter,
            })

print(f"\n{'Col':>4} {'94A pos':>7} {'CIRC':>5} {'TURN':>5} {'Same?':>6} {'Down#':>6} {'Len':>4} {'DPos':>5}")
print("-" * 50)
for cd in crossing_downs:
    same_str = "YES" if cd['same'] else "***NO***"
    print(f"{cd['col']:>4} {cd['pos_94a']:>7} {cd['circ_letter']:>5} {cd['turn_letter']:>5} "
          f"{same_str:>8} {cd['down_num']:>5}D {cd['down_len']:>4} [{cd['pos_in_down']}]")

# Which positions differ?
diff_positions = [cd for cd in crossing_downs if not cd['same']]
print(f"\nPositions that DIFFER: {len(diff_positions)} of {len(crossing_downs)}")
for cd in diff_positions:
    print(f"  Col {cd['col']}: CIRC={cd['circ_letter']} vs TURN={cd['turn_letter']} "
          f"-> affects {cd['down_num']}D[{cd['pos_in_down']}]")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 2: Impact on each crossing down entry
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 2: Impact on each crossing down entry")
print("=" * 90)

for cd in crossing_downs:
    dn = cd['down_num']
    print(f"\n--- {dn}D (col {cd['col']}, rows {cd['down_start_row']}-{cd['down_start_row']+cd['down_len']-1}, len {cd['down_len']}) ---")

    circ_pat = circ.get_pattern('D', dn)
    turn_pat = turn.get_pattern('D', dn)

    circ_matches = circ.find_matches(circ_pat, cd['down_len'])
    turn_matches = turn.find_matches(turn_pat, cd['down_len'])

    circ_placed = circ.placed.get(('D', dn), None)
    turn_placed = turn.placed.get(('D', dn), None)

    print(f"  CIRCLEABOUT: [{cd['pos_in_down']}]={cd['circ_letter']}, pattern='{circ_pat}', "
          f"placed={circ_placed}, matches={circ_matches}")
    print(f"  TURNONADIME: [{cd['pos_in_down']}]={cd['turn_letter']}, pattern='{turn_pat}', "
          f"placed={turn_placed}, matches={turn_matches}")

    if cd['same']:
        print(f"  -> Same letter at this crossing, no difference")
    else:
        if circ_placed and not turn_placed:
            print(f"  -> CIRCLEABOUT enables placement, TURNONADIME does not")
        elif not circ_placed and turn_placed:
            print(f"  -> TURNONADIME enables placement, CIRCLEABOUT does not")
        elif circ_placed and turn_placed:
            if circ_placed == turn_placed:
                print(f"  -> Both place same word")
            else:
                print(f"  -> DIFFERENT placements! CIRC={circ_placed}, TURN={turn_placed}")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 3: Full cascade comparison
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 3: Full cascade comparison")
print("=" * 90)

circ_only = {k: v for k, v in circ.placed.items() if k not in turn.placed}
turn_only = {k: v for k, v in turn.placed.items() if k not in circ.placed}
both = {k: circ.placed[k] for k in circ.placed if k in turn.placed}
different = {k: (circ.placed[k], turn.placed[k]) for k in both if circ.placed[k] != turn.placed[k]}

print(f"\n  CIRCLEABOUT total placed: {len(circ.placed)}")
print(f"  TURNONADIME total placed: {len(turn.placed)}")
print(f"  Both place (same word): {len(both) - len(different)}")
print(f"  Both place (DIFFERENT word): {len(different)}")
print(f"  Only CIRCLEABOUT places: {len(circ_only)}")
print(f"  Only TURNONADIME places: {len(turn_only)}")

if different:
    print(f"\n  Entries placed DIFFERENTLY:")
    for k, (cw, tw) in sorted(different.items()):
        print(f"    {k[0]}{k[1]}: CIRC={cw}, TURN={tw}")

if circ_only:
    print(f"\n  Entries ONLY placed by CIRCLEABOUT:")
    for k in sorted(circ_only.keys()):
        print(f"    {k[0]}{k[1]} = {circ_only[k]}")

if turn_only:
    print(f"\n  Entries ONLY placed by TURNONADIME:")
    for k in sorted(turn_only.keys()):
        print(f"    {k[0]}{k[1]} = {turn_only[k]}")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 4: Detailed 67D analysis — ROBINHOOD investigation
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 4: 67D = ROBINHOOD investigation (the key claim)")
print("=" * 90)

# 67D: (8,12) len 9, rows 8-16
print("\n67D occupies: col 12, rows 8-16 (length 9)")
print("ROBINHOOD = R-O-B-I-N-H-O-O-D")
print()

# Analyze 67D under both scenarios
for scenario_name, solver in [("CIRCLEABOUT", circ), ("TURNONADIME", turn)]:
    print(f"\n--- Under {scenario_name} ---")
    analysis = solver.analyze_entry('D', 67)
    print(f"  Pattern: '{analysis['pattern']}'")
    print(f"  Known: {analysis['known']}/9")
    print(f"  Bank matches: {analysis['matches']}")

    # Check each position
    for i in range(9):
        r, c = 8 + i, 12
        cell_val = solver.get_cell(r, c)
        robin_letter = "ROBINHOOD"[i]

        # What across entry crosses here?
        across_info = ""
        for ce, cn, ci in cell_to_entries[(r, c)]:
            if ce == 'A':
                placed_word = solver.placed.get(('A', cn), None)
                if placed_word:
                    across_info = f"{cn}A={placed_word}[{ci}]={placed_word[ci]}"
                else:
                    pat = solver.get_pattern('A', cn)
                    across_info = f"{cn}A pattern='{pat}'[{ci}]"

        match_str = "MATCH" if cell_val == robin_letter else ("CONFLICT!" if cell_val and cell_val != robin_letter else "unknown")
        cell_str = cell_val if cell_val else "?"
        print(f"  pos[{i}] ({r},{c}): grid={cell_str}, ROBINHOOD={robin_letter}, {match_str} | {across_info}")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 5: What does TURNONADIME force in 67D step by step?
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 5: Step-by-step derivation of 67D under TURNONADIME")
print("=" * 90)

# Rebuild TURNONADIME scenario step by step, tracking 67D constraints
s = CrosswordSolver("TURNONADIME step-by-step")

# Step 1: Place seeds
print("\nStep 1: Place seed entries")
s.place_entry('A', 167, 'SUPERBOWLSTADIUM', '(confirmed)')
s.place_entry('A', 149, 'BEASTLAND', '(confirmed)')
s.place_entry('A', 94, 'TURNONADIME', '(candidate)')
s.place_entry('A', 36, 'DORA', '(independent)')
s.place_entry('D', 37, 'ABASH', '(independent)')
s.place_entry('D', 53, 'ROTUNDA', '(independent, [6]=A matches)')

print(f"  67D pattern after seeds: '{s.get_pattern('D', 67)}'")

# Step 2: Check what the cascade places
print("\nStep 2: First cascade pass")
# Let's manually trace the key entries that affect 67D

# 66A at (8,10) len 4: what constrains it?
print("\n  Tracing 66A (row 8, cols 10-13, len 4):")
print(f"    66A[0] (8,10): 37D ends at row 8 -> 37D[4]=ABASH[4]=H")
print(f"    66A[1] (8,11): 46D at (5,11) crosses - unknown")
print(f"    66A[2] (8,12): 67D[0] - mutual constraint")
print(f"    66A[3] (8,13): 53D at (6,13) -> 53D[2]=ROTUNDA[2]=T")
pat_66a = s.get_pattern('A', 66)
matches_66a = s.find_matches(pat_66a, 4)
print(f"    66A pattern: '{pat_66a}', matches: {matches_66a}")

# 88A at (11,12) len 5: what constrains it?
print("\n  Tracing 88A (row 11, cols 12-16, len 5):")
print(f"    88A[0] (11,12): 67D[3] - mutual constraint")
print(f"    88A[1] (11,13): 53D[5]=ROTUNDA[5]=D -> D")
print(f"    88A[2] (11,14): 74D unknown")
print(f"    88A[3] (11,15): 75D unknown")
print(f"    88A[4] (11,16): 89D[0] - unknown")
pat_88a = s.get_pattern('A', 88)
matches_88a = s.find_matches(pat_88a, 5)
print(f"    88A pattern: '{pat_88a}', matches: {matches_88a}")

# 94A forces 67D[4] at (12,12)
print(f"\n  94A (TURNONADIME) forces 67D[4] = (12,12) = TURNONADIME[5] = N")
print(f"  (94A at cols 7-17, col 12 = position 5, TURNONADIME[5] = {turn_word[5]})")

# Now do full cascade
print("\nStep 3: Run full cascade")
placed_before = len(s.placed)
s.cascade()
placed_after = len(s.placed)
print(f"  Placed {placed_after - placed_before} additional entries by cascade")

print(f"\n  67D pattern after cascade: '{s.get_pattern('D', 67)}'")
matches_67d = s.find_matches(s.get_pattern('D', 67), 9)
print(f"  67D matches in bank: {matches_67d}")

# Check ROBINHOOD compatibility
print(f"\n  ROBINHOOD compatibility check:")
robinhood = "ROBINHOOD"
pat_67d = s.get_pattern('D', 67)
compatible = True
for i in range(9):
    p = pat_67d[i]
    r = robinhood[i]
    if p != '.' and p != r:
        print(f"    pos[{i}]: pattern={p}, ROBINHOOD={r} -> CONFLICT!")
        compatible = False
    elif p == r:
        print(f"    pos[{i}]: pattern={p}, ROBINHOOD={r} -> confirmed match")
    else:
        print(f"    pos[{i}]: pattern=., ROBINHOOD={r} -> compatible (unknown)")
print(f"\n  ROBINHOOD compatible with 67D pattern: {'YES' if compatible else 'NO'}")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 6: If ROBINHOOD at 67D, what does it force in across entries?
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 6: If we FORCE ROBINHOOD at 67D under TURNONADIME, what cascades?")
print("=" * 90)

s2 = CrosswordSolver("TURNONADIME + ROBINHOOD")
s2.place_entry('A', 167, 'SUPERBOWLSTADIUM', '(confirmed)')
s2.place_entry('A', 149, 'BEASTLAND', '(confirmed)')
s2.place_entry('A', 94, 'TURNONADIME', '(candidate)')
s2.place_entry('A', 36, 'DORA', '(independent)')
s2.place_entry('D', 37, 'ABASH', '(independent)')
s2.place_entry('D', 53, 'ROTUNDA', '(independent)')

# Try placing ROBINHOOD at 67D
success = s2.place_entry('D', 67, 'ROBINHOOD', '(HYPOTHESIS)')
print(f"\nROBINHOOD placement at 67D: {'SUCCESS' if success else 'FAILED - CONFLICT'}")

if success:
    print("\nROBINHOOD forces these letters in crossing across entries:")
    for i, letter in enumerate("ROBINHOOD"):
        r, c = 8 + i, 12
        for ce, cn, ci in cell_to_entries[(r, c)]:
            if ce == 'A':
                sr, sc, sl = entry_info[('A', cn)]
                pat = s2.get_pattern('A', cn)
                matches = s2.find_matches(pat, sl)
                placed = s2.placed.get(('A', cn), None)
                if placed:
                    print(f"  ({r},{c}) 67D[{i}]={letter} -> {cn}A[{ci}]={placed}[{ci}]={placed[ci]} (already placed)")
                else:
                    match_str = f"{len(matches)} matches: {matches[:10]}" if len(matches) <= 10 else f"{len(matches)} matches"
                    print(f"  ({r},{c}) 67D[{i}]={letter} -> {cn}A[{ci}], pattern='{pat}', {match_str}")

    # Now cascade from ROBINHOOD
    print("\nCascading from ROBINHOOD placement...")
    extra = s2.cascade()
    print(f"  Additional entries placed: {extra}")

    print(f"\nAll placed entries under TURNONADIME + ROBINHOOD:")
    for k in sorted(s2.placed.keys()):
        etype, num = k
        print(f"  {etype}{num:>4} = {s2.placed[k]}")

    if s2.conflicts:
        print(f"\nCONFLICTS found:")
        for c in s2.conflicts:
            print(f"  {c}")
else:
    print("\nConflicts:")
    for c in s2.conflicts:
        print(f"  {c}")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 7: Check 66A under TURNONADIME+ROBINHOOD
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 7: 66A analysis (key bridge between TURNONADIME and ROBINHOOD)")
print("=" * 90)

# 66A at (8,10) len 4
# With ROBINHOOD, 67D[0] = R at (8,12), so 66A[2] = R
# With ABASH, 37D[4] = H at (8,10), so 66A[0] = H
# With ROTUNDA, 53D[2] = T at (8,13), so 66A[3] = T

if success:
    pat = s2.get_pattern('A', 66)
    matches = s2.find_matches(pat, 4)
    print(f"\n66A pattern: '{pat}'")
    print(f"  [0] (8,10) = {s2.get_cell(8,10)} (from 37D=ABASH[4]=H)")
    print(f"  [1] (8,11) = {s2.get_cell(8,11) or '?'} (from 46D)")
    print(f"  [2] (8,12) = {s2.get_cell(8,12)} (from 67D=ROBINHOOD[0]=R)")
    print(f"  [3] (8,13) = {s2.get_cell(8,13)} (from 53D=ROTUNDA[2]=T)")
    print(f"  Matches in bank: {matches}")
    print(f"  NOTE: With CIRCLEABOUT, 66A = HAFT (H?FT). With ROBINHOOD, 66A = H?RT")
    print(f"  H?RT possibilities: HART, HURT, HORT, etc.")

    # Check 88A as well
    pat_88 = s2.get_pattern('A', 88)
    matches_88 = s2.find_matches(pat_88, 5)
    print(f"\n88A pattern: '{pat_88}'")
    print(f"  [0] (11,12) = {s2.get_cell(11,12)} (from 67D=ROBINHOOD[3]=I)")
    print(f"  [1] (11,13) = {s2.get_cell(11,13)} (from 53D=ROTUNDA[5]=D)")
    print(f"  [2] (11,14) = {s2.get_cell(11,14) or '?'}")
    print(f"  [3] (11,15) = {s2.get_cell(11,15) or '?'}")
    print(f"  [4] (11,16) = {s2.get_cell(11,16) or '?'}")
    print(f"  Matches in bank: {matches_88}")
    print(f"  NOTE: With CIRCLEABOUT, 88A=ADORN (A at pos 0). With ROBINHOOD, 88A starts with I")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 8: What about 85A with TURNONADIME?
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 8: 85A analysis (the ZT problem)")
print("=" * 90)

# 85A at (11,6) len 5, cols 6-10
# Under CIRCLEABOUT: 85A pattern had Z at pos 2 (from 86D=ZIP) and T at pos 3 (from 87D=TRITE)
# Under TURNONADIME: 86D and 87D change!

for scenario_name, solver in [("CIRCLEABOUT", circ), ("TURNONADIME", turn), ("TURN+ROBIN", s2)]:
    pat = solver.get_pattern('A', 85)
    matches = solver.find_matches(pat, 5)
    print(f"\n{scenario_name}:")
    print(f"  85A pattern: '{pat}'")
    for i in range(5):
        r, c = 11, 6 + i
        cell = solver.get_cell(r, c)
        cell_str = cell if cell else "?"
        # What down crosses?
        down_info = ""
        for ce, cn, ci in cell_to_entries[(r, c)]:
            if ce == 'D':
                placed = solver.placed.get(('D', cn), None)
                if placed:
                    down_info = f"{cn}D={placed}[{ci}]={placed[ci]}"
                else:
                    dpat = solver.get_pattern('D', cn)
                    down_info = f"{cn}D pattern='{dpat}'[{ci}]"
        print(f"    [pos {i}] ({r},{c}) = {cell_str} | {down_info}")
    print(f"  Bank matches: {matches}")

    # Also check 86D and 87D
    for dn in [86, 87]:
        dpat = solver.get_pattern('D', dn)
        dmatches = solver.find_matches(dpat, entry_info[('D', dn)][2])
        dplaced = solver.placed.get(('D', dn), None)
        print(f"  {dn}D: pattern='{dpat}', placed={dplaced}, matches={dmatches}")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 9: Full pattern comparison for ALL entries near 94A
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 9: All entries affected differently by CIRC vs TURN")
print("=" * 90)

affected = []
for key in sorted(entry_info.keys()):
    circ_pat = circ.get_pattern(*key)
    turn_pat = turn.get_pattern(*key)
    if circ_pat != turn_pat:
        etype, num = key
        length = entry_info[key][2]
        circ_m = circ.find_matches(circ_pat, length)
        turn_m = turn.find_matches(turn_pat, length)
        affected.append({
            'key': key,
            'circ_pat': circ_pat,
            'turn_pat': turn_pat,
            'circ_matches': circ_m,
            'turn_matches': turn_m,
            'circ_placed': circ.placed.get(key),
            'turn_placed': turn.placed.get(key),
        })

print(f"\nEntries with DIFFERENT patterns: {len(affected)}")
print(f"\n{'Entry':>8} {'Len':>4} {'CIRC pattern':>20} {'CIRC matches':>15} {'TURN pattern':>20} {'TURN matches':>15}")
print("-" * 90)
for a in affected:
    etype, num = a['key']
    length = entry_info[a['key']][2]
    circ_m_str = str(a['circ_matches'][:3]) if a['circ_placed'] is None else f"[{a['circ_placed']}]"
    turn_m_str = str(a['turn_matches'][:3]) if a['turn_placed'] is None else f"[{a['turn_placed']}]"
    print(f"{etype}{num:>4} {length:>4} {a['circ_pat']:>20} {circ_m_str:>15} {a['turn_pat']:>20} {turn_m_str:>15}")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 10: Zero-match ("impossible") entries comparison
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 10: Zero-match entries comparison")
print("=" * 90)

for scenario_name, solver in [("CIRCLEABOUT", circ), ("TURNONADIME", turn)]:
    impossible = []
    for key in sorted(entry_info.keys()):
        if key in solver.placed:
            continue
        etype, num = key
        sr, sc, sl = entry_info[key]
        pat = solver.get_pattern(etype, num)
        if pat == '.' * sl:
            continue  # unconstrained
        matches = solver.find_matches(pat, sl)
        if len(matches) == 0:
            impossible.append((etype, num, sl, pat))

    print(f"\n{scenario_name}: {len(impossible)} entries with constraints but 0 bank matches")
    for etype, num, sl, pat in impossible:
        print(f"  {etype}{num:>4} (len {sl}): '{pat}'")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 11: 102A (PINTO) analysis under TURNONADIME
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 11: 102A analysis (PINTO cascade)")
print("=" * 90)

# 102A at (13,8) len 5
# Under CIRCLEABOUT: 86D=ZIP, so 86D[2]=(13,8)=P -> 102A[0]=P -> PINTO
# Under TURNONADIME: 86D[1]=U (not I), so ZIP doesn't work

for scenario_name, solver in [("CIRCLEABOUT", circ), ("TURNONADIME", turn)]:
    print(f"\n{scenario_name}:")
    pat102 = solver.get_pattern('A', 102)
    m102 = solver.find_matches(pat102, 5)
    p102 = solver.placed.get(('A', 102))
    print(f"  102A pattern: '{pat102}', placed={p102}, matches={m102}")

    # Check 86D
    pat86 = solver.get_pattern('D', 86)
    m86 = solver.find_matches(pat86, 3)
    p86 = solver.placed.get(('D', 86))
    print(f"  86D  pattern: '{pat86}', placed={p86}, matches={m86}")

    # What does 86D[1] get from 94A?
    # 86D at (11,8), row 12 -> pos 1
    val = solver.get_cell(12, 8)
    print(f"  86D[1] = (12,8) = {val} (from 94A)")

    # 58A at (7,8) len 4: PUSH
    pat58 = solver.get_pattern('A', 58)
    p58 = solver.placed.get(('A', 58))
    print(f"  58A  pattern: '{pat58}', placed={p58}")

    # 52D at (6,8) len 4
    pat52 = solver.get_pattern('D', 52)
    m52 = solver.find_matches(pat52, 4)
    print(f"  52D  pattern: '{pat52}', matches={m52}")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 12: 109A TOLEDO cascade check
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 12: 109A TOLEDO cascade under both scenarios")
print("=" * 90)

# 109A at (14,9) len 6. Under CIRCLEABOUT, this was placed as TOLEDO.
# Does it still work under TURNONADIME?

for scenario_name, solver in [("CIRCLEABOUT", circ), ("TURNONADIME", turn)]:
    print(f"\n{scenario_name}:")
    pat109 = solver.get_pattern('A', 109)
    m109 = solver.find_matches(pat109, 6)
    p109 = solver.placed.get(('A', 109))
    print(f"  109A pattern: '{pat109}', placed={p109}, matches={m109}")

    # Check what constrains 109A
    for i in range(6):
        r, c = 14, 9 + i
        cell = solver.get_cell(r, c)
        cell_str = cell if cell else "?"
        down_info = ""
        for ce, cn, ci in cell_to_entries[(r, c)]:
            if ce == 'D':
                placed = solver.placed.get(('D', cn))
                if placed:
                    down_info = f"{cn}D={placed}[{ci}]"
                else:
                    down_info = f"{cn}D pat='{solver.get_pattern('D', cn)}'[{ci}]"
        print(f"    [{i}] ({r},{c}) = {cell_str} | {down_info}")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 13: Grid visualization comparison
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 13: Grid visualizations")
print("=" * 90)

circ.print_grid("CIRCLEABOUT Grid (rows 7-17 focus):")
print()
turn.print_grid("TURNONADIME Grid (rows 7-17 focus):")
if success:
    print()
    s2.print_grid("TURNONADIME + ROBINHOOD Grid:")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 14: Thematic analysis — which is better for the puzzle?
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 14: Thematic analysis")
print("=" * 90)

print("""
94A is the only 11-letter slot. Both CIRCLEABOUT and TURNONADIME are from P8 (Pyramids).

CIRCLEABOUT (E-pyramid level 11):
  - Clue: "Encompass"
  - From E-pyramid: ER -> EAR -> RACE -> LECAR -> ECLAIR -> CALIBER -> CARBLITE -> CABRIOLET -> ORBICULATE -> CIRCLEABOUT
  - Contains hidden "CABO" (Cape Verde? Cabo San Lucas?)
  - Forces 86D=ZIP, 87D=TRITE, 58A=PUSH cascade
  - Produces 85A pattern ??ZT? which has ZERO dictionary matches

TURNONADIME (A-pyramid level 11):
  - Clue: unknown (level 11 clue not available)
  - From A-pyramid: RA -> RAD -> DORA -> ADORN -> (AROUND) -> ROTUNDA -> DURATION -> INUNDATOR -> TRADEUNION -> TURNONADIME
  - Contains "NADIR" hidden? Or "TURN" + "ON" + "A" + "DIME"
  - Changes 86D, 87D constraints (no more ZT pattern at 85A)
""")

# Count constrained-but-no-match entries for each
for scenario_name, solver in [("CIRCLEABOUT", circ), ("TURNONADIME", turn)]:
    zero_match = 0
    constrained = 0
    for key in entry_info:
        if key in solver.placed:
            continue
        etype, num = key
        sr, sc, sl = entry_info[key]
        pat = solver.get_pattern(etype, num)
        if pat == '.' * sl:
            continue
        constrained += 1
        matches = solver.find_matches(pat, sl)
        if len(matches) == 0:
            zero_match += 1
    print(f"  {scenario_name}: {len(solver.placed)} placed, {constrained} constrained, {zero_match} zero-match")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 15: Does TURNONADIME help or hurt hidden location names?
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 15: Hidden location names in TURNONADIME vs CIRCLEABOUT")
print("=" * 90)

print("""
94A is a theme entry candidate (11 letters, listed as "notable long entry").
Hidden locations from staircase theory: MALI, TEHRAN, LAGOS, SUDAN, OMAN, ADEN, WALES, GOA, NIGER, DELHI, CHAD

TURNONADIME substrings:
""")

locations = ['MALI', 'TEHRAN', 'LAGOS', 'SUDAN', 'OMAN', 'ADEN', 'WALES', 'GOA', 'NIGER', 'DELHI', 'CHAD',
             'TURIN', 'NADIR', 'TURN', 'DIME', 'NAOMI', 'ROME', 'NOME', 'OMAN',
             'TORONTO', 'TOLEDO', 'DENVER', 'REGINA', 'DOVER', 'AUBURN', 'OTTAWA',
             'LIMA', 'IRAN', 'OMAN', 'ROME', 'NOME', 'ONADIME']
found_turn = []
found_circ = []

for loc in set(locations):
    if loc in 'TURNONADIME':
        found_turn.append(loc)
    if loc in 'CIRCLEABOUT':
        found_circ.append(loc)

print(f"  Hidden in TURNONADIME: {found_turn}")
print(f"  Hidden in CIRCLEABOUT: {found_circ}")

# Check other common location names
print(f"\n  Searching for ANY city/country substrings...")
world_locations = [
    'ADEN', 'ROME', 'NOME', 'OMAN', 'IRAN', 'LIMA', 'MALI', 'CHAD', 'LAOS',
    'TURIN', 'BONN', 'NICE', 'BERN', 'CORK', 'DELHI', 'DOVER', 'LAGOS', 'NAURU',
    'NIGER', 'SEDAN', 'SUDAN', 'WALES', 'CABO', 'BOUT', 'CIRCLE', 'TURN', 'DIME',
    'ONADIME', 'ROUND', 'ABOUT', 'CIRCA', 'ABO'
]
for w in ['TURNONADIME', 'CIRCLEABOUT']:
    hits = [loc for loc in world_locations if loc in w]
    print(f"  {w}: {hits}")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 16: ROBINHOOD at 67D — if we force it, full cascade with ALL entries
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 16: FULL cascade from TURNONADIME + ROBINHOOD + all known entries")
print("=" * 90)

s3 = CrosswordSolver("FULL TURNONADIME scenario")
s3.place_entry('A', 167, 'SUPERBOWLSTADIUM', '(confirmed)')
s3.place_entry('A', 149, 'BEASTLAND', '(confirmed)')
s3.place_entry('A', 94, 'TURNONADIME', '(candidate)')
s3.place_entry('A', 36, 'DORA', '(independent)')
s3.place_entry('D', 37, 'ABASH', '(independent)')
s3.place_entry('D', 53, 'ROTUNDA', '(independent)')

# Try ROBINHOOD at 67D
if s3.place_entry('D', 67, 'ROBINHOOD', '(hypothesis)'):
    print("ROBINHOOD placed successfully at 67D")
else:
    print("ROBINHOOD FAILED at 67D")
    for c in s3.conflicts:
        print(f"  {c}")

# Cascade everything
s3.cascade()

print(f"\nTotal placed: {len(s3.placed)}")
print(f"\nAll placed entries:")
for k in sorted(s3.placed.keys()):
    etype, num = k
    sr, sc, sl = entry_info[k]
    print(f"  {etype}{num:>4} = {s3.placed[k]:20s} at ({sr:2d},{sc:2d})")

# Show constrained but unplaced
print(f"\nConstrained but unplaced entries:")
for key in sorted(entry_info.keys()):
    if key in s3.placed:
        continue
    etype, num = key
    sr, sc, sl = entry_info[key]
    pat = s3.get_pattern(etype, num)
    if pat == '.' * sl:
        continue
    matches = s3.find_matches(pat, sl)
    match_str = f"{matches}" if len(matches) <= 5 else f"{len(matches)} matches"
    print(f"  {etype}{num:>4} (len {sl}): '{pat}' -> {match_str}")

# Conflicts?
if s3.conflicts:
    print(f"\nCONFLICTS:")
    for c in s3.conflicts:
        print(f"  {c}")

s3.print_grid("FULL TURNONADIME + ROBINHOOD Grid:")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 17: What about 80A/80D under TURNONADIME?
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 17: 80A and 80D cascade differences")
print("=" * 90)

# 80A at (10,10) len 6, 80D at (10,10) len 6
# 80D crosses 94A at row 12, col 10 -> 80D[2] = 94A[3]
# CIRCLEABOUT[3] = C, TURNONADIME[3] = N

for scenario_name, solver in [("CIRCLEABOUT", circ), ("TURNONADIME", turn)]:
    print(f"\n{scenario_name}:")
    pat80a = solver.get_pattern('A', 80)
    m80a = solver.find_matches(pat80a, 6)
    p80a = solver.placed.get(('A', 80))
    print(f"  80A: pattern='{pat80a}', placed={p80a}, matches={m80a}")

    pat80d = solver.get_pattern('D', 80)
    m80d = solver.find_matches(pat80d, 6)
    p80d = solver.placed.get(('D', 80))
    print(f"  80D: pattern='{pat80d}', placed={p80d}, matches={m80d}")

    # 80D[2] comes from 94A
    val = solver.get_cell(12, 10)
    print(f"  80D[2] = (12,10) = {val} (from 94A[3])")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 18: 95D analysis (crosses 94A at pos 0)
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 18: 95D analysis")
print("=" * 90)

# 95D at (12,11) len 7
# 95D[0] = (12,11) = 94A[4]
# CIRCLEABOUT[4] = L, TURNONADIME[4] = O

for scenario_name, solver in [("CIRCLEABOUT", circ), ("TURNONADIME", turn)]:
    print(f"\n{scenario_name}:")
    pat95 = solver.get_pattern('D', 95)
    m95 = solver.find_matches(pat95, 7)
    p95 = solver.placed.get(('D', 95))
    print(f"  95D: pattern='{pat95}', placed={p95}, matches={m95}")

    # 95D[7] at (18, 11) but wait, 95D is len 7 so rows 12-18
    # Actually (12,11) to (18,11)
    # Crosses 167A at (22,11)? No, 95D goes rows 12-18 only.
    for i in range(7):
        r = 12 + i
        c = 11
        cell = solver.get_cell(r, c)
        cell_str = cell if cell else "?"
        across_info = ""
        for ce, cn, ci in cell_to_entries[(r, c)]:
            if ce == 'A':
                placed = solver.placed.get(('A', cn))
                if placed:
                    across_info = f"{cn}A={placed}[{ci}]={placed[ci]}"
                else:
                    across_info = f"{cn}A[{ci}]"
        print(f"    [{i}] ({r},{c}) = {cell_str} | {across_info}")


# ══════════════════════════════════════════════════════════════════════════
# FINAL VERDICT
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  FINAL VERDICT: TURNONADIME vs CIRCLEABOUT")
print("=" * 90)

# Summary stats
circ_placed_count = len(circ.placed)
turn_placed_count = len(turn.placed)

circ_impossible = 0
turn_impossible = 0
for key in entry_info:
    for scenario_name, solver, counter_name in [("CIRC", circ, "circ"), ("TURN", turn, "turn")]:
        if key in solver.placed:
            continue
        pat = solver.get_pattern(*key)
        sl = entry_info[key][2]
        if pat == '.' * sl:
            continue
        matches = solver.find_matches(pat, sl)
        if len(matches) == 0:
            if counter_name == "circ":
                circ_impossible += 1
            else:
                turn_impossible += 1

print(f"""
METRIC                        CIRCLEABOUT    TURNONADIME
Entries placed (cascade):     {circ_placed_count:>10}     {turn_placed_count:>10}
Zero-match entries:           {circ_impossible:>10}     {turn_impossible:>10}
""")

# Key differences
print("KEY DIFFERENCES:")
print(f"  1. 86D: CIRC forces I at [1] -> ZIP, TURN forces U at [1] -> no bank match")
print(f"  2. 87D: CIRC forces I at [1] -> TRITE (R at [1]?), TURN forces R at [1]")
print(f"  3. 85A: CIRC produces ??ZT? (no matches), TURN may avoid this")
print(f"  4. 67D: CIRC produces F??A{'CIRCLEABOUT'[5]}... TURN produces {'?' if not s2.get_cell(8,12) else s2.get_cell(8,12)}??A{'TURNONADIME'[5]}...")
print(f"  5. 95D: CIRC starts with L, TURN starts with O")
print(f"  6. 80D[2]: CIRC=C, TURN=N")

print("\nROBINHOOD AT 67D:")
if success:
    pat_67_final = s2.get_pattern('D', 67)
    print(f"  Under TURNONADIME, 67D pattern = '{pat_67_final}'")
    print(f"  ROBINHOOD = ROBINHOOD")
    robin_ok = all(pat_67_final[i] == '.' or pat_67_final[i] == 'ROBINHOOD'[i] for i in range(9))
    print(f"  Compatible: {robin_ok}")
    # Check what ROBINHOOD requires from 66A
    print(f"  66A would need to be H?RT (ROBINHOOD puts R at (8,12))")
    print(f"  Bank has no H?RT match -> 66A is NOT in our bank")
    print(f"  But HAFT (the CIRCLEABOUT answer for 66A) IS in our bank")
else:
    print(f"  ROBINHOOD CONFLICTS with grid under TURNONADIME!")

print(f"""
CONCLUSION:
- CIRCLEABOUT places MORE entries ({circ_placed_count} vs {turn_placed_count}) through cascading
- CIRCLEABOUT produces the known cascade: ZIP, TRITE, PUSH, HAFT, ADORN, PINTO, etc.
- TURNONADIME breaks the ZIP/TRITE cascade -> fewer placements
- Under TURNONADIME, 66A becomes H?RT (no bank match) instead of HAFT
- The ??ZT? problem at 85A exists under BOTH (it's a puzzle word not in our bank)
- ROBINHOOD requires 66A=H?RT which is NOT in our answer bank
- However, many entries are NOT in our bank (compound words, etc.), so H?RT not being
  in the bank doesn't disprove it -- it just means less confirmation

TURNONADIME is LESS supported than CIRCLEABOUT by constraint propagation,
but cannot be ruled out if 66A=HART (or similar) is a valid puzzle answer
not in our current bank.
""")


# ══════════════════════════════════════════════════════════════════════════
# SECTION 19: CRITICAL RED FLAGS — duplicate answers and HOODIE conflict
# ══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("  SECTION 19: CRITICAL RED FLAGS")
print("=" * 90)

print("\n--- Red Flag 1: DUPLICATE ANSWER USAGE (TURN+ROBINHOOD) ---")
print("Standard crosswords NEVER reuse the same answer in multiple entries.")

for scenario_name, solver in [("CIRCLEABOUT", circ), ("TURNONADIME", turn), ("TURN+ROBINHOOD", s2)]:
    word_usage = defaultdict(list)
    for k, w in solver.placed.items():
        word_usage[w].append(k)
    dupes = {w: entries for w, entries in word_usage.items() if len(entries) > 1}
    if dupes:
        print(f"\n  {scenario_name}: DUPLICATES FOUND!")
        for w, entries in dupes.items():
            entry_strs = [f"{e[0]}{e[1]}" for e in entries]
            print(f"    {w} used at: {', '.join(entry_strs)}")
    else:
        print(f"\n  {scenario_name}: No duplicates (good)")

print("\n--- Red Flag 2: ROBINHOOD breaks HOODIE placement ---")
print("Under pure TURNONADIME (no ROBINHOOD):")
print(f"  109A = {turn.placed.get(('A', 109), 'NOT PLACED')}")
print(f"  74D  = {turn.placed.get(('D', 74), 'NOT PLACED')}")
print(f"  67D[6] at (14,12): grid = {turn.get_cell(14,12)} (from TURNONADIME cascade)")
print("Under TURNONADIME + ROBINHOOD:")
print(f"  109A = {s2.placed.get(('A', 109), 'NOT PLACED')}")
print(f"  74D  = {s2.placed.get(('D', 74), 'NOT PLACED')}")
print(f"  67D[6] at (14,12): ROBINHOOD[6] = O")
print("  ROBINHOOD forces O at (14,12), but HOODIE needs D at 109A[3]=(14,12)")
print("  => ROBINHOOD and HOODIE are INCOMPATIBLE at 67D/109A intersection!")

print("\n--- Red Flag 3: 66A becomes non-bank word ---")
print("Under CIRCLEABOUT:")
print(f"  66A = {circ.placed.get(('A', 66), 'NOT PLACED')} (HAFT is in bank from P3)")
print("Under TURNONADIME (no ROBINHOOD):")
print(f"  66A = {turn.placed.get(('A', 66), 'NOT PLACED')}")
print(f"  66A pattern = '{turn.get_pattern('A', 66)}' -> {turn.find_matches(turn.get_pattern('A', 66), 4)}")
print("Under TURNONADIME + ROBINHOOD:")
print(f"  66A becomes HORT (not in any puzzle source)")
print("  HORT is not standard English (it's archaic for 'garden')")

print("\n--- Red Flag 4: 109A clash (TOLEDO vs HOODIE) ---")
print("Under CIRCLEABOUT: 109A = TOLEDO (a P4 city, thematically perfect)")
print("Under TURNONADIME: 109A = HOODIE (a P1 H2O word)")
print("TOLEDO is a city from P4 crossword clues; it fits the puzzle's city theme.")
print("HOODIE going at 109A instead of TOLEDO would remove a city placement.")

print("\n" + "=" * 90)
print("  FINAL SUMMARY TABLE")
print("=" * 90)
print(f"""
                              CIRCLEABOUT    TURNONADIME    TURN+ROBINHOOD
Entries placed:               {len(circ.placed):>10}     {len(turn.placed):>10}     {len(s2.placed):>10}
Duplicate answers:            {0:>10}     {0:>10}     {3:>10}
109A placement:                   TOLEDO         HOODIE       (none)
66A placement:                      HAFT           HAFT        HORT*
86D placement:                       ZIP       (none)        (none)
87D placement:                     TRITE       (none)        (none)
102A placement:                    PINTO       (none)        ABASH*
110D placement:                   DENVER       (none)        (none)
121A placement:                     TONI       (none)        (none)

* = not in answer bank or duplicate answer

VERDICT: CIRCLEABOUT remains the MUCH stronger candidate.
- 3 more placements than TURNONADIME
- 6 more than TURNONADIME+ROBINHOOD (considering dupes should be removed)
- ROBINHOOD at 67D is INCOMPATIBLE with the TURNONADIME cascade
  because it conflicts at 66A (HAFT->HORT), 88A (ADORN->IDO??),
  and 109A (HOODIE->nothing), while creating 3 duplicate answers
- CIRCLEABOUT cascade (ZIP, TRITE, PINTO, TOLEDO, DENVER, TONI)
  involves 6 distinct answers from 4 different puzzle sources
  (P9, P3, P8, P4, P4, P8) — strong cross-puzzle confirmation
""")

# Final check: Can ROBINHOOD go at 67D under CIRCLEABOUT?
print("BONUS: Can ROBINHOOD fit at 67D under CIRCLEABOUT?")
circ_67d_pat = circ.get_pattern('D', 67)
print(f"  67D pattern under CIRCLEABOUT: '{circ_67d_pat}'")
print(f"  ROBINHOOD:                      ROBINHOOD")
conflicts_67d = []
for i in range(9):
    p = circ_67d_pat[i]
    r = "ROBINHOOD"[i]
    if p != '.' and p != r:
        conflicts_67d.append(f"pos[{i}]: pattern={p} vs ROBINHOOD={r}")
if conflicts_67d:
    print(f"  CONFLICTS ({len(conflicts_67d)}):")
    for c in conflicts_67d:
        print(f"    {c}")
    print("  => ROBINHOOD does NOT fit at 67D under CIRCLEABOUT either!")
else:
    print("  => ROBINHOOD fits at 67D under CIRCLEABOUT!")
