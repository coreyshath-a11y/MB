#!/usr/bin/env python3
"""
Investigate 73A (14 letters, U at pos 2) and hidden location names in theme entries.
"""

import re

# ============================================================
# PART 1: What is 73A?
# ============================================================
print("=" * 70)
print("73A INVESTIGATION")
print("=" * 70)
print()
print("73A: row 9, cols 11-24, 14 letters")
print("Known constraints:")
print("  Position 2 (col 13): U (from ROTUNDA at 53D)")
print("  Position 13 (col 24): ? (end of row)")
print()

# What other constraints exist from down entries crossing 73A?
# 73A spans cols 11-24 at row 9
# Down entries that include row 9:
# - 46D: (5,11) len 6, rows 5-10. Row 9 = pos 4. 73A pos 0.
# - No entry at col 12 row 9 going down that starts before row 9?
#   Let me check: 67D starts at (8,12) - that's row 8. 67D pos 1 at row 9. 73A pos 1.
# - 53D: (6,13) len 7, rows 6-12. Row 9 = pos 3 = U (ROTUNDA). 73A pos 2 = U. Confirmed.
# - 39D: (4,14) len 4, rows 4-7. Doesn't reach row 9.
# - 74D: (9,14) len 6, starts at row 9. 73A pos 3 = 74D pos 0.
# - 75D: (9,15) len 5, starts at row 9. 73A pos 4 = 75D pos 0.
# - 27D: (2,15) len 6, rows 2-7. Doesn't reach row 9.
# - 33D: (3,16) len 3, rows 3-5. Doesn't reach row 9.
# - 60D: (7,16) len 3, rows 7-9. Row 9 = pos 2. 73A pos 5 = 60D pos 2.
# - 14D: (0,17) len 7, rows 0-6. Doesn't reach row 9.
# - 69D: (8,17) len 3, rows 8-10. Row 9 = pos 1. 73A pos 6 = 69D pos 1.
# - 55D: (6,18) len 6, rows 6-11. Row 9 = pos 3. 73A pos 7 = 55D pos 3.
# - 56D: (6,19) len 7, rows 6-12. Row 9 = pos 3. 73A pos 8 = 56D pos 3.
# - 16D: (0,19) len 5, rows 0-4. Doesn't reach row 9.
# - 76D: (9,20) len 5, starts at row 9. 73A pos 9 = 76D pos 0.
# - 40D: (4,20) len 4, rows 4-7. Doesn't reach row 9.
# - 49D: (5,21) len 5, rows 5-9. Row 9 = pos 4. 73A pos 10 = 49D pos 4.
# - 19D: (0,22) len 15, rows 0-14. Row 9 = pos 9. 73A pos 11 = 19D pos 9.
# - 20D: (0,23) len 6, rows 0-5. Doesn't reach row 9.
# - 62D: (7,23) len 8, rows 7-14. Row 9 = pos 2. 73A pos 12 = 62D pos 2.
# - 71D: (8,24) len 6, rows 8-13. Row 9 = pos 1. 73A pos 13 = 71D pos 1.
# - 21D: (0,24) len 6, rows 0-5. Doesn't reach row 9.

print("Down entries crossing 73A:")
print("  pos 0 (col 11): 46D pos 4 - unknown")
print("  pos 1 (col 12): 67D pos 1 - unknown")
print("  pos 2 (col 13): 53D pos 3 = U (ROTUNDA)")
print("  pos 3 (col 14): 74D pos 0 - unknown")
print("  pos 4 (col 15): 75D pos 0 - unknown")
print("  pos 5 (col 16): 60D pos 2 - unknown")
print("  pos 6 (col 17): 69D pos 1 - unknown")
print("  pos 7 (col 18): 55D pos 3 - unknown")
print("  pos 8 (col 19): 56D pos 3 - unknown")
print("  pos 9 (col 20): 76D pos 0 - unknown")
print("  pos 10 (col 21): 49D pos 4 - unknown")
print("  pos 11 (col 22): 19D pos 9 - unknown")
print("  pos 12 (col 23): 62D pos 2 - unknown")
print("  pos 13 (col 24): 71D pos 1 - unknown")
print()
print("Pattern: ??U???????????")
print()

# Also check: 72A at (9,3) len 6 = cols 3-8. Then black at (9,9) and (9,10).
# 73A starts at col 11. No overlap with 72A.

# What 14-letter words/phrases have U at position 2?
# The screenshot showed something like FOOTBALLSTANDS which has OO at pos 1-2
# But U at pos 2 is confirmed from ROTUNDA

# Let's think about Super Bowl themed 14-letter phrases:
candidates_73a = [
    # Super Bowl themed
    "TOUCHDOWNDANCE",   # T-O-U-C-H-D-O-W-N-D-A-N-C-E (U at pos 2!)
    "TOUCHDOWNPASSES",  # 15 letters, too long
    "TOUCHDOWNDRIVES",  # 15 letters, too long
    "FOURTHDOWNPLAY",   # F-O-U-R-T-H-D-O-W-N-P-L-A-Y (U at pos 2!)
    "FOURTHQUARTERS",   # F-O-U-R-T-H-Q-U-A-R-T-E-R-S (15, too long)
    "FOURTHQUARTER",    # 13 letters
    "COUCHPOTATOES",    # 13 letters
    "DOUBLEHEADERS",    # 13 letters
    "TROUBLEMAKERS",    # 13 letters
    "OUTSTANDINGLY",    # 13 letters
    "OUTPERFORMING",    # 13 letters
    "OUTOFBOUNDSPLAY",  # 15 letters
    "SUPERBOWLPARTY",   # 14! S-U-P-E-R-B-O-W-L-P-A-R-T-Y (U at pos 1!)
    "STUFFEDANIMALS",   # S-T-U-F-F-E-D-A-N-I-M-A-L-S (U at pos 2!)
    "TOUCHDOWNPASS",    # 13 letters
    "ROUGHHOUSINGG",    # no
    "FOURDOWNTEAMS",    # not a phrase
    "NUMBERONEFANS",    # N-U-M-B-E-R-O-N-E-F-A-N-S (13 letters)
    "OUTSTANDINGWIN",   # 14! O-U-T-S-T-A-N-D-I-N-G-W-I-N (U at pos 1!)
    "QUARTERFINALS",    # 13 letters
    "QUARTERBACKED",    # 13 letters
    "OUTFOXEDAGAIN",    # 13 letters
    "PUBLICADDRESS",    # P-U-B-L-I-C-A-D-D-R-E-S-S (13 letters)
    "SUPERBOWLRING",    # 13 letters
    "FULLCOURTPRESS",   # 14! F-U-L-L-C-O-U-R-T-P-R-E-S-S (U at pos 1!)
    "TOUCHDOWNSCORE",   # 14! T-O-U-C-H-D-O-W-N-S-C-O-R-E (U at pos 2!)
    "DOUBLEOVERTIME",   # 14! D-O-U-B-L-E-O-V-E-R-T-I-M-E (U at pos 2!)
    "TOURNAMENTPLAY",   # 14! T-O-U-R-N-A-M-E-N-T-P-L-A-Y (U at pos 2!)
    "COUNTDOWNCLOCK",   # 14! C-O-U-N-T-D-O-W-N-C-L-O-C-K (U at pos 2!)
    "ROUGHANDTUMBLE",   # 14! R-O-U-G-H-A-N-D-T-U-M-B-L-E (U at pos 2!)
    "FOURTHDOWNKICK",   # 14! F-O-U-R-T-H-D-O-W-N-K-I-C-K (U at pos 2!)
    "TOUCHDOWNRULES",   # 14! T-O-U-C-H-D-O-W-N-R-U-L-E-S (U at pos 2!)
    "TOUCHDOWNTRICK",   # 14!
    "SOURPUSSFACES",    # 13 letters
    "BOUNDARYLINES",    # 13 letters
    "OUTOFTHISWORLD",   # 14! O-U-T-O-F-T-H-I-S-W-O-R-L-D (U at pos 1!)
    "YOUTUBEVIDEOS",    # 13 letters
    "YOUTUBESTADIUM",   # 14! Y-O-U-T-U-B-E-S-T-A-D-I-U-M (U at pos 2!)
    "OUTOFTHISWORLD",   # already listed
    "DOUBLEJEOPARDY",   # 14! D-O-U-B-L-E-J-E-O-P-A-R-D-Y (U at pos 2!)
    "FOUNDINGFATHER",    # 14!
    "TROUBLESHOOTS",    # 13
    "BOUNDLESSREACH",   # 14!
    "JOURNEYTOWARD",    # 13
]

# Filter to exactly 14 letters with U at position 2
print("14-letter candidates with U at position 2:")
print("-" * 60)
for c in candidates_73a:
    c_clean = c.replace(" ", "").upper()
    if len(c_clean) == 14 and c_clean[2] == 'U':
        # Check: also needs to NOT have certain letters at known crossing positions
        print(f"  {c_clean}")

# Also try from /usr/share/dict/words
print()
print("Searching dictionary for 14-letter words with U at position 2...")
try:
    with open('/usr/share/dict/words', 'r') as f:
        words = [w.strip().upper() for w in f if len(w.strip()) == 14]

    u_at_2 = [w for w in words if len(w) == 14 and w[2] == 'U']
    print(f"Found {len(u_at_2)} dictionary words of length 14 with U at pos 2:")
    for w in sorted(u_at_2):
        print(f"  {w}")
except Exception as e:
    print(f"Error: {e}")

# ============================================================
# PART 2: Hidden Location Names in Theme Entries
# ============================================================
print()
print("=" * 70)
print("HIDDEN LOCATION NAMES IN THEME ENTRIES")
print("=" * 70)
print()

# The 167A clue says: "What this puzzle commemorates in eleven hidden words in theme entries"
# 167A = SUPERBOWLSTADIUM
# So: 11 location names are hidden as substrings within the theme entries
# Theme entries: 25A, 50A, 73A, 94A, 114A, 138A, 167A, 19D, 78D

# Known theme entry text:
theme_entries = {
    "94A": "CIRCLEABOUT",
    "167A": "SUPERBOWLSTADIUM",
    "149A": "BEASTLAND",  # not a theme entry but long
}

# What locations could be hidden?
# From AROUNDWORLD staircase theory: MALI, TEHRAN, LAGOS, SUDAN, OMAN, ADEN, WALES, GOA, NIGER, DELHI, CHAD
# Plus many other world locations

# Comprehensive location database
locations = [
    # Countries
    "AFGHANISTAN", "ALBANIA", "ALGERIA", "ANDORRA", "ANGOLA", "ARGENTINA", "ARMENIA",
    "AUSTRALIA", "AUSTRIA", "AZERBAIJAN", "BAHAMAS", "BAHRAIN", "BANGLADESH", "BARBADOS",
    "BELARUS", "BELGIUM", "BELIZE", "BENIN", "BHUTAN", "BOLIVIA", "BOSNIA", "BOTSWANA",
    "BRAZIL", "BRUNEI", "BULGARIA", "BURKINAFASO", "BURUNDI", "CAMBODIA", "CAMEROON",
    "CANADA", "CHAD", "CHILE", "CHINA", "COLOMBIA", "COMOROS", "CONGO", "COSTARICA",
    "CROATIA", "CUBA", "CYPRUS", "CZECH", "DENMARK", "DJIBOUTI", "DOMINICA",
    "ECUADOR", "EGYPT", "ELSALVADOR", "ERITREA", "ESTONIA", "ETHIOPIA", "FIJI",
    "FINLAND", "FRANCE", "GABON", "GAMBIA", "GEORGIA", "GERMANY", "GHANA", "GREECE",
    "GRENADA", "GUATEMALA", "GUINEA", "GUYANA", "HAITI", "HONDURAS", "HUNGARY",
    "ICELAND", "INDIA", "INDONESIA", "IRAN", "IRAQ", "IRELAND", "ISRAEL", "ITALY",
    "JAMAICA", "JAPAN", "JORDAN", "KAZAKHSTAN", "KENYA", "KIRIBATI", "KOREA",
    "KUWAIT", "KYRGYZSTAN", "LAOS", "LATVIA", "LEBANON", "LESOTHO", "LIBERIA",
    "LIBYA", "LIECHTENSTEIN", "LITHUANIA", "LUXEMBOURG", "MADAGASCAR", "MALAWI",
    "MALAYSIA", "MALDIVES", "MALI", "MALTA", "MAURITANIA", "MAURITIUS", "MEXICO",
    "MOLDOVA", "MONACO", "MONGOLIA", "MONTENEGRO", "MOROCCO", "MOZAMBIQUE", "MYANMAR",
    "NAMIBIA", "NAURU", "NEPAL", "NETHERLANDS", "NEWZEALAND", "NICARAGUA", "NIGER",
    "NIGERIA", "NORWAY", "OMAN", "PAKISTAN", "PALAU", "PALESTINE", "PANAMA", "PARAGUAY",
    "PERU", "PHILIPPINES", "POLAND", "PORTUGAL", "QATAR", "ROMANIA", "RUSSIA",
    "RWANDA", "SAMOA", "SANMARINO", "SAUDIARABIA", "SENEGAL", "SERBIA", "SEYCHELLES",
    "SIERRALEONE", "SINGAPORE", "SLOVAKIA", "SLOVENIA", "SOMALIA", "SOUTHAFRICA",
    "SPAIN", "SRILANKA", "SUDAN", "SURINAME", "SWEDEN", "SWITZERLAND", "SYRIA",
    "TAIWAN", "TAJIKISTAN", "TANZANIA", "THAILAND", "TOGO", "TONGA", "TRINIDAD",
    "TUNISIA", "TURKEY", "TURKMENISTAN", "TUVALU", "UGANDA", "UKRAINE",
    "UAE", "UK", "USA", "URUGUAY", "UZBEKISTAN", "VANUATU", "VATICAN",
    "VENEZUELA", "VIETNAM", "YEMEN", "ZAMBIA", "ZIMBABWE",
    # Major cities
    "LONDON", "PARIS", "TOKYO", "DELHI", "MUMBAI", "BEIJING", "CAIRO", "LAGOS",
    "ISTANBUL", "KARACHI", "DHAKA", "MOSCOW", "SAOPAULO", "LIMA", "BANGKOK",
    "SEOUL", "NAIROBI", "BOGOTA", "BAGHDAD", "RIYADH", "SANTIAGO", "SYDNEY",
    "BERLIN", "MADRID", "ROME", "DUBLIN", "OSLO", "ATHENS", "VIENNA", "PRAGUE",
    "WARSAW", "BUCHAREST", "BUDAPEST", "LISBON", "AMSTERDAM", "BRUSSELS",
    "COPENHAGEN", "HELSINKI", "STOCKHOLM", "REYKJAVIK", "BERN", "ZURICH",
    "TEHRAN", "KABUL", "DAKAR", "ACCRA", "ABUJA", "KINSHASA", "ADDISABABA",
    "KHARTOUM", "ADEN", "DOHA", "MUSCAT", "MANAMA", "AMMAN", "BEIRUT",
    "DAMASCUS", "ANKARA", "TBILISI", "YEREVAN", "BAKU", "TASHKENT", "ASTANA",
    "ULAANBAATAR", "HANOI", "MANILA", "JAKARTA", "KUALALUMPUR", "SINGAPORE",
    "WELLINGTON", "CANBERRA", "OTTAWA", "MEXICOCITY", "HAVANA", "KINGSTON",
    "BOGOTA", "QUITO", "LAPAZ", "BRASILIA", "BUENOSAIRES", "MONTEVIDEO",
    "ASUNCION", "GEORGETOWN", "PARAMARIBO", "CAYENNE",
    # US cities from P4
    "TOLEDO", "DENVER", "REGINA", "TORONTO", "OWENSBORO", "ROSWELL", "DRESDEN",
    "TEMPE", "SEVILLE", "OTTAWA", "ROCHESTER", "ORLANDO", "WOODWAY", "AUBURN",
    "DOVER", "ANNAPOLIS", "ADELAIDE", "SANJUAN", "WILMINGTON", "SACRAMENTO",
    # Regions/areas
    "WALES", "SCOTLAND", "CORNWALL", "CATALONIA", "BAVARIA", "TUSCANY",
    "SIBERIA", "SAHARA", "GOBI", "ARABIA", "PERSIA",
    # Small notable places
    "GOA", "BALI", "FIJI", "GUAM", "NIUE", "TONGA",
]

# Remove duplicates
locations = list(set(locations))

print("Searching for hidden location names in known theme entries...")
print()

for entry_name, entry_text in theme_entries.items():
    print(f"\n--- {entry_name}: {entry_text} ---")
    found = []
    for loc in locations:
        if len(loc) >= 3 and loc in entry_text:
            found.append(loc)
    if found:
        found.sort(key=lambda x: (-len(x), x))
        for loc in found:
            idx = entry_text.index(loc)
            print(f"  FOUND: {loc} at positions {idx}-{idx+len(loc)-1}")
    else:
        print("  No location names found as substrings")

# ============================================================
# PART 3: What locations COULD be hidden in partially-known entries?
# ============================================================
print()
print("=" * 70)
print("POTENTIAL HIDDEN LOCATIONS IN PARTIAL THEME ENTRIES")
print("=" * 70)

# For each theme entry, what locations could fit given known letters?
partial_themes = {
    "25A": {"len": 16, "known": {}},  # completely unknown
    "50A": {"len": 16, "known": {10: 'A', 13: 'R'}},  # DAKAR hypothesis
    "73A": {"len": 14, "known": {2: 'U'}},
    "114A": {"len": 14, "known": {8: 'E', 12: 'E'}},  # pos 8=col8=E(TRITE), pos 12=...
    # Actually let me recheck 114A constraints
    # 114A at (15,0) len 14, cols 0-13
    # 87D at (11,9) len 5 = TRITE. Rows 11-15. At row 15 = pos 4 = E. Col 9, 114A pos 9 = E.
    # 110D at (14,13) len 6 = DENVER. Rows 14-19. At row 15 = pos 1 = E. Col 13, 114A pos 13 = E.
    # 115D at (15,3) len 5. 114A pos 3 = 115D pos 0.
    # So 114A: pos 9 = E (from TRITE), pos 13 = E (from DENVER)
    "138A": {"len": 16, "known": {4: 'E'}},  # pos 4 from DENVER? Let me check.
    # 138A at (18,9) len 16, cols 9-24
    # DENVER at 110D (14,13) len 6, rows 14-19. Row 18 = pos 4 = E. Col 13. 138A pos = 13-9 = 4. So 138A pos 4 = E.
    # Actually wait: 138A starts at col 9. Col 13 = pos 4. Yes.
    # ORGANIC at 104D (13,18) len 7, rows 13-19. Row 18 = pos 5 = I. Col 18. 138A pos = 18-9 = 9. So 138A pos 9 = I (if ORGANIC correct).
    "19D": {"len": 15, "known": {}},  # completely unknown
    "78D": {"len": 15, "known": {}},  # completely unknown
}

# Fix 114A
partial_themes["114A"]["known"] = {9: 'E', 13: 'E'}

# Fix 138A
partial_themes["138A"]["known"] = {4: 'E'}  # and pos 9 = I if ORGANIC

print()
for entry_name, info in partial_themes.items():
    length = info["len"]
    known = info["known"]
    pattern = ['?'] * length
    for pos, letter in known.items():
        pattern[pos] = letter
    pattern_str = ''.join(pattern)

    print(f"\n--- {entry_name} ({length} letters): {pattern_str} ---")

    # For each location, check if it could be hidden somewhere in this entry
    possible = []
    for loc in locations:
        if len(loc) < 3 or len(loc) > length:
            continue
        # Try each starting position
        for start in range(length - len(loc) + 1):
            fits = True
            for i, ch in enumerate(loc):
                pos = start + i
                if pos in known and known[pos] != ch:
                    fits = False
                    break
            if fits:
                possible.append((loc, start, start + len(loc) - 1))

    # Group by location, show unique positions
    from collections import defaultdict
    loc_positions = defaultdict(list)
    for loc, s, e in possible:
        loc_positions[loc].append((s, e))

    # Sort by location length (longer = more interesting)
    sorted_locs = sorted(loc_positions.items(), key=lambda x: (-len(x[0]), x[0]))

    # Only show locations 3+ letters
    count = 0
    for loc, positions in sorted_locs:
        if len(loc) >= 4:  # Focus on 4+ letter locations
            for s, e in positions:
                # Show which known letters overlap
                overlaps = [(p, known[p]) for p in range(s, e+1) if p in known]
                overlap_str = f" (matches: {overlaps})" if overlaps else ""
                print(f"  {loc} at pos {s}-{e}{overlap_str}")
                count += 1
    if count == 0:
        for loc, positions in sorted_locs[:20]:
            for s, e in positions:
                overlaps = [(p, known[p]) for p in range(s, e+1) if p in known]
                overlap_str = f" (matches: {overlaps})" if overlaps else ""
                print(f"  {loc} at pos {s}-{e}{overlap_str}")

# ============================================================
# PART 4: If AROUNDWORLD locations must appear in theme entries,
# which theme entry hosts which location?
# ============================================================
print()
print("=" * 70)
print("AROUNDWORLD LOCATION ASSIGNMENT TO THEME ENTRIES")
print("=" * 70)
print()

aw_locations = ["MALI", "TEHRAN", "LAGOS", "SUDAN", "OMAN", "ADEN", "WALES", "GOA", "NIGER", "DELHI", "CHAD"]

print("If these 11 locations must be hidden in 9 theme entries:")
print(f"Locations: {aw_locations}")
print()
print("Total theme entry characters available:")
themes_info = [
    ("25A", 16), ("50A", 16), ("73A", 14), ("94A", 11),
    ("114A", 14), ("138A", 16), ("167A", 16), ("19D", 15), ("78D", 15)
]
total_chars = sum(t[1] for t in themes_info)
print(f"  9 entries × varying lengths = {total_chars} total characters")
total_loc_chars = sum(len(loc) for loc in aw_locations)
print(f"  11 locations total {total_loc_chars} characters")
print()

# Check known entries for locations
print("Known entries - location check:")
known_themes = {
    "94A": "CIRCLEABOUT",
    "167A": "SUPERBOWLSTADIUM",
}

for name, text in known_themes.items():
    print(f"\n  {name} = {text}:")
    for loc in aw_locations:
        if loc in text:
            idx = text.index(loc)
            print(f"    CONTAINS: {loc} at pos {idx}-{idx+len(loc)-1}")
    # Also check all locations
    any_found = False
    for loc in locations:
        if len(loc) >= 3 and loc in text:
            idx = text.index(loc)
            print(f"    contains: {loc} at pos {idx}-{idx+len(loc)-1}")
            any_found = True
    if not any_found:
        print(f"    No locations found!")

# ============================================================
# PART 5: Could SUPERBOWLSTADIUM contain a location?
# ============================================================
print()
print("=" * 70)
print("DETAILED SUBSTRING ANALYSIS OF SUPERBOWLSTADIUM")
print("=" * 70)
text = "SUPERBOWLSTADIUM"
print(f"\nText: {text}")
print(f"All substrings of length 3-8:")
for length in range(3, 9):
    for start in range(len(text) - length + 1):
        sub = text[start:start+length]
        print(f"  [{start}:{start+length}] = {sub}")

# Check each against ALL known world locations
print()
print("Location substrings found:")
all_world_locs = set()
# Add a very comprehensive set
for loc in locations:
    all_world_locs.add(loc)

# Add more obscure locations
more_locs = [
    "STAD", "BOWL", "SUPER", "OWL", "PERU", "LSTAD", "UBER", "STADI",
    "PERB", "WLST", "ERBOW", "PERBOWL", "BOWLS", "OWLS", "ADIUM",
    "DIUM", "TADI", "TADIUM", "STAD", "ERB", "OWL", "TAD",
    "LSTA", "WLSTA", "STADIU", "UPERB", "RBOW", "BOWLST",
    # Real but obscure places
    "UBER", "SUEZ", "OWL",  # Owl is a place?
    "TULUM", "DIUMA", "PERBO",
]

for loc in all_world_locs:
    if len(loc) >= 3 and loc in text:
        idx = text.index(loc)
        print(f"  MATCH: {loc} at positions {idx}-{idx+len(loc)-1}")

# What about CIRCLEABOUT?
print()
print("=" * 70)
print("DETAILED SUBSTRING ANALYSIS OF CIRCLEABOUT")
print("=" * 70)
text2 = "CIRCLEABOUT"
for loc in all_world_locs:
    if len(loc) >= 3 and loc in text2:
        idx = text2.index(loc)
        print(f"  MATCH: {loc} at positions {idx}-{idx+len(loc)-1}")
print("  (CABO could be hidden if: CIR-C-A-B-O-UT → but CABO = positions 3-6? C-A-B-O = CABO!)")
if "CABO" in text2:
    print("  YES! CABO is at positions 3-6 in CIRCLEABOUT!")
else:
    # Manual check: CIRCLEABOUT[3:7] = C,L,E,A... no that's not CABO
    for i in range(len(text2) - 3):
        sub = text2[i:i+4]
        if sub == "CABO":
            print(f"  CABO at position {i}")
    print("  CABO is NOT a contiguous substring of CIRCLEABOUT")
    # But what if we consider: CIRCLEABOUT
    # C-I-R-C-L-E-A-B-O-U-T
    # LEA = a place? LEA is a meadow but also some places
    # BOUT = not a place
    # ABLE? A-B... not contiguous as ABLE
    print()
    print("  All length-3+ substrings:")
    for length in range(3, min(8, len(text2)+1)):
        for start in range(len(text2) - length + 1):
            sub = text2[start:start+length]
            print(f"    [{start}:{start+length}] = {sub}")

# ============================================================
# PART 6: BEASTLAND analysis
# ============================================================
print()
print("=" * 70)
print("BEASTLAND SUBSTRING ANALYSIS")
print("=" * 70)
text3 = "BEASTLAND"
for loc in all_world_locs:
    if len(loc) >= 3 and loc in text3:
        idx = text3.index(loc)
        print(f"  MATCH: {loc} at positions {idx}-{idx+len(loc)-1}")

print()
print("DONE!")
