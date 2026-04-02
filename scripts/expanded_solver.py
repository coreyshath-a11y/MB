#!/usr/bin/env python3
"""
Expanded Crossword Solver - Testing ORGANIC hypothesis at 104D
Builds on 17 confirmed placements with aggressive constraint propagation
"""

import re
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict

# Grid dimensions
GRID_SIZE = 25

# Entry data: number -> (row, col, length, direction)
ENTRIES = {}

# Parse entry data
ACROSS_DATA = [
    "1A(0,0,7)", "8A(0,9,6)", "14A(0,17,8)", "22A(1,0,7)", "23A(1,8,7)", "24A(1,17,8)",
    "25A(2,0,16)", "28A(2,17,8)", "29A(3,0,4)", "30A(3,5,5)", "31A(3,11,3)", "32A(3,15,5)",
    "34A(3,21,4)", "35A(4,0,4)", "36A(4,7,4)", "38A(4,12,9)", "41A(4,22,3)", "42A(5,0,4)",
    "43A(5,5,3)", "45A(5,9,4)", "47A(5,14,4)", "48A(5,20,5)", "50A(6,0,16)", "54A(6,17,6)",
    "57A(7,0,7)", "58A(7,8,4)", "59A(7,13,4)", "61A(7,18,6)", "63A(8,0,3)", "64A(8,4,5)",
    "66A(8,10,4)", "68A(8,16,4)", "70A(8,21,4)", "72A(9,3,6)", "73A(9,11,14)", "77A(10,1,3)",
    "79A(10,5,3)", "80A(10,10,6)", "81A(10,17,4)", "82A(10,22,3)", "83A(11,0,5)", "85A(11,6,5)",
    "88A(11,12,5)", "90A(11,18,3)", "91A(11,22,3)", "92A(12,0,6)", "94A(12,7,11)", "97A(12,19,6)",
    "99A(13,0,3)", "100A(13,4,3)", "102A(13,8,5)", "103A(13,14,5)", "105A(13,20,5)", "106A(14,0,3)",
    "107A(14,4,4)", "109A(14,9,6)", "111A(14,17,3)", "113A(14,21,3)", "114A(15,0,14)", "117A(15,16,6)",
    "119A(16,0,4)", "120A(16,5,4)", "121A(16,11,4)", "123A(16,16,5)", "124A(16,22,3)", "127A(17,1,6)",
    "129A(17,8,4)", "132A(17,13,4)", "134A(17,18,7)", "136A(18,2,6)", "138A(18,9,16)", "141A(19,0,5)",
    "143A(19,7,4)", "145A(19,12,4)", "146A(19,17,3)", "147A(19,21,4)", "148A(20,0,3)", "149A(20,4,9)",
    "153A(20,14,4)", "155A(20,21,4)", "156A(21,0,4)", "158A(21,5,5)", "159A(21,11,3)", "161A(21,15,5)",
    "164A(21,21,4)", "165A(22,0,8)", "167A(22,9,16)", "171A(23,0,8)", "172A(23,10,7)", "173A(23,18,7)",
    "174A(24,0,8)", "175A(24,10,6)", "176A(24,18,7)"
]

DOWN_DATA = [
    "1D(0,0,9)", "2D(0,1,9)", "3D(0,2,9)", "4D(0,3,8)", "5D(0,4,3)", "6D(0,5,4)", "7D(0,6,4)",
    "8D(0,9,8)", "9D(0,10,3)", "10D(0,11,4)", "11D(0,12,7)", "12D(0,13,5)", "13D(0,14,3)",
    "14D(0,17,7)", "15D(0,18,5)", "16D(0,19,5)", "17D(0,20,3)", "18D(0,21,4)", "19D(0,22,15)",
    "20D(0,23,6)", "21D(0,24,6)", "23D(1,8,4)", "26D(2,7,5)", "27D(2,15,6)", "33D(3,16,3)",
    "37D(4,10,5)", "39D(4,14,4)", "40D(4,20,4)", "43D(5,5,6)", "44D(5,6,7)", "46D(5,11,6)",
    "49D(5,21,5)", "51D(6,4,4)", "52D(6,8,4)", "53D(6,13,7)", "55D(6,18,6)", "56D(6,19,7)",
    "60D(7,16,3)", "62D(7,23,8)", "65D(8,7,5)", "67D(8,12,9)", "69D(8,17,3)", "71D(8,24,6)",
    "72D(9,3,4)", "74D(9,14,6)", "75D(9,15,5)", "76D(9,20,5)", "77D(10,1,8)", "78D(10,2,15)",
    "80D(10,10,6)", "83D(11,0,6)", "84D(11,4,5)", "86D(11,8,3)", "87D(11,9,5)", "89D(11,16,3)",
    "93D(12,5,7)", "95D(12,11,7)", "96D(12,17,5)", "98D(12,21,4)", "101D(13,6,6)", "104D(13,18,7)",
    "108D(14,7,3)", "110D(14,13,6)", "112D(14,19,6)", "115D(15,3,5)", "116D(15,8,3)", "117D(15,16,4)",
    "118D(15,20,4)", "122D(16,14,5)", "124D(16,22,9)", "125D(16,23,9)", "126D(16,24,9)", "128D(17,4,4)",
    "130D(17,9,6)", "131D(17,10,4)", "133D(17,15,8)", "135D(17,21,8)", "137D(18,7,7)", "139D(18,12,7)",
    "140D(18,17,5)", "141D(19,0,6)", "142D(19,1,6)", "144D(19,8,3)", "150D(20,5,5)", "151D(20,6,5)",
    "152D(20,11,5)", "154D(20,16,4)", "157D(21,3,4)", "160D(21,13,4)", "162D(21,18,4)", "163D(21,19,4)",
    "166D(22,4,3)", "168D(22,10,3)", "169D(22,14,3)", "170D(22,20,3)"
]

def parse_entry_data():
    """Parse entry position data into ENTRIES dict"""
    for data in ACROSS_DATA:
        match = re.match(r'(\d+)A\((\d+),(\d+),(\d+)\)', data)
        if match:
            num, row, col, length = match.groups()
            ENTRIES[f"{num}A"] = (int(row), int(col), int(length), 'A')

    for data in DOWN_DATA:
        match = re.match(r'(\d+)D\((\d+),(\d+),(\d+)\)', data)
        if match:
            num, row, col, length = match.groups()
            ENTRIES[f"{num}D"] = (int(row), int(col), int(length), 'D')

# Confirmed placements
CONFIRMED = {
    "36A": "DORA",
    "37D": "ABASH",
    "53D": "ROTUNDA",
    "58A": "PUSH",
    "66A": "HAFT",
    "86D": "ZIP",
    "87D": "TRITE",
    "88A": "ADORN",
    "94A": "CIRCLEABOUT",
    "96D": "TONER",
    "102A": "PINTO",
    "103A": "ACHOO",
    "109A": "TOLEDO",
    "110D": "DENVER",
    "117A": "REGINA",
    "121A": "TONI",
    "123A": "ERASE"
}

# All confirmed puzzle answers
PUZZLE_ANSWERS = [
    # P1
    "ACHOO", "TYPHOON", "SCHOOL", "HOODWINK", "OHSHOOT", "OHIOAN", "HULAHOOP", "HOODIE",
    "HOOVERDAM", "DHOW", "ROBINHOOD", "WAHOO",
    # P3
    "HAFT", "DITHERING", "HOWITZERS", "SCENARIO", "ABASH", "NEUROTIC", "HEARTED", "HIGHHEELS",
    "SCREENER", "INTRODUCTIONS", "MATTER", "OPERA", "ALLUSIONS", "RESISTIVE", "ABSOLUTE",
    "ERASE", "TEAMSEAS", "TRITE", "MUSTERS",
    # P8
    "RA", "RAD", "DORA", "ADORN", "ROTUNDA", "DURATION", "INUNDATOR", "TRADEUNION",
    "TURNONADIME", "ER", "EAR", "RACE", "LECAR", "ECLAIR", "CALIBER", "CARBLITE",
    "CABRIOLET", "ORBICULATE", "CIRCLEABOUT", "OI", "ION", "TONI", "PINTO", "OPTION",
    "PORTION", "POSITRON", "RATPOISON", "STAINPROOF", "OUTFORASPIN", "NO", "EON",
    "NOTE", "TONER", "ORIENT", "INUTERO", "ROUTINES", "OUTLINERS", "RESOLUTION",
    "REVOLUTIONS", "ZIP",
    # P9
    "CHAIRS", "QUORUMS", "FLAMINGO", "PUSH", "CONVEX", "HIRPLED",
    # P4 cities
    "TORONTO", "REGINA", "OWENSBORO", "TOLEDO", "ROSWELL", "DRESDEN", "TEMPE", "WARSAW",
    "SANJUAN", "ADELAIDE", "DENVER", "SEVILLE", "OTTAWA", "WILMINGTON", "SACRAMENTO",
    "ANNAPOLIS", "AUBURN", "DOVER", "ROCHESTER", "ORLANDO", "WOODWAY"
]

# Convert to uppercase and deduplicate
PUZZLE_ANSWERS = sorted(set(word.upper() for word in PUZZLE_ANSWERS))

class CrosswordSolver:
    def __init__(self):
        parse_entry_data()
        self.grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.placements = {}
        self.dictionary = self.load_dictionary()

    def load_dictionary(self) -> Set[str]:
        """Load dictionary words"""
        words = set()

        # Try system dictionary first
        dict_paths = ['/usr/share/dict/words', '/usr/dict/words', '/usr/share/dict/american-english']
        loaded = False

        for path in dict_paths:
            try:
                with open(path, 'r') as f:
                    for line in f:
                        word = line.strip().upper()
                        if word and word.isalpha() and 3 <= len(word) <= 16:
                            words.add(word)
                print(f"Loaded {len(words)} words from {path}")
                loaded = True
                break
            except:
                continue

        # Fallback: add common crossword words
        if not loaded:
            print("Warning: Could not load system dictionary, using minimal word list")
            common_words = [
                "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN", "HER",
                "WAS", "ONE", "OUR", "OUT", "DAY", "GET", "HAS", "HIM", "HIS", "HOW",
                "ITS", "MAY", "NEW", "NOW", "OLD", "SEE", "TWO", "WAY", "WHO", "BOY",
                "DID", "ITS", "LET", "PUT", "SAY", "SHE", "TOO", "USE", "ERA", "ART",
                "ACE", "AGE", "ALE", "APE", "ATE", "AWE", "AXE", "EAR", "EEL", "EGG",
                "ELF", "ERA", "EVE", "EWE", "EYE", "ICE", "ILL", "INK", "INN", "ION",
                "IRE", "OAK", "OAR", "OAT", "ODD", "ODE", "OFT", "OIL", "ORE", "OWE",
                "OWL", "OWN", "AREA", "ARTS", "ASIA", "ATOM", "AUTO", "ABLE", "ACID",
                "ACRE", "ACTS", "AGED", "AGES", "AIDS", "AIMS", "AIRS", "AJAR", "ALAS",
                "ALSO", "AMID", "AMPS", "ANTS", "APEX", "ARCH", "AREA", "ARIA", "ARID",
                "ARMS", "ARMY", "ARTY", "ASIA", "ASKS", "ATOM", "ATOP", "AUTO", "AVID"
            ]
            words = set(common_words)

        return words

    def place_word(self, entry: str, word: str) -> bool:
        """Place a word in the grid"""
        if entry not in ENTRIES:
            return False

        row, col, length, direction = ENTRIES[entry]
        word = word.upper()

        if len(word) != length:
            return False

        # Check compatibility with existing letters
        for i, char in enumerate(word):
            if direction == 'A':
                r, c = row, col + i
            else:
                r, c = row + i, col

            if self.grid[r][c] != '.' and self.grid[r][c] != char:
                return False

        # Place the word
        for i, char in enumerate(word):
            if direction == 'A':
                self.grid[row][col + i] = char
            else:
                self.grid[row + i][col] = char

        self.placements[entry] = word
        return True

    def get_pattern(self, entry: str) -> str:
        """Get current pattern for an entry with constraints"""
        if entry not in ENTRIES:
            return ""

        row, col, length, direction = ENTRIES[entry]
        pattern = []

        for i in range(length):
            if direction == 'A':
                pattern.append(self.grid[row][col + i])
            else:
                pattern.append(self.grid[row + i][col])

        return ''.join(pattern)

    def matches_pattern(self, word: str, pattern: str) -> bool:
        """Check if word matches pattern (. = any letter)"""
        if len(word) != len(pattern):
            return False
        return all(p == '.' or p == w for p, w in zip(pattern, word.upper()))

    def get_candidates(self, entry: str, word_list: List[str]) -> List[str]:
        """Get candidate words for an entry"""
        if entry in self.placements:
            return []

        pattern = self.get_pattern(entry)
        _, _, length, _ = ENTRIES[entry]

        candidates = []
        for word in word_list:
            if len(word) == length and self.matches_pattern(word, pattern):
                candidates.append(word)

        return candidates

    def propagate_constraints(self) -> int:
        """Propagate constraints and place words with single candidates"""
        placed = 0
        max_iterations = 50

        for iteration in range(max_iterations):
            made_progress = False

            # Try puzzle answers first
            for entry in sorted(ENTRIES.keys()):
                if entry in self.placements:
                    continue

                candidates = self.get_candidates(entry, PUZZLE_ANSWERS)

                if len(candidates) == 1:
                    word = candidates[0]
                    if self.place_word(entry, word):
                        print(f"  [Iteration {iteration+1}] Placed {entry} = {word} (unique puzzle answer)")
                        made_progress = True
                        placed += 1

            # Try dictionary words
            for entry in sorted(ENTRIES.keys()):
                if entry in self.placements:
                    continue

                candidates = self.get_candidates(entry, list(self.dictionary))

                if len(candidates) == 1:
                    word = candidates[0]
                    if self.place_word(entry, word):
                        print(f"  [Iteration {iteration+1}] Placed {entry} = {word} (unique dictionary word)")
                        made_progress = True
                        placed += 1

            if not made_progress:
                break

        return placed

    def try_all_puzzle_answers(self) -> int:
        """Try placing all puzzle answers in compatible slots"""
        placed = 0

        for word in PUZZLE_ANSWERS:
            if word in self.placements.values():
                continue

            length = len(word)
            compatible_entries = []

            for entry, (row, col, elen, direction) in ENTRIES.items():
                if entry in self.placements:
                    continue
                if elen == length:
                    pattern = self.get_pattern(entry)
                    if self.matches_pattern(word, pattern):
                        compatible_entries.append(entry)

            # If only one compatible entry, place it
            if len(compatible_entries) == 1:
                entry = compatible_entries[0]
                if self.place_word(entry, word):
                    print(f"  Placed {entry} = {word} (unique compatible slot)")
                    placed += 1

        return placed

    def analyze_entry(self, entry: str):
        """Analyze constraints for a specific entry"""
        if entry not in ENTRIES:
            print(f"Entry {entry} not found")
            return

        pattern = self.get_pattern(entry)
        row, col, length, direction = ENTRIES[entry]

        print(f"\n{entry} at ({row},{col}) length {length} direction {direction}")
        print(f"  Pattern: {pattern}")

        if entry in self.placements:
            print(f"  Placed: {self.placements[entry]}")
        else:
            puzzle_candidates = self.get_candidates(entry, PUZZLE_ANSWERS)
            print(f"  Puzzle answer candidates ({len(puzzle_candidates)}): {puzzle_candidates[:10]}")

            dict_candidates = self.get_candidates(entry, list(self.dictionary))
            print(f"  Dictionary candidates ({len(dict_candidates)}): {dict_candidates[:10]}")

    def print_grid_section(self, start_row: int, end_row: int):
        """Print a section of the grid"""
        print(f"\nGrid rows {start_row}-{end_row}:")
        print("   ", end="")
        for c in range(GRID_SIZE):
            print(f"{c%10}", end="")
        print()

        for r in range(start_row, min(end_row + 1, GRID_SIZE)):
            print(f"{r:2} ", end="")
            for c in range(GRID_SIZE):
                print(self.grid[r][c], end="")
            print()

    def get_crossing_entries(self, entry: str) -> List[Tuple[str, int, int]]:
        """Get entries that cross this entry"""
        if entry not in ENTRIES:
            return []

        row, col, length, direction = ENTRIES[entry]
        crossings = []

        for other_entry, (other_row, other_col, other_len, other_dir) in ENTRIES.items():
            if other_entry == entry or other_dir == direction:
                continue

            # Check if they cross
            for i in range(length):
                if direction == 'A':
                    r, c = row, col + i
                else:
                    r, c = row + i, col

                for j in range(other_len):
                    if other_dir == 'A':
                        or_, oc = other_row, other_col + j
                    else:
                        or_, oc = other_row + j, other_col

                    if r == or_ and c == oc:
                        crossings.append((other_entry, i, j))
                        break

        return crossings

    def check_conflicts(self) -> List[str]:
        """Check for entries with impossible patterns"""
        conflicts = []

        for entry in ENTRIES:
            if entry in self.placements:
                continue

            pattern = self.get_pattern(entry)
            known = sum(1 for c in pattern if c != '.')

            if known >= 4:
                # Check if pattern could match any word
                puzzle_matches = self.get_candidates(entry, PUZZLE_ANSWERS)
                dict_matches = self.get_candidates(entry, list(self.dictionary))

                if len(puzzle_matches) == 0 and len(dict_matches) == 0:
                    conflicts.append(f"{entry}: {pattern} (no matches)")

        return conflicts

def main():
    print("=" * 80)
    print("EXPANDED CROSSWORD SOLVER - Testing ORGANIC Hypothesis")
    print("=" * 80)

    solver = CrosswordSolver()

    # Step 1: Place confirmed entries
    print("\n[STEP 1] Placing 17 confirmed entries...")
    for entry, word in CONFIRMED.items():
        if solver.place_word(entry, word):
            print(f"  ✓ {entry} = {word}")

    print(f"\nPlacements: {len(solver.placements)}")

    # Step 2: Place ORGANIC hypothesis
    print("\n[STEP 2] Placing ORGANIC at 104D (HYPOTHESIS)...")
    if solver.place_word("104D", "ORGANIC"):
        print("  ✓ 104D = ORGANIC")
        print("\n  Analyzing ORGANIC crossings...")
        crossings = solver.get_crossing_entries("104D")
        for cross_entry, pos_self, pos_cross in crossings:
            pattern = solver.get_pattern(cross_entry)
            print(f"    {cross_entry}: {pattern}")
    else:
        print("  ✗ Failed to place ORGANIC")

    print(f"\nPlacements: {len(solver.placements)}")

    # Step 3: First round of constraint propagation
    print("\n[STEP 3] Running constraint propagation...")
    placed = solver.propagate_constraints()
    print(f"\n  Placed {placed} new entries via constraint propagation")
    print(f"  Total placements: {len(solver.placements)}")

    # Step 4: Try all puzzle answers
    print("\n[STEP 4] Trying all puzzle answers in compatible slots...")
    placed = solver.try_all_puzzle_answers()
    print(f"\n  Placed {placed} new entries")
    print(f"  Total placements: {len(solver.placements)}")

    # Step 5: Second round of constraint propagation
    print("\n[STEP 5] Running second constraint propagation...")
    placed = solver.propagate_constraints()
    print(f"\n  Placed {placed} new entries")
    print(f"  Total placements: {len(solver.placements)}")

    # Step 6: Check for conflicts
    print("\n[STEP 6] Checking for impossible patterns...")
    conflicts = solver.check_conflicts()
    if conflicts:
        print(f"  Found {len(conflicts)} entries with no matching words:")
        for conflict in conflicts[:10]:
            print(f"    ⚠ {conflict}")
    else:
        print("  No obvious conflicts detected")

    # Step 7: Analyze key theme entries
    print("\n[STEP 7] Analyzing theme entries...")
    theme_entries = ["25A", "50A", "73A", "114A", "138A", "167A", "19D", "78D"]
    for entry in theme_entries:
        solver.analyze_entry(entry)

    # Step 8: Show grid sections
    print("\n[STEP 8] Partial Grid Display")
    print("\nTop section (rows 0-9):")
    solver.print_grid_section(0, 9)

    print("\nMiddle section (rows 10-19):")
    solver.print_grid_section(10, 19)

    print("\nBottom section (rows 20-24):")
    solver.print_grid_section(20, 24)

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total placements: {len(solver.placements)}")
    print(f"Percentage complete: {len(solver.placements)/176*100:.1f}%")

    print("\nAll placements:")
    for entry in sorted(solver.placements.keys(), key=lambda x: (x[-1], int(x[:-1]))):
        word = solver.placements[entry]
        row, col, length, direction = ENTRIES[entry]
        print(f"  {entry:5} = {word:15} at ({row:2},{col:2})")

    print("\nEntries with highly constrained patterns:")
    constrained = []
    for entry in ENTRIES:
        if entry in solver.placements:
            continue
        pattern = solver.get_pattern(entry)
        known_letters = sum(1 for c in pattern if c != '.')
        if known_letters >= 2:
            puzzle_cands = solver.get_candidates(entry, PUZZLE_ANSWERS)
            dict_cands = solver.get_candidates(entry, list(solver.dictionary))
            constrained.append((entry, pattern, known_letters, len(puzzle_cands), len(dict_cands)))

    constrained.sort(key=lambda x: (-x[2], x[3]))

    for entry, pattern, known, puzzle_count, dict_count in constrained[:20]:
        row, col, length, direction = ENTRIES[entry]
        print(f"  {entry:5} ({row:2},{col:2}): {pattern} | {known} known | {puzzle_count} puzzle | {dict_count} dict")

if __name__ == "__main__":
    main()
