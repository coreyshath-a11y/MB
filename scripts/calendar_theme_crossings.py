#!/usr/bin/env python3
"""
Calendar Theme Crossings Analysis for MrBeast Million Dollar Puzzle Hunt
Analyzes how the 11 calendar date entries cross the theme entries in the 25x25 crossword.

The 11 circled calendar dates map to entry numbers via month×10+day.
This script determines where these entries intersect theme entries and whether they mark
the starting positions of hidden location names.
"""

# Entry format: (row, col, length)
ACROSS_ENTRIES = {
    1: (0, 0, 7), 8: (0, 9, 6), 14: (0, 17, 8), 22: (1, 0, 7), 23: (1, 8, 7),
    24: (1, 17, 8), 25: (2, 0, 16), 28: (2, 17, 8), 29: (3, 0, 4), 30: (3, 5, 5),
    31: (3, 11, 3), 32: (3, 15, 5), 34: (3, 21, 4), 35: (4, 0, 4), 36: (4, 7, 4),
    38: (4, 12, 9), 41: (4, 22, 3), 42: (5, 0, 4), 43: (5, 5, 3), 45: (5, 9, 4),
    47: (5, 14, 4), 48: (5, 20, 5), 50: (6, 0, 16), 54: (6, 17, 6), 57: (7, 0, 7),
    58: (7, 8, 4), 59: (7, 13, 4), 61: (7, 18, 6), 63: (8, 0, 3), 64: (8, 4, 5),
    66: (8, 10, 4), 68: (8, 16, 4), 70: (8, 21, 4), 72: (9, 3, 6), 73: (9, 11, 14),
    77: (10, 1, 3), 79: (10, 5, 3), 80: (10, 10, 6), 81: (10, 17, 4), 82: (10, 22, 3),
    83: (11, 0, 5), 85: (11, 6, 5), 88: (11, 12, 5), 90: (11, 18, 3), 91: (11, 22, 3),
    92: (12, 0, 6), 94: (12, 7, 11), 97: (12, 19, 6), 99: (13, 0, 3), 100: (13, 4, 3),
    102: (13, 8, 5), 103: (13, 14, 5), 105: (13, 20, 5), 106: (14, 0, 3), 107: (14, 4, 4),
    109: (14, 9, 6), 111: (14, 17, 3), 113: (14, 21, 3), 114: (15, 0, 14), 117: (15, 16, 6),
    119: (16, 0, 4), 120: (16, 5, 4), 121: (16, 11, 4), 123: (16, 16, 5), 124: (16, 22, 3),
    127: (17, 1, 6), 129: (17, 8, 4), 132: (17, 13, 4), 134: (17, 18, 7), 136: (18, 2, 6),
    138: (18, 9, 16), 141: (19, 0, 5), 143: (19, 7, 4), 145: (19, 12, 4), 146: (19, 17, 3),
    147: (19, 21, 4), 148: (20, 0, 3), 149: (20, 4, 9), 153: (20, 14, 4), 155: (20, 21, 4),
    156: (21, 0, 4), 158: (21, 5, 5), 159: (21, 11, 3), 161: (21, 15, 5), 164: (21, 21, 4),
    165: (22, 0, 8), 167: (22, 9, 16), 171: (23, 0, 8), 172: (23, 10, 7), 173: (23, 18, 7),
    174: (24, 0, 8), 175: (24, 10, 6), 176: (24, 18, 7)
}

DOWN_ENTRIES = {
    1: (0, 0, 9), 2: (0, 1, 9), 3: (0, 2, 9), 4: (0, 3, 8), 5: (0, 4, 3),
    6: (0, 5, 4), 7: (0, 6, 4), 8: (0, 9, 8), 9: (0, 10, 3), 10: (0, 11, 4),
    11: (0, 12, 7), 12: (0, 13, 5), 13: (0, 14, 3), 14: (0, 17, 7), 15: (0, 18, 5),
    16: (0, 19, 5), 17: (0, 20, 3), 18: (0, 21, 4), 19: (0, 22, 15), 20: (0, 23, 6),
    21: (0, 24, 6), 23: (1, 8, 4), 26: (2, 7, 5), 27: (2, 15, 6), 33: (3, 16, 3),
    37: (4, 10, 5), 39: (4, 14, 4), 40: (4, 20, 4), 43: (5, 5, 6), 44: (5, 6, 7),
    46: (5, 11, 6), 49: (5, 21, 5), 51: (6, 4, 4), 52: (6, 8, 4), 53: (6, 13, 7),
    55: (6, 18, 6), 56: (6, 19, 7), 60: (7, 16, 3), 62: (7, 23, 8), 65: (8, 7, 5),
    67: (8, 12, 9), 69: (8, 17, 3), 71: (8, 24, 6), 72: (9, 3, 4), 74: (9, 14, 6),
    75: (9, 15, 5), 76: (9, 20, 5), 77: (10, 1, 8), 78: (10, 2, 15), 80: (10, 10, 6),
    83: (11, 0, 6), 84: (11, 4, 5), 86: (11, 8, 3), 87: (11, 9, 5), 89: (11, 16, 3),
    93: (12, 5, 7), 95: (12, 11, 7), 96: (12, 17, 5), 98: (12, 21, 4), 101: (13, 6, 6),
    104: (13, 18, 7), 108: (14, 7, 3), 110: (14, 13, 6), 112: (14, 19, 6), 115: (15, 3, 5),
    116: (15, 8, 3), 117: (15, 16, 4), 118: (15, 20, 4), 122: (16, 14, 5), 124: (16, 22, 9),
    125: (16, 23, 9), 126: (16, 24, 9), 128: (17, 4, 4), 130: (17, 9, 6), 131: (17, 10, 4),
    133: (17, 15, 8), 135: (17, 21, 8), 137: (18, 7, 7), 139: (18, 12, 7), 140: (18, 17, 5),
    141: (19, 0, 6), 142: (19, 1, 6), 144: (19, 8, 3), 150: (20, 5, 5), 151: (20, 6, 5),
    152: (20, 11, 5), 154: (20, 16, 4), 157: (21, 3, 4), 160: (21, 13, 4), 162: (21, 18, 4),
    163: (21, 19, 4), 166: (22, 4, 3), 168: (22, 10, 3), 169: (22, 14, 3), 170: (22, 20, 3)
}

# Calendar entries (month×10 + day = entry number)
# These are the 11 circled calendar dates
CALENDAR_ENTRIES = ['11D', '22A', '31A', '33D', '61A', '71D', '81A', '86D', '91A', '115D', '127A']

# Theme entries (long entries likely containing hidden location names)
THEME_ENTRIES = ['25A', '50A', '73A', '94A', '114A', '138A', '167A', '19D', '78D']

# Known placed letters in theme entries (from solver results)
KNOWN_LETTERS = {
    '50A': {10: 'A', 13: 'R'},
    '73A': {2: 'U'},
    '94A': {0: 'C', 1: 'I', 2: 'R', 3: 'C', 4: 'L', 5: 'E', 6: 'A', 7: 'B', 8: 'O', 9: 'U', 10: 'T'},
    '114A': {9: 'E', 13: 'E'},
    '138A': {4: 'E'},  # potentially 9: 'I' from ORGANIC hypothesis
}

# Staircase row lengths (AROUNDWORLD spine, column 4)
STAIRCASE_ROWS = [4, 6, 5, 5, 4, 4, 5, 3, 5, 5, 4]
STAIRCASE_LETTERS = "AROUNDWORLD"

# Common location names to check for compatibility
LOCATION_NAMES = [
    "AMSTERDAM", "ATHENS", "ATLANTA", "AUSTIN",
    "BALTIMORE", "BANGKOK", "BARCELONA", "BEIJING", "BERLIN", "BOSTON", "BRUSSELS",
    "CAIRO", "CHICAGO", "COPENHAGEN",
    "DALLAS", "DELHI", "DENVER", "DETROIT", "DUBAI", "DUBLIN",
    "EDINBURGH",
    "FLORENCE", "FRANKFURT",
    "GENEVA", "GLASGOW",
    "HAMBURG", "HELSINKI", "HOUSTON",
    "ISTANBUL",
    "JERUSALEM",
    "LASVEGAS", "LISBON", "LONDON", "LOSANGELES",
    "MADRID", "MANCHESTER", "MELBOURNE", "MEXICO", "MIAMI", "MILAN", "MOSCOW", "MUNICH",
    "NAPLES", "NASHVILLE", "NEWORLEANS", "NEWYORK",
    "ORLANDO", "OSLO",
    "PARIS", "PHILADELPHIA", "PHOENIX", "PORTLAND", "PRAGUE",
    "ROME",
    "SANANTONIO", "SANDIEGO", "SANFRANCISCO", "SEATTLE", "SEOUL", "SHANGHAI", "SINGAPORE", "STOCKHOLM", "SYDNEY",
    "TOKYO", "TOLEDO", "TORONTO",
    "VALENCIA", "VANCOUVER", "VENICE", "VIENNA",
    "WARSAW", "WASHINGTON",
    "ZURICH"
]


def parse_entry(entry_str):
    """Parse entry string like '11D' or '22A' into (number, direction)"""
    if entry_str[-1] in 'AD':
        num = int(entry_str[:-1])
        direction = entry_str[-1]
        return num, direction
    return None, None


def get_entry_info(entry_str):
    """Get (row, col, length) for an entry"""
    num, direction = parse_entry(entry_str)
    if not num:
        return None

    if direction == 'A':
        return ACROSS_ENTRIES.get(num)
    else:  # D
        return DOWN_ENTRIES.get(num)


def get_entry_cells(entry_str):
    """Get all cells (row, col) occupied by an entry"""
    info = get_entry_info(entry_str)
    if not info:
        return []

    row, col, length = info
    num, direction = parse_entry(entry_str)

    if direction == 'A':
        return [(row, col + i) for i in range(length)]
    else:  # D
        return [(row + i, col) for i in range(length)]


def find_crossing(entry1_str, entry2_str):
    """Find where two entries cross, return (row, col, pos_in_entry1, pos_in_entry2) or None"""
    cells1 = get_entry_cells(entry1_str)
    cells2 = get_entry_cells(entry2_str)

    for i, cell1 in enumerate(cells1):
        for j, cell2 in enumerate(cells2):
            if cell1 == cell2:
                return (cell1[0], cell1[1], i, j)
    return None


def check_location_compatibility(theme_entry, start_pos, location_name):
    """Check if a location name fits at start_pos in theme_entry given known letters"""
    if theme_entry not in KNOWN_LETTERS:
        return True  # No constraints, so compatible

    known = KNOWN_LETTERS[theme_entry]
    for pos, letter in known.items():
        # Check if this known letter position falls within the location name
        loc_pos = pos - start_pos
        if 0 <= loc_pos < len(location_name):
            if location_name[loc_pos] != letter:
                return False
    return True


def analyze_calendar_crossings():
    """Main analysis of calendar entries crossing theme entries"""

    print("=" * 100)
    print("CALENDAR THEME CROSSINGS ANALYSIS")
    print("MrBeast Million Dollar Puzzle Hunt - 25×25 Crossword")
    print("=" * 100)
    print()
    print(f"Analyzing {len(CALENDAR_ENTRIES)} calendar entries: {', '.join(CALENDAR_ENTRIES)}")
    print(f"Against {len(THEME_ENTRIES)} theme entries: {', '.join(THEME_ENTRIES)}")
    print()

    # Store all crossings for summary
    all_crossings = []
    calendar_to_themes = {}
    theme_to_calendars = {}

    # Analyze each calendar entry
    for cal_entry in CALENDAR_ENTRIES:
        print("\n" + "=" * 100)
        print(f"CALENDAR ENTRY: {cal_entry}")
        print("=" * 100)

        cal_info = get_entry_info(cal_entry)
        if not cal_info:
            print(f"  ERROR: Could not find entry info for {cal_entry}")
            continue

        cal_row, cal_col, cal_len = cal_info
        cal_num, cal_dir = parse_entry(cal_entry)
        print(f"  Position: row={cal_row}, col={cal_col}, length={cal_len}, direction={cal_dir}")

        # Decode calendar date
        month = cal_num // 10
        day = cal_num % 10
        if day == 0:
            month -= 1
            day = 10
        month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        if 1 <= month <= 12:
            print(f"  Calendar Date: {month_names[month]} {day}")

        crossings_for_this_entry = []

        # Check crossings with each theme entry
        for theme_entry in THEME_ENTRIES:
            crossing = find_crossing(cal_entry, theme_entry)
            if crossing:
                row, col, pos_cal, pos_theme = crossing

                theme_info = get_entry_info(theme_entry)
                theme_row, theme_col, theme_len = theme_info

                crossing_data = {
                    'calendar': cal_entry,
                    'theme': theme_entry,
                    'grid_pos': (row, col),
                    'pos_in_cal': pos_cal,
                    'pos_in_theme': pos_theme,
                    'theme_len': theme_len,
                    'cal_len': cal_len
                }

                crossings_for_this_entry.append(crossing_data)
                all_crossings.append(crossing_data)

                # Update mappings
                if cal_entry not in calendar_to_themes:
                    calendar_to_themes[cal_entry] = []
                calendar_to_themes[cal_entry].append(theme_entry)

                if theme_entry not in theme_to_calendars:
                    theme_to_calendars[theme_entry] = []
                theme_to_calendars[theme_entry].append(cal_entry)

                print(f"\n  ✓ Crosses {theme_entry} (length {theme_len})")
                print(f"    Grid cell: ({row}, {col})")
                print(f"    Position in {cal_entry}: {pos_cal}/{cal_len-1}")
                print(f"    Position in {theme_entry}: {pos_theme}/{theme_len-1}")

                # Check if this marks the START of theme entry
                if pos_theme == 0:
                    print(f"    ★★★ {cal_entry} crosses at the START of {theme_entry}! ★★★")

                # Check known letters
                if theme_entry in KNOWN_LETTERS:
                    if pos_theme in KNOWN_LETTERS[theme_entry]:
                        letter = KNOWN_LETTERS[theme_entry][pos_theme]
                        print(f"    Known letter at this position: {letter}")

                    # Show all known letters for this theme entry
                    known_str = ['_'] * theme_len
                    for kpos, kletter in KNOWN_LETTERS[theme_entry].items():
                        if 0 <= kpos < theme_len:
                            known_str[kpos] = kletter
                    print(f"    {theme_entry} pattern: {''.join(known_str)}")

                # Check if location names could fit starting at this crossing
                print(f"    Checking if location names could start at position {pos_theme}:")
                compatible_locations = []
                for location in LOCATION_NAMES:
                    if pos_theme + len(location) <= theme_len:
                        if check_location_compatibility(theme_entry, pos_theme, location):
                            compatible_locations.append(location)

                if compatible_locations:
                    print(f"    Compatible locations ({len(compatible_locations)}): {', '.join(compatible_locations[:10])}")
                    if len(compatible_locations) > 10:
                        print(f"      ... and {len(compatible_locations) - 10} more")
                else:
                    print(f"    No compatible locations found starting at position {pos_theme}")

        if not crossings_for_this_entry:
            print(f"\n  No crossings with theme entries found.")

    # Summary section
    print("\n\n" + "=" * 100)
    print("SUMMARY: Calendar to Theme Mappings")
    print("=" * 100)

    for cal_entry in sorted(calendar_to_themes.keys(), key=lambda x: int(x[:-1])):
        themes = calendar_to_themes[cal_entry]
        print(f"\n{cal_entry} crosses {len(themes)} theme(s): {', '.join(themes)}")

    print("\n\n" + "=" * 100)
    print("SUMMARY: Theme to Calendar Mappings")
    print("=" * 100)

    for theme_entry in THEME_ENTRIES:
        if theme_entry in theme_to_calendars:
            cals = theme_to_calendars[theme_entry]
            print(f"\n{theme_entry} is crossed by {len(cals)} calendar entry/entries: {', '.join(cals)}")

            # Show crossing positions
            for cal in cals:
                for crossing in all_crossings:
                    if crossing['calendar'] == cal and crossing['theme'] == theme_entry:
                        print(f"  {cal} at position {crossing['pos_in_theme']}/{crossing['theme_len']-1}")
        else:
            print(f"\n{theme_entry} - NO calendar crossings")

    # Check for patterns
    print("\n\n" + "=" * 100)
    print("PATTERN ANALYSIS")
    print("=" * 100)

    # Check if calendar entries mark starts of theme entries
    start_markers = []
    for crossing in all_crossings:
        if crossing['pos_in_theme'] == 0:
            start_markers.append((crossing['calendar'], crossing['theme']))

    print(f"\nCalendar entries that cross at START of theme entries ({len(start_markers)}):")
    for cal, theme in start_markers:
        print(f"  {cal} → {theme} (position 0)")

    # Check spacing patterns
    print("\n\nCalendar entry spacing in theme entries:")
    for theme_entry in THEME_ENTRIES:
        if theme_entry in theme_to_calendars:
            positions = []
            for cal in theme_to_calendars[theme_entry]:
                for crossing in all_crossings:
                    if crossing['calendar'] == cal and crossing['theme'] == theme_entry:
                        positions.append((crossing['pos_in_theme'], cal))

            positions.sort()
            if len(positions) > 1:
                print(f"\n  {theme_entry}: {len(positions)} crossings")
                for pos, cal in positions:
                    print(f"    Position {pos:2d}: {cal}")

                # Calculate spacing
                spacings = [positions[i+1][0] - positions[i][0] for i in range(len(positions)-1)]
                print(f"    Spacings: {spacings}")

    # Check if all 11 calendar entries are accounted for
    print("\n\nCalendar entries NOT crossing any theme entries:")
    for cal in CALENDAR_ENTRIES:
        if cal not in calendar_to_themes:
            print(f"  {cal}")

    # Staircase analysis
    print("\n\n" + "=" * 100)
    print("STAIRCASE ANALYSIS (AROUNDWORLD spine)")
    print("=" * 100)
    print(f"\nStaircase at column 4, lengths: {STAIRCASE_ROWS}")
    print(f"Letters: {' '.join(STAIRCASE_LETTERS)}")

    # Find which entries intersect column 4
    print("\n\nEntries crossing the staircase spine (column 4):")
    for theme_entry in THEME_ENTRIES:
        cells = get_entry_cells(theme_entry)
        for i, (row, col) in enumerate(cells):
            if col == 4:
                print(f"  {theme_entry} position {i} at row {row}, col {col}")
                if row < len(STAIRCASE_LETTERS):
                    print(f"    Staircase letter: {STAIRCASE_LETTERS[row]}")

    print("\n\n" + "=" * 100)
    print("Analysis complete!")
    print("=" * 100)


if __name__ == '__main__':
    analyze_calendar_crossings()
