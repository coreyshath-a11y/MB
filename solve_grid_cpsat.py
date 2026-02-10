#!/usr/bin/env python3
"""
Crossword grid reconstruction using OR-tools CP-SAT solver.

Variables: grid[r][c] = 0 (BLACK) or 1 (WHITE) for each cell
           num[r][c] = entry number assigned to cell (0 if not numbered)

Constraints encode crossword numbering rules and match against the
known ACROSS and DOWN entry lists.
"""

import time
from ortools.sat.python import cp_model

SIZE = 21
MAX_NUM = 176

# Entry data
across_set = set([1,8,14,22,23,24,25,28,29,30,31,32,34,35,36,38,41,42,43,45,
    47,48,50,54,57,58,59,61,63,64,66,68,70,72,73,77,79,80,81,82,83,85,88,90,
    91,92,94,97,99,100,102,103,105,106,107,109,111,113,114,117,119,120,121,123,
    124,127,129,132,134,136,138,141,143,145,148,153,155,156,158,159,161,164,165,
    167,171,172,173,174,175,176])

down_set = set([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,26,
    27,33,37,39,40,43,44,46,49,51,52,53,55,56,60,62,65,67,69,71,72,74,75,76,
    77,78,80,83,84,86,87,89,93,95,96,98,101,104,108,110,112,115,116,117,118,
    122,124,125,126,128,130,131,133,135,137,139,140,141,142,144,150,151,152,154,
    157,160,162,163,166,168,169,170])

# Compute entry types
entry_type = {}
for n in range(1, MAX_NUM + 1):
    a = n in across_set
    d = n in down_set
    if a and d: entry_type[n] = 'B'
    elif a: entry_type[n] = 'A'
    elif d: entry_type[n] = 'D'
    else: entry_type[n] = '?'  # unknown (146, 147, 149)

print("Entry types for entries 1-30:")
for n in range(1, 31):
    print(f"  {n}: {entry_type[n]}")
print(f"Unknown entries: {[n for n in range(1, MAX_NUM+1) if entry_type[n] == '?']}")

# Build the model
model = cp_model.CpModel()
print("\nBuilding CP-SAT model...")

# Variables: is_white[r][c] = 1 if white, 0 if black
is_white = {}
for r in range(SIZE):
    for c in range(SIZE):
        is_white[r, c] = model.NewBoolVar(f'w_{r}_{c}')

# Helper: is_left_blocked[r][c] = 1 if (c==0) or cell to left is black
is_left_blocked = {}
for r in range(SIZE):
    for c in range(SIZE):
        if c == 0:
            is_left_blocked[r, c] = model.NewConstant(1)
        else:
            # left_blocked = NOT is_white[r][c-1]
            is_left_blocked[r, c] = is_white[r, c-1].Not()

# Helper: is_above_blocked[r][c]
is_above_blocked = {}
for r in range(SIZE):
    for c in range(SIZE):
        if r == 0:
            is_above_blocked[r, c] = model.NewConstant(1)
        else:
            is_above_blocked[r, c] = is_white[r-1, c].Not()

# starts_across[r][c] = white AND left_blocked AND right_is_white
starts_across = {}
for r in range(SIZE):
    for c in range(SIZE):
        sa = model.NewBoolVar(f'sa_{r}_{c}')
        starts_across[r, c] = sa
        if c + 1 >= SIZE:
            # Can't start across at rightmost column
            model.Add(sa == 0)
        else:
            # sa = is_white[r,c] AND is_left_blocked[r,c] AND is_white[r,c+1]
            model.AddBoolAnd([is_white[r, c], is_left_blocked[r, c], is_white[r, c+1]]).OnlyEnforceIf(sa)
            model.AddBoolOr([is_white[r, c].Not(), is_left_blocked[r, c].Not(), is_white[r, c+1].Not()]).OnlyEnforceIf(sa.Not())

# starts_down[r][c] = white AND above_blocked AND below_is_white
starts_down = {}
for r in range(SIZE):
    for c in range(SIZE):
        sd = model.NewBoolVar(f'sd_{r}_{c}')
        starts_down[r, c] = sd
        if r + 1 >= SIZE:
            model.Add(sd == 0)
        else:
            model.AddBoolAnd([is_white[r, c], is_above_blocked[r, c], is_white[r+1, c]]).OnlyEnforceIf(sd)
            model.AddBoolOr([is_white[r, c].Not(), is_above_blocked[r, c].Not(), is_white[r+1, c].Not()]).OnlyEnforceIf(sd.Not())

# is_numbered[r][c] = starts_across OR starts_down
is_numbered = {}
for r in range(SIZE):
    for c in range(SIZE):
        n = model.NewBoolVar(f'num_{r}_{c}')
        is_numbered[r, c] = n
        # n = sa OR sd
        model.AddBoolOr([starts_across[r, c], starts_down[r, c]]).OnlyEnforceIf(n)
        model.AddBoolAnd([starts_across[r, c].Not(), starts_down[r, c].Not()]).OnlyEnforceIf(n.Not())

# Total numbered cells must equal MAX_NUM
model.Add(sum(is_numbered[r, c] for r in range(SIZE) for c in range(SIZE)) == MAX_NUM)

# Now we need to assign entry numbers 1..176 to the numbered cells in reading order.
# This is the tricky part. We need to map reading-order position to entry number.
#
# Approach: for each cell (r,c), define entry_number[r,c] which is the entry number
# if the cell is numbered, or 0 if not.
# The entry numbers must be consecutive: 1, 2, 3, ..., 176 in reading order.
#
# Alternative approach: define cum_count[r,c] = number of numbered cells at or before (r,c)
# in reading order. Then cell (r,c) has entry number cum_count[r,c] if it's numbered.

# cum_count[r][c] = sum of is_numbered for all cells up to and including (r,c) in reading order
# We can compute this incrementally.

print("Building cumulative count constraints...")

cum_count = {}
prev_var = None
for r in range(SIZE):
    for c in range(SIZE):
        cc = model.NewIntVar(0, MAX_NUM, f'cc_{r}_{c}')
        cum_count[r, c] = cc
        if r == 0 and c == 0:
            # First cell
            model.Add(cc == is_numbered[0, 0])
        else:
            # Previous cell in reading order
            if c == 0:
                prev = cum_count[r-1, SIZE-1]
            else:
                prev = cum_count[r, c-1]
            model.Add(cc == prev + is_numbered[r, c])

# The last cell's cumulative count must equal MAX_NUM
model.Add(cum_count[SIZE-1, SIZE-1] == MAX_NUM)

# Now, for each entry number n (1..176), we need to find the cell where cum_count == n
# and is_numbered == 1, and check its starts_across/starts_down against the entry lists.
#
# Approach: for each cell (r,c), if is_numbered[r,c] == 1, then its entry number is
# cum_count[r,c]. We need cum_count[r,c] to be in across_set iff starts_across is true,
# and in down_set iff starts_down is true.
#
# But this is hard to encode directly because cum_count is an integer variable.
# Instead, let's use indicator variables.

# For each cell and each entry number, define: is_entry_n[r,c,n] = 1 iff cell (r,c)
# has entry number n. But that's SIZE*SIZE*MAX_NUM = 441*176 = ~77K variables. Feasible.

# Actually, a better approach: for each entry number n, create a boolean variable for each
# cell indicating if that cell has this entry number. Then constrain based on type.

# But 77K booleans might be slow. Let me try a different encoding.

# Alternative: for each cell (r,c), if it's numbered, its entry number determines
# whether it should start across/down. We can encode this using element constraints.

# Create arrays for across membership and down membership
across_membership = [1 if n in across_set else 0 for n in range(MAX_NUM + 1)]  # index 0..176
down_membership = [1 if n in down_set else 0 for n in range(MAX_NUM + 1)]

print("Building entry type constraints...")

# For each cell (r,c): if is_numbered, then:
#   starts_across[r,c] == across_membership[cum_count[r,c]]
#   starts_down[r,c] == down_membership[cum_count[r,c]]
#
# If NOT numbered: cum_count constraint is already handled.
#
# Use AddElement constraint: model.AddElement(index, array, target)
# which means array[index] == target

for r in range(SIZE):
    for c in range(SIZE):
        # If numbered: across_membership[cum_count] must equal starts_across
        # If not numbered: no constraint needed (cum_count doesn't change)

        # When numbered:
        # Create a temp var for the across membership lookup
        sa_lookup = model.NewIntVar(0, 1, f'sal_{r}_{c}')
        model.AddElement(cum_count[r, c], across_membership, sa_lookup)

        sd_lookup = model.NewIntVar(0, 1, f'sdl_{r}_{c}')
        model.AddElement(cum_count[r, c], down_membership, sd_lookup)

        # When the cell is numbered, its starts_across must match the lookup
        # starts_across[r,c] == sa_lookup when is_numbered[r,c]
        # starts_down[r,c] == sd_lookup when is_numbered[r,c]

        # If numbered and starts_across: sa_lookup must be 1
        # If numbered and not starts_across: sa_lookup must be 0
        model.Add(sa_lookup == 1).OnlyEnforceIf(is_numbered[r, c], starts_across[r, c])
        model.Add(sa_lookup == 0).OnlyEnforceIf(is_numbered[r, c], starts_across[r, c].Not())

        # Same for down
        model.Add(sd_lookup == 1).OnlyEnforceIf(is_numbered[r, c], starts_down[r, c])
        model.Add(sd_lookup == 0).OnlyEnforceIf(is_numbered[r, c], starts_down[r, c].Not())

# Pre-seed known constraints
print("Adding known constraints...")

# Row 1 all white (from analysis)
for c in range(SIZE):
    model.Add(is_white[1, c] == 1)

# Rows 19-20 all white
for r in [19, 20]:
    for c in range(SIZE):
        model.Add(is_white[r, c] == 1)

# Row 0 analytical constraint: exactly 2 white runs (length 7 and 6) separated by 1 black
# Pattern: X blacks, 7 whites, 1 black, 6 whites, (7-X) blacks
# We know there are exactly 8 black cells in row 0
row0_blacks = sum(is_white[0, c].Not() for c in range(SIZE))
model.Add(row0_blacks == 8)

# Entry 1 must be type B: first numbered cell starts both across and down
# This means first white cell in row 0 has left_blocked, starts_across, starts_down
# Entry 8 must be type B: second run start
# The first 7 entries (1-7) are: B D D D D D D
# The next 6 entries (8-13) are: B D D D D D
# This means row 0 has exactly 2 white runs

# Constraint: row 0 has exactly 2 "runs" of white cells
# A run starts when a cell is white and the previous cell is black (or it's the first cell)
# We already constrain 8 black cells. Let's also constrain the structure.

# Additional constraint: (18,0) must be WHITE (from end-game analysis)
model.Add(is_white[18, 0] == 1)

# Solve
print("\nSolving...")
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 600
solver.parameters.num_workers = 4
solver.parameters.log_search_progress = True

status = solver.Solve(model)

print(f"\nStatus: {solver.StatusName(status)}")
print(f"Time: {solver.WallTime():.1f}s")

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print("\nSOLUTION FOUND!")

    # Extract grid
    grid = [[0]*SIZE for _ in range(SIZE)]
    for r in range(SIZE):
        for c in range(SIZE):
            grid[r][c] = solver.Value(is_white[r, c])

    # Print grid
    print("\nGrid:")
    for r in range(SIZE):
        print(''.join('#' if grid[r][c] == 0 else '.' for c in range(SIZE)))

    # Verify and analyze
    entries = []
    num = 0
    for r in range(SIZE):
        for c in range(SIZE):
            if grid[r][c] == 0:
                continue
            lb = (c == 0) or (grid[r][c-1] == 0)
            ab = (r == 0) or (grid[r-1][c] == 0)
            sa = lb and (c + 1 < SIZE and grid[r][c+1] == 1)
            sd = ab and (r + 1 < SIZE and grid[r+1][c] == 1)
            if sa or sd:
                num += 1
                al = 0
                if sa:
                    cc = c
                    while cc < SIZE and grid[r][cc] == 1:
                        al += 1
                        cc += 1
                dl = 0
                if sd:
                    rr = r
                    while rr < SIZE and grid[rr][c] == 1:
                        dl += 1
                        rr += 1
                entries.append({
                    'num': num, 'row': r, 'col': c,
                    'across': sa, 'down': sd,
                    'across_len': al, 'down_len': dl,
                })

    print(f"\nTotal numbered cells: {num}")

    # Verify
    comp_across = set(e['num'] for e in entries if e['across'])
    comp_down = set(e['num'] for e in entries if e['down'])

    if comp_across == across_set and comp_down == down_set:
        print("VERIFICATION PASSED!")
    else:
        if comp_across != across_set:
            print(f"ACROSS mismatch! Missing: {across_set - comp_across}, Extra: {comp_across - across_set}")
        if comp_down != down_set:
            print(f"DOWN mismatch! Missing: {down_set - comp_down}, Extra: {comp_down - comp_down}")

    # Save results
    output_file = "/home/user/MB/analysis/CROSSWORD_GRID_DIGITIZED.md"
    with open(output_file, 'w') as f:
        f.write("# Crossword Grid - Digitized from Entry Lists\n\n")
        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        black_count = sum(1 for r in range(SIZE) for c in range(SIZE) if grid[r][c] == 0)
        f.write(f"## Statistics\n")
        f.write(f"- Grid size: {SIZE}x{SIZE} = {SIZE*SIZE} cells\n")
        f.write(f"- Black cells: {black_count}\n")
        f.write(f"- White cells: {SIZE*SIZE - black_count}\n")
        f.write(f"- Numbered cells: {len(entries)}\n")
        f.write(f"- Across entries: {sum(1 for e in entries if e['across'])}\n")
        f.write(f"- Down entries: {sum(1 for e in entries if e['down'])}\n\n")

        f.write("## Grid Pattern (# = black, . = white)\n\n```\n")
        f.write("     " + "".join(f"{c%10}" for c in range(SIZE)) + "\n")
        f.write("     " + "-" * SIZE + "\n")
        for r in range(SIZE):
            row_str = f"{r:2d} | "
            for c in range(SIZE):
                row_str += "#" if grid[r][c] == 0 else "."
            f.write(row_str + "\n")
        f.write("```\n\n")

        f.write("## Grid with Entry Numbers\n\n```\n")
        num_map = {}
        for e in entries:
            num_map[(e['row'], e['col'])] = e['num']
        for r in range(SIZE):
            row_str = ""
            for c in range(SIZE):
                if grid[r][c] == 0:
                    row_str += " ## "
                elif (r, c) in num_map:
                    row_str += f"{num_map[(r,c)]:3d} "
                else:
                    row_str += "  . "
            f.write(row_str + "\n")
        f.write("```\n\n")

        f.write("## All Entries\n\n")
        f.write("| # | Row | Col | Across | Down | A-Len | D-Len |\n")
        f.write("|---|-----|-----|--------|------|-------|-------|\n")
        for e in entries:
            a_str = f"{e['across_len']}" if e['across'] else "-"
            d_str = f"{e['down_len']}" if e['down'] else "-"
            a_flag = "Yes" if e['across'] else ""
            d_flag = "Yes" if e['down'] else ""
            f.write(f"| {e['num']} | {e['row']} | {e['col']} | {a_flag} | {d_flag} | {a_str} | {d_str} |\n")

        f.write("\n\n## Across Entries\n\n")
        for e in entries:
            if e['across']:
                f.write(f"- **{e['num']} Across**: Row {e['row']}, Col {e['col']}, Length {e['across_len']}\n")

        f.write("\n## Down Entries\n\n")
        for e in entries:
            if e['down']:
                f.write(f"- **{e['num']} Down**: Row {e['row']}, Col {e['col']}, Length {e['down_len']}\n")

    print(f"\nResults saved to {output_file}")

else:
    print("NO SOLUTION FOUND")
    if status == cp_model.INFEASIBLE:
        print("Model is infeasible - check constraints")
    elif status == cp_model.MODEL_INVALID:
        print("Model is invalid")
