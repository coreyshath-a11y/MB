#!/usr/bin/env python3
"""
Staircase Grid Solver v2 - FIXED constraint model.

KEY FIX: Only ADJACENT rows share letters at overlapping columns.
Non-adjacent rows at the same column can have DIFFERENT letters.
The old solver incorrectly treated each column as having one global letter.

Critical insight: Column 4 is used by ALL 11 rows AND every pair of adjacent rows
shares col 4, so col 4 IS globally shared (one letter for all 11 rows).
But other columns have "breaks" where non-adjacent rows can differ.
"""

import itertools

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

# Build ADJACENT-ONLY constraints: (row_i, pos_in_i, row_j, pos_in_j)
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
# COMPREHENSIVE LOCATION DATABASE
# ============================================================
# Include: countries, capitals, major cities, regions, islands,
# geographic features, historical places, MrBeast-related locations

LOCATIONS_BY_LEN = {
    3: [
        "GOA", "FEZ", "HUE", "ABO", "UFA", "ICA", "ZUG", "NIS", "PAU",
        "AYR", "ELY", "RYE", "WYE", "AXE", "DEE", "ESK", "URE", "DON",
        "CAM", "TAY", "RAJ", "OBI", "RIO", "GAP", "SPA", "DAM", "BAY",
        "COS", "IOS", "KEA", "MEL", "NIL", "OAT", "QOM",
        "URK", "VIS", "YAM", "JAM", "ROM", "ULM", "LUZ", "TUZ",
        "SAL", "JOS", "SAG", "ZOD", "MOB",
    ],
    4: [
        "BALI", "CUBA", "DOHA", "FIJI", "GUAM", "IRAN", "IRAQ", "LAOS",
        "LIMA", "MALI", "NICE", "OMAN", "OSLO", "PERU", "ROME", "SUVA",
        "TOGO", "CHAD", "GAZA", "BAKU", "LOME", "LYON", "BONN",
        "CORK", "YORK", "BATH", "MESA", "RENO", "WACO", "TROY",
        "NARA", "KOBE", "AGRA", "PUNE", "CEBU", "SANA", "ADEN",
        "RIGA", "BERN", "GRAZ", "LINZ", "KIEV", "LVIV",
        "APIA", "MALE", "LAMU", "MERU", "PERM", "OMSK", "TULA",
        "SION", "CHUR", "COMO", "PISA", "BARI", "FARO", "VIGO",
        "GENT", "MONS", "LIEGE", "LODZ", "BRNO", "PECS", "OULU",
        "KIEL", "GRAZ", "LINZ", "WELS", "EIBAR",
        "MOAB", "Nome", "GARY", "ERIE", "WACO", "YUMA", "ENID",
        "GIZA", "LUXOR",  # 5
        "ACRE", "NIUE", "GUAM", "WAKE", "FIJI",
        "SOCHI",  # 5
        "DILI", "IPOH", "IASI", "PULA", "PERM",
        "LODI", "GALE", "FORD",
        "OAHU", "JAVA", "CALI", "QUAY",
    ],
    5: [
        "ACCRA", "TOKYO", "PARIS", "CAIRO", "MIAMI", "DUBAI", "KABUL",
        "DHAKA", "HANOI", "NAURU", "LAGOS", "DAKAR", "RABAT", "TUNIS",
        "MINSK", "SOFIA", "ABUJA", "QUITO", "TEMPE", "DOVER", "BOISE",
        "TULSA", "OMAHA", "DELHI", "OSAKA", "KYOTO", "BUSAN", "ARUBA",
        "MALTA", "NEPAL", "KENYA", "BENIN", "GABON", "NIGER", "SUDAN",
        "LIBYA", "SYRIA", "YEMEN", "SAMOA", "TONGA", "PALAU",
        "CHILE", "HAITI", "ITALY", "SPAIN", "CHINA", "JAPAN", "INDIA",
        "KOREA", "QATAR", "GHANA", "EGYPT", "MACAU", "CUSCO", "LUXOR",
        "PETRA", "BANFF", "MOAB",  # 4
        "NIMES", "DIJON", "REIMS", "TOURS", "VISBY",
        "VADUZ", "DAVOS", "SIENA", "PERTH", "LHASA", "SOCHI",
        "KAZAN", "PSKOV", "TRIER", "MALMÖ", "TURKU", "DELFT",
        "LIEGE", "GHENT", "PORTO", "AVILA", "SORIA",
        "NAXOS", "CORFU", "VOLOS", "PATNA", "SURAT", "THANE",
        "DACCA", "MEDAN", "JOGJA", "SURIN", "SUBIC",
        "NATAL", "BELEM", "BAHIA", "CUSCO", "SUCRE", "TALCA",
        "OAXACA",  # 6
        "TACNA", "PIURA", "ORURO", "POTOSI",  # 6
        "OGDEN", "PROVO", "NAMPA", "BOISE", "ELGIN", "MACON",
        "AKRON", "SALEM", "FARGO", "SIOUX",
        "ASWAN", "EDINA", "PLANO", "FRISCO",  # 6
        "WUHAN", "HEFEI", "JINAN", "XIAN", "DALIAN",  # 6
        "ABACO", "CAPRI", "IBIZA", "TULUM", "SITKA",
        "HAIFA", "JAFFA", "EILAT", "IZMIR",
        "ZULIA", "TIGRE", "COLÓN",
        # More well-known 5-letter locations
        "TONGA", "NAURU", "PALAU", "WALES", "GENOA", "PADUA",
        "LUCCA", "PARMA", "PRATO", "MONZA", "LECCE", "AOSTA",
        "UDINE", "TRENTO", "LIEGE", "NAMUR",
        "POZNAN", # 6
        "WROCLAW",  # 7
        "GDYNIA",  # 6
        "BURSA", "ADANA", "KONYA", "SIVAS",
        "BASRA", "MOSUL", "KABUL", "HERAT",
        "LHASA", "THIMBU",  # 6
        "LUSAKA",  # 6
        "ABUJA",
        "LYONS", "SEDAN", "CAEN",  # 4
        "MECCA",
    ],
    6: [
        "LONDON", "BERLIN", "MOSCOW", "VIENNA", "LISBON", "DUBLIN",
        "ATHENS", "SYDNEY", "MUMBAI", "MANILA", "HAVANA", "BOGOTA",
        "NASSAU", "RIYADH", "MUSCAT", "TEHRAN", "ANKARA",
        "WARSAW", "PRAGUE", "ZURICH", "GENEVA", "NAPLES", "VENICE",
        "MADRID", "MALAGA", "OTTAWA", "DENVER", "AUSTIN", "BOSTON",
        "DALLAS", "FRESNO", "TOLEDO", "AUBURN", "REGINA", "NAGOYA",
        "ALEPPO", "CANCUN", "BRUGES", "GDANSK",
        "LAHORE", "YANGON", "JEDDAH", "LUSAKA", "MAPUTO",
        "BAMAKO", "BANJUL", "BISSAU", "HARARE", "KIGALI",
        "LUANDA", "MASERU", "MALAWI", "ZAMBIA", "JORDAN",
        "ISRAEL", "PANAMA", "BELIZE", "GUYANA", "FRANCE",
        "POLAND", "GREECE", "TURKEY", "SWEDEN", "NORWAY",
        "BRAZIL", "MEXICO", "CANADA", "RUSSIA", "TUVALU",
        "BHUTAN", "BRUNEI", "KUWAIT", "MONACO", "LATVIA",
        "SERBIA", "CYPRUS", "MALAWI",
        "NASSAU", "DARWIN", "CAIRNS", "HOBART",
        "ODESSA", "BATUMI", "MUSCAT", "MANAMA",
        "LUANDA", "DOUALA", "KUMASI", "IBADAN",
        "PUEBLA", "MERIDA", "OAXACA", "CUSCO",
        "RECIFE", "SANTOS",
        "POZNAN", "GDYNIA", "TOULON", "DIEPPE",
        "BILBAO", "SEVILLE",  # 7
        "CUENCA", "AREQUIPA",  # 8
        "THIMBU",
    ],
}

# Clean up: ensure correct lengths and remove duplicates
for length in LOCATIONS_BY_LEN:
    LOCATIONS_BY_LEN[length] = sorted(set(
        w.upper() for w in LOCATIONS_BY_LEN[length] if len(w.upper()) == length
    ))

for length in sorted(LOCATIONS_BY_LEN.keys()):
    print(f"Length {length}: {len(LOCATIONS_BY_LEN[length])} candidates")

# ============================================================
# SOLVE using backtracking with adjacent-only constraints
# ============================================================

# For each row, store its word as a list of characters
solution = [None] * 11

# Build constraint list indexed by row
row_constraints_from = [[] for _ in range(11)]  # constraints where row i is the "from"
row_constraints_to = [[] for _ in range(11)]    # constraints where row i is the "to"

for ri, pi, rj, pj in constraints:
    row_constraints_from[ri].append((pi, rj, pj))
    row_constraints_to[rj].append((pj, ri, pi))

def is_consistent(row_idx, word):
    """Check if placing word at row_idx is consistent with already-placed adjacent rows."""
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
    candidates = LOCATIONS_BY_LEN.get(length, [])

    for word in candidates:
        if is_consistent(row_idx, word):
            solution[row_idx] = word
            solve(row_idx + 1)
            solution[row_idx] = None

print("\nSolving with adjacent-only constraints...")
solve(0)
print(f"Found {len(solutions_found)} solutions")

if solutions_found:
    # Analyze solutions
    if len(solutions_found) <= 50:
        for i, sol in enumerate(solutions_found[:50]):
            print(f"\n  Solution {i+1}:")
            for j, word in enumerate(sol):
                print(f"    Row {j+1:2d}: {word}")
    else:
        # Show consensus
        print("\n  Too many solutions. Finding consensus...")
        for row_idx in range(11):
            words = set(sol[row_idx] for sol in solutions_found)
            if len(words) <= 10:
                print(f"  Row {row_idx+1}: {sorted(words)}")
            else:
                print(f"  Row {row_idx+1}: {len(words)} options")

    # Check column 4 letter distribution (should be same for all rows in all solutions)
    col4_letters = set()
    for sol in solutions_found:
        for row_idx in range(11):
            pos = ROWS[row_idx][1].index(4)
            col4_letters.add(sol[row_idx][pos])
    print(f"\nCol 4 letters across all solutions: {sorted(col4_letters)}")

else:
    print("\nNo solutions found! Trying analysis...")

    # Try each letter for col 4 (globally shared)
    print("\nCol 4 analysis (must be same letter for all 11 rows):")
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        row_counts = []
        all_viable = True
        for row_idx in range(11):
            length = ROWS[row_idx][0]
            col4_pos = ROWS[row_idx][1].index(4)
            candidates = [w for w in LOCATIONS_BY_LEN.get(length, [])
                         if w[col4_pos] == letter]
            row_counts.append(len(candidates))
            if len(candidates) == 0:
                all_viable = False
                break
        if all_viable:
            min_count = min(row_counts)
            total = sum(row_counts)
            print(f"  Col4={letter}: candidates per row = {row_counts}, min={min_count}")

    # Also try solving just the R1-R2-R3 chain (most constrained)
    print("\n\nR1-R2-R3 chain analysis:")
    print("R2 = R3[0:2] + R1  (R2's first 2 letters from R3, last 4 from R1)")
    print("R3[2:5] = R1[0:3]  (R3's last 3 letters = R1's first 3)")

    found_chains = []
    for r1 in LOCATIONS_BY_LEN.get(4, []):
        for r3 in LOCATIONS_BY_LEN.get(5, []):
            # Check R3[2:5] = R1[0:3]
            if r3[2:5] != r1[0:3]:
                continue
            # R2 = R3[0:2] + R1
            r2_candidate = r3[0:2] + r1
            if r2_candidate in LOCATIONS_BY_LEN.get(6, []):
                found_chains.append((r1, r2_candidate, r3))

    print(f"\nValid R1-R2-R3 chains found: {len(found_chains)}")
    for r1, r2, r3 in found_chains:
        print(f"  R1={r1}, R2={r2}, R3={r3}")
        # Try to extend to R4
        for r4 in LOCATIONS_BY_LEN.get(5, []):
            if r4[0:3] == r3[2:5]:  # R4[0:3] = R3[2:5] = R1[0:3]
                # Try R5
                for r5 in LOCATIONS_BY_LEN.get(4, []):
                    if r5[2:4] == r4[0:2]:
                        # Try R6
                        for r6 in LOCATIONS_BY_LEN.get(4, []):
                            if r6[0:2] == r5[2:4]:
                                if r6[1] == r1[1]:  # col 4 match (global)
                                    print(f"    R4={r4}, R5={r5}, R6={r6}")
