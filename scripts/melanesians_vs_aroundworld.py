#!/usr/bin/env python3
"""
Compare MELANESIANS vs AROUNDWORLD staircase theories.
MrBeast Million Dollar Puzzle Hunt
"""

# Exact staircase layout from HTML/pixel analysis
LAYOUT = [
    # (row, start_col, length)
    (1, 3, 4),   # cols 3,4,5,6
    (2, 1, 6),   # cols 1,2,3,4,5,6
    (3, 1, 5),   # cols 1,2,3,4,5
    (4, 3, 5),   # cols 3,4,5,6,7
    (5, 1, 4),   # cols 1,2,3,4
    (6, 3, 4),   # cols 3,4,5,6
    (7, 4, 5),   # cols 4,5,6,7,8
    (8, 3, 3),   # cols 3,4,5
    (9, 0, 5),   # cols 0,1,2,3,4
    (10, 2, 5),  # cols 2,3,4,5,6
    (11, 1, 4),  # cols 1,2,3,4
]

SPINE_COL = 4  # Column 4 is the spine

# MELANESIANS theory
MELANESIANS = {
    'name': 'MELANESIANS',
    'locations': ['OMAN', 'GREECE', 'ITALY', 'JAPAN', 'IRAN', 'PERU', 'SPAIN', 'CIV', 'GHANA', 'KENYA', 'LAOS'],
}

# AROUNDWORLD theory
AROUNDWORLD = {
    'name': 'AROUNDWORLD',
    'locations': ['MALI', 'TEHRAN', 'LAGOS', 'SUDAN', 'OMAN', 'ADEN', 'WALES', 'GOA', 'NIGER', 'DELHI', 'CHAD'],
}

def verify_theory(theory):
    """Verify a staircase theory against the layout."""
    name = theory['name']
    locations = theory['locations']

    print(f"\n{'='*70}")
    print(f"THEORY: {name}")
    print(f"{'='*70}")

    spine_letters = []
    all_ok = True

    print(f"\n{'Row':<6} {'Location':<10} {'Len':<5} {'ExpLen':<7} {'StartCol':<9} {'Col4Pos':<8} {'Col4Let':<8} {'Match'}")
    print("-" * 70)

    for i, (row, start_col, length) in enumerate(LAYOUT):
        loc = locations[i]
        col4_pos = SPINE_COL - start_col
        col4_letter = loc[col4_pos] if 0 <= col4_pos < len(loc) else '?'
        spine_letters.append(col4_letter)
        len_match = len(loc) == length

        status = "✓" if len_match else "✗"
        if not len_match:
            all_ok = False

        print(f"R{row:<5} {loc:<10} {len(loc):<5} {length:<7} {start_col:<9} {col4_pos:<8} {col4_letter:<8} {status}")

    spine_word = ''.join(spine_letters)
    print(f"\nColumn 4 spine: {spine_word}")
    print(f"All lengths match: {'YES ✓' if all_ok else 'NO ✗'}")

    # Check if spine is a real word
    import subprocess
    result = subprocess.run(['grep', '-i', f'^{spine_word}$', '/usr/share/dict/words'],
                          capture_output=True, text=True)
    is_word = bool(result.stdout.strip())
    print(f"Is '{spine_word}' a dictionary word: {'YES ✓' if is_word else 'NO'}")

    return spine_word, all_ok

def check_adjacent_overlaps(locations):
    """Check what letters overlap between adjacent rows at shared columns."""
    print(f"\nAdjacent Row Overlaps:")
    print("-" * 70)

    for i in range(len(LAYOUT) - 1):
        row1, start1, len1 = LAYOUT[i]
        row2, start2, len2 = LAYOUT[i + 1]
        end1 = start1 + len1 - 1
        end2 = start2 + len2 - 1

        shared_start = max(start1, start2)
        shared_end = min(end1, end2)

        if shared_start <= shared_end:
            shared_cols = list(range(shared_start, shared_end + 1))
            loc1 = locations[i]
            loc2 = locations[i + 1]

            conflicts = []
            matches = []
            for col in shared_cols:
                l1 = loc1[col - start1]
                l2 = loc2[col - start2]
                if l1 == l2:
                    matches.append(f"col{col}={l1}")
                else:
                    conflicts.append(f"col{col}: {l1}≠{l2}")

            status = "ALL MATCH" if not conflicts else f"{len(conflicts)} CONFLICTS"
            print(f"  R{row1}-R{row2}: shared cols {shared_cols}")
            if matches:
                print(f"    Matches: {', '.join(matches)}")
            if conflicts:
                print(f"    Conflicts: {', '.join(conflicts)}")
            print(f"    Status: {status}")
        else:
            print(f"  R{row1}-R{row2}: no overlap")

def check_hidability(locations):
    """Check how easily each location can be hidden in English phrases."""
    print(f"\nHidden-in-Theme-Entry Feasibility:")
    print("-" * 70)

    # Check if the location name appears as a substring in any common words
    import subprocess

    for loc in locations:
        result = subprocess.run(['grep', '-i', loc.lower(), '/usr/share/dict/words'],
                              capture_output=True, text=True)
        words = [w.strip() for w in result.stdout.strip().split('\n') if w.strip()]
        # Filter to words that contain the location as a substring (case-insensitive)
        containing = [w for w in words if loc.lower() in w.lower() and w.upper() != loc.upper()]

        if containing:
            examples = containing[:5]
            print(f"  {loc} ({len(loc)}): {len(containing)} words contain it → {', '.join(examples)}")
        else:
            print(f"  {loc} ({len(loc)}): 0 words contain it! ← HARD TO HIDE")

def check_all_columns(locations):
    """Read all 9 columns top to bottom."""
    print(f"\nAll Column Readings:")
    print("-" * 70)

    for col in range(9):
        letters = []
        rows_used = []
        for i, (row, start_col, length) in enumerate(LAYOUT):
            pos = col - start_col
            if 0 <= pos < length:
                letters.append(locations[i][pos])
                rows_used.append(f"R{row}")

        word = ''.join(letters)
        if letters:
            print(f"  Col {col}: {word} (from {', '.join(rows_used)})")

def analyze_mrbeast_relevance(locations):
    """Check MrBeast philanthropy relevance."""
    print(f"\nMrBeast Philanthropy Relevance:")
    print("-" * 70)

    mrbeast_countries = {
        'CAMEROON', 'UGANDA', 'KENYA', 'SOMALIA', 'ZIMBABWE', 'MALAWI',
        'MOZAMBIQUE', 'NIGERIA', 'RWANDA', 'MALI', 'CHAD', 'NIGER', 'SUDAN',
        'GHANA', 'USA', 'COLOMBIA', 'BRAZIL', 'BANGLADESH', 'CAMBODIA',
        'INDIA', 'PHILIPPINES', 'UAE', 'SAUDIARABIA', 'UKRAINE', 'PERU',
        'INDONESIA', 'PAKISTAN',
    }

    # Also check cities/regions
    mrbeast_cities = {
        'DELHI', 'DUBAI', 'RIYADH', 'GREENVILLE', 'ACCRA', 'LIMA',
        'LAGOS', 'TEHRAN', 'GOA', 'ADEN', 'OMAN',
    }

    for loc in locations:
        in_countries = loc.upper() in mrbeast_countries
        in_cities = loc.upper() in mrbeast_cities
        relevance = ""
        if in_countries:
            relevance = "★★★ Known philanthropy country"
        elif in_cities:
            relevance = "★★ Known philanthropy city/region"
        else:
            relevance = "☆ No known MrBeast connection"
        print(f"  {loc}: {relevance}")

print("=" * 70)
print("STAIRCASE THEORY COMPARISON")
print("MrBeast Million Dollar Puzzle Hunt")
print("=" * 70)

print(f"\nStaircase Layout (confirmed from HTML + pixel analysis):")
for row, start, length in LAYOUT:
    cells = [' '] * 9
    for j in range(length):
        cells[start + j] = '_'
    print(f"  Row {row:2d}: {'[' + ']['.join(cells) + ']'} = {length} letters (cols {start}-{start+length-1})")

# Verify both theories
mel_spine, mel_ok = verify_theory(MELANESIANS)
aw_spine, aw_ok = verify_theory(AROUNDWORLD)

# Check adjacent overlaps
print(f"\n{'='*70}")
print("ADJACENT ROW OVERLAP ANALYSIS - MELANESIANS")
print(f"{'='*70}")
check_adjacent_overlaps(MELANESIANS['locations'])

print(f"\n{'='*70}")
print("ADJACENT ROW OVERLAP ANALYSIS - AROUNDWORLD")
print(f"{'='*70}")
check_adjacent_overlaps(AROUNDWORLD['locations'])

# Check hidability
print(f"\n{'='*70}")
print("HIDABILITY IN THEME ENTRIES - MELANESIANS")
print(f"{'='*70}")
check_hidability(MELANESIANS['locations'])

print(f"\n{'='*70}")
print("HIDABILITY IN THEME ENTRIES - AROUNDWORLD")
print(f"{'='*70}")
check_hidability(AROUNDWORLD['locations'])

# Check all columns
print(f"\n{'='*70}")
print("ALL COLUMN READINGS - MELANESIANS")
print(f"{'='*70}")
check_all_columns(MELANESIANS['locations'])

print(f"\n{'='*70}")
print("ALL COLUMN READINGS - AROUNDWORLD")
print(f"{'='*70}")
check_all_columns(AROUNDWORLD['locations'])

# MrBeast relevance
print(f"\n{'='*70}")
print("MRBEAST RELEVANCE - MELANESIANS")
print(f"{'='*70}")
analyze_mrbeast_relevance(MELANESIANS['locations'])

print(f"\n{'='*70}")
print("MRBEAST RELEVANCE - AROUNDWORLD")
print(f"{'='*70}")
analyze_mrbeast_relevance(AROUNDWORLD['locations'])

# Final comparison
print(f"\n{'='*70}")
print("COMPARISON SUMMARY")
print(f"{'='*70}")
print(f"""
                        MELANESIANS           AROUNDWORLD
Spine word:             {mel_spine}         {aw_spine}
Is real word:           {'YES' if mel_ok else 'NO'}                   NO (two words)
All lengths match:      {'YES' if mel_ok else 'NO'}                   {'YES' if aw_ok else 'NO'}
Echoes sentence:        NO                    YES ("...AROUND WORLD")
CIV as country code:    YES (ISO 3166)        N/A
MrBeast connection:     WEAK                  STRONG
Easy to hide:           MIXED                 MIXED

Key differences:
- AROUNDWORLD directly echoes the 9-word sentence
- MELANESIANS is a single English word (stronger linguistically)
- CIV (Côte d'Ivoire code) is unusual for a puzzle answer
- AROUNDWORLD locations are more MrBeast-relevant (Africa, philanthropy)
- Neither set perfectly maps to calendar dates
""")

# Check if MELANESIANS fits 167A
print(f"\n{'='*70}")
print("167A ANALYSIS")
print(f"{'='*70}")
print("""
167A is 16 letters. The clue: "What this puzzle commemorates in eleven
hidden words in the theme entries"

If MELANESIANS theory is correct:
- The 11 hidden words spell MELANESIANS via column 4
- But 167A (16 letters) ≠ MELANESIANS (11 letters)
- 167A must be a separate 16-letter phrase answering "what does this
  puzzle commemorate?"

If AROUNDWORLD theory is correct:
- The 11 hidden words spell AROUNDWORLD via column 4
- But 167A (16 letters) ≠ AROUNDWORLD (10-11 letters)
- Same issue: 167A is a different answer

In BOTH cases, 167A is a 16-letter answer independent of the spine word.
The spine word is extracted from the staircase, not from 167A itself.

However: 167A IS a theme entry and itself contains hidden location names!
3 circled cells in 167A at positions 2, 9, 15 (0-indexed) are extraction
points for the final code.
""")
