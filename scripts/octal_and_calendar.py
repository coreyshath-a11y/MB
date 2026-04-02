#!/usr/bin/env python3
"""
Test octal encoding theory + deep calendar date analysis.
"""

print("=" * 60)
print("OCTAL ENCODING THEORY")
print("=" * 60)
print()

# User's theory:
# 7:00 = 7 minutes = 420 seconds
# Octagon = base 8
# Convert key numbers to octal

numbers_to_convert = {
    420: "7:00 = 420 seconds",
    73: "repeated number",
    673: "elephant ate $673",
    67: "Don't say 67",
    17: "17 STOP NOW HERE",
    27: "pervasive number",
    7: "most repeated digit",
    14: "core constant",
    41: "41-day countdown",
    75: "MAY+BELLE A1Z26",
    103: "Barclay Hotel address",
    108: "Lost numbers sum",
    777: "The Row address",
    109: "jersey number / entry",
    6601: "tank turret",
    3634826: "ENDGAME phone keypad",
}

print("Number → Octal conversions:")
for num, desc in numbers_to_convert.items():
    octal = oct(num)[2:]
    print(f"  {num:>10d}₁₀ = {octal:>15s}₈  ({desc})")

print()
print("User's concatenation: 644 + 111 + 1241 = 6441111241")
print()

# Test the concatenated code
code = "6441111241"
print(f"Code: {code}")
print(f"Length: {len(code)} digits")
print()

# Could it be a phone number?
print("As phone number: 644-111-1241 (not a standard US format)")
print(f"As decimal → octal: N/A (it IS octal)")
print(f"As octal → decimal: {int(code, 8)}")
print(f"As binary (3 bits per octal digit): ", end="")
binary = ''
for d in code:
    binary += format(int(d), '03b')
print(binary)
print(f"Binary length: {len(binary)} bits")

# Decode binary as ASCII
print()
print("Binary as ASCII (8-bit chunks):")
for i in range(0, len(binary) - 7, 8):
    byte = binary[i:i+8]
    val = int(byte, 2)
    ch = chr(val) if 32 <= val <= 126 else f'[{val}]'
    print(f"  {byte} = {val} = '{ch}'")

# Also try other octal combinations
print()
print("Other octal concatenation orders:")
combos = [
    ("644-111-1241", "6441111241"),
    ("111-644-1241", "1116441241"),
    ("1241-111-644", "1241111644"),
    ("1241-644-111", "1241644111"),
    ("644-1241-111", "6441241111"),
    ("111-1241-644", "1111241644"),
]
for label, c in combos:
    try:
        dec = int(c, 8)
        binary_c = bin(dec)[2:]
        ascii_chars = ''
        for i in range(0, len(binary_c) - 7, 8):
            byte = binary_c[i:i+8]
            val = int(byte, 2)
            if 32 <= val <= 126:
                ascii_chars += chr(val)
            else:
                ascii_chars += '.'
        print(f"  {label}: octal={c} decimal={dec} ascii='{ascii_chars}'")
    except:
        print(f"  {label}: invalid octal")

# What if the octal digits are entry numbers?
print()
print("Octal digits as entry references:")
print(f"  Digits of 6441111241: 6,4,4,1,1,1,1,2,4,1")
print(f"  As entry numbers: 6D, 4D, 4D, 1A, 1A, 1A, 1D, 2D, 4D, 1A")
print(f"  Or paired: 64, 41, 11, 12, 41")
print(f"  Entries: 64A, 41A, 11D, 12D, 41A")

# ============================================================
print()
print("=" * 60)
print("DEEP CALENDAR DATE ANALYSIS")
print("=" * 60)
print()

# The 11 dates from our calendar analysis
our_dates = [
    (1, 1, "Jan 1"),
    (2, 2, "Feb 2"),
    (3, 1, "Mar 1"),
    (3, 3, "Mar 3"),
    (6, 1, "Jun 1"),
    (7, 1, "Jul 1"),
    (8, 1, "Aug 1"),
    (8, 6, "Aug 6"),
    (9, 1, "Sep 1"),
    (11, 5, "Nov 5"),
    (12, 7, "Dec 7"),
]

# Gist theory: double dates (1/1, 2/2, 3/3, ... 12/12)
double_dates = [(m, m, f"{m}/{m}") for m in range(1, 13)]

print("=== OUR 11 CALENDAR DATES ===")
print()

# All entry info
all_across = {
    1:(0,0,7),8:(0,9,6),14:(0,17,8),22:(1,0,7),23:(1,8,7),24:(1,17,8),
    25:(2,0,16),28:(2,17,8),29:(3,0,4),30:(3,5,5),31:(3,11,3),32:(3,15,5),
    34:(3,21,4),35:(4,0,4),36:(4,7,4),38:(4,12,9),41:(4,22,3),42:(5,0,4),
    43:(5,5,3),45:(5,9,4),47:(5,14,4),48:(5,20,5),50:(6,0,16),54:(6,17,6),
    57:(7,0,7),58:(7,8,4),59:(7,13,4),61:(7,18,6),63:(8,0,3),64:(8,4,5),
    66:(8,10,4),68:(8,16,4),70:(8,21,4),72:(9,3,6),73:(9,11,14),77:(10,1,3),
    79:(10,5,3),80:(10,10,6),81:(10,17,4),82:(10,22,3),83:(11,0,5),85:(11,6,5),
    88:(11,12,5),90:(11,18,3),91:(11,22,3),92:(12,0,6),94:(12,7,11),97:(12,19,6),
    99:(13,0,3),100:(13,4,3),102:(13,8,5),103:(13,14,5),105:(13,20,5),
    106:(14,0,3),107:(14,4,4),109:(14,9,6),111:(14,17,3),113:(14,21,3),
    114:(15,0,14),117:(15,16,6),119:(16,0,4),120:(16,5,4),121:(16,11,4),
    123:(16,16,5),124:(16,22,3),127:(17,1,6),129:(17,8,4),132:(17,13,4),
    134:(17,18,7),136:(18,2,6),138:(18,9,16),141:(19,0,5),143:(19,7,4),
    145:(19,12,4),146:(19,17,3),147:(19,21,4),148:(20,0,3),149:(20,4,9),
    153:(20,14,4),155:(20,21,4),156:(21,0,4),158:(21,5,5),159:(21,11,3),
    161:(21,15,5),164:(21,21,4),165:(22,0,8),167:(22,9,16),171:(23,0,8),
    172:(23,10,7),173:(23,18,7),174:(24,0,8),175:(24,10,6),176:(24,18,7),
}

all_down = {
    1:(0,0,9),2:(0,1,9),3:(0,2,9),4:(0,3,8),5:(0,4,3),6:(0,5,4),7:(0,6,4),
    8:(0,9,8),9:(0,10,3),10:(0,11,4),11:(0,12,7),12:(0,13,5),13:(0,14,3),
    14:(0,17,7),15:(0,18,5),16:(0,19,5),17:(0,20,3),18:(0,21,4),19:(0,22,15),
    20:(0,23,6),21:(0,24,6),23:(1,8,4),26:(2,7,5),27:(2,15,6),33:(3,16,3),
    37:(4,10,5),39:(4,14,4),40:(4,20,4),43:(5,5,6),44:(5,6,7),46:(5,11,6),
    49:(5,21,5),51:(6,4,4),52:(6,8,4),53:(6,13,7),55:(6,18,6),56:(6,19,7),
    60:(7,16,3),62:(7,23,8),65:(8,7,5),67:(8,12,9),69:(8,17,3),71:(8,24,6),
    72:(9,3,4),74:(9,14,6),75:(9,15,5),76:(9,20,5),77:(10,1,8),78:(10,2,15),
    80:(10,10,6),83:(11,0,6),84:(11,4,5),86:(11,8,3),87:(11,9,5),89:(11,16,3),
    93:(12,5,7),95:(12,11,7),96:(12,17,5),98:(12,21,4),101:(13,6,6),
    104:(13,18,7),108:(14,7,3),110:(14,13,6),112:(14,19,6),115:(15,3,5),
    116:(15,8,3),117:(15,16,4),118:(15,20,4),122:(16,14,5),124:(16,22,9),
    125:(16,23,9),126:(16,24,9),128:(17,4,4),130:(17,9,6),131:(17,10,4),
    133:(17,15,8),135:(17,21,8),137:(18,7,7),139:(18,12,7),140:(18,17,5),
    141:(19,0,6),142:(19,1,6),144:(19,8,3),150:(20,5,5),151:(20,6,5),
    152:(20,11,5),154:(20,16,4),157:(21,3,4),160:(21,13,4),162:(21,18,4),
    163:(21,19,4),166:(22,4,3),168:(22,10,3),169:(22,14,3),170:(22,20,3),
}

# Theme entries
theme_across = {25, 50, 73, 94, 114, 138, 167}
theme_down = {19, 78}

# Staircase word lengths
staircase_lengths = [4, 6, 5, 5, 4, 4, 5, 3, 5, 5, 4]

print("Date → Entry Number → Entry Details → Theme Crossing Analysis")
print()

for i, (month, day, label) in enumerate(our_dates):
    entry_num = month * 10 + day

    # Find entry info
    entry_type = ""
    row, col, length = 0, 0, 0
    if entry_num in all_across:
        r, c, l = all_across[entry_num]
        entry_type += f"{entry_num}A(r{r},c{c},len{l})"
        row, col, length = r, c, l
    if entry_num in all_down:
        r, c, l = all_down[entry_num]
        if entry_type:
            entry_type += " + "
        entry_type += f"{entry_num}D(r{r},c{c},len{l})"

    staircase_len = staircase_lengths[i]

    # Check which theme entries this entry crosses
    crossings = []
    # For across entries
    if entry_num in all_across:
        ar, ac, al = all_across[entry_num]
        for tc in range(ac, ac + al):
            # Check if any theme down entry passes through (ar, tc)
            for td_num in theme_down:
                if td_num in all_down:
                    td_r, td_c, td_l = all_down[td_num]
                    if td_c == tc and td_r <= ar < td_r + td_l:
                        pos_in_theme = ar - td_r
                        pos_in_entry = tc - ac
                        crossings.append(f"crosses {td_num}D at pos {pos_in_theme}")
        # Also check if entry IS a theme entry
        if entry_num in theme_across:
            crossings.append("IS a theme entry!")

    # For down entries
    if entry_num in all_down:
        dr, dc, dl = all_down[entry_num]
        for tr in range(dr, dr + dl):
            # Check if any theme across entry passes through (tr, dc)
            for ta_num in theme_across:
                if ta_num in all_across:
                    ta_r, ta_c, ta_l = all_across[ta_num]
                    if ta_r == tr and ta_c <= dc < ta_c + ta_l:
                        pos_in_theme = dc - ta_c
                        pos_in_entry = tr - dr
                        crossings.append(f"crosses {ta_num}A at theme-pos {pos_in_theme}")

    print(f"  {i+1}. {label:8s} → entry {entry_num:3d} → {entry_type}")
    print(f"     Staircase row {i+1}: needs {staircase_len}-letter location")
    if crossings:
        for cx in crossings:
            print(f"     *** {cx}")
    else:
        print(f"     No theme crossings")
    print()

# Also check: are any calendar entries at circled cells?
circled_cells = [
    (0,12), (2,4), (3,8), (3,24), (4,19), (10,12),
    (11,2), (11,22), (13,0), (18,7), (19,17), (20,2),
    (22,11), (22,18), (22,24), (24,20)
]

print("=== CALENDAR ENTRIES AT CIRCLED CELLS ===")
for i, (month, day, label) in enumerate(our_dates):
    entry_num = month * 10 + day
    # Check if this entry starts at or passes through a circled cell
    if entry_num in all_across:
        r, c, l = all_across[entry_num]
        for pos in range(l):
            if (r, c + pos) in circled_cells:
                print(f"  {label} → {entry_num}A pos {pos} at circled cell ({r},{c+pos})")
    if entry_num in all_down:
        r, c, l = all_down[entry_num]
        for pos in range(l):
            if (r + pos, c) in circled_cells:
                print(f"  {label} → {entry_num}D pos {pos} at circled cell ({r+pos},{c})")

# ============================================================
print()
print("=== ALTERNATIVE DATE THEORIES ===")
print()

# Theory: Dates as (row, col) coordinates
print("Dates as (month-1, day-1) grid coordinates (0-indexed):")
for month, day, label in our_dates:
    r, c = month - 1, day - 1
    print(f"  {label} → ({r},{c})")

print()
print("Dates as (day, month) grid coordinates:")
for month, day, label in our_dates:
    r, c = day, month
    if r < 25 and c < 25:
        print(f"  {label} → ({r},{c})")

# Theory: month and day separately encode something
print()
print("Months only: ", [m for m, d, l in our_dates])
print("Days only:   ", [d for m, d, l in our_dates])
months = [m for m, d, l in our_dates]
days = [d for m, d, l in our_dates]
print(f"Month A1Z26: {''.join(chr(64+m) for m in months)}")
print(f"Day A1Z26:   {''.join(chr(64+d) for d in days)}")

# Sum analysis
print(f"\nMonth sum: {sum(months)}")
print(f"Day sum: {sum(days)}")
print(f"Total sum: {sum(months) + sum(days)}")
print(f"Entry number sum: {sum(m*10+d for m,d,l in our_dates)}")

# Theory: Double date vs our dates
print()
print("=== DOUBLE DATES (Gist Theory) vs OUR DATES ===")
print()
print("If double dates 1/1 through 9/9 (only 9 that map to valid entries):")
for m in range(1, 10):
    entry_num = m * 10 + m
    entry_info = ""
    if entry_num in all_across:
        r, c, l = all_across[entry_num]
        entry_info += f"{entry_num}A(len{l}) "
    if entry_num in all_down:
        r, c, l = all_down[entry_num]
        entry_info += f"{entry_num}D(len{l})"
    print(f"  {m}/{m} → entry {entry_num}: {entry_info}")

# Check: do 10/10, 11/11, 12/12 map to anything?
print()
print("10/10 → 1010: no entry (max is 176)")
print("11/11 → 1111: no entry")
print("12/12 → 1212: no entry")
print("So double-dates theory only works for 9 dates (1/1 through 9/9), not 11")
print("Our 11-date theory uses variable dates and produces 11 entries matching staircase rows")

# ============================================================
print()
print("=== WHAT IF CALENDAR ENTRIES ARE CLUES FOR STAIRCASE? ===")
print()
print("Calendar entry → its answer → hidden location in answer?")
print("Or: Calendar entry → crosses theme entry → position reveals location?")
print()
print("Calendar entries and their staircase location requirements:")
print(f"{'#':>2} {'Date':>8} {'Entry':>5} {'Len':>4} {'StLen':>5} {'Match?':>7}")
for i, (month, day, label) in enumerate(our_dates):
    entry_num = month * 10 + day
    staircase_len = staircase_lengths[i]
    entry_len = 0
    if entry_num in all_across:
        entry_len = all_across[entry_num][2]
    elif entry_num in all_down:
        entry_len = all_down[entry_num][2]
    match = "YES" if entry_len == staircase_len else "NO"
    print(f"{i+1:>2} {label:>8} {entry_num:>5} {entry_len:>4} {staircase_len:>5} {match:>7}")

print()
print("DONE!")
