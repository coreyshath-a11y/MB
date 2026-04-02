#!/usr/bin/env python3
"""
Test DELHI hidden in 114A at positions 8-12.
Trace all cascading constraints.
"""

print("=" * 70)
print("DELHI IN 114A ANALYSIS")
print("=" * 70)
print()

# 114A at (15,0) len 14, cols 0-13
# Known: pos 9 = E (from TRITE/87D), pos 13 = E (from DENVER/110D)
#
# DELHI at pos 8-12: D(8), E(9), L(10), H(11), I(12)
# pos 9 = E from DELHI ✓ matches TRITE constraint
# pos 13 = E from DENVER ✓ (this is AFTER DELHI, independent)

print("114A = ????????DELHIE (14 letters)")
print("  pos 8 = D (from DELHI)")
print("  pos 9 = E (from DELHI) ← matches TRITE constraint ✓")
print("  pos 10 = L (from DELHI)")
print("  pos 11 = H (from DELHI)")
print("  pos 12 = I (from DELHI)")
print("  pos 13 = E (from DENVER) ← independent constraint ✓")
print()

# Now trace DOWN entries crossed by 114A at these new positions
# 114A is at row 15, cols 0-13
# New letters: D at col 8, L at col 10, H at col 11, I at col 12

# Col 8: 116D at (15,8) len 3, rows 15-17. 114A gives pos 0 = D.
# 116D was previously unknown. Now 116D = D??.
print("New constraints from DELHI at 114A:")
print()

# 116D: (15,8) down, len 3
# pos 0 = D (from 114A/DELHI)
# pos 1 = (16,8) → black! No wait, (16,9) is black, (16,10) is black.
# Actually (16,8) - is it black? Let me check.
# Black cells at row 16: (16,4), (16,9), (16,10), (16,15), (16,21)
# (16,8) is NOT black. So 116D[1] at (16,8) is white.
# 119A at (16,0) len 4 = cols 0-3. Col 8 is outside. 120A at (16,5) len 4 = cols 5-8. Col 8 = pos 3.
# So 120A[3] = 116D[1]. Both unknown.
# pos 2 = (17,8) → 129A at (17,8) len 4 = cols 8-11. 129A[0] = 116D[2].
print("  116D (15,8, len 3): now D?? (D from DELHI)")
print("    pos 1 = (16,8) = 120A[3]")
print("    pos 2 = (17,8) = 129A[0]")
print()

# Col 10: 80D at (10,10) len 6, rows 10-15. Row 15 = pos 5. 80D[5] = L.
# 80D was: ??CNO? (C from CIRCLEABOUT, N from ROTUNDA, O from ?)
# Wait, let me recheck. 80D at (10,10) len 6:
# pos 0: (10,10) → 80A at (10,10) len 6, pos 0. Unknown.
# pos 1: (11,10) → black cell (11,11 is black, but 11,10? Let me check. Black at row 11: (11,5),(11,11),(11,17),(11,21). So (11,10) is NOT black.
# 85A at (11,6) len 5 = cols 6-10. Col 10 = pos 4.
# 37D at (4,10) = ABASH. Row 11 = pos 7... ABASH is only len 5 (rows 4-8). Doesn't reach row 11.
# So 85A[4] at (11,10). Unknown.
# pos 2: (12,10) → 94A CIRCLEABOUT. Col 10 = pos 3 = C. 80D[2] = C.
# pos 3: (13,10) → 102A PINTO. (13,8) len 5 = cols 8-12. Col 10 = pos 2 = N. 80D[3] = N.
# pos 4: (14,10) → 109A TOLEDO. (14,9) len 6 = cols 9-14. Col 10 = pos 1 = O. 80D[4] = O.
# pos 5: (15,10) → 114A. If DELHI at pos 8-12, col 10 = pos 10 = L. 80D[5] = L.
# So 80D = ??CNOL. Previously it was ??CNO?. Now the last letter is L.
print("  80D (10,10, len 6): now ??CNOL (L from DELHI)")
print("    Was: ??CNO? → now ??CNOL")
print("    What 6-letter word matches ??CNOL? Very unusual.")
print()

# Col 11: nothing standard. Let me check what down entry is at col 11 row 15.
# 95D at (12,11) len 7, rows 12-18. Row 15 = pos 3. 95D[3] = H.
# 95D was: LTL?T?? (L from CIRCLEABOUT, T from TONI, L from ?).
# Wait, let me recheck: 95D at (12,11):
# pos 0: (12,11) = 94A col 11 = pos 4 = L (CIRCLEABOUT). 95D[0] = L.
# pos 1: (13,11) → 13,11 is... 102A at (13,8) len 5 = cols 8-12. Col 11 = pos 3 = T (PINTO[3]=T). 95D[1] = T.
# pos 2: (14,11) → 109A TOLEDO col 11 = pos 2 = L. 95D[2] = L.
# pos 3: (15,11) → 114A pos 11 = H (DELHI[3]). 95D[3] = H.
# pos 4: (16,11) → 121A TONI[0] = T. 95D[4] = T.
# pos 5: (17,11) → 129A at (17,8) len 4 = cols 8-11. Col 11 = pos 3. Unknown.
# Also 131D at (17,10) len 4 = rows 17-20. But that's col 10 not 11.
# What's at (17,11)? Check: any down entry? 95D continues: pos 5 = (17,11).
# Any across entry? 127A at (17,1) len 6 = cols 1-6. Doesn't reach col 11.
# 129A at (17,8) len 4 = cols 8-11. Col 11 = pos 3. So 95D[5] = 129A[3].
# pos 6: (18,11) → 138A at (18,9) len 16 = cols 9-24. Col 11 = pos 2. So 95D[6] = 138A[2].

# 95D now = LTL H T ?? → LTLHT??
# Wait: L(0), T(1), L(2), H(3), T(4), ?(5), ?(6)
print("  95D (12,11, len 7): now LTLHT?? (H from DELHI)")
print("    Was: LTL?T?? → now LTLHT??")
print("    Even more constrained. What 7-letter word matches LTLHT???")
print("    (This is an impossible pattern for standard English. Suggests")
print("    this is a compound/multi-word entry, which is normal for Selinker.)")
print()

# Col 12: what down entry?
# 67D at (8,12) len 9, rows 8-16. Row 15 = pos 7. 67D[7] = I.
# 67D was: F??AEOE?O → now F??AEOEI0
# Wait: F(0),?(1),?(2),A(3),E(4),O(5),E(6),I(7),O(8)
# = F??AEOEI0
print("  67D (8,12, len 9): now F??AEOEIO (I from DELHI)")
print("    Was: F??AEOE?O → now F??AEOEIO")
print("    9-letter word matching F??AEOEIO:")
print("    Still very unusual. But more constrained (8/9 letters known).")
print()

# 67D = F ? ? A E O E I O
# With only position 1 and 2 unknown. Let me think about what letters could go there.
# The word is F_?_?_AEOEIO... that's F + 2 unknowns + AEOEIO
# 9 letters total
# Could this be a compound? Like F?? + AEOEIO?
# AEOEIO doesn't parse as a suffix
# Or maybe it's read as a phrase: F__ A_E_O_E_I_O
# This looks like it could be multiple words without spaces

# What if 73A with SUDAN gives us 67D[1] = S?
# 73A at (9,11) len 14. SUDAN at pos 1-5 means col 12 pos = 1, so 67D[1] = S
# 67D = FS?AEOEIO
# F-S-?-A-E-O-E-I-O → what could this be?
# Only 1 unknown at position 2.
# FS_AEOEIO
# Position 2 = (10,12) = 80A at (10,10) len 6, col 12 = pos 2. 80A[2] = ?

# If 80D is now ??CNOL, then 80D[0] at (10,10) and 80D[1] at (11,10) are unknown.
# 80A at (10,10) len 6 = cols 10-15. Currently: pos 2 = C (from 80D[2])? No...
# Wait. 80A and 80D start at the same cell (10,10). 80A goes across, 80D goes down.
# 80A[0] = (10,10), 80A[1] = (10,11), 80A[2] = (10,12), etc.
# 80D[0] = (10,10), 80D[1] = (11,10), 80D[2] = (12,10), etc.
# So 80A[2] at (10,12) = 67D[2] at (10,12). Both unknown.

# What if we test SUDAN at 73A pos 1:
# 67D[1] at (9,12) = 73A[1] = S (from SUDAN)
# So 67D = FS?AEOEIO
# What letter at position 2? (10,12) = 80A[2].
# 80A = ?????L (if 80D[5] = L from DELHI)
# Actually 80A at (10,10) len 6 = cols 10-15.
# 80A[0] = (10,10), [1] = (10,11), [2] = (10,12), [3] = (10,13), [4] = (10,14), [5] = (10,15)
# 80A[3] at (10,13) = 53D ROTUNDA row 10 = pos 4 = N.
# 80A[4] at (10,14) = ?
# 80A[5] at (10,15) = ?
# Wait, 80D[5] = L is at (15,10), not (10,15). 80A[5] is at (10,15), different cell!
# So 80A = ???N?? still.
# Previously 80A = ???N?? = ??CNO? was wrong. Let me recompute.
# Hmm, 80D = ??CNOL means:
# 80D[0] = (10,10), 80D[1] = (11,10), 80D[2] = (12,10)=C, 80D[3] = (13,10)=N, 80D[4] = (14,10)=O, 80D[5] = (15,10)=L
# These are all in column 10!
# 80A goes across from (10,10) to (10,15) in row 10, columns 10-15.
# So 80A and 80D share only (10,10). 80A[0] = 80D[0] = same cell.
# The "80A = ??CNO?" pattern I had before was WRONG. Let me recompute 80A properly.

# 80A at (10,10) len 6 = cells (10,10), (10,11), (10,12), (10,13), (10,14), (10,15)
# (10,10): 80D[0] = unknown. 80A[0] = unknown.
# (10,11): 46D at (5,11) len 6. Row 10 = pos 5. 46D[5] = ?. Also no other constraint.
# (10,12): 67D at (8,12). Row 10 = pos 2. 67D[2] = ?. Also 80A[2].
# (10,13): 53D ROTUNDA. Row 10 = pos 4 = N. So 80A[3] = N.
# (10,14): 74D at (9,14) len 6. Row 10 = pos 1. 74D[1] = ?.
# (10,15): 75D at (9,15) len 5. Row 10 = pos 1. 75D[1] = ?.

print("  80A (10,10, len 6): ???N?? (N at pos 3 from ROTUNDA)")
print("    80A was never ??CNO? — that was 80D. Correcting confusion!")
print()

# With DELHI at 114A + SUDAN at 73A:
# 67D = F, S, ?, A, E/N, O, E, I, O
# Wait, let me re-derive 67D completely:
# 67D at (8,12) len 9, col 12:
# pos 0: (8,12) = 66A HAFT[2] = F. ✓
# pos 1: (9,12) = 73A pos 1. If SUDAN: S.
# pos 2: (10,12) = 80A[2]. Unknown.
# pos 3: (11,12) = 88A ADORN[0] = A. ✓
# pos 4: (12,12) = 94A CIRCLEABOUT[5] = E. ✓
# pos 5: (13,12) = 102A PINTO[4] = O. ✓
# pos 6: (14,12) = 109A TOLEDO[3] = E. ✓
# pos 7: (15,12) = 114A. If DELHI at 8-12: pos 12 = I. ✓
# pos 8: (16,12) = 121A TONI pos 1 = O. Wait: 121A at (16,11) len 4 = cols 11-14.
#   Col 12 = pos 1 = O (T-O-N-I). ✓

# So 67D = F, S, ?, A, E, O, E, I, O = FS?AEOEIO
# With only position 2 unknown!
print("  If DELHI at 114A AND SUDAN at 73A:")
print("  67D = FS?AEOEIO (only pos 2 unknown!)")
print("  What letter could pos 2 be?")
print("  67D[2] at (10,12) = 80A[2]")
print()

# For 67D = FS?AEOEIO to be a word/phrase:
# FSA... = FSA? Like an abbreviation?
# FSO... = FSOAEOEIO?
# Let me try each letter:
for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    word = f"FS{letter}AEOEIO"
    # Does this look like a recognizable word or phrase?
    # Check common patterns
    pass

print("  Testing all 26 possibilities for 67D[2]:")
for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    word = f"FS{letter}AEOEIO"
    print(f"    FS{letter}AEOEIO", end="")
    # Try to parse as multi-word
    # Common word breaks: FS + ?AEOEIO, F + S?AEOEIO, FS?A + EOEIO
    # F + S + ?AEOEIO
    # FACE + RADIO → FACERADIO? No, doesn't match
    # Actually none of these parse into English words
    print()

print()
print("CONCLUSION:")
print("67D = FS?AEOEIO doesn't parse into any recognizable English word or phrase.")
print("This strongly suggests EITHER:")
print("  1. SUDAN is NOT in 73A (meaning 73A[1] ≠ S, and 67D[1] ≠ S)")
print("  2. DELHI is NOT in 114A (meaning 67D[7] ≠ I)")
print("  3. Both could be wrong")
print("  4. 67D is a very unusual creative fill we can't guess")
print()
print("DELHI at 114A is more likely correct because it satisfies TWO independent constraints.")
print("SUDAN at 73A is WEAKER because 67D = FS?AEOEIO makes no sense.")
print()
print("If DELHI at 114A is correct but SUDAN at 73A is wrong:")
print("  67D = F??AEOEIO (pos 7 = I from DELHI, but pos 1 still unknown)")
print("  73A still has U at pos 2 but pos 1 is free to be any letter")
print("  SUDAN might be in a different theme entry instead")
