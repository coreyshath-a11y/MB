#!/usr/bin/env python3
"""
Test alternative ways to read the crossword grid for hidden messages.
Checks 13 different reading patterns on the partial 25x25 grid.
"""

import itertools
import re
import string
from collections import defaultdict

# ── The partial 25×25 grid ──────────────────────────────────────────────
grid_text = [
    ".......##......##........",  # R0
    ".......#.......##........",  # R1
    "................#........",  # R2
    "....#.....#...#.....#....",  # R3
    "....###DORA#.........#...",  # R4
    "....#...#.B..#....##.....",  # R5
    "..........A..R..#......##",  # R6
    ".......#PUSH#O...#......#",  # R7
    "...#.....#HAFT##....#....",  # R8
    "###......##..U...........",  # R9
    "#...#...##...N..#....#...",  # R10
    ".....#..ZT.#ADORN#...#...",  # R11
    "......#CIRCLEABOUT#......",  # R12
    "...#...#PINTO#ACHOO#.....",  # R13
    "...#....#TOLEDO##NRA#...#",  # R14
    ".........E...E##REGINA###",  # R15
    "....#....##TONI#ERASE#...",  # R16
    "#......#....#V...#.......",  # R17
    "##......#....E...........",  # R18
    ".....##....#.R..#...#....",  # R19
    "...#BEASTLAND#....###....",  # R20
    "....#.....#...#.....#....",  # R21
    "........#SUPERBOWLSTADIUM",  # R22
    "........##.......#.......",  # R23
    "........##......##.......",  # R24
]

ROWS = 25
COLS = 25

# Parse grid into 2D array
grid = []
for r, line in enumerate(grid_text):
    row = []
    for c, ch in enumerate(line):
        row.append(ch)
    grid.append(row)

def cell(r, c):
    """Return the character at (r,c) or None if out of bounds."""
    if 0 <= r < ROWS and 0 <= c < COLS:
        return grid[r][c]
    return None

def is_letter(ch):
    """True if ch is an uppercase letter (filled cell)."""
    return ch is not None and ch.isalpha() and ch.isupper()

def is_filled(ch):
    """True if ch is a letter (filled). '.' = unfilled, '#' = black."""
    return ch is not None and ch not in ('.', '#')

# ── Word list for checking ──────────────────────────────────────────────
WORDS = set()
try:
    from english_words import get_english_words_set
    raw = get_english_words_set(['gcide'])
    WORDS = {w.upper() for w in raw if len(w) >= 3 and w.isalpha()}
    print(f"[INFO] Loaded {len(WORDS)} words from english_words package.\n")
except Exception:
    pass

if not WORDS:
    try:
        with open('/usr/share/dict/words', 'r') as f:
            for w in f:
                w = w.strip().upper()
                if len(w) >= 3:
                    WORDS.add(w)
        print(f"[INFO] Loaded {len(WORDS)} words from system dictionary.\n")
    except FileNotFoundError:
        WORDS = {
            "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN",
            "HER", "WAS", "ONE", "OUR", "OUT", "DAY", "HAD", "HAS", "HIS",
            "HOW", "MAN", "NEW", "NOW", "OLD", "SEE", "WAY", "WHO", "BOY",
            "DID", "ITS", "LET", "PUT", "SAY", "SHE", "TOO", "USE",
            "BEAST", "LAND", "CODE", "HIDE", "FIND", "PRIZE", "SECRET",
            "MILLION", "DOLLAR", "SUPER", "BOWL", "STADIUM", "ISLAND",
            "WORLD", "AROUND", "EVERY", "CHALLENGE", "LEADS", "TOWARDS",
            "LOCATION", "NAME", "SOMEWHERE", "PUSH", "DORA", "HAFT",
            "ADORN", "PINTO", "ACHOO", "TOLEDO", "REGINA", "TONI", "ERASE",
            "TONER", "DENVER", "CIRCLEABOUT", "BEASTLAND", "SUPERBOWLSTADIUM",
        }
        print(f"[INFO] No dictionary found. Using curated list of {len(WORDS)} words.\n")

def find_words_in_string(s, min_len=3, max_results=25):
    """Find all dictionary words that appear as substrings in s."""
    found = []
    s_upper = s.upper()
    for w in WORDS:
        if len(w) >= min_len and len(w) <= len(s_upper) and w in s_upper:
            idx = s_upper.find(w)
            found.append((w, idx))
    found.sort(key=lambda x: (-len(x[0]), x[1]))
    return found[:max_results]


# ═══════════════════════════════════════════════════════════════════════
# TEST 1: Main Diagonal (top-left to bottom-right)
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 1: Main Diagonal (top-left to bottom-right)")
print("=" * 70)
diag_main = []
for i in range(min(ROWS, COLS)):
    ch = grid[i][i]
    diag_main.append((i, i, ch))
letters_only = ''.join(ch for _, _, ch in diag_main if is_filled(ch))
all_chars = ''.join(ch if is_filled(ch) else '_' for _, _, ch in diag_main)
print(f"  All cells:    {all_chars}")
print(f"  Letters only: {letters_only}")
words = find_words_in_string(letters_only)
if words:
    print(f"  Words found:  {words}")
else:
    print("  No dictionary words found.")
print()


# ═══════════════════════════════════════════════════════════════════════
# TEST 2: Anti-Diagonal (top-right to bottom-left)
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 2: Anti-Diagonal (top-right to bottom-left)")
print("=" * 70)
diag_anti = []
for i in range(min(ROWS, COLS)):
    r, c = i, COLS - 1 - i
    ch = grid[r][c]
    diag_anti.append((r, c, ch))
letters_only = ''.join(ch for _, _, ch in diag_anti if is_filled(ch))
all_chars = ''.join(ch if is_filled(ch) else '_' for _, _, ch in diag_anti)
print(f"  All cells:    {all_chars}")
print(f"  Letters only: {letters_only}")
words = find_words_in_string(letters_only)
if words:
    print(f"  Words found:  {words}")
else:
    print("  No dictionary words found.")
print()


# ═══════════════════════════════════════════════════════════════════════
# TEST 3: All Diagonals
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 3: All Diagonals (both directions, min 3 letters)")
print("=" * 70)

def get_all_diagonals():
    """Return all diagonals (top-left to bottom-right and top-right to bottom-left)."""
    diags = []
    # TL-BR diagonals
    for start_c in range(COLS):
        d = []
        r, c = 0, start_c
        while r < ROWS and c < COLS:
            d.append((r, c, grid[r][c]))
            r += 1; c += 1
        diags.append(('TL-BR', start_c, d))
    for start_r in range(1, ROWS):
        d = []
        r, c = start_r, 0
        while r < ROWS and c < COLS:
            d.append((r, c, grid[r][c]))
            r += 1; c += 1
        diags.append(('TL-BR', f'r{start_r}', d))
    # TR-BL diagonals
    for start_c in range(COLS):
        d = []
        r, c = 0, start_c
        while r < ROWS and c >= 0:
            d.append((r, c, grid[r][c]))
            r += 1; c -= 1
        diags.append(('TR-BL', start_c, d))
    for start_r in range(1, ROWS):
        d = []
        r, c = start_r, COLS - 1
        while r < ROWS and c >= 0:
            d.append((r, c, grid[r][c]))
            r += 1; c -= 1
        diags.append(('TR-BL', f'r{start_r}', d))
    return diags

all_diags = get_all_diagonals()
diag_word_hits = []
for direction, start, cells in all_diags:
    letters = ''.join(ch for _, _, ch in cells if is_filled(ch))
    if len(letters) >= 3:
        words_found = find_words_in_string(letters)
        if words_found:
            diag_word_hits.append((direction, start, letters, words_found))

if diag_word_hits:
    for direction, start, letters, words_found in diag_word_hits:
        print(f"  {direction} start={start}: '{letters}' -> {words_found}")
else:
    print("  No words found in any diagonal.")
print()


# ═══════════════════════════════════════════════════════════════════════
# TEST 4: Spiral Read (outside in, clockwise)
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 4: Spiral Read (outside-in, clockwise)")
print("=" * 70)

def spiral_order(rows, cols):
    """Generate (r,c) in spiral order, outside-in clockwise."""
    top, bottom, left, right = 0, rows - 1, 0, cols - 1
    coords = []
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            coords.append((top, c))
        top += 1
        for r in range(top, bottom + 1):
            coords.append((r, right))
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                coords.append((bottom, c))
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                coords.append((r, left))
            left += 1
    return coords

spiral_coords = spiral_order(ROWS, COLS)
spiral_letters = ''.join(grid[r][c] for r, c in spiral_coords if is_filled(grid[r][c]))
spiral_all = ''.join(grid[r][c] if is_filled(grid[r][c]) else '_' for r, c in spiral_coords)

print(f"  Letters only ({len(spiral_letters)} chars): {spiral_letters[:100]}...")
if len(spiral_letters) > 100:
    print(f"    ...{spiral_letters[100:]}")
words = find_words_in_string(spiral_letters, min_len=4)
if words:
    print(f"  Words found (>=4 chars): {words[:20]}")
else:
    print("  No dictionary words found (>=4 chars).")
print()


# ═══════════════════════════════════════════════════════════════════════
# TEST 5: Snake/Boustrophedon Read
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 5: Snake/Boustrophedon Read")
print("=" * 70)
snake_letters = []
for r in range(ROWS):
    if r % 2 == 0:
        for c in range(COLS):
            if is_filled(grid[r][c]):
                snake_letters.append(grid[r][c])
    else:
        for c in range(COLS - 1, -1, -1):
            if is_filled(grid[r][c]):
                snake_letters.append(grid[r][c])
snake_str = ''.join(snake_letters)
print(f"  Letters ({len(snake_str)} chars): {snake_str[:100]}...")
if len(snake_str) > 100:
    print(f"    ...{snake_str[100:]}")
words = find_words_in_string(snake_str, min_len=4)
if words:
    print(f"  Words found (>=4 chars): {words[:20]}")
else:
    print("  No dictionary words found (>=4 chars).")
print()


# ═══════════════════════════════════════════════════════════════════════
# TEST 6: Column Reads
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 6: Column Reads (top to bottom)")
print("=" * 70)
for c in range(COLS):
    col_letters = ''.join(grid[r][c] for r in range(ROWS) if is_filled(grid[r][c]))
    if len(col_letters) >= 3:
        words = find_words_in_string(col_letters, min_len=3)
        if words:
            print(f"  Col {c:2d}: '{col_letters}' -> {words}")
        else:
            print(f"  Col {c:2d}: '{col_letters}'")
    else:
        print(f"  Col {c:2d}: '{col_letters}' (too short)")
print()


# ═══════════════════════════════════════════════════════════════════════
# TEST 7: First letter of each placed entry in numerical order
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 7: First letters of placed entries in entry-number order")
print("=" * 70)

# Placed entries with their entry numbers
placed_entries = [
    (36, 'A', 'DORA'),
    (37, 'D', 'ABASH'),      # starts at (4,10) going down: A,B,A,S,H?
    (53, 'D', 'ROTUNDA'),
    (58, 'A', 'PUSH'),
    (66, 'A', 'HAFT'),
    (86, 'D', 'ZIP'),
    (87, 'D', 'TRITE'),
    (88, 'A', 'ADORN'),
    (94, 'A', 'CIRCLEABOUT'),
    (96, 'D', 'TONER'),
    (102, 'A', 'PINTO'),
    (103, 'A', 'ACHOO'),
    (109, 'A', 'TOLEDO'),
    (110, 'D', 'DENVER'),
    (117, 'A', 'REGINA'),
    (121, 'A', 'TONI'),
    (123, 'A', 'ERASE'),
    (149, 'A', 'BEASTLAND'),
    (167, 'A', 'SUPERBOWLSTADIUM'),
]

# Sort by entry number
placed_entries.sort(key=lambda x: x[0])

first_letters = ''.join(e[2][0] for e in placed_entries)
print(f"  Entries (sorted): {[(e[0], e[1], e[2]) for e in placed_entries]}")
print(f"  First letters: {first_letters}")
words = find_words_in_string(first_letters, min_len=3)
if words:
    print(f"  Words found: {words}")
print()


# ═══════════════════════════════════════════════════════════════════════
# TEST 8: Last letters of placed entries in numerical order
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 8: Last letters of placed entries in entry-number order")
print("=" * 70)
last_letters = ''.join(e[2][-1] for e in placed_entries)
print(f"  Last letters: {last_letters}")
words = find_words_in_string(last_letters, min_len=3)
if words:
    print(f"  Words found: {words}")
print()


# ═══════════════════════════════════════════════════════════════════════
# TEST 9: Middle letters of placed entries
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 9: Middle letters of placed entries")
print("=" * 70)
middle_letters = ''.join(e[2][len(e[2])//2] for e in placed_entries)
print(f"  Middle letters: {middle_letters}")
words = find_words_in_string(middle_letters, min_len=3)
if words:
    print(f"  Words found: {words}")
print()


# ═══════════════════════════════════════════════════════════════════════
# TEST 10: Nth letter extraction
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 10: Nth letter extraction (position in list = letter index)")
print("=" * 70)
nth_letters = []
for idx, entry in enumerate(placed_entries):
    word = entry[2]
    n = idx  # 0-based
    if n < len(word):
        nth_letters.append(word[n])
        print(f"  Entry #{idx+1} ({entry[0]}{entry[1]} = {word}): letter[{n}] = '{word[n]}'")
    else:
        nth_letters.append('?')
        print(f"  Entry #{idx+1} ({entry[0]}{entry[1]} = {word}): index {n} out of range (len={len(word)})")
nth_str = ''.join(nth_letters)
print(f"  Result: {nth_str}")
words = find_words_in_string(nth_str.replace('?', ''), min_len=3)
if words:
    print(f"  Words found: {words}")
print()

# Also try 1-based indexing
print("  --- Also trying 1-based indexing ---")
nth_letters_1 = []
for idx, entry in enumerate(placed_entries):
    word = entry[2]
    n = idx + 1  # 1-based
    if n <= len(word):
        nth_letters_1.append(word[n-1])
    else:
        nth_letters_1.append('?')
nth_str_1 = ''.join(nth_letters_1)
print(f"  Result (1-based): {nth_str_1}")
words = find_words_in_string(nth_str_1.replace('?', ''), min_len=3)
if words:
    print(f"  Words found: {words}")
print()


# ═══════════════════════════════════════════════════════════════════════
# TEST 11: Cells adjacent to black cells (border cells)
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 11: Letters adjacent to black cells")
print("=" * 70)
border_letters = []
for r in range(ROWS):
    for c in range(COLS):
        if is_filled(grid[r][c]):
            # Check 4-neighbors for black cell
            neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
            touches_black = False
            for nr, nc in neighbors:
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    if grid[nr][nc] == '#':
                        touches_black = True
                        break
                else:
                    # edge of grid counts as adjacent to boundary
                    pass
            if touches_black:
                border_letters.append((r, c, grid[r][c]))

border_str = ''.join(ch for _, _, ch in border_letters)
print(f"  Border letters ({len(border_str)} chars): {border_str}")
words = find_words_in_string(border_str, min_len=4)
if words:
    print(f"  Words found (>=4 chars): {words[:20]}")
print()

# Also try reading just the letters that are immediately AFTER a black cell (left-to-right)
print("  --- Letters immediately right of a black cell (row by row) ---")
after_black = []
for r in range(ROWS):
    for c in range(COLS):
        if is_filled(grid[r][c]) and c > 0 and grid[r][c-1] == '#':
            after_black.append(grid[r][c])
after_str = ''.join(after_black)
print(f"  After-black letters: {after_str}")
words = find_words_in_string(after_str, min_len=3)
if words:
    print(f"  Words found: {words}")
print()


# ═══════════════════════════════════════════════════════════════════════
# TEST 12: Word Search
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 12: Word Search (horizontal, vertical, diagonal, both dirs)")
print("=" * 70)

target_words = [
    "MRBEAST", "BEAST", "SUPERBOWL", "LEVIS", "STADIUM", "MILLION",
    "DOLLAR", "PRIZE", "SECRET", "CODE", "ENDGAME", "HIDE", "FIND",
    "ISLAND", "BARCLAY", "MALI", "TEHRAN", "LAGOS", "SUDAN", "OMAN",
    "ADEN", "WALES", "NIGER", "DELHI", "CHAD", "DAKAR", "AROUNDWORLD",
    "MELANESIANS", "PUZZLE", "HUNT", "TREASURE", "FINAL", "ANSWER",
    "CLUE", "SUBMIT", "REWARD", "MONEY", "CASH", "CIRCLE", "ABOUT",
    "DORA", "PUSH", "HAFT", "ADORN", "PINTO", "ACHOO", "TOLEDO",
    "REGINA", "TONI", "ERASE", "DENVER", "TONER", "BEASTLAND",
    "ROTUNDA", "ABASH", "ZIP", "TRITE", "NRA", "ORGANIC",
    "AROUND", "WORLD", "EVERY", "CHALLENGE", "LEADS", "TOWARDS",
    "LOCATION", "NAME", "SOMEWHERE",
]

def extract_all_lines():
    """Extract all horizontal, vertical, and diagonal lines from the grid."""
    lines = []
    # Horizontal
    for r in range(ROWS):
        line = ''.join(grid[r])
        lines.append(('H', r, 0, 0, 1, line))
    # Vertical
    for c in range(COLS):
        line = ''.join(grid[r][c] for r in range(ROWS))
        lines.append(('V', 0, c, 1, 0, line))
    # Diagonals TL-BR
    for start in range(-(ROWS-1), COLS):
        line_chars = []
        r0 = max(0, -start)
        c0 = max(0, start)
        r, c = r0, c0
        while r < ROWS and c < COLS:
            line_chars.append(grid[r][c])
            r += 1; c += 1
        lines.append(('D1', r0, c0, 1, 1, ''.join(line_chars)))
    # Diagonals TR-BL
    for start in range(0, ROWS + COLS - 1):
        line_chars = []
        r0 = max(0, start - COLS + 1)
        c0 = min(start, COLS - 1)
        r, c = r0, c0
        while r < ROWS and c >= 0:
            line_chars.append(grid[r][c])
            r += 1; c -= 1
        lines.append(('D2', r0, c0, 1, -1, ''.join(line_chars)))
    return lines

all_lines = extract_all_lines()
found_in_search = defaultdict(list)

for word in target_words:
    for direction, r0, c0, dr, dc, line in all_lines:
        # Forward
        idx = line.find(word)
        while idx != -1:
            found_in_search[word].append((direction, r0 + idx * dr, c0 + idx * dc, 'fwd'))
            idx = line.find(word, idx + 1)
        # Reverse
        rev = word[::-1]
        idx = line.find(rev)
        while idx != -1:
            found_in_search[word].append((direction, r0 + idx * dr, c0 + idx * dc, 'rev'))
            idx = line.find(rev, idx + 1)

for word in target_words:
    if word in found_in_search:
        for hit in found_in_search[word]:
            print(f"  FOUND: '{word}' at dir={hit[0]}, start=({hit[1]},{hit[2]}), {hit[3]}")
    # Don't print "not found" for every word - too noisy

# Report words NOT found
not_found = [w for w in target_words if w not in found_in_search]
print(f"\n  Not found: {not_found}")
print()

# Now also do a broader word search: look for ANY dictionary word >= 5 letters
# Use only letters (strip . and #) for each line to find hidden words in fill
print("  --- Broader word search: any dictionary word >= 5 letters ---")
print("  (Searching only filled-cell sequences for non-trivial hidden words)")
broader_hits = defaultdict(list)
target_upper = {w.upper() for w in target_words}

# Build letter-only versions of each line (contiguous letter runs)
def extract_letter_runs(line_str):
    """Extract runs of consecutive uppercase letters from a line."""
    runs = []
    current = []
    for ch in line_str:
        if ch.isalpha() and ch.isupper():
            current.append(ch)
        else:
            if current:
                runs.append(''.join(current))
                current = []
    if current:
        runs.append(''.join(current))
    return runs

# Filter dictionary to words >= 5 letters for performance
big_words = {w for w in WORDS if len(w) >= 5}

for direction, r0, c0, dr, dc, line in all_lines:
    runs = extract_letter_runs(line)
    for run in runs:
        if len(run) < 5:
            continue
        for word in big_words:
            if len(word) > len(run):
                continue
            if word in run and word not in target_upper:
                broader_hits[word].append((direction, r0, c0, 'fwd', run))
            rev = run[::-1]
            if word in rev and word not in target_upper:
                broader_hits[word].append((direction, r0, c0, 'rev', run))

# Show top results sorted by length
shown = 0
for word in sorted(broader_hits.keys(), key=lambda w: -len(w)):
    locs = broader_hits[word]
    contexts = set(loc[4] for loc in locs)
    print(f"  FOUND (broader): '{word}' in {contexts}")
    shown += 1
    if shown >= 40:
        print(f"  ... and {len(broader_hits) - shown} more words found")
        break

print()


# ═══════════════════════════════════════════════════════════════════════
# TEST 13: Circled Cells
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 13: Circled cells reading in different orders")
print("=" * 70)

circled_cells = [
    (0, 12), (2, 4), (3, 8), (3, 24), (4, 19), (10, 12),
    (11, 2), (11, 22), (13, 0), (18, 7), (19, 17), (20, 2),
    (22, 11), (22, 18), (22, 24), (24, 20),
]

# Show what's currently in each circled cell
print("  Circled cell contents:")
for r, c in circled_cells:
    ch = grid[r][c]
    status = "LETTER" if is_filled(ch) else ("black" if ch == '#' else "unfilled")
    print(f"    ({r:2d},{c:2d}): '{ch}' [{status}]")

# Extract letters where available
def read_circled(order):
    result = []
    for r, c in order:
        ch = grid[r][c]
        if is_filled(ch):
            result.append(ch)
        else:
            result.append('_')
    return ''.join(result)

# Row order (default)
print(f"\n  Row order:       {read_circled(circled_cells)}")
# Reverse row order
print(f"  Reverse row:     {read_circled(list(reversed(circled_cells)))}")
# By column order
by_col = sorted(circled_cells, key=lambda x: (x[1], x[0]))
print(f"  Column order:    {read_circled(by_col)}")
# By column reversed
print(f"  Column reversed: {read_circled(list(reversed(by_col)))}")

# Clockwise from top-left (approximate: sort by angle from center)
center_r = sum(r for r, c in circled_cells) / len(circled_cells)
center_c = sum(c for r, c in circled_cells) / len(circled_cells)
import math
by_angle = sorted(circled_cells, key=lambda x: math.atan2(x[0] - center_r, x[1] - center_c))
print(f"  Clockwise:       {read_circled(by_angle)}")
print(f"  Counter-CW:      {read_circled(list(reversed(by_angle)))}")

# By distance from center (inside out)
by_dist = sorted(circled_cells, key=lambda x: (x[0] - center_r)**2 + (x[1] - center_c)**2)
print(f"  Inside-out:      {read_circled(by_dist)}")
print(f"  Outside-in:      {read_circled(list(reversed(by_dist)))}")

print(f"\n  Note: Only 3 cells have known letters. Need more grid fill to test fully.")
print()


# ═══════════════════════════════════════════════════════════════════════
# BONUS: Additional pattern tests
# ═══════════════════════════════════════════════════════════════════════

print("=" * 70)
print("BONUS A: Read only the central row and central column")
print("=" * 70)
mid_r = ROWS // 2
mid_c = COLS // 2
central_row = ''.join(grid[mid_r][c] for c in range(COLS))
central_col = ''.join(grid[r][mid_c] for r in range(ROWS))
central_row_letters = ''.join(ch for ch in central_row if ch.isalpha())
central_col_letters = ''.join(ch for ch in central_col if ch.isalpha())
print(f"  Central row ({mid_r}): {central_row}")
print(f"    Letters: {central_row_letters}")
print(f"  Central col ({mid_c}): {central_col}")
print(f"    Letters: {central_col_letters}")
words_r = find_words_in_string(central_row_letters, min_len=3)
words_c = find_words_in_string(central_col_letters, min_len=3)
if words_r:
    print(f"    Row words: {words_r}")
if words_c:
    print(f"    Col words: {words_c}")
print()


print("=" * 70)
print("BONUS B: Intersection letters (cells at crossing of Across/Down)")
print("=" * 70)
# This is hard to determine without full numbering, but we can look at
# the specific intersection cells for our placed entries
print("  (Skipped - requires full entry position mapping)")
print()


print("=" * 70)
print("BONUS C: Every Nth cell reading (N=1,2,3,5,7,11,...)")
print("=" * 70)
# Flatten all filled cells row by row
all_filled = []
for r in range(ROWS):
    for c in range(COLS):
        if is_filled(grid[r][c]):
            all_filled.append((r, c, grid[r][c]))

print(f"  Total filled cells: {len(all_filled)}")
for N in [2, 3, 5, 7, 11, 13, 16, 17, 19]:
    every_n = ''.join(ch for i, (_, _, ch) in enumerate(all_filled) if i % N == 0)
    words = find_words_in_string(every_n, min_len=4)
    word_note = f" -> {words}" if words else ""
    print(f"  Every {N:2d}th: {every_n[:60]}{'...' if len(every_n)>60 else ''}{word_note}")
print()


print("=" * 70)
print("BONUS D: Reading entry answers by length")
print("=" * 70)
# Group placed entries by length and read first letters
by_length = defaultdict(list)
for num, direction, word in placed_entries:
    by_length[len(word)].append((num, direction, word))
for length in sorted(by_length.keys()):
    entries = by_length[length]
    first = ''.join(e[2][0] for e in entries)
    last = ''.join(e[2][-1] for e in entries)
    print(f"  Length {length:2d} ({len(entries)} entries): first='{first}' last='{last}'")
print()


print("=" * 70)
print("BONUS E: Column 13 (ROTUNDA column) - full vertical read")
print("=" * 70)
col13 = []
for r in range(ROWS):
    ch = grid[r][13]
    col13.append(ch if is_filled(ch) else '_')
col13_str = ''.join(col13)
col13_letters = ''.join(ch for ch in col13 if ch != '_')
print(f"  Column 13 (all):     {col13_str}")
print(f"  Column 13 (letters): {col13_letters}")
words = find_words_in_string(col13_letters, min_len=3)
if words:
    print(f"  Words: {words}")
print()


print("=" * 70)
print("SUMMARY: Key findings")
print("=" * 70)
print("""
Patterns tested:
  1. Main diagonal - checked
  2. Anti-diagonal - checked
  3. All diagonals - checked
  4. Spiral read - checked
  5. Snake/boustrophedon - checked
  6. Column reads - checked
  7. First letters of entries - checked
  8. Last letters of entries - checked
  9. Middle letters of entries - checked
  10. Nth letter extraction - checked
  11. Border cells (adj to black) - checked
  12. Word search (all directions) - checked
  13. Circled cells (multiple orderings) - checked

  Bonus A: Central row/column - checked
  Bonus C: Every Nth cell - checked
  Bonus D: Entries by length - checked
  Bonus E: Column 13 (ROTUNDA) - checked
""")

print("Done! Review output above for any promising patterns.")
