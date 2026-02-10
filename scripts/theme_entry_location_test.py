#!/usr/bin/env python3
"""
Test whether MELANESIANS or AROUNDWORLD locations can be hidden at positions
compatible with known crossword letters in theme entries.
"""

# Known theme entry constraints (from 17 placed entries)
THEME_CONSTRAINTS = {
    '25A': {'length': 16, 'row': 2, 'col': 0, 'known': {}},  # No known letters
    '50A': {'length': 16, 'row': 6, 'col': 0, 'known': {10: 'A', 13: 'R'}},  # From ABASH, ROTUNDA
    '73A': {'length': 14, 'row': 9, 'col': 11, 'known': {}},  # Check crossings
    '94A': {'length': 11, 'row': 12, 'col': 7, 'known': {i: c for i, c in enumerate('CIRCLEABOUT')}},  # COMPLETE
    '114A': {'length': 14, 'row': 15, 'col': 0, 'known': {9: 'E', 13: 'E'}},  # From TRITE[4], DENVER[1]
    '138A': {'length': 16, 'row': 18, 'col': 9, 'known': {4: 'E'}},  # From DENVER[4]
    '167A': {'length': 16, 'row': 22, 'col': 9, 'known': {}},  # No known letters
    '19D': {'length': 15, 'row': 0, 'col': 22, 'known': {}},  # No known letters
    '78D': {'length': 15, 'row': 10, 'col': 2, 'known': {}},  # No known letters
}

# Add ORGANIC hypothesis constraint
ORGANIC_EXTRA = {'138A_organic': {9: 'I'}}  # If 104D = ORGANIC

MELANESIANS = ['OMAN', 'GREECE', 'ITALY', 'JAPAN', 'IRAN', 'PERU', 'SPAIN', 'CIV', 'GHANA', 'KENYA', 'LAOS']
AROUNDWORLD = ['MALI', 'TEHRAN', 'LAGOS', 'SUDAN', 'OMAN', 'ADEN', 'WALES', 'GOA', 'NIGER', 'DELHI', 'CHAD']

def check_location_fit(location, theme_entry, known_letters):
    """Check all possible positions where a location could be hidden in a theme entry."""
    entry_len = theme_entry['length']
    loc_len = len(location)
    valid_positions = []

    for start in range(entry_len - loc_len + 1):
        # Check if location letters conflict with known letters
        conflict = False
        matches = 0
        for i, letter in enumerate(location):
            pos = start + i
            if pos in known_letters:
                if known_letters[pos] == letter:
                    matches += 1
                else:
                    conflict = True
                    break

        if not conflict:
            valid_positions.append((start, matches))

    return valid_positions

print("=" * 80)
print("THEME ENTRY LOCATION COMPATIBILITY TEST")
print("=" * 80)

for theory_name, locations in [("MELANESIANS", MELANESIANS), ("AROUNDWORLD", AROUNDWORLD)]:
    print(f"\n{'='*80}")
    print(f"THEORY: {theory_name}")
    print(f"{'='*80}")

    # Skip 94A (already complete, no room for additional hidden words)
    theme_entries = {k: v for k, v in THEME_CONSTRAINTS.items() if k != '94A'}

    for loc in locations:
        print(f"\n  {loc} ({len(loc)} letters):")
        found_any = False

        for entry_name, entry in theme_entries.items():
            positions = check_location_fit(loc, entry, entry['known'])
            if positions:
                found_any = True
                for start, matches in positions:
                    match_str = f" (matches {matches} known letter{'s' if matches > 1 else ''}!)" if matches > 0 else ""
                    # Show which letters match
                    detail = ""
                    if matches > 0:
                        for i, letter in enumerate(loc):
                            pos = start + i
                            if pos in entry['known'] and entry['known'][pos] == letter:
                                detail += f" pos{pos}={letter}"
                    print(f"    {entry_name}: positions {start}-{start+len(loc)-1}{match_str}{detail}")

        if not found_any:
            print(f"    NO compatible theme entries found!")

    # KEY TEST: Can any location span BOTH known letters in 50A (pos10=A, pos13=R)?
    print(f"\n  --- KEY TEST: Single location matching BOTH 50A pos10=A AND pos13=R ---")
    for loc in locations:
        for start in range(16 - len(loc) + 1):
            hits_10 = False
            hits_13 = False
            conflict = False
            for i, letter in enumerate(loc):
                pos = start + i
                if pos == 10:
                    if letter == 'A':
                        hits_10 = True
                    else:
                        conflict = True
                if pos == 13:
                    if letter == 'R':
                        hits_13 = True
                    else:
                        conflict = True
            if hits_10 and hits_13 and not conflict:
                print(f"    {loc} at pos {start}-{start+len(loc)-1}: "
                      f"{''.join(['['+c+']' if (start+j)==10 or (start+j)==13 else c for j, c in enumerate(loc)])}")

    # Also test with ORGANIC hypothesis for 138A
    print(f"\n  --- 138A with ORGANIC hypothesis (pos4=E, pos9=I) ---")
    known_138a_organic = {4: 'E', 9: 'I'}
    for loc in locations:
        entry_len = 16
        loc_len = len(loc)
        for start in range(entry_len - loc_len + 1):
            conflict = False
            matches = 0
            for i, letter in enumerate(loc):
                pos = start + i
                if pos in known_138a_organic:
                    if known_138a_organic[pos] == letter:
                        matches += 1
                    else:
                        conflict = True
                        break
            if not conflict and matches > 0:
                print(f"    {loc} at pos {start}-{start+len(loc)-1}: matches {matches} letter(s)")

# DAKAR specific test (not in either list but relevant)
print(f"\n{'='*80}")
print("SPECIAL TEST: DAKAR in 50A")
print(f"{'='*80}")
dakar = "DAKAR"
known_50a = {10: 'A', 13: 'R'}
for start in range(16 - len(dakar) + 1):
    conflict = False
    matches = 0
    for i, letter in enumerate(dakar):
        pos = start + i
        if pos in known_50a:
            if known_50a[pos] == letter:
                matches += 1
            else:
                conflict = True
                break
    if not conflict and matches > 0:
        vis = ""
        for i, letter in enumerate(dakar):
            pos = start + i
            if pos in known_50a:
                vis += f"[{letter}]"
            else:
                vis += letter
        print(f"  DAKAR at pos {start}-{start+len(dakar)-1}: {vis} → matches {matches} known letters!")

print(f"\n{'='*80}")
print("CONCLUSION")
print(f"{'='*80}")
print("""
CRITICAL FINDING: 50A known letters (pos10=A, pos13=R)

For AROUNDWORLD theory:
  DAKAR at positions 9-13: D,[A],K,A,[R] → matches BOTH known letters perfectly!
  This is a 5-letter location explaining 2 out of 2 known letters.

For MELANESIANS theory:
  NO single location matches both pos10=A and pos13=R simultaneously.
  The locations would need to be placed to avoid conflicting with known letters,
  but none can CONFIRM both letters at once.

This is STRONG evidence favoring AROUNDWORLD over MELANESIANS for the
50A theme entry.

However, MELANESIANS cannot be fully ruled out — the known letters could
be explained by non-location parts of the 50A answer phrase. But the
elegance of DAKAR matching both constraints is compelling.
""")
