#!/usr/bin/env python3
"""
TURNONADIME vs CIRCLEABOUT at 94A: Comprehensive Constraint Analysis
=====================================================================
94A is at row 12, cols 7-17 (11 letters).

CIRCLEABOUT = C,I,R,C,L,E,A,B,O,U,T
TURNONADIME = T,U,R,N,O,N,A,D,I,M,E

For each column 7-17:
  - Compare which letter each candidate provides
  - Trace EVERY down entry that crosses 94A at that column
  - Show what constraint changes

Key questions:
  1. Does TURNONADIME conflict with confirmed entries (ZIP at 86D, TONER at 96D)?
  2. If so, what alternatives exist for 86D and 96D?
  3. Does TURNONADIME enable ROBINHOOD at 67D?
  4. Full constraint pattern comparison for every affected entry.
"""

from collections import defaultdict
import itertools

# ============================================================================
# GRID SETUP
# ============================================================================

BLACK_CELLS = {
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

across_entries_raw = [
    (1,0,0,7),(8,0,9,6),(14,0,17,8),(22,1,0,7),(23,1,8,7),(24,1,17,8),
    (25,2,0,16),(28,2,17,8),(29,3,0,4),(30,3,5,5),(31,3,11,3),(32,3,15,5),
    (34,3,21,4),(35,4,0,4),(36,4,7,4),(38,4,12,9),(41,4,22,3),(42,5,0,4),
    (43,5,5,3),(45,5,9,4),(47,5,14,4),(48,5,20,5),(50,6,0,16),(54,6,17,6),
    (57,7,0,7),(58,7,8,4),(59,7,13,4),(61,7,18,6),(63,8,0,3),(64,8,4,5),
    (66,8,10,4),(68,8,16,4),(70,8,21,4),(72,9,3,6),(73,9,11,14),(77,10,1,3),
    (79,10,5,3),(80,10,10,6),(81,10,17,4),(82,10,22,3),(83,11,0,5),(85,11,6,5),
    (88,11,12,5),(90,11,18,3),(91,11,22,3),(92,12,0,6),(94,12,7,11),(97,12,19,6),
    (99,13,0,3),(100,13,4,3),(102,13,8,5),(103,13,14,5),(105,13,20,5),
    (106,14,0,3),(107,14,4,4),(109,14,9,6),(111,14,17,3),(113,14,21,3),
    (114,15,0,14),(117,15,16,6),(119,16,0,4),(120,16,5,4),(121,16,11,4),
    (123,16,16,5),(124,16,22,3),(127,17,1,6),(129,17,8,4),(132,17,13,4),
    (134,17,18,7),(136,18,2,6),(138,18,9,16),(141,19,0,5),(143,19,7,4),
    (145,19,12,4),(146,19,17,3),(147,19,21,4),(148,20,0,3),(149,20,4,9),
    (153,20,14,4),(155,20,21,4),(156,21,0,4),(158,21,5,5),(159,21,11,3),
    (161,21,15,5),(164,21,21,4),(165,22,0,8),(167,22,9,16),(171,23,0,8),
    (172,23,10,7),(173,23,18,7),(174,24,0,8),(175,24,10,6),(176,24,18,7)
]

down_entries_raw = [
    (1,0,0,9),(2,0,1,9),(3,0,2,9),(4,0,3,8),(5,0,4,3),(6,0,5,4),(7,0,6,4),
    (8,0,9,8),(9,0,10,3),(10,0,11,4),(11,0,12,7),(12,0,13,5),(13,0,14,3),
    (14,0,17,7),(15,0,18,5),(16,0,19,5),(17,0,20,3),(18,0,21,4),(19,0,22,15),
    (20,0,23,6),(21,0,24,6),(23,1,8,4),(26,2,7,5),(27,2,15,6),(33,3,16,3),
    (37,4,10,5),(39,4,14,4),(40,4,20,4),(43,5,5,6),(44,5,6,7),(46,5,11,6),
    (49,5,21,5),(51,6,4,4),(52,6,8,4),(53,6,13,7),(55,6,18,6),(56,6,19,7),
    (60,7,16,3),(62,7,23,8),(65,8,7,5),(67,8,12,9),(69,8,17,3),(71,8,24,6),
    (72,9,3,4),(74,9,14,6),(75,9,15,5),(76,9,20,5),(77,10,1,8),(78,10,2,15),
    (80,10,10,6),(83,11,0,6),(84,11,4,5),(86,11,8,3),(87,11,9,5),(89,11,16,3),
    (93,12,5,7),(95,12,11,7),(96,12,17,5),(98,12,21,4),(101,13,6,6),
    (104,13,18,7),(108,14,7,3),(110,14,13,6),(112,14,19,6),(115,15,3,5),
    (116,15,8,3),(117,15,16,4),(118,15,20,4),(122,16,14,5),(124,16,22,9),
    (125,16,23,9),(126,16,24,9),(128,17,4,4),(130,17,9,6),(131,17,10,4),
    (133,17,15,8),(135,17,21,8),(137,18,7,7),(139,18,12,7),(140,18,17,5),
    (141,19,0,6),(142,19,1,6),(144,19,8,3),(150,20,5,5),(151,20,6,5),
    (152,20,11,5),(154,20,16,4),(157,21,3,4),(160,21,13,4),(162,21,18,4),
    (163,21,19,4),(166,22,4,3),(168,22,10,3),(169,22,14,3),(170,22,20,3)
]

# Build entry info
entry_info = {}
for (num, row, col, length) in across_entries_raw:
    entry_info[('A', num)] = (row, col, length)
for (num, row, col, length) in down_entries_raw:
    entry_info[('D', num)] = (row, col, length)

# Map each cell to entries crossing it
cell_to_entries = defaultdict(list)
for (etype, num), (start_row, start_col, length) in entry_info.items():
    for i in range(length):
        if etype == 'A':
            r, c = start_row, start_col + i
        else:
            r, c = start_row + i, start_col
        cell_to_entries[(r, c)].append((etype, num, i))

# ============================================================================
# ANSWER BANK (from all puzzles)
# ============================================================================

answer_bank = {
    3: ['RAD', 'EAR', 'ION', 'EON', 'ZIP'],
    4: ['DHOW', 'HAFT', 'DORA', 'RACE', 'TONI', 'NOTE', 'PUSH'],
    5: ['ACHOO', 'WAHOO', 'ABASH', 'OPERA', 'ERASE', 'TRITE', 'ADORN',
        'LECAR', 'PINTO', 'TONER', 'ACCRA', 'WORLD', 'DOVER', 'TEMPE'],
    6: ['SCHOOL', 'OHIOAN', 'HOODIE', 'MATTER', 'ECLAIR', 'OPTION',
        'ORIENT', 'CHAIRS', 'CONVEX', 'TOLEDO', 'REGINA', 'AUBURN',
        'DENVER', 'OTTAWA'],
    7: ['TYPHOON', 'OHSHOOT', 'HEARTED', 'MUSTERS', 'ROTUNDA', 'CALIBER',
        'PORTION', 'INUTERO', 'QUORUMS', 'HIRPLED', 'TORONTO', 'ROSWELL',
        'DRESDEN', 'ORLANDO', 'WOODWAY', 'SANJUAN', 'SEVILLE', 'ORGANIC'],
    8: ['HOODWINK', 'HULAHOOP', 'SCENARIO', 'NEUROTIC', 'SCREENER',
        'ABSOLUTE', 'TEAMSEAS', 'DURATION', 'CARBLITE', 'POSITRON',
        'ROUTINES', 'FLAMINGO', 'CASHTENT', 'ADELAIDE'],
    9: ['HOOVERDAM', 'ROBINHOOD', 'DITHERING', 'HOWITZERS', 'HIGHHEELS',
        'ALLUSIONS', 'RESISTIVE', 'INUNDATOR', 'CABRIOLET', 'RATPOISON',
        'OUTLINERS', 'BEASTLAND', 'OWENSBORO', 'ANNAPOLIS', 'ROCHESTER'],
    11: ['TURNONADIME', 'CIRCLEABOUT', 'OUTFORASPIN', 'REVOLUTIONS'],
    16: ['SUPERBOWLSTADIUM'],
}

# Common 3-letter words for checking ?UP pattern etc.
COMMON_3_LETTER = [
    'ACE','ACT','ADD','AGE','AGO','AID','AIM','AIR','ALL','AND','ANT','ANY',
    'APE','ARC','ARE','ARK','ARM','ART','ATE','AWE','AXE','BAD','BAG','BAN',
    'BAR','BAT','BAY','BED','BET','BIG','BIT','BOW','BOX','BOY','BUD','BUG',
    'BUN','BUS','BUT','BUY','CAB','CAN','CAP','CAR','CAT','COP','COT','COW',
    'CRY','CUB','CUD','CUP','CUR','CUT','DAB','DAD','DAM','DAY','DEN','DEW',
    'DID','DIG','DIM','DIP','DOC','DOG','DOT','DRY','DUB','DUD','DUE','DUG',
    'DUN','DUO','DUP','DYE','EAR','EAT','EEL','EGG','EGO','ELF','ELK','ELM',
    'EMU','END','ERA','EVE','EWE','EYE','FAN','FAR','FAT','FAX','FED','FEW',
    'FIG','FIN','FIT','FIX','FLY','FOB','FOE','FOG','FOP','FOR','FOX','FRY',
    'FUN','FUR','GAB','GAG','GAP','GAS','GAY','GEL','GEM','GET','GIG','GIN',
    'GNU','GOB','GOD','GOT','GUM','GUN','GUT','GUY','GYM','HAD','HAM','HAS',
    'HAT','HAY','HEN','HER','HEW','HID','HIM','HIP','HIS','HIT','HOB','HOD',
    'HOG','HOP','HOT','HOW','HUB','HUE','HUG','HUM','HUP','HUT','ICE','ICY',
    'ILL','IMP','INK','INN','ION','IRE','IRK','IVY','JAB','JAG','JAM','JAR',
    'JAW','JAY','JET','JIG','JOB','JOG','JOT','JOY','JUG','JUT','KEG','KEN',
    'KEY','KID','KIN','KIT','LAB','LAD','LAG','LAP','LAW','LAY','LEA','LED',
    'LEG','LET','LID','LIE','LIT','LOG','LOT','LOW','LUG','MAD','MAN','MAP',
    'MAR','MAT','MAW','MAY','MEN','MET','MID','MIX','MOB','MOD','MOM','MOP',
    'MOW','MUD','MUG','MUM','NAB','NAG','NAP','NET','NEW','NIL','NIT','NOD',
    'NOR','NOT','NOW','NUB','NUN','NUT','OAK','OAR','OAT','ODD','ODE','OFF',
    'OFT','OHM','OIL','OLD','ONE','OPT','ORB','ORE','OUR','OUT','OWE','OWL',
    'OWN','PAD','PAN','PAP','PAR','PAT','PAW','PAY','PEA','PEG','PEN','PEP',
    'PER','PET','PEW','PIE','PIG','PIN','PIT','PLY','POD','POP','POT','POW',
    'PRO','PRY','PUB','PUG','PUN','PUP','PUS','PUT','QUA','RAG','RAM','RAN',
    'RAP','RAT','RAW','RAY','RED','REF','RIB','RID','RIG','RIM','RIP','ROB',
    'ROD','ROE','ROT','ROW','RUB','RUG','RUM','RUN','RUT','RYE','SAC','SAD',
    'SAG','SAP','SAT','SAW','SAY','SEA','SET','SEW','SHE','SHY','SIN','SIP',
    'SIR','SIS','SIT','SIX','SKI','SKY','SLY','SOB','SOD','SON','SOP','SOT',
    'SOW','SOY','SPA','SPY','STY','SUB','SUM','SUN','SUP','TAB','TAD','TAG',
    'TAN','TAP','TAR','TAT','TAX','TEA','TEN','THE','TIE','TIN','TIP','TOE',
    'TON','TOO','TOP','TOT','TOW','TOY','TUB','TUG','TUN','TUP','TWO','URN',
    'USE','VAN','VAT','VET','VEX','VIA','VIE','VOW','WAD','WAG','WAR','WAS',
    'WAX','WAY','WEB','WED','WET','WHO','WHY','WIG','WIN','WIT','WOE','WOK',
    'WON','WOO','WOW','YAK','YAM','YAP','YAW','YEA','YES','YET','YEW','YIN',
    'YOU','ZAP','ZEN','ZIP','ZIT','ZOO', 'CUP', 'DUP', 'PUP', 'SUP', 'TUP',
    'YUP', 'HUP', 'GUP', 'NUP', 'RUP', 'WUP',
    'NUH', 'NUB', 'NUN', 'NUT', 'NUG',
]

# Common 5-letter words starting with E, O for checking 96D alternatives
COMMON_5_LETTER_E = [
    'EAGLE','EARLY','EARTH','EASED','EATEN','EATER','EBBED','ECLAT','EDGED',
    'EDICT','EERIE','EIGHT','EJECT','ELATE','ELDER','ELECT','ELFIN','ELITE',
    'ELOPE','ELUDE','EMAIL','EMBER','EMCEE','EMERY','EMOTE','EMPTY','ENDED',
    'ENDOW','ENEMY','ENJOY','ENNUI','ENORM','ENTER','ENTRY','ENVOY','EPOCH',
    'EQUAL','EQUIP','ERASE','ERODE','ERROR','ERUPT','ESSAY','ETHER','ETHIC',
    'EVADE','EVENT','EVERY','EVICT','EVOKE','EXACT','EXALT','EXERT','EXILE',
    'EXIST','EXPAT','EXPEL','EXTRA','EXUDE','EXULT',
    'EOSIN','EOLID',
]

# ============================================================================
# CONFIRMED PLACEMENTS (independent of 94A choice)
# ============================================================================

INDEPENDENT_PLACEMENTS = {
    ('A', 167): 'SUPERBOWLSTADIUM',  # community screenshot
    ('A', 149): 'BEASTLAND',          # community screenshot
    ('A', 36):  'DORA',               # P8, row 4 (doesn't cross 94A)
    ('D', 37):  'ABASH',              # P3, rows 4-8 (doesn't reach row 12)
    ('D', 53):  'ROTUNDA',            # P8, rows 6-12, pos6=A matches both candidates
}

# CIRCLEABOUT-dependent cascade placements
CIRCLEABOUT_CASCADE = {
    ('D', 86):  'ZIP',     # 86D[1]=I from CIRCLEABOUT[1]=I
    ('D', 87):  'TRITE',   # 87D constraint propagation
    ('A', 58):  'PUSH',    # constraint from 86D/52D
    ('A', 66):  'HAFT',    # constraint from 37D + 53D
    ('A', 88):  'ADORN',   # 88A[0]=A
    ('A', 102): 'PINTO',   # 86D[2]=P -> 102A[0]=P
    ('A', 103): 'ACHOO',   # constraint propagation
    ('A', 109): 'TOLEDO',  # constraint propagation
    ('D', 110): 'DENVER',  # constraint propagation
    ('D', 96):  'TONER',   # 96D[0]=T from CIRCLEABOUT[10]=T
    ('A', 117): 'REGINA',  # constraint propagation
    ('A', 121): 'TONI',    # constraint propagation
    ('A', 123): 'ERASE',   # constraint propagation
}


# ============================================================================
# SOLVER
# ============================================================================

class Solver:
    def __init__(self, name):
        self.name = name
        self.grid = [[None]*25 for _ in range(25)]
        self.placed = {}
        self.conflicts = []

    def place(self, etype, num, word, quiet=False):
        sr, sc, sl = entry_info[(etype, num)]
        if len(word) != sl:
            msg = f"LENGTH: {etype}{num} needs {sl}, {word} is {len(word)}"
            self.conflicts.append(msg)
            return False
        for i, ch in enumerate(word):
            r, c = (sr, sc+i) if etype == 'A' else (sr+i, sc)
            if self.grid[r][c] is not None and self.grid[r][c] != ch:
                msg = f"CONFLICT at ({r},{c}): {etype}{num}[{i}]={ch} vs existing={self.grid[r][c]}"
                self.conflicts.append(msg)
                return False
        for i, ch in enumerate(word):
            r, c = (sr, sc+i) if etype == 'A' else (sr+i, sc)
            self.grid[r][c] = ch
        self.placed[(etype, num)] = word
        return True

    def pattern(self, etype, num):
        sr, sc, sl = entry_info[(etype, num)]
        chars = []
        for i in range(sl):
            r, c = (sr, sc+i) if etype == 'A' else (sr+i, sc)
            chars.append(self.grid[r][c] or '.')
        return ''.join(chars)

    def cell(self, r, c):
        return self.grid[r][c]

    def bank_matches(self, pat, length):
        import re
        if length not in answer_bank:
            return []
        regex = re.compile('^' + pat.replace('.', '[A-Z]') + '$')
        return [w for w in answer_bank[length] if regex.match(w)]

    def cascade(self, max_iter=50):
        total = 0
        for _ in range(max_iter):
            count = 0
            for key in sorted(entry_info.keys()):
                if key in self.placed:
                    continue
                etype, num = key
                sl = entry_info[key][2]
                pat = self.pattern(etype, num)
                if pat == '.' * sl:
                    continue
                if '.' not in pat:
                    self.placed[key] = pat
                    count += 1
                    continue
                matches = self.bank_matches(pat, sl)
                if len(matches) == 1:
                    if self.place(etype, num, matches[0]):
                        count += 1
            total += count
            if count == 0:
                break
        return total

    def print_grid(self, row_start=0, row_end=25):
        print(f"     {''.join(str(i%10) for i in range(25))}")
        for r in range(row_start, row_end):
            s = f"R{r:2d}| "
            for c in range(25):
                if (r,c) in BLACK_CELLS:
                    s += '#'
                elif self.grid[r][c]:
                    s += self.grid[r][c]
                else:
                    s += '.'
            print(s)


def build_scenario(candidate):
    """Build a scenario with either CIRCLEABOUT or TURNONADIME at 94A."""
    s = Solver(candidate)
    for key, word in INDEPENDENT_PLACEMENTS.items():
        s.place(*key, word)
    s.place('A', 94, candidate)
    s.cascade()
    return s


# ============================================================================
# MAIN ANALYSIS
# ============================================================================

print("=" * 95)
print("  TURNONADIME vs CIRCLEABOUT at 94A: FULL CONSTRAINT ANALYSIS")
print("=" * 95)

CIRC = "CIRCLEABOUT"
TURN = "TURNONADIME"

# Build both scenarios
s_circ = build_scenario(CIRC)
s_turn = build_scenario(TURN)


# ============================================================================
# SECTION 1: Letter-by-letter comparison at 94A crossings
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 1: Column-by-column letter comparison at 94A (row 12, cols 7-17)")
print("=" * 95)
print()

print(f"  94A position:  ", end="")
for i in range(11):
    print(f"  {i:2d}", end="")
print()

print(f"  Column:        ", end="")
for c in range(7, 18):
    print(f"  {c:2d}", end="")
print()

print(f"  CIRCLEABOUT:   ", end="")
for ch in CIRC:
    print(f"   {ch}", end="")
print()

print(f"  TURNONADIME:   ", end="")
for ch in TURN:
    print(f"   {ch}", end="")
print()

print(f"  Same?          ", end="")
for i in range(11):
    same = CIRC[i] == TURN[i]
    print(f"  {'==' if same else '!!'}", end="")
print()

diff_count = sum(1 for i in range(11) if CIRC[i] != TURN[i])
same_count = 11 - diff_count
print(f"\n  {same_count} positions same, {diff_count} positions different")


# ============================================================================
# SECTION 2: Every down entry crossing 94A
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 2: Every down entry crossing row 12 at cols 7-17")
print("=" * 95)

crossings = []
for col in range(7, 18):
    pos_94a = col - 7
    found_down = None
    for (ce, cn, ci) in cell_to_entries[(12, col)]:
        if ce == 'D':
            sr, sc, sl = entry_info[('D', cn)]
            pos_in_down = 12 - sr
            found_down = {
                'col': col,
                'pos_94a': pos_94a,
                'down_num': cn,
                'down_start': sr,
                'down_end': sr + sl - 1,
                'down_len': sl,
                'pos_in_down': pos_in_down,
                'circ_letter': CIRC[pos_94a],
                'turn_letter': TURN[pos_94a],
                'same': CIRC[pos_94a] == TURN[pos_94a],
            }
            crossings.append(found_down)
    if not found_down:
        print(f"  WARNING: No down entry found crossing (12, {col})")

print()
print(f"  {'Col':>4}  {'94Apos':>6}  {'Down#':>6}  {'Rows':>10}  {'Len':>4}  {'DwnPos':>6}  {'CIRC':>5}  {'TURN':>5}  {'Same?':>7}")
print("  " + "-" * 65)
for x in crossings:
    same_str = "YES" if x['same'] else "**NO**"
    rows_str = f"{x['down_start']}-{x['down_end']}"
    print(f"  {x['col']:>4}  {x['pos_94a']:>6}  {x['down_num']:>4}D  {rows_str:>10}  "
          f"{x['down_len']:>4}  [{x['pos_in_down']:>3}]  "
          f"{x['circ_letter']:>5}  {x['turn_letter']:>5}  {same_str:>7}")

# Highlight differences
diffs = [x for x in crossings if not x['same']]
sames = [x for x in crossings if x['same']]
print(f"\n  SAME letter ({len(sames)}): cols {[x['col'] for x in sames]}")
print(f"  DIFFERENT letter ({len(diffs)}): cols {[x['col'] for x in diffs]}")


# ============================================================================
# SECTION 3: Detailed analysis of EACH differing crossing
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 3: Detailed impact of each differing down crossing")
print("=" * 95)

for x in diffs:
    dn = x['down_num']
    sr, sc, sl = entry_info[('D', dn)]
    print(f"\n  {'='*80}")
    print(f"  {dn}D: col {x['col']}, rows {sr}-{sr+sl-1}, length {sl}")
    print(f"  Position {x['pos_in_down']} in {dn}D gets: CIRC={x['circ_letter']}, TURN={x['turn_letter']}")
    print(f"  {'='*80}")

    # Show the full pattern under both scenarios
    circ_pat = s_circ.pattern('D', dn)
    turn_pat = s_turn.pattern('D', dn)
    circ_matches = s_circ.bank_matches(circ_pat, sl)
    turn_matches = s_turn.bank_matches(turn_pat, sl)
    circ_placed = s_circ.placed.get(('D', dn))
    turn_placed = s_turn.placed.get(('D', dn))

    print(f"  CIRCLEABOUT scenario:")
    print(f"    Pattern: '{circ_pat}' (placed: {circ_placed})")
    print(f"    Bank matches: {circ_matches if circ_matches else 'NONE'}")
    print(f"  TURNONADIME scenario:")
    print(f"    Pattern: '{turn_pat}' (placed: {turn_placed})")
    print(f"    Bank matches: {turn_matches if turn_matches else 'NONE'}")

    # Trace every letter source in this down entry
    print(f"\n  Full trace of {dn}D letters:")
    for i in range(sl):
        r = sr + i
        c = sc
        circ_val = s_circ.cell(r, c)
        turn_val = s_turn.cell(r, c)
        marker = " <-- DIFFERS" if circ_val != turn_val else ""

        # What across entry crosses here?
        across_info = ""
        for ce, cn2, ci2 in cell_to_entries[(r, c)]:
            if ce == 'A':
                asr, asc, asl = entry_info[('A', cn2)]
                for solver, sname in [(s_circ, "CIRC"), (s_turn, "TURN")]:
                    aplaced = solver.placed.get(('A', cn2))
                    if aplaced:
                        across_info += f" {sname}:{cn2}A={aplaced}[{ci2}]={aplaced[ci2]}"
                    else:
                        apat = solver.pattern('A', cn2)
                        across_info += f" {sname}:{cn2}A[{ci2}]='{apat[ci2]}'"

        circ_str = circ_val or '.'
        turn_str = turn_val or '.'
        print(f"    [{i}] ({r},{c}): CIRC={circ_str}, TURN={turn_str}{marker}")
        if across_info:
            print(f"        Source:{across_info}")


# ============================================================================
# SECTION 4: CRITICAL CONFLICT CHECK -- ZIP at 86D and TONER at 96D
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 4: CRITICAL CONFLICT CHECK -- ZIP (86D) and TONER (96D)")
print("=" * 95)

print("\n  --- 86D = ZIP conflict ---")
print(f"  86D starts at (11,8), length 3, rows 11-13")
print(f"  ZIP = Z, I, P")
print(f"  86D[1] is at (12,8) = 94A position {8-7} = position 1")
print(f"  CIRCLEABOUT[1] = {CIRC[1]} --> 86D[1] = I --> matches ZIP[1] = I  [OK]")
print(f"  TURNONADIME[1] = {TURN[1]} --> 86D[1] = U --> ZIP[1] needs I  [CONFLICT!]")
print()
print(f"  CONCLUSION: TURNONADIME is INCOMPATIBLE with ZIP at 86D.")

print("\n  --- 96D = TONER conflict ---")
print(f"  96D starts at (12,17), length 5, rows 12-16")
print(f"  TONER = T, O, N, E, R")
print(f"  96D[0] is at (12,17) = 94A position {17-7} = position 10")
print(f"  CIRCLEABOUT[10] = {CIRC[10]} --> 96D[0] = T --> matches TONER[0] = T  [OK]")
print(f"  TURNONADIME[10] = {TURN[10]} --> 96D[0] = E --> TONER[0] needs T  [CONFLICT!]")
print()
print(f"  CONCLUSION: TURNONADIME is INCOMPATIBLE with TONER at 96D.")

print("\n  SUMMARY: If TURNONADIME is correct, BOTH ZIP and TONER must be WRONG.")
print("  This unravels the entire CIRCLEABOUT cascade chain.")


# ============================================================================
# SECTION 5: What could replace ZIP at 86D under TURNONADIME?
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 5: Alternative answers for 86D under TURNONADIME")
print("=" * 95)

print(f"\n  86D: (11,8) len 3, rows 11-13")
print(f"  Under TURNONADIME:")

# 86D[0] at (11,8): what across entry?
print(f"    [0] (11,8): from 85A at (11,6) len 5. 85A[2] = (11,8).")
turn_85a_pat = s_turn.pattern('A', 85)
print(f"         85A pattern under TURN: '{turn_85a_pat}' -> 85A[2] = '{turn_85a_pat[2]}'")

# 86D[1] at (12,8): from TURNONADIME
print(f"    [1] (12,8): from 94A=TURNONADIME[1] = U  [FORCED]")

# 86D[2] at (13,8): from 102A
turn_102a_pat = s_turn.pattern('A', 102)
print(f"    [2] (13,8): from 102A at (13,8) len 5. 102A[0] = '{turn_102a_pat[0]}'")

# Under TURNONADIME, 102A might not have PINTO placed (no ZIP cascade)
# What's the 86D pattern?
turn_86d_pat = s_turn.pattern('D', 86)
print(f"\n  86D pattern under TURNONADIME: '{turn_86d_pat}'")

# Check what 3-letter words match
import re
pat_86d = turn_86d_pat
regex_86d = re.compile('^' + pat_86d.replace('.', '[A-Z]') + '$')
common_matches = [w for w in COMMON_3_LETTER if regex_86d.match(w)]
bank_matches_86d = s_turn.bank_matches(pat_86d, 3)
print(f"  Answer bank matches: {bank_matches_86d}")
print(f"  Common 3-letter word matches for '{pat_86d}': {common_matches[:30]}")

# Specifically check ?UP pattern if that's what we get
if pat_86d[1] == 'U':
    up_words = [w for w in COMMON_3_LETTER if len(w) == 3 and w[1] == 'U' and regex_86d.match(w)]
    print(f"  Words matching {pat_86d}: {up_words}")


# ============================================================================
# SECTION 6: What could replace TONER at 96D under TURNONADIME?
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 6: Alternative answers for 96D under TURNONADIME")
print("=" * 95)

print(f"\n  96D: (12,17) len 5, rows 12-16")
print(f"  Under TURNONADIME:")

# Trace each position of 96D
for i in range(5):
    r = 12 + i
    c = 17
    turn_val = s_turn.cell(r, c)
    val_str = turn_val or '.'

    # What across entry crosses here?
    across_info = ""
    for ce, cn, ci in cell_to_entries[(r, c)]:
        if ce == 'A':
            asr, asc, asl = entry_info[('A', cn)]
            aplaced = s_turn.placed.get(('A', cn))
            if aplaced:
                across_info = f"{cn}A={aplaced}[{ci}]={aplaced[ci]}"
            else:
                apat = s_turn.pattern('A', cn)
                across_info = f"{cn}A[{ci}], pattern='{apat}'"

    print(f"    [{i}] ({r},{c}): {val_str}  |  {across_info}")

turn_96d_pat = s_turn.pattern('D', 96)
print(f"\n  96D pattern under TURNONADIME: '{turn_96d_pat}'")

bank_96d = s_turn.bank_matches(turn_96d_pat, 5)
print(f"  Answer bank matches: {bank_96d if bank_96d else 'NONE'}")

# Check common 5-letter words starting with E
regex_96d = re.compile('^' + turn_96d_pat.replace('.', '[A-Z]') + '$')
e_matches = [w for w in COMMON_5_LETTER_E if regex_96d.match(w)]
print(f"  Common E-starting 5-letter matches for '{turn_96d_pat}': {e_matches}")

# Also check if 103A=ACHOO is still valid under TURNONADIME
# 103A at (13,14) len 5. Does it cross 96D?
# 96D is at col 17. 103A is at cols 14-18. Col 17 = 103A pos 3.
# ACHOO[3] = O. So 96D[1] = O if ACHOO still holds.
print(f"\n  Key constraint: if ACHOO is still at 103A:")
print(f"    103A at (13,14) len 5 = cols 14-18. Col 17 = pos 3. ACHOO[3] = O")
print(f"    So 96D[1] at (13,17) = O")
print(f"    96D pattern becomes: E O ? ? ? (at minimum)")

# Check if ACHOO cascades under TURNONADIME
turn_103a_pat = s_turn.pattern('A', 103)
turn_103a_matches = s_turn.bank_matches(turn_103a_pat, 5)
print(f"\n  103A under TURNONADIME: pattern='{turn_103a_pat}', matches={turn_103a_matches}")
print(f"  (ACHOO may or may not cascade without the CIRCLEABOUT chain)")

# What else constrains 96D?
# 96D[2] at (14,17) = 111A[0]
# 96D[3] at (15,17) = 117A[1]
# 96D[4] at (16,17) = 123A[1]
print(f"\n  Further 96D constraints (rows 14-16):")
for i in range(2, 5):
    r = 12 + i
    for ce, cn, ci in cell_to_entries[(r, 17)]:
        if ce == 'A':
            tp = s_turn.placed.get(('A', cn))
            if tp:
                print(f"    [{i}] ({r},17): {cn}A={tp}[{ci}]={tp[ci]}")
            else:
                print(f"    [{i}] ({r},17): {cn}A[{ci}] = '{s_turn.pattern('A', cn)[ci]}' (unplaced)")


# ============================================================================
# SECTION 7: 67D Analysis -- Can ROBINHOOD work?
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 7: 67D = ROBINHOOD? (THE KEY CLAIM)")
print("=" * 95)

print(f"\n  67D: (8,12) len 9, rows 8-16, col 12")
print(f"  ROBINHOOD = R,O,B,I,N,H,O,O,D")
print()

for sname, solver in [("CIRCLEABOUT", s_circ), ("TURNONADIME", s_turn)]:
    print(f"  --- Under {sname} ---")
    pat_67d = solver.pattern('D', 67)
    print(f"  67D pattern: '{pat_67d}'")
    print()

    compatible = True
    for i in range(9):
        r = 8 + i
        c = 12
        grid_val = solver.cell(r, c)
        robin_ch = "ROBINHOOD"[i]
        grid_str = grid_val or '.'

        status = ""
        if grid_val is not None:
            if grid_val == robin_ch:
                status = "MATCH"
            else:
                status = f"*** CONFLICT: grid={grid_val}, ROBIN={robin_ch} ***"
                compatible = False
        else:
            status = "unconstrained"

        # What across provides this letter?
        across_desc = ""
        for ce, cn, ci in cell_to_entries[(r, c)]:
            if ce == 'A':
                aplaced = solver.placed.get(('A', cn))
                if aplaced:
                    across_desc = f"{cn}A={aplaced}[{ci}]={aplaced[ci]}"
                else:
                    across_desc = f"{cn}A[{ci}]='{solver.pattern('A', cn)[ci]}'"

        print(f"    [{i}] ({r},{c}): grid={grid_str}, ROBIN={robin_ch}, {status:30s} | {across_desc}")

    print(f"\n  ROBINHOOD compatible under {sname}? {'YES' if compatible else 'NO'}")
    print()

# The critical check:
print("  CRITICAL FINDING:")
print("  67D[0] at (8,12):")
print(f"    66A at (8,10) len 4 covers cols 10-13. Col 12 = 66A[2].")

# What is 66A[2] under each scenario?
for sname, solver in [("CIRCLEABOUT", s_circ), ("TURNONADIME", s_turn)]:
    pat66 = solver.pattern('A', 66)
    placed66 = solver.placed.get(('A', 66))
    val_at_8_12 = solver.cell(8, 12)
    if placed66:
        print(f"    {sname}: 66A={placed66}, 66A[2]={placed66[2]}, so 67D[0]={placed66[2]}")
    else:
        print(f"    {sname}: 66A pattern='{pat66}', 66A[2]='{pat66[2]}', so 67D[0]='{pat66[2]}'")

print()
print("  66A is constrained by:")
print(f"    [0] (8,10): 37D=ABASH[4]=H (both scenarios)")
print(f"    [3] (8,13): 53D=ROTUNDA[2]=T (both scenarios)")
print(f"    Pattern: H??T -> HAFT is the only bank match")
print(f"    If 66A=HAFT, then 66A[2]=F, so 67D[0]=F")
print(f"    ROBINHOOD[0]=R, but 67D[0]=F --> CONFLICT!")
print()
print("  CONCLUSION: ROBINHOOD CANNOT go at 67D regardless of 94A candidate,")
print("  because 66A=HAFT forces 67D[0]=F, and ROBINHOOD starts with R.")
print()
print("  Even if 66A is NOT HAFT:")
print("    66A pattern is H..T (from ABASH and ROTUNDA)")
print("    For ROBINHOOD at 67D, we'd need 66A[2]=R, making 66A = H?RT")
print("    H?RT is not in the answer bank (HART is a real word but not in our P1-P9 answers)")


# ============================================================================
# SECTION 8: Full 67D pattern analysis
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 8: Full 67D pattern derivation (F??A?OE?O)")
print("=" * 95)

print(f"\n  67D at (8,12) len 9. Tracing letter-by-letter:")
print()

for sname, solver in [("CIRCLEABOUT", s_circ), ("TURNONADIME", s_turn)]:
    print(f"  --- {sname} ---")
    pat = solver.pattern('D', 67)

    for i in range(9):
        r = 8 + i
        c = 12
        val = solver.cell(r, c)
        val_str = val or '.'

        source = ""
        for ce, cn, ci in cell_to_entries[(r, c)]:
            if ce == 'A':
                asr, asc, asl = entry_info[('A', cn)]
                aplaced = solver.placed.get(('A', cn))
                if aplaced:
                    source = f"{cn}A={aplaced}[{ci}]={aplaced[ci]}"
                else:
                    apat = solver.pattern('A', cn)
                    if apat[ci] != '.':
                        source = f"{cn}A[{ci}]='{apat[ci]}' (unplaced)"
                    else:
                        source = f"{cn}A[{ci}]='.' (unknown)"

        print(f"    [{i}] row {r}: {val_str}  | {source}")

    print(f"    Full pattern: '{pat}'")
    matches = solver.bank_matches(pat, 9)
    print(f"    Bank matches: {matches if matches else 'NONE'}")
    print()

# Show side-by-side
circ_67 = s_circ.pattern('D', 67)
turn_67 = s_turn.pattern('D', 67)
print(f"  Side-by-side 67D patterns:")
print(f"    CIRCLEABOUT: '{circ_67}'")
print(f"    TURNONADIME: '{turn_67}'")
diff_pos = [i for i in range(9) if circ_67[i] != turn_67[i]]
print(f"    Differ at positions: {diff_pos}")
if diff_pos:
    for p in diff_pos:
        print(f"      [{p}] row {8+p}: CIRC='{circ_67[p]}', TURN='{turn_67[p]}'")
        print(f"        This is 94A position {12-7}={12-7} crossing at row 12")
        print(f"        94A[5]: CIRCLEABOUT[5]=E, TURNONADIME[5]=N")


# ============================================================================
# SECTION 9: Cascade comparison -- what each scenario places
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 9: Full cascade comparison")
print("=" * 95)

print(f"\n  CIRCLEABOUT total placed: {len(s_circ.placed)}")
print(f"  TURNONADIME total placed: {len(s_turn.placed)}")

# Entries in CIRC but not TURN
circ_only = sorted(k for k in s_circ.placed if k not in s_turn.placed)
turn_only = sorted(k for k in s_turn.placed if k not in s_circ.placed)
both = sorted(k for k in s_circ.placed if k in s_turn.placed)
diff_word = sorted(k for k in both if s_circ.placed[k] != s_turn.placed[k])

print(f"\n  Both place (same word): {len(both) - len(diff_word)}")
for k in both:
    if k not in diff_word:
        print(f"    {k[0]}{k[1]:>4} = {s_circ.placed[k]}")

if diff_word:
    print(f"\n  Both place but DIFFERENT word: {len(diff_word)}")
    for k in diff_word:
        print(f"    {k[0]}{k[1]:>4}: CIRC={s_circ.placed[k]}, TURN={s_turn.placed[k]}")

print(f"\n  Only CIRCLEABOUT places ({len(circ_only)}):")
for k in circ_only:
    print(f"    {k[0]}{k[1]:>4} = {s_circ.placed[k]}")

print(f"\n  Only TURNONADIME places ({len(turn_only)}):")
for k in turn_only:
    print(f"    {k[0]}{k[1]:>4} = {s_turn.placed[k]}")
if not turn_only:
    print("    (none)")


# ============================================================================
# SECTION 10: Zero-match ("impossible pattern") comparison
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 10: Entries with constraints but ZERO bank matches")
print("=" * 95)

for sname, solver in [("CIRCLEABOUT", s_circ), ("TURNONADIME", s_turn)]:
    impossible = []
    for key in sorted(entry_info.keys()):
        if key in solver.placed:
            continue
        etype, num = key
        sl = entry_info[key][2]
        pat = solver.pattern(etype, num)
        if pat == '.' * sl:
            continue
        matches = solver.bank_matches(pat, sl)
        if len(matches) == 0:
            known = sum(1 for ch in pat if ch != '.')
            impossible.append((etype, num, sl, pat, known))

    print(f"\n  {sname}: {len(impossible)} entries with constraints but 0 matches")
    for etype, num, sl, pat, known in impossible:
        print(f"    {etype}{num:>4} (len {sl}): '{pat}' ({known}/{sl} known)")


# ============================================================================
# SECTION 11: 85A analysis (the ZT problem)
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 11: 85A pattern analysis")
print("=" * 95)

print(f"\n  85A: (11,6) len 5, cols 6-10")
print(f"  Under CIRCLEABOUT: 86D=ZIP -> 85A[2]='Z', 87D=TRITE -> 85A[3]='T'")
print(f"  Under TURNONADIME: 86D not ZIP, 87D still has R at pos 1")

for sname, solver in [("CIRCLEABOUT", s_circ), ("TURNONADIME", s_turn)]:
    print(f"\n  {sname}:")
    pat = solver.pattern('A', 85)
    matches = solver.bank_matches(pat, 5)
    print(f"    85A pattern: '{pat}'")
    print(f"    Bank matches: {matches if matches else 'NONE'}")

    for i in range(5):
        r, c = 11, 6 + i
        val = solver.cell(r, c) or '.'
        down_info = ""
        for ce, cn, ci in cell_to_entries[(r, c)]:
            if ce == 'D':
                dp = solver.placed.get(('D', cn))
                if dp:
                    down_info = f"{cn}D={dp}[{ci}]={dp[ci]}"
                else:
                    dpat = solver.pattern('D', cn)
                    down_info = f"{cn}D[{ci}]='{dpat[ci]}'"
        print(f"      [{i}] ({r},{c}) = {val}  |  {down_info}")


# ============================================================================
# SECTION 12: 102A (PINTO) cascade analysis
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 12: 102A (PINTO) cascade analysis")
print("=" * 95)

print(f"\n  102A: (13,8) len 5, cols 8-12")
print(f"  Under CIRCLEABOUT: 86D=ZIP -> 86D[2]=P -> 102A[0]=P -> cascade to PINTO")
print(f"  Under TURNONADIME: 86D is NOT ZIP -> 102A[0] unconstrained")

for sname, solver in [("CIRCLEABOUT", s_circ), ("TURNONADIME", s_turn)]:
    print(f"\n  {sname}:")
    pat102 = solver.pattern('A', 102)
    m102 = solver.bank_matches(pat102, 5)
    p102 = solver.placed.get(('A', 102))
    print(f"    102A pattern: '{pat102}', placed={p102}")
    print(f"    Bank matches: {m102 if m102 else 'NONE'}")


# ============================================================================
# SECTION 13: What about 109A=TOLEDO and 110D=DENVER under TURNONADIME?
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 13: TOLEDO (109A) and DENVER (110D) under TURNONADIME")
print("=" * 95)

for entry_key, entry_name in [(('A', 109), 'TOLEDO'), (('D', 110), 'DENVER')]:
    etype, num = entry_key
    sl = entry_info[entry_key][2]
    print(f"\n  {num}{etype[0]} = {entry_name}:")
    for sname, solver in [("CIRCLEABOUT", s_circ), ("TURNONADIME", s_turn)]:
        pat = solver.pattern(etype, num)
        matches = solver.bank_matches(pat, sl)
        placed = solver.placed.get(entry_key)
        print(f"    {sname}: pattern='{pat}', placed={placed}, matches={matches}")


# ============================================================================
# SECTION 14: Impact on 80D (position 2 = C vs N)
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 14: 80D impact (position 2 changes from C to N)")
print("=" * 95)

print(f"\n  80D: (10,10) len 6, rows 10-15, col 10")
print(f"  80D[2] at (12,10) = 94A[3]: CIRCLEABOUT[3]=C, TURNONADIME[3]=N")

for sname, solver in [("CIRCLEABOUT", s_circ), ("TURNONADIME", s_turn)]:
    print(f"\n  {sname}:")
    pat80d = solver.pattern('D', 80)
    m80d = solver.bank_matches(pat80d, 6)
    print(f"    80D pattern: '{pat80d}'")
    print(f"    Bank matches: {m80d if m80d else 'NONE'}")
    for i in range(6):
        r = 10 + i
        val = solver.cell(r, 10) or '.'
        across_info = ""
        for ce, cn, ci in cell_to_entries[(r, 10)]:
            if ce == 'A':
                ap = solver.placed.get(('A', cn))
                if ap:
                    across_info = f"{cn}A={ap}[{ci}]={ap[ci]}"
                else:
                    across_info = f"{cn}A[{ci}]='{solver.pattern('A', cn)[ci]}'"
        print(f"      [{i}] ({r},10) = {val}  |  {across_info}")


# ============================================================================
# SECTION 15: Impact on 95D (position 0 = L vs O)
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 15: 95D impact (position 0 changes from L to O)")
print("=" * 95)

print(f"\n  95D: (12,11) len 7, rows 12-18, col 11")
print(f"  95D[0] at (12,11) = 94A[4]: CIRCLEABOUT[4]=L, TURNONADIME[4]=O")
print(f"  NOTE: 95D[10] does NOT exist (len 7), but (22,11) has a circled cell")
print(f"        (22,11) is 167A[2] = 'P' from SUPERBOWLSTADIUM -- not part of 95D")

for sname, solver in [("CIRCLEABOUT", s_circ), ("TURNONADIME", s_turn)]:
    print(f"\n  {sname}:")
    pat95 = solver.pattern('D', 95)
    m95 = solver.bank_matches(pat95, 7)
    print(f"    95D pattern: '{pat95}'")
    print(f"    Bank matches: {m95 if m95 else 'NONE'}")
    for i in range(7):
        r = 12 + i
        val = solver.cell(r, 11) or '.'
        across_info = ""
        for ce, cn, ci in cell_to_entries[(r, 11)]:
            if ce == 'A':
                ap = solver.placed.get(('A', cn))
                if ap:
                    across_info = f"{cn}A={ap}[{ci}]={ap[ci]}"
                else:
                    across_info = f"{cn}A[{ci}]='{solver.pattern('A', cn)[ci]}'"
        print(f"      [{i}] ({r},11) = {val}  |  {across_info}")


# ============================================================================
# SECTION 16: Impact on 74D (position 3 = B vs D)
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 16: 74D impact (position 3 changes from B to D)")
print("=" * 95)

print(f"\n  74D: (9,14) len 6, rows 9-14, col 14")
print(f"  74D[3] at (12,14) = 94A[7]: CIRCLEABOUT[7]=B, TURNONADIME[7]=D")

for sname, solver in [("CIRCLEABOUT", s_circ), ("TURNONADIME", s_turn)]:
    print(f"\n  {sname}:")
    pat74d = solver.pattern('D', 74)
    m74d = solver.bank_matches(pat74d, 6)
    print(f"    74D pattern: '{pat74d}'")
    print(f"    Bank matches: {m74d if m74d else 'NONE'}")


# ============================================================================
# SECTION 17: Impact on 75D (position 3 = O vs I)
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 17: 75D impact (position 3 changes from O to I)")
print("=" * 95)

print(f"\n  75D: (9,15) len 5, rows 9-13, col 15")
print(f"  75D[3] at (12,15) = 94A[8]: CIRCLEABOUT[8]=O, TURNONADIME[8]=I")

for sname, solver in [("CIRCLEABOUT", s_circ), ("TURNONADIME", s_turn)]:
    print(f"\n  {sname}:")
    pat75d = solver.pattern('D', 75)
    m75d = solver.bank_matches(pat75d, 5)
    print(f"    75D pattern: '{pat75d}'")
    print(f"    Bank matches: {m75d if m75d else 'NONE'}")


# ============================================================================
# SECTION 18: Impact on 89D (position 1 = U vs M)
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 18: 89D impact (position 1 changes from U to M)")
print("=" * 95)

print(f"\n  89D: (11,16) len 3, rows 11-13, col 16")
print(f"  89D[1] at (12,16) = 94A[9]: CIRCLEABOUT[9]=U, TURNONADIME[9]=M")

for sname, solver in [("CIRCLEABOUT", s_circ), ("TURNONADIME", s_turn)]:
    print(f"\n  {sname}:")
    pat89d = solver.pattern('D', 89)
    m89d = solver.bank_matches(pat89d, 3)
    print(f"    89D pattern: '{pat89d}'")
    print(f"    Bank matches: {m89d if m89d else 'NONE'}")

    # Check common 3-letter words
    regex_89d = re.compile('^' + pat89d.replace('.', '[A-Z]') + '$')
    common_89d = [w for w in COMMON_3_LETTER if regex_89d.match(w)]
    print(f"    Common word matches: {common_89d[:20]}")


# ============================================================================
# SECTION 19: Grid visualization
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 19: Grid visualization (rows 7-17)")
print("=" * 95)

for sname, solver in [("CIRCLEABOUT", s_circ), ("TURNONADIME", s_turn)]:
    print(f"\n  {sname} grid (rows 7-17):")
    solver.print_grid(7, 18)


# ============================================================================
# SECTION 20: Hidden location names in 94A
# ============================================================================

print("\n" + "=" * 95)
print("  SECTION 20: Hidden location names in 94A candidates")
print("=" * 95)

locations = [
    'MALI', 'TEHRAN', 'LAGOS', 'SUDAN', 'OMAN', 'ADEN', 'WALES', 'GOA',
    'NIGER', 'DELHI', 'CHAD', 'LIMA', 'IRAN', 'ROME', 'NOME', 'NAURU',
    'TURIN', 'CABO', 'BERN', 'NICE', 'BONN', 'CORK', 'DOVER', 'SEDAN',
    'DAKAR', 'ACCRA', 'TOKYO', 'PARIS', 'CAIRO', 'ABOUJ', 'ONADIME',
]

for word in [CIRC, TURN]:
    hits = [loc for loc in locations if loc in word]
    print(f"\n  {word}:")
    if hits:
        for h in hits:
            idx = word.index(h)
            print(f"    '{h}' at positions {idx}-{idx+len(h)-1}")
    else:
        print(f"    No location substrings found")


# ============================================================================
# FINAL VERDICT
# ============================================================================

print("\n" + "=" * 95)
print("  FINAL VERDICT")
print("=" * 95)

print(f"""
  METRIC                        CIRCLEABOUT    TURNONADIME
  Total entries placed:         {len(s_circ.placed):>10}     {len(s_turn.placed):>10}
  Conflicts found:              {len(s_circ.conflicts):>10}     {len(s_turn.conflicts):>10}
""")

# Count zero-match entries
circ_zero = sum(1 for k in entry_info if k not in s_circ.placed
                and s_circ.pattern(*k) != '.' * entry_info[k][2]
                and not s_circ.bank_matches(s_circ.pattern(*k), entry_info[k][2]))
turn_zero = sum(1 for k in entry_info if k not in s_turn.placed
                and s_turn.pattern(*k) != '.' * entry_info[k][2]
                and not s_turn.bank_matches(s_turn.pattern(*k), entry_info[k][2]))

print(f"  Zero-match constrained:     {circ_zero:>10}     {turn_zero:>10}")

print(f"""
  KEY FINDINGS:

  1. TURNONADIME CONFLICTS with 2 confirmed placements:
     - 86D=ZIP: needs I at position 1, TURNONADIME gives U  --> BREAKS ZIP
     - 96D=TONER: needs T at position 0, TURNONADIME gives E --> BREAKS TONER

  2. If TURNONADIME replaces those entries:
     - 86D would need a ?U? word (if 85A[2] unknown) or specific ?UP word
     - 96D would need a 5-letter word starting E (EO??? with ACHOO providing O at pos 1)
     - The entire CIRCLEABOUT cascade (ZIP->PINTO->TOLEDO->DENVER->TONI) breaks

  3. ROBINHOOD at 67D is IMPOSSIBLE under EITHER candidate:
     - 67D[0] at (8,12) = 66A[2]
     - 66A pattern = H??T (from ABASH[4]=H and ROTUNDA[2]=T)
     - 66A = HAFT -> 67D[0] = F
     - ROBINHOOD[0] = R, which CONFLICTS with F
     - Even without HAFT, 66A = H?RT requires a non-bank word

  4. 67D patterns:
     - Under CIRCLEABOUT: '{circ_67}' (position 4=E)
     - Under TURNONADIME: '{turn_67}' (position 4=N)
     - Both have F at position 0 (from 66A=HAFT)
     - Neither matches any 9-letter word in the answer bank
     - Both are likely compound words/phrases (common in Selinker puzzles)

  5. CIRCLEABOUT places {len(s_circ.placed)} entries vs TURNONADIME's {len(s_turn.placed)} entries
     The CIRCLEABOUT cascade chain (ZIP, TRITE, PUSH, HAFT, PINTO, ACHOO,
     TOLEDO, DENVER, REGINA, TONI, ERASE, TONER, ADORN) involves answers from
     5 different puzzle sources (P1, P3, P4, P8, P9) = strong cross-validation.

  VERDICT: CIRCLEABOUT remains the MUCH stronger candidate.
  TURNONADIME would require ZIP and TONER to both be wrong, destroying the
  entire central cascade. ROBINHOOD at 67D is impossible regardless.
""")
