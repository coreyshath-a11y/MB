#!/usr/bin/env python3
"""
Staircase Spine Solver - Independent Rows Theory

If the 11 staircase rows are INDEPENDENT (no cell sharing), then the visual
layout creates "columns" where you can read letters downward. Column 4 passes
through ALL 11 rows, creating an 11-letter message.

For each row, the letter at column 4 comes from a specific position in the word:
  Row 1 (cols 3-6):    word[1] → col 4
  Row 2 (cols 1-6):    word[3] → col 4
  Row 3 (cols 1-5):    word[3] → col 4
  Row 4 (cols 3-7):    word[1] → col 4
  Row 5 (cols 1-4):    word[3] → col 4
  Row 6 (cols 3-6):    word[1] → col 4
  Row 7 (cols 4-8):    word[0] → col 4
  Row 8 (cols 3-5):    word[1] → col 4
  Row 9 (cols 0-4):    word[4] → col 4
  Row 10 (cols 2-6):   word[2] → col 4
  Row 11 (cols 1-4):   word[3] → col 4
"""

from collections import defaultdict

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

# Column 4 position within each word
COL4_POS = [row[1].index(4) for row in ROWS]
print("Column 4 extraction positions:")
for i, (length, cols) in enumerate(ROWS):
    pos = COL4_POS[i]
    print(f"  Row {i+1:2d} ({length} letters, cols {cols}): word[{pos}] → col 4")

# Comprehensive world capital/location database
# Focus on sovereign nation capitals, US state capitals, and MrBeast-relevant cities
LOCATIONS = {
    3: sorted(set([
        "RIO", "UFA", "HUE", "FEZ", "GOA", "LAE", "AGO",
        "NIS", "PAU", "SPA", "DAM", "AYR", "ELY", "RYE",
        "QOM", "ZUG", "JOS", "MEL",
    ])),
    4: sorted(set([
        # Sovereign capitals
        "DOHA", "SUVA", "LIMA", "BAKU", "ROME", "OSLO", "RIGA",
        "BERN", "LOME", "MALE", "APIA", "DILI", "KYIV", "SANA",
        "ADEN",
        # Former/notable capitals
        "BONN", "TROY", "NARA", "AGRA",
        # US State capitals (none are 4 letters)
        # Major cities / MrBeast-related
        "NICE", "LYON", "BATH", "YORK", "CORK", "CEBU", "KOBE",
        "BARI", "COMO", "GRAZ", "LINZ", "BRNO", "PISA",
        "MESA", "RENO", "OMSK", "OULU", "PERM",
        "GIZA", "WACO", "ERIE", "ACRE", "FIJI",
        "JAVA", "OAHU", "CALI", "IPOH", "IASI", "PULA",
        "MOAB", "GARY", "YUMA", "ENID", "LODI",
        "CHAD", "MALI", "CUBA", "IRAN", "IRAQ", "LAOS",
        "TOGO", "PERU", "OMAN", "GAZA", "NIUE",
    ])),
    5: sorted(set([
        # Sovereign capitals
        "ACCRA", "TOKYO", "PARIS", "CAIRO", "KABUL", "DHAKA",
        "HANOI", "MINSK", "SOFIA", "ABUJA", "QUITO", "SUCRE",
        "RABAT", "DAKAR", "TUNIS", "VADUZ", "PRAIA", "SANAA",
        "BERNE", "SEOUL", "DELHI",
        # US state capitals
        "DOVER", "BOISE", "SALEM",
        # Former/notable
        "CUSCO", "LHASA", "KYOTO", "LAGOS",
        # Major cities / MrBeast-related
        "DUBAI", "MIAMI", "TULSA", "OMAHA", "OSAKA", "BUSAN",
        "HAIFA", "IZMIR", "BURSA", "BASRA", "MOSUL", "MECCA",
        "DAVOS", "PETRA",
        # Country names that are locations
        "CHILE", "CHINA", "EGYPT", "GHANA", "HAITI", "INDIA",
        "ITALY", "JAPAN", "KENYA", "KOREA", "LIBYA", "MALTA",
        "NAURU", "NEPAL", "NIGER", "PALAU", "QATAR", "SAMOA",
        "SPAIN", "SUDAN", "SYRIA", "TONGA", "WALES", "YEMEN",
        # Additional
        "BENIN", "GABON", "ARUBA", "MACAU",
        "GENOA", "SIENA", "LUCCA", "PARMA", "PADUA", "PERTH",
        "NIMES", "DIJON", "REIMS", "TOURS",
        "KAZAN", "MALMÖ", "TURKU", "DELFT", "GHENT", "PORTO",
    ])),
    6: sorted(set([
        # Sovereign capitals
        "LONDON", "BERLIN", "MOSCOW", "VIENNA", "LISBON", "DUBLIN",
        "ATHENS", "MADRID", "OTTAWA", "ANKARA", "TEHRAN", "WARSAW",
        "PRAGUE", "NASSAU", "RIYADH", "MUSCAT", "MANAMA", "LUSAKA",
        "MAPUTO", "BAMAKO", "BANJUL", "BISSAU", "HARARE", "KIGALI",
        "LUANDA", "MASERU", "HAVANA", "BOGOTA", "MANILA", "ASTANA",
        "TIRANA", "ZAGREB", "SKOPJE", "NIAMEY", "BANGUI", "ASMARA",
        "MORONI", "DODOMA", "MALABO", "ROSEAU", "TAIPEI", "THIMBU",
        # US state capitals
        "AUSTIN", "BOSTON", "DENVER", "HELENA", "JUNEAU", "TOPEKA",
        # Former/notable
        "YANGON", "DARWIN", "HOBART", "TOLEDO", "REGINA",
        # Major cities / MrBeast-related
        "SYDNEY", "MUMBAI", "ZURICH", "GENEVA", "NAPLES", "VENICE",
        "MALAGA", "DALLAS", "FRESNO", "AUBURN",
        "JEDDAH", "LAHORE", "PUEBLA", "MERIDA", "BRUGES", "GDANSK",
        "ODESSA",
        # Countries
        "BRAZIL", "CANADA", "FRANCE", "GREECE", "ISRAEL", "JORDAN",
        "KUWAIT", "LATVIA", "MALAWI", "MEXICO", "MONACO", "NORWAY",
        "PANAMA", "POLAND", "RUSSIA", "SERBIA", "SWEDEN", "TURKEY",
        "TUVALU", "ZAMBIA", "BRUNEI", "BHUTAN", "CYPRUS", "BELIZE",
        "GUYANA", "ANGOLA",
    ])),
}

# Clean
for length in LOCATIONS:
    LOCATIONS[length] = sorted(set(
        w.upper() for w in LOCATIONS[length] if len(w.upper()) == length
    ))

# Build letter→words map for each row's col4 position
row_by_letter = []
for row_idx in range(11):
    length = ROWS[row_idx][0]
    pos = COL4_POS[row_idx]
    letter_map = defaultdict(list)
    for word in LOCATIONS.get(length, []):
        letter_map[word[pos]].append(word)
    row_by_letter.append(letter_map)
    letters_available = sorted(letter_map.keys())
    print(f"\nRow {row_idx+1} (len={length}, col4 at word[{pos}]): {len(letters_available)} possible letters")
    for letter in letters_available:
        words = letter_map[letter]
        if len(words) <= 8:
            print(f"  {letter}: {words}")
        else:
            print(f"  {letter}: ({len(words)} options) {words[:5]}...")

# ============================================================
# TRY KNOWN 11-LETTER PHRASES
# ============================================================
print("\n" + "="*60)
print("TESTING KNOWN 11-LETTER PHRASES AS COLUMN 4 SPINE")
print("="*60)

target_phrases = [
    "CHANGELIVES",  # MrBeast's mission
    "MRBEASTTEAM",  # His team
    "CHANGETHEM",   # 10 - skip
    "SALSFORCEMB",  # 11 but unlikely
    "SALESFORCES",  # 11
    "PHILANTHROP",  # 11 (philanthropist minus last 2)
    "BESTCHANNEL",  # 11
    "WORLDIMPACT",  # 11
    "CHANGEDWRLD",  # 11
    "JIMMYDONALS",  # 11
    "BEASTLYLAND",  # 11
    "GREENVILLEN",  # 11
    "MRBEASTRULZ",  # 11
    "AROUNDWORLD",  # 11
    "CELEBRATION",  # 11
    "COMPETITION",  # 11
    "COOPERATION",  # 11
    "INSPIRATION",  # 11
    "MILLIONAIRE",  # 11
    "ACHIEVEMENT",  # 11
    "EXPLORATION",  # 11
    "OPPORTUNITY",  # 11
    "IMAGINATION",  # 11
    "RECOGNITION",  # 11
    "GENEROUSITY",  # 11
    "MRBEASTLAND",  # 11
    "MRBESTVIRAL",  # 11
    "SLACKMEBEAS",  # 11
    "DONALDSLAND",  # 11
    "JIMMYDWORLD",  # 11
    "CIRCLEABOUT",  # 11 - the puzzle answer!
    "GLOBETROTER",  # 11
    "JIMMYBEAST" + "S",  # 11
    "SUPERBOWLAD",  # 11
    "BEASTNATION",  # 11
    "CHANGINGWOR",  # 11
]

for phrase in target_phrases:
    if len(phrase) != 11:
        continue
    phrase = phrase.upper()
    possible = True
    choices = []
    for row_idx in range(11):
        letter = phrase[row_idx]
        options = row_by_letter[row_idx].get(letter, [])
        if not options:
            possible = False
            break
        choices.append((letter, options))

    if possible:
        print(f"\n  ✓ '{phrase}' IS POSSIBLE!")
        for row_idx, (letter, options) in enumerate(choices):
            if len(options) <= 5:
                print(f"    Row {row_idx+1}: need [{letter}] → {options}")
            else:
                print(f"    Row {row_idx+1}: need [{letter}] → ({len(options)} options) {options[:4]}...")
    # Only show near-misses
    elif choices:
        missing_at = len(choices)
        missing_letter = phrase[missing_at]
        # print(f"  ✗ '{phrase}' fails at Row {missing_at+1}: no words with [{missing_letter}] at position {COL4_POS[missing_at]}")

# ============================================================
# BRUTE FORCE: What 11-letter strings CAN column 4 spell?
# ============================================================
print("\n" + "="*60)
print("ALL POSSIBLE LETTERS AT EACH ROW'S COLUMN 4 POSITION")
print("="*60)

possible_letters = []
for row_idx in range(11):
    letters = sorted(row_by_letter[row_idx].keys())
    possible_letters.append(set(letters))
    print(f"  Row {row_idx+1}: {letters} ({len(letters)} options)")

# Show which letters are available at ALL rows (could appear anywhere)
common = possible_letters[0]
for s in possible_letters[1:]:
    common = common & s
print(f"\n  Letters available at ALL 11 rows: {sorted(common)}")

# ============================================================
# CHECK: Can we spell things related to MrBeast locations?
# ============================================================
print("\n" + "="*60)
print("CHECKING MRBEAST-THEMED 11-LETTER TARGETS")
print("="*60)

# Given the 11 locations/dates and MrBeast theme, what 11-letter messages make sense?
# Let's try all dictionary words of length 11
try:
    import nltk
    nltk.download('words', quiet=True)
    from nltk.corpus import words
    all_words_11 = [w.upper() for w in words.words() if len(w) == 11]
    print(f"\n11-letter English words: {len(all_words_11)}")

    valid_spine_words = []
    for word in all_words_11:
        possible = True
        for row_idx in range(11):
            letter = word[row_idx]
            if letter not in row_by_letter[row_idx]:
                possible = False
                break
        if possible:
            valid_spine_words.append(word)

    print(f"11-letter words that CAN be spelled on column 4: {len(valid_spine_words)}")
    if valid_spine_words:
        # Score by relevance to MrBeast/philanthropy/puzzle
        keywords = ["CHANGE", "BEAST", "WORLD", "JIMMY", "MILLION", "PHILANT",
                    "CHALLENGE", "GIVE", "HELP", "EXPLORE", "GLOBAL", "CELEB",
                    "ACHIEV", "AWARD", "DONAT", "CHARIT", "IMPACT", "INSPIR"]
        scored = []
        for word in valid_spine_words:
            score = sum(1 for kw in keywords if kw in word)
            scored.append((score, word))
        scored.sort(reverse=True)

        print("\n  Top relevant matches:")
        for score, word in scored[:50]:
            if score > 0:
                print(f"    [{score}] {word}")

        print("\n  All valid words (first 100):")
        for word in sorted(valid_spine_words)[:100]:
            print(f"    {word}")

except ImportError:
    print("NLTK not available, skipping dictionary check")

# ============================================================
# ALSO CHECK: What if we use ONLY actual capitals?
# ============================================================
print("\n" + "="*60)
print("STRICT CAPITALS ONLY - SPINE ANALYSIS")
print("="*60)

STRICT_CAPITALS = {
    3: ["RIO", "UFA", "HUE", "FEZ", "GOA"],
    4: ["DOHA", "SUVA", "LIMA", "BAKU", "ROME", "OSLO", "RIGA",
        "BERN", "LOME", "MALE", "APIA", "DILI", "KYIV", "SANA", "ADEN",
        # Include countries too
        "CHAD", "MALI", "CUBA", "IRAN", "IRAQ", "LAOS",
        "TOGO", "PERU", "OMAN", "FIJI", "NIUE"],
    5: ["ACCRA", "TOKYO", "PARIS", "CAIRO", "KABUL", "DHAKA",
        "HANOI", "MINSK", "SOFIA", "ABUJA", "QUITO", "SUCRE",
        "RABAT", "DAKAR", "TUNIS", "VADUZ", "PRAIA", "SANAA",
        "BERNE", "SEOUL", "DELHI", "DOVER", "BOISE", "SALEM",
        "LHASA", "CUSCO", "KYOTO", "LAGOS",
        # Countries
        "CHILE", "CHINA", "EGYPT", "GHANA", "HAITI", "INDIA",
        "ITALY", "JAPAN", "KENYA", "KOREA", "LIBYA", "NEPAL",
        "NIGER", "QATAR", "SAMOA", "SPAIN", "SUDAN", "SYRIA",
        "TONGA", "WALES", "YEMEN", "BENIN", "GABON", "NAURU",
        "PALAU", "MALTA"],
    6: ["LONDON", "BERLIN", "MOSCOW", "VIENNA", "LISBON", "DUBLIN",
        "ATHENS", "MADRID", "OTTAWA", "ANKARA", "TEHRAN", "WARSAW",
        "PRAGUE", "NASSAU", "RIYADH", "MUSCAT", "MANAMA", "LUSAKA",
        "MAPUTO", "BAMAKO", "BANJUL", "BISSAU", "HARARE", "KIGALI",
        "LUANDA", "MASERU", "HAVANA", "BOGOTA", "MANILA", "ASTANA",
        "TIRANA", "ZAGREB", "SKOPJE", "NIAMEY", "BANGUI", "ASMARA",
        "MORONI", "DODOMA", "MALABO", "ROSEAU", "TAIPEI", "THIMBU",
        "AUSTIN", "BOSTON", "DENVER", "HELENA", "JUNEAU", "TOPEKA",
        # Countries
        "BRAZIL", "CANADA", "FRANCE", "GREECE", "ISRAEL", "JORDAN",
        "KUWAIT", "LATVIA", "MALAWI", "MEXICO", "NORWAY", "PANAMA",
        "POLAND", "RUSSIA", "SWEDEN", "TURKEY", "ZAMBIA", "ANGOLA",
        "SERBIA", "CYPRUS", "BELIZE", "GUYANA", "TUVALU", "BRUNEI",
        "BHUTAN", "MONACO"],
}

for length in STRICT_CAPITALS:
    STRICT_CAPITALS[length] = sorted(set(
        w.upper() for w in STRICT_CAPITALS[length] if len(w.upper()) == length
    ))

strict_row_by_letter = []
for row_idx in range(11):
    length = ROWS[row_idx][0]
    pos = COL4_POS[row_idx]
    letter_map = defaultdict(list)
    for word in STRICT_CAPITALS.get(length, []):
        letter_map[word[pos]].append(word)
    strict_row_by_letter.append(letter_map)
    letters_available = sorted(letter_map.keys())
    print(f"  Row {row_idx+1}: letters possible: {''.join(letters_available)}")

# Check which 11-letter words can be spelled with STRICT capitals only
print("\n  Checking 11-letter words with strict capitals...")
if 'all_words_11' in dir():
    strict_valid = []
    for word in all_words_11:
        possible = True
        for row_idx in range(11):
            letter = word[row_idx]
            if letter not in strict_row_by_letter[row_idx]:
                possible = False
                break
        if possible:
            strict_valid.append(word)
    print(f"  11-letter words possible with strict capitals: {len(strict_valid)}")
    for word in sorted(strict_valid)[:100]:
        print(f"    {word}")
