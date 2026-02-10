#!/usr/bin/env python3
"""
Crossword grid reconstruction - optimized with analytical seeds.

Key insight: Row 0 has exactly 2 white runs of length 7 and 6 (entries 1-7 and 8-13),
separated by 1 black cell, with X blacks at start and (7-X) blacks at end.
Row 1 is all white, giving entries 14-21.
Rows 19-20 are all white (from pixel analysis).

We try X from 1 to 7 and solve the remaining grid (rows 2-18).
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

entry_type = {}
for n in range(1, MAX_NUM + 1):
    a = n in across_set
    d = n in down_set
    if a and d: entry_type[n] = 'B'
    elif a: entry_type[n] = 'A'
    elif d: entry_type[n] = 'D'
    else: entry_type[n] = '?'

print("Entry types 1-25:", [entry_type[n] for n in range(1, 26)])
print("Unknown entries:", [n for n in range(1, MAX_NUM+1) if entry_type[n] == '?'])

call_count = 0
start_time = 0
solution_found = None

def solve_for_x(X):
    """Try solving with X leading blacks in row 0."""
    global call_count, start_time, solution_found

    print(f"\n{'='*60}")
    print(f"Trying X={X} (row 0: {X} blacks, 7 whites, 1 black, 6 whites, {7-X} blacks)")
    print(f"{'='*60}")

    grid = [[None]*SIZE for _ in range(SIZE)]

    # Row 0: X blacks, 7 whites, 1 black, 6 whites, (7-X) blacks
    for c in range(SIZE):
        if c < X:
            grid[0][c] = BLACK
        elif c < X + 7:
            grid[0][c] = WHITE
        elif c == X + 7:
            grid[0][c] = BLACK
        elif c < X + 14:
            grid[0][c] = WHITE
        else:
            grid[0][c] = BLACK

    # Row 1: all WHITE
    for c in range(SIZE):
        grid[1][c] = WHITE

    # Rows 19-20: all WHITE
    for r in [19, 20]:
        for c in range(SIZE):
            grid[r][c] = WHITE

    # Force row 2 cells from down entries in row 1
    # Entry 14 (B) at (1,0): forces (2,0) WHITE
    grid[2][0] = WHITE
    # D entries in row 1 at columns where row 0 is BLACK
    for c in range(1, SIZE):
        if grid[0][c] == BLACK:
            # (1,c) has above_blocked -> starts down -> (2,c) must be WHITE
            if grid[2][c] is None:
                grid[2][c] = WHITE

    # Print row 0 pattern
    r0 = ''.join('#' if grid[0][c] == BLACK else '.' for c in range(SIZE))
    print(f"Row 0: {r0}")
    r1_entries = []
    for c in range(SIZE):
        if grid[0][c] == BLACK:
            r1_entries.append(c)
    print(f"Row 1 entries with above_blocked at cols: [0] + {r1_entries[1:] if len(r1_entries) > 1 else r1_entries}")
    r2 = ''.join('#' if grid[2][c] == BLACK else ('.' if grid[2][c] == WHITE else '?') for c in range(SIZE))
    print(f"Row 2 forced: {r2}")

    call_count = 0
    start_time = time.time()
    max_pos = [0]

    def force(r, c, val, undo):
        """Force cell to val. Returns False if conflict."""
        if r < 0 or r >= SIZE or c < 0 or c >= SIZE:
            return val == BLACK  # off-grid treated as blocked
        if grid[r][c] is not None:
            return grid[r][c] == val
        grid[r][c] = val
        undo.append((r, c))
        return True

    def unforce(undo):
        for r, c in undo:
            grid[r][c] = None

    def solve(pos, next_num):
        global call_count, solution_found
        call_count += 1

        if call_count % 5000000 == 0:
            elapsed = time.time() - start_time
            rr, cc = divmod(pos, SIZE) if pos < SIZE*SIZE else (SIZE, 0)
            print(f"  X={X}: {call_count/1e6:.0f}M calls, {elapsed:.0f}s, "
                  f"pos=({rr},{cc}), num={next_num}, maxpos={max_pos[0]}", flush=True)
            if elapsed > 180:
                print("  TIMEOUT at 3 minutes, trying next X")
                return False

        if pos == SIZE * SIZE:
            if next_num == MAX_NUM + 1:
                solution_found = [row[:] for row in grid]
                return True
            return False

        if pos > max_pos[0]:
            max_pos[0] = pos

        r, c = divmod(pos, SIZE)

        # Pruning: not enough cells left for remaining entries
        remaining_cells = SIZE * SIZE - pos
        remaining_nums = MAX_NUM + 1 - next_num
        if remaining_nums > remaining_cells:
            return False

        # If cell is already set, process directly
        if grid[r][c] is not None:
            return process_white_or_black(r, c, pos, next_num, grid[r][c], False, max_pos)

        # Cell is undecided - try WHITE first (most cells are white), then BLACK
        for color in (WHITE, BLACK):
            if process_white_or_black(r, c, pos, next_num, color, True, max_pos):
                return True
        return False

    def process_white_or_black(r, c, pos, next_num, color, undoable, max_pos):
        global call_count, solution_found

        if undoable:
            grid[r][c] = color

        if color == BLACK:
            result = solve(pos + 1, next_num)
            if not result and undoable:
                grid[r][c] = None
            return result

        # WHITE cell
        left_blocked = (c == 0) or (grid[r][c-1] == BLACK)
        above_blocked = (r == 0) or (grid[r-1][c] == BLACK)

        if not left_blocked and not above_blocked:
            # Not a potential numbered cell - just continue
            result = solve(pos + 1, next_num)
            if not result and undoable:
                grid[r][c] = None
            return result

        # Cell might be numbered. Build branches.
        branches = []

        if left_blocked and above_blocked:
            # Could be numbered (B/A/D) or not numbered (isolated)
            if next_num <= MAX_NUM:
                t = entry_type[next_num]
                types_to_try = [t] if t != '?' else ['B', 'A', 'D']

                for tt in types_to_try:
                    forces = []
                    ok = True

                    if tt == 'B':
                        if c + 1 < SIZE:
                            forces.append((r, c+1, WHITE))
                        else:
                            ok = False
                        if ok:
                            if r + 1 < SIZE:
                                forces.append((r+1, c, WHITE))
                            else:
                                ok = False
                    elif tt == 'A':
                        if c + 1 < SIZE:
                            forces.append((r, c+1, WHITE))
                        else:
                            ok = False
                        if ok and r + 1 < SIZE:
                            forces.append((r+1, c, BLACK))
                    elif tt == 'D':
                        if r + 1 < SIZE:
                            forces.append((r+1, c, WHITE))
                        else:
                            ok = False
                        if ok and c + 1 < SIZE:
                            forces.append((r, c+1, BLACK))

                    if ok:
                        branches.append((forces, next_num + 1))

            # Not numbered branch: right=BLACK/edge AND below=BLACK/edge
            nn_forces = []
            nn_ok = True
            if c + 1 < SIZE:
                nn_forces.append((r, c+1, BLACK))
            if r + 1 < SIZE:
                nn_forces.append((r+1, c, BLACK))
            branches.append((nn_forces, next_num))

        elif left_blocked:
            # above_blocked = False. Can only start across (type A).
            if next_num <= MAX_NUM:
                t = entry_type[next_num]
                if t in ('A', '?'):
                    if c + 1 < SIZE:
                        branches.append(([(r, c+1, WHITE)], next_num + 1))

            # Not numbered: right must be BLACK/edge
            if c + 1 < SIZE:
                branches.append(([(r, c+1, BLACK)], next_num))
            else:
                branches.append(([], next_num))

        elif above_blocked:
            # left_blocked = False. Can only start down (type D).
            if next_num <= MAX_NUM:
                t = entry_type[next_num]
                if t in ('D', '?'):
                    if r + 1 < SIZE:
                        branches.append(([(r+1, c, WHITE)], next_num + 1))

            # Not numbered: below must be BLACK/edge
            if r + 1 < SIZE:
                branches.append(([(r+1, c, BLACK)], next_num))
            else:
                branches.append(([], next_num))

        # Try each branch
        for forces, new_num in branches:
            undo = []
            ok = True
            for (fr, fc, fv) in forces:
                if not force(fr, fc, fv, undo):
                    ok = False
                    break

            if ok:
                if solve(pos + 1, new_num):
                    return True

            unforce(undo)

        if undoable:
            grid[r][c] = None
        return False

    # Run solver
    if solve(0, 1):
        elapsed = time.time() - start_time
        print(f"\nSOLUTION FOUND! X={X}, {elapsed:.1f}s, {call_count:,} calls")
        return True
    else:
        elapsed = time.time() - start_time
        print(f"\nNo solution for X={X} after {elapsed:.1f}s, {call_count:,} calls")
        print(f"  Max position: {max_pos[0]} (row {max_pos[0]//SIZE}, col {max_pos[0]%SIZE})")
        return False


def print_grid(g):
    for r in range(SIZE):
        print(''.join('#' if g[r][c] == BLACK else '.' for c in range(SIZE)))

def analyze_grid(g):
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
                entries.append({
                    'num': num, 'row': r, 'col': c,
                    'across': starts_across, 'down': starts_down,
                    'across_len': across_len, 'down_len': down_len,
                })
    return entries

def verify_solution(g):
    entries = analyze_grid(g)
    computed_across = set(e['num'] for e in entries if e['across'])
    computed_down = set(e['num'] for e in entries if e['down'])
    across_match = computed_across == across_set
    down_match = computed_down == down_set

    if not across_match:
        print(f"ACROSS MISMATCH!")
        print(f"  Missing: {across_set - computed_across}")
        print(f"  Extra: {computed_across - across_set}")
    if not down_match:
        print(f"DOWN MISMATCH!")
        print(f"  Missing: {down_set - computed_down}")
        print(f"  Extra: {computed_down - down_set}")
    if across_match and down_match:
        print("VERIFICATION PASSED!")
    return across_match and down_match, entries

def save_results(g, entries, filename):
    with open(filename, 'w') as f:
        f.write("# Crossword Grid - Digitized from Entry Lists\n\n")
        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        black_count = sum(1 for r in range(SIZE) for c in range(SIZE) if g[r][c] == BLACK)
        white_count = SIZE * SIZE - black_count
        f.write(f"## Statistics\n")
        f.write(f"- Grid size: {SIZE}x{SIZE} = {SIZE*SIZE} cells\n")
        f.write(f"- Black cells: {black_count}\n")
        f.write(f"- White cells: {white_count}\n")
        f.write(f"- Numbered cells: {len(entries)}\n")
        f.write(f"- Across entries: {sum(1 for e in entries if e['across'])}\n")
        f.write(f"- Down entries: {sum(1 for e in entries if e['down'])}\n\n")

        f.write("## Grid Pattern (# = black, . = white)\n\n```\n")
        f.write("     " + "".join(f"{c%10}" for c in range(SIZE)) + "\n")
        f.write("     " + "-" * SIZE + "\n")
        for r in range(SIZE):
            row_str = f"{r:2d} | "
            for c in range(SIZE):
                row_str += "#" if g[r][c] == BLACK else "."
            f.write(row_str + "\n")
        f.write("```\n\n")

        f.write("## Grid with Entry Numbers\n\n```\n")
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

# Main
print("Solving crossword grid...")
print(f"Across entries: {len(across_set)}, Down entries: {len(down_set)}")
print(f"Both: {len(across_set & down_set)}, Total numbered: {MAX_NUM}")

for X in range(1, 8):
    if solve_for_x(X):
        print("\n" + "="*60)
        print("SOLUTION:")
        print("="*60)
        print_grid(solution_found)
        print()
        ok, entries = verify_solution(solution_found)
        if ok:
            output_file = "/home/user/MB/analysis/CROSSWORD_GRID_DIGITIZED.md"
            save_results(solution_found, entries, output_file)
            print(f"\nResults saved to {output_file}")
        else:
            print("\nWARNING: Verification failed. Saving anyway.")
            output_file = "/home/user/MB/analysis/CROSSWORD_GRID_DIGITIZED.md"
            save_results(solution_found, entries, output_file)
            print(f"Results saved to {output_file}")
        break
else:
    print("\nNO SOLUTION FOUND for any X value (1-7)")
    print("Check constraints or try different assumptions.")
