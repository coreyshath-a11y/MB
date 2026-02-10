#!/usr/bin/env python3
"""
Validate the proposed staircase grid countries.
Check if letter overlaps are consistent and what the extraction column spells.
"""

# The proposed staircase countries (from community image)
# We need to figure out the exact staircase structure from the crossword

# From the "Close up of crossword grey" image, the staircase has ~11 rows
# It's in the bottom-right corner of the crossword puzzle page

# Let me try to reconstruct the staircase shape
# Looking at the user's handwritten image, the positions appear to be:

countries = [
    "OMAN",      # Row 1
    "GREECE",    # Row 2
    "ITALY",     # Row 3
    "JAPAN",     # Row 4
    "IRAN",      # Row 5
    "PERU",      # Row 6
    "SPAIN",     # Row 7
    "CIV",       # Row 8 (Cote d'Ivoire? Only 3 letters seems short)
    "GHANA",     # Row 9
    "KENYA",     # Row 10
    "LAOS",      # Row 11
]

# From the image, the staircase appears to have this structure:
# Each word is positioned at a specific column offset
# The staircase pattern from the crossword image shows:
# Words alternate between starting further left and further right
# Critical: overlapping cells must have matching letters

# Let me read the actual staircase structure from the grey image
# The close-up shows numbers 169, 170 at top
# And about 11 rows with varying widths and offsets

# Let me define the staircase layout based on what I can see:
# (start_col, length) for each row
# From the grey image, measuring cell positions:

# Row 1: starts at col 2, 4 cells    (cols 2-5)
# Row 2: starts at col 0, 6 cells    (cols 0-5)
# Row 3: starts at col 1, 5 cells    (cols 1-5)
# Row 4: starts at col 2, 5 cells    (cols 2-6)
# Row 5: starts at col 1, 4 cells    (cols 1-4)
# Row 6: starts at col 2, 4 cells    (cols 2-5)
# Row 7: starts at col 2, 5 cells    (cols 2-6)
# Row 8: starts at col 3, 3 cells    (cols 3-5) <-- CIV only 3 letters, suspicious
# Row 9: starts at col 0, 5 cells    (cols 0-4)
# Row 10: starts at col 1, 5 cells   (cols 1-5)
# Row 11: starts at col 1, 4 cells   (cols 1-4)

staircase_layout = [
    (2, 4),  # OMAN
    (0, 6),  # GREECE
    (1, 5),  # ITALY
    (2, 5),  # JAPAN
    (1, 4),  # IRAN
    (2, 4),  # PERU
    (2, 5),  # SPAIN
    (3, 3),  # CIV
    (0, 5),  # GHANA
    (1, 5),  # KENYA
    (1, 4),  # LAOS
]

# Verify lengths match
print("=== LENGTH VALIDATION ===")
all_match = True
for i, (country, (start, length)) in enumerate(zip(countries, staircase_layout)):
    match = len(country) == length
    if not match:
        all_match = False
    print(f"  Row {i+1}: {country:8s} length={len(country)}, slot={length} {'OK' if match else 'MISMATCH!'}")

print(f"\nAll lengths match: {all_match}")

# Build the staircase grid
max_col = max(start + length for start, length in staircase_layout)
n_rows = len(countries)
print(f"\nStaircase dimensions: {n_rows} rows x {max_col} cols")

# Place countries in grid
grid = [['.' for _ in range(max_col)] for _ in range(n_rows)]
for i, (country, (start, _)) in enumerate(zip(countries, staircase_layout)):
    for j, letter in enumerate(country):
        grid[i][start + j] = letter

# Print the staircase
print("\n=== STAIRCASE GRID ===")
for i, row in enumerate(grid):
    print(f"  Row {i+1:2d}: {''.join(row)}")

# Check overlapping cells (same column, adjacent rows)
print("\n=== OVERLAP CHECK ===")
overlaps = []
for col in range(max_col):
    col_letters = []
    for row in range(n_rows):
        if grid[row][col] != '.':
            col_letters.append((row, grid[row][col]))

    if len(col_letters) > 1:
        # Check if all letters in this column match (for adjacent cells)
        for k in range(len(col_letters) - 1):
            r1, l1 = col_letters[k]
            r2, l2 = col_letters[k + 1]
            if r2 == r1 + 1:  # Adjacent rows sharing a column
                match = l1 == l2
                overlaps.append((r1, r2, col, l1, l2, match))
                status = "MATCH" if match else "CONFLICT"
                print(f"  Col {col}: Row {r1+1}({l1}) vs Row {r2+1}({l2}) → {status}")

conflicts = [o for o in overlaps if not o[5]]
if conflicts:
    print(f"\n*** {len(conflicts)} CONFLICTS FOUND! ***")
    for r1, r2, col, l1, l2, _ in conflicts:
        print(f"    Col {col}: {countries[r1]}[{col - staircase_layout[r1][0]}]={l1} vs {countries[r2]}[{col - staircase_layout[r2][0]}]={l2}")
else:
    print(f"\n  No conflicts! All {len(overlaps)} overlaps match.")

# Extract the "central column" letters (the column that passes through most words)
print("\n=== COLUMN EXTRACTION ===")
for col in range(max_col):
    letters = []
    for row in range(n_rows):
        if grid[row][col] != '.':
            letters.append(grid[row][col])
    if len(letters) >= 3:
        print(f"  Col {col}: {''.join(letters)} ({len(letters)} letters)")

# Also try extracting where words cross (shared cells only)
print("\n=== SHARED CELL EXTRACTION ===")
shared_letters = []
for col in range(max_col):
    for row in range(n_rows - 1):
        if grid[row][col] != '.' and grid[row+1][col] != '.':
            shared_letters.append(grid[row][col])  # They should be equal
            break  # Only count once per pair

print(f"  Shared letters: {''.join(shared_letters)}")

# Alternative: for the staircase, the DOWN reading might be along the "step" edges
# Let's try reading the first letter of each word
print(f"\n  First letters: {''.join(c[0] for c in countries)}")
print(f"  Last letters: {''.join(c[-1] for c in countries)}")

# Try reading specific positions from each word
for pos in range(7):
    letters = []
    for c in countries:
        if pos < len(c):
            letters.append(c[pos])
        else:
            letters.append('_')
    print(f"  Position {pos}: {''.join(letters)}")

# Check if CIV is actually something else
print("\n=== CIV ANALYSIS ===")
print("CIV is only 3 letters - unusually short for a country name")
print("Possibilities:")
print("  - Côte d'Ivoire (abbreviated CIV in ISO)")
print("  - Could be a longer word: CIVIC (5), CIVIL (5), CIVILIZATION (12)")
print("  - Maybe the image shows more letters we can't read?")

# What if CIV is actually CIVIC or CIVIL?
for alt in ["CIVIC", "CIVIL"]:
    print(f"\n  If CIV → {alt}:")
    start, _ = staircase_layout[7]
    if len(alt) > 3:
        new_start = max(0, start - (len(alt) - 3) // 2)
        for offset in range(max(0, start - len(alt) + 1), start + 1):
            test_grid_row = ['.'] * max_col
            for j, letter in enumerate(alt):
                if offset + j < max_col:
                    test_grid_row[offset + j] = letter
            # Check overlaps
            ok = True
            for col in range(max_col):
                if test_grid_row[col] != '.' and grid[6][col] != '.' and test_grid_row[col] != grid[6][col]:
                    ok = False
                if test_grid_row[col] != '.' and grid[8][col] != '.' and test_grid_row[col] != grid[8][col]:
                    ok = False
            if ok:
                print(f"    Offset {offset}: {''.join(test_grid_row)} - no conflicts with adjacent rows")
