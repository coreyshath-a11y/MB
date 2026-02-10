#!/usr/bin/env python3
"""
Reconstruct the 21x21 crossword grid using constraint propagation + backtracking.

Instead of image analysis (which keeps failing), we use the known ACROSS and DOWN
entry number lists plus standard crossword numbering rules to mathematically
determine which cells are black vs white.

Key insight: In standard crossword numbering, cells are numbered left-to-right,
top-to-bottom. A cell gets a number if it starts an across word, a down word, or both.
We know EXACTLY which numbers are across, down, or both. This constrains the grid heavily.
"""

import json
import sys
from itertools import product

# Known entry lists
ACROSS = [1,8,14,22,23,24,25,28,29,30,31,32,34,35,36,38,41,42,43,45,47,48,50,54,57,58,59,61,63,64,66,68,70,72,73,77,79,80,81,82,83,85,88,90,91,92,94,97,99,100,102,103,105,106,107,109,111,113,114,117,119,120,121,123,124,127,129,132,134,136,138,141,143,145,147,148,149,153,155,156,158,159,161,164,165,167,171,172,173,174,175,176]
DOWN = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,26,27,33,37,39,40,43,44,46,49,51,52,53,55,56,60,62,65,67,69,71,72,74,75,76,77,78,80,83,84,86,87,89,93,95,96,98,101,104,108,110,112,115,116,117,118,122,124,125,126,128,130,131,133,135,137,139,140,141,142,144,150,151,152,153,154,157,160,162,163,166,168,169,170]

ACROSS_SET = set(ACROSS)
DOWN_SET = set(DOWN)
BOTH_SET = ACROSS_SET & DOWN_SET
ALL_NUMBERS = sorted(ACROSS_SET | DOWN_SET)
MAX_NUM = 176  # highest entry number

# For each number, classify it
NUM_TYPE = {}
for n in range(1, MAX_NUM + 1):
    if n in ALL_NUMBERS:
        is_a = n in ACROSS_SET
        is_d = n in DOWN_SET
        NUM_TYPE[n] = ('A' if is_a and not is_d else
                       'D' if is_d and not is_a else
                       'B')  # Both

SIZE = 21

def number_grid(grid):
    """Apply standard crossword numbering to a grid. Returns (numbering_dict, max_number)."""
    numbering = {}
    num = 1

    for r in range(SIZE):
        for c in range(SIZE):
            if grid[r][c] == 1:  # Black
                continue

            starts_across = False
            starts_down = False

            # Starts across: left edge or left is black, AND right neighbor is white
            if (c == 0 or grid[r][c-1] == 1):
                if c + 1 < SIZE and grid[r][c+1] == 0:
                    starts_across = True

            # Starts down: top edge or above is black, AND below is white
            if (r == 0 or grid[r-1][c] == 1):
                if r + 1 < SIZE and grid[r+1][c] == 0:
                    starts_down = True

            if starts_across or starts_down:
                numbering[num] = (r, c, starts_across, starts_down)
                num += 1

    return numbering, num - 1


def check_grid(grid):
    """Check if a grid matches our known entry lists. Returns (match, details)."""
    numbering, max_num = number_grid(grid)

    if max_num != MAX_NUM:
        return False, f"Wrong number count: {max_num} vs {MAX_NUM}"

    for n in range(1, MAX_NUM + 1):
        if n not in numbering:
            return False, f"Missing number {n}"

        r, c, is_a, is_d = numbering[n]
        expected_a = n in ACROSS_SET
        expected_d = n in DOWN_SET

        if is_a != expected_a or is_d != expected_d:
            return False, f"Number {n}: across={is_a} (expected {expected_a}), down={is_d} (expected {expected_d})"

    return True, "Perfect match!"


def grid_from_image_with_csp(pdf_path):
    """
    Extract grid from high-res PDF image, then use CSP to fix any errors.
    """
    try:
        import fitz
        from PIL import Image
        import numpy as np
    except ImportError:
        print("Missing dependencies for image extraction")
        return None

    doc = fitz.open(pdf_path)
    page = doc[0]

    # Try multiple zoom levels and grid bounds
    best_grid = None
    best_score = -1

    for zoom in [8, 10, 6]:
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        img_data = pix.samples
        w, h = pix.width, pix.height

        # Convert to numpy grayscale
        arr = np.frombuffer(img_data, dtype=np.uint8).reshape(h, w, -1)
        gray = np.mean(arr[:, :, :3], axis=2)

        # Try different grid bound estimates
        # The crossword is roughly in the right-center of the page
        bound_options = [
            (0.365, 0.870, 0.058, 0.715),  # Original estimate
            (0.355, 0.865, 0.055, 0.712),
            (0.370, 0.875, 0.060, 0.718),
            (0.360, 0.868, 0.056, 0.714),
            (0.358, 0.872, 0.057, 0.716),
        ]

        for lf, rf, tf, bf in bound_options:
            left = int(w * lf)
            right = int(w * rf)
            top = int(h * tf)
            bottom = int(h * bf)

            cell_w = (right - left) / SIZE
            cell_h = (bottom - top) / SIZE

            grid = [[0]*SIZE for _ in range(SIZE)]

            for row in range(SIZE):
                for col in range(SIZE):
                    # Sample center 30% of cell to avoid grid lines and numbers
                    cy = int(top + (row + 0.5) * cell_h)
                    cx = int(left + (col + 0.5) * cell_w)

                    # Sample a region
                    r1 = max(0, int(cy - cell_h * 0.15))
                    r2 = min(h, int(cy + cell_h * 0.15))
                    c1 = max(0, int(cx - cell_w * 0.15))
                    c2 = min(w, int(cx + cell_w * 0.15))

                    region = gray[r1:r2, c1:c2]
                    if region.size == 0:
                        continue

                    avg = np.mean(region)

                    # Try different thresholds
                    grid[row][col] = 1 if avg < 100 else 0  # 1=black, 0=white

            # Score this grid
            numbering, max_num = number_grid(grid)

            # Count how many numbers match
            correct = 0
            for n in range(1, min(max_num, MAX_NUM) + 1):
                if n in numbering:
                    r, c, is_a, is_d = numbering[n]
                    expected_a = n in ACROSS_SET
                    expected_d = n in DOWN_SET
                    if is_a == expected_a and is_d == expected_d:
                        correct += 1

            score = correct
            black_count = sum(sum(row) for row in grid)

            if score > best_score:
                best_score = score
                best_grid = [row[:] for row in grid]
                print(f"  zoom={zoom}, bounds=({lf},{rf},{tf},{bf}): "
                      f"max_num={max_num}, correct={correct}/{MAX_NUM}, "
                      f"black={black_count}")

            # Also try with threshold adjustments
            for thresh in [80, 90, 110, 120, 130]:
                test_grid = [[0]*SIZE for _ in range(SIZE)]
                for row in range(SIZE):
                    for col in range(SIZE):
                        cy = int(top + (row + 0.5) * cell_h)
                        cx = int(left + (col + 0.5) * cell_w)
                        r1 = max(0, int(cy - cell_h * 0.15))
                        r2 = min(h, int(cy + cell_h * 0.15))
                        c1 = max(0, int(cx - cell_w * 0.15))
                        c2 = min(w, int(cx + cell_w * 0.15))
                        region = gray[r1:r2, c1:c2]
                        if region.size > 0:
                            test_grid[row][col] = 1 if np.mean(region) < thresh else 0

                numbering, max_num = number_grid(test_grid)
                correct = 0
                for n in range(1, min(max_num, MAX_NUM) + 1):
                    if n in numbering:
                        rr, cc, is_a, is_d = numbering[n]
                        if (is_a == (n in ACROSS_SET)) and (is_d == (n in DOWN_SET)):
                            correct += 1

                if correct > best_score:
                    best_score = correct
                    best_grid = [row[:] for row in test_grid]
                    black_count = sum(sum(row) for row in test_grid)
                    print(f"  zoom={zoom}, thresh={thresh}, bounds=({lf},{rf},{tf},{bf}): "
                          f"correct={correct}/{MAX_NUM}, black={black_count}")

    if best_grid:
        print(f"\nBest extraction: {best_score}/{MAX_NUM} correct")

        # Check if perfect
        match, detail = check_grid(best_grid)
        if match:
            print("PERFECT MATCH!")
            return best_grid
        else:
            print(f"Not perfect: {detail}")
            print("Will attempt CSP repair...")
            return best_grid

    return None


def try_csp_repair(grid):
    """
    Given a grid that's close but not perfect, try flipping individual cells
    to see if we can achieve a perfect match.
    """
    print("\nAttempting CSP repair...")

    # First check current state
    match, detail = check_grid(grid)
    if match:
        return grid

    numbering, max_num = number_grid(grid)

    # Find which numbers are wrong
    wrong_numbers = []
    for n in range(1, min(max_num + 5, MAX_NUM + 5)):
        if n in numbering:
            r, c, is_a, is_d = numbering[n]
            expected_a = n in ACROSS_SET
            expected_d = n in DOWN_SET
            if is_a != expected_a or is_d != expected_d:
                wrong_numbers.append((n, r, c, is_a, is_d, expected_a, expected_d))

    print(f"Current max_num: {max_num}, target: {MAX_NUM}")
    print(f"Wrong numbers: {len(wrong_numbers)}")
    for n, r, c, is_a, is_d, exp_a, exp_d in wrong_numbers[:20]:
        print(f"  #{n} at ({r},{c}): across={is_a}(exp={exp_a}), down={is_d}(exp={exp_d})")

    # Strategy: try flipping each cell and see if score improves
    def score_grid(g):
        num, mx = number_grid(g)
        if mx != MAX_NUM:
            # Penalize wrong total
            penalty = abs(mx - MAX_NUM) * 10
        else:
            penalty = 0
        correct = 0
        for n in range(1, min(mx, MAX_NUM) + 1):
            if n in num:
                r, c, is_a, is_d = num[n]
                if (is_a == (n in ACROSS_SET)) and (is_d == (n in DOWN_SET)):
                    correct += 1
        return correct - penalty

    current_score = score_grid(grid)
    print(f"Starting score: {current_score}")

    improved = True
    iterations = 0
    while improved and iterations < 50:
        improved = False
        iterations += 1

        for r in range(SIZE):
            for c in range(SIZE):
                # Try flipping this cell
                grid[r][c] = 1 - grid[r][c]
                new_score = score_grid(grid)

                if new_score > current_score:
                    current_score = new_score
                    improved = True
                    print(f"  Flip ({r},{c}) -> score {current_score}")

                    match, detail = check_grid(grid)
                    if match:
                        print("FOUND PERFECT GRID!")
                        return grid
                else:
                    # Revert
                    grid[r][c] = 1 - grid[r][c]

        print(f"  Iteration {iterations}: score={current_score}")

    # Try flipping pairs of cells
    print("\nTrying pair flips...")
    for r1 in range(SIZE):
        for c1 in range(SIZE):
            grid[r1][c1] = 1 - grid[r1][c1]
            for r2 in range(r1, SIZE):
                c2_start = c1 + 1 if r2 == r1 else 0
                for c2 in range(c2_start, SIZE):
                    grid[r2][c2] = 1 - grid[r2][c2]
                    new_score = score_grid(grid)

                    if new_score > current_score:
                        current_score = new_score
                        print(f"  Pair flip ({r1},{c1})+({r2},{c2}) -> score {current_score}")

                        match, detail = check_grid(grid)
                        if match:
                            print("FOUND PERFECT GRID!")
                            return grid

                        # Keep this flip and continue
                        grid[r1][c1] = 1 - grid[r1][c1]  # Will be re-flipped in outer loop
                        break
                    else:
                        grid[r2][c2] = 1 - grid[r2][c2]
                else:
                    continue
                break
            else:
                grid[r1][c1] = 1 - grid[r1][c1]  # Revert outer flip
                continue
            break

    print(f"Final score after repair: {current_score}")
    return grid


def print_grid(grid):
    """Print grid visually."""
    for r, row in enumerate(grid):
        line = f"{r:2d} "
        for cell in row:
            line += "██" if cell == 1 else "░░"
        print(line)


def save_results(grid, output_path):
    """Save grid and computed data."""
    numbering, max_num = number_grid(grid)

    # Compute entry lengths
    across_lengths = {}
    down_lengths = {}
    entries = {}

    for num, (r, c, is_a, is_d) in numbering.items():
        if is_a:
            length = 0
            cc = c
            while cc < SIZE and grid[r][cc] == 0:
                length += 1
                cc += 1
            across_lengths[num] = length
            entries[f"{num}A"] = {
                'cells': [(r, c+i) for i in range(length)],
                'length': length,
                'start': [r, c]
            }

        if is_d:
            length = 0
            rr = r
            while rr < SIZE and grid[rr][c] == 0:
                length += 1
                rr += 1
            down_lengths[num] = length
            entries[f"{num}D"] = {
                'cells': [(r+i, c) for i in range(length)],
                'length': length,
                'start': [r, c]
            }

    match, detail = check_grid(grid)

    results = {
        'grid': grid,
        'valid': match,
        'detail': detail,
        'max_num': max_num,
        'black_cells': sum(sum(row) for row in grid),
        'white_cells': SIZE*SIZE - sum(sum(row) for row in grid),
        'numbering': {str(k): {'row': v[0], 'col': v[1], 'across': v[2], 'down': v[3]}
                     for k, v in numbering.items()},
        'across_lengths': {str(k): v for k, v in across_lengths.items()},
        'down_lengths': {str(k): v for k, v in down_lengths.items()},
        'entries': entries,
    }

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Saved to {output_path}")
    print(f"Valid: {match} - {detail}")
    print(f"Black cells: {results['black_cells']}, White cells: {results['white_cells']}")

    # Print some key entry lengths
    key_entries = ['167A', '149A', '1A', '1D']
    for key in key_entries:
        if key in entries:
            print(f"  {key}: length {entries[key]['length']}")

    return results


def main():
    pdf_path = "/home/user/MB/puzzles/Million-Dollar-Crossword.pdf"
    output_path = "/home/user/MB/analysis/grid_reconstructed.json"

    print("="*60)
    print("CROSSWORD GRID RECONSTRUCTION")
    print("="*60)

    # Step 1: Extract from image with multiple parameter sweeps
    print("\nStep 1: Image extraction with parameter sweep...")
    grid = grid_from_image_with_csp(pdf_path)

    if grid is None:
        print("Image extraction failed completely.")
        return

    print("\nExtracted grid:")
    print_grid(grid)

    # Step 2: Check if it's valid
    match, detail = check_grid(grid)
    print(f"\nValidation: {detail}")

    if not match:
        # Step 3: CSP repair
        grid = try_csp_repair(grid)

    # Step 4: Save results
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)

    print_grid(grid)
    results = save_results(grid, output_path)

    return grid, results


if __name__ == '__main__':
    main()
