#!/usr/bin/env python3
"""
Staircase Grid Solver - Find the 11 hidden location names.

Staircase structure (columns 0-8):
  Row  1 (4 cells):       ████████      cols: [3, 4, 5, 6]
  Row  2 (6 cells):   ████████████      cols: [1, 2, 3, 4, 5, 6]
  Row  3 (5 cells):   ██████████        cols: [1, 2, 3, 4, 5]
  Row  4 (5 cells):       ██████████    cols: [3, 4, 5, 6, 7]
  Row  5 (4 cells):   ████████          cols: [1, 2, 3, 4]
  Row  6 (4 cells):       ████████      cols: [3, 4, 5, 6]
  Row  7 (5 cells):         ██████████  cols: [4, 5, 6, 7, 8]
  Row  8 (3 cells):       ██████        cols: [3, 4, 5]
  Row  9 (5 cells): ██████████          cols: [0, 1, 2, 3, 4]
  Row 10 (5 cells):     ██████████      cols: [2, 3, 4, 5, 6]
  Row 11 (4 cells):   ████████          cols: [1, 2, 3, 4]

Constraint: where two rows share a column, the letters must match.
"""

# Staircase row definitions: (word_length, [columns])
ROWS = [
    (4, [3, 4, 5, 6]),      # Row 1
    (6, [1, 2, 3, 4, 5, 6]),  # Row 2
    (5, [1, 2, 3, 4, 5]),    # Row 3
    (5, [3, 4, 5, 6, 7]),    # Row 4
    (4, [1, 2, 3, 4]),       # Row 5
    (4, [3, 4, 5, 6]),       # Row 6
    (5, [4, 5, 6, 7, 8]),    # Row 7
    (3, [3, 4, 5]),          # Row 8
    (5, [0, 1, 2, 3, 4]),    # Row 9
    (5, [2, 3, 4, 5, 6]),    # Row 10
    (4, [1, 2, 3, 4]),       # Row 11
]

# Build constraint pairs: (row_i, pos_in_i, row_j, pos_in_j)
constraints = []
for i in range(len(ROWS)):
    for j in range(i+1, len(ROWS)):
        cols_i = set(ROWS[i][1])
        cols_j = set(ROWS[j][1])
        shared = cols_i & cols_j
        for col in shared:
            pos_i = ROWS[i][1].index(col)
            pos_j = ROWS[j][1].index(col)
            constraints.append((i, pos_i, j, pos_j))

print(f"Total constraints: {len(constraints)}")

# Comprehensive world location name database
# Focus on well-known places that would appear in a mainstream puzzle

LOCATIONS_3 = [
    "GOA", "FEZ", "HUE", "ABO",
]

LOCATIONS_4 = [
    "ACCRA",  # Wait, 5 letters
    "BALI", "CUBA", "DOHA", "FIJI", "GUAM", "IRAN", "IRAQ", "LAOS",
    "LIMA", "MALI", "NICE", "OMAN", "OSLO", "PERU", "ROME", "SUVA",
    "TOGO", "CHAD", "GAZA", "BAKU", "LOME", "LYON", "BONN",
    "CORK", "YORK", "BATH", "MESA", "RENO", "WACO", "TROY",
    "NARA", "KOBE", "AGRA", "PUNE", "CEBU", "SANA",
    "RIGA", "BERN", "GRAZ", "LINZ", "KIEV", "LVIV",
    "APIA", "MALE",
]

LOCATIONS_5 = [
    "ACCRA", "TOKYO", "PARIS", "CAIRO", "MIAMI", "DUBAI", "KABUL",
    "DHAKA", "HANOI", "NAURU", "LAGOS", "DAKAR", "RABAT", "TUNIS",
    "MINSK", "SOFIA", "ABUJA", "ASMARA",  # 6 letters
    "QUITO", "TEMPE", "DOVER", "BOISE", "TULSA", "OMAHA",
    "DELHI", "OSAKA", "KYOTO", "BUSAN", "ARUBA", "MALTA",
    "NEPAL", "KENYA", "BENIN", "GABON", "NIGER", "SUDAN",
    "LIBYA", "SYRIA", "YEMEN", "SAMOA", "TONGA", "PALAU",
    "CHILE", "HAITI", "ITALY", "SPAIN", "CHINA", "JAPAN", "INDIA",
    "KOREA", "QATAR", "GHANA", "EGYPT", "CHILE", "BRAZIL",  # 6
    "MACAU", "PHUKET",  # 6
    "CUSCO", "LUXOR", "PETRA", "BANFF", "MOAB",  # 4
    "NIMES", "DIJON", "REIMS", "TOURS", "VISBY",
    "VADUZ", "THUN", "DAVOS", "SIENA", "PISA",  # 4
    "PERTH", "LHASA", "SOCHI", "KAZAN", "PSKOV",
    "OAXACA",  # 6
    "AUBER",
]

LOCATIONS_6 = [
    "LONDON", "BERLIN", "MOSCOW", "VIENNA", "LISBON", "DUBLIN",
    "ATHENS", "SYDNEY", "MUMBAI", "MANILA", "HAVANA", "BOGOTA",
    "NASSAU", "RIYADH", "MUSCAT", "TEHRAN", "ANKARA",
    "WARSAW", "PRAGUE", "ZURICH", "GENEVA", "NAPLES", "VENICE",
    "MADRID", "MALAGA", "MADRID",
    "OTTAWA", "DENVER", "AUSTIN", "BOSTON", "DALLAS", "FRESNO",
    "SEATTLE",  # 7
    "TOLEDO", "AUBURN", "REGINA", "NAGOYA",
    "ALEPPO", "CANCUN", "NASSAU", "BRUGES", "GDANSK",
    "BEIJING",  # 7
    "LAHORE", "YANGON", "JEDDAH", "LUSAKA", "MAPUTO",
    "BAMAKO", "BANJUL", "BISSAU", "HARARE", "KIGALI",
    "LUANDA", "MASERU",
]

# Clean up lists to correct lengths
LOCATIONS = {
    3: [w for w in LOCATIONS_3 if len(w) == 3],
    4: [w for w in LOCATIONS_4 if len(w) == 4],
    5: [w for w in LOCATIONS_5 if len(w) == 5],
    6: [w for w in LOCATIONS_6 if len(w) == 6],
}

# Remove duplicates
for k in LOCATIONS:
    LOCATIONS[k] = list(set(LOCATIONS[k]))

for k in sorted(LOCATIONS.keys()):
    print(f"Length {k}: {len(LOCATIONS[k])} locations")

# Build candidates per row
row_candidates = []
for row_idx, (length, cols) in enumerate(ROWS):
    candidates = LOCATIONS.get(length, [])
    row_candidates.append(candidates)
    print(f"Row {row_idx+1} (len={length}): {len(candidates)} candidates")

# Solve using backtracking with constraint propagation
grid = {}  # column -> letter (shared across all rows)
solution = [None] * 11

def is_consistent(row_idx, word):
    """Check if placing word at row_idx is consistent with current grid."""
    length, cols = ROWS[row_idx]
    for i, col in enumerate(cols):
        if col in grid and grid[col] != word[i]:
            return False
    return True

def place(row_idx, word):
    """Place word at row_idx, return list of newly set columns."""
    length, cols = ROWS[row_idx]
    new_cols = []
    for i, col in enumerate(cols):
        if col not in grid:
            grid[col] = word[i]
            new_cols.append(col)
    solution[row_idx] = word
    return new_cols

def unplace(row_idx, new_cols):
    """Undo placement."""
    for col in new_cols:
        del grid[col]
    solution[row_idx] = None

solutions = []
MAX_SOLUTIONS = 100

def solve(row_idx):
    if len(solutions) >= MAX_SOLUTIONS:
        return
    if row_idx == 11:
        solutions.append(list(solution))
        return

    for word in row_candidates[row_idx]:
        if is_consistent(row_idx, word):
            new_cols = place(row_idx, word)
            solve(row_idx + 1)
            unplace(row_idx, new_cols)

print("\nSolving...")
solve(0)

print(f"\nFound {len(solutions)} solutions")
for i, sol in enumerate(solutions[:20]):
    print(f"\n  Solution {i+1}:")
    for j, word in enumerate(sol):
        length, cols = ROWS[j]
        print(f"    Row {j+1:2d}: {word:6s} (cols {cols})")

    # Read the grid column by column
    g = {}
    for j, word in enumerate(sol):
        for k, col in enumerate(ROWS[j][1]):
            g[col] = word[k]
    print(f"    Grid cols 0-8: {''.join(g.get(c, '?') for c in range(9))}")

# If too many solutions, show what's constrained
if len(solutions) > 20:
    print(f"\n  ... and {len(solutions)-20} more")

    # Find positions where all solutions agree
    print("\n  Consensus letters:")
    for col in range(9):
        letters = set()
        for sol in solutions:
            for j, word in enumerate(sol):
                for k, c in enumerate(ROWS[j][1]):
                    if c == col:
                        letters.add(word[k])
        if len(letters) == 1:
            print(f"    Col {col}: {list(letters)[0]} (ALL solutions agree)")
        else:
            print(f"    Col {col}: {letters} ({len(letters)} options)")
