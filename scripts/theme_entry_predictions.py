#!/usr/bin/env python3
"""
Use AROUNDWORLD staircase locations to predict theme entry content.
If 11 locations must be hidden in theme entries as substrings, what theme entries contain them?
"""

# Best AROUNDWORLD candidates for each staircase row:
locations = [
    ("MALI", 4, "Row 1"),
    ("TEHRAN", 6, "Row 2"),
    ("LAGOS", 5, "Row 3"),
    ("SUDAN", 5, "Row 4"),
    ("OMAN", 4, "Row 5"),
    ("ADEN", 4, "Row 6"),
    ("WALES", 5, "Row 7"),
    ("GOA", 3, "Row 8"),
    ("DAKAR", 5, "Row 9"),  # Confirmed in 50A
    ("DELHI", 5, "Row 10"),
    ("CHAD", 4, "Row 11"),
]

# Theme entries with their constraints
theme_entries = {
    "25A": {"length": 16, "known": {}, "text": "?" * 16},
    "50A": {"length": 16, "known": {10: 'A', 13: 'R'}, "text": "?" * 16},
    "73A": {"length": 14, "known": {2: 'U'}, "text": "?" * 14},
    "94A": {"length": 11, "known": {}, "text": "CIRCLEABOUT"},
    "114A": {"length": 14, "known": {9: 'E', 13: 'E'}, "text": "?" * 14},
    "138A": {"length": 16, "known": {4: 'E'}, "text": "?" * 16},
    "167A": {"length": 16, "known": {}, "text": "SUPERBOWLSTADIUM"},
    "19D": {"length": 15, "known": {}, "text": "?" * 15},
    "78D": {"length": 15, "known": {}, "text": "?" * 15},
}

print("=" * 70)
print("THEME ENTRY LOCATION PREDICTIONS")
print("=" * 70)
print()
print("11 AROUNDWORLD locations to hide in theme entries:")
for loc, length, row in locations:
    print(f"  {row}: {loc} ({length} letters)")
print()

# For DAKAR: it's confirmed in 50A at positions 9-13
# 50A pattern: ??????????A??R?? → DAKAR at pos 9 = ..........DAKAR..
# D at 9, A at 10 (matches known A), K at 11, A at 12, R at 13 (matches known R)
print("CONFIRMED: DAKAR in 50A at positions 9-13")
print()

# For each location, check which theme entries could contain it
# given the known letter constraints
print("=" * 70)
print("LOCATION-TO-ENTRY COMPATIBILITY")
print("=" * 70)

for loc, loc_len, row in locations:
    if loc == "DAKAR":
        print(f"\n{loc} ({row}): CONFIRMED in 50A (pos 9-13)")
        continue

    print(f"\n{loc} ({row}, {loc_len} letters):")
    compatible = []

    for entry_name, info in theme_entries.items():
        entry_len = info["length"]
        known = info["known"]
        text = info["text"]

        # Skip already-filled entries
        if text == "CIRCLEABOUT" or text == "SUPERBOWLSTADIUM":
            # Check if location is hidden in the known text
            if loc in text:
                idx = text.index(loc)
                compatible.append((entry_name, idx, "FOUND IN KNOWN TEXT"))
            continue

        # Try each possible starting position
        for start in range(entry_len - loc_len + 1):
            fits = True
            for i, ch in enumerate(loc):
                pos = start + i
                if pos in known and known[pos] != ch:
                    fits = False
                    break
            if fits:
                # Check how many known letters it matches
                matched_known = sum(1 for i, ch in enumerate(loc) if (start+i) in known and known[start+i] == ch)
                compatible.append((entry_name, start, f"matches {matched_known} known"))

    if compatible:
        for entry_name, start, note in compatible:
            print(f"  → {entry_name} at pos {start}-{start+loc_len-1} ({note})")
    else:
        print(f"  → NO compatible entries!")

# ============================================================
# KEY INSIGHT: Location-to-theme assignment
# ============================================================
print("\n" + "=" * 70)
print("ASSIGNMENT ANALYSIS")
print("=" * 70)
print()
print("Each location must be hidden exactly once in a theme entry.")
print("Each theme entry can contain 0, 1, or 2 locations.")
print("We have 7 unfilled entries and 10 remaining locations (DAKAR already assigned).")
print()

# Check which locations are FORCED to be in specific entries
# by looking at which entries have constrained positions

# 73A: ??U??????????? (U at pos 2)
# Locations containing U: SUDAN (S-U-D-A-N), TEHRAN doesn't have U
# If SUDAN is hidden in 73A, it could start at pos 1: ?SUDAN???????? → pos 1 = S, pos 2 = U ✓
# That works! SUDAN at 73A pos 1-5 has U at pos 2 matching the constraint.
print("KEY FINDING: SUDAN could be in 73A starting at pos 1")
print("  73A = ?SUDAN???????? → U at pos 2 matches ROTUNDA constraint!")
print()

# 114A: ?????????E???E (E at pos 9, E at pos 13)
# Which locations have E? ADEN (A-D-E-N), WALES (W-A-L-E-S), TEHRAN (T-E-H-R-A-N), DELHI (D-E-L-H-I)
# ADEN at pos 9: ????????ADEN??E → D at 10, E at 11, N at 12... E at 13 → N ≠ E. Doesn't work.
# ADEN at pos 10: ?????????ADEN?E → A at 10 → but E at 9, A at 10... E ≠ A at pos 10? No:
# Actually: 114A pos 9 = E. If ADEN starts at pos 9: E = A? No, A ≠ E. Doesn't work.
# WALES at pos 9: ?????????WALES → 114A is 14 letters, WALES is 5. Pos 9-13 = WALES
# W at 9: W ≠ E at pos 9. Doesn't work.
# TEHRAN at pos 8: ????????TEHRAN → T at 8, E at 9 ✓, H at 10, R at 11, A at 12, N at 13 → N ≠ E at pos 13. Doesn't work.
# DELHI at pos 9: ?????????DELHI → D at 9 → D ≠ E. Doesn't work.
# DELHI at pos 8: ????????DELHI? → D at 8, E at 9 ✓, L at 10, H at 11, I at 12, then pos 13 = E → next char after DELHI (pos 13) must be E. So 114A[13] = E ✓ is satisfied by the letter AFTER DELHI.
# 114A = ????????DELHIE → pos 8=D, 9=E✓, 10=L, 11=H, 12=I, 13=E✓ → BOTH constraints satisfied!
print("KEY FINDING: DELHI could be in 114A starting at pos 8")
print("  114A = ????????DELHI? → E at pos 9 and E at pos 13 BOTH satisfied!")
print("  (D at 8, E at 9 ✓, L at 10, H at 11, I at 12, E at 13 ✓)")
print()

# What about OMAN at pos 9-12 in 114A?
# OMAN starts at 9: O at 9 → O ≠ E at pos 9. No.

# ADEN in 138A: ????E????I??????
# 138A pos 4 = E, pos 9 = I (if ORGANIC correct)
# ADEN at pos 3: ???ADEN??????????? → A at 3, D at 4 → D ≠ E at pos 4. No.
# ADEN at pos 4: ????ADEN???????? → A at 4 → A ≠ E at pos 4. No.
# ADEN at pos other: just check if ADEN can go somewhere in 138A without conflicting
# 138A = ????E????I??????
# Positions 0-3: unconstrained
# Position 4: E
# Positions 5-8: unconstrained
# Position 9: I (if ORGANIC)
# Positions 10-15: unconstrained
# ADEN at pos 0: ADEN + 12 more. A at 0, D at 1, E at 2, N at 3. No conflict with pos 4 E or pos 9 I.
# Works!
# ADEN at pos 5: ?????ADEN?I?????? → A at 5, D at 6, E at 7, N at 8. No conflict. Works!
# ADEN at pos 10: ????E????IADEN?? → A at 10, D at 11, E at 12, N at 13. No conflict. Works!
# ADEN at pos 12: ????E????I??ADEN → A at 12, D at 13, E at 14, N at 15. No conflict. Works!

print("ADEN can go in many positions in 138A (no conflicts)")
print("  Also in 25A, 19D, 78D (all unconstrained)")
print()

# What about MALI?
# MALI = M-A-L-I (4 letters)
# 73A: ??U??????????? → MALI can't overlap pos 2 (U): M at 2 = U? No. A at 2 = U? No.
# MALI could go elsewhere in 73A: pos 0-1 (MA-), or pos 3+ (no U conflict)
# e.g., 73A pos 0: MALI?????????U → no, pos 2 = L ≠ U. Conflict!
# 73A pos 1: ?MALI?????????U → pos 2 = A ≠ U. Conflict!
# 73A pos 3: ??UMALI???????? → pos 3 = M, no constraint. OK.
# 73A pos 4: ??U?MALI?????? → pos 4 = M, no constraint. OK.
# So MALI can go at pos 3+ in 73A, or in any unconstrained entry.

# Let me specifically check: if SUDAN is at 73A pos 1, and MALI also in 73A:
# 73A = ?SUDAN???MALI? (14 letters) → S at 1, U at 2 ✓, D at 3, A at 4, N at 5, then MALI at pos 9-12
# = ?SUDANXXXMALIY? (example, 14 letters) → This would mean 73A contains BOTH Sudan and Mali!
# That's 5 + 4 = 9 characters out of 14 accounted for by locations.
# The remaining 5 characters (?+XXX+?+Y) need to form a real word/phrase with SUDAN and MALI embedded.
# Example: _SUDANISHMALI_ → "SUDANISH MALI"? Not a phrase.
# Or: ASUDANORMAL? → doesn't work length-wise.
# Hmm, need to think of 14-letter phrases containing both SUDAN and MALI.

print("POTENTIAL DOUBLE-LOCATION ENTRIES:")
print()

# Let me check each theme entry for pairs of locations
from itertools import combinations

unassigned_locs = [loc for loc, _, _ in locations if loc != "DAKAR"]
unfilled_entries = {k: v for k, v in theme_entries.items()
                    if v["text"].startswith("?")}

for entry_name, info in unfilled_entries.items():
    entry_len = info["length"]
    known = info["known"]

    print(f"\n{entry_name} ({entry_len} letters, known: {known}):")

    for loc1, loc2 in combinations(unassigned_locs, 2):
        # Try to fit both locations in this entry without overlap
        for s1 in range(entry_len - len(loc1) + 1):
            # Check loc1 at s1
            ok1 = True
            for i, ch in enumerate(loc1):
                pos = s1 + i
                if pos in known and known[pos] != ch:
                    ok1 = False
                    break
            if not ok1:
                continue

            for s2 in range(entry_len - len(loc2) + 1):
                # Check non-overlapping
                e1 = s1 + len(loc1) - 1
                e2 = s2 + len(loc2) - 1
                if not (s2 > e1 or e2 < s1):
                    continue  # overlapping

                # Check loc2 at s2
                ok2 = True
                for i, ch in enumerate(loc2):
                    pos = s2 + i
                    if pos in known and known[pos] != ch:
                        ok2 = False
                        break
                if not ok2:
                    continue

                # Both fit! But only print interesting ones
                # Only if they use up a reasonable fraction of the entry
                total_loc_chars = len(loc1) + len(loc2)
                if total_loc_chars >= entry_len * 0.4:  # At least 40% coverage
                    print(f"  {loc1}({s1}-{s1+len(loc1)-1}) + {loc2}({s2}-{s2+len(loc2)-1}): "
                          f"{total_loc_chars}/{entry_len} chars covered")

# ============================================================
# FINAL PREDICTIONS
# ============================================================
print("\n" + "=" * 70)
print("BEST PREDICTIONS")
print("=" * 70)
print()
print("Based on constraints, the most likely assignments are:")
print()
print("CONFIRMED:")
print("  50A: contains DAKAR at pos 9-13")
print()
print("STRONG PREDICTIONS:")
print("  73A: contains SUDAN at pos 1-5 (U at pos 2 matches)")
print("  114A: contains DELHI at pos 8-12 (E at pos 9 and 13 both match)")
print()
print("REMAINING 8 locations for 5 entries (25A, 138A, 19D, 78D, + 73A/114A second slots):")
print("  MALI, TEHRAN, LAGOS, OMAN, ADEN, WALES, GOA, CHAD")
print()
print("These 8 locations must fit in the theme entries as substrings.")
print("Some entries will contain 2 locations.")
print()

# Check: 50A with DAKAR
# 50A = ??????????A??R?? → .........DAKAR..
# The A at pos 10 and R at pos 13 are BOTH satisfied by DAKAR (D at 9, A at 10, K at 11, A at 12, R at 13)
# What other location could be in 50A? It's 16 letters with DAKAR at 9-13.
# Remaining positions: 0-8 (9 chars) and 14-15 (2 chars)
# TEHRAN is 6 letters, could fit at pos 0-5 or 1-6 or 2-7 or 3-8
# LAGOS is 5 letters, could fit at pos 0-4 or 1-5 or 2-6 or 3-7 or 4-8
# Example: 50A = XXXLAGOSXDAKARXX → LAGOS at 3-7, DAKAR at 9-13 → 16 chars
# Or: 50A = TEHRANXXXDAKARXX → TEHRAN at 0-5, DAKAR at 9-13 → 16 chars
# Or: 50A = XTEHRANXXDAKARXX → TEHRAN at 1-6, DAKAR at 9-13 → 16 chars

print("50A could also contain a second location before DAKAR:")
for loc, loc_len, row in locations:
    if loc == "DAKAR":
        continue
    # Can this location fit in 50A positions 0-8?
    for start in range(min(9, 16 - loc_len + 1)):
        end = start + loc_len - 1
        if end >= 9:  # Would overlap with DAKAR at 9
            continue
        fits = True
        for i, ch in enumerate(loc):
            pos = start + i
            if pos in theme_entries["50A"]["known"] and theme_entries["50A"]["known"][pos] != ch:
                fits = False
                break
        if fits:
            print(f"  {loc} at pos {start}-{end}")

print("\nDONE!")
