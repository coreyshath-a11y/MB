#!/usr/bin/env python3
"""
Dictionary-based solver for heavily constrained crossword entries.
Uses /usr/share/dict/words plus confirmed answers to fill grid.
"""

import subprocess
import re

# Load word list
words_by_len = {}
try:
    with open('/usr/share/dict/words') as f:
        for line in f:
            w = line.strip().upper()
            if w.isalpha() and 3 <= len(w) <= 16:
                l = len(w)
                if l not in words_by_len:
                    words_by_len[l] = []
                words_by_len[l].append(w)
except:
    pass

# Also try nltk
try:
    from nltk.corpus import words as nltk_words
    for w in nltk_words.words():
        w = w.upper()
        if w.isalpha() and 3 <= len(w) <= 16:
            l = len(w)
            if l not in words_by_len:
                words_by_len[l] = []
            words_by_len[l].append(w)
except:
    pass

# Deduplicate
for l in words_by_len:
    words_by_len[l] = sorted(set(words_by_len[l]))

print(f"Dictionary sizes: {', '.join(f'{l}:{len(words_by_len[l])}' for l in sorted(words_by_len.keys()))}")

# Constrained entries (from comprehensive solver output)
# Format: (entry_id, pattern) where . = unknown
CONSTRAINED = [
    ("67D", "F..AEOE.O", 9),
    ("74D", "..OBAO", 6),
    ("75D", "..ROC", 5),
    ("80D", "..CNO.", 6),
    ("95D", "LTL.T..", 7),
    ("104D", "O.GA...", 7),
    ("46D", "..HA..", 6),
    ("112D", ".IS...", 6),
    ("8D", "....R..U", 8),
    ("89D", "NUH", 3),
    ("45A", ".B..", 4),
    ("59A", "O...", 4),
    ("111A", "N..", 3),
    ("85A", "..ZT.", 5),
    ("132A", "V...", 4),
    ("145A", ".R..", 4),
    ("80A", "...N..", 6),
    ("26D", "..D..", 5),
    ("52D", ".P..", 4),
    ("65D", "....C", 5),
    ("23D", "...O", 4),
    ("117D", "RE..", 4),
    ("118D", "NE..", 4),
    ("122D", "I....", 5),
    ("98D", "...A", 4),
]

# For compound words / proper nouns in crosswords, also add known answers
KNOWN_ANSWERS = [
    'ACHOO', 'TYPHOON', 'SCHOOL', 'HOODWINK', 'OHSHOOT', 'OHIOAN', 'HULAHOOP',
    'HOODIE', 'HOOVERDAM', 'DHOW', 'ROBINHOOD', 'WAHOO',
    'HAFT', 'DITHERING', 'HOWITZERS', 'SCENARIO', 'ABASH', 'NEUROTIC',
    'HEARTED', 'HIGHHEELS', 'SCREENER', 'INTRODUCTIONS', 'MATTER', 'OPERA',
    'ALLUSIONS', 'RESISTIVE', 'ABSOLUTE', 'ERASE', 'TEAMSEAS', 'TRITE', 'MUSTERS',
    'RAD', 'EAR', 'ION', 'EON', 'DORA', 'RACE', 'TONI', 'NOTE',
    'ADORN', 'LECAR', 'PINTO', 'TONER', 'ECLAIR', 'OPTION', 'ORIENT',
    'ROTUNDA', 'CALIBER', 'PORTION', 'INUTERO', 'DURATION', 'CARBLITE',
    'POSITRON', 'ROUTINES', 'INUNDATOR', 'CABRIOLET', 'RATPOISON', 'OUTLINERS',
    'CIRCLEABOUT', 'TURNONADIME', 'OUTFORASPIN', 'REVOLUTIONS',
    'ZIP', 'CHAIRS', 'QUORUMS', 'FLAMINGO', 'PUSH', 'CONVEX', 'HIRPLED',
    'TORONTO', 'REGINA', 'OWENSBORO', 'TOLEDO', 'ROSWELL', 'DRESDEN',
    'TEMPE', 'WARSAW', 'ADELAIDE', 'DENVER', 'SEVILLE', 'OTTAWA',
    'ANNAPOLIS', 'AUBURN', 'DOVER', 'ROCHESTER', 'ORLANDO', 'WOODWAY',
    'ACCRA', 'CASHTENT', 'CONTRADICTION',
    # P1 uncertain
    'VOODOO', 'YAHOO',
]

for w in KNOWN_ANSWERS:
    l = len(w)
    if l not in words_by_len:
        words_by_len[l] = []
    if w not in words_by_len[l]:
        words_by_len[l].append(w)

def matches_pattern(word, pattern):
    if len(word) != len(pattern):
        return False
    for w, p in zip(word, pattern):
        if p != '.' and w != p:
            return False
    return True

print("\n" + "="*70)
print("DICTIONARY SEARCH FOR CONSTRAINED ENTRIES")
print("="*70)

for entry_id, pattern, length in CONSTRAINED:
    candidates = [w for w in words_by_len.get(length, []) if matches_pattern(w, pattern)]
    if len(candidates) <= 30:
        print(f"\n  {entry_id} [{pattern}] ({len(candidates)} matches): {candidates}")
    else:
        print(f"\n  {entry_id} [{pattern}] ({len(candidates)} matches): {candidates[:15]}...")

# ============================================================
# SPECIAL ANALYSIS: What words match 67D = F??AEOE?O?
# ============================================================
print("\n" + "="*70)
print("SPECIAL: 67D = F__AEOE_O")
print("="*70)

# This is so constrained, let's be flexible about dictionary
# Maybe it's a compound: F_RAEOE_O? FOULWEOE?O?
# Or a name: FARAGOEO?
# Pattern: F . . A E O E . O (positions 0-8)
# Could be: FARCE + something? No.
# Let's check character by character

# Let me also check what entries cross 67D at unknown positions
# 67D starts at (8,12), goes down to (16,12)
# Unknown positions: 1 (row 9), 2 (row 10), 7 (row 15)
# Row 9, col 12: part of 73A (theme entry, len 14, starts (9,11))
#   73A pos 1 = this letter
# Row 10, col 12: part of 80A (len 6, starts (10,10))
#   80A pos 2 = this letter (80A state: ...N..)
# Row 15, col 12: part of 114A (theme entry, len 14, starts (15,0))
#   114A pos 12 = this letter

print("\n67D unknown positions:")
print("  pos 1 (row 9): = 73A[1] (theme entry)")
print("  pos 2 (row 10): = 80A[2] (state: ...N..)")
print("  pos 7 (row 15): = 114A[12] (theme entry)")

# Actually - what if 67D isn't a standard dictionary word?
# It could be a phrase or compound. In crosswords, multi-word answers are common.
# F__AEOE_O... Let me think about it as parts:
# F + ?AE + OE + ?O
# or F?? + AEOE + ?O

# ============================================================
# SPECIAL ANALYSIS: 95D = LTL.T.. (7 letters)
# ============================================================
print("\n" + "="*70)
print("SPECIAL: 95D = LTL.T..")
print("="*70)

# 95D starts at (12,11), goes down to (18,11)
# Pos 0: (12,11) = L from CIRCLEABOUT[4]
# Pos 1: (13,11) = T from PINTO[3]
# Pos 2: (14,11) = L from TOLEDO[2]
# Pos 3: (15,11) = ? (114A pos 11)
# Pos 4: (16,11) = T from TONI[0]
# Pos 5: (17,11) = ? (no across entry at (17,11) because (17,12) is black)
# Actually wait, let me check. At row 17, col 11: is there an across entry?
# 129A starts at (17,8) length 4: covers (17,8) to (17,11). So (17,11) is 129A[3].
# And pos 5 = (17,11) which is 129A[3]
# Pos 6: (18,11) = ? (138A pos 2, the theme entry)

print("  Pattern: L T L . T . .")
print("  Pos 3 = 114A[11]")
print("  Pos 5 = 129A[3]")
print("  Pos 6 = 138A[2]")

# L T L ? T ? ?
# LETTUCE? No... L E T T U C E - doesn't match (need pos 0=L, pos 2=L)
# LATTICE? L A T T I C E - pos0=L, pos1=A≠T
# LOTLITE? Not a word
# LATLOT? No
# Could this be part of a phrase? Like "LITTLE" something?
# L I T L E? No LITTLE has 6 letters
# What about reading it correctly: L, T, L, ?, T, ?, ?
# LTLETOP? Not a word
# What if it's a compound? Like "LIT-LEST" or something...

# Hmm, this pattern is very unusual. Maybe it's a multi-word answer.
# Let me check if LITTLETON fits... L I T T L E T O N = 9 letters, too long
# OUTLETS? O U T L E T S = 7 letters. O≠L

# Actually wait - could it be LATTICE but shifted? No.
# Let me search the dictionary more carefully

candidates_95d = [w for w in words_by_len.get(7, []) if matches_pattern(w, "LTL.T..")]
print(f"  Dictionary matches: {candidates_95d}")

# ============================================================
# SPECIAL: 74D = ??OBAO (6 letters)
# ============================================================
print("\n" + "="*70)
print("SPECIAL: 74D = ??OBAO")
print("="*70)

candidates_74d = [w for w in words_by_len.get(6, []) if matches_pattern(w, "..OBAO")]
print(f"  Dictionary matches: {candidates_74d}")
# Probably very few. GLOBAL fits at pos 2-5: GLOB... no.
# ??OBAO - this is unusual. Maybe it's a proper name? NAOBAO? LAOBAO?

# ============================================================
# SPECIAL: 80A = ...N.. (6 letters at row 10, cols 10-15)
# ============================================================
print("\n" + "="*70)
print("SPECIAL: 80A = ...N.. (6 letters)")
print("="*70)

# 80A starts at (10,10), length 6
# (10,10) = ? (80D pos 0)
# (10,11) = ? (46D pos ?)
# (10,12) = ? (circled cell! 67D pos 2)
# (10,13) = N (from 53D: ROTUNDA pos 4)
# (10,14) = ? (74D pos 1, 39D pos ?)
# (10,15) = ? (75D pos 1, 27D pos ?)

# So we need a 6-letter word: ???N??
# With 80D state ..CNO. → 80D pos 0 = 80A pos 0
# Wait 80D starts at (10,10) going DOWN col 10. Its pos 0 is (10,10) which is 80A pos 0.
# We have 80D = ? ? C N O ?
# So 80D[0] = 80A[0]

# We also have 80A[2] = 67D[2] (the circled cell at (10,12))
# This is interesting for extraction!

candidates_80a = [w for w in words_by_len.get(6, []) if matches_pattern(w, "...N..")]
print(f"  {len(candidates_80a)} dictionary matches for ???N??")

# ============================================================
# Key crossings from 67D to theme entries
# ============================================================
print("\n" + "="*70)
print("KEY THEME ENTRY CONSTRAINTS")
print("="*70)

# 67D[1] = 73A[1] (theme entry pos 1)
# 67D[7] = 114A[12] (theme entry pos 12)
# 95D[3] = 114A[11]
# 95D[6] = 138A[2]
# 104D has state O.GA...: this crosses several entries

# Let me analyze 104D more carefully
# 104D starts at (13,18), goes DOWN col 18, length 7
# (13,18): 103A pos 4 or 105A? Let me check.
#   103A at (13,14) len 5: covers cols 14-18. So (13,18) = 103A[4] = O (from ACHOO[4])
#   Wait no: 103A is ACHOO at (13,14): A=14, C=15, H=16, O=17, O=18. So (13,18)=O ✓
# (14,18): ?
# (15,18): ?
# (16,18): 123A at (16,16) len 5: ERASE covers 16-20. (16,18)=A ← ERASE[2]
#   Wait: 123A starts at col 16, length 5 = cols 16,17,18,19,20. ERASE: E=16,R=17,A=18,S=19,E=20. So (16,18)=A
#   Hmm but solver shows 104D state = O.GA...
#   That means (14,18)=?, (15,18)=G?, (16,18)=A
#   Wait, that doesn't look right. Let me recount.
# Actually 104D = 7 letters starting (13,18) going down:
# pos 0: (13,18) = O
# pos 1: (14,18) = ? ... but (14,18) should be in 109A or something. Let me check.
#   14 row, col 18: 109A at (14,9) len 6 covers 9-14. So col 18 is NOT in 109A.
#   111A at (14,17) len 3 covers 17-19. So (14,18) = 111A[1]. 111A state is "N.."
#   So (14,17)=N, (14,18)=?, (14,19)=?.
#   Actually wait, I placed DENVER at 110D. 110D starts at (14,13) going down col 13.
#   That doesn't affect col 18.
#   Hmm, the solver output says 104D state = O.GA... Let me check what gives G.
#   pos 2: (15,18) - 117A at (15,16) len 6 = REGINA. R=16, E=17, G=18, I=19, N=20, A=21.
#   Wait, 117A at (15,16) length 6 covers cols 16-21. REGINA: R(16), E(17), G(18), I(19), N(20), A(21).
#   So (15,18) = G from REGINA. ✓
# pos 3: (16,18) = A from ERASE[2]? Let me check 123A: starts (16,16) len 5 = cols 16-20.
#   ERASE: E(16), R(17), A(18), S(19), E(20). So (16,18) = A ✓
# pos 4: (17,18) = ? 134A at (17,18) len 7 starts here. So this is 134A[0].
# pos 5: (18,18) = ? 138A at (18,9) len 16 covers cols 9-24. (18,18) = 138A[9]
# pos 6: (19,18) = ? 145A? No, 145A at (19,12) len 4 covers 12-15.
#   146A at (19,17) len 3 covers 17-19. So (19,18) = 146A[1]

print("\n104D = O ? G A ? ? ? (7 letters)")
print("  pos 0 = O (from ACHOO)")
print("  pos 1 = ? (= 111A[1])")
print("  pos 2 = G (from REGINA)")
print("  pos 3 = A (from ERASE)")
print("  pos 4 = ? (= 134A[0])")
print("  pos 5 = ? (= 138A[9], theme entry!)")
print("  pos 6 = ? (= 146A[1])")

# So 104D has O?GA???
# Looking for 7-letter words matching O.GA...
candidates_104d = [w for w in words_by_len.get(7, []) if matches_pattern(w, "O.GA...")]
print(f"  Dictionary matches: {candidates_104d}")

# ============================================================
# 112D = .IS... (6 letters, starts at (14,19))
# ============================================================
print("\n112D = ? I S ? ? ? (6 letters)")
# pos 0: (14,19) - from 111A or something? 111A at (14,17) len 3: cols 17,18,19 → (14,19) = 111A[2]
#   So 112D[0] = 111A[2]
#   Wait the solver says 112D state = .IS...
#   pos 0 = ?
#   pos 1: (15,19) = I from REGINA[3]
#   pos 2: (16,19) = S from ERASE[3]
#   pos 3-5: unknown
# So 112D = ?IS???
candidates_112d = [w for w in words_by_len.get(6, []) if matches_pattern(w, ".IS...")]
print(f"  Dictionary matches ({len(candidates_112d)}): {candidates_112d[:20]}...")

# ============================================================
# Look at 46D = ..HA.. (6 letters)
# ============================================================
print("\n46D = ? ? H A ? ? (6 letters, starts at (5,11))")
# pos 0: (5,11) - 45A at (5,9) len 4: cols 9,10,11,12 → (5,11) = 45A[2]
# pos 1: (6,11) - 50A at (6,0) len 16 → (6,11) = 50A[11]
# pos 2: (7,11) - 58A at (7,8) len 4: PUSH covers 8-11 → (7,11) = PUSH[3] = H ✓
# pos 3: (8,11) - 66A at (8,10) len 4: HAFT covers 10-13 → (8,11) = HAFT[1] = A ✓
# pos 4: (9,11) - 73A at (9,11) len 14 → (9,11) = 73A[0]
# pos 5: (10,11) - 80A at (10,10) len 6 → (10,11) = 80A[1]

candidates_46d = [w for w in words_by_len.get(6, []) if matches_pattern(w, "..HA..")]
print(f"  Dictionary matches ({len(candidates_46d)}): {candidates_46d[:20]}...")

print("\n  Key crossings:")
print("  pos 0 = 45A[2]")
print("  pos 1 = 50A[11] (theme entry!)")
print("  pos 4 = 73A[0] (theme entry!)")
print("  pos 5 = 80A[1]")

# ============================================================
# 8D = ....R..U (8 letters, starts at (0,9))
# ============================================================
print("\n8D = ? ? ? ? R ? ? U (8 letters, starts at (0,9))")
# pos 4: (4,9) = R from DORA[2]
# pos 7: (7,9) = U from PUSH[1]
candidates_8d = [w for w in words_by_len.get(8, []) if matches_pattern(w, "....R..U")]
print(f"  Dictionary matches ({len(candidates_8d)}): {candidates_8d[:20]}...")

# Check against our confirmed 8-letter answers
for ans in ['HOODWINK', 'HULAHOOP', 'SCENARIO', 'NEUROTIC', 'SCREENER', 'ABSOLUTE', 'TEAMSEAS',
            'DURATION', 'CARBLITE', 'POSITRON', 'ROUTINES', 'CASHTENT', 'FLAMINGO', 'ADELAIDE']:
    if matches_pattern(ans, "....R..U"):
        print(f"  CONFIRMED ANSWER MATCH: {ans}")

# ============================================================
# Summary of what we can deduce for theme entries
# ============================================================
print("\n" + "="*70)
print("THEME ENTRY LETTER DEDUCTIONS")
print("="*70)

print("\n73A (14 letters): Currently ..U...........\n")
print("  pos 0 = 46D[4] (46D = ??HA??)")
print("  pos 1 = 67D[1] (67D = F??AEOE?O)")
print("  → If 67D has few matches, this constrains 73A pos 1")

print("\n114A (14 letters): Currently .........E...E\n")
print("  pos 11 = 95D[3] (95D = LTL?T??)")
print("  pos 12 = 67D[7] (67D = F??AEOE?O)")

print("\n50A (16 letters): Currently ..........A..R..\n")
print("  pos 11 = 46D[1] (46D = ??HA??)")
print("  → 46D has pattern ??HA??, its pos 1 goes to 50A pos 11")
print("  → If 46D's pos 1 options are limited, this constrains 50A")
