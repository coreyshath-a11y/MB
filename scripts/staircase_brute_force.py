#!/usr/bin/env python3
"""
Staircase Grid Brute Force Solver
MrBeast Million Dollar Puzzle Hunt

Exhaustively searches for valid location sets that fit the 11-row staircase grid.
Tests AROUNDWORLD, MELANESIANS, and unconstrained column-4 spines.
Also cross-references locations against known theme entries for substring matches.
"""

import itertools
import sys
from collections import defaultdict

# ============================================================
# STAIRCASE GRID DEFINITION (confirmed from HTML + pixel analysis)
# ============================================================
# (row_number, start_col, word_length)
LAYOUT = [
    (1, 3, 4),   # Row 1:  cols 3,4,5,6     → 4 letters
    (2, 1, 6),   # Row 2:  cols 1,2,3,4,5,6 → 6 letters
    (3, 1, 5),   # Row 3:  cols 1,2,3,4,5   → 5 letters
    (4, 3, 5),   # Row 4:  cols 3,4,5,6,7   → 5 letters
    (5, 1, 4),   # Row 5:  cols 1,2,3,4     → 4 letters
    (6, 3, 4),   # Row 6:  cols 3,4,5,6     → 4 letters
    (7, 4, 5),   # Row 7:  cols 4,5,6,7,8   → 5 letters
    (8, 3, 3),   # Row 8:  cols 3,4,5       → 3 letters
    (9, 0, 5),   # Row 9:  cols 0,1,2,3,4   → 5 letters
    (10, 2, 5),  # Row 10: cols 2,3,4,5,6   → 5 letters
    (11, 1, 4),  # Row 11: cols 1,2,3,4     → 4 letters
]

SPINE_COL = 4  # Column 4 is the spine

# Compute word lengths and col4 position within each word
WORD_LENGTHS = [length for _, _, length in LAYOUT]
COL4_POSITIONS = [SPINE_COL - start_col for _, start_col, length in LAYOUT]

print("=" * 80)
print("STAIRCASE GRID BRUTE FORCE SOLVER")
print("=" * 80)
print(f"\nWord lengths:      {WORD_LENGTHS}")
print(f"Col4 positions:    {COL4_POSITIONS}")
print(f"  (Position within each word where the spine letter appears)")
print()

# Verify column 4 positions
for i, (row, start_col, length) in enumerate(LAYOUT):
    pos = COL4_POSITIONS[i]
    assert 0 <= pos < length, f"Row {row}: col4 pos {pos} out of range for length {length}"
    print(f"  Row {row:2d}: {length}-letter word, cols {start_col}-{start_col+length-1}, "
          f"col4 = word[{pos}]")

# ============================================================
# COMPREHENSIVE LOCATION DATABASE
# All world countries, capitals, major cities, regions, territories
# organized by string length (3-6 letters)
# ============================================================

LOCATIONS_BY_LENGTH = {
    3: sorted(set("""
        GOA UFA HUE FEZ PAU AYR ELY RYE QOM ZUG JOS MEL NIS SPA
        DAM AGO LAE GAP AIX SAL ICA ADO ABA OYO OWO UYO EDO SUE
        CIV URN QAT TAR RIO GAN LUZ NHA CAN DAX PAL BOA ILO
    """.split())),

    4: sorted(set("""
        DOHA SUVA LIMA BAKU ROME OSLO RIGA BERN LOME MALE APIA DILI
        KYIV SANA ADEN BONN TROY NARA AGRA NICE LYON BATH YORK CORK
        CEBU KOBE BARI COMO GRAZ LINZ BRNO PISA MESA RENO OMSK OULU
        PERM GIZA WACO ERIE ACRE JAVA OAHU CALI IPOH IASI PULA MOAB
        GARY YUMA ENID LODI CHAD MALI CUBA IRAN IRAQ LAOS TOGO PERU
        OMAN GAZA NIUE FIJI TYRE SIWA ASIR WADI DIRE ADIS HOMS SFAX
        ORAN FARO LUGO VIGO GENT METZ KIEL LUND BODO ASTI LUCA TULA
        IRUN RUSE SION THUN ALES ARTH BRIG EGER GYÖR PECS TATA NOWY
        LODZ OLOT BODO BIEL BALE BRIG CHUR FADO NYON YALA ABHA JISR
        ACRE AKKO BEER HAIF HAIL HAMA KRAK LAMU MALA MBAN MUNH PORT
        ONDO ORON OSUN WARI YOLA EKET EKET IDAH ISAN MUBI ORON OTTA
        BIDA ZARI BAMA GAYA KANO KEBI KIRU KOGI ABOH EDEA BUEA MONG
        WUMS BATA BATA OYEM BATA MOYO FORT GULU JUBA WAUS MITU TANA
        TENA OLOT IBIS ALAN AVON VALE DEAL HOVE HULL BURY DISS ROSS
        WARK WICK ALVA DUNS MUIR NIGG OBAN DYCE ELBA ELBE HAIN TARN
        OISE EYRE ARAL GOBI ALPS ETNA ELAM SIAM NUUK YUMA FUJI NILE
        ELBE NEVA ODER AMUR DNPR OREL TVER GORI BAKU GIFU NAHA GUMI
        JEJU INSA SUWN GUAM WAKE MAUI
    """.split())),

    5: sorted(set("""
        ACCRA TOKYO PARIS CAIRO KABUL DHAKA HANOI MINSK SOFIA ABUJA
        QUITO SUCRE RABAT DAKAR TUNIS VADUZ PRAIA SANAA BERNE SEOUL
        DELHI DOVER BOISE SALEM CUSCO LHASA KYOTO LAGOS DUBAI MIAMI
        TULSA OMAHA OSAKA BUSAN HAIFA IZMIR BURSA BASRA MOSUL MECCA
        DAVOS PETRA CHILE CHINA EGYPT GHANA HAITI INDIA ITALY JAPAN
        KENYA KOREA LIBYA MALTA NAURU NEPAL NIGER PALAU QATAR SAMOA
        SPAIN SUDAN SYRIA TONGA WALES YEMEN BENIN GABON ARUBA MACAU
        GENOA SIENA LUCCA PARMA PADUA PERTH NIMES DIJON REIMS TOURS
        KAZAN TURKU DELFT GHENT PORTO NATAL BAHIA BELEM GOIAS TIKSI
        PSKOV LIPSK TOMSK CHITA PENZA KURSK SAROV TUMEN SOCHI ANAPA
        TUAPSE DERBENT ELISTA TYMEN PITER PARAN TACNA
        MOSUL ERBIL AMMAN MUSQT JEDDH TABUK AQABA EILAT ASWAN
        LUXOR HURGH IBIZA CADIZ JEREZ GIJON OVIEDO VIANA SETUBAL EVORA
        BRAGA NAMUR LIEGE ARLON MAINZ TRIER BOZEN AOSTA LECCE UDINE
        PARMA RIMNI LUCCA SIENA PRATO AREZO TRENT PLZEN BRAHA KOSIC
        PRJOV POPRD BANSK NITRA TRNAV ZELIN TARTU VILNA GOMEL BREST
        GRODE MOGTL VITEB PINSK ORSHA BABIA BRASL RECIF MACEA MANAU
        CUIAB CAMPO TERES NATAL BELML PASSO TAUBE NATAL CUIAB LONDR
        CAMPI OLIND JUIZD TAMPE TALLA SAVAN AUROR PLAIN CEDAR LARGO
        AKRON FLINT IRVIN PLANO LAIRD FRISK BOISE PROVO OGDEN WUHAN
        HEFEI JINAN XIANG LHASA NANJG GUIYN ZIGNG LANZU XANTH SUYNG
        LUOYN DAQNG TULOU FOSHA SHAOG SHENZ TAWAN KUNMG NANNNG
        LIUZU ZHUHA PUTIA ZHANJ MAOMG BAODI YANGZ WULUQ KASHI
        DEHRA PATNA SURAT THANE PUNE  VISAKHAPATNAM
        ABUJA ENUGU WARRI AKURE EKITI ASABA LAFIA MINNA YENAG SAPEL
        OKENE OFFA  LOKJA KONTN OGBMS BADGR IJEBU IJERO OSOGB SAGAM
        IKARE IKIRUN ILESA ILOBI AKOKO IKIRI OKITB AKOKO AKURE
        MAKRD AWEIL KASLA EDAMR KADUL SENNAR WADDM DAMAZN GENDA
        ARISH TANTA BENHA QWESN ISMLA ASWAN LUXOR MINIA ASYUT SUHAG
        ACCRA KUMSI TAMLE SUNYA CAPEC TAKOR BOLGA HOMOBWE
        COTONOU ABOMEY DJOUGOU PARAKOU KANDI NATITING LOKOSSA
        BOUAK DALOA SANPD KORHO YAMSK ODIEN GAGNOA DUEKUE MAND
        LAMIN SEREK BASSE BRIKA KUNTD JANJG FARAM KERWA BANJL
        KIDAL BAMAK TIMBC MOPTI KAYES SEGU GOUNDAM NIONO DJENNE BANAMBA
        KAOLACK THIES ZIGUINCHOR MBOUR DIOURBEL TAMBACOUNDA KEDOUGOU
        LOUGA MATAM FATCK KAFFR
        ACCRA LAGOS ADDIS NAIROBI ABIDJAN DAKAR KAMPALA LUSAKA HARARE
        MAPUTO LUANDA KIGALI LILONGWE FREETOWN CONAKRY MONROVIA
        BAMAK OUAGA NIAME BANJU CONTO ABOMEY LOMEL PORTO MALABO
        LIBRE MORONI ANTANANARIVO DODOMA GABORONE MASERU MBABANE
        WINDHOEK ASMARA DJIBOUTI MOGADISHU JUBA BANGUI NDJAMENA
        NIAMEY BRAZZAVILLE KINSHASA
    """.split())),

    6: sorted(set("""
        LONDON BERLIN MOSCOW VIENNA LISBON DUBLIN ATHENS MADRID OTTAWA
        ANKARA TEHRAN WARSAW PRAGUE NASSAU RIYADH MUSCAT MANAMA LUSAKA
        MAPUTO BAMAKO BANJUL BISSAU HARARE KIGALI LUANDA MASERU HAVANA
        BOGOTA MANILA ASTANA TIRANA ZAGREB SKOPJE NIAMEY BANGUI ASMARA
        MORONI DODOMA MALABO ROSEAU TAIPEI THIMBU AUSTIN BOSTON DENVER
        HELENA JUNEAU TOPEKA YANGON DARWIN HOBART TOLEDO REGINA SYDNEY
        MUMBAI ZURICH GENEVA NAPLES VENICE MALAGA DALLAS FRESNO AUBURN
        JEDDAH LAHORE PUEBLA MERIDA BRUGES GDANSK ODESSA BRAZIL CANADA
        FRANCE GREECE ISRAEL JORDAN KUWAIT LATVIA MALAWI MEXICO MONACO
        NORWAY PANAMA POLAND RUSSIA SERBIA SWEDEN TURKEY TUVALU ZAMBIA
        BRUNEI BHUTAN CYPRUS BELIZE GUYANA ANGOLA GUINEA DANZIG LUBECK
        ERFURT ROSTOV SAMARA KALUGA TAMBOV KURGAN TYUMEN SURGUT BARNAUL
        ABAKAN RYAZAN ORYOL PSKOV LIPETSK SMOLENSK KALININGRAD
        BELGOROD ULYANOVSK PERM SARANSK CHEBOKSARY YOSHKAR KIROV
        IZHEVSK ORENBG
        MOMBSA KISUMU NAKURU ELDORT NYERIA THIKA GARISS KAKAMG KIAMBU
        NAIVSH NANYUK EMBU MERU KITALE BUNGMA BUSIA HOMABY MIGRI KERCH
        SIAYA VIHIGA TURKNA BARINGO ELGEYO KERICHO BOMET KISII NYAMRA
        SAIMIA GARSEN MALIND KILIFI KWALE LAMU MARIAKANI GEDE WATAMU
        IBADAN KADUNA ILORIN BENIN AGBARA MUSHIN SURULR SHOMOL AGEGE
        OSHOGB IJESHA ILESHA ILARE AKOKO ILAWE IKIRUN
        CAIRNS HOBART DARWIN BROOME ALICE PERTH MACKAY WHYALL CEDUNA
        ALBANY COLLIE NARROG DUBBO WAGGA ALBURY GOULBN ORANGE TAMWTH
        GRAFTN LISMORE CASINO BALLNA COOLAB GYMPIE CALOUNDR IPSWICH
    """.split())),
}

# Clean up: ensure each word matches its expected length, uppercase, no dupes
for length in list(LOCATIONS_BY_LENGTH.keys()):
    cleaned = sorted(set(
        w.upper().strip() for w in LOCATIONS_BY_LENGTH[length]
        if len(w.strip()) == length and w.strip().isalpha()
    ))
    LOCATIONS_BY_LENGTH[length] = cleaned

# Print database stats
print("\n" + "=" * 80)
print("LOCATION DATABASE STATS")
print("=" * 80)
for length in sorted(LOCATIONS_BY_LENGTH.keys()):
    print(f"  {length}-letter locations: {len(LOCATIONS_BY_LENGTH[length])}")
total = sum(len(v) for v in LOCATIONS_BY_LENGTH.values())
print(f"  TOTAL: {total} locations")


# ============================================================
# HELPER: Build index of locations by (length, position, letter)
# ============================================================
def build_index(locations_by_length):
    """Build lookup: (length, position, letter) -> list of matching locations."""
    index = defaultdict(list)
    for length, words in locations_by_length.items():
        for word in words:
            for pos, letter in enumerate(word):
                index[(length, pos, letter)].append(word)
    return index

LOC_INDEX = build_index(LOCATIONS_BY_LENGTH)


# ============================================================
# PART 1: AROUNDWORLD THEORY
# ============================================================
def find_valid_sets_for_spine(spine_word, label=""):
    """Find ALL sets of 11 locations that spell the given spine word down column 4."""
    assert len(spine_word) == 11, f"Spine word must be 11 characters, got {len(spine_word)}"

    print(f"\n{'=' * 80}")
    print(f"SPINE THEORY: {spine_word} {label}")
    print(f"{'=' * 80}")

    # For each row, find all candidate locations
    candidates_per_row = []
    for row_idx in range(11):
        row_num, start_col, length = LAYOUT[row_idx]
        col4_pos = COL4_POSITIONS[row_idx]
        target_letter = spine_word[row_idx]

        candidates = LOC_INDEX.get((length, col4_pos, target_letter), [])
        candidates_per_row.append(candidates)

        print(f"  Row {row_num:2d} (len={length}, word[{col4_pos}]={target_letter}): "
              f"{len(candidates)} candidates", end="")
        if len(candidates) <= 15:
            print(f" → {candidates}")
        else:
            print(f" → {candidates[:10]}... (+{len(candidates)-10} more)")

    # Check if any row has zero candidates
    for row_idx in range(11):
        if len(candidates_per_row[row_idx]) == 0:
            row_num = LAYOUT[row_idx][0]
            length = WORD_LENGTHS[row_idx]
            target = spine_word[row_idx]
            print(f"\n  *** IMPOSSIBLE: Row {row_num} needs a {length}-letter location "
                  f"with '{target}' at position {COL4_POSITIONS[row_idx]} - NONE FOUND ***")
            return candidates_per_row, []

    # Compute total number of combinations
    total_combos = 1
    for c in candidates_per_row:
        total_combos *= len(c)
    print(f"\n  Total possible combinations: {total_combos:,}")

    # If small enough, enumerate all combinations
    if total_combos <= 50_000_000:
        # Enumerate with pruning
        all_sets = list(itertools.product(*candidates_per_row))
        print(f"  Enumerated {len(all_sets):,} combinations")

        # For display, limit to first 50
        if len(all_sets) > 50:
            print(f"\n  Showing first 50 of {len(all_sets):,} valid sets:")
            for i, combo in enumerate(all_sets[:50]):
                print(f"    Set {i+1}: {list(combo)}")
            print(f"    ... and {len(all_sets) - 50:,} more")
        else:
            print(f"\n  ALL {len(all_sets)} valid sets:")
            for i, combo in enumerate(all_sets):
                print(f"    Set {i+1}: {list(combo)}")

        return candidates_per_row, all_sets
    else:
        print(f"  Too many combinations to enumerate. Showing candidates per row only.")
        return candidates_per_row, None


print("\n")
print("#" * 80)
print("# PART 1: AROUNDWORLD THEORY")
print("#" * 80)
aw_candidates, aw_sets = find_valid_sets_for_spine("AROUNDWORLD", "(primary theory)")


print("\n")
print("#" * 80)
print("# PART 2: MELANESIANS THEORY")
print("#" * 80)
mel_candidates, mel_sets = find_valid_sets_for_spine("MELANESIANS", "(community theory)")


# ============================================================
# PART 3: UNCONSTRAINED BRUTE FORCE
# ============================================================
print("\n")
print("#" * 80)
print("# PART 3: UNCONSTRAINED COLUMN-4 ANALYSIS")
print("#" * 80)
print("For each row, which letters are possible at the col4 position?")
print("Then: which 11-letter strings can column 4 spell?")

possible_letters_per_row = []
letter_to_candidates = []  # For each row: dict letter -> [locations]

for row_idx in range(11):
    row_num, start_col, length = LAYOUT[row_idx]
    col4_pos = COL4_POSITIONS[row_idx]

    letter_map = defaultdict(list)
    for word in LOCATIONS_BY_LENGTH.get(length, []):
        letter_at_col4 = word[col4_pos]
        letter_map[letter_at_col4].append(word)

    available_letters = sorted(letter_map.keys())
    possible_letters_per_row.append(set(available_letters))
    letter_to_candidates.append(letter_map)

    print(f"\n  Row {row_num:2d} (len={length}, col4=word[{col4_pos}]): "
          f"{''.join(available_letters)} ({len(available_letters)} letters)")
    for letter in available_letters:
        count = len(letter_map[letter])
        examples = letter_map[letter][:8]
        if count <= 8:
            print(f"    {letter}: {examples}")
        else:
            print(f"    {letter}: ({count} locs) {examples}...")

# Now test every possible 11-letter combination of letters
# Since each row typically has ~15-20 letters, that's ~20^11 = too many
# Instead, let's check known meaningful 11-letter strings

print("\n" + "-" * 80)
print("CHECKING ALL 11-LETTER ENGLISH WORDS AGAINST LOCATION DATABASE")
print("-" * 80)

# Try to use nltk words corpus, then /usr/share/dict/words
eleven_letter_words = []
try:
    import nltk
    nltk.download('words', quiet=True)
    from nltk.corpus import words as nltk_words
    eleven_letter_words = [w.upper() for w in nltk_words.words()
                           if len(w) == 11 and w.isalpha()]
    eleven_letter_words = sorted(set(eleven_letter_words))
    print(f"  Found {len(eleven_letter_words)} 11-letter words from NLTK corpus")
except (ImportError, LookupError):
    try:
        with open('/usr/share/dict/words', 'r') as f:
            for line in f:
                word = line.strip().upper()
                if len(word) == 11 and word.isalpha():
                    eleven_letter_words.append(word)
        print(f"  Found {len(eleven_letter_words)} 11-letter words in dictionary")
    except FileNotFoundError:
        print("  No dictionary found, using built-in list only")

# Additional 11-letter strings to test (MrBeast/puzzle themed)
custom_spines = [
    "AROUNDWORLD",
    "MELANESIANS",
    "CHANGELIVES",
    "CELEBRATION",
    "COMPETITION",
    "MRBEASTLAND",
    "EXPLORATION",
    "INSPIRATION",
    "ACHIEVEMENT",
    "RECOGNITION",
    "COOPERATION",
    "IMAGINATION",
    "OPPORTUNITY",
    "MILLIONAIRE",
    "INFORMATION",
    "APPLICATION",
    "DECLARATION",
    "DESTRUCTION",
    "COMBINATION",
    "CIRCULATION",
    "COMPOSITION",
    "CORRELATION",
    "DESTINATION",
    "EDUCATIONAL",
    "ELIMINATION",
    "FABRICATION",
    "FASCINATION",
    "IMPLICATION",
    "INTEGRATION",
    "OBSERVATION",
    "ORIENTATION",
    "PREPARATION",
    "PUBLICATION",
    "RESTAURANTS",
    "TERMINATION",
    "UNDERGROUND",
    "CELEBRATION",
    "BENEFACTION",
    "MRBEASTVLOG",
    "SUPERBOWLAD",
    "BEASTNATION",
    "DONALDWORLD",
    "JIMMYBEASTS",
    "CHANGINGWRD",
    "WORLDCHANGE",
    "SALESFORCEX",
    "GLOBALREACH",
    "WORLDTOURED",
    "WORLDSAPART",
    "CIRCUITRYDE",
    "PHILANTROPY",
    "CIRCUMWORLD",
]

all_candidates_to_test = list(set(eleven_letter_words + custom_spines))
print(f"  Testing {len(all_candidates_to_test)} candidate spine words...")

valid_spines = []
for spine in all_candidates_to_test:
    if len(spine) != 11:
        continue
    spine = spine.upper()

    feasible = True
    min_options = float('inf')
    total_options = 1

    for row_idx in range(11):
        letter = spine[row_idx]
        options = letter_to_candidates[row_idx].get(letter, [])
        if not options:
            feasible = False
            break
        min_options = min(min_options, len(options))
        total_options *= len(options)

    if feasible:
        valid_spines.append((spine, min_options, total_options))

# Sort by total_options (fewer = more constrained = more interesting)
valid_spines.sort(key=lambda x: x[2])

print(f"\n  Found {len(valid_spines)} feasible spine words")
print(f"\n  TOP 50 MOST CONSTRAINED feasible spines (fewest total combos):")
for i, (spine, min_opt, total_opt) in enumerate(valid_spines[:50]):
    marker = ""
    if spine == "AROUNDWORLD":
        marker = " <<<< PRIMARY THEORY"
    elif spine == "MELANESIANS":
        marker = " <<<< COMMUNITY THEORY"
    elif any(kw in spine for kw in ["BEAST", "JIMMY", "WORLD", "CHANGE", "GIVE",
                                      "HELP", "PHILANT", "GLOBAL", "MILLION"]):
        marker = " * thematic"
    print(f"    {i+1:3d}. {spine}  (min_opts={min_opt}, total_combos={total_opt:,}){marker}")

# Show all thematic matches
print(f"\n  ALL THEMATICALLY RELEVANT feasible spines:")
thematic_keywords = ["BEAST", "JIMMY", "WORLD", "CHANGE", "GIVE", "HELP",
                     "PHILANT", "GLOBAL", "MILLION", "AROUND", "CIRCLE",
                     "CHALLENGE", "SUPER", "DONAT", "CHARIT", "IMPACT",
                     "INSPIR", "EXPLOR", "CELEB", "AWARD", "GENER"]
thematic_spines = [(s, m, t) for s, m, t in valid_spines
                   if any(kw in s for kw in thematic_keywords)]
for spine, min_opt, total_opt in thematic_spines:
    print(f"    {spine}  (combos={total_opt:,})")


# ============================================================
# PART 4: CROSS-REFERENCE WITH THEME ENTRIES
# ============================================================
print("\n")
print("#" * 80)
print("# PART 4: CROSS-REFERENCE LOCATIONS WITH THEME ENTRIES")
print("#" * 80)

# Known and candidate theme entry answers
THEME_ENTRIES = {
    "94A (11, CONFIRMED)": "CIRCLEABOUT",
    "25A (16, UNKNOWN)": None,
    "50A (16, partial)": None,   # known: pos10=A, pos13=R
    "73A (14, partial)": None,   # known: pos2=U
    "114A (14, partial)": None,  # known: pos9=E, pos13=E
    "138A (16, partial)": None,  # known: pos4=E
    "167A (16, UNKNOWN)": None,
    "19D (15, UNKNOWN)": None,
    "78D (15, UNKNOWN)": None,
}

# Candidate answers for 167A
CANDIDATE_167A = [
    "CHANGINGTHEWORLD",
    "ACTSOFGENEROSITY",
    "GLOBALCHALLENGES",
    "HELPINGTHEPLANET",
    "WORLDWIDEIMPACTS",
    "GLOBALADVENTURES",
    "AROUNDTHEWORLDIN",
    "SUPERBOWLSTADIUM",
    "CHARITYCHALLENGE",
    "TENTHANNIVERSARY",
]

print("\nAll locations in our database (all lengths):")
all_locations = []
for length, locs in sorted(LOCATIONS_BY_LENGTH.items()):
    all_locations.extend(locs)
all_locations = sorted(set(all_locations))
print(f"  Total unique locations: {len(all_locations)}")

print("\n" + "-" * 80)
print("SUBSTRING SEARCH: Which locations appear inside known theme entries?")
print("-" * 80)

def find_hidden_locations(entry_answer, entry_label, min_len=3):
    """Find all locations that appear as substrings in the entry answer."""
    if not entry_answer:
        return []

    answer = entry_answer.upper()
    found = []

    for loc in all_locations:
        if len(loc) < min_len:
            continue
        if loc in answer and loc != answer:
            # Find position
            pos = answer.index(loc)
            found.append((loc, pos, pos + len(loc) - 1))

    if found:
        print(f"\n  {entry_label} = {answer}")
        for loc, start, end in sorted(found, key=lambda x: (-len(x[0]), x[1])):
            # Show the location highlighted in context
            before = answer[:start]
            match = answer[start:end+1]
            after = answer[end+1:]
            fits_staircase = "YES" if len(loc) in WORD_LENGTHS else "no"
            print(f"    [{loc}] at pos {start}-{end} (len={len(loc)}, "
                  f"staircase fit: {fits_staircase}): {before}[{match}]{after}")
    else:
        print(f"\n  {entry_label} = {answer}: NO locations found as substrings")

    return found

# Check the confirmed entry
find_hidden_locations("CIRCLEABOUT", "94A (confirmed)")

# Check 167A candidates
print("\n" + "-" * 80)
print("167A CANDIDATES - Location substrings")
print("-" * 80)
for candidate in CANDIDATE_167A:
    find_hidden_locations(candidate, f"167A candidate: {candidate}")

# Also check some other possible theme answers
print("\n" + "-" * 80)
print("ADDITIONAL THEME ENTRY CANDIDATES - Location substrings")
print("-" * 80)

additional_entries = [
    ("BEASTPHILANTHROPY", "167A alt"),  # 17 letters - too long but check
    ("WORLDRECORDVIDEO", "167A alt"),
    ("GLOBALPHILANTHRO", "167A alt"),
    ("CHANGINGTHEWORLD", "167A prime"),
    ("PHILANTHROPIST", "114A candidate"),
    ("ROMANTICCOMEDY", "114A candidate"),
    ("FORMALDEHYDE", "unknown theme"),
    ("NORMALIZEDATA", "unknown theme"),
    ("ROMANEMPIRE", "unknown theme"),
    ("SUPERBOWLWINNER", "unknown theme"),
    ("SUPERBOWLCHAMPS", "unknown theme"),
    ("CHANGINGOFGUARD", "unknown theme"),
    ("CHANGINGTHETIDE", "unknown theme"),
    ("OPERATINGBUDGET", "unknown theme"),
    ("CAPITALCITYNAME", "unknown theme"),
]

for answer, label in additional_entries:
    if len(answer) in [11, 14, 15, 16]:  # theme entry lengths
        find_hidden_locations(answer, f"{label} ({len(answer)})")


# ============================================================
# PART 5: ADJACENT ROW OVERLAP ANALYSIS
# ============================================================
print("\n")
print("#" * 80)
print("# PART 5: ADJACENT ROW COLUMN OVERLAPS")
print("#" * 80)
print("If rows SHARE cells (original theory), which columns overlap?")
print("Even if rows are independent, this shows visual alignment.\n")

for i in range(len(LAYOUT) - 1):
    row1, start1, len1 = LAYOUT[i]
    row2, start2, len2 = LAYOUT[i + 1]
    end1 = start1 + len1 - 1
    end2 = start2 + len2 - 1

    shared_start = max(start1, start2)
    shared_end = min(end1, end2)

    if shared_start <= shared_end:
        shared_cols = list(range(shared_start, shared_end + 1))
        # Position within each word
        pos1 = [c - start1 for c in shared_cols]
        pos2 = [c - start2 for c in shared_cols]
        print(f"  R{row1}-R{row2}: shared cols {shared_cols}")
        print(f"    R{row1} positions: {pos1}, R{row2} positions: {pos2}")

        if 4 in shared_cols:
            print(f"    *** Col 4 (spine) is shared between these rows ***")
    else:
        print(f"  R{row1}-R{row2}: NO overlap")


# ============================================================
# PART 6: ALL COLUMNS READING FOR AROUNDWORLD SET
# ============================================================
print("\n")
print("#" * 80)
print("# PART 6: COLUMN READINGS FOR TOP AROUNDWORLD CANDIDATES")
print("#" * 80)

# The "best" AROUNDWORLD set from the analysis file
best_aw_set = ['MALI', 'TEHRAN', 'LAGOS', 'SUDAN', 'OMAN', 'ADEN', 'WALES', 'GOA', 'NIGER', 'DELHI', 'CHAD']

def read_all_columns(location_set, label=""):
    """Read all 9 columns of the grid for a given set of locations."""
    print(f"\n  Location set: {location_set}  {label}")

    # Validate lengths
    for i, loc in enumerate(location_set):
        expected = WORD_LENGTHS[i]
        if len(loc) != expected:
            print(f"    WARNING: Row {i+1} = {loc} (len={len(loc)}) but expected len={expected}")

    # Build grid
    grid = {}
    for i, (row_num, start_col, length) in enumerate(LAYOUT):
        loc = location_set[i]
        for j, ch in enumerate(loc):
            grid[(i, start_col + j)] = ch

    # Read columns
    for col in range(9):
        letters = []
        for i in range(11):
            ch = grid.get((i, col), '.')
            letters.append(ch)
        col_str = ''.join(letters)
        # Only show if at least 3 letters
        actual_letters = [c for c in col_str if c != '.']
        if actual_letters:
            print(f"    Col {col}: {col_str} ({''.join(actual_letters)})")

read_all_columns(best_aw_set, "(best AROUNDWORLD set)")

# MELANESIANS best set
best_mel_set = ['OMAN', 'GREECE', 'ITALY', 'JAPAN', 'IRAN', 'PERU', 'SPAIN', 'CIV', 'GHANA', 'KENYA', 'LAOS']
read_all_columns(best_mel_set, "(MELANESIANS set)")


# ============================================================
# PART 7: SCORE ALL AROUNDWORLD SETS BY MRBEAST RELEVANCE
# ============================================================
print("\n")
print("#" * 80)
print("# PART 7: SCORING AROUNDWORLD SETS BY MRBEAST RELEVANCE")
print("#" * 80)

MRBEAST_LOCATIONS = {
    # Tier 3: Strong MrBeast connection (philanthropy, videos, events)
    'MALI': 3, 'CHAD': 3, 'NIGER': 3, 'SUDAN': 3, 'GHANA': 3,
    'KENYA': 3, 'LAGOS': 3, 'ACCRA': 3, 'DELHI': 3, 'INDIA': 3,
    'PERU': 3, 'LIMA': 3, 'DUBAI': 3, 'CAIRO': 3, 'EGYPT': 3,
    # Tier 2: Moderate connection (regions, nearby)
    'TEHRAN': 2, 'OMAN': 2, 'ADEN': 2, 'DAKAR': 2, 'BENIN': 2,
    'TOGO': 2, 'GABON': 2, 'NEPAL': 2, 'JAPAN': 2, 'CHINA': 2,
    'BRAZIL': 2, 'MUMBAI': 2, 'GOA': 2, 'ABUJA': 2, 'RIYADH': 2,
    # Tier 1: Weak connection
    'WALES': 1, 'DOVER': 1, 'ROME': 1, 'OSLO': 1, 'BALI': 1,
    'CUBA': 1, 'IRAN': 1,
}

if aw_sets is not None and len(aw_sets) > 0:
    scored_sets = []
    for combo in aw_sets:
        score = sum(MRBEAST_LOCATIONS.get(loc, 0) for loc in combo)
        scored_sets.append((score, combo))

    scored_sets.sort(key=lambda x: -x[0])

    print(f"\n  Top 30 AROUNDWORLD sets by MrBeast relevance score:")
    seen = set()
    count = 0
    for score, combo in scored_sets:
        key = tuple(sorted(combo))
        if key in seen:
            continue
        seen.add(key)
        count += 1
        if count > 30:
            break
        loc_scores = [f"{loc}({MRBEAST_LOCATIONS.get(loc, 0)})" for loc in combo]
        print(f"    Score {score:2d}: {list(combo)}")
        print(f"             {' '.join(loc_scores)}")

    print(f"\n  Total unique AROUNDWORLD sets: {len(set(tuple(sorted(c)) for _, c in scored_sets))}")
elif aw_candidates:
    print("\n  Too many combinations to score individually.")
    print("  Showing best individual candidates per row:")
    for row_idx in range(11):
        row_num = LAYOUT[row_idx][0]
        candidates = aw_candidates[row_idx]
        scored = [(MRBEAST_LOCATIONS.get(c, 0), c) for c in candidates]
        scored.sort(key=lambda x: -x[0])
        top5 = scored[:5]
        print(f"    Row {row_num:2d}: {[(s,c) for s,c in top5]}")


# ============================================================
# PART 8: 50A CONSTRAINT CHECK (positions 10=A, 13=R)
# ============================================================
print("\n")
print("#" * 80)
print("# PART 8: 50A SUBSTRING CHECK (known letters: pos10=A, pos13=R)")
print("#" * 80)
print("50A is a 16-letter theme entry. Positions 10 and 13 are known (A and R).")
print("If a location is hidden in 50A, it must be compatible with these letters.\n")

# Check which locations could be hidden in 50A
# 50A has 16 positions (0-15), with A at 10 and R at 13
print("\n  TIER 1: Locations that USE BOTH known letters (A@10 AND R@13):")
print("  " + "-" * 70)
tier1_matches = []
tier2_matches = []

for loc in sorted(all_locations, key=lambda x: (-len(x), x)):
    if len(loc) < 3:
        continue
    for start in range(16 - len(loc) + 1):
        end = start + len(loc) - 1
        compatible = True
        uses_A10 = False
        uses_R13 = False

        for loc_pos in range(len(loc)):
            entry_pos = start + loc_pos
            if entry_pos == 10:
                if loc[loc_pos] != 'A':
                    compatible = False
                    break
                uses_A10 = True
            if entry_pos == 13:
                if loc[loc_pos] != 'R':
                    compatible = False
                    break
                uses_R13 = True

        if compatible and (uses_A10 or uses_R13):
            entry = ['_'] * 16
            entry[10] = 'A'
            entry[13] = 'R'
            for j, ch in enumerate(loc):
                entry[start + j] = ch
            fits_staircase = "YES" if len(loc) in WORD_LENGTHS else "no"
            score = MRBEAST_LOCATIONS.get(loc, 0)
            result = (loc, start, end, ''.join(entry), fits_staircase, score,
                      uses_A10, uses_R13)

            if uses_A10 and uses_R13:
                tier1_matches.append(result)
            else:
                tier2_matches.append(result)

# Show Tier 1 (overlaps BOTH)
for loc, start, end, display, fits, score, _, _ in sorted(tier1_matches, key=lambda x: -x[5]):
    stars = '*' * score if score else ''
    print(f"  {loc:10s} at pos {start:2d}-{end:2d}: {display}  "
          f"(staircase: {fits}) {stars}")

print(f"\n  TIER 2: Locations that use ONE known letter (showing top 30 by MrBeast score):")
print("  " + "-" * 70)
tier2_sorted = sorted(tier2_matches, key=lambda x: (-x[5], x[0]))
for loc, start, end, display, fits, score, u_a, u_r in tier2_sorted[:30]:
    stars = '*' * score if score else ''
    letter_used = "A@10" if u_a else "R@13"
    print(f"  {loc:10s} at pos {start:2d}-{end:2d}: {display}  "
          f"(staircase: {fits}, uses {letter_used}) {stars}")

print(f"\n  Total Tier 1 (both letters): {len(tier1_matches)}")
print(f"  Total Tier 2 (one letter): {len(tier2_matches)}")


# ============================================================
# PART 9: SPECIFIC AROUNDWORLD ALTERNATIVES
# ============================================================
print("\n")
print("#" * 80)
print("# PART 9: DETAILED AROUNDWORLD ROW ALTERNATIVES")
print("#" * 80)
print("For each row, showing ALL location candidates with AROUNDWORLD spine:\n")

AROUNDWORLD = "AROUNDWORLD"
for row_idx in range(11):
    row_num, start_col, length = LAYOUT[row_idx]
    col4_pos = COL4_POSITIONS[row_idx]
    target_letter = AROUNDWORLD[row_idx]

    candidates = LOC_INDEX.get((length, col4_pos, target_letter), [])

    # Score by MrBeast relevance
    scored = [(MRBEAST_LOCATIONS.get(c, 0), c) for c in candidates]
    scored.sort(key=lambda x: (-x[0], x[1]))

    print(f"  Row {row_num:2d} (len={length}, need '{target_letter}' at word[{col4_pos}]):")
    for score, loc in scored:
        stars = '*' * score if score > 0 else '-'
        print(f"    {loc:10s}  MrBeast score: {stars} ({score})")
    if not scored:
        print(f"    *** NO CANDIDATES ***")
    print()


# ============================================================
# SUMMARY
# ============================================================
print("\n")
print("#" * 80)
print("# SUMMARY")
print("#" * 80)

if aw_sets is not None:
    print(f"\n  AROUNDWORLD: {len(aw_sets):,} valid location sets found")
else:
    print(f"\n  AROUNDWORLD: Too many combinations to enumerate")
    if aw_candidates:
        combos = 1
        for c in aw_candidates:
            combos *= len(c)
        print(f"    Estimated: {combos:,} combinations")

if mel_sets is not None:
    print(f"  MELANESIANS: {len(mel_sets):,} valid location sets found")
else:
    print(f"  MELANESIANS: Too many combinations to enumerate")
    if mel_candidates:
        zeros = [i for i, c in enumerate(mel_candidates) if len(c) == 0]
        if zeros:
            print(f"    IMPOSSIBLE: Rows {[LAYOUT[z][0] for z in zeros]} have no candidates")

print(f"\n  Feasible dictionary spine words: {len(valid_spines)}")
print(f"  Thematically relevant feasible spines: {len(thematic_spines)}")

print("\n  DONE.")
