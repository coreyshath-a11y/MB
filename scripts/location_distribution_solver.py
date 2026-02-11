#!/usr/bin/env python3
"""
Solve the distribution of 11 AROUNDWORLD locations across 7 theme entries.
94A and 167A contain no locations, so 11 locations go into:
  25A(16), 50A(16), 73A(14), 114A(14), 138A(16), 19D(15), 78D(15)
  Total: 106 letters for 11 locations (~50 letters)

Constraints:
- Each location is a contiguous substring within ONE theme entry
- Locations cannot overlap within the same entry
- Known letter constraints must be satisfied
- DAKAR at 50A pos 9-13 (CONFIRMED)
- DELHI at 114A pos 8-12 (STRONG)
"""

from itertools import product

print("=" * 70)
print("LOCATION DISTRIBUTION SOLVER")
print("=" * 70)

# 11 AROUNDWORLD locations
locations = {
    "MALI":   4,
    "TEHRAN": 6,
    "LAGOS":  5,
    "SUDAN":  5,
    "OMAN":   4,
    "ADEN":   4,
    "WALES":  5,
    "GOA":    3,
    "DAKAR":  5,
    "DELHI":  5,
    "CHAD":   4,
}

# 7 available theme entries (94A and 167A excluded - no location substrings)
entries = {
    "25A":  {"length": 16, "known": {}},
    "50A":  {"length": 16, "known": {10: 'A', 13: 'R'}},
    "73A":  {"length": 14, "known": {2: 'U'}},
    "114A": {"length": 14, "known": {9: 'E', 13: 'E'}},
    "138A": {"length": 16, "known": {4: 'E'}},
    "19D":  {"length": 15, "known": {}},
    "78D":  {"length": 15, "known": {}},
}

def can_place(loc_name, entry_key, start):
    """Check if location fits at given position without conflicts."""
    entry = entries[entry_key]
    if start + len(loc_name) > entry["length"]:
        return False
    for i, ch in enumerate(loc_name):
        pos = start + i
        if pos in entry["known"] and entry["known"][pos] != ch:
            return False
    return True

def constraint_matches(loc_name, entry_key, start):
    """Count how many known constraints are satisfied."""
    entry = entries[entry_key]
    matches = 0
    for i, ch in enumerate(loc_name):
        pos = start + i
        if pos in entry["known"] and entry["known"][pos] == ch:
            matches += 1
    return matches

def locations_overlap(placements_in_entry):
    """Check if any placements in the same entry overlap."""
    for i, (loc1, start1) in enumerate(placements_in_entry):
        end1 = start1 + len(loc1) - 1
        for j, (loc2, start2) in enumerate(placements_in_entry):
            if i >= j:
                continue
            end2 = start2 + len(loc2) - 1
            if start1 <= end2 and start2 <= end1:
                return True
    return False


# First: enumerate valid placements for each location in each entry
print("\n--- Valid placements per location ---")
valid_placements = {}  # loc -> list of (entry, start, matches)

for loc_name, loc_len in locations.items():
    placements = []
    for entry_key in entries:
        entry = entries[entry_key]
        for start in range(entry["length"] - loc_len + 1):
            if can_place(loc_name, entry_key, start):
                matches = constraint_matches(loc_name, entry_key, start)
                placements.append((entry_key, start, matches))
    valid_placements[loc_name] = placements
    best_match = max((p[2] for p in placements), default=0)
    total_valid = len(placements)
    constrained = [p for p in placements if p[2] > 0]
    print(f"  {loc_name}: {total_valid} valid positions, {len(constrained)} with constraint matches (best={best_match})")
    if constrained:
        for entry, start, matches in constrained:
            print(f"    {entry} pos {start}-{start+loc_len-1}: {matches} match(es)")


# Fixed placements (high confidence)
print("\n--- Fixed placements (confirmed/strong) ---")
fixed = {
    "DAKAR": ("50A", 9),   # 2 constraint matches
    "DELHI": ("114A", 8),  # 1 constraint match (E@9)
}

for loc, (entry, start) in fixed.items():
    matches = constraint_matches(loc, entry, start)
    print(f"  {loc} → {entry} pos {start}-{start+len(loc)-1} ({matches} matches) FIXED")

# Find best placement for each remaining location
remaining = [loc for loc in locations if loc not in fixed]
print(f"\n--- Remaining locations to place: {remaining} ---")

# Score each possible assignment
# For now, let's find which locations MUST go in certain entries
# based on constraint matching

print("\n--- Constraint-based assignment ---")
for loc in remaining:
    best_constrained = [p for p in valid_placements[loc] if p[2] > 0]
    if best_constrained:
        best = max(best_constrained, key=lambda p: p[2])
        print(f"  {loc}: best = {best[0]} pos {best[1]}-{best[1]+len(loc)-1} ({best[2]} matches)")
    else:
        print(f"  {loc}: no constraint-matching positions (can go in any unconstrained entry)")


# Check: which entries from fixed placements still have room?
print("\n--- Capacity analysis ---")
for entry_key in entries:
    entry_len = entries[entry_key]["length"]
    fixed_in_entry = [(loc, start) for loc, (e, start) in fixed.items() if e == entry_key]

    used_positions = set()
    for loc, start in fixed_in_entry:
        for i in range(len(loc)):
            used_positions.add(start + i)

    free_positions = entry_len - len(used_positions)
    print(f"  {entry_key} (len {entry_len}): {len(fixed_in_entry)} fixed, "
          f"{len(used_positions)} used, {free_positions} free")

    # Can any remaining location fit in the free space?
    if fixed_in_entry:
        for loc in remaining:
            loc_len = len(loc)
            for start in range(entry_len - loc_len + 1):
                end = start + loc_len - 1
                # Check no overlap with fixed placements
                overlap = any(start <= p <= end for p in used_positions)
                if not overlap and can_place(loc, entry_key, start):
                    matches = constraint_matches(loc, entry_key, start)
                    if matches > 0:
                        print(f"    {loc} can fit at pos {start}-{end} ({matches} matches) ★")


# Try ADEN in 114A alongside DELHI
print("\n--- Testing ADEN + DELHI coexistence in 114A ---")
delhi_start = 8
delhi_end = 12
for start in range(14 - 4 + 1):
    end = start + 3
    # Check no overlap with DELHI
    if end < delhi_start or start > delhi_end:
        if can_place("ADEN", "114A", start):
            matches = constraint_matches("ADEN", "114A", start)
            print(f"  ADEN at pos {start}-{end}: valid ✓ ({matches} constraint matches)")

# Try TEHRAN in 50A alongside DAKAR
print("\n--- Testing TEHRAN + DAKAR coexistence in 50A ---")
dakar_start = 9
dakar_end = 13
for start in range(16 - 6 + 1):
    end = start + 5
    if end < dakar_start or start > dakar_end:
        if can_place("TEHRAN", "50A", start):
            matches = constraint_matches("TEHRAN", "50A", start)
            print(f"  TEHRAN at pos {start}-{end}: valid ✓ ({matches} constraint matches)")

# Try MALI in 50A alongside DAKAR
print("\n--- Testing MALI + DAKAR coexistence in 50A ---")
for start in range(16 - 4 + 1):
    end = start + 3
    if end < dakar_start or start > dakar_end:
        if can_place("MALI", "50A", start):
            matches = constraint_matches("MALI", "50A", start)
            print(f"  MALI at pos {start}-{end}: valid ✓ ({matches} constraint matches)")

# What about LAGOS, OMAN, SUDAN, WALES, GOA, CHAD in 73A?
print("\n--- Testing locations in 73A (pos 2=U) ---")
for loc in remaining:
    for start in range(14 - len(loc) + 1):
        if can_place(loc, "73A", start):
            matches = constraint_matches(loc, "73A", start)
            if matches > 0:
                print(f"  {loc} at 73A pos {start}-{start+len(loc)-1}: {matches} match(es) ★")

# What about 138A (pos 4=E)?
print("\n--- Testing locations in 138A (pos 4=E) ---")
for loc in remaining:
    for start in range(16 - len(loc) + 1):
        if can_place(loc, "138A", start):
            matches = constraint_matches(loc, "138A", start)
            if matches > 0:
                print(f"  {loc} at 138A pos {start}-{start+len(loc)-1}: {matches} match(es) ★")


# Summary: proposed distribution
print("\n" + "=" * 70)
print("PROPOSED LOCATION DISTRIBUTION")
print("=" * 70)
print("""
CONFIRMED/STRONG:
  50A:  DAKAR at pos 9-13 (2 constraint matches) ★★★
  114A: DELHI at pos 8-12 (1 constraint match) ★★★

LIKELY (based on constraint matching):
  50A:  + TEHRAN at pos 0-5 or 1-6 (no overlap with DAKAR, 1 match if pos 6-11)
  114A: + ADEN at pos 0-3 or 3-6 (no overlap with DELHI, unconstrained)
  73A:  SUDAN at pos 1-5 (1 match: U@2) — but WEAK due to 67D conflict
  138A: WALES at pos 1-5 (1 match: E@4) or TEHRAN at pos 3-8 (1 match: E@4)

UNCONSTRAINED (could go in 25A, 19D, 78D):
  MALI (4), LAGOS (5), OMAN (4), GOA (3), CHAD (4)
  + whatever doesn't go in constrained entries

KEY QUESTION: Do 94A and 167A truly have 0 hidden locations?
  If so, 7 entries hold 11 locations → average 1.6 per entry.
  With DAKAR+TEHRAN in 50A and DELHI+ADEN in 114A, that's 4 placed.
  Remaining 7 locations need 5 entries. Some entries get 2, some get 1.
""")
