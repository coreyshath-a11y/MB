#!/usr/bin/env python3
"""
Cascade from HULAHOOP at 133D and ACCRA at 151D to find new placements.
Then cascade from those, etc. Keep going until no more unique fits.
"""

# Full grid setup
grid = {}
black = {
    (0,7),(0,8),(0,15),(0,16),(1,7),(1,15),(1,16),(2,16),
    (3,4),(3,10),(3,14),(3,20),(4,4),(4,5),(4,6),(4,11),(4,21),
    (5,4),(5,8),(5,13),(5,18),(5,19),(6,16),(6,23),(6,24),
    (7,7),(7,12),(7,17),(7,24),(8,3),(8,9),(8,14),(8,15),(8,20),
    (9,0),(9,1),(9,2),(9,9),(9,10),(10,0),(10,4),(10,8),(10,9),(10,16),(10,21),
    (11,5),(11,11),(11,17),(11,21),(12,6),(12,18),
    (13,3),(13,7),(13,13),(13,19),(14,3),(14,8),(14,15),(14,16),(14,20),(14,24),
    (15,14),(15,15),(15,22),(15,23),(15,24),(16,4),(16,9),(16,10),(16,15),(16,21),
    (17,0),(17,7),(17,12),(17,17),(18,0),(18,1),(18,8),
    (19,5),(19,6),(19,11),(19,16),(19,20),(20,3),(20,13),(20,18),(20,19),(20,20),
    (21,4),(21,10),(21,14),(21,20),(22,8),(23,8),(23,9),(23,17),
    (24,8),(24,9),(24,16),(24,17)
}

def place_a(row, col, word):
    for i, ch in enumerate(word):
        grid[(row, col+i)] = ch

def place_d(row, col, word):
    for i, ch in enumerate(word):
        grid[(row+i, col)] = ch

# All confirmed
place_a(4,7,"DORA"); place_d(4,10,"ABASH"); place_d(6,13,"ROTUNDA")
place_a(7,8,"PUSH"); place_a(8,10,"HAFT"); place_d(11,8,"ZIP")
place_d(11,9,"TRITE"); place_a(11,12,"ADORN"); place_a(12,7,"CIRCLEABOUT")
place_d(12,17,"TONER"); place_a(13,8,"PINTO"); place_a(13,14,"ACHOO")
place_a(14,9,"TOLEDO"); place_d(14,13,"DENVER"); place_a(15,16,"REGINA")
place_a(16,11,"TONI"); place_a(16,16,"ERASE"); place_a(22,9,"SUPERBOWLSTADIUM")
place_a(20,4,"BEASTLAND")
# Hypothetical
place_d(13,18,"ORGANIC"); place_a(14,17,"NRA")

# New cascade level 1
place_d(17,15,"HULAHOOP")  # 133D
place_d(20,6,"ACCRA")  # 151D = A,C,C,R,A at rows 20-24

print("=== After HULAHOOP + ACCRA placement ===")
print()

# Now build complete entry list
across_entries = {
    '1A': (0,0,7), '8A': (0,9,6), '14A': (0,17,8), '22A': (1,0,7),
    '23A': (1,8,7), '24A': (1,17,8), '25A': (2,0,16), '28A': (2,17,8),
    '29A': (3,0,4), '30A': (3,5,5), '31A': (3,11,3), '32A': (3,15,5),
    '34A': (3,21,4), '35A': (4,0,4), '36A': (4,7,4), '38A': (4,12,9),
    '41A': (4,22,3), '42A': (5,0,4), '43A': (5,5,3), '45A': (5,9,4),
    '47A': (5,14,4), '48A': (5,20,5), '50A': (6,0,16), '54A': (6,17,6),
    '57A': (7,0,7), '58A': (7,8,4), '59A': (7,13,4), '61A': (7,18,6),
    '63A': (8,0,3), '64A': (8,4,5), '66A': (8,10,4), '68A': (8,16,4),
    '70A': (8,21,4), '72A': (9,3,6), '73A': (9,11,14), '77A': (10,1,3),
    '79A': (10,5,3), '80A': (10,10,6), '81A': (10,17,4), '82A': (10,22,3),
    '83A': (11,0,5), '85A': (11,6,5), '88A': (11,12,5), '90A': (11,18,3),
    '91A': (11,22,3), '92A': (12,0,6), '94A': (12,7,11), '97A': (12,19,6),
    '99A': (13,0,3), '100A': (13,4,3), '102A': (13,8,5), '103A': (13,14,5),
    '105A': (13,20,5), '106A': (14,0,3), '107A': (14,4,4), '109A': (14,9,6),
    '111A': (14,17,3), '113A': (14,21,3), '114A': (15,0,14), '117A': (15,16,6),
    '119A': (16,0,4), '120A': (16,5,4), '121A': (16,11,4), '123A': (16,16,5),
    '124A': (16,22,3), '127A': (17,1,6), '129A': (17,8,4), '132A': (17,13,4),
    '134A': (17,18,7), '136A': (18,2,6), '138A': (18,9,16), '141A': (19,0,5),
    '143A': (19,7,4), '145A': (19,12,4), '146A': (19,17,3), '147A': (19,21,4),
    '148A': (20,0,3), '149A': (20,4,9), '153A': (20,14,4), '155A': (20,21,4),
    '156A': (21,0,4), '158A': (21,5,5), '159A': (21,11,3), '161A': (21,15,5),
    '164A': (21,21,4), '165A': (22,0,8), '167A': (22,9,16), '171A': (23,0,8),
    '172A': (23,10,7), '173A': (23,18,7), '174A': (24,0,8), '175A': (24,10,6),
    '176A': (24,18,7),
}
down_entries = {
    '1D': (0,0,9), '2D': (0,1,9), '3D': (0,2,9), '4D': (0,3,8),
    '5D': (0,4,3), '6D': (0,5,4), '7D': (0,6,4), '8D': (0,9,8),
    '9D': (0,10,3), '10D': (0,11,4), '11D': (0,12,7), '12D': (0,13,5),
    '13D': (0,14,3), '14D': (0,17,7), '15D': (0,18,5), '16D': (0,19,5),
    '17D': (0,20,3), '18D': (0,21,4), '19D': (0,22,15), '20D': (0,23,6),
    '21D': (0,24,6), '23D': (1,8,4), '26D': (2,7,5), '27D': (2,15,6),
    '33D': (3,16,3), '37D': (4,10,5), '39D': (4,14,4), '40D': (4,20,4),
    '43D': (5,5,6), '44D': (5,6,7), '46D': (5,11,6), '49D': (5,21,5),
    '51D': (6,4,4), '52D': (6,8,4), '53D': (6,13,7), '55D': (6,18,6),
    '56D': (6,19,7), '60D': (7,16,3), '62D': (7,23,8), '65D': (8,7,5),
    '67D': (8,12,9), '69D': (8,17,3), '71D': (8,24,6), '72D': (9,3,4),
    '74D': (9,14,6), '75D': (9,15,5), '76D': (9,20,5), '77D': (10,1,8),
    '78D': (10,2,15), '80D': (10,10,6), '83D': (11,0,6), '84D': (11,4,5),
    '86D': (11,8,3), '87D': (11,9,5), '89D': (11,16,3), '93D': (12,5,7),
    '95D': (12,11,7), '96D': (12,17,5), '98D': (12,21,4), '101D': (13,6,6),
    '104D': (13,18,7), '108D': (14,7,3), '110D': (14,13,6), '112D': (14,19,6),
    '115D': (15,3,5), '116D': (15,8,3), '117D': (15,16,4), '118D': (15,20,4),
    '122D': (16,14,5), '124D': (16,22,9), '125D': (16,23,9), '126D': (16,24,9),
    '128D': (17,4,4), '130D': (17,9,6), '131D': (17,10,4), '133D': (17,15,8),
    '135D': (17,21,8), '137D': (18,7,7), '139D': (18,12,7), '140D': (18,17,5),
    '141D': (19,0,6), '142D': (19,1,6), '144D': (19,8,3), '150D': (20,5,5),
    '151D': (20,6,5), '152D': (20,11,5), '154D': (20,16,4), '157D': (21,3,4),
    '160D': (21,13,4), '162D': (21,18,4), '163D': (21,19,4), '166D': (22,4,3),
    '168D': (22,10,3), '169D': (22,14,3), '170D': (22,20,3),
}

placed = {
    '36A', '37D', '53D', '58A', '66A', '86D', '87D', '88A', '94A',
    '96D', '102A', '103A', '109A', '110D', '117A', '121A', '123A',
    '167A', '149A', '104D', '111A', '133D', '151D'
}

all_entries = {}
all_entries.update(across_entries)
all_entries.update(down_entries)

# All available answers (including ones not yet placed)
all_answers = {
    3: ['RAD', 'EAR', 'ION', 'EON'],
    4: ['DHOW', 'RACE', 'NOTE'],
    5: ['WAHOO', 'OPERA', 'LECAR', 'TEMPE', 'DOVER'],
    6: ['SCHOOL', 'OHIOAN', 'HOODIE', 'MATTER', 'ECLAIR', 'OPTION', 'ORIENT',
        'CHAIRS', 'CONVEX', 'WARSAW', 'OTTAWA', 'AUBURN'],
    7: ['TYPHOON', 'OHSHOOT', 'HEARTED', 'MUSTERS', 'CALIBER', 'PORTION',
        'INUTERO', 'QUORUMS', 'HIRPLED', 'TORONTO', 'ROSWELL', 'DRESDEN',
        'SANJUAN', 'SEVILLE', 'ORLANDO', 'WOODWAY'],
    8: ['HOODWINK', 'SCENARIO', 'NEUROTIC', 'SCREENER', 'ABSOLUTE',
        'TEAMSEAS', 'DURATION', 'CARBLITE', 'POSITRON', 'ROUTINES', 'FLAMINGO',
        'CASHTENT', 'ADELAIDE'],
    9: ['HOOVERDAM', 'ROBINHOOD', 'DITHERING', 'HOWITZERS', 'HIGHHEELS',
        'ALLUSIONS', 'RESISTIVE', 'INUNDATOR', 'CABRIOLET', 'RATPOISON',
        'OUTLINERS', 'OWENSBORO', 'ROCHESTER', 'ANNAPOLIS'],
}

def get_pattern(name, info):
    row, col, length = info
    is_down = name.endswith('D')
    pattern = []
    for i in range(length):
        if is_down:
            cell = (row + i, col)
        else:
            cell = (row, col + i)
        if cell in grid:
            pattern.append(grid[cell])
        else:
            pattern.append('?')
    return ''.join(pattern)

def matches_pattern(word, pattern):
    if len(word) != len(pattern):
        return False
    for w, p in zip(word, pattern):
        if p != '?' and p != w:
            return False
    return True

# Check all entries for new unique fits
print("Checking all entries after HULAHOOP + ACCRA cascade...\n")

new_placements = []
for name in sorted(all_entries.keys(), key=lambda x: (int(x[:-1]), x[-1])):
    if name in placed:
        continue
    info = all_entries[name]
    length = info[2]
    pattern = get_pattern(name, info)
    known = sum(1 for c in pattern if c != '?')

    if known == 0:
        continue

    candidates = all_answers.get(length, [])
    matching = [c for c in candidates if matches_pattern(c, pattern)]

    if len(matching) == 1:
        print(f"  UNIQUE FIT: {name}: {pattern} → {matching[0]}")
        new_placements.append((name, matching[0], info))
    elif len(matching) == 0 and known >= 2:
        print(f"  ZERO FIT:   {name}: {pattern} ({known} known, {len(candidates)} candidates checked)")
    elif len(matching) > 1 and known >= 2:
        print(f"  MULTI FIT:  {name}: {pattern} → {matching}")

# If we found new unique placements, cascade again
print("\n" + "=" * 60)
print(f"NEW UNIQUE FITS FROM CASCADE: {len(new_placements)}")
print("=" * 60)

if new_placements:
    for name, answer, info in new_placements:
        row, col, length = info
        is_down = name.endswith('D')
        print(f"\n  Placing {name} = {answer}:")
        for i in range(length):
            if is_down:
                cell = (row + i, col)
            else:
                cell = (row, col + i)
            if cell not in grid:
                grid[cell] = answer[i]
                print(f"    New letter '{answer[i]}' at {cell}")
        placed.add(name)

    # Check for another round
    print("\n\n=== ROUND 2: Checking after new placements ===\n")
    round2_placements = []
    for name in sorted(all_entries.keys(), key=lambda x: (int(x[:-1]), x[-1])):
        if name in placed:
            continue
        info = all_entries[name]
        length = info[2]
        pattern = get_pattern(name, info)
        known = sum(1 for c in pattern if c != '?')

        if known == 0:
            continue

        candidates = all_answers.get(length, [])
        matching = [c for c in candidates if matches_pattern(c, pattern)]

        if len(matching) == 1:
            print(f"  UNIQUE FIT: {name}: {pattern} → {matching[0]}")
            round2_placements.append((name, matching[0], info))
        elif len(matching) == 0 and known >= 2:
            print(f"  ZERO FIT:   {name}: {pattern} ({known} known)")
        elif len(matching) > 1 and known >= 1:
            print(f"  MULTI FIT:  {name}: {pattern} → {matching}")

    if round2_placements:
        print(f"\n  Round 2 unique fits: {len(round2_placements)}")
        for name, answer, info in round2_placements:
            row, col, length = info
            is_down = name.endswith('D')
            print(f"\n  Placing {name} = {answer}:")
            for i in range(length):
                if is_down:
                    cell = (row + i, col)
                else:
                    cell = (row, col + i)
                if cell not in grid:
                    grid[cell] = answer[i]
                    print(f"    New letter '{answer[i]}' at {cell}")
            placed.add(name)

        # Round 3
        print("\n\n=== ROUND 3: Checking after round 2 ===\n")
        for name in sorted(all_entries.keys(), key=lambda x: (int(x[:-1]), x[-1])):
            if name in placed:
                continue
            info = all_entries[name]
            length = info[2]
            pattern = get_pattern(name, info)
            known = sum(1 for c in pattern if c != '?')
            if known == 0:
                continue
            candidates = all_answers.get(length, [])
            matching = [c for c in candidates if matches_pattern(c, pattern)]
            if len(matching) == 1:
                print(f"  UNIQUE FIT: {name}: {pattern} → {matching[0]}")
            elif len(matching) == 0 and known >= 2:
                print(f"  ZERO FIT:   {name}: {pattern} ({known} known)")
            elif len(matching) > 1 and known >= 1:
                print(f"  MULTI FIT:  {name}: {pattern} → {matching}")

# Print final grid
print("\n\nFINAL GRID STATE:")
print("     ", end="")
for c in range(25):
    print(f"{c%10}", end="")
print()
for r in range(25):
    print(f"R{r:2d} |", end="")
    for c in range(25):
        if (r,c) in black:
            print("#", end="")
        elif (r,c) in grid:
            print(grid[(r,c)], end="")
        else:
            print(".", end="")
    print("|")

# Count placed entries and known circled cell letters
print(f"\nTotal placed entries: {len(placed)}")

# Circled cells
circled = [(0,12),(2,4),(3,8),(3,24),(4,19),(10,12),(11,2),(11,22),
           (13,0),(18,7),(19,17),(20,2),(22,11),(22,18),(22,24),(24,20)]
print("\nCircled cell letters:")
code = []
for r,c in circled:
    if (r,c) in grid:
        code.append(grid[(r,c)])
        print(f"  ({r},{c}): {grid[(r,c)]}")
    else:
        code.append('_')
        print(f"  ({r},{c}): unknown")
print(f"\nFinal code: {''.join(code)}")
print(f"Known: {sum(1 for c in code if c != '_')}/16")
