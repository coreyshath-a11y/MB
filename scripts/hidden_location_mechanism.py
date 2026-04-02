#!/usr/bin/env python3
"""
Investigate HOW locations are hidden in theme entries.
Key puzzle: 94A=CIRCLEABOUT and 167A=SUPERBOWLSTADIUM contain NO location substrings.
Either these entries don't contain locations, or the mechanism is different.

167A clue: "What this puzzle commemorates in eleven hidden words in theme entries"
→ 11 hidden words IN theme entries. The words = location names.
→ 11 locations distributed across 9 theme entries.
→ Some entries may have 2 locations, some may have 0.

Hypothesis: Maybe not ALL theme entries contain locations.
The staircase has 11 rows but there are 9 theme entries.
If locations are 1-per-entry, 2 entries have none. CIRCLEABOUT and SUPERBOWLSTADIUM could be those 2.
OR some entries have 2 locations and some have 0.
"""

print("=" * 70)
print("HIDDEN LOCATION MECHANISM INVESTIGATION")
print("=" * 70)

# Theme entries and their lengths
theme_entries = [
    ("25A",  16, None),           # Unconstrained
    ("50A",  16, None),           # DAKAR at 9-13 confirmed
    ("73A",  14, None),           # U at pos 2
    ("94A",  11, "CIRCLEABOUT"),  # COMPLETE - no locations found
    ("114A", 14, None),           # DELHI at 8-12 strong
    ("138A", 16, None),           # E at pos 4
    ("167A", 16, "SUPERBOWLSTADIUM"),  # COMPLETE - no locations found
    ("19D",  15, None),           # Unconstrained
    ("78D",  15, None),           # Unconstrained
]

aroundworld = ["MALI", "TEHRAN", "LAGOS", "SUDAN", "OMAN", "ADEN", "WALES", "GOA", "DAKAR", "DELHI", "CHAD"]

print("\n--- Distribution of 11 locations across 9 theme entries ---")
print()
print("If each theme entry has at most 2 hidden locations:")
print(f"  Total theme entry letters: {sum(e[1] for e in theme_entries)} = 133")
print(f"  Total location letters: {sum(len(l) for l in aroundworld)} = {sum(len(l) for l in aroundworld)}")
print(f"  Location letters as fraction: {sum(len(l) for l in aroundworld)/sum(e[1] for e in theme_entries):.1%}")
print()

# Can theme entries contain MULTIPLE locations?
# 94A = CIRCLEABOUT (11 letters) - could it contain 2 short locations overlapping?
print("--- Check for OVERLAPPING location names ---")
print()

for name, length, fill in theme_entries:
    if fill:
        print(f"{name} = {fill} ({length} letters):")
        # Check all possible location substrings, including partial
        for loc in aroundworld:
            for start in range(length - len(loc) + 1):
                if fill[start:start+len(loc)] == loc:
                    print(f"  FOUND: {loc} at pos {start}-{start+len(loc)-1}")

        # Check REVERSED
        rev_fill = fill[::-1]
        for loc in aroundworld:
            for start in range(length - len(loc) + 1):
                if rev_fill[start:start+len(loc)] == loc:
                    print(f"  REVERSED: {loc} at pos {length-1-start-len(loc)+1}-{length-1-start} (reading backwards)")

        # Check for locations reading DOWN through the entry
        # (Not applicable for across entries read normally)

        print()

# What about non-contiguous hidden words?
# e.g., "hidden" in the classic sense: every Nth letter?
print("--- Check for EVERY-OTHER-LETTER patterns ---")
for name, length, fill in theme_entries:
    if fill:
        print(f"\n{name} = {fill}:")
        # Every 2nd letter starting from pos 0
        even = fill[0::2]
        odd = fill[1::2]
        print(f"  Even positions: {even}")
        print(f"  Odd positions:  {odd}")
        for loc in aroundworld:
            if loc in even:
                print(f"  ★ {loc} found in even-position letters!")
            if loc in odd:
                print(f"  ★ {loc} found in odd-position letters!")

# What about reading the FIRST letter of each theme entry?
print("\n--- First letters of theme entries ---")
# We only know 2 complete entries
# 94A = C, 167A = S
# If 25A = S (SUPERBOWLATLEVIS?), 50A = ?, 73A = ?, etc.
print("94A → C, 167A → S")
print("If 25A = SUPERBOWLATLEVIS: S")
print("First letters: S, ?, ?, C, ?, ?, S, ?, ?")
print("Not enough data.")

# What about theme entry ANSWERS forming a message?
# The 9 theme entries could spell something when their first/last letters are read
print("\n--- Possible theme entry patterns ---")
print("Theme entries serve as CONTAINERS for hidden location names.")
print("If 11 locations in 9 entries, distribution could be:")
print("  - 7 entries with 1 location each + 2 entries with 2 locations each")
print("  - 9 entries with 1 location each + 2 locations share across entries")
print("  - Or some entries have 0 locations (like 94A, 167A)")
print()

# Key insight: the staircase grid has 11 rows = 11 locations.
# 167A asks for "eleven hidden words in the theme entries"
# So ALL 11 must be IN theme entries.
# CIRCLEABOUT has 11 letters. No location substring.
# SUPERBOWLSTADIUM has 16 letters. No location substring.
# These are theme entries without locations, OR we're missing something.

print("=" * 70)
print("CHECK: Are any locations hidden ACROSS entry boundaries?")
print("=" * 70)
print()
print("What if a location spans across two adjacent theme entries")
print("that share crossing down entries? Probably not — 167A says")
print("'hidden words IN the theme entries', implying within single entries.")
print()

# Let me reconsider: what if the location names aren't the AROUNDWORLD set?
# What if they're the USER-PROVIDED locations?
print("=" * 70)
print("ALTERNATIVE: What if hidden locations are from USER's list?")
print("=" * 70)
print()

user_locs = ["LIMA", "ACCRA", "TOKYO", "LONDON", "CHICAGO", "NEWYORK",
             "BUFFALO", "ATHENS", "TIJUANA", "LINCOLN", "USHUAIA",
             "KUPANG", "ARLES", "KABUL", "DIVO", "MACON", "WICHITA"]

for name_entry, length, fill in theme_entries:
    if fill:
        print(f"{name_entry} = {fill}:")
        for loc in user_locs:
            if loc in fill:
                pos = fill.index(loc)
                print(f"  FOUND: {loc} at pos {pos}-{pos+len(loc)-1}")
        # Also check reversed
        rev = fill[::-1]
        for loc in user_locs:
            if loc in rev:
                pos = len(fill) - rev.index(loc) - len(loc)
                print(f"  REVERSED: {loc} at pos {pos}-{pos+len(loc)-1}")

# Check SUPERBOWLSTADIUM more carefully
print()
print("SUPERBOWLSTADIUM letter-by-letter:")
fill = "SUPERBOWLSTADIUM"
for i, ch in enumerate(fill):
    print(f"  pos {i:2d}: {ch}", end="")
    # Check if any location starts with the remaining substring
    remaining = fill[i:]
    starters = [l for l in aroundworld + user_locs if remaining.startswith(l)]
    if starters:
        print(f"  ← starts: {starters}")
    else:
        print()

# KEY CHECK: what about the word "STAD" in SUPERBOWLSTADIUM?
# STAD could be... no, that's not a location.
# What about BOWL? BOWL isn't a location.
# SUP? No. STADIUM? No.
# STADI? STAD? No.
# But wait: "SUPER" could hide... no.
# "OWL" — not a location
# "BOWL" — Bowl is not...

print()
print("=" * 70)
print("CHECK: Country NAMES hidden via creative parsing")
print("=" * 70)
# What about IRAN in "SUPERBOWLSTADIUM"?
# S-U-P-E-R-B-O-W-L-S-T-A-D-I-U-M
# No IRAN substring
# What about less common location names?
# STA? — not a location
# PERU backwards = UREP... no.
# OMAN backwards = NAMO... no.
# MALI backwards = ILAM...

# What about the word STADIUM itself?
# S-T-A-D-I-U-M
# Contains: STADI, TADIU, ADIUM, STAD, TADI, ADIU, DIUM...
# None are locations.

# What about Abu (in Abu Dhabi)?
# No ABU substring.

# CUBA? No CUBA in SUPERBOWLSTADIUM.
# CHAD? C not in SUPERBOWLSTADIUM.

# Let me check a much broader set
print("\nBrute-force: ALL 3+ letter substrings of SUPERBOWLSTADIUM that are locations:")
import subprocess
result = subprocess.run(['cat', '/usr/share/dict/words'], capture_output=True, text=True)
all_words = set(w.strip().upper() for w in result.stdout.split('\n') if len(w.strip()) >= 3)

# Also check against a list of world countries/cities
countries = [
    "AFGHANISTAN", "ALBANIA", "ALGERIA", "ANDORRA", "ANGOLA", "ARGENTINA",
    "ARMENIA", "AUSTRALIA", "AUSTRIA", "AZERBAIJAN", "BAHAMAS", "BAHRAIN",
    "BANGLADESH", "BARBADOS", "BELARUS", "BELGIUM", "BELIZE", "BENIN",
    "BHUTAN", "BOLIVIA", "BOSNIA", "BOTSWANA", "BRAZIL", "BRUNEI",
    "BULGARIA", "BURKINA", "BURMA", "BURUNDI", "CAMBODIA", "CAMEROON",
    "CANADA", "CHAD", "CHILE", "CHINA", "COLOMBIA", "COMOROS", "CONGO",
    "COSTARICA", "CROATIA", "CUBA", "CYPRUS", "CZECH", "DENMARK",
    "DJIBOUTI", "DOMINICA", "ECUADOR", "EGYPT", "ELSALVADOR", "ERITREA",
    "ESTONIA", "ETHIOPIA", "FIJI", "FINLAND", "FRANCE", "GABON", "GAMBIA",
    "GEORGIA", "GERMANY", "GHANA", "GREECE", "GRENADA", "GUATEMALA",
    "GUINEA", "GUYANA", "HAITI", "HONDURAS", "HUNGARY", "ICELAND", "INDIA",
    "INDONESIA", "IRAN", "IRAQ", "IRELAND", "ISRAEL", "ITALY", "JAMAICA",
    "JAPAN", "JORDAN", "KAZAKHSTAN", "KENYA", "KIRIBATI", "KOREA", "KUWAIT",
    "KYRGYZSTAN", "LAOS", "LATVIA", "LEBANON", "LESOTHO", "LIBERIA",
    "LIBYA", "LIECHTENSTEIN", "LITHUANIA", "LUXEMBOURG", "MADAGASCAR",
    "MALAWI", "MALAYSIA", "MALDIVES", "MALI", "MALTA", "MAURITANIA",
    "MAURITIUS", "MEXICO", "MICRONESIA", "MOLDOVA", "MONACO", "MONGOLIA",
    "MONTENEGRO", "MOROCCO", "MOZAMBIQUE", "MYANMAR", "NAMIBIA", "NAURU",
    "NEPAL", "NETHERLANDS", "NEWZEALAND", "NICARAGUA", "NIGER", "NIGERIA",
    "NORWAY", "OMAN", "PAKISTAN", "PALAU", "PANAMA", "PAPUA", "PARAGUAY",
    "PERU", "PHILIPPINES", "POLAND", "PORTUGAL", "QATAR", "ROMANIA",
    "RUSSIA", "RWANDA", "SAMOA", "SANMARINO", "SAUDIARABIA", "SENEGAL",
    "SERBIA", "SEYCHELLES", "SIERRALEONE", "SINGAPORE", "SLOVAKIA",
    "SLOVENIA", "SOLOMON", "SOMALIA", "SOUTHAFRICA", "SPAIN", "SRILANKA",
    "SUDAN", "SURINAME", "SWAZILAND", "SWEDEN", "SWITZERLAND", "SYRIA",
    "TAIWAN", "TAJIKISTAN", "TANZANIA", "THAILAND", "TOGO", "TONGA",
    "TRINIDAD", "TUNISIA", "TURKEY", "TURKMENISTAN", "TUVALU", "UGANDA",
    "UKRAINE", "UAE", "UK", "USA", "URUGUAY", "UZBEKISTAN", "VANUATU",
    "VATICAN", "VENEZUELA", "VIETNAM", "YEMEN", "ZAMBIA", "ZIMBABWE",
]

# Major cities
cities = [
    "TOKYO", "DELHI", "LONDON", "PARIS", "CAIRO", "LIMA", "ACCRA",
    "LAGOS", "NAIROBI", "DAKAR", "TEHRAN", "KABUL", "ADEN", "GOA",
    "MALI", "CHAD", "WALES", "OMAN", "SUDAN", "NIGER",
    "ROME", "OSLO", "BERN", "DOHA", "SUVA", "LOME",
    "RIYADH", "DUBAI", "MOSCOW", "BERLIN", "MADRID", "LISBON",
    "ATHENS", "VIENNA", "PRAGUE", "WARSAW", "BUCHAREST", "BUDAPEST",
    "STOCKHOLM", "HELSINKI", "OSLO", "COPENHAGEN", "DUBLIN", "EDINBURGH",
    "DIVO", "ARLES", "MACON", "LINCOLN", "BUFFALO", "CHICAGO",
]

all_locs = set(countries + cities)

for entry_name, length, fill in theme_entries:
    if fill:
        print(f"\n{entry_name} = {fill}:")
        for i in range(length):
            for j in range(i+3, length+1):
                substr = fill[i:j]
                if substr in all_locs:
                    print(f"  pos {i}-{j-1}: {substr} ★")

# Check CIRCLEABOUT
print("\nCIRCLEABOUT substrings that are locations:")
fill = "CIRCLEABOUT"
for i in range(len(fill)):
    for j in range(i+2, len(fill)+1):
        substr = fill[i:j]
        if substr in all_locs:
            print(f"  pos {i}-{j-1}: {substr} ★")

print()
print("=" * 70)
print("IMPORTANT REALIZATION")
print("=" * 70)
print("""
If 94A=CIRCLEABOUT and 167A=SUPERBOWLSTADIUM contain NO location names,
then the 11 locations must be distributed across the remaining 7 theme entries:
  25A (16), 50A (16), 73A (14), 114A (14), 138A (16), 19D (15), 78D (15)
  Total: 106 letters for 11 locations (~50 letters)

This works! 11 locations averaging ~4.5 letters each = ~50 letters hidden in
106 available letters. Some entries would have 2 locations, others 1.

Possible distribution (AROUNDWORLD):
  50A (16):  DAKAR (pos 9-13) + one more? TEHRAN (pos 6-11)? MALI (pos 9-12)?
  73A (14):  SUDAN (pos 1-5)? — but this is WEAK due to 67D constraint
  114A (14): DELHI (pos 8-12) + ADEN (pos 7-10)? — ADEN overlaps with DELHI!
  138A (16): TEHRAN (pos 3-8)? WALES (pos 1-5)?
  25A (16):  LAGOS? MALI? CHAD?
  19D (15):  GOA? OMAN? CHAD?
  78D (15):  GOA? OMAN? CHAD?

Some entries likely have 2 locations and some have 1.
With 11 locations in 7 entries: 4 entries with 2 + 3 entries with 1 = 11.
Or: 3 entries with 2 + 1 with 0 + 5 with 1 = 11.
""")

# Check: can ADEN and DELHI both be in 114A without overlapping?
print("Can ADEN + DELHI both fit in 114A (14 letters)?")
print("  114A known: pos 9=E, pos 13=E")
print("  DELHI at pos 8-12: D(8),E(9),L(10),H(11),I(12)")
print("  ADEN at pos 7-10: A(7),D(8),E(9),N(10)")
print("  OVERLAP at pos 8-9: ADEN gives D,E; DELHI gives D,E — MATCH! ✓")
print("  But ADEN[3]=N at pos 10, DELHI[2]=L at pos 10 — CONFLICT! ✗")
print("  They CANNOT both be at these positions simultaneously.")
print()
print("  Try ADEN elsewhere in 114A:")
print("  ADEN at pos 0-3: A(0),D(1),E(2),N(3) — no constraint conflicts ✓")
print("  ADEN at pos 3-6: A(3),D(4),E(5),N(6) — no constraint conflicts ✓")
print("  So ADEN + DELHI can coexist in 114A if ADEN is before pos 7.")
print()
print("  114A = ????ADEN?DELHIE or ADEN??????????E or ...ADEN...DELHIE")
print("  Interesting: if ADEN at pos 0-3 and DELHI at 8-12:")
print("  ADEN????DELHIE (14 letters)")
print("  This is a valid distribution!")
