#!/usr/bin/env python3
"""
Brute-force location finder for the MrBeast crossword.
Tests every world location name against every entry position,
using known crossing letter constraints to filter matches.
"""

import re

# ===== STEP 1: Parse entries from grid file =====
with open('/home/user/MB/analysis/CROSSWORD_GRID_DIGITIZED.md') as f:
    content = f.read()

entries = {}
in_across = False
in_down = False
for line in content.split('\n'):
    if '## ACROSS ENTRIES' in line:
        in_across = True
        in_down = False
        continue
    if '## DOWN ENTRIES' in line:
        in_across = False
        in_down = True
        continue
    if '## Entry Length' in line:
        in_down = False
        continue
    if in_across or in_down:
        m = re.match(r'\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|', line)
        if m:
            num = int(m.group(1))
            row = int(m.group(2))
            col = int(m.group(3))
            length = int(m.group(4))
            direction = 'A' if in_across else 'D'
            key = f"{num}{direction}"
            entries[key] = {"row": row, "col": col, "len": length, "dir": direction}

print(f"Parsed {len(entries)} entries ({sum(1 for k in entries if k.endswith('A'))} across, "
      f"{sum(1 for k in entries if k.endswith('D'))} down)")

# ===== STEP 2: All confirmed placements =====
placements = {
    # From solver v5 (confirmed)
    "36A": "DORA", "37D": "ABASH", "53D": "ROTUNDA", "58A": "PUSH",
    "66A": "HAFT", "86D": "ZIP", "87D": "TRITE", "88A": "ADORN",
    "94A": "CIRCLEABOUT", "96D": "TONER", "102A": "PINTO", "103A": "ACHOO",
    "109A": "TOLEDO", "110D": "DENVER", "117A": "REGINA", "121A": "TONI",
    "123A": "ERASE", "167A": "SUPERBOWLSTADIUM", "149A": "BEASTLAND",
    # Cascade (high confidence)
    "133D": "HULAHOOP", "153A": "RACE", "151D": "ACCRA",
    "174A": "TEAMSEAS", "104D": "ORGANIC", "111A": "NRA",
}

# ===== STEP 3: Build constraint grid =====
grid = {}
for name, answer in placements.items():
    if name not in entries:
        print(f"WARNING: {name} not found!")
        continue
    e = entries[name]
    for i, ch in enumerate(answer):
        if e["dir"] == "A":
            r, c = e["row"], e["col"] + i
        else:
            r, c = e["row"] + i, e["col"]
        if (r, c) in grid and grid[(r, c)] != ch:
            print(f"CONFLICT at ({r},{c}): {grid[(r,c)]} vs {ch} from {name}[{i}]")
        grid[(r, c)] = ch

# Add DELHI at 114A pos 8-12 (strong hypothesis)
e114 = entries["114A"]
for i, ch in enumerate("DELHI"):
    r, c = e114["row"], e114["col"] + 8 + i
    if (r, c) in grid and grid[(r, c)] != ch:
        print(f"DELHI CONFLICT at ({r},{c})")
    else:
        grid[(r, c)] = ch

# Add DAKAR at 50A pos 9-13 (confirmed hypothesis)
e50 = entries["50A"]
for i, ch in enumerate("DAKAR"):
    r, c = e50["row"], e50["col"] + 9 + i
    if (r, c) in grid and grid[(r, c)] != ch:
        print(f"DAKAR CONFLICT at ({r},{c})")
    else:
        grid[(r, c)] = ch

print(f"Total cells with known letters: {len(grid)}")

# ===== STEP 4: Comprehensive location database =====
locations = set()

# US Cities (comprehensive)
us_cities = [
    "ROSWELL", "WICHITA", "DURHAM", "PUEBLO", "TOLEDO", "DENVER",
    "ANCHORAGE", "SACRAMENTO", "WILMINGTON", "SPRINGFIELD",
    "TULSA", "RENO", "REGINA", "MACON", "SITKA", "BOISE", "ALBANY",
    "BUFFALO", "LINCOLN", "PROVO", "TACOMA", "CHICAGO", "NEWYORK",
    "SANFRANCISCO", "TEMPE", "ORLANDO", "ROCHESTER", "ANNAPOLIS",
    "AUBURN", "DOVER", "ATLANTA", "SEATTLE", "DALLAS", "HOUSTON",
    "PHOENIX", "AUSTIN", "OMAHA", "MIAMI", "MEMPHIS", "DETROIT",
    "ERIE", "FARGO", "FLINT", "GARY", "RENO", "NOME", "LIMA",
    "WACO", "YUMA", "MESA", "TROY", "AMES", "BEND", "ELKO",
    "LUBBOCK", "LAREDO", "FRESNO", "MODESTO", "STOCKTON",
    "BATONROUGE", "DESMOINES", "FORTWORTH", "ELPASO", "SANANTONIO",
    "SANDIEGO", "SANJOSE", "PORTLAND", "NASHVILLE", "LOUISVILLE",
    "COLUMBUS", "JACKSONVILLE", "CHARLOTTE", "MADISON", "RICHMOND",
    "NEWARK", "NEWBURGH", "BAYRIDGE", "GREENVILLE", "OWENSBORO",
    "WOODWAY", "SEVILLE", "NEPEAN", "OTTAWA",
]

# World Cities
world_cities = [
    "TOKYO", "DELHI", "LONDON", "PARIS", "CAIRO", "LIMA", "ACCRA",
    "LAGOS", "NAIROBI", "DAKAR", "TEHRAN", "KABUL", "ADEN", "GOA",
    "ROME", "OSLO", "BERN", "DOHA", "SUVA", "LOME", "BAKU",
    "RIYADH", "DUBAI", "MOSCOW", "BERLIN", "MADRID", "LISBON",
    "ATHENS", "VIENNA", "PRAGUE", "WARSAW", "BUCHAREST", "BUDAPEST",
    "STOCKHOLM", "HELSINKI", "COPENHAGEN", "DUBLIN", "EDINBURGH",
    "DIVO", "ARLES", "MACON", "TIJUANA", "USHUAIA", "KUPANG",
    "SYDNEY", "MELBOURNE", "BRISBANE", "PERTH", "AUCKLAND",
    "TORONTO", "MONTREAL", "VANCOUVER", "CALGARY",
    "SEOUL", "TAIPEI", "MANILA", "HANOI", "BANGKOK", "JAKARTA",
    "MUMBAI", "KOLKATA", "CHENNAI", "KARACHI", "LAHORE",
    "ISTANBUL", "ANKARA", "BEIRUT", "AMMAN", "BAGDAD",
    "SANJUAN", "ADELAIDE", "DRESDEN", "REGINA",
    "ABUJA", "KINSHASA", "LUANDA", "MAPUTO", "HARARE",
    "NAPLES", "MILAN", "FLORENCE", "VENICE", "GENOA",
    "LYON", "NICE", "MARSEILLE", "BORDEAUX",
    "MUNICH", "HAMBURG", "COLOGNE",
    "TAIPEI", "HANOI", "PHNOM", "VIENTIANE",
    "BOGOTA", "QUITO", "LAPAZ", "ASUNCION", "SANTIAGO",
    "MONTEVIDEO", "CARACAS", "HAVANA", "NASSAU",
]

# Countries
countries = [
    "AFGHANISTAN", "ALBANIA", "ALGERIA", "ANDORRA", "ANGOLA", "ARGENTINA",
    "ARMENIA", "AUSTRALIA", "AUSTRIA", "BAHAMAS", "BAHRAIN", "BANGLADESH",
    "BARBADOS", "BELARUS", "BELGIUM", "BELIZE", "BENIN", "BHUTAN",
    "BOLIVIA", "BOSNIA", "BOTSWANA", "BRAZIL", "BRUNEI", "BULGARIA",
    "BURMA", "BURUNDI", "CAMBODIA", "CAMEROON", "CANADA", "CHAD",
    "CHILE", "CHINA", "COLOMBIA", "COMOROS", "CONGO", "CROATIA",
    "CUBA", "CYPRUS", "DENMARK", "DJIBOUTI", "DOMINICA", "ECUADOR",
    "EGYPT", "ERITREA", "ESTONIA", "ETHIOPIA", "FIJI", "FINLAND",
    "FRANCE", "GABON", "GAMBIA", "GEORGIA", "GERMANY", "GHANA",
    "GREECE", "GRENADA", "GUATEMALA", "GUINEA", "GUYANA", "HAITI",
    "HONDURAS", "HUNGARY", "ICELAND", "INDIA", "INDONESIA", "IRAN",
    "IRAQ", "IRELAND", "ISRAEL", "ITALY", "JAMAICA", "JAPAN",
    "JORDAN", "KAZAKHSTAN", "KENYA", "KOREA", "KUWAIT", "LAOS",
    "LATVIA", "LEBANON", "LESOTHO", "LIBERIA", "LIBYA", "LITHUANIA",
    "MADAGASCAR", "MALAWI", "MALAYSIA", "MALDIVES", "MALI", "MALTA",
    "MAURITANIA", "MAURITIUS", "MEXICO", "MOLDOVA", "MONACO",
    "MONGOLIA", "MONTENEGRO", "MOROCCO", "MOZAMBIQUE", "MYANMAR",
    "NAMIBIA", "NAURU", "NEPAL", "NETHERLANDS", "NICARAGUA",
    "NIGER", "NIGERIA", "NORWAY", "OMAN", "PAKISTAN", "PALAU",
    "PANAMA", "PARAGUAY", "PERU", "PHILIPPINES", "POLAND", "PORTUGAL",
    "QATAR", "ROMANIA", "RUSSIA", "RWANDA", "SAMOA", "SENEGAL",
    "SERBIA", "SINGAPORE", "SLOVAKIA", "SLOVENIA", "SOMALIA",
    "SPAIN", "SRILANKA", "SUDAN", "SURINAME", "SWEDEN", "SWITZERLAND",
    "SYRIA", "TAIWAN", "TANZANIA", "THAILAND", "TOGO", "TONGA",
    "TRINIDAD", "TUNISIA", "TURKEY", "TUVALU", "UGANDA", "UKRAINE",
    "URUGUAY", "UZBEKISTAN", "VANUATU", "VENEZUELA", "VIETNAM",
    "YEMEN", "ZAMBIA", "ZIMBABWE", "WALES",
]

# Regions/Territories
regions = [
    "GUAM", "SAMOA", "TIBET", "CRIMEA", "BERMUDA", "ARUBA",
    "CURACAO", "BALI", "BORNEO", "SICILY", "CORSICA", "SARDINIA",
    "CRETE", "RHODES", "SUMATRA", "JAVA", "HOKKAIDO", "OKINAWA",
    "LUZON", "MINDANAO", "TIERRA", "FUEGO", "PATAGONIA",
    "SAHARA", "KALAHARI", "GOBI", "TUNDRA",
    "CANDYLAND", "BEASTLAND",
]

# Add all to set
for lst in [us_cities, world_cities, countries, regions]:
    for loc in lst:
        locations.add(loc.upper())

# Remove very short (<=2) and very long (>16) — won't fit typical entries
locations = {loc for loc in locations if 3 <= len(loc) <= 16}

print(f"Total locations in database: {len(locations)}")

# Group by length for faster lookup
loc_by_len = {}
for loc in locations:
    l = len(loc)
    if l not in loc_by_len:
        loc_by_len[l] = []
    loc_by_len[l].append(loc)

# ===== STEP 5: For each unplaced entry, build pattern and test locations =====
print(f"\n{'='*70}")
print("BRUTE-FORCE LOCATION MATCHING")
print(f"{'='*70}")

placed_entries = set(placements.keys())
results_by_confidence = {"HIGH": [], "MEDIUM": [], "LOW": []}

for name in sorted(entries.keys(), key=lambda x: (int(x[:-1]), x[-1])):
    if name in placed_entries:
        continue

    e = entries[name]
    elen = e["len"]

    # Build pattern from known grid letters
    pattern = []
    known_count = 0
    for i in range(elen):
        if e["dir"] == "A":
            r, c = e["row"], e["col"] + i
        else:
            r, c = e["row"] + i, e["col"]
        if (r, c) in grid:
            pattern.append(grid[(r, c)])
            known_count += 1
        else:
            pattern.append('?')

    pat_str = ''.join(pattern)

    # Test all locations of matching length
    if elen not in loc_by_len:
        continue

    matches = []
    for loc in loc_by_len[elen]:
        fit = True
        constraint_matches = 0
        for i, ch in enumerate(pat_str):
            if ch != '?':
                if ch != loc[i]:
                    fit = False
                    break
                constraint_matches += 1
        if fit:
            matches.append((loc, constraint_matches))

    if matches:
        # Sort by constraint matches (more = higher confidence)
        matches.sort(key=lambda x: -x[1])

        for loc, cm in matches:
            if cm >= 3:
                conf = "HIGH"
            elif cm >= 1:
                conf = "MEDIUM"
            else:
                conf = "LOW"
            results_by_confidence[conf].append((name, elen, pat_str, known_count, loc, cm))

# Print results grouped by confidence
for conf in ["HIGH", "MEDIUM", "LOW"]:
    results = results_by_confidence[conf]
    if not results:
        continue
    print(f"\n--- {conf} CONFIDENCE ({len(results)} matches) ---")
    for name, elen, pat, known, loc, cm in results:
        print(f"  {name:6s} (len {elen:2d}): {pat} → {loc:20s} ({cm} constraint matches)")

# ===== STEP 6: Special check — theme entries with hidden locations =====
print(f"\n{'='*70}")
print("THEME ENTRY HIDDEN LOCATION CHECK")
print(f"{'='*70}")

theme_entries = ["25A", "50A", "73A", "94A", "114A", "138A", "167A", "19D", "78D"]

for te in theme_entries:
    if te not in entries:
        continue
    e = entries[te]
    elen = e["len"]

    # Build pattern
    pattern = []
    for i in range(elen):
        if e["dir"] == "A":
            r, c = e["row"], e["col"] + i
        else:
            r, c = e["row"] + i, e["col"]
        pattern.append(grid.get((r, c), '?'))

    pat_str = ''.join(pattern)
    print(f"\n{te} (len {elen}): {pat_str}")

    # Check which locations could hide at which positions
    for loc in sorted(locations, key=lambda x: (-len(x), x)):
        llen = len(loc)
        if llen > elen:
            continue
        for start in range(elen - llen + 1):
            fits = True
            cm = 0
            for i, ch in enumerate(loc):
                pos = start + i
                if pat_str[pos] != '?':
                    if pat_str[pos] != ch:
                        fits = False
                        break
                    cm += 1
            if fits:
                end = start + llen - 1
                indicator = " ★" if cm > 0 else ""
                if cm > 0 or (llen >= 4 and te not in ["94A", "167A"]):
                    print(f"  {loc:15s} at pos {start:2d}-{end:2d} ({cm} confirmed letters){indicator}")

# ===== STEP 7: Check specifically for P4 cities =====
print(f"\n{'='*70}")
print("P4 CITY MATCHING (21 decoded cities)")
print(f"{'='*70}")

p4_cities = [
    "TORONTO", "REGINA", "OWENSBORO", "TOLEDO", "ROSWELL", "DRESDEN",
    "TEMPE", "WARSAW", "SANJUAN", "ADELAIDE", "DENVER", "SEVILLE",
    "OTTAWA", "WILMINGTON", "SACRAMENTO", "ANNAPOLIS", "AUBURN",
    "DOVER", "ROCHESTER", "ORLANDO", "WOODWAY",
]

for city in p4_cities:
    clen = len(city)
    for name in sorted(entries.keys(), key=lambda x: (int(x[:-1]), x[-1])):
        if name in placed_entries:
            continue
        e = entries[name]
        if e["len"] != clen:
            continue

        # Build pattern
        pattern = []
        for i in range(clen):
            if e["dir"] == "A":
                r, c = e["row"], e["col"] + i
            else:
                r, c = e["row"] + i, e["col"]
            pattern.append(grid.get((r, c), '?'))

        pat_str = ''.join(pattern)

        # Check fit
        fit = True
        cm = 0
        for i, ch in enumerate(pat_str):
            if ch != '?':
                if ch != city[i]:
                    fit = False
                    break
                cm += 1

        if fit:
            indicator = " ★★★" if cm >= 2 else (" ★★" if cm >= 1 else "")
            print(f"  {city:15s} → {name:6s} ({pat_str}){indicator}")

# ===== STEP 8: Circled cell analysis =====
print(f"\n{'='*70}")
print("CIRCLED CELL STATUS")
print(f"{'='*70}")

circled = [
    (0, 12), (2, 4), (3, 8), (3, 24), (4, 19), (10, 12),
    (11, 2), (11, 22), (13, 0), (18, 7), (19, 17), (20, 2),
    (22, 11), (22, 18), (22, 24), (24, 20),
]

code = []
for i, (r, c) in enumerate(circled):
    letter = grid.get((r, c), '?')
    code.append(letter)
    # Find which entries cross this cell
    crossing = []
    for ename, edata in entries.items():
        if edata["dir"] == "A":
            if edata["row"] == r and edata["col"] <= c < edata["col"] + edata["len"]:
                crossing.append(ename)
        else:
            if edata["col"] == c and edata["row"] <= r < edata["row"] + edata["len"]:
                crossing.append(ename)
    print(f"  Cell {i+1:2d}: ({r:2d},{c:2d}) = {letter}  entries: {', '.join(crossing)}")

print(f"\n  Final code: {''.join(code)}")
unknown = sum(1 for c in code if c == '?')
print(f"  Known: {16-unknown}/16, Unknown: {unknown}/16")
