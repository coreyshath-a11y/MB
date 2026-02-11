#!/usr/bin/env python3
"""
Comprehensive Crossword Constraint Solver v5 for MrBeast Puzzle
25x25 grid with 176 entries (93 across, 95 down - but 12 already placed)
"""

# ============================================================
# 1. DEFINE THE 25x25 GRID AND ALL ENTRIES
# ============================================================

GRID_SIZE = 25

# All across entries: (label, row, col, length)
ACROSS_ENTRIES = [
    ("1A", 0, 0, 7), ("8A", 0, 9, 6), ("14A", 0, 17, 8),
    ("22A", 1, 0, 7), ("23A", 1, 8, 7), ("24A", 1, 17, 8),
    ("25A", 2, 0, 16), ("28A", 2, 17, 8), ("29A", 3, 0, 4),
    ("30A", 3, 5, 5), ("31A", 3, 11, 3), ("32A", 3, 15, 5),
    ("34A", 3, 21, 4), ("35A", 4, 0, 4), ("36A", 4, 7, 4),
    ("38A", 4, 12, 9), ("41A", 4, 22, 3), ("42A", 5, 0, 4),
    ("43A", 5, 5, 3), ("45A", 5, 9, 4), ("47A", 5, 14, 4),
    ("48A", 5, 20, 5), ("50A", 6, 0, 16), ("54A", 6, 17, 6),
    ("57A", 7, 0, 7), ("58A", 7, 8, 4), ("59A", 7, 13, 4),
    ("61A", 7, 18, 6), ("63A", 8, 0, 3), ("64A", 8, 4, 5),
    ("66A", 8, 10, 4), ("68A", 8, 16, 4), ("70A", 8, 21, 4),
    ("72A", 9, 3, 6), ("73A", 9, 11, 14), ("77A", 10, 1, 3),
    ("79A", 10, 5, 3), ("80A", 10, 10, 6), ("81A", 10, 17, 4),
    ("82A", 10, 22, 3), ("83A", 11, 0, 5), ("85A", 11, 6, 5),
    ("88A", 11, 12, 5), ("90A", 11, 18, 3), ("91A", 11, 22, 3),
    ("92A", 12, 0, 6), ("94A", 12, 7, 11), ("97A", 12, 19, 6),
    ("99A", 13, 0, 3), ("100A", 13, 4, 3), ("102A", 13, 8, 5),
    ("103A", 13, 14, 5), ("105A", 13, 20, 5), ("106A", 14, 0, 3),
    ("107A", 14, 4, 4), ("109A", 14, 9, 6), ("111A", 14, 17, 3),
    ("113A", 14, 21, 3), ("114A", 15, 0, 14), ("117A", 15, 16, 6),
    ("119A", 16, 0, 4), ("120A", 16, 5, 4), ("121A", 16, 11, 4),
    ("123A", 16, 16, 5), ("124A", 16, 22, 3), ("127A", 17, 1, 6),
    ("129A", 17, 8, 4), ("132A", 17, 13, 4), ("134A", 17, 18, 7),
    ("136A", 18, 2, 6), ("138A", 18, 9, 16), ("141A", 19, 0, 5),
    ("143A", 19, 7, 4), ("145A", 19, 12, 4), ("146A", 19, 17, 3),
    ("147A", 19, 21, 4), ("148A", 20, 0, 3), ("149A", 20, 4, 9),
    ("153A", 20, 14, 4), ("155A", 20, 21, 4), ("156A", 21, 0, 4),
    ("158A", 21, 5, 5), ("159A", 21, 11, 3), ("161A", 21, 15, 5),
    ("164A", 21, 21, 4), ("165A", 22, 0, 8), ("167A", 22, 9, 16),
    ("171A", 23, 0, 8), ("172A", 23, 10, 7), ("173A", 23, 18, 7),
    ("174A", 24, 0, 8), ("175A", 24, 10, 6), ("176A", 24, 18, 7),
]

# All down entries: (label, row, col, length)
DOWN_ENTRIES = [
    ("1D", 0, 0, 9), ("2D", 0, 1, 9), ("3D", 0, 2, 9), ("4D", 0, 3, 8),
    ("5D", 0, 4, 3), ("6D", 0, 5, 4), ("7D", 0, 6, 4), ("8D", 0, 9, 8),
    ("9D", 0, 10, 3), ("10D", 0, 11, 4), ("11D", 0, 12, 7), ("12D", 0, 13, 5),
    ("13D", 0, 14, 3), ("14D", 0, 17, 7), ("15D", 0, 18, 5), ("16D", 0, 19, 5),
    ("17D", 0, 20, 3), ("18D", 0, 21, 4), ("19D", 0, 22, 15), ("20D", 0, 23, 6),
    ("21D", 0, 24, 6), ("23D", 1, 8, 4), ("26D", 2, 7, 5), ("27D", 2, 15, 6),
    ("33D", 3, 16, 3), ("37D", 4, 10, 5), ("39D", 4, 14, 4), ("40D", 4, 20, 4),
    ("43D", 5, 5, 6), ("44D", 5, 6, 7), ("46D", 5, 11, 6), ("49D", 5, 21, 5),
    ("51D", 6, 4, 4), ("52D", 6, 8, 4), ("53D", 6, 13, 7), ("55D", 6, 18, 6),
    ("56D", 6, 19, 7), ("60D", 7, 16, 3), ("62D", 7, 23, 8), ("65D", 8, 7, 5),
    ("67D", 8, 12, 9), ("69D", 8, 17, 3), ("71D", 8, 24, 6), ("72D", 9, 3, 4),
    ("74D", 9, 14, 6), ("75D", 9, 15, 5), ("76D", 9, 20, 5), ("77D", 10, 1, 8),
    ("78D", 10, 2, 15), ("80D", 10, 10, 6), ("83D", 11, 0, 6), ("84D", 11, 4, 5),
    ("86D", 11, 8, 3), ("87D", 11, 9, 5), ("89D", 11, 16, 3), ("93D", 12, 5, 7),
    ("95D", 12, 11, 7), ("96D", 12, 17, 5), ("98D", 12, 21, 4), ("101D", 13, 6, 6),
    ("104D", 13, 18, 7), ("108D", 14, 7, 3), ("110D", 14, 13, 6), ("112D", 14, 19, 6),
    ("115D", 15, 3, 5), ("116D", 15, 8, 3), ("117D", 15, 16, 4), ("118D", 15, 20, 4),
    ("122D", 16, 14, 5), ("124D", 16, 22, 9), ("125D", 16, 23, 9), ("126D", 16, 24, 9),
    ("128D", 17, 4, 4), ("130D", 17, 9, 6), ("131D", 17, 10, 4), ("133D", 17, 15, 8),
    ("135D", 17, 21, 8), ("137D", 18, 7, 7), ("139D", 18, 12, 7), ("140D", 18, 17, 5),
    ("141D", 19, 0, 6), ("142D", 19, 1, 6), ("144D", 19, 8, 3), ("150D", 20, 5, 5),
    ("151D", 20, 6, 5), ("152D", 20, 11, 5), ("154D", 20, 16, 4), ("157D", 21, 3, 4),
    ("160D", 21, 13, 4), ("162D", 21, 18, 4), ("163D", 21, 19, 4), ("166D", 22, 4, 3),
    ("168D", 22, 10, 3), ("169D", 22, 14, 3), ("170D", 22, 20, 3),
]

ALL_ENTRIES = ACROSS_ENTRIES + DOWN_ENTRIES

# ============================================================
# 2. CONFIRMED PLACEMENTS
# ============================================================

CONFIRMED = {
    # (label, word, row, col, direction)
    "36A":  ("DORA",            4,  7,  "A"),
    "37D":  ("ABASH",           4,  10, "D"),
    "53D":  ("ROTUNDA",         6,  13, "D"),
    "58A":  ("PUSH",            7,  8,  "A"),
    "66A":  ("HAFT",            8,  10, "A"),
    "86D":  ("ZIP",             11, 8,  "A"),  # down
    "87D":  ("TRITE",           11, 9,  "A"),  # down
    "88A":  ("ADORN",           11, 12, "A"),
    "94A":  ("CIRCLEABOUT",     12, 7,  "A"),
    "96D":  ("TONER",           12, 17, "D"),
    "102A": ("PINTO",           13, 8,  "A"),
    "103A": ("ACHOO",           13, 14, "A"),
    "109A": ("TOLEDO",          14, 9,  "A"),
    "110D": ("DENVER",          14, 13, "D"),
    "117A": ("REGINA",          15, 16, "A"),
    "121A": ("TONI",            16, 11, "A"),
    "123A": ("ERASE",           16, 16, "A"),
    "167A": ("SUPERBOWLSTADIUM", 22, 9, "A"),
    "149A": ("BEASTLAND",       20, 4,  "A"),
}

HYPOTHETICAL = {
    "104D": ("ORGANIC",         13, 18, "D"),
    "111A": ("NRA",             14, 17, "A"),
}

# ============================================================
# 3. ANSWER POOL
# ============================================================

UNPLACED_ANSWERS = [
    # Length 3
    "RAD", "EAR", "ION", "EON",
    # Length 4
    "DHOW", "RACE", "NOTE",
    # Length 5
    "WAHOO", "OPERA", "LECAR", "ACCRA",
    # Length 6
    "SCHOOL", "OHIOAN", "HOODIE", "MATTER", "ECLAIR", "OPTION", "ORIENT",
    "CHAIRS", "CONVEX",
    # Length 7
    "TYPHOON", "OHSHOOT", "HEARTED", "MUSTERS", "CALIBER", "PORTION",
    "INUTERO", "QUORUMS", "HIRPLED",
    # Length 8
    "HOODWINK", "HULAHOOP", "SCENARIO", "NEUROTIC", "SCREENER", "ABSOLUTE",
    "TEAMSEAS", "DURATION", "CARBLITE", "POSITRON", "ROUTINES", "FLAMINGO",
    "CASHTENT",
    # Length 9
    "HOOVERDAM", "ROBINHOOD", "DITHERING", "HOWITZERS", "HIGHHEELS",
    "ALLUSIONS", "RESISTIVE", "INUNDATOR", "CABRIOLET", "RATPOISON",
    "OUTLINERS",
]

# P4 cities (unplaced)
P4_CITIES = [
    "TORONTO", "OWENSBORO", "ROSWELL", "DRESDEN", "TEMPE", "WARSAW",
    "SANJUAN", "ADELAIDE", "SEVILLE", "OTTAWA", "ROCHESTER", "ORLANDO",
    "WOODWAY", "AUBURN", "DOVER", "ANNAPOLIS",
]

# Combine all candidate answers
ALL_CANDIDATES = UNPLACED_ANSWERS + P4_CITIES

# Group by length
from collections import defaultdict
candidates_by_length = defaultdict(list)
for w in ALL_CANDIDATES:
    candidates_by_length[len(w)].append(w)

# ============================================================
# 4. BUILD THE LETTER GRID
# ============================================================

grid = [[None]*GRID_SIZE for _ in range(GRID_SIZE)]

def place_word(word, row, col, direction):
    """Place a word on the grid. direction: 'A'=across, 'D'=down"""
    conflicts = []
    for i, ch in enumerate(word):
        r = row + (i if direction == 'D' else 0)
        c = col + (i if direction == 'A' else 0)
        if r >= GRID_SIZE or c >= GRID_SIZE:
            conflicts.append(f"  OUT OF BOUNDS: ({r},{c}) for letter '{ch}'")
            continue
        if grid[r][c] is not None and grid[r][c] != ch:
            conflicts.append(f"  CONFLICT at ({r},{c}): grid has '{grid[r][c]}', trying to place '{ch}'")
        grid[r][c] = ch
    return conflicts

print("=" * 80)
print("STEP 1: PLACING CONFIRMED ENTRIES")
print("=" * 80)

# Place confirmed entries
for label, (word, row, col, direction) in sorted(CONFIRMED.items(), key=lambda x: x[0]):
    # Determine actual direction from entry list
    is_down = label.endswith("D") or (label in ["86D", "87D"])
    # Fix: direction should come from the label, not from stored direction
    actual_dir = "D" if label.endswith("D") else "A"
    conflicts = place_word(word, row, col, actual_dir)
    status = "OK" if not conflicts else "CONFLICT!"
    print(f"  {label:6s} = {word:20s} at ({row:2d},{col:2d}) {actual_dir} [{status}]")
    for c in conflicts:
        print(f"    {c}")

print()
print("PLACING HYPOTHETICAL ENTRIES:")
for label, (word, row, col, direction) in sorted(HYPOTHETICAL.items(), key=lambda x: x[0]):
    actual_dir = "D" if label.endswith("D") else "A"
    conflicts = place_word(word, row, col, actual_dir)
    status = "OK" if not conflicts else "CONFLICT!"
    print(f"  {label:6s} = {word:20s} at ({row:2d},{col:2d}) {actual_dir} [HYPO] [{status}]")
    for c in conflicts:
        print(f"    {c}")

# ============================================================
# 5. PRINT THE FULL CONSTRAINT GRID
# ============================================================

print()
print("=" * 80)
print("STEP 2: FULL 25x25 CONSTRAINT GRID (. = empty, letters = known)")
print("=" * 80)

print("     ", end="")
for c in range(GRID_SIZE):
    print(f"{c:2d}", end=" ")
print()
print("     ", end="")
for c in range(GRID_SIZE):
    print("--", end=" ")
print()

for r in range(GRID_SIZE):
    print(f"{r:2d} | ", end="")
    for c in range(GRID_SIZE):
        if grid[r][c] is not None:
            print(f" {grid[r][c]}", end=" ")
        else:
            print(" .", end=" ")
    print()

# ============================================================
# 6. BUILD CONSTRAINT PATTERNS FOR ALL ENTRIES
# ============================================================

print()
print("=" * 80)
print("STEP 3: CONSTRAINT PATTERNS FOR ALL 176 ENTRIES")
print("=" * 80)

placed_labels = set(CONFIRMED.keys()) | set(HYPOTHETICAL.keys())

def get_pattern(row, col, length, direction):
    """Get the constraint pattern for an entry"""
    pattern = []
    for i in range(length):
        r = row + (i if direction == 'D' else 0)
        c = col + (i if direction == 'A' else 0)
        if r < GRID_SIZE and c < GRID_SIZE and grid[r][c] is not None:
            pattern.append(grid[r][c])
        else:
            pattern.append('.')
    return ''.join(pattern)

def matches_pattern(word, pattern):
    """Check if a word matches a constraint pattern"""
    if len(word) != len(pattern):
        return False
    for w, p in zip(word, pattern):
        if p != '.' and w != p:
            return False
    return True

def count_constraints(pattern):
    """Count the number of known letters in a pattern"""
    return sum(1 for c in pattern if c != '.')

# Collect all entry data
entry_data = []
for label, row, col, length in ALL_ENTRIES:
    direction = 'D' if label.endswith('D') else 'A'
    pattern = get_pattern(row, col, length, direction)
    is_placed = label in placed_labels
    n_constraints = count_constraints(pattern)

    # Find matching candidates
    matching = []
    if not is_placed:
        for word in candidates_by_length.get(length, []):
            if matches_pattern(word, pattern):
                matching.append(word)

    entry_data.append({
        'label': label,
        'row': row,
        'col': col,
        'length': length,
        'direction': direction,
        'pattern': pattern,
        'is_placed': is_placed,
        'n_constraints': n_constraints,
        'matching': matching,
    })

# Print all entries organized by status
print("\n--- ALREADY PLACED ENTRIES ---")
for e in entry_data:
    if e['is_placed']:
        placed_word = CONFIRMED.get(e['label'], HYPOTHETICAL.get(e['label'], ('?',)))[0]
        hypo = " [HYPOTHETICAL]" if e['label'] in HYPOTHETICAL else ""
        print(f"  {e['label']:6s} len={e['length']:2d} at ({e['row']:2d},{e['col']:2d}) {e['direction']} = {placed_word}{hypo}")

print("\n--- UNPLACED ENTRIES WITH CONSTRAINTS (sorted by #constraints desc) ---")
constrained = [e for e in entry_data if not e['is_placed'] and e['n_constraints'] > 0]
constrained.sort(key=lambda x: (-x['n_constraints'], x['label']))

for e in constrained:
    n_match = len(e['matching'])
    match_str = ', '.join(e['matching']) if e['matching'] else '(no candidates match)'
    marker = " *** UNIQUE FIT ***" if n_match == 1 else ""
    marker = " *** NO FIT ***" if n_match == 0 else marker
    print(f"  {e['label']:6s} len={e['length']:2d} pattern=[{e['pattern']}] "
          f"constraints={e['n_constraints']} matches={n_match}: {match_str}{marker}")

print("\n--- UNPLACED ENTRIES WITH NO CONSTRAINTS ---")
unconstrained = [e for e in entry_data if not e['is_placed'] and e['n_constraints'] == 0]
unconstrained.sort(key=lambda x: x['label'])
for e in unconstrained:
    n_match = len(e['matching'])
    match_str = ', '.join(e['matching'][:10])
    if n_match > 10:
        match_str += f"... (+{n_match-10} more)"
    print(f"  {e['label']:6s} len={e['length']:2d} pattern=[{e['pattern']}] "
          f"matches={n_match}: {match_str}")

# ============================================================
# 7. UNIQUE FITS SUMMARY
# ============================================================

print()
print("=" * 80)
print("STEP 4: UNIQUE FITS (entries where exactly 1 candidate matches)")
print("=" * 80)

unique_fits = [e for e in entry_data if not e['is_placed'] and len(e['matching']) == 1]
unique_fits.sort(key=lambda x: -x['n_constraints'])

if unique_fits:
    for e in unique_fits:
        print(f"  {e['label']:6s} len={e['length']:2d} pattern=[{e['pattern']}] "
              f"=> {e['matching'][0]}")
else:
    print("  No unique fits found from candidate list alone.")

# ============================================================
# 8. CONFLICT CHECKING - Place each candidate and check crossings
# ============================================================

print()
print("=" * 80)
print("STEP 5: CONFLICT CHECKING FOR ALL MATCHING CANDIDATES")
print("=" * 80)

def check_placement_conflicts(entry, word):
    """
    Simulate placing a word at an entry position and check if any new letters
    conflict with existing grid letters at crossing points.
    Returns list of conflict descriptions, or empty list if no conflicts.
    """
    conflicts = []
    row, col, direction = entry['row'], entry['col'], entry['direction']

    for i, ch in enumerate(word):
        r = row + (i if direction == 'D' else 0)
        c = col + (i if direction == 'A' else 0)

        if r >= GRID_SIZE or c >= GRID_SIZE:
            conflicts.append(f"OUT OF BOUNDS ({r},{c})")
            continue

        # Check against existing grid
        if grid[r][c] is not None and grid[r][c] != ch:
            conflicts.append(f"({r},{c}): grid='{grid[r][c]}' vs word='{ch}'")

    return conflicts

for e in entry_data:
    if e['is_placed'] or not e['matching']:
        continue

    for word in e['matching']:
        conflicts = check_placement_conflicts(e, word)
        if conflicts:
            print(f"  CONFLICT: {e['label']} = {word}: {'; '.join(conflicts)}")

# ============================================================
# 9. CROSS-REFERENCING: For each constrained slot, show which
#    OTHER entries would be affected by placing each candidate
# ============================================================

print()
print("=" * 80)
print("STEP 6: CASCADING ANALYSIS - What new constraints does each placement add?")
print("=" * 80)

# Build a map from (row, col) -> list of entry labels that use that cell
cell_to_entries = defaultdict(list)
for e in entry_data:
    row, col, length, direction = e['row'], e['col'], e['length'], e['direction']
    for i in range(length):
        r = row + (i if direction == 'D' else 0)
        c = col + (i if direction == 'A' else 0)
        cell_to_entries[(r, c)].append((e['label'], i))

# For each constrained unplaced entry with matches, show cascade
for e in constrained:
    if not e['matching']:
        continue

    for word in e['matching']:
        new_letters = []
        row, col, direction = e['row'], e['col'], e['direction']
        for i, ch in enumerate(word):
            r = row + (i if direction == 'D' else 0)
            c = col + (i if direction == 'A' else 0)
            if grid[r][c] is None:
                # This is a new letter - find crossing entries
                crossings = []
                for other_label, other_idx in cell_to_entries[(r, c)]:
                    if other_label != e['label']:
                        crossings.append(f"{other_label}[pos {other_idx}]={ch}")
                if crossings:
                    new_letters.append(f"  ({r},{c})='{ch}' -> {', '.join(crossings)}")

        if new_letters:
            print(f"\n  If {e['label']} = {word}:")
            for nl in new_letters:
                print(f"    {nl}")

# ============================================================
# 10. FULL CASCADE SIMULATION - Try all unique fits and see
#     if they enable more unique fits
# ============================================================

print()
print("=" * 80)
print("STEP 7: FULL CASCADE SIMULATION")
print("=" * 80)

def simulate_cascade(initial_placements):
    """
    Starting from the current grid + initial_placements,
    iteratively find unique fits and place them.
    """
    # Create a copy of the grid
    sim_grid = [row[:] for row in grid]

    # Place initial placements
    placed = []
    for label, word in initial_placements:
        entry = next(e for e in entry_data if e['label'] == label)
        row, col, direction = entry['row'], entry['col'], entry['direction']
        for i, ch in enumerate(word):
            r = row + (i if direction == 'D' else 0)
            c = col + (i if direction == 'A' else 0)
            sim_grid[r][c] = ch
        placed.append((label, word))

    # Iteratively find unique fits
    iteration = 0
    while True:
        iteration += 1
        new_placements = []

        for e in entry_data:
            if e['is_placed'] or e['label'] in [p[0] for p in placed]:
                continue

            # Get pattern from sim_grid
            row, col, length, direction = e['row'], e['col'], e['length'], e['direction']
            pattern = []
            for i in range(length):
                r = row + (i if direction == 'D' else 0)
                c = col + (i if direction == 'A' else 0)
                if r < GRID_SIZE and c < GRID_SIZE and sim_grid[r][c] is not None:
                    pattern.append(sim_grid[r][c])
                else:
                    pattern.append('.')
            pat = ''.join(pattern)

            # Find matching candidates
            matching = [w for w in candidates_by_length.get(length, []) if matches_pattern(w, pat)]

            if len(matching) == 1:
                new_placements.append((e['label'], matching[0], pat))

        if not new_placements:
            break

        print(f"  Cascade iteration {iteration}:")
        for label, word, pat in new_placements:
            print(f"    {label} = {word} (pattern: [{pat}])")
            entry = next(e for e in entry_data if e['label'] == label)
            row, col, direction = entry['row'], entry['col'], entry['direction']
            for i, ch in enumerate(word):
                r = row + (i if direction == 'D' else 0)
                c = col + (i if direction == 'A' else 0)
                if sim_grid[r][c] is not None and sim_grid[r][c] != ch:
                    print(f"      *** CONFLICT at ({r},{c}): grid='{sim_grid[r][c]}' vs '{ch}' ***")
                sim_grid[r][c] = ch
            placed.append((label, word))

    return placed, sim_grid

# Try cascade from current state (no new initial placements)
print("\nCascade from current state (confirmed + hypothetical placements):")
placed, sim_grid = simulate_cascade([])
if not placed:
    print("  No new unique fits found from cascade.")

# Try cascade starting from each single unique fit
if unique_fits:
    print("\nCascade starting from each unique fit:")
    for uf in unique_fits:
        print(f"\n  Starting with {uf['label']} = {uf['matching'][0]}:")
        placed, _ = simulate_cascade([(uf['label'], uf['matching'][0])])
        if len(placed) <= 1:
            print("    No further cascade.")

# ============================================================
# 11. ENTRY LENGTH DISTRIBUTION
# ============================================================

print()
print("=" * 80)
print("STEP 8: ENTRY LENGTH DISTRIBUTION vs CANDIDATE LENGTH DISTRIBUTION")
print("=" * 80)

entry_lengths = defaultdict(int)
placed_lengths = defaultdict(int)
for e in entry_data:
    entry_lengths[e['length']] += 1
    if e['is_placed']:
        placed_lengths[e['length']] += 1

print(f"{'Length':>6s} {'Total':>6s} {'Placed':>7s} {'Open':>5s} {'Candidates':>11s}")
print("-" * 40)
for l in sorted(entry_lengths.keys()):
    total = entry_lengths[l]
    placed = placed_lengths[l]
    open_count = total - placed
    cands = len(candidates_by_length.get(l, []))
    surplus = "DEFICIT" if cands < open_count else ""
    print(f"{l:6d} {total:6d} {placed:7d} {open_count:5d} {cands:11d} {surplus}")

# ============================================================
# 12. DETAILED CROSSING ANALYSIS FOR KEY ENTRIES
# ============================================================

print()
print("=" * 80)
print("STEP 9: DETAILED CROSSING ANALYSIS FOR ALL CONSTRAINED ENTRIES")
print("=" * 80)

for e in constrained:
    if not e['matching']:
        continue

    row, col, length, direction = e['row'], e['col'], e['length'], e['direction']
    print(f"\n  {e['label']} (len={length}, pattern=[{e['pattern']}]):")
    print(f"    Candidates: {', '.join(e['matching'])}")

    # Show crossing entries at each position
    for i in range(length):
        r = row + (i if direction == 'D' else 0)
        c = col + (i if direction == 'A' else 0)

        crossers = []
        for other_label, other_idx in cell_to_entries[(r, c)]:
            if other_label != e['label']:
                other_entry = next(oe for oe in entry_data if oe['label'] == other_label)
                other_pat = other_entry['pattern']
                crossers.append(f"{other_label}[{other_idx}] pat=[{other_pat}]")

        letter_in_grid = grid[r][c] if grid[r][c] else '.'
        # What letters could go here from candidates?
        possible_letters = set(w[i] for w in e['matching'])

        cross_str = ', '.join(crossers) if crossers else 'no crossing'
        print(f"    pos {i} ({r},{c}) grid='{letter_in_grid}' possible={possible_letters} cross: {cross_str}")

# ============================================================
# 13. SUMMARY OF MOST PROMISING DEDUCTIONS
# ============================================================

print()
print("=" * 80)
print("STEP 10: SUMMARY OF MOST PROMISING DEDUCTIONS")
print("=" * 80)

# Entries with few matches (2-3) are also interesting
few_matches = [e for e in entry_data if not e['is_placed'] and 0 < len(e['matching']) <= 5]
few_matches.sort(key=lambda x: (len(x['matching']), -x['n_constraints']))

print("\nEntries with 1-5 candidate matches (most constrained):")
for e in few_matches:
    print(f"  {e['label']:6s} len={e['length']:2d} pattern=[{e['pattern']}] "
          f"({e['n_constraints']} known) => {', '.join(e['matching'])}")

# Entries with 0 matches (impossible with current candidates)
no_matches = [e for e in entry_data if not e['is_placed'] and e['n_constraints'] > 0 and len(e['matching']) == 0]
if no_matches:
    print("\nEntries with constraints but NO matching candidates (need new words):")
    for e in no_matches:
        print(f"  {e['label']:6s} len={e['length']:2d} pattern=[{e['pattern']}] "
              f"({e['n_constraints']} known letters)")

# ============================================================
# 14. SPECIAL: Check 167A SUPERBOWLSTADIUM interactions
# ============================================================

print()
print("=" * 80)
print("STEP 11: 167A=SUPERBOWLSTADIUM CROSSING ANALYSIS")
print("=" * 80)

e167 = next(e for e in entry_data if e['label'] == '167A')
row167, col167 = e167['row'], e167['col']
word167 = "SUPERBOWLSTADIUM"

for i, ch in enumerate(word167):
    c = col167 + i
    crossers = []
    for other_label, other_idx in cell_to_entries[(row167, c)]:
        if other_label != '167A':
            other_entry = next(oe for oe in entry_data if oe['label'] == other_label)
            placed_info = ""
            if other_entry['is_placed']:
                pw = CONFIRMED.get(other_label, HYPOTHETICAL.get(other_label, ('?',)))[0]
                placed_info = f" = {pw}"
            crossers.append(f"{other_label}[{other_idx}]{placed_info}")
    cross_str = ', '.join(crossers) if crossers else 'none'
    print(f"  pos {i:2d} ({22},{c:2d}) = '{ch}' crossings: {cross_str}")

# ============================================================
# 15. SPECIAL: Check 149A BEASTLAND interactions
# ============================================================

print()
print("=" * 80)
print("STEP 12: 149A=BEASTLAND CROSSING ANALYSIS")
print("=" * 80)

e149 = next(e for e in entry_data if e['label'] == '149A')
row149, col149 = e149['row'], e149['col']
word149 = "BEASTLAND"

for i, ch in enumerate(word149):
    c = col149 + i
    crossers = []
    for other_label, other_idx in cell_to_entries[(row149, c)]:
        if other_label != '149A':
            other_entry = next(oe for oe in entry_data if oe['label'] == other_label)
            placed_info = ""
            if other_entry['is_placed']:
                pw = CONFIRMED.get(other_label, HYPOTHETICAL.get(other_label, ('?',)))[0]
                placed_info = f" = {pw}"
            crossers.append(f"{other_label}[{other_idx}]{placed_info}")
    cross_str = ', '.join(crossers) if crossers else 'none'
    print(f"  pos {i:2d} ({20},{c:2d}) = '{ch}' crossings: {cross_str}")

# ============================================================
# 16. MUTUAL CONSTRAINT CHECK: pairs of crossing unplaced entries
# ============================================================

print()
print("=" * 80)
print("STEP 13: MUTUAL CONSTRAINT PAIRS (unplaced entries that cross each other)")
print("=" * 80)

# Find pairs of unplaced constrained entries that cross
crossing_pairs = []
for e1 in entry_data:
    if e1['is_placed'] or not e1['matching']:
        continue
    for e2 in entry_data:
        if e2['is_placed'] or not e2['matching'] or e1['label'] >= e2['label']:
            continue
        if e1['direction'] == e2['direction']:
            continue  # same direction entries don't cross

        # Find crossing point
        r1, c1, l1, d1 = e1['row'], e1['col'], e1['length'], e1['direction']
        r2, c2, l2, d2 = e2['row'], e2['col'], e2['length'], e2['direction']

        for i in range(l1):
            r_i = r1 + (i if d1 == 'D' else 0)
            c_i = c1 + (i if d1 == 'A' else 0)
            for j in range(l2):
                r_j = r2 + (j if d2 == 'D' else 0)
                c_j = c2 + (j if d2 == 'A' else 0)
                if r_i == r_j and c_i == c_j:
                    # Found crossing!
                    # Check compatibility
                    compatible = []
                    for w1 in e1['matching']:
                        for w2 in e2['matching']:
                            if w1[i] == w2[j]:
                                compatible.append((w1, w2, w1[i]))

                    if len(compatible) < len(e1['matching']) * len(e2['matching']):
                        crossing_pairs.append({
                            'e1': e1['label'], 'e2': e2['label'],
                            'pos': (r_i, c_i),
                            'idx1': i, 'idx2': j,
                            'total_combos': len(e1['matching']) * len(e2['matching']),
                            'compatible': compatible,
                            'words1': e1['matching'],
                            'words2': e2['matching'],
                        })

if crossing_pairs:
    for cp in crossing_pairs:
        print(f"\n  {cp['e1']} x {cp['e2']} at {cp['pos']}:")
        print(f"    {cp['e1']}[{cp['idx1']}] x {cp['e2']}[{cp['idx2']}]")
        print(f"    {cp['e1']} candidates: {cp['words1']}")
        print(f"    {cp['e2']} candidates: {cp['words2']}")
        print(f"    Compatible pairs ({len(cp['compatible'])}/{cp['total_combos']}):")
        for w1, w2, letter in cp['compatible']:
            print(f"      {w1} + {w2} (letter='{letter}')")
else:
    print("  No crossing pairs found among constrained unplaced entries.")

# ============================================================
# 17. COMPLETE GRID STATE WITH ROW/COL LABELS
# ============================================================

print()
print("=" * 80)
print("STEP 14: FINAL GRID STATE (complete)")
print("=" * 80)

# Count filled vs empty cells
filled = sum(1 for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] is not None)
total_white = sum(1 for e in entry_data for i in range(e['length']))  # approximate
print(f"Filled cells: {filled}")
print(f"Total entries: {len(entry_data)}")
print(f"Placed entries: {len(placed_labels)}")
print(f"Unplaced entries: {len(entry_data) - len(placed_labels)}")
print(f"Unplaced with constraints: {len(constrained)}")
print(f"Unplaced with unique fits: {len(unique_fits)}")

print("\nGrid (. = empty white cell, letters = filled):")
print("      ", end="")
for c in range(GRID_SIZE):
    print(f"{c%10}", end="")
print()
for r in range(GRID_SIZE):
    print(f"  {r:2d} | ", end="")
    for c in range(GRID_SIZE):
        if grid[r][c] is not None:
            print(grid[r][c], end="")
        else:
            print(".", end="")
    print(f" | {r}")
print("      ", end="")
for c in range(GRID_SIZE):
    print(f"{c%10}", end="")
print()

print("\n\nDone! Comprehensive solver v5 complete.")
