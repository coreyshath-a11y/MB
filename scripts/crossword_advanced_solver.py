#!/usr/bin/env python3
"""
Advanced Crossword Solver for MrBeast 25x25 Puzzle

Multi-phase approach:
  Phase 1: Basic constraint propagation (known answers only)
  Phase 2: Dictionary-aided elimination (NLTK crossing validation)
  Phase 3: Speculative placement with contradiction detection
  Phase 4: Cell-level forced-letter analysis

Uses NLTK English word list + all known puzzle answers for crossing validation.
When placing a candidate word at a position, checks whether all crossing entries
still have at least one valid completion in the dictionary. If any crossing
becomes impossible (zero matches), the placement is rejected.
"""

import sys
import re
from collections import defaultdict
from copy import deepcopy

try:
    from nltk.corpus import words as nltk_words_corpus
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("WARNING: NLTK not available. Dictionary validation disabled.")

# ============================================================
# GRID STRUCTURE (25x25, from CROSSWORD_GRID_DIGITIZED.md)
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
    (1, 0, 0, 9), (2, 0, 1, 9), (3, 0, 2, 9), (4, 0, 3, 8),
    (5, 0, 4, 3), (6, 0, 5, 4), (7, 0, 6, 4),
    (8, 0, 9, 8), (9, 0, 10, 3), (10, 0, 11, 4),
    (11, 0, 12, 7), (12, 0, 13, 5), (13, 0, 14, 3),
    (14, 0, 17, 7), (15, 0, 18, 5), (16, 0, 19, 5),
    (17, 0, 20, 3), (18, 0, 21, 4), (19, 0, 22, 15),
    (20, 0, 23, 6), (21, 0, 24, 6),
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

# Build entry lookup: "1A" -> ('A', row, col, length), "1D" -> ('D', row, col, length)
ALL_ENTRIES = {}
for num, row, col, length in ACROSS:
    ALL_ENTRIES[f"{num}A"] = ('A', row, col, length)
for num, row, col, length in DOWN:
    ALL_ENTRIES[f"{num}D"] = ('D', row, col, length)

print(f"Total entries: {len(ALL_ENTRIES)} ({len(ACROSS)} across, {len(DOWN)} down)")

# ============================================================
# ALL KNOWN ANSWERS (with length and source)
# ============================================================

ALL_ANSWERS_RAW = {
    # P1 (H2O words) - all contain H + two O's
    "ACHOO": (5, "P1"), "TYPHOON": (7, "P1"), "SCHOOL": (6, "P1"),
    "HOODWINK": (8, "P1"), "OHSHOOT": (7, "P1"), "OHIOAN": (6, "P1"),
    "HULAHOOP": (8, "P1"), "HOODIE": (6, "P1"), "HOOVERDAM": (9, "P1"),
    "DHOW": (4, "P1"), "ROBINHOOD": (9, "P1"),
    "WAHOO": (5, "P1"),     # P1-13 candidate 1
    "YAHOO": (5, "P1alt"),  # P1-13 candidate 2
    "HOOPLA": (6, "P1"),    # P1-8 candidate 1 (upset/nonsense)
    "VOODOO": (6, "P1alt"), # P1-8 candidate 2

    # P3 (Beach) - all definitive
    "HAFT": (4, "P3"), "DITHERING": (9, "P3"), "HOWITZERS": (9, "P3"),
    "SCENARIO": (8, "P3"), "ABASH": (5, "P3"), "NEUROTIC": (8, "P3"),
    "HEARTED": (7, "P3"), "HIGHHEELS": (9, "P3"), "SCREENER": (8, "P3"),
    "MATTER": (6, "P3"), "OPERA": (5, "P3"),
    "ALLUSIONS": (9, "P3"), "RESISTIVE": (9, "P3"), "ABSOLUTE": (8, "P3"),
    "ERASE": (5, "P3"), "TEAMSEAS": (8, "P3"), "TRITE": (5, "P3"),
    "MUSTERS": (7, "P3"),

    # P8 (Pyramids) - levels 3-9 only (len 2 and 10-11 excluded where needed)
    "RAD": (3, "P8"), "EAR": (3, "P8"), "ION": (3, "P8"), "EON": (3, "P8"),
    "DORA": (4, "P8"), "RACE": (4, "P8"), "TONI": (4, "P8"), "NOTE": (4, "P8"),
    "ADORN": (5, "P8"), "LECAR": (5, "P8"), "PINTO": (5, "P8"), "TONER": (5, "P8"),
    "ECLAIR": (6, "P8"), "OPTION": (6, "P8"), "ORIENT": (6, "P8"),
    "ROTUNDA": (7, "P8"), "CALIBER": (7, "P8"), "PORTION": (7, "P8"), "INUTERO": (7, "P8"),
    "DURATION": (8, "P8"), "CARBLITE": (8, "P8"), "POSITRON": (8, "P8"), "ROUTINES": (8, "P8"),
    "INUNDATOR": (9, "P8"), "CABRIOLET": (9, "P8"), "RATPOISON": (9, "P8"), "OUTLINERS": (9, "P8"),
    "CIRCLEABOUT": (11, "P8"),  # Confirmed at 94A

    # P9 (Circle) - hidden words
    "ZIP": (3, "P9"), "CHAIRS": (6, "P9"), "QUORUMS": (7, "P9"),
    "FLAMINGO": (8, "P9"), "PUSH": (4, "P9"), "CONVEX": (6, "P9"),
    "HIRPLED": (7, "P9"),

    # Video puzzles
    "CASHTENT": (8, "VIDEO"),
    "ACCRA": (5, "VIDEO"),

    # P4 cities (all confirmed from Team Omega decoding)
    "TORONTO": (7, "P4"), "REGINA": (6, "P4"), "OWENSBORO": (9, "P4"),
    "TOLEDO": (6, "P4"), "ROSWELL": (7, "P4"), "DRESDEN": (7, "P4"),
    "TEMPE": (5, "P4"), "WARSAW": (6, "P4"), "SANJUAN": (7, "P4"),
    "ADELAIDE": (8, "P4"), "DENVER": (6, "P4"), "SEVILLE": (7, "P4"),
    "OTTAWA": (6, "P4"), "ANNAPOLIS": (9, "P4"), "AUBURN": (6, "P4"),
    "DOVER": (5, "P4"), "ROCHESTER": (9, "P4"), "ORLANDO": (7, "P4"),
    "WOODWAY": (7, "P4"),
}

# Filter to answers with lengths that exist in the grid
valid_lengths = set()
for key, (d, r, c, l) in ALL_ENTRIES.items():
    valid_lengths.add(l)

ALL_ANSWERS = {}
excluded_answers = []
for word, (length, src) in ALL_ANSWERS_RAW.items():
    if length in valid_lengths:
        ALL_ANSWERS[word] = (length, src)
    else:
        excluded_answers.append((word, length, src))

print(f"Valid grid lengths: {sorted(valid_lengths)}")
print(f"Answers with valid lengths: {len(ALL_ANSWERS)}")
if excluded_answers:
    print(f"Excluded answers (no matching grid slots):")
    for word, length, src in sorted(excluded_answers, key=lambda x: -x[1]):
        print(f"  {word:20s} len={length:2d} ({src})")

# ============================================================
# CONFIRMED PLACEMENTS (13 from v2 solver)
# ============================================================

CONFIRMED_PLACEMENTS = {
    "36A": "DORA",
    "37D": "ABASH",
    "53D": "ROTUNDA",
    "58A": "PUSH",
    "66A": "HAFT",
    "86D": "ZIP",
    "87D": "TRITE",
    "88A": "ADORN",
    "94A": "CIRCLEABOUT",
    "102A": "PINTO",
    "109A": "TOLEDO",
    "110D": "DENVER",
    "121A": "TONI",
}

# ============================================================
# DICTIONARY SETUP (NLTK + all known answers)
# ============================================================

print("\nBuilding dictionary index...")

# Collect all valid words: NLTK + known answers
all_valid_words = set()

if NLTK_AVAILABLE:
    for w in nltk_words_corpus.words():
        upper = w.upper()
        if upper.isalpha():
            all_valid_words.add(upper)
    print(f"  NLTK words loaded: {len(all_valid_words)}")

# Add ALL known answers (including compound words, proper nouns, etc.)
for word in ALL_ANSWERS_RAW:
    all_valid_words.add(word)

# Add additional crossword-common words that might not be in NLTK
EXTRA_WORDS = {
    # Common crossword abbreviations and fill
    "ERA", "ORE", "ALE", "IRE", "OLE", "ERE", "ARE", "ORE",
    "EEL", "EEK", "OOH", "AAH", "OOF", "OOT", "OON",
    # More proper nouns that might appear
    "MALI", "TEHRAN", "LAGOS", "SUDAN", "OMAN", "ADEN", "WALES",
    "NIGER", "DELHI", "CHAD", "DUBAI", "WUHAN", "DAKAR",
    "GHANA", "TEMPE", "ACCRA",
}
all_valid_words.update(EXTRA_WORDS)

print(f"  Total valid words: {len(all_valid_words)}")

# Index words by length
words_by_length = defaultdict(set)
for w in all_valid_words:
    words_by_length[len(w)].add(w)

# Build fast lookup index: (length, position, letter) -> set of word indices
# This allows O(1) checking of pattern matches via set intersection
print("  Building position-letter index...")
word_lists = {}  # length -> list of words (for index reference)
word_index = {}  # (length, pos, letter) -> set of indices

for length in sorted(words_by_length.keys()):
    if length < 3 or length > 16:
        continue
    wlist = sorted(words_by_length[length])
    word_lists[length] = wlist
    for idx, word in enumerate(wlist):
        for pos, letter in enumerate(word):
            key = (length, pos, letter)
            if key not in word_index:
                word_index[key] = set()
            word_index[key].add(idx)

print("  Index built.")
for length in sorted(word_lists.keys()):
    if 3 <= length <= 16:
        print(f"    Length {length:2d}: {len(word_lists[length]):6d} words")

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_cells(direction, row, col, length):
    """Return list of (row, col) cells for an entry."""
    if direction == 'A':
        return [(row, col + i) for i in range(length)]
    else:
        return [(row + i, col) for i in range(length)]

def has_pattern_match(pattern, length):
    """
    Check if ANY word in the dictionary matches the given pattern.
    pattern: string like "T.L.D." where . is wildcard.
    Uses the position-letter index for fast intersection.
    Returns True if at least one word matches.
    """
    if length not in word_lists:
        return False
    if all(c == '.' for c in pattern):
        return True  # Any word matches an all-wildcard pattern

    constrained = [(pos, ch) for pos, ch in enumerate(pattern) if ch != '.']

    # Check each constraint has at least one word
    sets = []
    for pos, letter in constrained:
        key = (length, pos, letter)
        if key not in word_index:
            return False  # No word has this letter at this position
        sets.append(word_index[key])

    # Intersect from smallest set to largest for efficiency
    sets.sort(key=len)
    result = sets[0]
    for s in sets[1:]:
        result = result & s
        if not result:
            return False
    return True

def count_pattern_matches(pattern, length, limit=1000):
    """Count how many words match the pattern (up to limit)."""
    if length not in word_lists:
        return 0
    if all(c == '.' for c in pattern):
        return len(word_lists[length])

    constrained = [(pos, ch) for pos, ch in enumerate(pattern) if ch != '.']

    sets = []
    for pos, letter in constrained:
        key = (length, pos, letter)
        if key not in word_index:
            return 0
        sets.append(word_index[key])

    sets.sort(key=len)
    result = sets[0]
    for s in sets[1:]:
        result = result & s
        if not result:
            return 0
    return min(len(result), limit)

def get_pattern_matches(pattern, length, limit=50):
    """Get actual words matching the pattern."""
    if length not in word_lists:
        return []
    if all(c == '.' for c in pattern):
        return word_lists[length][:limit]

    constrained = [(pos, ch) for pos, ch in enumerate(pattern) if ch != '.']

    sets = []
    for pos, letter in constrained:
        key = (length, pos, letter)
        if key not in word_index:
            return []
        sets.append(word_index[key])

    sets.sort(key=len)
    result = sets[0]
    for s in sets[1:]:
        result = result & s
        if not result:
            return []

    wlist = word_lists[length]
    matches = [wlist[i] for i in sorted(result)]
    return matches[:limit]

# ============================================================
# BUILD CROSSING MAP
# ============================================================

# Map each cell to its across/down entry and position within that entry
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

# crossing_map[entry_key] = [(other_entry_key, my_position, their_position), ...]
crossing_map = defaultdict(list)
for cell in cell_to_across:
    if cell in cell_to_down:
        a_key, a_pos = cell_to_across[cell]
        d_key, d_pos = cell_to_down[cell]
        crossing_map[a_key].append((d_key, a_pos, d_pos))
        crossing_map[d_key].append((a_key, d_pos, a_pos))

# Verify crossing counts
total_crossings = sum(len(v) for v in crossing_map.values()) // 2
print(f"\nCrossing map: {total_crossings} crossing points")

# ============================================================
# SOLVER CLASS
# ============================================================

class CrosswordSolver:
    def __init__(self):
        self.grid = {}           # (row, col) -> letter
        self.placements = {}     # entry_key -> word
        self.available = {}      # word -> (length, source)  -- answers not yet placed
        self.placement_log = []  # list of (entry_key, word, phase, reason)

    def clone(self):
        """Create a deep copy for speculative solving."""
        s = CrosswordSolver()
        s.grid = dict(self.grid)
        s.placements = dict(self.placements)
        s.available = dict(self.available)
        s.placement_log = list(self.placement_log)
        return s

    def place_word(self, entry_key, word, phase="", reason=""):
        """
        Place a word at an entry position.
        Returns True if successful, False if conflict detected.
        """
        d, row, col, length = ALL_ENTRIES[entry_key]
        if len(word) != length:
            return False
        cells = get_cells(d, row, col, length)

        # Check compatibility with existing grid letters
        for i, (r, c) in enumerate(cells):
            if (r, c) in self.grid and self.grid[(r, c)] != word[i]:
                return False

        # Place the word
        for i, (r, c) in enumerate(cells):
            self.grid[(r, c)] = word[i]
        self.placements[entry_key] = word
        if word in self.available:
            del self.available[word]
        self.placement_log.append((entry_key, word, phase, reason))
        return True

    def check_compatible(self, word, entry_key):
        """Check if word is compatible with current grid at entry (no conflicts)."""
        d, row, col, length = ALL_ENTRIES[entry_key]
        if len(word) != length:
            return False
        cells = get_cells(d, row, col, length)
        for i, (r, c) in enumerate(cells):
            if (r, c) in self.grid and self.grid[(r, c)] != word[i]:
                return False
        return True

    def get_entry_pattern(self, entry_key):
        """Get current letter pattern for an entry from the grid."""
        d, row, col, length = ALL_ENTRIES[entry_key]
        cells = get_cells(d, row, col, length)
        pattern = ""
        for r, c in cells:
            if (r, c) in self.grid:
                pattern += self.grid[(r, c)]
            else:
                pattern += "."
        return pattern

    def get_pattern_after_placement(self, entry_key, word, crossing_entry_key):
        """
        If we tentatively place word at entry_key, what pattern does
        crossing_entry_key get?
        """
        # Start with current pattern of crossing entry
        cd, cr, cc, cl = ALL_ENTRIES[crossing_entry_key]
        cells = get_cells(cd, cr, cc, cl)
        pattern = list(self.get_entry_pattern(crossing_entry_key))

        # Apply letters from the tentative placement
        d, row, col, length = ALL_ENTRIES[entry_key]
        word_cells = get_cells(d, row, col, length)
        word_cell_map = {cell: word[i] for i, cell in enumerate(word_cells)}

        for i, cell in enumerate(cells):
            if cell in word_cell_map:
                pattern[i] = word_cell_map[cell]

        return "".join(pattern)

    def evaluate_placement(self, word, entry_key):
        """
        Evaluate placing word at entry_key.
        Returns (valid, n_impossible, n_crossings, detail_str)
          valid: True if no crossing becomes impossible
          n_impossible: number of crossings with zero dictionary matches
          n_crossings: total number of crossings checked
        """
        d, row, col, length = ALL_ENTRIES[entry_key]

        if not self.check_compatible(word, entry_key):
            return False, 0, 0, "grid conflict"

        total_crossings = 0
        impossible_crossings = 0
        impossible_details = []

        for crossing_entry, my_pos, their_pos in crossing_map[entry_key]:
            # If crossing entry is already placed, just verify letter match
            if crossing_entry in self.placements:
                placed = self.placements[crossing_entry]
                if placed[their_pos] != word[my_pos]:
                    return False, 0, 0, f"conflict with placed {crossing_entry}={placed}"
                continue

            total_crossings += 1

            # Get pattern for crossing entry after this tentative placement
            pattern = self.get_pattern_after_placement(entry_key, word, crossing_entry)
            cl = ALL_ENTRIES[crossing_entry][3]

            # Check if any valid word matches this pattern
            if not has_pattern_match(pattern, cl):
                impossible_crossings += 1
                impossible_details.append(f"{crossing_entry}[{their_pos}]={word[my_pos]} pattern={pattern}")

        valid = (impossible_crossings == 0)
        detail = f"{impossible_crossings}/{total_crossings} impossible"
        if impossible_details:
            detail += ": " + "; ".join(impossible_details[:3])

        return valid, impossible_crossings, total_crossings, detail

    # ----------------------------------------------------------
    # PHASE 1: Basic constraint propagation
    # ----------------------------------------------------------
    def phase1_basic_propagation(self):
        """
        Place answers where:
        - Only one known answer fits an entry (right length + grid compatible), OR
        - Only one entry can accept a given known answer
        Returns number of new placements.
        """
        total_new = 0
        changed = True
        iteration = 0

        while changed:
            changed = False
            iteration += 1
            unplaced_entries = {k: ALL_ENTRIES[k] for k in ALL_ENTRIES if k not in self.placements}

            # For each unplaced entry, find which known answers fit
            for entry_key in sorted(unplaced_entries.keys(), key=lambda k: int(k[:-1])):
                d, row, col, length = unplaced_entries[entry_key]
                fitting = [w for w, (wl, _) in self.available.items()
                          if wl == length and self.check_compatible(w, entry_key)]
                if len(fitting) == 1:
                    if self.place_word(entry_key, fitting[0], "P1", f"only answer for {entry_key}"):
                        changed = True
                        total_new += 1

            # For each unplaced answer, find which entries can accept it
            for word in list(self.available.keys()):
                wlen, _ = self.available[word]
                fitting_entries = [k for k in unplaced_entries
                                 if ALL_ENTRIES[k][3] == wlen and self.check_compatible(word, k)]
                if len(fitting_entries) == 1:
                    if self.place_word(fitting_entries[0], word, "P1", f"only slot for {word}"):
                        changed = True
                        total_new += 1

        return total_new

    # ----------------------------------------------------------
    # PHASE 2: Dictionary-aided elimination
    # ----------------------------------------------------------
    def phase2_dict_elimination(self):
        """
        For each unplaced answer, test each possible entry position.
        Reject positions where placement creates impossible crossings.
        If only one valid position remains, place the word.
        Similarly, for each entry, if only one known answer produces valid crossings, place it.
        Returns number of new placements.
        """
        total_new = 0
        changed = True
        iteration = 0

        while changed:
            changed = False
            iteration += 1
            unplaced_entries = {k: ALL_ENTRIES[k] for k in ALL_ENTRIES if k not in self.placements}

            # Strategy A: For each known answer, find valid positions
            for word in list(self.available.keys()):
                wlen, src = self.available[word]
                valid_positions = []

                for entry_key in unplaced_entries:
                    if ALL_ENTRIES[entry_key][3] != wlen:
                        continue
                    valid, n_imp, n_cross, detail = self.evaluate_placement(word, entry_key)
                    if valid:
                        valid_positions.append((entry_key, n_cross))

                if len(valid_positions) == 1:
                    ek = valid_positions[0][0]
                    if self.place_word(ek, word, "P2", f"dict-elim: only valid pos for {word}"):
                        changed = True
                        total_new += 1
                        print(f"  [P2] {ek} = {word} (only valid position, {src})")
                elif len(valid_positions) == 0 and word in self.available:
                    print(f"  [P2] WARNING: {word} ({src}) has NO valid positions!")

            # Strategy B: For each entry, find valid known answers
            for entry_key in sorted(unplaced_entries.keys(), key=lambda k: int(k[:-1])):
                d, row, col, length = ALL_ENTRIES[entry_key]
                valid_answers = []

                for word, (wlen, src) in self.available.items():
                    if wlen != length:
                        continue
                    valid, n_imp, n_cross, detail = self.evaluate_placement(word, entry_key)
                    if valid:
                        valid_answers.append((word, src))

                if len(valid_answers) == 1:
                    word, src = valid_answers[0]
                    if self.place_word(entry_key, word, "P2", f"dict-elim: only valid answer for {entry_key}"):
                        changed = True
                        total_new += 1
                        print(f"  [P2] {entry_key} = {word} (only valid answer, {src})")

        return total_new

    # ----------------------------------------------------------
    # PHASE 3: Speculative placement with contradiction detection
    # ----------------------------------------------------------
    def phase3_speculative(self, max_depth=2):
        """
        For entries with 2-3 candidate answers, try each one.
        If placing one leads to a contradiction (impossible crossing after
        cascading basic propagation), eliminate it.
        If all but one lead to contradictions, place the survivor.
        Returns number of new placements.
        """
        total_new = 0
        changed = True

        while changed:
            changed = False
            unplaced_entries = {k: ALL_ENTRIES[k] for k in ALL_ENTRIES if k not in self.placements}

            # Collect entries with few candidates
            candidate_list = []
            for word in list(self.available.keys()):
                wlen, src = self.available[word]
                valid_positions = []
                for entry_key in unplaced_entries:
                    if ALL_ENTRIES[entry_key][3] != wlen:
                        continue
                    valid, _, _, _ = self.evaluate_placement(word, entry_key)
                    if valid:
                        valid_positions.append(entry_key)
                if 2 <= len(valid_positions) <= 4:
                    candidate_list.append((word, valid_positions))

            # Sort by number of candidates (try most constrained first)
            candidate_list.sort(key=lambda x: len(x[1]))

            for word, positions in candidate_list:
                if word not in self.available:
                    continue  # Already placed in a previous iteration

                survivors = []
                for entry_key in positions:
                    # Clone solver and try this placement
                    test_solver = self.clone()
                    if not test_solver.place_word(entry_key, word, "P3-test", "speculative"):
                        continue

                    # Run basic propagation on the clone
                    try:
                        test_solver.phase1_basic_propagation()
                        # Check if any entry now has zero valid answers AND zero dict matches
                        contradiction = False
                        for ek in ALL_ENTRIES:
                            if ek in test_solver.placements:
                                continue
                            pattern = test_solver.get_entry_pattern(ek)
                            el = ALL_ENTRIES[ek][3]
                            if any(c != '.' for c in pattern):
                                if not has_pattern_match(pattern, el):
                                    contradiction = True
                                    break
                        if not contradiction:
                            survivors.append(entry_key)
                    except Exception:
                        # Any error means this path is invalid
                        pass

                if len(survivors) == 1:
                    ek = survivors[0]
                    if self.place_word(ek, word, "P3", f"speculative: only non-contradictory position"):
                        changed = True
                        total_new += 1
                        print(f"  [P3] {ek} = {word} (sole survivor of {len(positions)} candidates)")
                        # Run basic propagation to cascade
                        n = self.phase1_basic_propagation()
                        if n > 0:
                            total_new += n
                            print(f"       -> cascaded {n} more placements")
                elif len(survivors) == 0:
                    print(f"  [P3] WARNING: {word} - ALL positions lead to contradictions!")

        return total_new

    # ----------------------------------------------------------
    # PHASE 4: Pattern-based discovery from grid state
    # ----------------------------------------------------------
    def phase4_pattern_discovery(self):
        """
        For each unplaced entry, get its current pattern from the grid.
        Check if any known answer uniquely matches that pattern.
        Also check if the pattern uniquely identifies a dictionary word.
        Returns number of new placements.
        """
        total_new = 0
        changed = True

        while changed:
            changed = False

            for entry_key in sorted(ALL_ENTRIES.keys(), key=lambda k: int(k[:-1])):
                if entry_key in self.placements:
                    continue

                pattern = self.get_entry_pattern(entry_key)
                length = ALL_ENTRIES[entry_key][3]

                # Skip if no letters are known
                if all(c == '.' for c in pattern):
                    continue

                # Check known answers that match this pattern
                matching_known = []
                for word, (wlen, src) in self.available.items():
                    if wlen != length:
                        continue
                    if all(p == '.' or p == w for p, w in zip(pattern, word)):
                        matching_known.append((word, src))

                if len(matching_known) == 1:
                    word, src = matching_known[0]
                    # Verify with dictionary check
                    valid, _, _, _ = self.evaluate_placement(word, entry_key)
                    if valid:
                        if self.place_word(entry_key, word, "P4", f"pattern match: {pattern}"):
                            changed = True
                            total_new += 1
                            print(f"  [P4] {entry_key} = {word} (pattern {pattern} -> unique match, {src})")

        return total_new

    # ----------------------------------------------------------
    # PHASE 5: Mutual exclusion / naked pairs
    # ----------------------------------------------------------
    def phase5_mutual_exclusion(self):
        """
        If two answers A, B can each only go in entries E1, E2, and they're the
        ONLY answers that fit E1 and E2, then we know {A,B} fills {E1,E2}.
        Try both assignments and use contradiction detection to resolve.
        Returns number of new placements.
        """
        total_new = 0
        unplaced_entries = {k: ALL_ENTRIES[k] for k in ALL_ENTRIES if k not in self.placements}

        # Build word -> valid positions map
        word_positions = {}
        for word in list(self.available.keys()):
            wlen, src = self.available[word]
            valid = []
            for entry_key in unplaced_entries:
                if ALL_ENTRIES[entry_key][3] != wlen:
                    continue
                if self.check_compatible(word, entry_key):
                    v, _, _, _ = self.evaluate_placement(word, entry_key)
                    if v:
                        valid.append(entry_key)
            if valid:
                word_positions[word] = valid

        # Build entry -> valid words map
        entry_words = defaultdict(list)
        for word, positions in word_positions.items():
            for pos in positions:
                entry_words[pos].append(word)

        # Look for naked pairs: two words that share exactly 2 positions,
        # and those positions each have exactly those 2 words as candidates
        words_with_2_pos = [(w, pos) for w, pos in word_positions.items() if len(pos) == 2]

        for i, (w1, pos1) in enumerate(words_with_2_pos):
            for j, (w2, pos2) in enumerate(words_with_2_pos):
                if j <= i:
                    continue
                if set(pos1) == set(pos2) and len(pos1) == 2:
                    e1, e2 = pos1
                    wlen1, _ = self.available.get(w1, (0, ""))
                    wlen2, _ = self.available.get(w2, (0, ""))
                    if wlen1 != wlen2:
                        continue
                    # Check that these are the only 2 words for these entries
                    if set(entry_words.get(e1, [])) == {w1, w2} and \
                       set(entry_words.get(e2, [])) == {w1, w2}:
                        print(f"  [P5] Naked pair: {w1}/{w2} in {e1}/{e2}")
                        # Try w1->e1, w2->e2
                        test1 = self.clone()
                        ok1 = test1.place_word(e1, w1, "P5-test", "")
                        ok1 = ok1 and test1.place_word(e2, w2, "P5-test", "")
                        contradiction1 = False
                        if ok1:
                            test1.phase1_basic_propagation()
                            for ek in ALL_ENTRIES:
                                if ek in test1.placements:
                                    continue
                                pat = test1.get_entry_pattern(ek)
                                if any(c != '.' for c in pat):
                                    if not has_pattern_match(pat, ALL_ENTRIES[ek][3]):
                                        contradiction1 = True
                                        break

                        # Try w1->e2, w2->e1
                        test2 = self.clone()
                        ok2 = test2.place_word(e1, w2, "P5-test", "")
                        ok2 = ok2 and test2.place_word(e2, w1, "P5-test", "")
                        contradiction2 = False
                        if ok2:
                            test2.phase1_basic_propagation()
                            for ek in ALL_ENTRIES:
                                if ek in test2.placements:
                                    continue
                                pat = test2.get_entry_pattern(ek)
                                if any(c != '.' for c in pat):
                                    if not has_pattern_match(pat, ALL_ENTRIES[ek][3]):
                                        contradiction2 = True
                                        break

                        if ok1 and not contradiction1 and (not ok2 or contradiction2):
                            print(f"       -> Resolved: {e1}={w1}, {e2}={w2}")
                            self.place_word(e1, w1, "P5", f"naked pair with {w2}")
                            self.place_word(e2, w2, "P5", f"naked pair with {w1}")
                            total_new += 2
                        elif ok2 and not contradiction2 and (not ok1 or contradiction1):
                            print(f"       -> Resolved: {e1}={w2}, {e2}={w1}")
                            self.place_word(e1, w2, "P5", f"naked pair with {w1}")
                            self.place_word(e2, w1, "P5", f"naked pair with {w2}")
                            total_new += 2
                        else:
                            print(f"       -> Could not resolve (both valid or both contradicted)")

        return total_new

    # ----------------------------------------------------------
    # PHASE 6: Relaxed dictionary constraints
    # ----------------------------------------------------------
    def phase6_relaxed_dict(self, max_impossible=1):
        """
        Like Phase 2, but allows up to max_impossible dictionary-failed crossings.
        Only for high-confidence answers (P3 DEFINITIVE, P8 confirmed, P4 confirmed).
        If only one position has <= max_impossible failed crossings, place it.
        Returns number of new placements.
        """
        HIGH_CONF_SOURCES = {"P3", "P8", "P4", "P1", "P9"}
        total_new = 0
        changed = True

        while changed:
            changed = False
            unplaced_entries = {k: ALL_ENTRIES[k] for k in ALL_ENTRIES if k not in self.placements}

            # For each high-confidence answer, find positions with few impossible crossings
            for word in list(self.available.keys()):
                wlen, src = self.available[word]
                if src not in HIGH_CONF_SOURCES:
                    continue

                best_positions = []  # (entry_key, n_impossible, n_total)

                for entry_key in unplaced_entries:
                    if ALL_ENTRIES[entry_key][3] != wlen:
                        continue
                    if not self.check_compatible(word, entry_key):
                        continue

                    valid, n_imp, n_cross, detail = self.evaluate_placement(word, entry_key)
                    if n_imp <= max_impossible and n_cross > 0:
                        best_positions.append((entry_key, n_imp, n_cross))
                    elif valid:  # n_imp == 0
                        best_positions.append((entry_key, 0, n_cross))

                if len(best_positions) == 1:
                    ek, n_imp, n_cross = best_positions[0]
                    tag = "relaxed" if n_imp > 0 else "strict-ok"
                    if self.place_word(ek, word, "P6", f"{tag}: {n_imp}/{n_cross} impossible crossings"):
                        changed = True
                        total_new += 1
                        print(f"  [P6] {ek} = {word} ({tag}, {n_imp} impossible of {n_cross} crossings, {src})")

            # Also: for entries, find if only one answer works with relaxed constraints
            for entry_key in sorted(unplaced_entries.keys(), key=lambda k: int(k[:-1])):
                d, row, col, length = ALL_ENTRIES[entry_key]
                candidates = []

                for word, (wlen, src) in self.available.items():
                    if wlen != length:
                        continue
                    if src not in HIGH_CONF_SOURCES:
                        continue
                    if not self.check_compatible(word, entry_key):
                        continue

                    valid, n_imp, n_cross, detail = self.evaluate_placement(word, entry_key)
                    if n_imp <= max_impossible:
                        candidates.append((word, n_imp, n_cross, src))

                if len(candidates) == 1:
                    word, n_imp, n_cross, src = candidates[0]
                    tag = "relaxed" if n_imp > 0 else "strict-ok"
                    if self.place_word(entry_key, word, "P6", f"{tag}: only candidate"):
                        changed = True
                        total_new += 1
                        print(f"  [P6] {entry_key} = {word} ({tag}, only candidate, {n_imp} impossible, {src})")

        return total_new

    # ----------------------------------------------------------
    # PHASE 7: Dictionary fill for unknown entries
    # ----------------------------------------------------------
    def phase7_dict_fill(self):
        """
        For entries where NO known answer fits but the pattern from crossings
        uniquely identifies a dictionary word, fill it in.
        This helps generate more crossing constraints for other entries.
        Returns number of new placements.
        """
        total_new = 0
        changed = True

        while changed:
            changed = False

            for entry_key in sorted(ALL_ENTRIES.keys(), key=lambda k: int(k[:-1])):
                if entry_key in self.placements:
                    continue

                pattern = self.get_entry_pattern(entry_key)
                length = ALL_ENTRIES[entry_key][3]
                known_count = sum(1 for c in pattern if c != '.')

                # Only try if we have substantial information (>=40% of letters known)
                if known_count < max(2, length * 0.4):
                    continue

                # Check if pattern uniquely identifies a word
                matches = get_pattern_matches(pattern, length, limit=5)

                if len(matches) == 1:
                    word = matches[0]
                    # Extra validation: make sure placing this doesn't create impossible crossings
                    valid, n_imp, _, _ = self.evaluate_placement(word, entry_key)
                    if valid:
                        if self.place_word(entry_key, word, "P7", f"unique dict match for pattern {pattern}"):
                            changed = True
                            total_new += 1
                            print(f"  [P7] {entry_key} = {word} (unique dictionary match for [{pattern}])")

        return total_new

    # ----------------------------------------------------------
    # DIAGNOSTICS
    # ----------------------------------------------------------
    def diagnose_unplaceable(self, word):
        """Show detailed diagnostics for why an answer can't be placed."""
        wlen, src = ALL_ANSWERS_RAW.get(word, (len(word), "???"))
        print(f"\n  Diagnosing: {word} (len={wlen}, {src})")
        unplaced = {k: ALL_ENTRIES[k] for k in ALL_ENTRIES if k not in self.placements}

        for entry_key in sorted(unplaced.keys(), key=lambda k: int(k[:-1])):
            if ALL_ENTRIES[entry_key][3] != wlen:
                continue

            compatible = self.check_compatible(word, entry_key)
            if not compatible:
                # Show which cell conflicts
                d, row, col, length = ALL_ENTRIES[entry_key]
                cells = get_cells(d, row, col, length)
                conflicts = []
                for i, (r, c) in enumerate(cells):
                    if (r, c) in self.grid and self.grid[(r, c)] != word[i]:
                        conflicts.append(f"pos{i}:grid={self.grid[(r,c)]},need={word[i]}")
                print(f"    {entry_key}: GRID CONFLICT - {'; '.join(conflicts)}")
                continue

            valid, n_imp, n_cross, detail = self.evaluate_placement(word, entry_key)
            if valid:
                print(f"    {entry_key}: VALID ({n_cross} crossings all OK)")
            else:
                print(f"    {entry_key}: BLOCKED - {detail}")

    # ----------------------------------------------------------
    # REPORTING
    # ----------------------------------------------------------
    def print_grid(self):
        """Print the current grid state."""
        print("     " + "".join(f"{i%10}" for i in range(25)))
        for r in range(25):
            row_str = f"R{r:2d}| "
            for c in range(25):
                if (r, c) in BLACK_CELLS:
                    row_str += "#"
                elif (r, c) in self.grid:
                    row_str += self.grid[(r, c)]
                else:
                    row_str += "."
            print(row_str)

    def print_placements(self):
        """Print all placed entries."""
        for ek in sorted(self.placements.keys(), key=lambda k: int(k[:-1])):
            d, r, c, l = ALL_ENTRIES[ek]
            word = self.placements[ek]
            # Find the phase/reason from log
            phase = ""
            reason = ""
            for log_ek, log_word, log_phase, log_reason in self.placement_log:
                if log_ek == ek:
                    phase = log_phase
                    reason = log_reason
                    break
            src = ALL_ANSWERS_RAW.get(word, (0, "???"))[1]
            print(f"  {ek:6s} = {word:16s} at ({r:2d},{c:2d}) len={l:2d}  [{phase}] {src}")

    def print_remaining_analysis(self):
        """Show unplaced answers and their candidate positions."""
        print(f"\n--- Unplaced answers ({len(self.available)}) ---")
        unplaced_entries = {k: ALL_ENTRIES[k] for k in ALL_ENTRIES if k not in self.placements}

        for word in sorted(self.available.keys()):
            wlen, src = self.available[word]
            valid_positions = []
            for entry_key in sorted(unplaced_entries.keys(), key=lambda k: int(k[:-1])):
                if ALL_ENTRIES[entry_key][3] != wlen:
                    continue
                valid, n_imp, n_cross, detail = self.evaluate_placement(word, entry_key)
                if valid:
                    valid_positions.append(entry_key)

            pos_str = ", ".join(valid_positions) if valid_positions else "NONE"
            print(f"  {word:16s} (len={wlen}, {src:6s}): {len(valid_positions):2d} positions -> {pos_str}")

    def print_entry_analysis(self):
        """Show unplaced entries and what could go in them."""
        print(f"\n--- Unplaced entries with known-answer candidates ---")
        unplaced_entries = {k: ALL_ENTRIES[k] for k in ALL_ENTRIES if k not in self.placements}

        for entry_key in sorted(unplaced_entries.keys(), key=lambda k: int(k[:-1])):
            d, row, col, length = ALL_ENTRIES[entry_key]
            pattern = self.get_entry_pattern(entry_key)
            known_count = sum(1 for c in pattern if c != '.')

            candidates = []
            for word, (wlen, src) in self.available.items():
                if wlen != length:
                    continue
                valid, _, _, _ = self.evaluate_placement(word, entry_key)
                if valid:
                    candidates.append(f"{word}({src})")

            if candidates or known_count > 0:
                print(f"  {entry_key:6s} len={length:2d} at ({row:2d},{col:2d}) pattern=[{pattern}] "
                      f"known_letters={known_count}: {', '.join(candidates) if candidates else '(no known answers fit)'}")

    def print_theme_entries(self):
        """Show theme entry status."""
        print(f"\n--- Theme Entry Status ---")
        theme_across = [25, 50, 73, 114, 138, 167]
        theme_down = [19, 78]

        for num in theme_across:
            ek = f"{num}A"
            d, r, c, l = ALL_ENTRIES[ek]
            pattern = self.get_entry_pattern(ek)
            known = sum(1 for ch in pattern if ch != '.')
            print(f"  {ek}: len={l} pattern=[{pattern}] ({known}/{l} known)")

        for num in theme_down:
            ek = f"{num}D"
            d, r, c, l = ALL_ENTRIES[ek]
            pattern = self.get_entry_pattern(ek)
            known = sum(1 for ch in pattern if ch != '.')
            print(f"  {ek}: len={l} pattern=[{pattern}] ({known}/{l} known)")


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    solver = CrosswordSolver()

    # Load all known answers
    solver.available = dict(ALL_ANSWERS)

    # Remove the three extra length-11 P8 answers that can't fit (only one 11-slot: 94A)
    for extra in ["TURNONADIME", "OUTFORASPIN", "REVOLUTIONS"]:
        if extra in solver.available:
            del solver.available[extra]
            print(f"Removed {extra} (no slot available, 94A taken by CIRCLEABOUT)")

    # Place confirmed entries
    print(f"\n{'='*70}")
    print("PLACING 13 CONFIRMED ENTRIES")
    print(f"{'='*70}")
    for entry_key, word in CONFIRMED_PLACEMENTS.items():
        ok = solver.place_word(entry_key, word, "CONF", "confirmed from v2 solver")
        if ok:
            print(f"  {entry_key} = {word}")
        else:
            print(f"  FAILED to place {entry_key} = {word}!")

    print(f"\nConfirmed placements: {len(solver.placements)}")
    print(f"Remaining known answers: {len(solver.available)}")

    # Phase 1
    print(f"\n{'='*70}")
    print("PHASE 1: Basic Constraint Propagation")
    print(f"{'='*70}")
    n1 = solver.phase1_basic_propagation()
    print(f"Phase 1 result: {n1} new placements")
    print(f"Total placed: {len(solver.placements)}")

    # Phase 2
    print(f"\n{'='*70}")
    print("PHASE 2: Dictionary-Aided Elimination")
    print(f"{'='*70}")
    n2 = solver.phase2_dict_elimination()
    print(f"Phase 2 result: {n2} new placements")
    print(f"Total placed: {len(solver.placements)}")

    # After Phase 2, run Phase 1 again to cascade
    if n2 > 0:
        print(f"\n  Re-running Phase 1 to cascade...")
        n1b = solver.phase1_basic_propagation()
        print(f"  Phase 1 cascade: {n1b} more placements")

    # Phase 4 (pattern discovery - quick, run before expensive phase 3)
    print(f"\n{'='*70}")
    print("PHASE 4: Pattern-Based Discovery")
    print(f"{'='*70}")
    n4 = solver.phase4_pattern_discovery()
    print(f"Phase 4 result: {n4} new placements")
    print(f"Total placed: {len(solver.placements)}")

    if n4 > 0:
        print(f"\n  Re-running Phase 1+2 to cascade...")
        n1c = solver.phase1_basic_propagation()
        n2c = solver.phase2_dict_elimination()
        print(f"  Cascade: {n1c + n2c} more placements")

    # Phase 3 (speculative - expensive)
    print(f"\n{'='*70}")
    print("PHASE 3: Speculative Placement with Contradiction Detection")
    print(f"{'='*70}")
    n3 = solver.phase3_speculative()
    print(f"Phase 3 result: {n3} new placements")
    print(f"Total placed: {len(solver.placements)}")

    if n3 > 0:
        # Re-run all earlier phases to cascade
        print(f"\n  Re-running Phases 1+2+4 to cascade...")
        nx = solver.phase1_basic_propagation()
        nx += solver.phase2_dict_elimination()
        nx += solver.phase4_pattern_discovery()
        nx += solver.phase1_basic_propagation()
        print(f"  Cascade: {nx} more placements")

    # Phase 5 (mutual exclusion)
    print(f"\n{'='*70}")
    print("PHASE 5: Mutual Exclusion / Naked Pairs")
    print(f"{'='*70}")
    n5 = solver.phase5_mutual_exclusion()
    print(f"Phase 5 result: {n5} new placements")
    print(f"Total placed: {len(solver.placements)}")

    if n5 > 0:
        nx = solver.phase1_basic_propagation()
        nx += solver.phase2_dict_elimination()
        nx += solver.phase4_pattern_discovery()
        print(f"  Cascade: {nx} more placements")

    # Phase 6 (relaxed dictionary)
    print(f"\n{'='*70}")
    print("PHASE 6: Relaxed Dictionary Constraints (allow 1 impossible crossing)")
    print(f"{'='*70}")
    n6 = solver.phase6_relaxed_dict(max_impossible=1)
    print(f"Phase 6 result: {n6} new placements")
    print(f"Total placed: {len(solver.placements)}")

    if n6 > 0:
        print(f"\n  Re-running all phases to cascade...")
        nx = solver.phase1_basic_propagation()
        nx += solver.phase2_dict_elimination()
        nx += solver.phase4_pattern_discovery()
        nx += solver.phase6_relaxed_dict(max_impossible=1)
        nx += solver.phase1_basic_propagation()
        print(f"  Cascade: {nx} more placements")

    # Phase 7 (dictionary fill for unknown entries)
    print(f"\n{'='*70}")
    print("PHASE 7: Dictionary Fill for Unknown Entries")
    print(f"{'='*70}")
    n7 = solver.phase7_dict_fill()
    print(f"Phase 7 result: {n7} new placements")
    print(f"Total placed: {len(solver.placements)}")

    if n7 > 0:
        # Cascade everything
        print(f"\n  Cascading all phases...")
        total_cascade = 0
        for _ in range(3):
            nx = solver.phase1_basic_propagation()
            nx += solver.phase2_dict_elimination()
            nx += solver.phase4_pattern_discovery()
            nx += solver.phase6_relaxed_dict(max_impossible=1)
            nx += solver.phase7_dict_fill()
            total_cascade += nx
            if nx == 0:
                break
        print(f"  Total cascade: {total_cascade} more placements")

    TOTAL_ENTRY_SLOTS = len(ALL_ENTRIES)  # 188 (93 across + 95 down)

    # Final output
    print(f"\n{'='*70}")
    print(f"FINAL RESULTS: {len(solver.placements)} / {TOTAL_ENTRY_SLOTS} entry slots placed")
    print(f"{'='*70}")

    solver.print_placements()

    print(f"\n{'='*70}")
    print("FINAL GRID STATE")
    print(f"{'='*70}")
    solver.print_grid()

    solver.print_theme_entries()

    # Diagnose key unplaceable answers
    print(f"\n{'='*70}")
    print("DIAGNOSTICS: Why can't these high-confidence answers be placed?")
    print(f"{'='*70}")
    diagnose_words = []
    for word in sorted(solver.available.keys()):
        wlen, src = solver.available[word]
        if src in {"P3", "P8"} and wlen in valid_lengths:
            # Check if it truly has 0 positions
            has_any = False
            for ek in ALL_ENTRIES:
                if ek in solver.placements:
                    continue
                if ALL_ENTRIES[ek][3] != wlen:
                    continue
                if solver.check_compatible(word, ek):
                    has_any = True
                    break
            if has_any:
                diagnose_words.append(word)

    # Only diagnose a sample to keep output manageable
    for word in diagnose_words[:8]:
        solver.diagnose_unplaceable(word)

    solver.print_entry_analysis()
    solver.print_remaining_analysis()

    # Summary statistics
    print(f"\n{'='*70}")
    print("SUMMARY STATISTICS")
    print(f"{'='*70}")
    print(f"Total entry slots in grid: {TOTAL_ENTRY_SLOTS} (93 across + 95 down)")
    print(f"Entries placed: {len(solver.placements)}")
    print(f"Known answers remaining (unplaced): {len(solver.available)}")
    print(f"Unknown entries (no known answer): {TOTAL_ENTRY_SLOTS - len(solver.placements)}")

    placed_by_source = defaultdict(int)
    for word in solver.placements.values():
        src = ALL_ANSWERS_RAW.get(word, (0, "???"))[1]
        placed_by_source[src] += 1
    print(f"\nPlacements by source:")
    for src in sorted(placed_by_source.keys()):
        print(f"  {src}: {placed_by_source[src]}")

    placed_by_phase = defaultdict(int)
    for _, _, phase, _ in solver.placement_log:
        placed_by_phase[phase] += 1
    print(f"\nPlacements by phase:")
    for phase in sorted(placed_by_phase.keys()):
        print(f"  {phase}: {placed_by_phase[phase]}")

    # Count filled cells
    filled = len(solver.grid)
    total_white = 525
    print(f"\nGrid cells filled: {filled} / {total_white} white cells ({100*filled/total_white:.1f}%)")

    return solver


if __name__ == "__main__":
    solver = main()
