#!/usr/bin/env python3
"""
AROUNDWORLD Staircase Solver

Theory: Column 4 of the staircase spells AROUNDWORLD (11 letters).
This echoes the 9-word sentence: "EVERY CHALLENGE LEADS TOWARDS LOCATION NAME SOMEWHERE AROUND WORLD"

For each row, we need a location name where the specific position = the target letter.
"""

from collections import defaultdict
import itertools

# Row definitions
ROWS = [
    (4, [3, 4, 5, 6]),       # Row 1
    (6, [1, 2, 3, 4, 5, 6]), # Row 2
    (5, [1, 2, 3, 4, 5]),    # Row 3
    (5, [3, 4, 5, 6, 7]),    # Row 4
    (4, [1, 2, 3, 4]),       # Row 5
    (4, [3, 4, 5, 6]),       # Row 6
    (5, [4, 5, 6, 7, 8]),    # Row 7
    (3, [3, 4, 5]),          # Row 8
    (5, [0, 1, 2, 3, 4]),    # Row 9
    (5, [2, 3, 4, 5, 6]),    # Row 10
    (4, [1, 2, 3, 4]),       # Row 11
]

COL4_POS = [row[1].index(4) for row in ROWS]
TARGET = "AROUNDWORLD"

# Expanded location database - include ALL types of geographic locations
LOCATIONS = {
    3: sorted(set([
        # Cities, regions, landmarks
        "RIO", "UFA", "HUE", "FEZ", "GOA", "LAE", "AGO",
        "NIS", "PAU", "SPA", "DAM", "AYR", "ELY", "RYE",
        "QOM", "ZUG", "JOS", "MEL", "BOA", "COS", "IOS",
        "URK", "MOB", "SAL", "ROM", "MAN", "PAN", "BOR",
        "POP", "DOS", "FOG", "HOG", "LOG", "NOB", "SOD",
        "SOS", "BOG", "COG", "DOG", "FOB", "HOB", "JOB",
        "LOB", "MOB", "NOD", "POD", "ROD", "SOB", "TOD",
    ])),
    4: sorted(set([
        # Sovereign nation capitals
        "DOHA", "SUVA", "LIMA", "BAKU", "ROME", "OSLO", "RIGA",
        "BERN", "LOME", "MALE", "APIA", "DILI", "KYIV", "SANA",
        "ADEN",
        # Former/notable capitals
        "BONN", "TROY", "NARA", "AGRA",
        # Countries
        "CHAD", "MALI", "CUBA", "IRAN", "IRAQ", "LAOS",
        "TOGO", "PERU", "OMAN", "FIJI", "NIUE",
        # Major world cities
        "NICE", "LYON", "BATH", "YORK", "CORK", "CEBU", "KOBE",
        "BARI", "COMO", "GRAZ", "LINZ", "BRNO", "PISA",
        "MESA", "RENO", "OMSK", "OULU", "PERM",
        "GIZA", "WACO", "ERIE", "ACRE", "EDFU",
        "JAVA", "OAHU", "CALI", "IPOH", "IASI", "PULA",
        "MOAB", "GARY", "YUMA", "ENID", "LODI",
        "GAZA", "IDLIB",  # 5
        # Key additions
        "ODER", "ADAK", "EDER",
    ])),
    5: sorted(set([
        # Sovereign nation capitals
        "ACCRA", "TOKYO", "PARIS", "CAIRO", "KABUL", "DHAKA",
        "HANOI", "MINSK", "SOFIA", "ABUJA", "QUITO", "SUCRE",
        "RABAT", "DAKAR", "TUNIS", "VADUZ", "PRAIA", "SANAA",
        "BERNE", "SEOUL", "DELHI",
        # US state capitals
        "DOVER", "BOISE", "SALEM",
        # Former/notable
        "CUSCO", "LHASA", "KYOTO", "LAGOS",
        # Major cities
        "DUBAI", "MIAMI", "TULSA", "OMAHA", "OSAKA", "BUSAN",
        "HAIFA", "IZMIR", "BURSA", "BASRA", "MOSUL", "MECCA",
        "DAVOS", "PETRA",
        # Countries/territories
        "CHILE", "CHINA", "EGYPT", "GHANA", "HAITI", "INDIA",
        "ITALY", "JAPAN", "KENYA", "KOREA", "LIBYA", "MALTA",
        "NAURU", "NEPAL", "NIGER", "PALAU", "QATAR", "SAMOA",
        "SPAIN", "SUDAN", "SYRIA", "TONGA", "WALES", "YEMEN",
        "BENIN", "GABON", "ARUBA", "MACAU",
        # Additional European cities
        "GENOA", "SIENA", "LUCCA", "PARMA", "PADUA", "PERTH",
        "NIMES", "DIJON", "REIMS", "TOURS",
        "KAZAN", "TURKU", "DELFT", "GHENT", "PORTO",
        # Key additions
        "WUHAN",  # China - W start!
    ])),
    6: sorted(set([
        # Sovereign nation capitals
        "LONDON", "BERLIN", "MOSCOW", "VIENNA", "LISBON", "DUBLIN",
        "ATHENS", "MADRID", "OTTAWA", "ANKARA", "TEHRAN", "WARSAW",
        "PRAGUE", "NASSAU", "RIYADH", "MUSCAT", "MANAMA", "LUSAKA",
        "MAPUTO", "BAMAKO", "BANJUL", "BISSAU", "HARARE", "KIGALI",
        "LUANDA", "MASERU", "HAVANA", "BOGOTA", "MANILA", "ASTANA",
        "TIRANA", "ZAGREB", "SKOPJE", "NIAMEY", "BANGUI", "ASMARA",
        "MORONI", "DODOMA", "MALABO", "ROSEAU", "TAIPEI", "THIMBU",
        # US state capitals
        "AUSTIN", "BOSTON", "DENVER", "HELENA", "JUNEAU", "TOPEKA",
        # Major cities
        "SYDNEY", "MUMBAI", "ZURICH", "GENEVA", "NAPLES", "VENICE",
        "MALAGA", "DALLAS", "FRESNO",
        "JEDDAH", "LAHORE", "PUEBLA", "MERIDA", "BRUGES", "GDANSK",
        # Countries
        "BRAZIL", "CANADA", "FRANCE", "GREECE", "ISRAEL", "JORDAN",
        "KUWAIT", "LATVIA", "MALAWI", "MEXICO", "MONACO", "NORWAY",
        "PANAMA", "POLAND", "RUSSIA", "SERBIA", "SWEDEN", "TURKEY",
        "ZAMBIA", "ANGOLA", "BHUTAN", "BRUNEI", "CYPRUS", "BELIZE",
        "GUYANA", "TUVALU",
    ])),
}

# Clean
for length in LOCATIONS:
    LOCATIONS[length] = sorted(set(
        w.upper() for w in LOCATIONS[length] if len(w.upper()) == length
    ))

print("="*60)
print(f"TARGET SPINE: {TARGET}")
print("="*60)

for row_idx in range(11):
    letter = TARGET[row_idx]
    length = ROWS[row_idx][0]
    pos = COL4_POS[row_idx]
    candidates = [w for w in LOCATIONS.get(length, []) if w[pos] == letter]
    print(f"\n  Row {row_idx+1} (len={length}): need letter[{pos}] = '{letter}'")
    print(f"    Candidates ({len(candidates)}): {candidates}")

# ============================================================
# CHECK ALL COLUMNS, not just column 4
# ============================================================
print("\n" + "="*60)
print("ALL COLUMN READINGS (which rows contribute to each column)")
print("="*60)

for col in range(9):
    contributing_rows = []
    for row_idx, (length, cols) in enumerate(ROWS):
        if col in cols:
            pos = cols.index(col)
            contributing_rows.append((row_idx, pos))
    if contributing_rows:
        rows_str = ", ".join(f"R{r+1}[{p}]" for r, p in contributing_rows)
        print(f"  Column {col}: {len(contributing_rows)} rows → {rows_str}")

# ============================================================
# FOR AROUNDWORLD: Find all valid location sets
# ============================================================
print("\n" + "="*60)
print("VALID LOCATION SETS FOR 'AROUNDWORLD'")
print("="*60)

# Get candidates per row
row_candidates = []
for row_idx in range(11):
    letter = TARGET[row_idx]
    length = ROWS[row_idx][0]
    pos = COL4_POS[row_idx]
    candidates = [w for w in LOCATIONS.get(length, []) if w[pos] == letter]
    row_candidates.append(candidates)

# Count total combinations
total = 1
for i, c in enumerate(row_candidates):
    total *= len(c)
    print(f"  Row {i+1}: {len(c)} options")
print(f"\n  Total combinations: {total:,}")

# Since total might be huge, let's check if additional columns constrain further
# Column 3 has 9 rows: 1,2,3,4,5,6,8,9,10
# Let's see what column 3 reads for each combination

print("\n" + "="*60)
print("COLUMN 3 ANALYSIS (9 of 11 rows)")
print("="*60)

col3_pos = {}
for row_idx, (length, cols) in enumerate(ROWS):
    if 3 in cols:
        col3_pos[row_idx] = cols.index(3)

col3_rows = sorted(col3_pos.keys())
print(f"  Rows in column 3: {[r+1 for r in col3_rows]}")

for row_idx in col3_rows:
    pos = col3_pos[row_idx]
    candidates = row_candidates[row_idx]
    letters = sorted(set(c[pos] for c in candidates))
    print(f"  Row {row_idx+1}: position {pos} → letters: {''.join(letters)}")
    for letter in letters:
        words = [c for c in candidates if c[pos] == letter]
        if len(words) <= 5:
            print(f"    [{letter}]: {words}")
        else:
            print(f"    [{letter}]: ({len(words)} options)")

# ============================================================
# MrBeast-RELEVANT location filtering
# ============================================================
print("\n" + "="*60)
print("MRBEAST-RELEVANT LOCATIONS FOR AROUNDWORLD")
print("="*60)

# Score locations by MrBeast relevance
MRBEAST_RELEVANT = {
    # Beast Philanthropy countries
    "MALI": 3, "CHAD": 3, "KENYA": 3, "GHANA": 3, "NIGER": 3,
    "EGYPT": 3, "INDIA": 3, "HAITI": 3, "NEPAL": 3, "SUDAN": 3,
    # Beast Philanthropy specific locations
    "ACCRA": 3, "CAIRO": 3, "DELHI": 3, "DHAKA": 3, "DAKAR": 3,
    "LAGOS": 3, "DUBAI": 3,
    # Countries where MrBeast operates
    "BRAZIL": 2, "MEXICO": 2, "JAPAN": 2, "KOREA": 2,
    "CANADA": 2, "FRANCE": 2, "RUSSIA": 2,
    # Beastland / business
    "RIYADH": 2, "MANILA": 2,
    # Puzzle-mentioned
    "LIMA": 2, "PERU": 2, "OMAN": 2,
    # General world locations (still valid "around the world")
    "WALES": 1, "ADEN": 1, "GOA": 1, "QOM": 1, "JOS": 1,
    "QATAR": 1, "DOVER": 1, "IZMIR": 1, "BAKU": 1,
    "TEHRAN": 2, "MADRID": 1, "CYPRUS": 1, "ZAGREB": 1,
    "WUHAN": 1,
}

print("\nBest candidates per row (sorted by MrBeast relevance):")
for row_idx in range(11):
    letter = TARGET[row_idx]
    candidates = row_candidates[row_idx]
    scored = [(MRBEAST_RELEVANT.get(c, 0), c) for c in candidates]
    scored.sort(reverse=True)
    print(f"\n  Row {row_idx+1} [{letter}]:")
    for score, word in scored[:8]:
        print(f"    {'★' * score if score else '·'} {word}")

# ============================================================
# ENUMERATE BEST SOLUTIONS
# ============================================================
print("\n" + "="*60)
print("TOP LOCATION SETS (MrBeast-relevant)")
print("="*60)

# For manageable enumeration, pick top-3 per row
top_per_row = []
for row_idx in range(11):
    candidates = row_candidates[row_idx]
    scored = [(MRBEAST_RELEVANT.get(c, 0), c) for c in candidates]
    scored.sort(reverse=True)
    top = [c for _, c in scored[:5]]
    top_per_row.append(top)

# Enumerate
best_solutions = []
for combo in itertools.product(*top_per_row):
    total_score = sum(MRBEAST_RELEVANT.get(c, 0) for c in combo)
    # Check no duplicates
    if len(set(combo)) == 11:
        best_solutions.append((total_score, combo))

best_solutions.sort(reverse=True)
print(f"\nFound {len(best_solutions)} unique solutions from top candidates")
for score, combo in best_solutions[:20]:
    print(f"\n  Score {score}:")
    for i, word in enumerate(combo):
        length = ROWS[i][0]
        pos = COL4_POS[i]
        # Show the word with the spine letter highlighted
        display = list(word)
        display[pos] = f"[{display[pos]}]"
        rel = MRBEAST_RELEVANT.get(word, 0)
        print(f"    Row {i+1:2d}: {''.join(display):12s} {'★'*rel if rel else ''}")

# ============================================================
# CHECK: What do OTHER columns spell in the best solution?
# ============================================================
print("\n" + "="*60)
print("CHECKING OTHER COLUMN READINGS FOR TOP SOLUTION")
print("="*60)

if best_solutions:
    _, top_sol = best_solutions[0]
    print(f"\nTop solution: {list(top_sol)}")

    for col in range(9):
        reading = []
        for row_idx, (length, cols) in enumerate(ROWS):
            if col in cols:
                pos = cols.index(col)
                reading.append(top_sol[row_idx][pos])
            else:
                reading.append('.')
        col_str = ''.join(reading)
        # Only show columns with 3+ letters
        actual_letters = col_str.replace('.', '')
        if len(actual_letters) >= 3:
            print(f"  Column {col}: {col_str} → '{actual_letters}'")

# Also try MRBEASTLAND
print("\n" + "="*60)
print("ALSO TESTING: MRBEASTLAND")
print("="*60)

TARGET2 = "MRBEASTLAND"
for row_idx in range(11):
    letter = TARGET2[row_idx]
    length = ROWS[row_idx][0]
    pos = COL4_POS[row_idx]
    candidates = [w for w in LOCATIONS.get(length, []) if w[pos] == letter]
    print(f"  Row {row_idx+1} [{letter}] (len={length}, pos={pos}): {len(candidates)} → {candidates[:6]}{'...' if len(candidates) > 6 else ''}")

# Try CIRCLEABOUT (the known crossword answer)
print("\n" + "="*60)
print("ALSO TESTING: CIRCLEABOUT")
print("="*60)

TARGET3 = "CIRCLEABOUT"
for row_idx in range(11):
    letter = TARGET3[row_idx]
    length = ROWS[row_idx][0]
    pos = COL4_POS[row_idx]
    candidates = [w for w in LOCATIONS.get(length, []) if w[pos] == letter]
    if candidates:
        print(f"  Row {row_idx+1} [{letter}]: {candidates[:5]}")
    else:
        print(f"  Row {row_idx+1} [{letter}]: ✗ NO OPTIONS")

# Try PHILANTHROPY (too long, 12), CHANGELIVES
print("\n" + "="*60)
print("ALSO TESTING: CHANGELIVES")
print("="*60)

TARGET4 = "CHANGELIVES"
for row_idx in range(11):
    letter = TARGET4[row_idx]
    length = ROWS[row_idx][0]
    pos = COL4_POS[row_idx]
    candidates = [w for w in LOCATIONS.get(length, []) if w[pos] == letter]
    if candidates:
        print(f"  Row {row_idx+1} [{letter}]: {candidates[:5]}")
    else:
        print(f"  Row {row_idx+1} [{letter}]: ✗ NO OPTIONS")
