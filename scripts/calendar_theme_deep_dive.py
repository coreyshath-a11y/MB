#!/usr/bin/env python3
"""
Deep analysis of how calendar dates connect to theme entries in the MrBeast puzzle.

KEY DISCOVERY: 7 of 11 calendar dates correspond to entries that CROSS theme entries.
The crossing positions in theme entries may reveal where hidden location names are.
"""

print("=" * 80)
print("CALENDAR-THEME CROSSING DEEP DIVE ANALYSIS")
print("=" * 80)

# =============================================================================
# DATA SETUP
# =============================================================================

calendar_entries = [
    # (date_label, entry_num, entry_type, row, col, length, theme_crossings)
    # theme_crossings: list of (theme_entry, position_in_theme, position_in_calendar_entry)
    ("Jan 1",  11,  "D", 0,  12, 7, [("25A", 12, 2), ("50A", 12, 6)]),
    ("Feb 2",  22,  "A", 1,  0,  7, []),
    ("Mar 1",  31,  "A", 3,  11, 3, []),
    ("Mar 3",  33,  "D", 3,  16, 3, []),
    ("Jun 1",  61,  "A", 7,  18, 6, [("19D", 7, 7)]),
    ("Jul 1",  71,  "D", 8,  24, 6, [("73A", 13, 1)]),
    ("Aug 1",  81,  "A", 10, 17, 4, []),
    ("Aug 6",  86,  "D", 11, 8,  3, [("94A", 1, 0)]),
    ("Sep 1",  91,  "A", 11, 22, 3, [("19D", 11, 0)]),
    ("Nov 5", 115,  "D", 15, 3,  5, [("114A", 3, 0)]),
    ("Dec 7", 127,  "A", 17, 1,  6, [("78D", 7, 0)]),
]

theme_entries = {
    '25A':  {'row': 2,  'col': 0,  'len': 16, 'fill': '................', 'known': {}},
    '50A':  {'row': 6,  'col': 0,  'len': 16, 'fill': '..........A..R..', 'known': {10: 'A', 13: 'R'}},
    '73A':  {'row': 9,  'col': 11, 'len': 14, 'fill': '..U...........', 'known': {2: 'U'}},
    '94A':  {'row': 12, 'col': 7,  'len': 11, 'fill': 'CIRCLEABOUT', 'known': 'all'},
    '114A': {'row': 15, 'col': 0,  'len': 14, 'fill': '.........E...E', 'known': {9: 'E', 13: 'E'}},
    '138A': {'row': 18, 'col': 9,  'len': 16, 'fill': '....E...........', 'known': {4: 'E'}},
    '167A': {'row': 22, 'col': 9,  'len': 16, 'fill': 'SUPERBOWLSTADIUM', 'known': 'all'},
    '19D':  {'row': 0,  'col': 22, 'len': 15, 'fill': '...............', 'known': {}},
    '78D':  {'row': 10, 'col': 2,  'len': 15, 'fill': '...............', 'known': {}},
}

# Staircase grid: 11 rows, 9 columns
# Column 4 spine = AROUNDWORLD
staircase_lengths = [4, 6, 5, 5, 4, 4, 5, 3, 5, 5, 4]
aroundworld = "AROUNDWORLD"
assert len(aroundworld) == 11

# AROUNDWORLD theory locations (best fit)
aroundworld_locations = [
    "MALI", "TEHRAN", "LAGOS", "SUDAN", "OMAN",
    "ADEN", "WALES", "GOA", "NIGER", "DELHI", "CHAD"
]

# MELANESIANS alternative
melanesians_locations = [
    "OMAN", "GREECE", "ITALY", "JAPAN", "IRAN",
    "PERU", "SPAIN", "CIV", "GHANA", "KENYA", "LAOS"
]

# Calendar-to-staircase row mapping (1-indexed)
calendar_to_staircase = {
    11: 1, 22: 2, 31: 3, 33: 4, 61: 5,
    71: 6, 81: 7, 86: 8, 91: 9, 115: 10, 127: 11
}

print()
print("=" * 80)
print("SECTION 1: BASIC CROSSING DATA")
print("=" * 80)
print()

for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]
    spine_letter = aroundworld[stair_row - 1]
    aw_loc = aroundworld_locations[stair_row - 1]

    print(f"  {date} -> {num}{etype} (len={length}) | Staircase row {stair_row}: "
          f"{stair_len}-letter location, spine='{spine_letter}', candidate={aw_loc}")
    if crossings:
        for theme, theme_pos, cal_pos in crossings:
            te = theme_entries[theme]
            chars_left = te['len'] - theme_pos
            known_at = te['fill'][theme_pos] if theme_pos < len(te['fill']) else '?'
            print(f"    -> Crosses {theme} at theme-position {theme_pos} "
                  f"(0-indexed), cal-position {cal_pos}")
            print(f"       {theme} length={te['len']}, chars remaining from pos {theme_pos}: {chars_left}")
            print(f"       Known letter at theme-pos {theme_pos}: '{known_at}'")
    else:
        print(f"    -> NO theme crossings")
    print()


# =============================================================================
# THEORY A: Crossing position = START of hidden location in theme entry
# =============================================================================

print("=" * 80)
print("THEORY A: Crossing position = START of hidden location")
print("=" * 80)
print()
print("If the calendar entry crosses a theme entry at position P, the hidden")
print("location name in that theme entry STARTS at position P.")
print()

header = f"{'Stair Row':>9} | {'Calendar':>8} | {'Theme@Pos':>10} | {'Theme Len':>9} | {'Stair Len':>9} | {'Chars Left':>10} | {'Fits?':>5} | {'Location (AW)':>14}"
print(header)
print("-" * len(header))

theory_a_results = []
for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]
    aw_loc = aroundworld_locations[stair_row - 1]

    if crossings:
        for theme, theme_pos, cal_pos in crossings:
            te = theme_entries[theme]
            chars_left = te['len'] - theme_pos
            fits = chars_left >= stair_len
            end_pos = theme_pos + stair_len - 1
            fits_exact = (chars_left == stair_len)

            result = {
                'stair_row': stair_row, 'date': date, 'num': num, 'etype': etype,
                'theme': theme, 'theme_pos': theme_pos, 'theme_len': te['len'],
                'stair_len': stair_len, 'chars_left': chars_left,
                'fits': fits, 'fits_exact': fits_exact, 'aw_loc': aw_loc,
                'end_pos': end_pos
            }
            theory_a_results.append(result)

            marker = "EXACT!" if fits_exact else ("YES" if fits else "NO!")
            print(f"{stair_row:>9} | {date:>8} | {theme}@{theme_pos:<4} | {te['len']:>9} | "
                  f"{stair_len:>9} | {chars_left:>10} | {marker:>5} | {aw_loc:>14}")
    else:
        print(f"{stair_row:>9} | {date:>8} | {'(none)':>10} | {'---':>9} | "
              f"{stair_len:>9} | {'---':>10} | {'N/A':>5} | {aw_loc:>14}")

print()
print("THEORY A ANALYSIS:")
fits_count = sum(1 for r in theory_a_results if r['fits'])
exact_count = sum(1 for r in theory_a_results if r['fits_exact'])
no_fit = [r for r in theory_a_results if not r['fits']]
print(f"  Total crossings: {len(theory_a_results)}")
print(f"  Fits (room for location): {fits_count}")
print(f"  Exact fit (location ends at theme entry end): {exact_count}")
print(f"  Does NOT fit: {len(no_fit)}")
for r in no_fit:
    print(f"    -> Row {r['stair_row']}: {r['theme']}@{r['theme_pos']}, "
          f"need {r['stair_len']} letters but only {r['chars_left']} remaining")

# Check exact fits more carefully
print()
print("  EXACT FITS (location fills to end of theme entry):")
for r in theory_a_results:
    if r['fits_exact']:
        print(f"    -> Row {r['stair_row']}: {r['aw_loc']} in {r['theme']} "
              f"positions [{r['theme_pos']}..{r['end_pos']}] (end of entry)")

print()
print("  KEY OBSERVATION: Rows 6 (71D->73A@13) and 9 (91A->19D@11) DON'T FIT")
print("  as start positions. Row 6 needs 4 letters but only 1 char left at pos 13.")
print("  Row 9 needs 5 letters but only 4 chars left at pos 11.")

# =============================================================================
# THEORY A-variant: Crossing position = END of hidden location
# =============================================================================

print()
print("=" * 80)
print("THEORY A-VARIANT: Crossing position = END of hidden location")
print("=" * 80)
print()
print("If the calendar entry crosses a theme entry at position P, the hidden")
print("location name in that theme entry ENDS at position P.")
print()

header = f"{'Stair Row':>9} | {'Calendar':>8} | {'Theme@Pos':>10} | {'Start Pos':>9} | {'Stair Len':>9} | {'Fits?':>5} | {'Location (AW)':>14} | Range"
print(header)
print("-" * len(header))

theory_a_end_results = []
for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]
    aw_loc = aroundworld_locations[stair_row - 1]

    if crossings:
        for theme, theme_pos, cal_pos in crossings:
            te = theme_entries[theme]
            start_pos = theme_pos - stair_len + 1
            fits = start_pos >= 0

            result = {
                'stair_row': stair_row, 'theme': theme, 'theme_pos': theme_pos,
                'start_pos': start_pos, 'stair_len': stair_len, 'fits': fits,
                'aw_loc': aw_loc, 'date': date
            }
            theory_a_end_results.append(result)

            marker = "YES" if fits else "NO!"
            range_str = f"[{start_pos}..{theme_pos}]" if fits else f"[{start_pos}..{theme_pos}] OOB"
            print(f"{stair_row:>9} | {date:>8} | {theme}@{theme_pos:<4} | {start_pos:>9} | "
                  f"{stair_len:>9} | {marker:>5} | {aw_loc:>14} | {range_str}")
    else:
        print(f"{stair_row:>9} | {date:>8} | {'(none)':>10} | {'---':>9} | "
              f"{stair_len:>9} | {'N/A':>5} | {aw_loc:>14} |")

print()
no_fit_end = [r for r in theory_a_end_results if not r['fits']]
all_fit_end = all(r['fits'] for r in theory_a_end_results)
print(f"  ALL FIT as end positions? {'YES!' if all_fit_end else 'NO'}")
if no_fit_end:
    for r in no_fit_end:
        print(f"    -> Row {r['stair_row']}: would need start at {r['start_pos']} (negative = out of bounds)")


# =============================================================================
# THEORY A-variant2: Crossing position = CONTAINS (location spans across it)
# =============================================================================

print()
print("=" * 80)
print("THEORY A-VARIANT2: Crossing position is WITHIN the hidden location")
print("=" * 80)
print()
print("The crossing position falls somewhere within the hidden location.")
print("For each crossing, enumerate all valid placements of the location")
print("that include the crossing position.")
print()

for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]
    aw_loc = aroundworld_locations[stair_row - 1]
    spine_letter = aroundworld[stair_row - 1]

    if not crossings:
        continue

    for theme, theme_pos, cal_pos in crossings:
        te = theme_entries[theme]
        print(f"  Row {stair_row} ({aw_loc}, len={stair_len}): {num}{etype} crosses {theme}@{theme_pos}")
        print(f"    Theme {theme} has length {te['len']}")
        print(f"    Valid placements where location spans position {theme_pos}:")

        valid_starts = []
        for s in range(max(0, theme_pos - stair_len + 1), min(theme_pos + 1, te['len'] - stair_len + 1)):
            e = s + stair_len - 1
            if e < te['len']:
                offset_in_loc = theme_pos - s  # which letter of the location is at theme_pos

                # Check known letters
                conflict = False
                known_matches = []
                for pos_in_loc in range(stair_len):
                    theme_p = s + pos_in_loc
                    if te['known'] != 'all' and theme_p in te['known']:
                        known_letter = te['known'][theme_p]
                        known_matches.append((pos_in_loc, theme_p, known_letter))
                    elif te['known'] == 'all':
                        known_letter = te['fill'][theme_p]
                        known_matches.append((pos_in_loc, theme_p, known_letter))

                # For AROUNDWORLD: check if spine letter matches
                # Location's position 3 (0-indexed, column 4) = spine_letter
                spine_pos = 3  # column 4 in staircase (0-indexed)
                spine_check = ""
                if spine_pos < stair_len:
                    # The letter at position spine_pos in the location should be spine_letter
                    theme_p_for_spine = s + spine_pos
                    if te['known'] == 'all':
                        actual = te['fill'][theme_p_for_spine]
                        spine_check = f" [spine: loc[{spine_pos}]='{spine_letter}', theme[{theme_p_for_spine}]='{actual}' {'MATCH' if actual == spine_letter else 'MISMATCH'}]"
                    else:
                        spine_check = f" [spine: loc[{spine_pos}] should be '{spine_letter}']"

                valid_starts.append(s)
                loc_in_crossing = f"loc[{offset_in_loc}]"
                known_str = ""
                if known_matches:
                    km = ", ".join(f"loc[{p}]=theme[{tp}]='{l}'" for p, tp, l in known_matches)
                    known_str = f" | Known: {km}"
                print(f"      Start={s}, End={e}, crossing hits {loc_in_crossing}{spine_check}{known_str}")

        if not valid_starts:
            print(f"      ** NO VALID PLACEMENTS **")
        print()


# =============================================================================
# THEORY B: Crossing position = specific letter to extract
# =============================================================================

print("=" * 80)
print("THEORY B: Crossing position = letter extraction")
print("=" * 80)
print()
print("The letter at the crossing point in the theme entry is extracted.")
print("This letter goes into the staircase grid at a specific position.")
print()

for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]
    aw_loc = aroundworld_locations[stair_row - 1]
    spine_letter = aroundworld[stair_row - 1]

    if not crossings:
        print(f"  Row {stair_row} ({aw_loc}): {date} -> {num}{etype} — no crossing, no letter extracted")
        continue

    for theme, theme_pos, cal_pos in crossings:
        te = theme_entries[theme]
        if te['known'] == 'all':
            letter = te['fill'][theme_pos]
            print(f"  Row {stair_row} ({aw_loc}): {date} -> {num}{etype} crosses {theme}@{theme_pos} "
                  f"-> letter '{letter}' (from {te['fill']})")
            # Check: does this letter appear in the candidate location?
            if letter in aw_loc:
                positions = [i for i, c in enumerate(aw_loc) if c == letter]
                print(f"    '{letter}' appears in {aw_loc} at position(s) {positions}")
            else:
                print(f"    '{letter}' does NOT appear in {aw_loc}")
        elif isinstance(te['known'], dict) and theme_pos in te['known']:
            letter = te['known'][theme_pos]
            print(f"  Row {stair_row} ({aw_loc}): {date} -> {num}{etype} crosses {theme}@{theme_pos} "
                  f"-> letter '{letter}' (known)")
        else:
            fill_char = te['fill'][theme_pos] if theme_pos < len(te['fill']) else '?'
            print(f"  Row {stair_row} ({aw_loc}): {date} -> {num}{etype} crosses {theme}@{theme_pos} "
                  f"-> letter UNKNOWN (fill='{fill_char}')")

print()
print("  THEORY B INSIGHT: Only 94A is fully known. 86D crosses 94A@1 -> 'I'.")
print("  For AROUNDWORLD row 8 (GOA), spine letter should be 'O' at position 3.")
print("  But GOA only has 3 letters, so position 3 doesn't exist in GOA!")
print("  Wait - staircase is 9 columns wide, GOA occupies columns 1-3 (or some offset).")
print("  With AROUNDWORLD spine at column 4, GOA (3 letters) might be at columns 2-4,")
print("  making column 4 = GOA[2] = 'A'. But AROUNDWORLD[7] = 'O', not 'A'. CONFLICT!")
print("  Unless GOA is at columns 4-6, making column 4 = GOA[0] = 'G'. Still not 'O'.")


# =============================================================================
# THEORY C: Calendar entry's ANSWER contains the location name
# =============================================================================

print()
print("=" * 80)
print("THEORY C: Calendar entry answers contain location names")
print("=" * 80)
print()

# Known/suspected answers for calendar entries
known_calendar_answers = {
    86: ("ZIP", 3, "confirmed from solver"),
    # Others unknown
}

print("Calendar entry lengths vs staircase location lengths:")
print()
for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]
    aw_loc = aroundworld_locations[stair_row - 1]

    answer_info = known_calendar_answers.get(num, (None, None, None))
    answer_str = f" [ANSWER: {answer_info[0]}]" if answer_info[0] else ""

    can_contain = length >= stair_len
    print(f"  Row {stair_row}: {date} -> {num}{etype} (len={length}){answer_str} "
          f"vs staircase len={stair_len} -> {'CAN contain' if can_contain else 'TOO SHORT!'}")

    if answer_info[0]:
        ans = answer_info[0]
        # Check if location is hidden in answer
        if aw_loc in ans:
            print(f"    -> {aw_loc} IS in {ans}!")
        else:
            print(f"    -> {aw_loc} is NOT in {ans}")
            # Check partial
            for i in range(len(ans)):
                for j in range(i+1, len(ans)+1):
                    sub = ans[i:j]
                    if len(sub) >= 2 and sub in aw_loc:
                        pass  # too noisy

print()
print("  NOTE: 86D='ZIP' (3 letters) for staircase row 8 (3-letter location).")
print("  ZIP does not contain GOA, OMAN, or any obvious location name.")
print("  But the entry LENGTH matches the staircase length perfectly!")
print()

# Check: do ALL calendar entry lengths match staircase lengths?
print("  Length match check (calendar entry length == staircase location length?):")
match_count = 0
for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]
    match = length == stair_len
    if match:
        match_count += 1
    print(f"    Row {stair_row}: {num}{etype} len={length}, staircase len={stair_len} -> {'MATCH!' if match else 'no match'}")

print(f"\n  Matches: {match_count}/11")


# =============================================================================
# THEORY D: Non-crossing entries work differently
# =============================================================================

print()
print("=" * 80)
print("THEORY D: The 4 non-crossing calendar entries")
print("=" * 80)
print()

crossing_rows = []
non_crossing_rows = []

for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]
    aw_loc = aroundworld_locations[stair_row - 1]

    if crossings:
        crossing_rows.append((stair_row, date, num, etype, length, stair_len, aw_loc, crossings))
    else:
        non_crossing_rows.append((stair_row, date, num, etype, length, stair_len, aw_loc))

print("NON-CROSSING calendar entries (no theme entry interaction):")
for stair_row, date, num, etype, length, stair_len, aw_loc in non_crossing_rows:
    print(f"  Row {stair_row}: {date} -> {num}{etype} (len={length}), location={aw_loc} (len={stair_len})")

print()
print("CROSSING calendar entries:")
for stair_row, date, num, etype, length, stair_len, aw_loc, crossings in crossing_rows:
    cross_str = ", ".join(f"{t}@{p}" for t, p, _ in crossings)
    print(f"  Row {stair_row}: {date} -> {num}{etype} (len={length}), location={aw_loc} (len={stair_len}), crosses {cross_str}")

print()
print("Pattern analysis:")
print(f"  Non-crossing rows: {[r[0] for r in non_crossing_rows]} = staircase rows 2,3,4,7")
print(f"  Crossing rows: {[r[0] for r in crossing_rows]} = staircase rows 1,5,6,8,9,10,11")
print()
print("  Non-crossing staircase lengths: {}")
for r in non_crossing_rows:
    print(f"    Row {r[0]}: location length {r[5]}, entry length {r[4]}")
print()
print("  Are non-crossing entries' lengths == staircase lengths?")
nc_match = all(r[4] == r[5] for r in non_crossing_rows)
print(f"    {nc_match} -> ", end="")
if nc_match:
    print("YES! All non-crossing entry lengths match staircase location lengths!")
else:
    for r in non_crossing_rows:
        if r[4] != r[5]:
            print(f"\n    Row {r[0]}: entry len {r[4]} != staircase len {r[5]}")


# =============================================================================
# THEORY E: Build staircase using crossing positions + AROUNDWORLD
# =============================================================================

print()
print("=" * 80)
print("THEORY E: Mapping crossings to staircase construction")
print("=" * 80)
print()

print("AROUNDWORLD spine (column index 3, 0-based):")
for i, letter in enumerate(aroundworld):
    loc = aroundworld_locations[i]
    loc_len = staircase_lengths[i]
    # In the staircase, each location is placed so that its letter at some
    # position equals the spine letter. With spine at column 3 (0-indexed),
    # the location occupies columns (3-offset) to (3-offset+len-1).
    # The offset is the position within the location word of the spine letter.

    if letter in loc:
        spine_positions = [j for j, c in enumerate(loc) if c == letter]
        for sp in spine_positions:
            start_col = 3 - sp  # 0-indexed column where location starts
            end_col = start_col + loc_len - 1
            in_grid = 0 <= start_col and end_col <= 8
            print(f"  Row {i+1}: {loc} (len={loc_len}), spine '{letter}' at loc[{sp}], "
                  f"cols [{start_col}..{end_col}] {'IN GRID' if in_grid else 'OUT OF GRID!'}")
    else:
        print(f"  Row {i+1}: {loc} (len={loc_len}), spine '{letter}' NOT IN LOCATION! PROBLEM!")

print()
print("  NOTE: Several AROUNDWORLD locations don't contain the required spine letter!")
print("  This suggests the staircase alignment might not require the location name")
print("  itself to pass through column 4, but rather the THEME ENTRY answer does.")
print("  Or the staircase works differently than assumed.")


# =============================================================================
# CROSS-THEORY ANALYSIS: Position relationships
# =============================================================================

print()
print("=" * 80)
print("CROSS-THEORY ANALYSIS: Numeric relationships in crossing positions")
print("=" * 80)
print()

print("For each crossing, examine the numeric relationships:")
print()
print(f"{'Row':>3} | {'Date':>6} | {'Entry':>5} | {'Theme':>5} | {'ThPos':>5} | {'CalPos':>6} | {'ThLen':>5} | {'StLen':>5} | ThPos+StLen | ThLen-ThPos | ThPos-StLen")
print("-" * 100)

for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]

    if crossings:
        for theme, theme_pos, cal_pos in crossings:
            te = theme_entries[theme]
            print(f"{stair_row:>3} | {date:>6} | {num}{etype:>3} | {theme:>5} | {theme_pos:>5} | "
                  f"{cal_pos:>6} | {te['len']:>5} | {stair_len:>5} | "
                  f"{theme_pos + stair_len:>11} | {te['len'] - theme_pos:>11} | {theme_pos - stair_len:>11}")

print()
print("Looking for patterns:")
print()

# Check: ThPos + StLen == ThLen?
print("  Pattern: ThemePos + StaircaseLen == ThemeLen (location ends at theme end)?")
for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]
    for theme, theme_pos, cal_pos in crossings:
        te = theme_entries[theme]
        match = (theme_pos + stair_len == te['len'])
        if match:
            print(f"    Row {stair_row}: {theme}@{theme_pos} + {stair_len} = {te['len']} -> YES!")

print()
# Check: ThPos == StLen?
print("  Pattern: ThemePos == StaircaseLen?")
for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]
    for theme, theme_pos, cal_pos in crossings:
        match = (theme_pos == stair_len)
        if match:
            print(f"    Row {stair_row}: {theme}@{theme_pos} == staircase len {stair_len} -> YES!")

print()
# Check CalPos relationships
print("  Pattern: CalendarEntryPosition in crossing == ?")
for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]
    for theme, theme_pos, cal_pos in crossings:
        print(f"    Row {stair_row}: {num}{etype}[{cal_pos}] crosses {theme}[{theme_pos}], "
              f"cal_entry_len={length}, cal_pos_from_end={length-1-cal_pos}")


# =============================================================================
# THEORY: 11D special analysis (crosses TWO theme entries)
# =============================================================================

print()
print("=" * 80)
print("SPECIAL: 11D crosses TWO theme entries (25A and 50A)")
print("=" * 80)
print()

print("11D is a 7-letter Down entry starting at row 0, col 12.")
print("It crosses 25A (row 2) at theme-position 12, and 50A (row 6) at theme-position 12.")
print("Both crossings are at the SAME column (12) in the grid!")
print()
print("11D occupies rows 0-6, column 12.")
print("  25A is at row 2, so 11D[2] = 25A[12]")
print("  50A is at row 6, so 11D[6] = 50A[12]")
print()
print("For staircase row 1 (4-letter location, candidate MALI):")
print("  If location starts at 25A[12]: location occupies 25A[12..15] = last 4 chars of 25A")
print("  If location starts at 50A[12]: location occupies 50A[12..15] = last 4 chars of 50A")
print("  50A[13] = 'R' (known). If location at 50A[12..15], then location[1] = 'R'")
print("  MALI[1] = 'A', not 'R'. So MALI doesn't work at 50A[12..15]!")
print()
print("  BUT: What 4-letter locations have 'R' at position 1 (0-indexed)?")

# Common 4-letter locations with R at position 1
import itertools
four_letter_with_r_at_1 = []
location_candidates_4 = [
    "MALI", "CHAD", "IRAN", "IRAQ", "OMAN", "PERU", "CUBA", "FIJI", "LAOS",
    "TOGO", "GUAM", "BALI", "LYON", "ROME", "OSLO", "LIMA", "DOHA", "SUVA",
    "CORK", "NICE", "ERIE", "OREL", "URAL", "ARNO", "BAKU", "GRAZ", "BRNO"
]
for loc in location_candidates_4:
    if len(loc) == 4 and loc[1] == 'R':
        four_letter_with_r_at_1.append(loc)
print(f"  4-letter locations with [1]='R': {four_letter_with_r_at_1}")
print()

# If the crossing marks the END of the location in 50A:
# location at 50A[9..12], last letter at pos 12
# 50A[10] = 'A' (known). location[1] = 'A' (since start=9, pos 10 = loc[1])
print("  If crossing marks END of location in 50A:")
print("  Location at 50A[9..12] (end at crossing)")
print("  50A[10] = 'A' (known). location[1] = 'A'")
four_letter_with_a_at_1 = [loc for loc in location_candidates_4 if len(loc) == 4 and loc[1] == 'A']
print(f"  4-letter locations with [1]='A': {four_letter_with_a_at_1}")
print()

# Check: MALI[1] = 'A' -> fits end-position theory for 50A!
print("  MALI[1] = 'A' -> FITS the end-position theory for 50A!")
print("  Location MALI at 50A[9..12]: M-A-L-I")
print("    50A[9] = M, 50A[10] = A (KNOWN 'A' -> MATCH!), 50A[11] = L, 50A[12] = I")
print()

# What about 25A?
print("  For 25A with end-position theory:")
print("  Location at 25A[9..12] (end at crossing)")
print("  MALI at 25A[9..12]: M at 25A[9], A at 25A[10], L at 25A[11], I at 25A[12]")
print("  25A has no known letters, so no conflict. But same location in two theme entries?")
print("  Probably: 11D links TWO theme entries, but the location is in ONE of them.")
print("  Most likely: location is in 25A (first theme entry 11D crosses).")

# =============================================================================
# REVISED THEORY: Crossing marks a SPECIFIC letter position in the location
# =============================================================================

print()
print("=" * 80)
print("THEORY F: Calendar-position-in-entry tells WHICH letter of location")
print("=" * 80)
print()
print("The cal_pos value (position within the calendar entry where crossing occurs)")
print("might indicate which letter of the location name to place there.")
print()

for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]
    aw_loc = aroundworld_locations[stair_row - 1]

    if crossings:
        for theme, theme_pos, cal_pos in crossings:
            te = theme_entries[theme]
            in_range = cal_pos < stair_len
            letter = aw_loc[cal_pos] if cal_pos < len(aw_loc) else '?'
            print(f"  Row {stair_row}: {num}{etype}[{cal_pos}] -> location[{cal_pos}] = "
                  f"'{letter}' (from {aw_loc}), placed at {theme}[{theme_pos}]"
                  f" {'IN RANGE' if in_range else 'OUT OF RANGE!'}")

            # Check against known theme letters
            if te['known'] == 'all':
                actual = te['fill'][theme_pos]
                match = (letter == actual)
                print(f"    Theme {theme}[{theme_pos}] = '{actual}' -> {'MATCH!' if match else 'MISMATCH!'}")
            elif isinstance(te['known'], dict) and theme_pos in te['known']:
                actual = te['known'][theme_pos]
                match = (letter == actual)
                print(f"    Theme {theme}[{theme_pos}] = '{actual}' -> {'MATCH!' if match else 'MISMATCH!'}")

print()
print("  Check: 86D[0] crosses 94A[1]. cal_pos=0.")
print("  If location[0] goes at 94A[1], then for GOA: location[0]='G', 94A[1]='I'. MISMATCH.")
print("  This theory doesn't match known data for row 8.")


# =============================================================================
# COMPREHENSIVE FIT TABLE
# =============================================================================

print()
print("=" * 80)
print("COMPREHENSIVE POSITION ANALYSIS: All possible placement interpretations")
print("=" * 80)
print()

theories = {
    'start_at': 'Location STARTS at crossing position',
    'end_at': 'Location ENDS at crossing position',
    'center': 'Crossing is at CENTER of location',
    'last_letter': 'Crossing is at LAST letter of location (same as end_at)',
}

for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]
    aw_loc = aroundworld_locations[stair_row - 1]

    if not crossings:
        continue

    for theme, theme_pos, cal_pos in crossings:
        te = theme_entries[theme]
        print(f"Row {stair_row}: {num}{etype} crosses {theme}@{theme_pos}, location={aw_loc} (len={stair_len}), theme_len={te['len']}")

        # Start at
        s = theme_pos
        e = s + stair_len - 1
        fits = e < te['len']
        known_check = []
        if fits:
            for i in range(stair_len):
                tp = s + i
                if te['known'] == 'all':
                    known_check.append((i, tp, te['fill'][tp], aw_loc[i] if i < len(aw_loc) else '?'))
                elif isinstance(te['known'], dict) and tp in te['known']:
                    known_check.append((i, tp, te['known'][tp], aw_loc[i] if i < len(aw_loc) else '?'))
        kc_str = "; ".join(f"loc[{a}]='{d}' vs theme[{b}]='{c}'" for a, b, c, d in known_check)
        conflicts_start = any(c != d for a, b, c, d in known_check)
        print(f"  START@{theme_pos}: [{s}..{e}] {'FITS' if fits else 'OUT OF BOUNDS'}"
              f"{(' | ' + kc_str) if kc_str else ''}"
              f"{' CONFLICT!' if conflicts_start else ''}")

        # End at
        e2 = theme_pos
        s2 = e2 - stair_len + 1
        fits2 = s2 >= 0
        known_check2 = []
        if fits2:
            for i in range(stair_len):
                tp = s2 + i
                if te['known'] == 'all':
                    known_check2.append((i, tp, te['fill'][tp], aw_loc[i] if i < len(aw_loc) else '?'))
                elif isinstance(te['known'], dict) and tp in te['known']:
                    known_check2.append((i, tp, te['known'][tp], aw_loc[i] if i < len(aw_loc) else '?'))
        kc_str2 = "; ".join(f"loc[{a}]='{d}' vs theme[{b}]='{c}'" for a, b, c, d in known_check2)
        conflicts_end = any(c != d for a, b, c, d in known_check2)
        print(f"  END@{theme_pos}:   [{s2}..{e2}] {'FITS' if fits2 else 'OUT OF BOUNDS'}"
              f"{(' | ' + kc_str2) if kc_str2 else ''}"
              f"{' CONFLICT!' if conflicts_end else ''}")

        print()


# =============================================================================
# DAKAR VERIFICATION at 50A
# =============================================================================

print()
print("=" * 80)
print("DAKAR VERIFICATION at 50A (previously confirmed)")
print("=" * 80)
print()

print("DAKAR at 50A positions 9-13 was previously confirmed.")
print("  50A[9]=D, 50A[10]=A(known='A' MATCH), 50A[11]=K, 50A[12]=A, 50A[13]=R(known='R' MATCH)")
print()
print("11D crosses 50A at theme-position 12.")
print("  DAKAR occupies 50A[9..13]. Position 12 is DAKAR[3]='A'.")
print("  So 11D's crossing is at the 4th letter of DAKAR in 50A.")
print()
print("If DAKAR is staircase row 1 (replacing MALI):")
print("  DAKAR has 5 letters, but staircase row 1 needs 4 letters. MISMATCH!")
print()
print("If DAKAR maps to a different staircase row:")
staircase_5_rows = [i+1 for i, l in enumerate(staircase_lengths) if l == 5]
print(f"  Staircase rows needing 5-letter locations: {staircase_5_rows}")
print("  But 11D corresponds to staircase row 1 (4-letter location).")
print()
print("RESOLUTION: DAKAR (5 letters) might be in 50A but mapped to a different")
print("staircase row, OR the calendar-staircase mapping isn't 1-to-1 as assumed.")
print("OR: DAKAR is hidden in 50A but the calendar crossing is about 25A (first crossing).")
print("11D crosses BOTH 25A@12 and 50A@12. Perhaps:")
print("  - 25A has the row-1 location (4 letters) ending/starting at position 12")
print("  - 50A has DAKAR (5 letters) at positions 9-13, independently confirmed")
print("  - These are two DIFFERENT locations in two different theme entries")


# =============================================================================
# SUMMARY AND KEY INSIGHTS
# =============================================================================

print()
print("=" * 80)
print("SUMMARY OF KEY INSIGHTS")
print("=" * 80)
print()

print("1. THEORY A (START position) FAILS for rows 6 and 9:")
print("   - Row 6: 73A@13, only 1 char left (need 4)")
print("   - Row 9: 19D@11, only 4 chars left (need 5)")
print()

print("2. THEORY A-END (END position) works for ALL crossings:")
all_end_fit = True
for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]
    stair_len = staircase_lengths[stair_row - 1]
    for theme, theme_pos, cal_pos in crossings:
        start = theme_pos - stair_len + 1
        if start < 0:
            all_end_fit = False
            print(f"   FAIL: Row {stair_row}, {theme}@{theme_pos}, start={start}")
print(f"   All end-position fits: {all_end_fit}")
print()

if all_end_fit:
    print("   END POSITION PLACEMENTS:")
    for date, num, etype, row, col, length, crossings in calendar_entries:
        stair_row = calendar_to_staircase[num]
        stair_len = staircase_lengths[stair_row - 1]
        aw_loc = aroundworld_locations[stair_row - 1]
        for theme, theme_pos, cal_pos in crossings:
            te = theme_entries[theme]
            start = theme_pos - stair_len + 1
            end = theme_pos
            # Check known letters
            conflicts = []
            matches = []
            for i in range(stair_len):
                tp = start + i
                if te['known'] == 'all':
                    actual = te['fill'][tp]
                    expected = aw_loc[i] if i < len(aw_loc) else '?'
                    if actual == expected:
                        matches.append(f"[{tp}]='{actual}'")
                    else:
                        conflicts.append(f"theme[{tp}]='{actual}' vs loc[{i}]='{expected}'")
                elif isinstance(te['known'], dict) and tp in te['known']:
                    actual = te['known'][tp]
                    expected = aw_loc[i] if i < len(aw_loc) else '?'
                    if actual == expected:
                        matches.append(f"[{tp}]='{actual}'")
                    else:
                        conflicts.append(f"theme[{tp}]='{actual}' vs loc[{i}]='{expected}'")

            status = ""
            if conflicts:
                status = f" CONFLICTS: {', '.join(conflicts)}"
            elif matches:
                status = f" MATCHES: {', '.join(matches)}"

            print(f"   Row {stair_row}: {aw_loc} at {theme}[{start}..{end}]{status}")

print()
print("3. 11D (Jan 1) is UNIQUE: crosses TWO theme entries at same column (12)")
print("   This may link 25A and 50A, or indicate the location appears in both.")
print()

print("4. NON-CROSSING entries (rows 2,3,4,7) may encode locations differently:")
print("   Their answers might BE the location names, or contain them.")
print("   Entry lengths: ", end="")
for r in non_crossing_rows:
    print(f"Row {r[0]}:{r[4]}L(need {r[5]}), ", end="")
print()
print()

print("5. 94A = CIRCLEABOUT is fully known. 86D crosses at position 1 ('I').")
print("   For end-position theory: 3-letter location ends at 94A[1].")
print("   That means location at 94A[-1..1] which is INVALID (starts before entry)!")
print("   Wait: 94A[1] with 3-letter location ending there -> 94A[-1..1]. OUT OF BOUNDS!")
print()

# Re-check Theory A (start) for 94A
print("   Re-check START theory for 94A:")
print("   Location starts at 94A[1], length 3 -> 94A[1..3] = 'IRC'")
print("   GOA vs IRC -> no match. But if a different location...")
print()

# For the end theory to work with 94A, we need start >= 0
# start = 1 - 3 + 1 = -1. NO!
# So END theory fails for row 8!

print("   ** CRITICAL: END theory FAILS for row 8 (86D->94A@1) **")
print("   Start would be at position -1. Out of bounds!")
print()

print("6. REVISED POSITION THEORY:")
print("   Neither pure START nor pure END works for ALL crossings.")
print("   The crossing position might indicate different things:")
print("   - For most: the crossing is WITHIN the location name span")
print("   - The cal_pos (position within calendar entry) might indicate")
print("     which letter of the location name is at the crossing")
print()

print("7. BEST REMAINING THEORY: The crossing simply constrains a letter")
print("   in the theme entry, and the location can be found by solving")
print("   the theme entries with all cross-constraints applied.")
print("   The calendar dates are CLUES to their respective crossword entries,")
print("   and solving those entries provides letters in theme entries.")
print()

# Final: what letters do we get from crossing 94A (the only fully known theme)?
print("8. FROM 94A (CIRCLEABOUT):")
print("   86D crosses at 94A[1] = 'I'")
print("   This means 86D's first letter (cal_pos=0) = 'I'")
print("   But we said 86D = ZIP... ZIP[0] = 'Z', not 'I'. CONTRADICTION!")
print("   Either 86D != ZIP, or the crossing data needs review.")
print()

print("=" * 80)
print("CRITICAL CONTRADICTIONS TO RESOLVE")
print("=" * 80)
print()
print("A) 86D is said to be ZIP (3 letters) but crosses 94A[1]='I'.")
print("   If 86D starts at row 11, col 8, going down for 3 cells:")
print("   86D occupies (11,8), (12,8), (13,8).")
print("   94A starts at row 12, col 7, length 11.")
print("   94A occupies (12,7) through (12,17).")
print("   Crossing at (12,8) = 94A position 8-7=1. YES, 94A[1]='I'.")
print("   86D[1] (second letter) = 'I'. So 86D = ?I?")
print("   ZIP has Z-I-P -> 86D[1]='I'. MATCH! The cal_pos in our data is 0,")
print("   but actually 86D occupies 3 rows. Let me recalculate:")
print("   86D starts at (11,8). Crosses 94A at (12,8). That's 86D[12-11]=86D[1].")
print("   So cal_pos should be 1, not 0!")
print("   ZIP[1] = 'I' = CIRCLEABOUT[1] = 'I'. CONFIRMED MATCH!")
print()
print("   The cal_pos values in the input data may have errors.")
print("   This should be recalculated from grid positions.")
print()

# Recalculate cal_pos from grid positions
print("=" * 80)
print("RECALCULATING cal_pos FROM GRID GEOMETRY")
print("=" * 80)
print()

for date, num, etype, row, col, length, crossings in calendar_entries:
    stair_row = calendar_to_staircase[num]

    for theme, theme_pos, cal_pos in crossings:
        te = theme_entries[theme]

        if etype == 'D':
            # Down entry: occupies (row, col) to (row+length-1, col)
            # Theme entry (Across): occupies (te_row, te_col) to (te_row, te_col+te_len-1)
            # Crossing at (te_row, col)
            # cal position = te_row - row
            # theme position = col - te_col

            if theme.endswith('A'):
                cross_row = te['row']
                cross_col = col
                actual_cal_pos = cross_row - row
                actual_theme_pos = cross_col - te['col']
            else:
                # Down crosses Down - unusual, skip
                actual_cal_pos = '?'
                actual_theme_pos = '?'

        elif etype == 'A':
            # Across entry: occupies (row, col) to (row, col+length-1)
            # Theme entry (Down): occupies (te_row, te_col) to (te_row+te_len-1, te_col)
            # Crossing at (row, te_col)
            # cal position = te_col - col
            # theme position = row - te_row

            if theme.endswith('D'):
                cross_row = row
                cross_col = te['col']
                actual_cal_pos = cross_col - col
                actual_theme_pos = cross_row - te['row']
            else:
                # Across crosses Across - they'd need to be A and D
                # Actually an Across can cross an Across if one is relabeled
                # But standard crosswords: A crosses D and vice versa
                cross_row = row
                cross_col = col + theme_pos  # We can try to recalculate
                # For across crossing across at same row... this shouldn't happen
                # Let me check: if theme is Across, crossing with Across entry
                # means they share a row. Position in theme = col - te_col + theme_pos?
                # Actually this is ambiguous without more info
                actual_cal_pos = '?'
                actual_theme_pos = '?'

        match_cal = "OK" if actual_cal_pos == cal_pos else f"DIFF (given {cal_pos}, calculated {actual_cal_pos})"
        match_theme = "OK" if actual_theme_pos == theme_pos else f"DIFF (given {theme_pos}, calculated {actual_theme_pos})"

        print(f"  {num}{etype} (at r{row},c{col},len={length}) x {theme} (at r{te['row']},c{te['col']},len={te['len']})")
        print(f"    Given:      theme_pos={theme_pos}, cal_pos={cal_pos}")
        print(f"    Calculated: theme_pos={actual_theme_pos}, cal_pos={actual_cal_pos}")
        print(f"    Theme pos: {match_theme}")
        print(f"    Cal pos:   {match_cal}")

        if te['known'] == 'all' and isinstance(actual_theme_pos, int):
            letter = te['fill'][actual_theme_pos]
            print(f"    Letter at crossing: '{letter}'")
        elif isinstance(te['known'], dict) and isinstance(actual_theme_pos, int) and actual_theme_pos in te['known']:
            letter = te['known'][actual_theme_pos]
            print(f"    Known letter at crossing: '{letter}'")

        print()

print()
print("=" * 80)
print("FINAL ANALYSIS COMPLETE")
print("=" * 80)
