#!/usr/bin/env python3
"""
Theme Entry Mapping Script
Maps newly discovered crossword answers to their exact grid positions in the 25x25 crossword.
Checks for crossing conflicts with all previously confirmed placements.
"""

# ============================================================
# 1. GRID DEFINITION
# ============================================================

GRID_SIZE = 25

# Black cells (row, col)
BLACK_CELLS = {
    (0,7), (0,8), (0,15), (0,16),
    (1,7), (1,15), (1,16),
    (2,16),
    (3,4), (3,10), (3,14), (3,20),
    (4,4), (4,5), (4,6), (4,11), (4,21),
    (5,4), (5,8), (5,13), (5,18), (5,19),
    (6,16), (6,23), (6,24),
    (7,7), (7,12), (7,17), (7,24),
    (8,3), (8,9), (8,14), (8,15), (8,20),
    (9,0), (9,1), (9,2), (9,9), (9,10),
    (10,0), (10,4), (10,8), (10,9), (10,16), (10,21),
    (11,5), (11,11), (11,17), (11,21),
    (12,6), (12,18),
    (13,3), (13,7), (13,13), (13,19),
    (14,3), (14,8), (14,15), (14,16), (14,20), (14,24),
    (15,14), (15,15), (15,22), (15,23), (15,24),
    (16,4), (16,9), (16,10), (16,15), (16,21),
    (17,0), (17,7), (17,12), (17,17),
    (18,0), (18,1), (18,8),
    (19,5), (19,6), (19,11), (19,16), (19,20),
    (20,3), (20,13), (20,18), (20,19), (20,20),
    (21,4), (21,10), (21,14), (21,20),
    (22,8),
    (23,8), (23,9), (23,17),
    (24,8), (24,9), (24,16), (24,17),
}

# Circled cells (row, col)
CIRCLED_CELLS = {
    (0,12), (2,4), (3,8), (3,24), (4,19),
    (10,12), (11,2), (11,22),
    (13,0), (18,7), (19,17), (20,2),
    (22,11), (22,18), (22,24),
    (24,20),
}

# ============================================================
# 2. ENTRY DEFINITIONS
# ============================================================

# Across entries: {entry_number: (row, start_col, length)}
ACROSS = {
    1: (0, 0, 7), 8: (0, 9, 6), 14: (0, 17, 8),
    22: (1, 0, 7), 23: (1, 8, 7), 24: (1, 17, 8),
    25: (2, 0, 16), 28: (2, 17, 8),
    29: (3, 0, 4), 30: (3, 5, 5), 31: (3, 11, 3), 32: (3, 15, 5), 34: (3, 21, 4),
    35: (4, 0, 4), 36: (4, 7, 4), 38: (4, 12, 9), 41: (4, 22, 3),
    42: (5, 0, 4), 43: (5, 5, 3), 45: (5, 9, 4), 47: (5, 14, 4), 48: (5, 20, 5),
    50: (6, 0, 16), 54: (6, 17, 6),
    57: (7, 0, 7), 58: (7, 8, 4), 59: (7, 13, 4), 61: (7, 18, 6),
    63: (8, 0, 3), 64: (8, 4, 5), 66: (8, 10, 4), 68: (8, 16, 4), 70: (8, 21, 4),
    72: (9, 3, 6), 73: (9, 11, 14),
    77: (10, 1, 3), 79: (10, 5, 3), 80: (10, 10, 6), 81: (10, 17, 4), 82: (10, 22, 3),
    83: (11, 0, 5), 85: (11, 6, 5), 88: (11, 12, 5), 90: (11, 18, 3), 91: (11, 22, 3),
    92: (12, 0, 6), 94: (12, 7, 11), 97: (12, 19, 6),
    99: (13, 0, 3), 100: (13, 4, 3), 102: (13, 8, 5), 103: (13, 14, 5), 105: (13, 20, 5),
    106: (14, 0, 3), 107: (14, 4, 4), 109: (14, 9, 6), 111: (14, 17, 3), 113: (14, 21, 3),
    114: (15, 0, 14), 117: (15, 16, 6),
    119: (16, 0, 4), 120: (16, 5, 4), 121: (16, 11, 4), 123: (16, 16, 5), 124: (16, 22, 3),
    127: (17, 1, 6), 129: (17, 8, 4), 132: (17, 13, 4), 134: (17, 18, 7),
    136: (18, 2, 6), 138: (18, 9, 16),
    141: (19, 0, 5), 143: (19, 7, 4), 145: (19, 12, 4), 146: (19, 17, 3), 147: (19, 21, 4),
    148: (20, 0, 3), 149: (20, 4, 9), 153: (20, 14, 4), 155: (20, 21, 4),
    156: (21, 0, 4), 158: (21, 5, 5), 159: (21, 11, 3), 161: (21, 15, 5), 164: (21, 21, 4),
    165: (22, 0, 8), 167: (22, 9, 16),
    171: (23, 0, 8), 172: (23, 10, 7), 173: (23, 18, 7),
    174: (24, 0, 8), 175: (24, 10, 6), 176: (24, 18, 7),
}

# Down entries: {entry_number: (start_row, col, length)}
DOWN = {
    1: (0, 0, 9), 2: (0, 1, 9), 3: (0, 2, 9), 4: (0, 3, 8), 5: (0, 4, 3),
    6: (0, 5, 4), 7: (0, 6, 4), 8: (0, 9, 8), 9: (0, 10, 3), 10: (0, 11, 4),
    11: (0, 12, 7), 12: (0, 13, 5), 13: (0, 14, 3), 14: (0, 17, 7), 15: (0, 18, 5),
    16: (0, 19, 5), 17: (0, 20, 3), 18: (0, 21, 4), 19: (0, 22, 15), 20: (0, 23, 6),
    21: (0, 24, 6),
    23: (1, 8, 4), 26: (2, 7, 5), 27: (2, 15, 6),
    33: (3, 16, 3), 37: (4, 10, 5), 39: (4, 14, 4), 40: (4, 20, 4),
    43: (5, 5, 6), 44: (5, 6, 7), 46: (5, 11, 6), 49: (5, 21, 5),
    51: (6, 4, 4), 52: (6, 8, 4), 53: (6, 13, 7), 55: (6, 18, 6), 56: (6, 19, 7),
    60: (7, 16, 3), 62: (7, 23, 8),
    65: (8, 7, 5), 67: (8, 12, 9), 69: (8, 17, 3), 71: (8, 24, 6),
    72: (9, 3, 4), 74: (9, 14, 6), 75: (9, 15, 5), 76: (9, 20, 5),
    77: (10, 1, 8), 78: (10, 2, 15),
    80: (10, 10, 6), 83: (11, 0, 6), 84: (11, 4, 5), 86: (11, 8, 3), 87: (11, 9, 5),
    89: (11, 16, 3), 93: (12, 5, 7), 95: (12, 11, 7), 96: (12, 17, 5),
    98: (12, 21, 4), 101: (13, 6, 6), 104: (13, 18, 7), 108: (14, 7, 3),
    110: (14, 13, 6), 112: (14, 19, 6),
    115: (15, 3, 5), 116: (15, 8, 3), 117: (15, 16, 4),  # Note: 117 is both across and down
    118: (15, 20, 4), 122: (16, 14, 5),
    124: (16, 22, 9), 125: (16, 23, 9), 126: (16, 24, 9),
    128: (17, 4, 4), 130: (17, 9, 6), 131: (17, 10, 4),
    133: (17, 15, 8), 135: (17, 21, 8), 137: (18, 7, 7),
    139: (18, 12, 7), 140: (18, 17, 5),
    141: (19, 0, 6), 142: (19, 1, 6), 144: (19, 8, 3),
    150: (20, 5, 5), 151: (20, 6, 5), 152: (20, 11, 5), 154: (20, 16, 4),
    157: (21, 3, 4), 160: (21, 13, 4), 162: (21, 18, 4), 163: (21, 19, 4),
    166: (22, 4, 3), 168: (22, 10, 3), 169: (22, 14, 3), 170: (22, 20, 3),
}

# ============================================================
# 3. BUILD GRID AND CROSSING MAPS
# ============================================================

def create_empty_grid():
    """Create a 25x25 grid filled with None (unknown) or '#' (black)."""
    grid = [[None]*GRID_SIZE for _ in range(GRID_SIZE)]
    for (r, c) in BLACK_CELLS:
        grid[r][c] = '#'
    return grid

def get_cells_for_across(entry_num):
    """Return list of (row, col) for an across entry."""
    row, start_col, length = ACROSS[entry_num]
    return [(row, start_col + i) for i in range(length)]

def get_cells_for_down(entry_num):
    """Return list of (row, col) for a down entry."""
    start_row, col, length = DOWN[entry_num]
    return [(start_row + i, col) for i in range(length)]

def build_crossing_map():
    """For each cell, record which across and down entries pass through it."""
    cell_to_entries = {}

    for entry_num, (row, start_col, length) in ACROSS.items():
        for i in range(length):
            cell = (row, start_col + i)
            if cell not in cell_to_entries:
                cell_to_entries[cell] = {}
            cell_to_entries[cell]['across'] = (entry_num, i)  # (entry_num, position_in_entry)

    for entry_num, (start_row, col, length) in DOWN.items():
        for i in range(length):
            cell = (start_row + i, col)
            if cell not in cell_to_entries:
                cell_to_entries[cell] = {}
            cell_to_entries[cell]['down'] = (entry_num, i)

    return cell_to_entries

# ============================================================
# 4. PLACE ENTRIES
# ============================================================

def place_across(grid, entry_num, answer, confirmed_placements, label=""):
    """Place an across entry, checking for conflicts. Returns list of conflicts."""
    row, start_col, length = ACROSS[entry_num]
    conflicts = []

    if len(answer) != length:
        conflicts.append(f"LENGTH MISMATCH: {label}{entry_num}A expects {length} letters, got {len(answer)} ({answer})")
        return conflicts

    for i, ch in enumerate(answer):
        r, c = row, start_col + i
        existing = grid[r][c]
        if existing is not None and existing != '#' and existing.upper() != ch.upper():
            conflicts.append(
                f"CONFLICT at ({r},{c}): {label}{entry_num}A pos {i} wants '{ch}' "
                f"but cell already has '{existing}' (from {confirmed_placements.get((r,c), 'unknown')})"
            )
        else:
            if existing is None or existing == ch.upper():
                grid[r][c] = ch.upper()
                confirmed_placements[(r,c)] = f"{label}{entry_num}A"

    return conflicts

def place_down(grid, entry_num, answer, confirmed_placements, label=""):
    """Place a down entry, checking for conflicts. Returns list of conflicts."""
    start_row, col, length = DOWN[entry_num]
    conflicts = []

    if len(answer) != length:
        conflicts.append(f"LENGTH MISMATCH: {label}{entry_num}D expects {length} letters, got {len(answer)} ({answer})")
        return conflicts

    for i, ch in enumerate(answer):
        r, c = start_row + i, col
        existing = grid[r][c]
        if existing is not None and existing != '#' and existing.upper() != ch.upper():
            conflicts.append(
                f"CONFLICT at ({r},{c}): {label}{entry_num}D pos {i} wants '{ch}' "
                f"but cell already has '{existing}' (from {confirmed_placements.get((r,c), 'unknown')})"
            )
        else:
            if existing is None or existing == ch.upper():
                grid[r][c] = ch.upper()
                confirmed_placements[(r,c)] = f"{label}{entry_num}D"

    return conflicts

def check_across_no_place(grid, entry_num, answer, confirmed_placements, label=""):
    """Check an across entry for conflicts WITHOUT placing it."""
    row, start_col, length = ACROSS[entry_num]
    conflicts = []

    if len(answer) != length:
        conflicts.append(f"LENGTH MISMATCH: {label}{entry_num}A expects {length} letters, got {len(answer)} ({answer})")
        return conflicts

    for i, ch in enumerate(answer):
        r, c = row, start_col + i
        existing = grid[r][c]
        if existing is not None and existing != '#' and existing.upper() != ch.upper():
            conflicts.append(
                f"CONFLICT at ({r},{c}): {label}{entry_num}A pos {i} wants '{ch}' "
                f"but cell already has '{existing}' (from {confirmed_placements.get((r,c), 'unknown')})"
            )

    return conflicts

# ============================================================
# 5. CROSSING ANALYSIS
# ============================================================

def find_crossings_for_across(entry_num, cell_to_entries):
    """Find all down entries that cross a given across entry."""
    row, start_col, length = ACROSS[entry_num]
    crossings = []
    for i in range(length):
        cell = (row, start_col + i)
        if cell in cell_to_entries and 'down' in cell_to_entries[cell]:
            down_entry, down_pos = cell_to_entries[cell]['down']
            crossings.append({
                'cell': cell,
                'across_pos': i,
                'down_entry': down_entry,
                'down_pos': down_pos,
                'down_length': DOWN[down_entry][2],
            })
    return crossings

def find_crossings_for_down(entry_num, cell_to_entries):
    """Find all across entries that cross a given down entry."""
    start_row, col, length = DOWN[entry_num]
    crossings = []
    for i in range(length):
        cell = (start_row + i, col)
        if cell in cell_to_entries and 'across' in cell_to_entries[cell]:
            across_entry, across_pos = cell_to_entries[cell]['across']
            crossings.append({
                'cell': cell,
                'down_pos': i,
                'across_entry': across_entry,
                'across_pos': across_pos,
                'across_length': ACROSS[across_entry][1] + ACROSS[across_entry][2] - 1,  # last col
            })
    return crossings

def report_new_constraints(entry_num, answer, direction, grid, cell_to_entries, confirmed_placements):
    """Report what new letter constraints placing this entry creates at crossing entries."""
    print(f"\n  Crossing constraints from {entry_num}{'A' if direction == 'across' else 'D'} = {answer}:")

    if direction == 'across':
        row, start_col, length = ACROSS[entry_num]
        for i, ch in enumerate(answer):
            cell = (row, start_col + i)
            if cell in cell_to_entries and 'down' in cell_to_entries[cell]:
                down_entry, down_pos = cell_to_entries[cell]['down']
                down_len = DOWN[down_entry][2]
                existing = grid[cell[0]][cell[1]]
                status = ""
                if existing is not None and existing != '#':
                    if existing.upper() == ch.upper():
                        status = " [MATCHES existing]"
                    else:
                        status = f" [CONFLICTS with existing '{existing}']"
                else:
                    status = " [NEW constraint]"

                is_circled = " (CIRCLED)" if cell in CIRCLED_CELLS else ""
                print(f"    Cell ({cell[0]},{cell[1]}){is_circled}: {entry_num}A[{i}]='{ch}' crosses {down_entry}D[{down_pos}] (len {down_len}){status}")
    else:
        start_row, col, length = DOWN[entry_num]
        for i, ch in enumerate(answer):
            cell = (start_row + i, col)
            if cell in cell_to_entries and 'across' in cell_to_entries[cell]:
                across_entry, across_pos = cell_to_entries[cell]['across']
                across_len = ACROSS[across_entry][2]
                existing = grid[cell[0]][cell[1]]
                status = ""
                if existing is not None and existing != '#':
                    if existing.upper() == ch.upper():
                        status = " [MATCHES existing]"
                    else:
                        status = f" [CONFLICTS with existing '{existing}']"
                else:
                    status = " [NEW constraint]"

                is_circled = " (CIRCLED)" if cell in CIRCLED_CELLS else ""
                print(f"    Cell ({cell[0]},{cell[1]}){is_circled}: {entry_num}D[{i}]='{ch}' crosses {across_entry}A[{across_pos}] (len {across_len}){status}")


# ============================================================
# 6. FIND ALL POSSIBLE POSITIONS FOR AN ANSWER
# ============================================================

def find_all_positions(answer, grid):
    """Find all across and down entries where this answer could fit (by length), and check conflicts."""
    length = len(answer)
    results = []

    # Check all across entries of matching length
    for entry_num, (row, start_col, entry_len) in ACROSS.items():
        if entry_len == length:
            conflicts = []
            matches = []
            for i, ch in enumerate(answer):
                r, c = row, start_col + i
                existing = grid[r][c]
                if existing is not None and existing != '#':
                    if existing.upper() == ch.upper():
                        matches.append((r, c, i, ch))
                    else:
                        conflicts.append((r, c, i, ch, existing))
            results.append({
                'entry': f"{entry_num}A",
                'position': (row, start_col),
                'length': entry_len,
                'conflicts': conflicts,
                'matches': matches,
                'feasible': len(conflicts) == 0,
            })

    # Check all down entries of matching length
    for entry_num, (start_row, col, entry_len) in DOWN.items():
        if entry_len == length:
            conflicts = []
            matches = []
            for i, ch in enumerate(answer):
                r, c = start_row + i, col
                existing = grid[r][c]
                if existing is not None and existing != '#':
                    if existing.upper() == ch.upper():
                        matches.append((r, c, i, ch))
                    else:
                        conflicts.append((r, c, i, ch, existing))
            results.append({
                'entry': f"{entry_num}D",
                'position': (start_row, col),
                'length': entry_len,
                'conflicts': conflicts,
                'matches': matches,
                'feasible': len(conflicts) == 0,
            })

    return results


# ============================================================
# 7. PRINT GRID
# ============================================================

def print_grid(grid, title="Current Grid"):
    """Print the grid in a readable format."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print("     " + "".join(str(i % 10) for i in range(25)))
    print("     " + "-"*25)
    for r in range(GRID_SIZE):
        row_str = ""
        for c in range(GRID_SIZE):
            ch = grid[r][c]
            if ch == '#':
                row_str += '#'
            elif ch is None:
                row_str += '.'
            else:
                row_str += ch
        circle_markers = ""
        for c in range(GRID_SIZE):
            if (r, c) in CIRCLED_CELLS and grid[r][c] is not None and grid[r][c] != '#':
                circle_markers += f" ({r},{c})={grid[r][c]}"
        print(f"R{r:2d} |{row_str}{circle_markers}")


# ============================================================
# MAIN
# ============================================================

def main():
    grid = create_empty_grid()
    cell_to_entries = build_crossing_map()
    confirmed_placements = {}

    print("="*70)
    print("  CROSSWORD THEME ENTRY MAPPING - Feb 10, 2026")
    print("="*70)

    # --------------------------------------------------------
    # STEP 1: Place all 17 confirmed entries + 2 hypothetical
    # --------------------------------------------------------
    print("\n" + "="*70)
    print("  STEP 1: Placing 17 confirmed + 2 hypothetical entries")
    print("="*70)

    confirmed_across = {
        36: "DORA",
        58: "PUSH",
        66: "HAFT",
        88: "ADORN",
        94: "CIRCLEABOUT",
        102: "PINTO",
        103: "ACHOO",
        109: "TOLEDO",
        117: "REGINA",
        121: "TONI",
        123: "ERASE",
    }

    confirmed_down = {
        37: "ABASH",
        53: "ROTUNDA",
        86: "ZIP",
        87: "TRITE",
        96: "TONER",
        110: "DENVER",
    }

    hypothetical_across = {
        111: "NRA",
    }

    hypothetical_down = {
        104: "ORGANIC",
    }

    all_conflicts = []

    for entry_num, answer in confirmed_across.items():
        conflicts = place_across(grid, entry_num, answer, confirmed_placements, "CONFIRMED ")
        if conflicts:
            all_conflicts.extend(conflicts)
            for c in conflicts:
                print(f"  !! {c}")
        else:
            print(f"  OK: {entry_num}A = {answer}")

    for entry_num, answer in confirmed_down.items():
        conflicts = place_down(grid, entry_num, answer, confirmed_placements, "CONFIRMED ")
        if conflicts:
            all_conflicts.extend(conflicts)
            for c in conflicts:
                print(f"  !! {c}")
        else:
            print(f"  OK: {entry_num}D = {answer}")

    for entry_num, answer in hypothetical_across.items():
        conflicts = place_across(grid, entry_num, answer, confirmed_placements, "HYPO ")
        if conflicts:
            all_conflicts.extend(conflicts)
            for c in conflicts:
                print(f"  !! {c}")
        else:
            print(f"  ok: {entry_num}A = {answer} (hypothetical)")

    for entry_num, answer in hypothetical_down.items():
        conflicts = place_down(grid, entry_num, answer, confirmed_placements, "HYPO ")
        if conflicts:
            all_conflicts.extend(conflicts)
            for c in conflicts:
                print(f"  !! {c}")
        else:
            print(f"  ok: {entry_num}D = {answer} (hypothetical)")

    if all_conflicts:
        print(f"\n  WARNING: {len(all_conflicts)} conflicts in base placements!")
    else:
        print(f"\n  All base placements OK (0 conflicts)")

    print_grid(grid, "After placing 17+2 base entries")

    # --------------------------------------------------------
    # STEP 2: Try placing new entries
    # --------------------------------------------------------
    print("\n" + "="*70)
    print("  STEP 2: Testing new theme entry placements")
    print("="*70)

    new_entries = [
        ("SUPERBOWLSTADIUM", 167, "across", "Community screenshot"),
        ("FOOTBALLSTANDS", 73, "across", "Community screenshot"),
        ("BEASTLAND", 149, "across", "Community screenshot"),
    ]

    for answer, entry_num, direction, source in new_entries:
        print(f"\n{'~'*60}")
        print(f"  Testing: {entry_num}{'A' if direction=='across' else 'D'} = {answer} ({len(answer)} letters)")
        print(f"  Source: {source}")
        print(f"{'~'*60}")

        if direction == 'across':
            row, start_col, length = ACROSS[entry_num]
            print(f"  Position: row {row}, cols {start_col}-{start_col+length-1}, length {length}")

            # Letter-by-letter mapping
            print(f"\n  Letter mapping:")
            for i, ch in enumerate(answer):
                col = start_col + i
                existing = grid[row][col]
                is_circled = " *** CIRCLED ***" if (row, col) in CIRCLED_CELLS else ""
                if existing is not None and existing != '#':
                    if existing.upper() == ch.upper():
                        print(f"    pos {i:2d} -> ({row},{col:2d}) = '{ch}' [MATCHES '{existing}']{is_circled}")
                    else:
                        print(f"    pos {i:2d} -> ({row},{col:2d}) = '{ch}' [CONFLICT: cell has '{existing}' from {confirmed_placements.get((row,col), '?')}]{is_circled}")
                else:
                    print(f"    pos {i:2d} -> ({row},{col:2d}) = '{ch}'{is_circled}")

            # Check conflicts
            conflicts = check_across_no_place(grid, entry_num, answer, confirmed_placements)
            if conflicts:
                print(f"\n  RESULT: CANNOT PLACE - {len(conflicts)} conflict(s):")
                for c in conflicts:
                    print(f"    {c}")
            else:
                print(f"\n  RESULT: CAN PLACE - 0 conflicts!")
                # Actually place it
                place_across(grid, entry_num, answer, confirmed_placements, "NEW ")
                # Report crossing constraints
                report_new_constraints(entry_num, answer, 'across', grid, cell_to_entries, confirmed_placements)

    # --------------------------------------------------------
    # STEP 3: Check LEVISSUPERBOWL at all positions
    # --------------------------------------------------------
    print("\n" + "="*70)
    print("  STEP 3: Finding all possible positions for LEVISSUPERBOWL")
    print("="*70)

    levi_answer = "LEVISSUPERBOWL"
    print(f"\n  Answer: {levi_answer} ({len(levi_answer)} letters)")

    # Check specifically at 114A first
    print(f"\n  --- Specific check: 114A ---")
    row114, col114, len114 = ACROSS[114]
    print(f"  114A: row {row114}, cols {col114}-{col114+len114-1}, length {len114}")
    if len(levi_answer) == len114:
        print(f"  Length match: YES ({len(levi_answer)} == {len114})")
        for i, ch in enumerate(levi_answer):
            col = col114 + i
            existing = grid[row114][col]
            is_circled = " *** CIRCLED ***" if (row114, col) in CIRCLED_CELLS else ""
            if existing is not None and existing != '#':
                if existing.upper() == ch.upper():
                    print(f"    pos {i:2d} -> ({row114},{col:2d}) = '{ch}' [MATCHES '{existing}']{is_circled}")
                else:
                    print(f"    pos {i:2d} -> ({row114},{col:2d}) = '{ch}' [CONFLICT: cell has '{existing}' from {confirmed_placements.get((row114,col), '?')}]{is_circled}")
            else:
                print(f"    pos {i:2d} -> ({row114},{col:2d}) = '{ch}'{is_circled}")
    else:
        print(f"  Length match: NO ({len(levi_answer)} != {len114})")

    # Now check ALL positions
    print(f"\n  --- All possible positions for '{levi_answer}' ({len(levi_answer)} letters) ---")
    results = find_all_positions(levi_answer, grid)

    feasible = [r for r in results if r['feasible']]
    infeasible = [r for r in results if not r['feasible']]

    if feasible:
        print(f"\n  FEASIBLE positions ({len(feasible)}):")
        for r in feasible:
            print(f"    {r['entry']} at {r['position']}, length {r['length']}")
            if r['matches']:
                for m in r['matches']:
                    print(f"      Matches existing: ({m[0]},{m[1]}) pos {m[2]} = '{m[3]}'")
    else:
        print(f"\n  NO feasible positions found for {levi_answer}!")

    print(f"\n  Infeasible positions ({len(infeasible)}):")
    for r in infeasible:
        print(f"    {r['entry']} at {r['position']}: {len(r['conflicts'])} conflict(s)")
        for conf in r['conflicts']:
            print(f"      ({conf[0]},{conf[1]}) pos {conf[2]}: wants '{conf[3]}' but has '{conf[4]}'")

    # Also try common variants
    print(f"\n  --- Also trying LEVI'S variants ---")
    variants = [
        "SUPERBOWLATLEVIS",    # 16 letters
        "LEVISTADIUMGAME",     # 15 letters
        "LEVISSUPERBOWLX",     # 15 letters
        "SUPERBOWLXLEVIS",     # 15 letters
        "LEVISSTADIUMLX",      # 14 letters
        "STADIUMATLEVIS",       # 14 letters
        "LEVISSUPERBOWL",      # 14 letters (original)
        "SUPERBOWLLEVIS",      # 14 letters
        "LEVISSTADIUM",        # 12 letters (no 12-letter slots)
    ]

    for variant in variants:
        results = find_all_positions(variant, grid)
        feasible_v = [r for r in results if r['feasible']]
        total_slots = len(results)
        if total_slots == 0:
            print(f"    {variant} ({len(variant)}): No slots of this length exist")
        elif feasible_v:
            print(f"    {variant} ({len(variant)}): {len(feasible_v)} FEASIBLE out of {total_slots} slots")
            for r in feasible_v:
                matches_str = ""
                if r['matches']:
                    matches_str = " | matches: " + ", ".join(f"({m[0]},{m[1]})='{m[3]}'" for m in r['matches'])
                print(f"      -> {r['entry']} at {r['position']}{matches_str}")
        else:
            print(f"    {variant} ({len(variant)}): 0 feasible out of {total_slots} slots")
            # Show the one with fewest conflicts
            if results:
                best = min(results, key=lambda x: len(x['conflicts']))
                print(f"      Best: {best['entry']} with {len(best['conflicts'])} conflict(s)")
                for conf in best['conflicts']:
                    print(f"        ({conf[0]},{conf[1]}) pos {conf[2]}: wants '{conf[3]}' but has '{conf[4]}'")

    # --------------------------------------------------------
    # STEP 4: Summary of circled cells after all placements
    # --------------------------------------------------------
    print("\n" + "="*70)
    print("  STEP 4: Circled cell values after all placements")
    print("="*70)

    print(f"\n  {'#':>3s} | {'Cell':>7s} | {'Letter':>6s} | Source")
    print(f"  {'-'*3}-+-{'-'*7}-+-{'-'*6}-+-{'-'*30}")
    for idx, (r, c) in enumerate(sorted(CIRCLED_CELLS), 1):
        letter = grid[r][c]
        if letter is None:
            letter_str = "?"
        elif letter == '#':
            letter_str = "(black)"
        else:
            letter_str = letter
        source = confirmed_placements.get((r,c), "unknown/empty")
        print(f"  {idx:3d} | ({r:2d},{c:2d}) | {letter_str:>6s} | {source}")

    # --------------------------------------------------------
    # STEP 5: Show current theme entry partial fills
    # --------------------------------------------------------
    print("\n" + "="*70)
    print("  STEP 5: Theme entry partial fills")
    print("="*70)

    theme_entries = [25, 50, 73, 94, 114, 138, 167]
    for entry_num in theme_entries:
        row, start_col, length = ACROSS[entry_num]
        fill = ""
        known_count = 0
        for i in range(length):
            ch = grid[row][start_col + i]
            if ch is None:
                fill += "."
            elif ch == '#':
                fill += "#"
            else:
                fill += ch
                known_count += 1
        print(f"\n  {entry_num}A (row {row}, cols {start_col}-{start_col+length-1}, {length} letters): {known_count}/{length} known")
        print(f"    Fill: {fill}")

        # Show circled cells in this entry
        circles_in_entry = []
        for i in range(length):
            if (row, start_col + i) in CIRCLED_CELLS:
                ch = grid[row][start_col + i]
                circles_in_entry.append(f"pos {i}=({row},{start_col+i})='{ch if ch else '?'}'")
        if circles_in_entry:
            print(f"    Circled: {', '.join(circles_in_entry)}")

    # Also show 19D and 78D
    for entry_num in [19, 78]:
        start_row, col, length = DOWN[entry_num]
        fill = ""
        known_count = 0
        for i in range(length):
            ch = grid[start_row + i][col]
            if ch is None:
                fill += "."
            elif ch == '#':
                fill += "#"
            else:
                fill += ch
                known_count += 1
        print(f"\n  {entry_num}D (col {col}, rows {start_row}-{start_row+length-1}, {length} letters): {known_count}/{length} known")
        print(f"    Fill: {fill}")

    # --------------------------------------------------------
    # STEP 6: Print final grid
    # --------------------------------------------------------
    print_grid(grid, "Final grid after all placements")

    # --------------------------------------------------------
    # STEP 7: Impact analysis - what new down entries are constrained?
    # --------------------------------------------------------
    print("\n" + "="*70)
    print("  STEP 7: New crossing constraints from SUPERBOWLSTADIUM, FOOTBALLSTANDS, BEASTLAND")
    print("="*70)

    # For each newly placed entry, show what down entry patterns we can now derive
    newly_placed = [
        (167, "SUPERBOWLSTADIUM"),
        (73, "FOOTBALLSTANDS"),
        (149, "BEASTLAND"),
    ]

    for entry_num, answer in newly_placed:
        row, start_col, length = ACROSS[entry_num]
        print(f"\n  {entry_num}A = {answer} (row {row}):")
        print(f"  {'Down Entry':>12s} | {'Pos':>3s} | Letter | Pattern So Far")
        print(f"  {'-'*12}-+-{'-'*3}-+-{'-'*6}-+-{'-'*30}")

        for i, ch in enumerate(answer):
            col = start_col + i
            cell = (row, col)
            if cell in cell_to_entries and 'down' in cell_to_entries[cell]:
                down_entry, down_pos = cell_to_entries[cell]['down']
                down_start_row, down_col, down_len = DOWN[down_entry]

                # Build current pattern for this down entry
                pattern = ""
                for j in range(down_len):
                    cell_ch = grid[down_start_row + j][down_col]
                    if cell_ch is None:
                        pattern += "."
                    elif cell_ch == '#':
                        pattern += "#"
                    else:
                        pattern += cell_ch

                is_new = " (NEW)" if ch == grid[row][col] else ""
                is_circled = " *CIRCLED*" if cell in CIRCLED_CELLS else ""
                print(f"  {str(down_entry):>10s}D | {down_pos:>3d} | {ch:>6s} | {pattern}{is_new}{is_circled}")

    # --------------------------------------------------------
    # STEP 8: Check 114A constraints more carefully
    # --------------------------------------------------------
    print("\n" + "="*70)
    print("  STEP 8: 114A constraint analysis (what fits 14 letters, ..........E...E pattern?)")
    print("="*70)

    row114, col114, len114 = ACROSS[114]
    pattern_114 = ""
    for i in range(len114):
        ch = grid[row114][col114 + i]
        if ch is None:
            pattern_114 += "."
        else:
            pattern_114 += ch
    print(f"\n  114A current pattern: {pattern_114}")
    print(f"  Position: row {row114}, cols {col114}-{col114+len114-1}")

    # Show all crossings for 114A
    print(f"\n  All crossings for 114A:")
    crossings = find_crossings_for_across(114, cell_to_entries)
    for cx in crossings:
        cell = cx['cell']
        existing = grid[cell[0]][cell[1]]
        existing_str = existing if existing else "."
        is_circled = " *CIRCLED*" if cell in CIRCLED_CELLS else ""
        print(f"    pos {cx['across_pos']:2d} ({cell[0]},{cell[1]}): crosses {cx['down_entry']}D pos {cx['down_pos']} (len {cx['down_length']}) = '{existing_str}'{is_circled}")

    # Try SUPERBOWLATLEVIS for 114A? No, it's 16 letters and 114A is 14.
    # What about other 14-letter Super Bowl themed answers?
    sb_variants_14 = [
        "SUPERBOWLLEVIS",
        "LEVISSUPERBOWL",
        "STADIUMATLEVIS",
        "LEVISSTADIUMLX",
        "HALFTIMENUMBER",
        "SUPERBOWLFIELD",
        "THESUPERBOWLLX",
    ]

    print(f"\n  Testing 14-letter Super Bowl variants for 114A:")
    for variant in sb_variants_14:
        if len(variant) != 14:
            print(f"    {variant}: SKIP (length {len(variant)}, need 14)")
            continue
        conflicts = check_across_no_place(grid, 114, variant, confirmed_placements)
        if conflicts:
            print(f"    {variant}: {len(conflicts)} conflict(s)")
            for c in conflicts:
                print(f"      {c}")
        else:
            print(f"    {variant}: FITS! (0 conflicts)")

    print("\n" + "="*70)
    print("  DONE")
    print("="*70)


if __name__ == "__main__":
    main()
