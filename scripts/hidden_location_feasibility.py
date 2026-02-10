#!/usr/bin/env python3
"""
Check how feasible it is to hide each location name within 14-16 letter
English phrases (crossword theme entry answers).
"""

# Theme entry lengths: 25A(16), 50A(16), 73A(14), 114A(14), 138A(16), 167A(16), 19D(15), 78D(15)
# Total capacity: 16+16+14+14+16+16+15+15 = 122 letters across 8 entries
# Need to hide 11 locations

import subprocess
import re

def find_words_containing(pattern):
    """Find dictionary words containing the pattern as a case-insensitive substring."""
    result = subprocess.run(
        ['grep', '-i', pattern.lower(), '/usr/share/dict/words'],
        capture_output=True, text=True
    )
    words = [w.strip() for w in result.stdout.strip().split('\n') if w.strip()]
    # Filter to words that actually contain the pattern as substring
    return [w for w in words if pattern.lower() in w.lower()]

MELANESIANS_LOCS = ['OMAN', 'GREECE', 'ITALY', 'JAPAN', 'IRAN', 'PERU', 'SPAIN', 'CIV', 'GHANA', 'KENYA', 'LAOS']
AROUNDWORLD_LOCS = ['MALI', 'TEHRAN', 'LAGOS', 'SUDAN', 'OMAN', 'ADEN', 'WALES', 'GOA', 'NIGER', 'DELHI', 'CHAD']

print("=" * 80)
print("HIDDEN LOCATION FEASIBILITY ANALYSIS")
print("=" * 80)

for theory_name, locations in [("MELANESIANS", MELANESIANS_LOCS), ("AROUNDWORLD", AROUNDWORLD_LOCS)]:
    print(f"\n{'='*80}")
    print(f"THEORY: {theory_name}")
    print(f"{'='*80}")

    for loc in locations:
        # Method 1: Search dictionary for words containing the location
        containing = find_words_containing(loc)

        # Method 2: Manually check common English words/phrases
        # In crossword hidden-word puzzles, the word appears as consecutive
        # letters across a phrase. e.g., "ROMAN ATTIC" hides "OMAN"

        print(f"\n  {loc} ({len(loc)} letters):")

        if containing:
            # Show up to 10 examples
            examples = containing[:10]
            print(f"    Dictionary words containing '{loc}': {len(containing)}")
            for w in examples:
                # Highlight the location within the word
                idx = w.lower().index(loc.lower())
                highlighted = w[:idx] + '[' + w[idx:idx+len(loc)] + ']' + w[idx+len(loc):]
                print(f"      {highlighted}")
            if len(containing) > 10:
                print(f"      ... and {len(containing) - 10} more")
        else:
            print(f"    Dictionary words containing '{loc}': 0")

        # Method 3: Show common phrase examples where the word spans a boundary
        print(f"    Phrase examples (hidden word spanning word boundary):")
        phrase_examples = {
            'OMAN': ['RO[MAN]CE', 'RO[MAN]TIC', 'W[OMAN]HOOD', 'AUTO[MAN]IA', 'DIPLO[MAN]CY'],
            'GREECE': ['DIS[GREECE]D? (unlikely)', 'Hard to hide 6 letters naturally'],
            'ITALY': ['HOSP[ITAL]ITY → has ITAL but not ITALY', 'DIGI[TALLY] → has TALLY not ITALY', 'VIT[ALITY] → ALITY not ITALY', 'Very hard - no natural ITALY substring'],
            'JAPAN': ['No common English words/phrases with JAPAN substring', 'Would need something like "...JA PAN..." across boundary'],
            'IRAN': ['ASP[IRAN]T', 'CONSP[IRAN]CY? (not real)', 'ENV[IRON]MENT has IRON not IRAN', 'SP[IRAN]D? No...', 'Possible: "...IRA NEVER..." boundary trick'],
            'PERU': ['[PERU]SAL', '[PERU]SE', 'SUPER[PERU]b? No...', 'Easy via PERUSAL/PERUSE'],
            'SPAIN': ['Hard: SPAIN as substring is rare', 'DES[PAIN]? Missing S...', '"...PAS IN..." reversed? No.', 'Would need phrase like "...S PAIN..."'],
            'CIV': ['[CIV]IL', '[CIV]IC', '[CIV]ILITY', 'Very easy as substring'],
            'GHANA': ['AF[GHANA]ISTAN → but that\'s 11 letters', 'Possible in phrases: "...GH ANA..." boundary'],
            'KENYA': ['Rare as substring', 'Would need "...KEN YA..." or "DONKE[YA]RD?"', 'Mon[KENYA]? No...'],
            'LAOS': ['Hard: LAOS as substring is unusual', 'Possible: "...LA OS..." but forced'],
            'MALI': ['ANO[MALI]ES', 'ABNOR[MALI]TY', 'ANI[MALI]SM', 'FOR[MALI]TY', 'NOR[MALI]ZE', 'Very easy - many words contain MALI'],
            'TEHRAN': ['No common words contain TEHRAN', 'Would need phrase: "...THE RAN..." boundary'],
            'LAGOS': ['Hard as substring', '"...FLAG OS..." boundary?', 'Possible in phrases'],
            'SUDAN': ['No common words contain SUDAN', '"...S UDAN..." unlikely'],
            'ADEN': ['L[ADEN]', 'UNL[ADEN]', 'OVER[LADEN]', 'GR[ADEN]T? No: GRADIENT has ADIE not ADEN', 'G[ADEN]E? No...', 'ADEN in LADEN/UNLADEN is easiest'],
            'WALES': ['[WALES]? Hard in single words', 'Possible: "...W ALES..." or DOWNSCALES has no WALES'],
            'GOA': ['AR[GOA]TS? No...', '[GOA]T', '[GOA]L', '[GOA]LING', 'Easy - GOA appears in GOAT, GOAL etc.'],
            'NIGER': ['Common in many words but sensitive', 'NI[GER]IA has GERI not whole NIGER at right pos', 'In NIGER: "...NI GER..." boundary'],
            'DELHI': ['Hard: DELHI as substring', '"...DEL HI..." boundary possible'],
            'CHAD': ['OR[CHAD] → ORCHARD!', '[CHAD]? Limited in single words', 'Easy in ORCHARD'],
        }

        if loc in phrase_examples:
            for ex in phrase_examples[loc]:
                print(f"      {ex}")

    # Summary
    print(f"\n  HIDABILITY SUMMARY for {theory_name}:")
    easy = []
    medium = []
    hard = []

    for loc in locations:
        containing = find_words_containing(loc)
        if len(containing) >= 5:
            easy.append(loc)
        elif len(containing) >= 1:
            medium.append(loc)
        else:
            # Check phrase feasibility manually
            easy_phrases = {'OMAN', 'CIV', 'IRAN', 'PERU', 'MALI', 'ADEN', 'GOA', 'CHAD'}
            if loc in easy_phrases:
                medium.append(loc)
            else:
                hard.append(loc)

    print(f"    Easy (many dictionary words): {', '.join(easy) if easy else 'None'}")
    print(f"    Medium (some options/phrases): {', '.join(medium) if medium else 'None'}")
    print(f"    Hard (very few natural fits): {', '.join(hard) if hard else 'None'}")

# Key insight about theme entries
print(f"\n{'='*80}")
print("KEY INSIGHT: Theme entries are MULTI-WORD PHRASES")
print(f"{'='*80}")
print("""
Hidden-word puzzles hide words across WORD BOUNDARIES in phrases.
The theme entry answers are 14-16 letter phrases, often multi-word.

Example: If 25A = "AUTOMANIACALLY" (not real), it hides "OMAN" at pos 3-6.
Example: If 114A = "PERUSEDNOTEBOOK" (not real), it hides "PERU" at pos 0-3.

The feasibility depends on the ACTUAL theme entry answers, which we don't
know yet (except 94A = CIRCLEABOUT).

Hidden locations in CIRCLEABOUT (11 letters):
""")

# Check what's hidden in CIRCLEABOUT
circleabout = "CIRCLEABOUT"
all_locs = set(MELANESIANS_LOCS + AROUNDWORLD_LOCS)
for loc in sorted(all_locs):
    if loc.upper() in circleabout.upper():
        idx = circleabout.upper().index(loc.upper())
        print(f"  FOUND: {loc} at positions {idx}-{idx+len(loc)-1} in CIRCLEABOUT")

# Check partial matches
print("\n  Partial substring checks in CIRCLEABOUT:")
for loc in sorted(all_locs):
    for start in range(len(circleabout)):
        for end in range(start+2, min(start+len(loc)+1, len(circleabout)+1)):
            substr = circleabout[start:end]
            if substr.upper() == loc[:end-start].upper() and end-start >= 3:
                if end - start == len(loc):
                    print(f"  FULL MATCH: {loc} at positions {start}-{end-1}")
                elif end - start >= 3:
                    pass  # Don't print partial matches, too noisy

# What about known placed answers near theme entries?
print(f"\n{'='*80}")
print("THEME ENTRY CONSTRAINTS FROM PLACED CROSSINGS")
print(f"{'='*80}")
print("""
50A (16 letters, row 6): Known letters at pos 10=A, 13=R
  MELANESIANS needs: OMAN/GREECE/etc. hidden somewhere
  AROUNDWORLD needs: various locations hidden

73A (14 letters, row 9): Known letter at pos 0(?)=U (from col11=46D chain)

114A (14 letters, row 15): Known letters at pos 9=E, 13=E (from TOLEDO/DENVER)

138A (16 letters, row 18): Known letter at pos 4=E (from DENVER chain)
  If ORGANIC hypothesis: pos 9=I

For BOTH theories, the actual constraint test requires:
1. Knowing more letters in the theme entries
2. Finding multi-word phrases that contain the target location names
3. All crossing letters must be consistent

Without more crossword fill, we cannot definitively prove either theory
from theme entry analysis alone.
""")
