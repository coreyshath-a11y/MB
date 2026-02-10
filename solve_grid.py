#!/usr/bin/env python3
"""
Crossword grid reconstruction from entry number lists.
Reconstructs a 21x21 crossword grid given which numbers are ACROSS and DOWN entries.

Algorithm: Cell-by-cell backtracking with forced constraint propagation.
- Process cells left-to-right, top-to-bottom
- At each white cell, determine if it's numbered based on left_blocked/above_blocked
- Use entry_type to constrain neighbors (right, below)
- Propagate forced values to prune search
"""

import sys
import time

SIZE = 21
MAX_NUM = 176
BLACK = 0
WHITE = 1

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

# Entry types: B=both, A=across only, D=down only, ?=unknown
entry_type = {}
for n in range(1, MAX_NUM + 1):
    a = n in across_set
    d = n in down_set
    if a and d: entry_type[n] = 'B'
    elif a: entry_type[n] = 'A'
    elif d: entry_type[n] = 'D'
    else: entry_type[n] = '?'

print("Entry type sequence (first 30):")
for n in range(1, 31):
    print(f"  {n}: {entry_type[n]}")
print(f"Unknown entries: {[n for n in range(1, MAX_NUM+1) if entry_type[n] == '?']}")

# Grid state
grid = [[None]*SIZE for _ in range(SIZE)]
# Forced values: 0=unforced, 1=forced_white, -1=forced_black
forced = [[0]*SIZE for _ in range(SIZE)]

call_count = 0
start_time = time.time()
solution = None
max_pos_reached = 0

def force_cell(r, c, val, undo_list):
    """Force cell (r,c) to val. Returns False if conflict."""
    if r < 0 or r >= SIZE or c < 0 or c >= SIZE:
        return val == BLACK  # Off-grid is "blocked"

    fval = 1 if val == WHITE else -1

    if forced[r][c] != 0:
        return forced[r][c] == fval

    if grid[r][c] is not None:
        return grid[r][c] == val

    forced[r][c] = fval
    undo_list.append((r, c))
    return True

def undo_forces(undo_list):
    for (r, c) in undo_list:
        forced[r][c] = 0

def solve(pos, next_num):
    global call_count, solution, max_pos_reached
    call_count += 1

    if call_count % 2000000 == 0:
        elapsed = time.time() - start_time
        print(f"  Calls: {call_count/1e6:.1f}M, Time: {elapsed:.1f}s, "
              f"MaxPos: {max_pos_reached}, NextNum: {next_num}", flush=True)
        if elapsed > 600:
            print("TIMEOUT - 10 minutes")
            return False

    if pos == SIZE * SIZE:
        if next_num == MAX_NUM + 1:
            solution = [row[:] for row in grid]
            return True
        return False

    if pos > max_pos_reached:
        max_pos_reached = pos

    r, c = divmod(pos, SIZE)

    # Pruning: remaining cells must fit remaining numbers
    remaining_cells = SIZE * SIZE - pos
    remaining_nums = MAX_NUM + 1 - next_num
    if remaining_nums > remaining_cells:
        return False

    # Determine color options
    if forced[r][c] == 1:
        color_options = [WHITE]
    elif forced[r][c] == -1:
        color_options = [BLACK]
    else:
        color_options = [WHITE, BLACK]

    for color in color_options:
        grid[r][c] = color

        if color == BLACK:
            if solve(pos + 1, next_num):
                return True
            grid[r][c] = None
            continue

        # color == WHITE
        left_blocked = (c == 0) or (grid[r][c-1] == BLACK)
        above_blocked = (r == 0) or (grid[r-1][c] == BLACK)

        if not left_blocked and not above_blocked:
            # Not numbered - just continue
            if solve(pos + 1, next_num):
                return True
            grid[r][c] = None
            continue

        # Cell could be numbered. Generate branches.
        branches = []

        if left_blocked and above_blocked:
            # MUST be numbered (otherwise isolated)
            if next_num > MAX_NUM:
                grid[r][c] = None
                continue

            n = next_num
            t = entry_type[n]
            types_to_try = [t] if t != '?' else ['B', 'A', 'D']

            for tt in types_to_try:
                forces = []
                ok = True

                if tt == 'B':
                    if c + 1 < SIZE: forces.append((r, c+1, WHITE))
                    else: ok = False
                    if ok:
                        if r + 1 < SIZE: forces.append((r+1, c, WHITE))
                        else: ok = False
                elif tt == 'A':
                    if c + 1 < SIZE: forces.append((r, c+1, WHITE))
                    else: ok = False
                    if ok and r + 1 < SIZE:
                        forces.append((r+1, c, BLACK))
                    # r+1 >= SIZE means bottom edge, naturally no down start. OK.
                elif tt == 'D':
                    if r + 1 < SIZE: forces.append((r+1, c, WHITE))
                    else: ok = False
                    if ok and c + 1 < SIZE:
                        forces.append((r, c+1, BLACK))
                    # c+1 >= SIZE means right edge, naturally no across start. OK.

                if ok:
                    branches.append((forces, n + 1))

        elif left_blocked:
            # above_blocked = False
            # Branch 1: numbered as A (if type matches)
            if next_num <= MAX_NUM:
                t = entry_type[next_num]
                if t in ('A', '?'):
                    if c + 1 < SIZE:
                        branches.append(([(r, c+1, WHITE)], next_num + 1))

            # Branch 2: not numbered (right must be black/edge)
            if c + 1 < SIZE:
                branches.append(([(r, c+1, BLACK)], next_num))
            else:
                branches.append(([], next_num))  # at right edge, naturally not across

        elif above_blocked:
            # left_blocked = False
            # Branch 1: numbered as D (if type matches)
            if next_num <= MAX_NUM:
                t = entry_type[next_num]
                if t in ('D', '?'):
                    if r + 1 < SIZE:
                        branches.append(([(r+1, c, WHITE)], next_num + 1))

            # Branch 2: not numbered (below must be black/edge)
            if r + 1 < SIZE:
                branches.append(([(r+1, c, BLACK)], next_num))
            else:
                branches.append(([], next_num))  # at bottom edge, naturally not down

        # Try each branch
        for forces, new_num in branches:
            undo_list = []
            ok = True
            for (fr, fc, fv) in forces:
                if not force_cell(fr, fc, fv, undo_list):
                    ok = False
                    break

            if ok:
                if solve(pos + 1, new_num):
                    return True

            undo_forces(undo_list)

        grid[r][c] = None

    return False

def print_grid(g):
    """Print the grid."""
    for r in range(SIZE):
        row_str = ""
        for c in range(SIZE):
            if g[r][c] == BLACK:
                row_str += "#"
            else:
                row_str += "."
        print(row_str)

def analyze_grid(g):
    """Analyze the grid and return entry information."""
    entries = []
    num = 0

    for r in range(SIZE):
        for c in range(SIZE):
            if g[r][c] != WHITE:
                continue

            left_blocked = (c == 0) or (g[r][c-1] == BLACK)
            above_blocked = (r == 0) or (g[r-1][c] == BLACK)

            starts_across = left_blocked and (c + 1 < SIZE and g[r][c+1] == WHITE)
            starts_down = above_blocked and (r + 1 < SIZE and g[r+1][c] == WHITE)

            if starts_across or starts_down:
                num += 1

                # Calculate word lengths
                across_len = 0
                if starts_across:
                    cc = c
                    while cc < SIZE and g[r][cc] == WHITE:
                        across_len += 1
                        cc += 1

                down_len = 0
                if starts_down:
                    rr = r
                    while rr < SIZE and g[rr][c] == WHITE:
                        down_len += 1
                        rr += 1

                entry = {
                    'num': num,
                    'row': r,
                    'col': c,
                    'across': starts_across,
                    'down': starts_down,
                    'across_len': across_len,
                    'down_len': down_len,
                }
                entries.append(entry)

    return entries

def save_results(g, entries, filename):
    """Save results to markdown file."""
    with open(filename, 'w') as f:
        f.write("# Crossword Grid - Digitized from Entry Lists\n\n")
        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Count stats
        black_count = sum(1 for r in range(SIZE) for c in range(SIZE) if g[r][c] == BLACK)
        white_count = SIZE * SIZE - black_count
        f.write(f"## Statistics\n")
        f.write(f"- Grid size: {SIZE}x{SIZE} = {SIZE*SIZE} cells\n")
        f.write(f"- Black cells: {black_count}\n")
        f.write(f"- White cells: {white_count}\n")
        f.write(f"- Numbered cells: {len(entries)}\n")
        f.write(f"- Across entries: {sum(1 for e in entries if e['across'])}\n")
        f.write(f"- Down entries: {sum(1 for e in entries if e['down'])}\n\n")

        # Grid with # and .
        f.write("## Grid Pattern (# = black, . = white)\n\n")
        f.write("```\n")
        f.write("     " + "".join(f"{c%10}" for c in range(SIZE)) + "\n")
        f.write("     " + "-" * SIZE + "\n")
        for r in range(SIZE):
            row_str = f"{r:2d} | "
            for c in range(SIZE):
                if g[r][c] == BLACK:
                    row_str += "#"
                else:
                    row_str += "."

            f.write(row_str + "\n")
        f.write("```\n\n")

        # Grid with numbers
        f.write("## Grid with Entry Numbers\n\n")
        f.write("```\n")
        # Create a number map
        num_map = {}
        for e in entries:
            num_map[(e['row'], e['col'])] = e['num']

        for r in range(SIZE):
            row_str = ""
            for c in range(SIZE):
                if g[r][c] == BLACK:
                    row_str += " ## "
                elif (r, c) in num_map:
                    row_str += f"{num_map[(r,c)]:3d} "
                else:
                    row_str += "  . "
            f.write(row_str + "\n")
        f.write("```\n\n")

        # Entry list
        f.write("## All Entries\n\n")
        f.write("| # | Row | Col | Across | Down | A-Len | D-Len |\n")
        f.write("|---|-----|-----|--------|------|-------|-------|\n")
        for e in entries:
            a_str = f"{e['across_len']}" if e['across'] else "-"
            d_str = f"{e['down_len']}" if e['down'] else "-"
            a_flag = "Yes" if e['across'] else ""
            d_flag = "Yes" if e['down'] else ""
            f.write(f"| {e['num']} | {e['row']} | {e['col']} | {a_flag} | {d_flag} | {a_str} | {d_str} |\n")

        f.write("\n\n## Across Entries (with word lengths)\n\n")
        for e in entries:
            if e['across']:
                f.write(f"- **{e['num']} Across**: Row {e['row']}, Col {e['col']}, Length {e['across_len']}\n")

        f.write("\n## Down Entries (with word lengths)\n\n")
        for e in entries:
            if e['down']:
                f.write(f"- **{e['num']} Down**: Row {e['row']}, Col {e['col']}, Length {e['down_len']}\n")

def verify_solution(g):
    """Verify that the solution matches the input entry lists."""
    entries = analyze_grid(g)

    computed_across = set(e['num'] for e in entries if e['across'])
    computed_down = set(e['num'] for e in entries if e['down'])

    # Check against input
    across_match = computed_across == across_set
    down_match = computed_down == down_set

    if not across_match:
        print(f"ACROSS MISMATCH!")
        print(f"  Missing from computed: {across_set - computed_across}")
        print(f"  Extra in computed: {computed_across - across_set}")

    if not down_match:
        print(f"DOWN MISMATCH!")
        print(f"  Missing from computed: {down_set - computed_down}")
        print(f"  Extra in computed: {computed_down - down_set}")

    if across_match and down_match:
        print("VERIFICATION PASSED: All entries match!")

    return across_match and down_match, entries

# Pre-seed known constraints
# Rows 19-20 have zero black cells (from pixel analysis)
print("\nPre-seeding: Rows 19-20 all white")
for r in [19, 20]:
    for c in range(SIZE):
        forced[r][c] = 1  # WHITE

print("\nStarting solver...")
start_time = time.time()

if solve(0, 1):
    elapsed = time.time() - start_time
    print(f"\nSOLUTION FOUND in {elapsed:.1f}s after {call_count:,} calls!")
    print()
    print_grid(solution)
    print()

    ok, entries = verify_solution(solution)

    if ok:
        output_file = "/home/user/MB/analysis/CROSSWORD_GRID_DIGITIZED.md"
        save_results(solution, entries, output_file)
        print(f"\nResults saved to {output_file}")
    else:
        print("\nWARNING: Solution does not fully match input. Saving anyway.")
        output_file = "/home/user/MB/analysis/CROSSWORD_GRID_DIGITIZED.md"
        save_results(solution, entries, output_file)
        print(f"Results saved to {output_file}")
else:
    elapsed = time.time() - start_time
    print(f"\nNO SOLUTION FOUND in {elapsed:.1f}s after {call_count:,} calls")
    print(f"Max position reached: {max_pos_reached} (row {max_pos_reached//SIZE}, col {max_pos_reached%SIZE})")
    print(f"Try relaxing constraints.")
