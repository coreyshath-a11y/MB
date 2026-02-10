#!/usr/bin/env python3
"""
Calendar Dates → Entry Numbers Theory

The 11 circled dates from Mrs. Maybelle's calendar map to entry numbers.
This script investigates how these entries connect to the staircase grid
and theme entries with hidden location names.
"""

# Calendar dates → entry numbers (month × 10 + day)
CALENDAR_ENTRIES = [
    (1, "Jan 1",  11,  'D', 0,  12, 7),   # 11D at (0,12), len 7, col 12
    (2, "Feb 2",  22,  'A', 1,  0,  7),   # 22A at (1,0), len 7
    (3, "Mar 1",  31,  'A', 3,  11, 3),   # 31A at (3,11), len 3
    (4, "Mar 3",  33,  'D', 3,  16, 3),   # 33D at (3,16), len 3
    (5, "Jun 1",  61,  'A', 7,  18, 6),   # 61A at (7,18), len 6
    (6, "Jul 1",  71,  'D', 8,  24, 6),   # 71D at (8,24), len 6
    (7, "Aug 1",  81,  'A', 10, 17, 4),   # 81A at (10,17), len 4
    (8, "Aug 6",  86,  'D', 11, 8,  3),   # 86D at (11,8), len 3 = ZIP
    (9, "Sep 1",  91,  'A', 11, 22, 3),   # 91A at (11,22), len 3
    (10, "Nov 5", 115, 'D', 15, 3,  5),   # 115D at (15,3), len 5
    (11, "Dec 7", 127, 'A', 17, 1,  6),   # 127A at (17,1), len 6
]

# Staircase row data
STAIRCASE = [
    (1, 4, "AROUNDWORLD"[0]),  # Row 1: 4 letters, need col4 = A
    (2, 6, "AROUNDWORLD"[1]),  # Row 2: 6 letters, need col4 = R
    (3, 5, "AROUNDWORLD"[2]),  # Row 3: 5 letters, need col4 = O
    (4, 5, "AROUNDWORLD"[3]),  # Row 4: 5 letters, need col4 = U
    (5, 4, "AROUNDWORLD"[4]),  # Row 5: 4 letters, need col4 = N
    (6, 4, "AROUNDWORLD"[5]),  # Row 6: 4 letters, need col4 = D
    (7, 5, "AROUNDWORLD"[6]),  # Row 7: 5 letters, need col4 = W
    (8, 3, "AROUNDWORLD"[7]),  # Row 8: 3 letters, need col4 = O
    (9, 5, "AROUNDWORLD"[8]),  # Row 9: 5 letters, need col4 = R
    (10, 5, "AROUNDWORLD"[9]), # Row 10: 5 letters, need col4 = L
    (11, 4, "AROUNDWORLD"[10]),# Row 11: 4 letters, need col4 = D
]

# Theme entries
THEME_ENTRIES = {
    '25A':  (2,  0,  'A', 16),
    '50A':  (6,  0,  'A', 16),
    '73A':  (9,  11, 'A', 14),
    '94A':  (12, 7,  'A', 11),
    '114A': (15, 0,  'A', 14),
    '138A': (18, 9,  'A', 16),
    '167A': (22, 9,  'A', 16),
    '19D':  (0,  22, 'D', 15),
    '78D':  (10, 2,  'D', 15),
}

# ============================================================
# Theory 1: Calendar entries CROSS theme entries
# ============================================================
print("=" * 70)
print("THEORY 1: Calendar entries cross theme entries at location positions")
print("=" * 70)

for idx, date, entry_num, d, r, c, length in CALENDAR_ENTRIES:
    print(f"\n  #{idx} ({date}) → Entry {entry_num}{d} at ({r},{c}) len={length}")

    # Check which theme entries this entry crosses
    for i in range(length):
        if d == 'A':
            cell_r, cell_c = r, c + i
        else:
            cell_r, cell_c = r + i, c

        for theme_name, (tr, tc, td, tl) in THEME_ENTRIES.items():
            if td == 'A':
                if cell_r == tr and tc <= cell_c < tc + tl:
                    theme_pos = cell_c - tc
                    print(f"    pos {i}: ({cell_r},{cell_c}) crosses {theme_name}[{theme_pos}]")
            else:
                if cell_c == tc and tr <= cell_r < tr + tl:
                    theme_pos = cell_r - tr
                    print(f"    pos {i}: ({cell_r},{cell_c}) crosses {theme_name}[{theme_pos}]")

# ============================================================
# Theory 2: The DAY extracts a specific letter from the entry
# ============================================================
print("\n" + "=" * 70)
print("THEORY 2: Day number = position to extract from entry answer")
print("=" * 70)

for idx, date, entry_num, d, r, c, length in CALENDAR_ENTRIES:
    day = int(date.split()[-1])
    # Check both 0-indexed and 1-indexed
    staircase_row, staircase_len, target_letter = STAIRCASE[idx-1]

    print(f"\n  #{idx} ({date}) → Entry {entry_num}{d} (len={length})")
    print(f"    Day={day} → position {day} (1-indexed) or {day-1} (0-indexed)")
    if day <= length:
        print(f"    In range (1-indexed): extract position {day}")
    else:
        print(f"    OUT OF RANGE (1-indexed)!")
    if day - 1 < length:
        print(f"    In range (0-indexed): extract position {day-1}")
    else:
        print(f"    OUT OF RANGE (0-indexed)!")
    print(f"    Staircase Row {staircase_row}: needs {staircase_len}-letter location with '{target_letter}' at spine")

# ============================================================
# Theory 3: Calendar entries are clue numbers for staircase words
# ============================================================
print("\n" + "=" * 70)
print("THEORY 3: The entry ANSWER is the staircase word (or contains it)")
print("=" * 70)

# The staircase has specific word lengths. Let's check if any calendar entry
# has the same length as its corresponding staircase row.
print("\nLength comparison:")
for idx, date, entry_num, d, r, c, length in CALENDAR_ENTRIES:
    staircase_row, staircase_len, target_letter = STAIRCASE[idx-1]
    match = "✓ MATCH" if length == staircase_len else "✗ mismatch"
    print(f"  #{idx}: Entry {entry_num}{d} len={length}, Staircase row {staircase_row} len={staircase_len} → {match}")

# ============================================================
# Theory 4: Entry number itself encodes something
# ============================================================
print("\n" + "=" * 70)
print("THEORY 4: Entry numbers as grid coordinates")
print("=" * 70)

# Entry numbers: 11, 22, 31, 33, 61, 71, 81, 86, 91, 115, 127
# Could these be grid coordinates? Like (1,1), (2,2), (3,1), (3,3), (6,1), (7,1), (8,1), (8,6), (9,1), (11,5), (12,7)?
print("As (row, col) coordinates (1-indexed):")
for idx, date, entry_num, d, r, c, length in CALENDAR_ENTRIES:
    if entry_num < 100:
        row_guess = entry_num // 10
        col_guess = entry_num % 10
        print(f"  #{idx}: {entry_num} → ({row_guess},{col_guess}) = grid[{row_guess}][{col_guess}]")
    else:
        # 3 digits: could be (row, col) with row as first 1-2 digits
        row_guess1 = entry_num // 10
        col_guess1 = entry_num % 10
        row_guess2 = entry_num // 100
        col_guess2 = entry_num % 100
        print(f"  #{idx}: {entry_num} → ({row_guess1},{col_guess1}) or ({row_guess2},{col_guess2})")

# ============================================================
# Theory 5: Each calendar entry provides a letter for extraction
# ============================================================
print("\n" + "=" * 70)
print("THEORY 5: Calendar entries → letters → staircase or extraction code")
print("=" * 70)

# The key insight: We know entry 86D = ZIP.
# Calendar date 8 = Aug 6 → entry 86D
# Staircase row 8 = 3-letter word, col4 letter = O
# ZIP has O at... nowhere. ZIP = Z, I, P. No O.
# But GOA (a candidate for row 8) = G, O, A. O is at position 1.
# And the staircase needs word[1] = O for column 4.

# So the calendar entry ISN'T the staircase word. The calendar entry is a
# CROSSWORD entry that provides information ABOUT the staircase word.

# Maybe the day tells us which letter of the crossword entry answer to read?
# Aug 6 → entry 86 → read letter 6... but ZIP only has 3 letters.
# Unless it's the MONTH number? Month 8 → letter 8? Still too big.

# Or maybe the entry's answer CONTAINS the location name:
# Entry 86D = ZIP. Does ZIP contain GOA? No.
# Does the crossword entry for 86D help us find GOA somehow?

# What if the calendar date tells us WHERE in a theme entry to look?
# Aug 6 → look at position 6 of some theme entry?

# Let me try: for each calendar entry, which theme entry does it cross?
# If it crosses a theme entry at a specific position, that position might
# be where the location starts.

print("\nCalendar entry → theme entry crossing positions:")
for idx, date, entry_num, d, r, c, length in CALENDAR_ENTRIES:
    crossings = []
    for i in range(length):
        if d == 'A':
            cell_r, cell_c = r, c + i
        else:
            cell_r, cell_c = r + i, c

        for theme_name, (tr, tc, td, tl) in THEME_ENTRIES.items():
            if td == 'A':
                if cell_r == tr and tc <= cell_c < tc + tl:
                    theme_pos = cell_c - tc
                    crossings.append((theme_name, theme_pos, i))
            else:
                if cell_c == tc and tr <= cell_r < tr + tl:
                    theme_pos = cell_r - tr
                    crossings.append((theme_name, theme_pos, i))

    if crossings:
        staircase_row, staircase_len, target_letter = STAIRCASE[idx-1]
        print(f"\n  #{idx} ({date}) → {entry_num}{d}: Staircase location = {staircase_len}-letter word")
        for theme_name, theme_pos, entry_pos in crossings:
            print(f"    Crosses {theme_name}[{theme_pos}] at entry position {entry_pos}")
    else:
        print(f"\n  #{idx} ({date}) → {entry_num}{d}: NO theme entry crossings!")

# ============================================================
# Theory 6: Circled cells connection
# ============================================================
print("\n" + "=" * 70)
print("THEORY 6: Calendar dates and circled cells")
print("=" * 70)

CIRCLED = [
    (0, 12), (2, 4), (3, 8), (3, 24), (4, 19),
    (10, 12), (11, 2), (11, 22), (13, 0), (18, 7),
    (19, 17), (20, 2), (22, 11), (22, 18), (22, 24), (24, 20),
]

# Check if any calendar entries start at or contain circled cells
for idx, date, entry_num, d, r, c, length in CALENDAR_ENTRIES:
    circles_in_entry = []
    for i in range(length):
        if d == 'A':
            cell = (r, c + i)
        else:
            cell = (r + i, c)
        if cell in CIRCLED:
            circles_in_entry.append((cell, i))

    if circles_in_entry:
        print(f"  #{idx} ({date}) → {entry_num}{d}: Contains circled cells: {circles_in_entry}")
    else:
        print(f"  #{idx} ({date}) → {entry_num}{d}: No circled cells")

# Special: entry 11D starts at the first circled cell (0,12)!
print("\nNOTE: Entry 11D starts at circled cell (0,12) — first circled cell in the grid!")
print("NOTE: Entry 86D starts at (11,8) — cell 86 is NOT circled")
print("NOTE: Entry 91A starts at (11,22) — circled cell!")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("SUMMARY: WHICH THEORIES ARE VIABLE?")
print("=" * 70)

print("""
Theory 1 (entries cross theme entries):
  - 11D crosses 25A at pos 12
  - 31A crosses 25A at pos 11-13 (short, 3 letters)
  - 81A crosses 73A at pos 6-9 (short, 4 letters)
  - 115D crosses 114A at pos 3-7
  - Most calendar entries DO cross at least one theme entry!

Theory 2 (day = position to extract):
  - Aug 6 → position 6, but entry 86D has only 3 letters → OUT OF RANGE
  - Dec 7 → position 7, but entry 127A has only 6 letters → OUT OF RANGE
  - FAILS for entries 8 and 11

Theory 3 (entry answer = staircase word):
  - Only 2 length matches: #7 (81A len=4, staircase=5 NOPE) and #9 (91A len=3, staircase=5 NOPE)
  - Actually ZERO matches! FAILS completely.

Theory 4 (entry numbers as coordinates):
  - Some numbers like 86 → (8,6) or 115 → (11,5) look plausible
  - But 127 → (12,7) which IS the start of 94A = CIRCLEABOUT!
  - Also 86 → (8,6)... let me check what's there...

Theory 5 (entry answers contain location):
  - 86D = ZIP. Does it relate to GOA? Not obviously.
  - Need to fill more entries to test.

Theory 6 (circled cells):
  - 11D starts at first circled cell
  - 91A starts at a circled cell
  - 86D does NOT contain a circled cell
  - Mixed results.

MOST PROMISING: Theory 1 + Theory 4 (entry numbers as grid coordinates)
  Let me check Theory 4 more carefully...
""")

# Check Theory 4: entry numbers as (row, col) coordinates
print("Theory 4 detailed: Entry number digits as grid coordinates")
print("Read the letter at that grid position to get... something?")
for idx, date, entry_num, d, r, c, length in CALENDAR_ENTRIES:
    if entry_num < 100:
        coord_r = entry_num // 10
        coord_c = entry_num % 10
    else:
        coord_r = entry_num // 10
        coord_c = entry_num % 10

    # Check if coordinate is valid
    if 0 <= coord_r < 25 and 0 <= coord_c < 25:
        is_black = (coord_r, coord_c) in {(0,7),(0,8),(0,15),(0,16),(1,7),(1,15),(1,16),(2,16),
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
            (23,8),(23,9),(23,17),(24,8),(24,9),(24,16),(24,17)}
        status = "BLACK" if is_black else "white"
        is_circ = (coord_r, coord_c) in CIRCLED
        circ = " ⊙ CIRCLED!" if is_circ else ""
        print(f"  #{idx}: {entry_num} → ({coord_r},{coord_c}) = {status}{circ}")
    else:
        print(f"  #{idx}: {entry_num} → ({coord_r},{coord_c}) = OUT OF BOUNDS")

# One more: what if 127 → (12,7) which is the START of 94A = CIRCLEABOUT?
print("\nINTERESTING: 127 → (12,7) = start of 94A = CIRCLEABOUT")
print("And 115 → (11,5) which is a BLACK cell")
print("And 86 → (8,6) which is a white cell")
