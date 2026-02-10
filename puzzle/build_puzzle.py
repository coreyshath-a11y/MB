#!/usr/bin/env python3
"""
Build the authoritative 25x25 puzzle.json from user-provided entry metadata.
Reconstructs the grid from across/down start positions and lengths.

NOTE: The across entry list is truncated after #107 (55 of 92 entries).
Missing across entries: 109,111,113,114,117,119,120,121,123,124,127,129,
132,134,136,138,141,143,145,147,148,149,153,155,156,158,159,161,164,165,
167,171,172,173,174,175,176
Missing down entry: 153
"""
import json

GRID_SIZE = 25

# Column mapping: A=0, B=1, ..., Y=24
COL_MAP = {chr(65+i): i for i in range(25)}

def parse_cell(cell_str):
    """Parse cell reference like 'A1' -> (row_idx, col_idx)"""
    col_letter = cell_str[0]
    row_num = int(cell_str[1:])
    return (row_num - 1, COL_MAP[col_letter])

def cell_ref(row, col):
    """Convert (row_idx, col_idx) -> 'A1' style reference"""
    return f"{chr(65+col)}{row+1}"

# ============================================================
# ACROSS ENTRIES: (number, start_cell, length)
# 55 of 92 entries provided (truncated after #107)
# ============================================================
ACROSS = [
    (1,   "A1",  7),
    (8,   "A2",  7),
    (14,  "A3",  16),
    (22,  "A4",  4),
    (23,  "F4",  3),
    (24,  "J4",  1),
    (25,  "L4",  2),
    (28,  "A5",  4),
    (29,  "H5",  3),
    (30,  "L5",  7),
    (31,  "A6",  4),
    (32,  "F6",  3),
    (34,  "J6",  3),
    (35,  "A7",  16),
    (36,  "A8",  7),
    (38,  "I8",  3),
    (41,  "A9",  3),
    (42,  "E9",  4),
    (43,  "J9",  4),
    (45,  "A10", 3),
    (47,  "D10", 5),
    (48,  "K10", 15),
    (50,  "B11", 3),
    (54,  "F11", 3),
    (57,  "A12", 2),
    (58,  "D12", 2),
    (59,  "F12", 4),
    (61,  "J12", 4),
    (63,  "A13", 6),
    (64,  "H13", 10),
    (66,  "A14", 2),
    (68,  "E14", 3),
    (70,  "I14", 4),
    (72,  "A15", 3),
    (73,  "E15", 3),
    (77,  "A16", 14),
    (79,  "A17", 4),
    (80,  "F17", 4),
    (81,  "L17", 6),
    (82,  "A18", 2),
    (83,  "C18", 4),
    (85,  "I18", 3),
    (88,  "A19", 7),
    (90,  "J19", 16),
    (91,  "A20", 5),
    (92,  "H20", 3),
    (94,  "L20", 4),
    (97,  "A21", 2),
    (99,  "C21", 3),
    (100, "A22", 4),
    (102, "I22", 2),
    (103, "L22", 3),
    (105, "A23", 8),
    (106, "A24", 8),
    (107, "A25", 8),
]

# Known across entry NUMBERS that are missing start/length data
MISSING_ACROSS_NUMS = [109,111,113,114,117,119,120,121,123,124,127,129,
    132,134,136,138,141,143,145,147,148,149,153,155,156,158,159,161,164,
    165,167,171,172,173,174,175,176]

# ============================================================
# DOWN ENTRIES: (number, start_cell, length)
# 95 of 96 entries (missing #153)
# ============================================================
DOWN = [
    (1,   "A1",  9),
    (2,   "B1",  12),
    (3,   "C1",  9),
    (4,   "D1",  8),
    (5,   "E1",  2),
    (6,   "F1",  8),
    (7,   "G1",  7),
    (8,   "I1",  2),
    (9,   "J1",  7),
    (10,  "K1",  9),
    (11,  "L1",  8),
    (12,  "M1",  2),
    (13,  "N1",  7),
    (14,  "O1",  2),
    (15,  "R1",  8),
    (16,  "S1",  9),
    (17,  "T1",  7),
    (18,  "U1",  9),
    (19,  "V1",  9),
    (20,  "W1",  8),
    (21,  "X1",  9),
    (23,  "A2",  7),
    (26,  "E3",  4),
    (27,  "H3",  6),
    (33,  "M4",  7),
    (37,  "G5",  5),
    (39,  "Q5",  6),
    (40,  "Y5",  5),
    (43,  "A6",  4),
    (44,  "B6",  7),
    (46,  "D6",  4),
    (49,  "I6",  4),
    (51,  "L6",  4),
    (52,  "M6",  3),
    (53,  "O6",  4),
    (55,  "S6",  5),
    (56,  "T6",  4),
    (60,  "W6",  3),
    (62,  "Y6",  3),
    (65,  "H7",  5),
    (67,  "K7",  5),
    (69,  "N7",  5),
    (71,  "R7",  5),
    (72,  "A8",  3),
    (74,  "C9",  4),
    (75,  "D9",  3),
    (76,  "E9",  3),
    (77,  "F9",  4),
    (78,  "G9",  4),
    (80,  "J10", 5),
    (83,  "M10", 4),
    (84,  "N10", 5),
    (86,  "P10", 4),
    (87,  "Q10", 5),
    (89,  "T10", 4),
    (93,  "X10", 5),
    (95,  "C11", 4),
    (96,  "D11", 4),
    (98,  "F11", 4),
    (101, "J12", 4),
    (104, "M12", 4),
    (108, "R12", 4),
    (110, "T12", 4),
    (112, "V12", 4),
    (115, "Y12", 4),
    (116, "B13", 4),
    (117, "C13", 4),
    (118, "D13", 4),
    (122, "H14", 4),
    (124, "J14", 4),
    (125, "K14", 4),
    (126, "L14", 4),
    (128, "N14", 4),
    (130, "A15", 4),
    (131, "B15", 4),
    (132, "C15", 4),  # Note: was missing, inferred from pattern
    (133, "D15", 4),
    (135, "F15", 4),
    (137, "H15", 4),
    (139, "J15", 4),
    (140, "K15", 4),
    (141, "L15", 4),
    (142, "M15", 4),
    (144, "O15", 4),
    (150, "E17", 4),
    (151, "F17", 4),
    (152, "G17", 4),
    (154, "I17", 4),
    (157, "L17", 4),
    (160, "O17", 4),
    (162, "Q17", 4),
    (163, "R17", 4),
    (166, "U17", 4),
    (168, "W17", 4),
    (169, "X17", 4),
    (170, "Y17", 4),
]

# All entry numbers that should exist (from old analysis)
ALL_ACROSS_NUMS = sorted(set(n for n,_,_ in ACROSS) | set(MISSING_ACROSS_NUMS))
# = [1,8,14,22,23,24,25,28,29,30,31,32,34,35,36,38,41,42,43,45,47,48,50,54,
#    57,58,59,61,63,64,66,68,70,72,73,77,79,80,81,82,83,85,88,90,91,92,94,97,
#    99,100,102,103,105,106,107,109,111,113,114,117,119,120,121,123,124,127,129,
#    132,134,136,138,141,143,145,147,148,149,153,155,156,158,159,161,164,165,167,
#    171,172,173,174,175,176]

# Known circled cells (from user's explicit row data)
CIRCLED_CELLS = ["M1", "E3", "U25"]

def build_grid():
    """Reconstruct the 25x25 grid from entry metadata.
    Cells covered by entries = white(0), everything else = black(1).
    NOTE: Grid will be incomplete in the bottom-right due to missing across entries.
    """
    grid = [[1]*GRID_SIZE for _ in range(GRID_SIZE)]

    for num, start, length in ACROSS:
        row, col = parse_cell(start)
        for c in range(col, col + length):
            if 0 <= c < GRID_SIZE:
                grid[row][c] = 0

    for num, start, length in DOWN:
        row, col = parse_cell(start)
        for r in range(row, row + length):
            if 0 <= r < GRID_SIZE:
                grid[r][col] = 0

    for cell_str in CIRCLED_CELLS:
        row, col = parse_cell(cell_str)
        grid[row][col] = 2

    return grid

def compute_numbering(grid):
    """Compute standard crossword numbering."""
    numbering = {}
    num = 1
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 1:
                continue
            starts_across = False
            starts_down = False
            if (c == 0 or grid[r][c-1] == 1):
                if c + 1 < GRID_SIZE and grid[r][c+1] != 1:
                    starts_across = True
            if (r == 0 or grid[r-1][c] == 1):
                if r + 1 < GRID_SIZE and grid[r+1][c] != 1:
                    starts_down = True
            if starts_across or starts_down:
                numbering[num] = {
                    "row": r, "col": c, "cell": cell_ref(r, c),
                    "across": starts_across, "down": starts_down,
                }
                num += 1
    return numbering

def compute_entry_cells(grid):
    """Compute cell lists for each entry."""
    entries = {"across": {}, "down": {}}
    for num, start, length in ACROSS:
        row, col = parse_cell(start)
        cells = [cell_ref(row, col + i) for i in range(length)]
        entries["across"][num] = {"number": num, "start": start, "length": length, "cells": cells}
    for num, start, length in DOWN:
        row, col = parse_cell(start)
        cells = [cell_ref(row + i, col) for i in range(length)]
        entries["down"][num] = {"number": num, "start": start, "length": length, "cells": cells}
    return entries

def print_grid(grid, file=None):
    """Print ASCII grid."""
    import sys
    out = file or sys.stdout
    out.write("   " + " ".join(chr(65+c) for c in range(GRID_SIZE)) + "\n")
    for r in range(GRID_SIZE):
        row_str = f"{r+1:2d} "
        for c in range(GRID_SIZE):
            v = grid[r][c]
            if v == 1:   row_str += "# "
            elif v == 2: row_str += "O "
            else:        row_str += ". "
        out.write(row_str + "\n")

def validate(grid, numbering):
    """Validate entries against computed numbering."""
    errors = []
    warnings = []

    # Build a reverse lookup: (row, col) -> computed number
    pos_to_num = {}
    for num, info in numbering.items():
        pos_to_num[(info["row"], info["col"])] = num

    for num, start, length in ACROSS:
        row, col = parse_cell(start)
        if (row, col) not in pos_to_num:
            errors.append(f"ACROSS #{num} at {start}: no numbered cell at this position")
        else:
            computed_num = pos_to_num[(row, col)]
            if computed_num != num:
                warnings.append(f"ACROSS #{num} at {start}: computed as #{computed_num}")

    for num, start, length in DOWN:
        row, col = parse_cell(start)
        if (row, col) not in pos_to_num:
            errors.append(f"DOWN #{num} at {start}: no numbered cell at this position")
        else:
            computed_num = pos_to_num[(row, col)]
            if computed_num != num:
                warnings.append(f"DOWN #{num} at {start}: computed as #{computed_num}")

    return errors, warnings

def main():
    print("=" * 60)
    print("Building 25x25 Crossword Puzzle")
    print("=" * 60)

    grid = build_grid()

    black_count = sum(1 for r in grid for c in r if c == 1)
    white_count = sum(1 for r in grid for c in r if c == 0)
    circled_count = sum(1 for r in grid for c in r if c == 2)

    print(f"\nGrid: {GRID_SIZE}x{GRID_SIZE} = {GRID_SIZE*GRID_SIZE} cells")
    print(f"  Black:   {black_count}")
    print(f"  White:   {white_count}")
    print(f"  Circled: {circled_count}")
    print(f"  Fillable: {white_count + circled_count}")

    print(f"\nProvided entries:")
    print(f"  Across: {len(ACROSS)} of 92 (missing {len(MISSING_ACROSS_NUMS)} after #107)")
    print(f"  Down:   {len(DOWN)} of 96 (missing #153)")

    print("\nASCII Grid (NOTE: bottom-right incomplete due to missing across entries):")
    print_grid(grid)

    numbering = compute_numbering(grid)
    max_num = max(numbering.keys()) if numbering else 0
    print(f"\nComputed numbering: {len(numbering)} cells, max #{max_num}")

    errors, warnings = validate(grid, numbering)
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors[:10]:
            print(f"  {e}")
        if len(errors) > 10:
            print(f"  ... and {len(errors)-10} more")
    if warnings:
        print(f"\nNumber mismatches ({len(warnings)}):")
        for w in warnings[:10]:
            print(f"  {w}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings)-10} more")
    if not errors and not warnings:
        print("\n*** ALL VALIDATIONS PASSED ***")

    entry_cells = compute_entry_cells(grid)
    across_nums = set(n for n,_,_ in ACROSS)
    down_nums = set(n for n,_,_ in DOWN)
    both_nums = across_nums & down_nums

    puzzle = {
        "grid_size": GRID_SIZE,
        "grid": grid,
        "cell_types": {"0": "empty/fillable", "1": "black", "2": "circled"},
        "entries": entry_cells,
        "missing_across": MISSING_ACROSS_NUMS,
        "missing_down": [153],
        "stats": {
            "black_cells": black_count,
            "white_cells": white_count,
            "circled_cells": circled_count,
            "provided_across": len(ACROSS),
            "provided_down": len(DOWN),
            "total_across": 92,
            "total_down": 96,
            "both_entries": sorted(both_nums),
        },
        "coordinate_system": {
            "columns": "A-Y (left to right, A=0, Y=24)",
            "rows": "1-25 (top to bottom, 1=0, 25=24)",
            "example": "A1 = top-left, Y25 = bottom-right",
        },
    }

    out_path = "/home/user/MB/puzzle/puzzle.json"
    with open(out_path, "w") as f:
        json.dump(puzzle, f, indent=2)
    print(f"\nSaved to {out_path}")

    # Save compact grid text
    txt_path = "/home/user/MB/puzzle/grid.txt"
    with open(txt_path, "w") as f:
        f.write("# 25x25 Crossword Grid (PARTIAL - missing 37 across entries)\n")
        f.write("# 0=empty, 1=black, 2=circled\n")
        f.write("# Columns: A-Y, Rows: 1-25\n\n")
        print_grid(grid, f)
    print(f"Saved grid text to {txt_path}")

    return puzzle

if __name__ == "__main__":
    main()
