#!/usr/bin/env python3
"""
Staircase Grid Solver - Capital Cities Theory
"Stars stacked" = stars mark capital cities on maps, stacked in the staircase

Tests BOTH with cell-sharing constraints AND without (independent rows).
Row lengths: 4, 6, 5, 5, 4, 4, 5, 3, 5, 5, 4
"""

# Staircase row definitions: (word_length, [columns])
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

# Build ADJACENT-ONLY constraints
constraints = []
for i in range(len(ROWS) - 1):
    j = i + 1
    cols_i = ROWS[i][1]
    cols_j = ROWS[j][1]
    shared = set(cols_i) & set(cols_j)
    for col in sorted(shared):
        pos_i = cols_i.index(col)
        pos_j = cols_j.index(col)
        constraints.append((i, pos_i, j, pos_j))

print(f"Adjacent-only constraints: {len(constraints)}")
for c in constraints:
    print(f"  R{c[0]+1}[{c[1]}] = R{c[2]+1}[{c[3]}] (col {ROWS[c[0]][1][c[1]]})")

# ============================================================
# COMPREHENSIVE WORLD CAPITAL CITIES DATABASE
# ============================================================
# Every recognized sovereign state capital + some territories/regions

CAPITALS_RAW = {
    # 3-letter capitals and near-capitals
    3: [
        "RIO",  # Cultural capital of Brazil (not official but widely referenced)
        "UFA",  # Capital of Bashkortostan, Russia
        "HUE",  # Former imperial capital of Vietnam
        "FEZ",  # Former capital of Morocco
        "GOA",  # Former Portuguese colonial capital (India)
        "LAE",  # Papua New Guinea major city
        "AGO",  # Not a capital - placeholder
    ],
    # 4-letter capitals
    4: [
        "DOHA",  # Qatar
        "SUVA",  # Fiji
        "LIMA",  # Peru
        "BAKU",  # Azerbaijan
        "ROME",  # Italy
        "OSLO",  # Norway
        "RIGA",  # Latvia
        "BERN",  # Switzerland
        "LOME",  # Togo
        "MALE",  # Maldives
        "NIUE",  # Niue (self-governing)
        "APIA",  # Samoa
        "DILI",  # Timor-Leste
        "KIEV",  # Ukraine (also Kyiv)
        "KYIV",  # Ukraine
        "SANA",  # Yemen (Sana'a simplified)
        "ADEN",  # Yemen (southern capital)
        "AGRA",  # NOT capital, but Mughal capital
        "CEBU",  # NOT capital, but Philippine city
        "MESA",  # NOT capital (Arizona city)
        "RENO",  # NOT capital
        "TROY",  # Ancient capital
        "NARA",  # Former Japanese capital
        "KOBE",  # NOT capital
        "PISA",  # NOT capital
        "BARI",  # NOT capital
        "COMO",  # NOT capital
        "GRAZ",  # NOT capital (Austrian city)
        "LINZ",  # NOT capital
        "BRNO",  # NOT capital (Czech city)
        "CORK",  # NOT capital
        "YORK",  # NOT capital
        "BATH",  # NOT capital
        "BONN",  # Former West German capital
        "NICE",  # NOT capital
        "LYON",  # NOT capital
        "PERM",  # NOT capital (Russian city)
        "OMSK",  # NOT capital
        "OULU",  # NOT capital
    ],
    # 5-letter capitals
    5: [
        "ACCRA",  # Ghana
        "TOKYO",  # Japan
        "PARIS",  # France
        "CAIRO",  # Egypt
        "KABUL",  # Afghanistan
        "DHAKA",  # Bangladesh (also Dacca)
        "HANOI",  # Vietnam
        "MINSK",  # Belarus
        "SOFIA",  # Bulgaria
        "ABUJA",  # Nigeria
        "QUITO",  # Ecuador
        "SUCRE",  # Bolivia (constitutional)
        "RABAT",  # Morocco
        "DAKAR",  # Senegal
        "TUNIS",  # Tunisia
        "VADUZ",  # Liechtenstein
        "NAURU",  # Nauru (Yaren district, but NAURU used)
        "PRAIA",  # Cape Verde
        "SANAA",  # Yemen (also Sana'a)
        "THIMB",  # Bhutan (Thimphu truncated - doesn't fit)
        "BERNE",  # Switzerland (alternate spelling)
        "SEOUL",  # South Korea
        "LAGOS",  # Former Nigerian capital
        "DELHI",  # India (New Delhi)
        "OSAKA",  # NOT capital
        "KYOTO",  # Former Japanese capital
        "BUSAN",  # NOT capital
        "DUBAI",  # NOT capital (UAE emirate)
        "MIAMI",  # NOT capital
        "DOVER",  # Capital of Delaware!
        "BOISE",  # Capital of Idaho!
        "TULSA",  # NOT capital
        "OMAHA",  # NOT capital
        "SALEM",  # Capital of Oregon!
        "RIYADH", # 6 letters
        "ARUBA",  # NOT capital (territory)
        "QATAR",  # Country name, not capital
        "GHANA",  # Country name
        "EGYPT",  # Country name
        "CHINA",  # Country name
        "JAPAN",  # Country name
        "INDIA",  # Country name
        "NEPAL",  # Country name
        "KENYA",  # Country name
        "YEMEN",  # Country name
        "SYRIA",  # Country name
        "CHILE",  # Country name
        "HAITI",  # Country name
        "ITALY",  # Country name
        "SPAIN",  # Country name
        "KOREA",  # Country/region name
        "BENIN",  # Country name
        "GABON",  # Country name
        "NIGER",  # Country name
        "TONGA",  # Country name (capital: Nuku'alofa)
        "PALAU",  # Country name
        "SAMOA",  # Country name
        "WALES",  # NOT sovereign
        "MALTA",  # Country (capital: Valletta)
        "SUDAN",  # Country name
        "LIBYA",  # Country name
        "MACAU",  # Territory
        "HAIFA",  # NOT capital
        "IZMIR",  # NOT capital
        "BURSA",  # NOT capital
        "BASRA",  # NOT capital
        "MOSUL",  # NOT capital
        "LHASA",  # Capital of Tibet
        "MECCA",  # NOT capital
        "CUSCO",  # Former Inca capital
        "PETRA",  # NOT capital (ancient)
        "DAVOS",  # NOT capital
    ],
    # 6-letter capitals
    6: [
        "LONDON",  # United Kingdom
        "BERLIN",  # Germany
        "MOSCOW",  # Russia
        "VIENNA",  # Austria
        "LISBON",  # Portugal
        "DUBLIN",  # Ireland
        "ATHENS",  # Greece
        "MADRID",  # Spain
        "OTTAWA",  # Canada
        "ANKARA",  # Turkey
        "TEHRAN",  # Iran
        "WARSAW",  # Poland
        "PRAGUE",  # Czech Republic
        "NASSAU",  # Bahamas
        "RIYADH",  # Saudi Arabia
        "MUSCAT",  # Oman
        "MANAMA",  # Bahrain
        "LUSAKA",  # Zambia
        "MAPUTO",  # Mozambique
        "BAMAKO",  # Mali
        "BANJUL",  # Gambia
        "BISSAU",  # Guinea-Bissau
        "HARARE",  # Zimbabwe
        "KIGALI",  # Rwanda
        "LUANDA",  # Angola
        "MASERU",  # Lesotho
        "HAVANA",  # Cuba
        "BOGOTA",  # Colombia
        "MANILA",  # Philippines
        "YANGON",  # Former Myanmar capital
        "ASTANA",  # Kazakhstan (now Astana again)
        "TIRANA",  # Albania
        "ZAGREB",  # Croatia
        "SKOPJE",  # North Macedonia
        "NIAMEY",  # Niger
        "BANGUI",  # Central African Republic
        "ASMARA",  # Eritrea
        "MORONI",  # Comoros
        "DODOMA",  # Tanzania
        "MALABO",  # Equatorial Guinea
        "ROSEAU",  # Dominica
        "NASSAU",  # Bahamas
        "TAIPEI",  # Taiwan
        "THIMBU",  # Bhutan (Thimphu simplified)
        "SYDNEY",  # NOT capital (Australian city)
        "MUMBAI",  # NOT capital
        "ZURICH",  # NOT capital
        "GENEVA",  # NOT capital
        "NAPLES",  # NOT capital
        "VENICE",  # NOT capital
        "MALAGA",  # NOT capital
        "DENVER",  # Capital of Colorado!
        "AUSTIN",  # Capital of Texas!
        "BOSTON",  # Capital of Massachusetts!
        "DALLAS",  # NOT capital
        "FRESNO",  # NOT capital
        "TOLEDO",  # NOT capital (Ohio city, but capital of old Spain)
        "AUBURN",  # NOT capital
        "REGINA",  # Capital of Saskatchewan!
        "JEDDAH",  # NOT capital
        "LAHORE",  # NOT capital
        "PUEBLA",  # NOT capital
        "MERIDA",  # NOT capital (but capital of Yucatan)
        "BRUGES",  # NOT capital
        "GDANSK",  # NOT capital
        "ODESSA",  # NOT capital
        "DARWIN",  # Capital of Northern Territory!
        "HOBART",  # Capital of Tasmania!
    ],
}

# Clean up: ensure correct lengths and remove duplicates
for length in CAPITALS_RAW:
    CAPITALS_RAW[length] = sorted(set(
        w.upper() for w in CAPITALS_RAW[length] if len(w.upper()) == length
    ))

for length in sorted(CAPITALS_RAW.keys()):
    print(f"Length {length}: {len(CAPITALS_RAW[length])} candidates")
    for w in CAPITALS_RAW[length]:
        print(f"  {w}")

# ============================================================
# CONSTRAINT ANALYSIS
# ============================================================

print("\n" + "="*60)
print("CONSTRAINT ANALYSIS: Which R1-R2 pairs are possible?")
print("="*60)
print("R1 (4 letters, cols 3-6) shares ALL 4 columns with R2 (6 letters, cols 1-6)")
print("So R2's last 4 characters must equal R1")
print()

found_r1_r2 = []
for r1 in CAPITALS_RAW.get(4, []):
    for r2 in CAPITALS_RAW.get(6, []):
        if r2[2:6] == r1:
            found_r1_r2.append((r1, r2))
            print(f"  R1={r1}, R2={r2}  ({r2[:2]}+{r1})")

print(f"\nTotal R1-R2 pairs: {len(found_r1_r2)}")

print("\n" + "="*60)
print("R2-R3 ANALYSIS")
print("="*60)
print("R2 (cols 1-6) and R3 (cols 1-5) share cols 1,2,3,4,5")
print("R2[0:5] = R3[0:5] (first 5 characters of R2 = all of R3)")
print()

for r1, r2 in found_r1_r2:
    r3_needed = r2[0:5]
    if r3_needed in CAPITALS_RAW.get(5, []):
        print(f"  R1={r1}, R2={r2}, R3={r3_needed} ✓")
    else:
        print(f"  R1={r1}, R2={r2}, need R3={r3_needed} ✗ (not in database)")

print("\n" + "="*60)
print("BROADER ANALYSIS: R3-R4, R4-R5, etc.")
print("="*60)

# R3 (cols 1-5) and R4 (cols 3-7): share cols 3,4,5
# R3[2:5] = R4[0:3]
print("\nR3-R4: R3[2:5] = R4[0:3]")
for r3 in CAPITALS_RAW.get(5, []):
    for r4 in CAPITALS_RAW.get(5, []):
        if r3[2:5] == r4[0:3]:
            print(f"  R3={r3}, R4={r4}  (shared: {r3[2:5]})")

# R4 (cols 3-7) and R5 (cols 1-4): share cols 3,4
# R4[0:2] = R5[2:4]
print("\nR4-R5: R4[0:2] = R5[2:4]")
for r4 in CAPITALS_RAW.get(5, []):
    for r5 in CAPITALS_RAW.get(4, []):
        if r4[0:2] == r5[2:4]:
            print(f"  R4={r4}, R5={r5}  (shared: {r4[0:2]})")

# R5 (cols 1-4) and R6 (cols 3-6): share cols 3,4
# R5[2:4] = R6[0:2]
print("\nR5-R6: R5[2:4] = R6[0:2]")
for r5 in CAPITALS_RAW.get(4, []):
    for r6 in CAPITALS_RAW.get(4, []):
        if r5[2:4] == r6[0:2]:
            print(f"  R5={r5}, R6={r6}  (shared: {r5[2:4]})")

# R6 (cols 3-6) and R7 (cols 4-8): share cols 4,5,6
# R6[1:4] = R7[0:3]
print("\nR6-R7: R6[1:4] = R7[0:3]")
for r6 in CAPITALS_RAW.get(4, []):
    for r7 in CAPITALS_RAW.get(5, []):
        if r6[1:4] == r7[0:3]:
            print(f"  R6={r6}, R7={r7}  (shared: {r6[1:4]})")

# R7 (cols 4-8) and R8 (cols 3-5): share cols 4,5
# R7[0:2] = R8[1:3]
print("\nR7-R8: R7[0:2] = R8[1:3]")
for r7 in CAPITALS_RAW.get(5, []):
    for r8 in CAPITALS_RAW.get(3, []):
        if r7[0:2] == r8[1:3]:
            print(f"  R7={r7}, R8={r8}  (shared: {r7[0:2]})")

# R8 (cols 3-5) and R9 (cols 0-4): share cols 3,4
# R8[0:2] = R9[3:5]
print("\nR8-R9: R8[0:2] = R9[3:5]")
for r8 in CAPITALS_RAW.get(3, []):
    for r9 in CAPITALS_RAW.get(5, []):
        if r8[0:2] == r9[3:5]:
            print(f"  R8={r8}, R9={r9}  (shared: {r8[0:2]})")

# R9 (cols 0-4) and R10 (cols 2-6): share cols 2,3,4
# R9[2:5] = R10[0:3]
print("\nR9-R10: R9[2:5] = R10[0:3]")
for r9 in CAPITALS_RAW.get(5, []):
    for r10 in CAPITALS_RAW.get(5, []):
        if r9[2:5] == r10[0:3]:
            print(f"  R9={r9}, R10={r10}  (shared: {r9[2:5]})")

# R10 (cols 2-6) and R11 (cols 1-4): share cols 2,3,4
# R10[0:3] = R11[1:4]
print("\nR10-R11: R10[0:3] = R11[1:4]")
for r10 in CAPITALS_RAW.get(5, []):
    for r11 in CAPITALS_RAW.get(4, []):
        if r10[0:3] == r11[1:4]:
            print(f"  R10={r10}, R11={r11}  (shared: {r10[0:3]})")

# ============================================================
# FULL BACKTRACKING SOLVE (with constraints)
# ============================================================

print("\n" + "="*60)
print("FULL SOLVE WITH ADJACENT CONSTRAINTS")
print("="*60)

# For each row, store its word
solution = [None] * 11

# Build constraint list indexed by row
row_constraints_from = [[] for _ in range(11)]
row_constraints_to = [[] for _ in range(11)]

for ri, pi, rj, pj in constraints:
    row_constraints_from[ri].append((pi, rj, pj))
    row_constraints_to[rj].append((pj, ri, pi))

def is_consistent(row_idx, word):
    for pi, rj, pj in row_constraints_from[row_idx]:
        if solution[rj] is not None:
            if word[pi] != solution[rj][pj]:
                return False
    for pj, ri, pi in row_constraints_to[row_idx]:
        if solution[ri] is not None:
            if word[pj] != solution[ri][pi]:
                return False
    return True

solutions_found = []
MAX_SOLUTIONS = 1000

def solve(row_idx):
    if len(solutions_found) >= MAX_SOLUTIONS:
        return
    if row_idx == 11:
        solutions_found.append(list(solution))
        return

    length = ROWS[row_idx][0]
    candidates = CAPITALS_RAW.get(length, [])

    for word in candidates:
        if is_consistent(row_idx, word):
            solution[row_idx] = word
            solve(row_idx + 1)
            solution[row_idx] = None

solve(0)
print(f"\nFound {len(solutions_found)} solutions (with constraints)")

if solutions_found:
    for i, sol in enumerate(solutions_found[:50]):
        print(f"\n  Solution {i+1}:")
        for j, word in enumerate(sol):
            cols = ROWS[j][1]
            print(f"    Row {j+1:2d}: {word:8s} (cols {cols})")

# ============================================================
# ALSO TEST WITHOUT CONSTRAINTS (independent rows)
# ============================================================
print("\n" + "="*60)
print("INDEPENDENT ROWS (no sharing constraints)")
print("="*60)

for row_idx in range(11):
    length = ROWS[row_idx][0]
    candidates = CAPITALS_RAW.get(length, [])
    print(f"  Row {row_idx+1} ({length} letters): {len(candidates)} options")
    if len(candidates) <= 15:
        print(f"    {candidates}")

# Check: can all 11 be actual sovereign nation capitals?
print("\n" + "="*60)
print("STRICT SOVEREIGN NATION CAPITALS ONLY")
print("="*60)

SOVEREIGN_CAPITALS = {
    3: ["RIO"],  # Cultural capital only
    4: ["DOHA", "SUVA", "LIMA", "BAKU", "ROME", "OSLO", "RIGA", "BERN",
        "LOME", "MALE", "APIA", "DILI", "KYIV", "SANA", "BONN"],
    5: ["ACCRA", "TOKYO", "PARIS", "CAIRO", "KABUL", "DHAKA", "HANOI",
        "MINSK", "SOFIA", "ABUJA", "QUITO", "SUCRE", "RABAT", "DAKAR",
        "TUNIS", "VADUZ", "PRAIA", "SANAA", "BERNE", "SEOUL", "LHASA",
        "DELHI", "DOVER", "BOISE", "SALEM", "CUSCO", "LAGOS", "KYOTO",
        "MECCA", "DUBAI"],
    6: ["LONDON", "BERLIN", "MOSCOW", "VIENNA", "LISBON", "DUBLIN",
        "ATHENS", "MADRID", "OTTAWA", "ANKARA", "TEHRAN", "WARSAW",
        "PRAGUE", "NASSAU", "RIYADH", "MUSCAT", "MANAMA", "LUSAKA",
        "MAPUTO", "BAMAKO", "BANJUL", "BISSAU", "HARARE", "KIGALI",
        "LUANDA", "MASERU", "HAVANA", "BOGOTA", "MANILA", "ASTANA",
        "TIRANA", "ZAGREB", "SKOPJE", "NIAMEY", "BANGUI", "ASMARA",
        "MORONI", "DODOMA", "MALABO", "ROSEAU", "TAIPEI", "THIMBU",
        "DENVER", "AUSTIN", "BOSTON", "REGINA", "DARWIN", "HOBART"],
}

# Clean
for length in SOVEREIGN_CAPITALS:
    SOVEREIGN_CAPITALS[length] = sorted(set(
        w.upper() for w in SOVEREIGN_CAPITALS[length] if len(w.upper()) == length
    ))

print("\nRow 8 (3 letters) is the bottleneck:")
print(f"  Options: {SOVEREIGN_CAPITALS.get(3, [])}")
print("  Rio (de Janeiro) is NOT an official capital (Brasilia is)")
print("  UFA is capital of Bashkortostan (Russian republic)")
print()

# What about US state capitals?
US_STATE_CAPITALS = {
    4: ["BERN"],  # None that are 4 letters?
    # Actually: none. State capitals with 4 letters: none standard
    5: ["DOVER", "BOISE", "SALEM"],
    6: ["AUSTIN", "BOSTON", "DENVER", "HELENA", "JUNEAU", "TOPEKA", "TRENTON"],
}

# MrBeast-connected capitals
MRBEAST_CAPITALS = {
    3: ["RIO"],
    4: ["LIMA", "DOHA"],
    5: ["ACCRA", "CAIRO", "DHAKA", "HANOI", "DUBAI", "DELHI"],
    6: ["RIYADH", "MANILA", "HARARE", "KIGALI", "LUSAKA", "MAPUTO",
        "BOGOTA", "OTTAWA"],
}

print("\nMrBeast-connected capitals by length:")
for length in sorted(MRBEAST_CAPITALS.keys()):
    print(f"  {length}-letter: {MRBEAST_CAPITALS[length]}")

# ============================================================
# EXHAUSTIVE PAIRWISE COMPATIBILITY CHECK
# ============================================================
print("\n" + "="*60)
print("PAIRWISE COMPATIBILITY: Which adjacent pairs have solutions?")
print("="*60)

all_words = {}
for length in CAPITALS_RAW:
    all_words[length] = CAPITALS_RAW[length]

for i in range(10):
    j = i + 1
    len_i = ROWS[i][0]
    len_j = ROWS[j][0]
    cols_i = ROWS[i][1]
    cols_j = ROWS[j][1]
    shared_cols = sorted(set(cols_i) & set(cols_j))

    compatible_count = 0
    compatible_pairs = []
    for wi in all_words.get(len_i, []):
        for wj in all_words.get(len_j, []):
            compatible = True
            for col in shared_cols:
                pi = cols_i.index(col)
                pj = cols_j.index(col)
                if wi[pi] != wj[pj]:
                    compatible = False
                    break
            if compatible:
                compatible_count += 1
                compatible_pairs.append((wi, wj))

    print(f"\n  R{i+1}-R{j+1}: {len(shared_cols)} shared cols {shared_cols}")
    print(f"    {len(all_words.get(len_i, []))} × {len(all_words.get(len_j, []))} = {len(all_words.get(len_i, [])) * len(all_words.get(len_j, []))} possible, {compatible_count} compatible")
    if compatible_count <= 20:
        for wi, wj in compatible_pairs:
            shared_str = "".join(wi[cols_i.index(c)] for c in shared_cols)
            print(f"      {wi} + {wj} (shared: {shared_str})")
    elif compatible_count <= 100:
        print(f"    First 10: {compatible_pairs[:10]}")

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
