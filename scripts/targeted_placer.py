#!/usr/bin/env python3
"""
Targeted placement of 8-letter and 9-letter answers.
We have more answers than slots at these lengths, so we can use
crossing constraints to narrow placements.
"""

# ============================================================
# GRID DATA (from comprehensive_solver.py)
# ============================================================

BLACK = {
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
    (21,4),(21,10),(21,14),(21,20),(22,8),
    (23,8),(23,9),(23,17),(24,8),(24,9),(24,16),(24,17),
}

grid = {}

# All confirmed placements including new ones
PLACED = {
    'DORA': (4, 7, 'A'), 'ABASH': (4, 10, 'D'), 'ROTUNDA': (6, 13, 'D'),
    'PUSH': (7, 8, 'A'), 'HAFT': (8, 10, 'A'), 'ZIP': (11, 8, 'D'),
    'TRITE': (11, 9, 'D'), 'ADORN': (11, 12, 'A'), 'CIRCLEABOUT': (12, 7, 'A'),
    'PINTO': (13, 8, 'A'), 'TOLEDO': (14, 9, 'A'), 'DENVER': (14, 13, 'D'),
    'TONI': (16, 11, 'A'), 'TONER': (12, 17, 'D'), 'ACHOO': (13, 14, 'A'),
    'REGINA': (15, 16, 'A'), 'ERASE': (16, 16, 'A'),
}

for word, (r, c, d) in PLACED.items():
    for i, letter in enumerate(word):
        if d == 'A':
            grid[(r, c + i)] = letter
        else:
            grid[(r + i, c)] = letter

def get_cell(r, c):
    return grid.get((r, c), None)

# All entries
ENTRIES = [
    (1,'A',0,0,7), (8,'A',0,9,6), (14,'A',0,17,8),
    (22,'A',1,0,7), (23,'A',1,8,7), (24,'A',1,17,8),
    (25,'A',2,0,16), (28,'A',2,17,8),
    (29,'A',3,0,4), (30,'A',3,5,5), (31,'A',3,11,3), (32,'A',3,15,5), (34,'A',3,21,4),
    (35,'A',4,0,4), (36,'A',4,7,4), (38,'A',4,12,9), (41,'A',4,22,3),
    (42,'A',5,0,4), (43,'A',5,5,3), (45,'A',5,9,4), (47,'A',5,14,4), (48,'A',5,20,5),
    (50,'A',6,0,16), (54,'A',6,17,6),
    (57,'A',7,0,7), (58,'A',7,8,4), (59,'A',7,13,4), (61,'A',7,18,6),
    (63,'A',8,0,3), (64,'A',8,4,5), (66,'A',8,10,4), (68,'A',8,16,4), (70,'A',8,21,4),
    (72,'A',9,3,6), (73,'A',9,11,14),
    (77,'A',10,1,3), (79,'A',10,5,3), (80,'A',10,10,6), (81,'A',10,17,4), (82,'A',10,22,3),
    (83,'A',11,0,5), (85,'A',11,6,5), (88,'A',11,12,5), (90,'A',11,18,3), (91,'A',11,22,3),
    (92,'A',12,0,6), (94,'A',12,7,11), (97,'A',12,19,6),
    (99,'A',13,0,3), (100,'A',13,4,3), (102,'A',13,8,5), (103,'A',13,14,5), (105,'A',13,20,5),
    (106,'A',14,0,3), (107,'A',14,4,4), (109,'A',14,9,6), (111,'A',14,17,3), (113,'A',14,21,3),
    (114,'A',15,0,14), (117,'A',15,16,6),
    (119,'A',16,0,4), (120,'A',16,5,4), (121,'A',16,11,4), (123,'A',16,16,5), (124,'A',16,22,3),
    (127,'A',17,1,6), (129,'A',17,8,4), (132,'A',17,13,4), (134,'A',17,18,7),
    (136,'A',18,2,6), (138,'A',18,9,16),
    (141,'A',19,0,5), (143,'A',19,7,4), (145,'A',19,12,4), (146,'A',19,17,3), (147,'A',19,21,4),
    (148,'A',20,0,3), (149,'A',20,4,9), (153,'A',20,14,4), (155,'A',20,21,4),
    (156,'A',21,0,4), (158,'A',21,5,5), (159,'A',21,11,3), (161,'A',21,15,5), (164,'A',21,21,4),
    (165,'A',22,0,8), (167,'A',22,9,16),
    (171,'A',23,0,8), (172,'A',23,10,7), (173,'A',23,18,7),
    (174,'A',24,0,8), (175,'A',24,10,6), (176,'A',24,18,7),
    (1,'D',0,0,9), (2,'D',0,1,9), (3,'D',0,2,9), (4,'D',0,3,8), (5,'D',0,4,3), (6,'D',0,5,4), (7,'D',0,6,4),
    (8,'D',0,9,8), (9,'D',0,10,3), (10,'D',0,11,4), (11,'D',0,12,7), (12,'D',0,13,5), (13,'D',0,14,3),
    (14,'D',0,17,7), (15,'D',0,18,5), (16,'D',0,19,5), (17,'D',0,20,3), (18,'D',0,21,4), (19,'D',0,22,15), (20,'D',0,23,6), (21,'D',0,24,6),
    (23,'D',1,8,4), (26,'D',2,7,5), (27,'D',2,15,6), (33,'D',3,16,3),
    (37,'D',4,10,5), (39,'D',4,14,4), (40,'D',4,20,4),
    (43,'D',5,5,6), (44,'D',5,6,7), (46,'D',5,11,6), (49,'D',5,21,5),
    (51,'D',6,4,4), (52,'D',6,8,4), (53,'D',6,13,7), (55,'D',6,18,6), (56,'D',6,19,7),
    (60,'D',7,16,3), (62,'D',7,23,8),
    (65,'D',8,7,5), (67,'D',8,12,9), (69,'D',8,17,3), (71,'D',8,24,6),
    (72,'D',9,3,4), (74,'D',9,14,6), (75,'D',9,15,5), (76,'D',9,20,5),
    (77,'D',10,1,8), (78,'D',10,2,15), (80,'D',10,10,6), (83,'D',11,0,6), (84,'D',11,4,5),
    (86,'D',11,8,3), (87,'D',11,9,5), (89,'D',11,16,3), (93,'D',12,5,7), (95,'D',12,11,7), (96,'D',12,17,5), (98,'D',12,21,4),
    (101,'D',13,6,6), (104,'D',13,18,7), (108,'D',14,7,3), (110,'D',14,13,6), (112,'D',14,19,6),
    (115,'D',15,3,5), (116,'D',15,8,3), (117,'D',15,16,4), (118,'D',15,20,4),
    (122,'D',16,14,5), (124,'D',16,22,9), (125,'D',16,23,9), (126,'D',16,24,9),
    (128,'D',17,4,4), (130,'D',17,9,6), (131,'D',17,10,4), (133,'D',17,15,8), (135,'D',17,21,8),
    (137,'D',18,7,7), (139,'D',18,12,7), (140,'D',18,17,5),
    (141,'D',19,0,6), (142,'D',19,1,6), (144,'D',19,8,3),
    (150,'D',20,5,5), (151,'D',20,6,5), (152,'D',20,11,5), (154,'D',20,16,4),
    (157,'D',21,3,4), (160,'D',21,13,4), (162,'D',21,18,4), (163,'D',21,19,4),
    (166,'D',22,4,3), (168,'D',22,10,3), (169,'D',22,14,3), (170,'D',22,20,3),
]

# Placed entry keys
placed_keys = set()
for word, (r, c, d) in PLACED.items():
    for num, dd, rr, cc, ll in ENTRIES:
        if dd == d and rr == r and cc == c and ll == len(word):
            placed_keys.add((num, dd))
            break

def get_entry_state(num, d, r, c, l):
    cells = []
    for i in range(l):
        if d == 'A':
            cells.append(get_cell(r, c + i))
        else:
            cells.append(get_cell(r + i, c))
    return cells

def word_fits(word, state):
    if len(word) != len(state):
        return False
    for w, s in zip(word, state):
        if s is not None and w != s:
            return False
    return True

# ============================================================
# CONFIRMED ANSWERS BY LENGTH
# ============================================================

answers_8 = [
    'HOODWINK', 'HULAHOOP', 'SCENARIO', 'NEUROTIC', 'SCREENER', 'ABSOLUTE',
    'TEAMSEAS', 'DURATION', 'CARBLITE', 'POSITRON', 'ROUTINES', 'FLAMINGO', 'ADELAIDE',
    # 'CASHTENT' excluded (lower confidence)
]

answers_9 = [
    'HOOVERDAM', 'ROBINHOOD', 'DITHERING', 'HOWITZERS', 'HIGHHEELS', 'ALLUSIONS',
    'RESISTIVE', 'INUNDATOR', 'CABRIOLET', 'RATPOISON', 'OUTLINERS',
    'OWENSBORO', 'ANNAPOLIS', 'ROCHESTER',
]

answers_7 = [
    'TYPHOON', 'HEARTED', 'MUSTERS', 'CALIBER', 'PORTION', 'INUTERO',
    'QUORUMS', 'HIRPLED', 'TORONTO', 'ROSWELL', 'DRESDEN', 'SEVILLE', 'ORLANDO', 'WOODWAY',
    # ROTUNDA already placed
]

answers_6 = [
    'SCHOOL', 'OHIOAN', 'HOODIE', 'MATTER', 'ECLAIR', 'OPTION', 'ORIENT',
    'CHAIRS', 'CONVEX', 'AUBURN', 'OTTAWA', 'WARSAW',
    # TOLEDO, DENVER, REGINA already placed
]

answers_5 = [
    'OPERA', 'LECAR', 'TONER', 'ACCRA', 'DOVER', 'TEMPE',
    # ACHOO, ABASH, ERASE, TRITE, ADORN, PINTO already placed
]

# ============================================================
# CHECK ALL SLOTS FOR EACH LENGTH
# ============================================================

print("=" * 70)
print("8-LETTER SLOTS (12 total) vs 13 ANSWERS")
print("=" * 70)

slots_8 = [(num, d, r, c, l) for num, d, r, c, l in ENTRIES if l == 8 and (num, d) not in placed_keys]
print(f"\nUnfilled 8-letter slots: {len(slots_8)}")

for num, d, r, c, l in slots_8:
    state = get_entry_state(num, d, r, c, l)
    constrained = sum(1 for s in state if s is not None)
    state_str = ''.join(s if s else '.' for s in state)
    fitting = [w for w in answers_8 if word_fits(w, state)]
    if constrained > 0 or len(fitting) < len(answers_8):
        marker = " ← UNIQUE!" if len(fitting) == 1 else ""
        print(f"  {num}{d} [{state_str}] ({constrained} constraints): {fitting}{marker}")

print(f"\n{'=' * 70}")
print("9-LETTER SLOTS (9 total) vs 14 ANSWERS")
print(f"{'=' * 70}")

slots_9 = [(num, d, r, c, l) for num, d, r, c, l in ENTRIES if l == 9 and (num, d) not in placed_keys]
print(f"\nUnfilled 9-letter slots: {len(slots_9)}")

for num, d, r, c, l in slots_9:
    state = get_entry_state(num, d, r, c, l)
    constrained = sum(1 for s in state if s is not None)
    state_str = ''.join(s if s else '.' for s in state)
    fitting = [w for w in answers_9 if word_fits(w, state)]
    if constrained > 0:
        marker = " ← UNIQUE!" if len(fitting) == 1 else ""
        print(f"  {num}{d} [{state_str}] ({constrained} constraints): {fitting}{marker}")
    else:
        print(f"  {num}{d} [{state_str}] (0 constraints): all 14 fit")

print(f"\n{'=' * 70}")
print("7-LETTER SLOTS (17 unfilled) vs 14 ANSWERS")
print(f"{'=' * 70}")

slots_7 = [(num, d, r, c, l) for num, d, r, c, l in ENTRIES if l == 7 and (num, d) not in placed_keys]
print(f"\nUnfilled 7-letter slots: {len(slots_7)}")

for num, d, r, c, l in slots_7:
    state = get_entry_state(num, d, r, c, l)
    constrained = sum(1 for s in state if s is not None)
    state_str = ''.join(s if s else '.' for s in state)
    if constrained > 0:
        fitting = [w for w in answers_7 if word_fits(w, state)]
        marker = " ← UNIQUE!" if len(fitting) == 1 else ""
        if fitting:
            print(f"  {num}{d} [{state_str}] ({constrained} constraints): {fitting}{marker}")
        else:
            print(f"  {num}{d} [{state_str}] ({constrained} constraints): NO MATCHES")

print(f"\n{'=' * 70}")
print("6-LETTER SLOTS (25 unfilled) vs 12 ANSWERS")
print(f"{'=' * 70}")

slots_6 = [(num, d, r, c, l) for num, d, r, c, l in ENTRIES if l == 6 and (num, d) not in placed_keys]

for num, d, r, c, l in slots_6:
    state = get_entry_state(num, d, r, c, l)
    constrained = sum(1 for s in state if s is not None)
    state_str = ''.join(s if s else '.' for s in state)
    if constrained > 0:
        fitting = [w for w in answers_6 if word_fits(w, state)]
        if fitting:
            marker = " ← UNIQUE!" if len(fitting) == 1 else ""
            print(f"  {num}{d} [{state_str}] ({constrained} constraints): {fitting}{marker}")

print(f"\n{'=' * 70}")
print("5-LETTER SLOTS (28 unfilled) vs 6 ANSWERS")
print(f"{'=' * 70}")

slots_5 = [(num, d, r, c, l) for num, d, r, c, l in ENTRIES if l == 5 and (num, d) not in placed_keys]

for num, d, r, c, l in slots_5:
    state = get_entry_state(num, d, r, c, l)
    constrained = sum(1 for s in state if s is not None)
    state_str = ''.join(s if s else '.' for s in state)
    if constrained > 0:
        fitting = [w for w in answers_5 if word_fits(w, state)]
        if fitting:
            marker = " ← UNIQUE!" if len(fitting) == 1 else ""
            print(f"  {num}{d} [{state_str}] ({constrained} constraints): {fitting}{marker}")

# ============================================================
# P4 cities placement analysis
# ============================================================
print(f"\n{'=' * 70}")
print("P4 CITIES PLACEMENT ANALYSIS")
print(f"{'=' * 70}")

p4_cities = {
    5: ['TEMPE', 'DOVER'],
    6: ['REGINA', 'TOLEDO', 'DENVER', 'AUBURN', 'OTTAWA', 'WARSAW'],
    7: ['TORONTO', 'ROSWELL', 'DRESDEN', 'SEVILLE', 'ORLANDO', 'WOODWAY'],
    8: ['ADELAIDE'],
    9: ['OWENSBORO', 'ANNAPOLIS', 'ROCHESTER'],
}

placed_cities = {'TOLEDO', 'DENVER', 'REGINA'}

for length, cities in sorted(p4_cities.items()):
    for city in cities:
        if city in placed_cities:
            continue
        slots = [(num, d, r, c, l) for num, d, r, c, l in ENTRIES
                 if l == length and (num, d) not in placed_keys]
        constrained_fits = []
        unconstrained_fits = []
        for num, d, r, c, l in slots:
            state = get_entry_state(num, d, r, c, l)
            constrained = sum(1 for s in state if s is not None)
            if word_fits(city, state):
                if constrained > 0:
                    state_str = ''.join(s if s else '.' for s in state)
                    constrained_fits.append(f"{num}{d}[{state_str}]({constrained})")
                else:
                    unconstrained_fits.append(f"{num}{d}")
        total = len(constrained_fits) + len(unconstrained_fits)
        if constrained_fits:
            print(f"  {city:12s} ({length}): {total} slots | Constrained: {constrained_fits}")
        elif total <= 3:
            print(f"  {city:12s} ({length}): {total} slots only → {unconstrained_fits}")

# ============================================================
# SPECIAL: Try SANJUAN (7 letters, no space)
# ============================================================
print(f"\n{'=' * 70}")
print("SPECIAL: SANJUAN (7 letters)")
print(f"{'=' * 70}")
city = "SANJUAN"
slots = [(num, d, r, c, l) for num, d, r, c, l in ENTRIES
         if l == 7 and (num, d) not in placed_keys]
for num, d, r, c, l in slots:
    state = get_entry_state(num, d, r, c, l)
    constrained = sum(1 for s in state if s is not None)
    if word_fits(city, state) and constrained > 0:
        state_str = ''.join(s if s else '.' for s in state)
        print(f"  {num}{d} [{state_str}] ({constrained} constraints): FITS")

# ============================================================
# ANALYSIS: Entries where ONLY one answer fits
# ============================================================
print(f"\n{'=' * 70}")
print("ENTRIES WITH UNIQUE ANSWER (from all confirmed answers)")
print(f"{'=' * 70}")

all_answers_by_len = {
    3: ['RAD', 'EAR', 'ION', 'EON'],  # ZIP placed
    4: ['DHOW', 'RACE', 'NOTE'],  # DORA, HAFT, TONI, PUSH placed
    5: answers_5,
    6: answers_6,
    7: answers_7,
    8: answers_8,
    9: answers_9,
}

for num, d, r, c, l in ENTRIES:
    if (num, d) in placed_keys:
        continue
    state = get_entry_state(num, d, r, c, l)
    constrained = sum(1 for s in state if s is not None)
    if constrained == 0:
        continue

    fitting = [w for w in all_answers_by_len.get(l, []) if word_fits(w, state)]
    if len(fitting) == 1:
        state_str = ''.join(s if s else '.' for s in state)
        print(f"  {num}{d} [{state_str}] → UNIQUE: {fitting[0]}")
    elif len(fitting) == 2:
        state_str = ''.join(s if s else '.' for s in state)
        print(f"  {num}{d} [{state_str}] → 2 options: {fitting}")
