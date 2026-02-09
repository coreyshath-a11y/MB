#!/usr/bin/env python3
"""
Solve 9x9 Sudoku variant using letters L,I,F,E,C,H,A,N,G instead of 1-9.
This is one of the known puzzle types from the MrBeast x Salesforce puzzle.
"""
import sys

# Letter-to-number mapping: L=1, I=2, F=3, E=4, C=5, H=6, A=7, N=8, G=9
LETTER_ORDER = "LIFECHANG"
LETTER_MAP = {c: i + 1 for i, c in enumerate(LETTER_ORDER)}
NUM_MAP = {i + 1: c for i, c in enumerate(LETTER_ORDER)}


def parse_grid(text):
    """Parse grid from text. Use . or _ for empty cells."""
    grid = []
    for line in text.strip().split("\n"):
        row = []
        for ch in line.strip().split():
            if ch in (".", "_", "0"):
                row.append(0)
            elif ch.upper() in LETTER_MAP:
                row.append(LETTER_MAP[ch.upper()])
            elif ch.isdigit():
                row.append(int(ch))
        if len(row) == 9:
            grid.append(row)
    return grid


def is_valid(grid, row, col, num):
    """Check if placing num at (row, col) is valid."""
    if num in grid[row]:
        return False
    if num in [grid[r][col] for r in range(9)]:
        return False
    r0, c0 = 3 * (row // 3), 3 * (col // 3)
    for r in range(r0, r0 + 3):
        for c in range(c0, c0 + 3):
            if grid[r][c] == num:
                return False
    return True


def solve(grid):
    """Solve the grid using backtracking."""
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                for num in range(1, 10):
                    if is_valid(grid, r, c, num):
                        grid[r][c] = num
                        if solve(grid):
                            return True
                        grid[r][c] = 0
                return False
    return True


def print_grid(grid):
    """Print grid with letter labels."""
    for row in grid:
        print(" ".join(NUM_MAP.get(n, ".") for n in row))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            grid = parse_grid(f.read())
    else:
        print("Usage: python solve_lifechange.py puzzle.txt")
        print("Format: 9 rows, space-separated letters (L I F E C H A N G) or . for empty")
        print(f"Letter mapping: {', '.join(f'{c}={i+1}' for i, c in enumerate(LETTER_ORDER))}")
        sys.exit(1)

    print("Input grid:")
    print_grid(grid)
    print("\nSolving...")
    if solve(grid):
        print("\nSolved!")
        print_grid(grid)
    else:
        print("No solution found — check the input grid for errors.")
