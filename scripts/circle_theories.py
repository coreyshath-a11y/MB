#!/usr/bin/env python3
"""
Exhaustive testing of theories about the 16 circled cells in the MrBeast crossword.
"""

import math
import itertools

# ============================================================
# DATA
# ============================================================

circled_cells = [
    # (row, col, across_entry, down_entry, notes)
    (0, 12, '8A', '11D', '11D start'),           # cell 1
    (2, 4, '25A', '5D', 'in 25A pos5, 5D pos3'), # cell 2
    (3, 8, '30A', '8D', 'in 30A pos4, 8D pos4'), # cell 3
    (3, 24, '34A', '21D', 'in 34A pos4, 21D pos4'), # cell 4
    (4, 19, '38A', '16D', 'in 38A pos8, 16D pos5'), # cell 5
    (10, 12, '80A', '67D', 'in 80A pos3, 67D pos3'), # cell 6
    (11, 2, '83A', '78D', 'in 83A pos3, 78D pos2'),  # cell 7
    (11, 22, '91A', '124D', '91A start'),         # cell 8
    (13, 0, '99A', '83D', '99A start'),           # cell 9
    (18, 7, '136A', '137D', '137D start'),        # cell 10
    (19, 17, '146A', '140D', '146A start'),       # cell 11
    (20, 2, '148A', '78D', 'in 148A pos3, 78D pos11'), # cell 12
    (22, 11, '167A', '95D', 'known: P'),          # cell 13
    (22, 18, '167A', '104D', 'known: S'),         # cell 14
    (22, 24, '167A', '126D', 'known: M'),         # cell 15
    (24, 20, '176A', '170D', 'in 176A pos3, 170D pos3'), # cell 16
]

# Known letters (1-indexed cell number -> letter)
known_letters = {
    13: 'P',
    14: 'S',
    15: 'M',
}

# Theme entries
theme_entries = {
    '25A':  {'row': 2, 'col': 0, 'length': 15, 'direction': 'across', 'desc': 'theme across 1'},
    '50A':  {'row': 6, 'col': 1, 'length': 15, 'direction': 'across', 'desc': 'theme across 2'},
    '73A':  {'row': 9, 'col': 5, 'length': 15, 'direction': 'across', 'desc': 'theme across 3'},
    '114A': {'row': 14, 'col': 5, 'length': 15, 'direction': 'across', 'desc': 'theme across 4'},
    '138A': {'row': 18, 'col': 10, 'length': 15, 'direction': 'across', 'desc': 'theme across 5'},
    '167A': {'row': 22, 'col': 0, 'length': 25, 'direction': 'across', 'desc': 'theme across 6 (spanning row)'},
    '19D':  {'row': 0, 'col': 20, 'length': 15, 'direction': 'down', 'desc': 'theme down 1'},
    '78D':  {'row': 10, 'col': 2, 'length': 15, 'direction': 'down', 'desc': 'theme down 2'},
}

GRID_SIZE = 25

def banner(title):
    print("\n" + "=" * 72)
    print(f"  {title}")
    print("=" * 72)

# ============================================================
# THEORY A: Entry numbers at circled cells
# ============================================================
def theory_a():
    banner("THEORY A: Entry numbers at circled cells")

    # Entry numbers that START at circled cell positions
    # We check the notes for "start" indicators
    starts_at = []
    for i, (r, c, ae, de, notes) in enumerate(circled_cells, 1):
        entry_nums = []
        if 'start' in notes.lower():
            # Extract the entry number from the note
            for entry in [ae, de]:
                num = int(''.join(filter(str.isdigit, entry)))
                if f"{num}" in notes.split('start')[0].split()[-1] or entry[:-1] in notes:
                    entry_nums.append(num)
            # More robust: check if either across or down entry starts here
            # An entry "starts" at a cell if noted
            if 'D start' in notes:
                entry_nums = [int(''.join(filter(str.isdigit, de)))]
            elif 'A start' in notes:
                entry_nums = [int(''.join(filter(str.isdigit, ae)))]
        starts_at.append((i, r, c, entry_nums, notes))

    print("\nCircled cells and entry starts:")
    print(f"{'Cell':>4} {'Row':>3} {'Col':>3} {'Across':>8} {'Down':>8} {'Starts':>10}  Notes")
    print("-" * 72)
    for i, (r, c, ae, de, notes) in enumerate(circled_cells, 1):
        start_entries = starts_at[i-1][3]
        start_str = ','.join(map(str, start_entries)) if start_entries else '-'
        print(f"{i:>4} {r:>3} {c:>3} {ae:>8} {de:>8} {start_str:>10}  {notes}")

    # Collect just the starting entry numbers
    starting_nums = []
    for _, _, _, nums, _ in starts_at:
        starting_nums.extend(nums)
    print(f"\nEntry numbers starting at circled cells: {starting_nums}")

    # A1Z26 decode (mod 26)
    print("\nA1Z26 decode (number mod 26 -> letter, 0=Z):")
    for n in starting_nums:
        mod = n % 26
        letter = chr(ord('A') + mod - 1) if mod != 0 else 'Z'
        print(f"  {n} -> {n} mod 26 = {mod} -> {letter}")

    decoded = []
    for n in starting_nums:
        mod = n % 26
        decoded.append(chr(ord('A') + mod - 1) if mod != 0 else 'Z')
    print(f"  Decoded string: {''.join(decoded)}")

    # Also try digit-by-digit
    print("\nDigits of starting entry numbers concatenated:")
    digits_str = ''.join(str(n) for n in starting_nums)
    print(f"  {digits_str}")
    if len(digits_str) % 2 == 0:
        pairs = [digits_str[i:i+2] for i in range(0, len(digits_str), 2)]
        decoded2 = []
        for p in pairs:
            v = int(p)
            if 1 <= v <= 26:
                decoded2.append(chr(ord('A') + v - 1))
            else:
                decoded2.append(f'[{v}]')
        print(f"  Pairs: {pairs} -> {''.join(decoded2)}")

    # All across entry numbers at circled cells
    across_nums = [int(''.join(filter(str.isdigit, c[2]))) for c in circled_cells]
    down_nums = [int(''.join(filter(str.isdigit, c[3]))) for c in circled_cells]
    print(f"\nAll across entry numbers at circled cells: {across_nums}")
    print(f"All down entry numbers at circled cells: {down_nums}")

    # Differences between consecutive across numbers
    across_diffs = [across_nums[i+1] - across_nums[i] for i in range(len(across_nums)-1)]
    print(f"Across number differences: {across_diffs}")

    # Sum of all entry numbers
    print(f"Sum of across numbers: {sum(across_nums)}")
    print(f"Sum of down numbers: {sum(down_nums)}")
    print(f"Sum of all (across+down): {sum(across_nums) + sum(down_nums)}")

# ============================================================
# THEORY B: Reading order variations
# ============================================================
def theory_b():
    banner("THEORY B: Reading order variations")

    positions = [(r, c) for r, c, _, _, _ in circled_cells]
    cell_indices = list(range(16))  # 0-indexed

    # 1. Row order (already sorted: top-to-bottom, left-to-right)
    row_order = sorted(cell_indices, key=lambda i: (positions[i][0], positions[i][1]))
    print("\n1. Row order (top-bottom, left-right) [default]:")
    print(f"   Cell sequence: {[i+1 for i in row_order]}")

    # 2. Column order (left-to-right, top-to-bottom)
    col_order = sorted(cell_indices, key=lambda i: (positions[i][1], positions[i][0]))
    print("\n2. Column order (left-right, top-bottom):")
    print(f"   Cell sequence: {[i+1 for i in col_order]}")

    # 3. By across entry number (ascending)
    across_nums = [int(''.join(filter(str.isdigit, circled_cells[i][2]))) for i in range(16)]
    across_order = sorted(cell_indices, key=lambda i: across_nums[i])
    print("\n3. By across entry number (ascending):")
    print(f"   Cell sequence: {[i+1 for i in across_order]}")
    print(f"   Entry numbers: {[across_nums[i] for i in across_order]}")

    # 4. By down entry number (ascending)
    down_nums = [int(''.join(filter(str.isdigit, circled_cells[i][3]))) for i in range(16)]
    down_order = sorted(cell_indices, key=lambda i: down_nums[i])
    print("\n4. By down entry number (ascending):")
    print(f"   Cell sequence: {[i+1 for i in down_order]}")
    print(f"   Entry numbers: {[down_nums[i] for i in down_order]}")

    # 5. Spiral from outside in (approximate: sort by distance from center)
    center = (12, 12)
    def dist_from_center(i):
        r, c = positions[i]
        return math.sqrt((r - center[0])**2 + (c - center[1])**2)
    spiral_out = sorted(cell_indices, key=lambda i: -dist_from_center(i))
    print("\n5. Spiral from outside in (by distance from center, farthest first):")
    print(f"   Cell sequence: {[i+1 for i in spiral_out]}")
    print(f"   Distances: {[f'{dist_from_center(i):.1f}' for i in spiral_out]}")

    # 6. Clockwise from top-left
    def angle_from_center(i):
        r, c = positions[i]
        # Angle from center, with 0 = up, going clockwise
        return math.atan2(c - center[1], -(r - center[0])) % (2 * math.pi)
    clockwise_order = sorted(cell_indices, key=angle_from_center)
    print("\n6. Clockwise from top (starting north, going clockwise):")
    print(f"   Cell sequence: {[i+1 for i in clockwise_order]}")
    print(f"   Angles: {[f'{math.degrees(angle_from_center(i)):.0f}' for i in clockwise_order]}")

    # 7. Reverse row order
    reverse_row = list(reversed(row_order))
    print("\n7. Reverse row order:")
    print(f"   Cell sequence: {[i+1 for i in reverse_row]}")

    # 8. By minimum entry number (min of across, down)
    min_entry_order = sorted(cell_indices, key=lambda i: min(across_nums[i], down_nums[i]))
    print("\n8. By minimum entry number (min of across/down):")
    print(f"   Cell sequence: {[i+1 for i in min_entry_order]}")
    print(f"   Min entries: {[min(across_nums[i], down_nums[i]) for i in min_entry_order]}")

    # Show known letters in each ordering
    print("\n--- Known letters in each ordering ---")
    orderings = {
        'Row order': row_order,
        'Column order': col_order,
        'Across entry': across_order,
        'Down entry': down_order,
        'Spiral (out-in)': spiral_out,
        'Clockwise': clockwise_order,
        'Reverse row': reverse_row,
        'Min entry': min_entry_order,
    }
    for name, order in orderings.items():
        letters = []
        for i in order:
            cell_num = i + 1
            if cell_num in known_letters:
                letters.append(known_letters[cell_num])
            else:
                letters.append('?')
        print(f"  {name:20s}: {''.join(letters)}")

    # Theory B sub: 16-letter strings with P@13, S@14, M@15 (1-indexed, row order)
    print("\n--- 16-char pattern analysis (row order) ---")
    print("Pattern: ????????????PSM?")
    print("Positions 13,14,15 are P,S,M (1-indexed)")

    # Check some MrBeast-related possibilities
    candidates_16 = [
        "SUBSCRIBETODAYS",
        "MRBEASTCHALLENG",
        "BEASTPHILANTHRO",
        "TEAMTREESPLANTED",
        "SUBSCRIBEANDPSM",
        "AMAZINGPRISMBOX",
    ]
    # More systematic: what ends with _PSM_?
    print("\n  Common 16-letter phrases/words with P at pos 13, S at 14, M at 15:")
    print("  (Searching for pattern ????????????PSM?)")
    # Generate what the last 4 chars could be
    print("  Positions 13-16 = P S M ?")
    print("  Possible endings: PSMA, PSMB, ... PSMZ")
    print("  Does 'PSM' appear in any meaningful context?")
    print("  - PSM = Personal Spectral Match? Phase Shift Modulation?")
    print("  - Could be initials or abbreviation fragment")

    # What if it's in a different order? Check column order positions of known cells
    for name, order in orderings.items():
        pos_of_known = {}
        for idx, i in enumerate(order):
            cell_num = i + 1
            if cell_num in known_letters:
                pos_of_known[known_letters[cell_num]] = idx + 1  # 1-indexed position
        if pos_of_known:
            print(f"  {name:20s}: " + ", ".join(f"{l}@pos{p}" for l, p in sorted(pos_of_known.items(), key=lambda x: x[1])))

# ============================================================
# THEORY C: Circled cells form a pattern on the grid
# ============================================================
def theory_c():
    banner("THEORY C: Circled cells form a visual pattern on the grid")

    positions = [(r, c) for r, c, _, _, _ in circled_cells]

    # Print the 25x25 grid with circled cells marked
    print("\n25x25 grid with circled cells marked (O = circled, . = empty):\n")
    print("     " + "".join(f"{c:>2}" for c in range(25)))
    print("     " + "--" * 25)
    for r in range(25):
        row_str = f"{r:>3} | "
        for c in range(25):
            if (r, c) in positions:
                cell_num = positions.index((r, c)) + 1
                row_str += f"{cell_num:>2}" if cell_num < 10 else f"{cell_num:>2}"
            else:
                row_str += " ."
        print(row_str)

    # Simplified ASCII art (compressed)
    print("\nCompressed view (each char = 1 cell, O=circled):\n")
    for r in range(25):
        line = f"{r:>2} "
        for c in range(25):
            if (r, c) in positions:
                line += "O"
            else:
                line += "."
        print(line)

    # Analyze pattern
    rows = [r for r, c in positions]
    cols = [c for r, c in positions]

    print(f"\nRow distribution: {sorted(rows)}")
    print(f"Col distribution: {sorted(cols)}")
    print(f"Row range: {min(rows)}-{max(rows)}")
    print(f"Col range: {min(cols)}-{max(cols)}")
    print(f"Centroid: ({sum(rows)/len(rows):.1f}, {sum(cols)/len(cols):.1f})")

    # Check symmetry
    print("\n--- Symmetry checks ---")
    # Horizontal symmetry (around row 12)
    h_sym = [(24 - r, c) for r, c in positions]
    h_matches = sum(1 for p in h_sym if p in positions)
    print(f"Horizontal symmetry (row mirror around 12): {h_matches}/16 cells match")

    # Vertical symmetry (around col 12)
    v_sym = [(r, 24 - c) for r, c in positions]
    v_matches = sum(1 for p in v_sym if p in positions)
    print(f"Vertical symmetry (col mirror around 12): {v_matches}/16 cells match")

    # 180-degree rotational symmetry
    rot_sym = [(24 - r, 24 - c) for r, c in positions]
    rot_matches = sum(1 for p in rot_sym if p in positions)
    print(f"180-degree rotational symmetry: {rot_matches}/16 cells match")

    # Diagonal symmetry
    diag_sym = [(c, r) for r, c in positions]
    diag_matches = sum(1 for p in diag_sym if p in positions)
    print(f"Diagonal symmetry (r,c -> c,r): {diag_matches}/16 cells match")

    # Check if points form a letter
    print("\n--- Could the points form a recognizable shape? ---")

    # Normalize to a smaller grid for visualization
    # Map rows 0-24 to 0-12, cols 0-24 to 0-12
    print("\nNormalized to ~13x13 grid:")
    for r in range(13):
        line = ""
        for c in range(13):
            # Check if any circled cell maps here
            found = False
            for pr, pc in positions:
                nr = round(pr * 12 / 24)
                nc = round(pc * 12 / 24)
                if nr == r and nc == c:
                    found = True
                    break
            line += "X " if found else ". "
        print(f"  {line}")

    # Connect-the-dots analysis
    print("\n--- Connect the dots (in cell order 1-16) ---")
    print("Consecutive cell distances and directions:")
    for i in range(15):
        r1, c1 = positions[i]
        r2, c2 = positions[i+1]
        dr = r2 - r1
        dc = c2 - c1
        dist = math.sqrt(dr**2 + dc**2)
        angle = math.degrees(math.atan2(dc, dr))
        print(f"  Cell {i+1} -> {i+2}: delta=({dr:+d},{dc:+d}), dist={dist:.1f}, angle={angle:.0f}deg")

    # Total path length
    total_dist = sum(
        math.sqrt((positions[i+1][0]-positions[i][0])**2 + (positions[i+1][1]-positions[i][1])**2)
        for i in range(15)
    )
    print(f"\n  Total connect-the-dots path length: {total_dist:.1f}")

    # Check if closing the loop makes a polygon
    r_last, c_last = positions[-1]
    r_first, c_first = positions[0]
    close_dist = math.sqrt((r_first-r_last)**2 + (c_first-c_last)**2)
    print(f"  Closing distance (cell 16 -> cell 1): {close_dist:.1f}")

    # Convex hull area
    def cross(O, A, B):
        return (A[0] - O[0]) * (B[1] - O[1]) - (A[1] - O[1]) * (B[0] - O[0])

    pts = sorted(positions)
    if len(pts) > 1:
        lower = []
        for p in pts:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
        upper = []
        for p in reversed(pts):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
        hull = lower[:-1] + upper[:-1]
        # Area using shoelace
        n = len(hull)
        area = abs(sum(hull[i][0]*hull[(i+1)%n][1] - hull[(i+1)%n][0]*hull[i][1] for i in range(n))) / 2
        print(f"\n  Convex hull has {len(hull)} points, area = {area:.1f} sq cells")
        print(f"  Grid area = {24*24} = 576 sq cells")
        print(f"  Hull/Grid ratio: {area/576:.2%}")

# ============================================================
# THEORY D: Coordinates as numbers
# ============================================================
def theory_d():
    banner("THEORY D: Circled cell coordinates as numbers")

    positions = [(r, c) for r, c, _, _, _ in circled_cells]
    rows = [r for r, c in positions]
    cols = [c for r, c in positions]

    print("\nRow values:", rows)
    print("Col values:", cols)

    # Concatenated digits
    row_str = ''.join(str(r) for r in rows)
    col_str = ''.join(str(c) for c in cols)
    print(f"\nConcatenated row digits: {row_str} (length {len(row_str)})")
    print(f"Concatenated col digits: {col_str} (length {len(col_str)})")

    # Row + Col sums
    print(f"\nRow sum: {sum(rows)}")
    print(f"Col sum: {sum(cols)}")
    print(f"Total sum (rows+cols): {sum(rows) + sum(cols)}")
    print(f"Row sum mod 26 = {sum(rows) % 26} -> {chr(ord('A') + sum(rows) % 26 - 1) if sum(rows) % 26 > 0 else 'Z'}")
    print(f"Col sum mod 26 = {sum(cols) % 26} -> {chr(ord('A') + sum(cols) % 26 - 1) if sum(cols) % 26 > 0 else 'Z'}")

    # Row*Col products
    products = [r * c for r, c in positions]
    print(f"\nRow*Col products: {products}")
    print(f"Product sum: {sum(products)}")

    # ASCII from (row, col) pairs
    print("\n--- ASCII from coordinate pairs ---")
    print("Method 1: row*25 + col")
    for i, (r, c) in enumerate(positions):
        val = r * 25 + c
        ch = chr(val) if 32 <= val < 127 else f'[{val}]'
        print(f"  Cell {i+1}: ({r},{c}) -> {val} -> {ch!r}")

    print("\nMethod 2: row + col as 2-digit number -> A1Z26")
    for i, (r, c) in enumerate(positions):
        val = r + c
        if 1 <= val <= 26:
            letter = chr(ord('A') + val - 1)
        else:
            letter = f'[{val}]'
        print(f"  Cell {i+1}: {r}+{c} = {val} -> {letter}")

    # Row sums as A1Z26
    row_col_sums = [r + c for r, c in positions]
    letters_sum = []
    for val in row_col_sums:
        if 1 <= val <= 26:
            letters_sum.append(chr(ord('A') + val - 1))
        else:
            letters_sum.append('?')
    print(f"\n  Row+Col sums: {row_col_sums}")
    print(f"  As A1Z26: {''.join(letters_sum)}")

    # Differences
    print("\nMethod 3: |row - col|")
    diffs = [abs(r - c) for r, c in positions]
    letters_diff = []
    for val in diffs:
        if 1 <= val <= 26:
            letters_diff.append(chr(ord('A') + val - 1))
        elif val == 0:
            letters_diff.append('_')
        else:
            letters_diff.append('?')
    print(f"  |Row-Col| values: {diffs}")
    print(f"  As A1Z26: {''.join(letters_diff)}")

    # XOR
    print("\nMethod 4: row XOR col")
    xors = [r ^ c for r, c in positions]
    letters_xor = []
    for val in xors:
        if 1 <= val <= 26:
            letters_xor.append(chr(ord('A') + val - 1))
        else:
            letters_xor.append(f'[{val}]')
    print(f"  Row XOR Col: {xors}")
    xor_str = ''.join(letters_xor)
    print(f"  As A1Z26: {xor_str}")

    # Mod 26
    print("\nMethod 5: (row + col) mod 26")
    mod_vals = [(r + c) % 26 for r, c in positions]
    letters_mod = [chr(ord('A') + v - 1) if v > 0 else 'Z' for v in mod_vals]
    print(f"  Mod values: {mod_vals}")
    print(f"  As A1Z26: {''.join(letters_mod)}")

    # Two-digit concat as numbers
    print("\nMethod 6: concat row,col as 2-digit pairs -> numbers")
    print("(Treating each coordinate as a single value, pairs of cells -> 2-digit number)")
    for i in range(0, 16, 2):
        r1, c1 = positions[i]
        r2, c2 = positions[i+1]
        print(f"  Cells {i+1},{i+2}: rows ({r1},{r2}), cols ({c1},{c2})")

    # Row digits concatenated -> try A1Z26 pairs
    print(f"\nMethod 7: Row digits '{row_str}' as pairs:")
    if len(row_str) >= 2:
        for start in range(min(3, len(row_str))):  # try offsets
            pairs = []
            j = start
            while j + 1 < len(row_str):
                pairs.append(row_str[j:j+2])
                j += 2
            decoded = []
            for p in pairs:
                v = int(p)
                if 1 <= v <= 26:
                    decoded.append(chr(ord('A') + v - 1))
                else:
                    decoded.append(f'[{v}]')
            print(f"  Offset {start}: pairs={pairs} -> {''.join(decoded)}")

    print(f"\nMethod 8: Col digits '{col_str}' as pairs:")
    if len(col_str) >= 2:
        for start in range(min(3, len(col_str))):
            pairs = []
            j = start
            while j + 1 < len(col_str):
                pairs.append(col_str[j:j+2])
                j += 2
            decoded = []
            for p in pairs:
                v = int(p)
                if 1 <= v <= 26:
                    decoded.append(chr(ord('A') + v - 1))
                else:
                    decoded.append(f'[{v}]')
            print(f"  Offset {start}: pairs={pairs} -> {''.join(decoded)}")

# ============================================================
# THEORY E: 16-character strings with P@13, S@14, M@15
# ============================================================
def theory_e():
    banner("THEORY E: 16-character strings with P@13, S@14, M@15")

    print("\nConstraints: 16 characters, position 13=P, position 14=S, position 15=M (1-indexed)")
    print("Pattern: _ _ _ _ _ _ _ _ _ _ _ _ P S M _")
    print()

    # MrBeast related terms
    mrbeast_terms = [
        "SUPERBOWLSTADIUM",  # 17 chars - too long
        "SUBSCRIBETONOWPSM",
        "PHILANTHROPYPSM",
    ]

    # Check specific candidates
    candidates = [
        # Format: (candidate, description)
        ("MRBEASTGAMEPSMA", "MrBeast Game + PSMA"),
        ("AMAZINGCOUPSPSM", "amazing coups PSM"),
        ("SUBSCRIPTIONS16", "subscriptions"),
        ("BEASTCAMPAIGNPM", "beast campaign"),
    ]

    # What 3-letter combos before PSM make words?
    print("Looking at positions 12-16: _PSM_")
    print("Common letter combos with PSM:")
    # PSM is unusual in English
    print("  - PSM is not a common English trigram")
    print("  - Could be abbreviation: P.S.M. = ?")
    print()

    # More productive: what if 167A = SUPERBOWLSTADIUM?
    # That's 17 letters but 167A spans all 25 columns
    # Let's check what letters from 167A fall in circled cells
    print("--- If 167A = various candidates ---")
    # 167A starts at (22, 0) and goes across 25 cells
    # Circled cells in row 22: (22,11), (22,18), (22,24)
    # So positions in 167A: col 11 = pos 12, col 18 = pos 19, col 24 = pos 25

    candidates_167a = [
        "SUPERBOWLSTADIUMPARKWAYS",  # 25 - too many
        # 167A is 25 cells wide (full row)
        # Known: col 11 = P, col 18 = S, col 24 = M
    ]

    print("167A spans row 22, cols 0-24 (25 letters)")
    print("Circled cells in 167A:")
    print("  Cell 13: col 11 -> position 12 in 167A (0-indexed: 11)")
    print("  Cell 14: col 18 -> position 19 in 167A (0-indexed: 18)")
    print("  Cell 15: col 24 -> position 25 in 167A (0-indexed: 24)")
    print()
    print("If 167A answer has P at position 12, S at position 19, M at position 25...")
    print("That means the word/phrase has:")
    print("  pos 12 = P (12th letter)")
    print("  pos 19 = S (19th letter)")
    print("  pos 25 = M (25th/last letter)")
    print()

    # ACTSOFGENEROSITY is only 16 letters, but 167A is 25 letters
    # SUPERBOWLSTADIUM is 17 letters
    # Wait - let's reconsider. 167A clue says "What this puzzle commemorates in eleven hidden words in theme entries"
    # 167A is 25 letters long

    # Try known candidates
    for candidate in ["ACTSOFGENEROSITYANDKINDNE",  # 25 chars attempt
                       "SUPERBOWLSTADIUMINARIZONA",   # doesn't work well
                       ]:
        if len(candidate) == 25:
            p12 = candidate[11] if len(candidate) > 11 else '?'
            p19 = candidate[18] if len(candidate) > 18 else '?'
            p25 = candidate[24] if len(candidate) > 24 else '?'
            match = (p12 == 'P' and p19 == 'S' and p25 == 'M')
            print(f"  '{candidate}': pos12={p12}, pos19={p19}, pos25={p25} -> {'MATCH' if match else 'no match'}")

    print()
    print("--- What MrBeast-related 25-letter phrase has P@12, S@19, M@25? ---")
    print("Position:  1234567890123456789012345")
    print("Required:            P      S     M")
    print()

    # What if we think about the 16-letter extraction differently?
    # The 16 circled cells give 16 letters that form the final code
    print("--- Final code format analysis ---")
    print("16 letters extracted from circled cells")
    print("Submitted to Slackbot at mrbeast.salesforce.com")
    print("Could be:")
    print("  - A meaningful phrase (e.g., CONGRATULATIONS is 16 letters!)")
    print("    But: does CONGRATULATIONS have P@13? C-O-N-G-R-A-T-U-L-A-T-I-O-N-S -> pos13=O, no")
    print("  - An encoded/hashed value")
    print("  - A Salesforce record ID (15 or 18 chars - close to 16!)")
    print("  - A UUID fragment")
    print()

    # Interesting: Salesforce IDs are 15 or 18 characters
    print("Salesforce ID format: 15 chars (case-sensitive) or 18 chars (case-insensitive)")
    print("  15-char ID: 5 groups of 3 chars (alphanumeric)")
    print("  Our 16 chars is 1 more than a 15-char ID")
    print()

    # Check if known letters P, S, M could be Salesforce ID chars
    print("P, S, M are all valid Salesforce ID characters (alphanumeric)")
    print()

    # What 16-letter words exist? Let's check some common ones
    sixteen_letter_words = [
        "ACKNOWLEDGEMENTS",  # A-C-K-N-O-W-L-E-D-G-E-M-E-N-T-S -> pos13=E, no
        "CHARACTERIZATION",  # pos13=I, no
        "COMPARTMENTALIZE",  # pos13=I, no
        "DISPROPORTIONATE",  # pos13=A, no
        "ENTHUSIASTICALLY",  # pos13=A, no
        "INCOMPREHENSIBLE",  # pos13=I, no
        "INTERNATIONALISM",  # pos13=I, no
        "IRRECONCILABLEST",  #
        "MISREPRESENTATION", # 17 chars
        "OVERSIMPLIFICAT",   # incomplete
        "PREDETERMINABLE",   # 15 chars
        "RESPONSIBILITIES",  # R-E-S-P-O-N-S-I-B-I-L-I-T-I-E-S: 16! pos13=T, no
        "UNDERAPPRECIATED", # 16? U-N-D-E-R-A-P-P-R-E-C-I-A-T-E-D: 16! pos13=A, no
        "UNCOMPROMISINGLY",  # 16: pos13=G, no
        "UNPROFESSIONALLY", # 16: pos13=A, no
        "STRAIGHTFORWARD",   # 15
        "COUNTERPROPOSALM", # forced
        "HUMANITARIANPSM",   # forced - 15+1
    ]

    print("Checking 16-letter English words for P@13, S@14, M@15:")
    for word in sixteen_letter_words:
        if len(word) == 16:
            p13 = word[12]
            p14 = word[13]
            p15 = word[14]
            match_13 = (p13 == 'P')
            match_14 = (p14 == 'S')
            match_15 = (p15 == 'M')
            if match_13 or match_14 or match_15:
                stars = sum([match_13, match_14, match_15])
                print(f"  {word}: pos13={p13}, pos14={p14}, pos15={p15} -> {stars}/3 matches")
            else:
                print(f"  {word}: pos13={p13}, pos14={p14}, pos15={p15} -> no match")

    # What about "MRBEAST" embedded?
    print("\n--- Phrases with MRBEAST ---")
    print("  'THANKYOUMRBEAST' = 16 chars: T-H-A-N-K-Y-O-U-M-R-B-E-A-S-T -> only 15")
    thankyou = "THANKYOUMRBEAST"
    print(f"  Actually '{thankyou}' = {len(thankyou)} chars")
    padded = "THANKYOUMRBEASTS"
    print(f"  '{padded}' = {len(padded)} chars")
    if len(padded) == 16:
        print(f"    pos13={padded[12]}, pos14={padded[13]}, pos15={padded[14]}")

    # What about ILOVEMRBEASTPSM?
    test_phrases = [
        "BEASTCHALLNGPSMA",
        "PHILANTROPYPSMXX",
        "WELOVEMRBEASTPSM",  # not 16 with pattern
    ]

    # More systematic: what 4-letter sequences end with PSM_?
    print("\n--- If last 4 positions are PSM+something ---")
    print("This is position 13-16 = P,S,M,? in the 16-cell reading")
    print("These come from cells 13,14,15,16")
    print("Cell 13 = (22,11) in 167A and 95D")
    print("Cell 14 = (22,18) in 167A and 104D")
    print("Cell 15 = (22,24) in 167A and 126D")
    print("Cell 16 = (24,20) in 176A and 170D")
    print("Cell 16's letter is currently unknown")

# ============================================================
# THEORY F: Circled cells as binary
# ============================================================
def theory_f():
    banner("THEORY F: Circled cells as binary / positional encoding")

    positions = [(r, c) for r, c, _, _, _ in circled_cells]

    # Method 1: 16 bits from presence in a linearized grid
    print("\n--- Method 1: 25x25 grid linearized, circled positions as bit positions ---")
    linear_positions = [r * 25 + c for r, c in positions]
    print(f"Linear positions (row*25+col): {linear_positions}")
    print(f"As binary positions (which bits are set in a 625-bit number):")

    # This gives a very large number, but let's compute it
    big_num = 0
    for lp in linear_positions:
        big_num |= (1 << lp)
    print(f"  Big number: {big_num}")
    print(f"  Hex: {hex(big_num)}")
    print(f"  Bit count: {bin(big_num).count('1')} (should be 16)")

    # Method 2: 16 cells = 16 bits
    print("\n--- Method 2: Treat 16 cells as 16-bit number ---")
    print("If circle = 1 for each cell position, we have 16 1-bits -> not useful as binary")
    print("But if we use known letters as bits:")
    print("  Known: P=16(10000), S=19(10011), M=13(01101)")
    print()

    # Method 3: Row numbers as binary
    rows = [r for r, c in positions]
    cols = [c for r, c in positions]

    # Each row is 0-24, fits in 5 bits
    row_bits = ''.join(format(r, '05b') for r in rows)
    col_bits = ''.join(format(c, '05b') for c in cols)
    print(f"Row values as 5-bit binary (concatenated): {row_bits} ({len(row_bits)} bits)")
    print(f"Col values as 5-bit binary (concatenated): {col_bits} ({len(col_bits)} bits)")

    # 80 bits = 10 bytes
    print(f"\nRow bits as bytes (10 bytes from 80 bits):")
    for i in range(0, 80, 8):
        byte = row_bits[i:i+8]
        val = int(byte, 2)
        ch = chr(val) if 32 <= val < 127 else f'[{val}]'
        print(f"  bits {i}-{i+7}: {byte} = {val} = {ch!r}")

    print(f"\nCol bits as bytes (10 bytes from 80 bits):")
    for i in range(0, 80, 8):
        byte = col_bits[i:i+8]
        val = int(byte, 2)
        ch = chr(val) if 32 <= val < 127 else f'[{val}]'
        print(f"  bits {i}-{i+7}: {byte} = {val} = {ch!r}")

    # Interleaved (row bit, col bit, row bit, col bit...)
    interleaved = ''.join(rb + cb for rb, cb in zip(row_bits, col_bits))
    print(f"\nInterleaved row/col bits: {interleaved[:40]}... ({len(interleaved)} bits)")
    print("As bytes:")
    for i in range(0, min(160, len(interleaved)), 8):
        byte = interleaved[i:i+8]
        if len(byte) == 8:
            val = int(byte, 2)
            ch = chr(val) if 32 <= val < 127 else f'[{val}]'
            print(f"  bits {i}-{i+7}: {byte} = {val} = {ch!r}")

    # XOR rows and cols
    print("\n--- XOR pattern ---")
    xor_bits = ''.join(format(r ^ c, '05b') for r, c in positions)
    print(f"Row XOR Col as 5-bit: {xor_bits}")
    for i in range(0, 80, 8):
        byte = xor_bits[i:i+8]
        val = int(byte, 2)
        ch = chr(val) if 32 <= val < 127 else f'[{val}]'
        print(f"  bits {i}-{i+7}: {byte} = {val} = {ch!r}")

# ============================================================
# THEORY G: Circled cells vs theme entries
# ============================================================
def theory_g():
    banner("THEORY G: Circled cells alignment with theme entries")

    positions = [(r, c) for r, c, _, _, _ in circled_cells]

    print("\nTheme entries:")
    for entry_name, info in sorted(theme_entries.items(), key=lambda x: x[0]):
        r, c, length, direction = info['row'], info['col'], info['length'], info['direction']
        if direction == 'across':
            cells = [(r, c + i) for i in range(length)]
        else:
            cells = [(r + i, c) for i in range(length)]
        end_r, end_c = cells[-1]
        print(f"  {entry_name}: ({r},{c})->({end_r},{end_c}), {length} cells, {direction}")

    print("\n--- Which circled cells fall in which theme entries ---")
    for ci, (r, c, ae, de, notes) in enumerate(circled_cells, 1):
        in_themes = []
        for entry_name, info in theme_entries.items():
            er, ec, length, direction = info['row'], info['col'], info['length'], info['direction']
            if direction == 'across':
                if r == er and ec <= c < ec + length:
                    pos_in_entry = c - ec + 1
                    in_themes.append(f"{entry_name} (pos {pos_in_entry}/{length})")
            else:  # down
                if c == ec and er <= r < er + length:
                    pos_in_entry = r - er + 1
                    in_themes.append(f"{entry_name} (pos {pos_in_entry}/{length})")

        theme_str = ', '.join(in_themes) if in_themes else 'NOT in any theme entry'
        letter = known_letters.get(ci, '?')
        print(f"  Cell {ci:>2} ({r:>2},{c:>2}) [{letter}]: {theme_str}")

    # Count circled cells per theme entry
    print("\n--- Circled cells per theme entry ---")
    for entry_name, info in sorted(theme_entries.items()):
        er, ec, length, direction = info['row'], info['col'], info['length'], info['direction']
        count = 0
        cell_list = []
        for ci, (r, c, _, _, _) in enumerate(circled_cells, 1):
            if direction == 'across' and r == er and ec <= c < ec + length:
                count += 1
                cell_list.append(ci)
            elif direction == 'down' and c == ec and er <= r < er + length:
                count += 1
                cell_list.append(ci)
        print(f"  {entry_name}: {count} circled cells {cell_list if cell_list else ''}")

    # Which theme entries have NO circled cells?
    print("\n--- Theme entries with no circled cells ---")
    for entry_name, info in sorted(theme_entries.items()):
        er, ec, length, direction = info['row'], info['col'], info['length'], info['direction']
        has_circle = False
        for r, c, _, _, _ in circled_cells:
            if direction == 'across' and r == er and ec <= c < ec + length:
                has_circle = True
                break
            elif direction == 'down' and c == ec and er <= r < er + length:
                has_circle = True
                break
        if not has_circle:
            print(f"  {entry_name} - NO circled cells")

    # Positions within theme entries
    print("\n--- Position of circled cells within their theme entries ---")
    print("(Could the position within the theme entry encode something?)")
    for ci, (r, c, ae, de, notes) in enumerate(circled_cells, 1):
        for entry_name, info in theme_entries.items():
            er, ec, length, direction = info['row'], info['col'], info['length'], info['direction']
            if direction == 'across' and r == er and ec <= c < ec + length:
                pos = c - ec + 1
                print(f"  Cell {ci:>2} in {entry_name}: position {pos}/{length}")
            elif direction == 'down' and c == ec and er <= r < er + length:
                pos = r - er + 1
                print(f"  Cell {ci:>2} in {entry_name}: position {pos}/{length}")

    # Check: do circled cells that are in theme entries extract the hidden location names?
    print("\n--- Relationship to hidden locations (167A's answer) ---")
    print("167A asks for 11 hidden words (location names) in theme entries")
    print("Circled cells in theme entries might mark positions of hidden words")
    print("Or the circled cell positions might spell out/index into the locations")

# ============================================================
# BONUS: Cross-theory analysis
# ============================================================
def cross_theory():
    banner("CROSS-THEORY ANALYSIS AND SUMMARY")

    positions = [(r, c) for r, c, _, _, _ in circled_cells]

    print("\nKey observations:")
    print()

    # Number of circled cells that start entries
    starts = [i+1 for i, (r, c, ae, de, notes) in enumerate(circled_cells) if 'start' in notes.lower()]
    print(f"1. Cells at entry starts: {starts} ({len(starts)} of 16)")
    non_starts = [i+1 for i in range(16) if (i+1) not in starts]
    print(f"   Cells NOT at entry starts: {non_starts} ({len(non_starts)} of 16)")

    # Quadrant distribution
    q1 = sum(1 for r, c in positions if r < 12 and c < 12)  # top-left
    q2 = sum(1 for r, c in positions if r < 12 and c >= 12)  # top-right
    q3 = sum(1 for r, c in positions if r >= 12 and c < 12)  # bottom-left
    q4 = sum(1 for r, c in positions if r >= 12 and c >= 12) # bottom-right
    print(f"\n2. Quadrant distribution (dividing at row 12, col 12):")
    print(f"   Top-left:     {q1}")
    print(f"   Top-right:    {q2}")
    print(f"   Bottom-left:  {q3}")
    print(f"   Bottom-right: {q4}")

    # Row distribution
    print(f"\n3. Row distribution:")
    from collections import Counter
    row_counts = Counter(r for r, c in positions)
    for row in sorted(row_counts.keys()):
        cols_in_row = [c for r, c in positions if r == row]
        print(f"   Row {row:>2}: {row_counts[row]} cells at cols {cols_in_row}")

    # Which rows have 0 circled cells?
    rows_with = set(r for r, c in positions)
    rows_without = [r for r in range(25) if r not in rows_with]
    print(f"   Rows without circled cells: {rows_without}")
    print(f"   ({len(rows_without)} of 25 rows have no circled cells)")

    # Check if circled cells are at intersections of specific entry types
    print(f"\n4. Entry intersection analysis:")
    for ci, (r, c, ae, de, notes) in enumerate(circled_cells, 1):
        a_num = int(''.join(filter(str.isdigit, ae)))
        d_num = int(''.join(filter(str.isdigit, de)))
        print(f"   Cell {ci:>2}: {ae} x {de} (across#{a_num}, down#{d_num}, sum={a_num+d_num}, diff={abs(a_num-d_num)})")

    # Sum and difference patterns
    a_nums = [int(''.join(filter(str.isdigit, c[2]))) for c in circled_cells]
    d_nums = [int(''.join(filter(str.isdigit, c[3]))) for c in circled_cells]
    sums = [a + d for a, d in zip(a_nums, d_nums)]
    print(f"\n5. Across+Down sums: {sums}")
    print(f"   As A1Z26 (mod 26): ", end='')
    for s in sums:
        v = s % 26
        print(chr(ord('A') + v - 1) if v > 0 else 'Z', end='')
    print()

    # The golden test: what do we know about the final 16-character code?
    print(f"\n6. FINAL CODE CONSTRAINTS:")
    print(f"   Length: 16 characters")
    print(f"   Known letters (row order): ", end='')
    for i in range(1, 17):
        if i in known_letters:
            print(known_letters[i], end='')
        else:
            print('_', end='')
    print()
    print(f"   Positions known: {list(known_letters.keys())}")
    print(f"   Positions unknown: {[i for i in range(1,17) if i not in known_letters]}")
    print(f"   Known letters: P (cell 13), S (cell 14), M (cell 15)")
    print(f"   Pattern: _ _ _ _ _ _ _ _ _ _ _ _ P S M _")

    # What if we need more crossword answers to get the other letters?
    print(f"\n7. Which entries could reveal unknown circled cell letters?")
    for ci, (r, c, ae, de, notes) in enumerate(circled_cells, 1):
        if ci not in known_letters:
            print(f"   Cell {ci:>2} ({r},{c}): solve {ae} or {de} -> '{notes}'")

    # Check if the 16 entry numbers from across entries encode something via A1Z26
    print(f"\n8. Across entry numbers at circled cells -> A1Z26:")
    print(f"   Numbers: {a_nums}")
    decoded = []
    for n in a_nums:
        v = n % 26
        decoded.append(chr(ord('A') + v - 1) if v > 0 else 'Z')
    result = ''.join(decoded)
    print(f"   Decoded: {result}")
    # Check if this is interesting
    print(f"   (Checking if this looks like anything meaningful...)")

    print(f"\n9. Down entry numbers at circled cells -> A1Z26:")
    print(f"   Numbers: {d_nums}")
    decoded_d = []
    for n in d_nums:
        v = n % 26
        decoded_d.append(chr(ord('A') + v - 1) if v > 0 else 'Z')
    result_d = ''.join(decoded_d)
    print(f"   Decoded: {result_d}")


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("=" * 72)
    print("  EXHAUSTIVE ANALYSIS OF 16 CIRCLED CELLS IN MRBEAST CROSSWORD")
    print("=" * 72)
    print(f"\nTotal circled cells: {len(circled_cells)}")
    print(f"Known letters: {known_letters}")
    print(f"Grid size: {GRID_SIZE}x{GRID_SIZE}")

    theory_a()
    theory_b()
    theory_c()
    theory_d()
    theory_e()
    theory_f()
    theory_g()
    cross_theory()

    print("\n" + "=" * 72)
    print("  ANALYSIS COMPLETE")
    print("=" * 72)
