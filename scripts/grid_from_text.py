#!/usr/bin/env python3
"""
Extract the crossword grid by finding the TEXT numbers in the PDF.
Each numbered cell has a small number printed in it. By extracting text
positions, we can determine:
1. Where each numbered cell is located
2. The grid boundaries
3. Which cells are black vs white

This avoids all the image analysis problems.
"""

import json
import sys

try:
    import fitz
except ImportError:
    print("Need PyMuPDF: pip install PyMuPDF")
    sys.exit(1)

ACROSS = [1,8,14,22,23,24,25,28,29,30,31,32,34,35,36,38,41,42,43,45,47,48,50,54,57,58,59,61,63,64,66,68,70,72,73,77,79,80,81,82,83,85,88,90,91,92,94,97,99,100,102,103,105,106,107,109,111,113,114,117,119,120,121,123,124,127,129,132,134,136,138,141,143,145,147,148,149,153,155,156,158,159,161,164,165,167,171,172,173,174,175,176]
DOWN = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,26,27,33,37,39,40,43,44,46,49,51,52,53,55,56,60,62,65,67,69,71,72,74,75,76,77,78,80,83,84,86,87,89,93,95,96,98,101,104,108,110,112,115,116,117,118,122,124,125,126,128,130,131,133,135,137,139,140,141,142,144,150,151,152,153,154,157,160,162,163,166,168,169,170]
ACROSS_SET = set(ACROSS)
DOWN_SET = set(DOWN)
SIZE = 21

def extract_text_positions(pdf_path):
    """Extract all text and positions from the PDF."""
    doc = fitz.open(pdf_path)
    page = doc[0]

    # Get text with positions
    blocks = page.get_text("dict")["blocks"]

    text_items = []
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"].strip()
                bbox = span["bbox"]  # (x0, y0, x1, y1)
                font_size = span["size"]
                text_items.append({
                    'text': text,
                    'bbox': bbox,
                    'x': bbox[0],
                    'y': bbox[1],
                    'size': font_size
                })

    return text_items


def find_grid_numbers(text_items):
    """Find the small numbers that label crossword cells."""
    # Cell numbers are small text (typically 5-8pt) that are pure integers 1-176
    number_items = []

    for item in text_items:
        text = item['text']
        try:
            num = int(text)
            if 1 <= num <= 176:
                number_items.append({
                    'num': num,
                    'x': item['x'],
                    'y': item['y'],
                    'bbox': item['bbox'],
                    'size': item['size']
                })
        except ValueError:
            continue

    # Sort by number
    number_items.sort(key=lambda x: x['num'])

    print(f"Found {len(number_items)} potential cell numbers")

    if number_items:
        # Show size distribution
        sizes = set(round(n['size'], 1) for n in number_items)
        print(f"Font sizes: {sorted(sizes)}")

        # Filter to the most common small size (cell numbers are small)
        size_counts = {}
        for n in number_items:
            s = round(n['size'], 1)
            size_counts[s] = size_counts.get(s, 0) + 1
        print(f"Size distribution: {size_counts}")

        # Cell numbers should be the smallest text that has many instances
        # They should also form a dense cluster in position space
        # Filter to most likely cell number size
        if len(sizes) > 1:
            # Try each size and see which gives us closest to 176 numbers
            for target_size in sorted(sizes):
                filtered = [n for n in number_items if round(n['size'], 1) == target_size]
                nums_found = set(n['num'] for n in filtered)
                print(f"  Size {target_size}: {len(filtered)} items, {len(nums_found)} unique numbers, "
                      f"range {min(nums_found)}-{max(nums_found)}")

    return number_items


def numbers_to_grid(number_items, target_size=None):
    """Convert number positions to a 21x21 grid."""
    # Filter to target size if specified
    if target_size is not None:
        number_items = [n for n in number_items if round(n['size'], 1) == target_size]

    # Remove duplicate numbers (keep first occurrence)
    seen = set()
    unique = []
    for n in number_items:
        if n['num'] not in seen:
            seen.add(n['num'])
            unique.append(n)
    number_items = unique

    if not number_items:
        return None

    # Find grid bounds from number positions
    xs = [n['x'] for n in number_items]
    ys = [n['y'] for n in number_items]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    print(f"\nNumber positions span: x=[{min_x:.1f}, {max_x:.1f}], y=[{min_y:.1f}, {max_y:.1f}]")

    # Numbers are in the top-left corner of each cell
    # The grid extends slightly beyond the max number positions
    # Estimate cell size from the spacing of first-row numbers

    # Numbers 1-21 should mostly be in the first row (if first row is all white)
    first_row_nums = [n for n in number_items if 1 <= n['num'] <= 21]
    first_row_xs = sorted(set(round(n['x'], 1) for n in first_row_nums))

    if len(first_row_xs) >= 2:
        # Calculate typical cell width from consecutive numbers
        diffs = [first_row_xs[i+1] - first_row_xs[i] for i in range(len(first_row_xs)-1)]
        # Filter out large gaps (black cells between numbers)
        small_diffs = [d for d in diffs if d < max(diffs) * 0.7] if len(diffs) > 3 else diffs
        if small_diffs:
            cell_width = min(small_diffs)  # Smallest gap = one cell width
        else:
            cell_width = diffs[0]
        print(f"Estimated cell width: {cell_width:.2f}")
        print(f"First row x positions: {first_row_xs}")
        print(f"X diffs: {[f'{d:.2f}' for d in diffs]}")
    else:
        cell_width = (max_x - min_x) / 20
        print(f"Fallback cell width: {cell_width:.2f}")

    # Similarly for cell height - look at numbers in first column
    # Numbers that are at similar x positions but different y positions
    first_col_candidates = sorted(number_items, key=lambda n: n['y'])
    # Group by similar x position
    x_groups = {}
    for n in first_col_candidates:
        x_rounded = round(n['x'] / (cell_width * 0.5)) * (cell_width * 0.5)
        if x_rounded not in x_groups:
            x_groups[x_rounded] = []
        x_groups[x_rounded].append(n)

    # Find the leftmost group with multiple entries
    leftmost_groups = sorted(x_groups.items())
    cell_height = cell_width  # Default: square cells

    for x_pos, group in leftmost_groups:
        if len(group) >= 3:
            group_ys = sorted(n['y'] for n in group)
            y_diffs = [group_ys[i+1] - group_ys[i] for i in range(len(group_ys)-1)]
            small_y_diffs = [d for d in y_diffs if d < max(y_diffs) * 0.7] if len(y_diffs) > 3 else y_diffs
            if small_y_diffs:
                cell_height = min(small_y_diffs)
                print(f"Estimated cell height: {cell_height:.2f} (from x≈{x_pos:.1f} column)")
            break

    print(f"Cell size: {cell_width:.2f} x {cell_height:.2f}")

    # Now map each number to its grid position
    # The top-left of the grid is at approximately (min_x, min_y)
    # Numbers are in the top-left of their cell, so:
    grid_origin_x = min_x - cell_width * 0.05  # Small offset since number is near left edge
    grid_origin_y = min_y - cell_height * 0.05

    number_positions = {}
    for n in number_items:
        col = round((n['x'] - grid_origin_x) / cell_width)
        row = round((n['y'] - grid_origin_y) / cell_height)

        if 0 <= row < SIZE and 0 <= col < SIZE:
            number_positions[n['num']] = (row, col)

    print(f"\nMapped {len(number_positions)} numbers to grid positions")

    # Check if numbering order is correct (left-to-right, top-to-bottom)
    positions_list = sorted(number_positions.items())
    order_ok = True
    for i in range(len(positions_list) - 1):
        n1, (r1, c1) = positions_list[i]
        n2, (r2, c2) = positions_list[i+1]
        if (r2, c2) <= (r1, c1):
            if abs(n2 - n1) == 1:  # Only flag consecutive misordering
                order_ok = False
                print(f"  Order issue: #{n1} at ({r1},{c1}) before #{n2} at ({r2},{c2})")

    # Now reconstruct the grid
    # A cell is BLACK if no number maps to it AND no numbered entry passes through it
    # First, place all numbered cells
    grid = [[None]*SIZE for _ in range(SIZE)]

    for num, (row, col) in number_positions.items():
        grid[row][col] = 0  # White (numbered)

        is_across = num in ACROSS_SET
        is_down = num in DOWN_SET

        # Mark cells to the right (across entry)
        if is_across:
            # We don't know the length yet, but we know cells exist
            # For now just mark the numbered cell
            pass

        # Mark cells below (down entry)
        if is_down:
            pass

    # Use constraints to fill in the rest
    # Key constraint: if num N starts an across entry, cells to its right
    # must be white until we hit a black cell or edge.
    # We don't know lengths, but we know the NEXT numbered cell's position.

    # Better approach: determine black cells by looking at gaps
    # In standard numbering, black cells are cells that:
    # 1. No number maps to them
    # 2. They can't be reached by extending any across or down entry

    # Actually, let's use the positions to determine which cells MUST be white:
    # Any cell that a numbered entry passes through is white.
    # We can figure out entry extents by looking at where entries start and
    # where the next entry in the same row/column starts.

    # For each row, determine the across entry boundaries
    for row in range(SIZE):
        # Get all numbered cells in this row, sorted by column
        row_nums = [(num, col) for num, (r, c) in number_positions.items() if r == row
                     for col in [c]]
        row_nums.sort(key=lambda x: x[1])

        # For each across-starting number, extend right until we hit:
        # - Another number that starts an across entry (meaning there's a black cell between)
        # - The edge
        # But we also need to know where black cells are...

    # Simpler approach: just determine the grid from the pattern of numbered cells
    # Any row/col position that has a number is white
    # Use symmetry: most crosswords have 180° rotational symmetry
    for num, (row, col) in number_positions.items():
        grid[row][col] = 0
        # Symmetric cell
        sym_r = SIZE - 1 - row
        sym_c = SIZE - 1 - col
        if grid[sym_r][sym_c] is None:
            # If symmetric cell isn't numbered, it's also white
            # (this isn't always true - sometimes symmetric cell is also numbered)
            grid[sym_r][sym_c] = 0

    # Fill remaining None cells: they're likely black
    for r in range(SIZE):
        for c in range(SIZE):
            if grid[r][c] is None:
                grid[r][c] = 1  # Black

    # But this is too aggressive. Let's also mark cells that are between
    # two numbered cells in the same row/column as white.
    for row in range(SIZE):
        row_positions = sorted([(col, num) for num, (r, col) in number_positions.items() if r == row])
        for i in range(len(row_positions) - 1):
            c1, n1 = row_positions[i]
            c2, n2 = row_positions[i+1]
            # If n1 starts an across entry and the cells between are not numbered,
            # they should be white (part of n1's across entry)
            if n1 in ACROSS_SET and c2 - c1 <= 20:  # Reasonable entry length
                # Check if there should be a black cell between
                # If n2 also starts an across entry, there might be a black cell before n2
                # If n2 is down-only, it's within n1's across entry
                if n2 not in ACROSS_SET:
                    # n2 is within n1's across span - fill between as white
                    for cc in range(c1, c2 + 1):
                        grid[row][cc] = 0
                elif c2 - c1 == 1:
                    # Adjacent cells, both across-starting - impossible unless c1 is 1-letter
                    # across. In standard crosswords, across entries are at least 2 letters.
                    # So there must be a black cell between... but they're adjacent.
                    # This means c2 starts a new across, so c1's entry goes left from c1.
                    pass

    for col in range(SIZE):
        col_positions = sorted([(row, num) for num, (r, c) in number_positions.items() if c == col])
        for i in range(len(col_positions) - 1):
            r1, n1 = col_positions[i]
            r2, n2 = col_positions[i+1]
            if n1 in DOWN_SET and r2 - r1 <= 20:
                if n2 not in DOWN_SET:
                    for rr in range(r1, r2 + 1):
                        grid[rr][col] = 0

    return grid, number_positions, cell_width, cell_height


def refine_grid(grid, number_positions):
    """Iteratively refine the grid using crossword constraints."""
    # Apply numbering and check
    from scripts.grid_csp_reconstruct import number_grid, check_grid, ACROSS_SET, DOWN_SET, SIZE

    # Try the current grid
    numbering, max_num = number_grid(grid)
    match, detail = check_grid(grid)
    print(f"\nInitial: max_num={max_num}, match={match}")

    if match:
        return grid

    # Score function
    def score(g):
        num, mx = number_grid(g)
        if mx != 176:
            return -abs(mx - 176) * 10
        correct = sum(1 for n in range(1, 177)
                      if n in num and
                      (num[n][2] == (n in ACROSS_SET)) and
                      (num[n][3] == (n in DOWN_SET)))
        return correct

    best_score = score(grid)
    print(f"Initial score: {best_score}")

    # Hill climbing
    improved = True
    while improved:
        improved = False
        for r in range(SIZE):
            for c in range(SIZE):
                grid[r][c] = 1 - grid[r][c]
                s = score(grid)
                if s > best_score:
                    best_score = s
                    improved = True
                    match, detail = check_grid(grid)
                    if match:
                        print(f"FOUND PERFECT GRID! Score: {best_score}")
                        return grid
                else:
                    grid[r][c] = 1 - grid[r][c]

        print(f"  Score: {best_score}")

    return grid


def main():
    pdf_path = "/home/user/MB/puzzles/Million-Dollar-Crossword.pdf"

    print("="*60)
    print("GRID RECONSTRUCTION FROM PDF TEXT EXTRACTION")
    print("="*60)

    # Step 1: Extract text
    text_items = extract_text_positions(pdf_path)
    print(f"Total text items: {len(text_items)}")

    # Show all text items for debugging
    print("\nAll text items (sorted by position):")
    for item in sorted(text_items, key=lambda x: (x['y'], x['x'])):
        print(f"  ({item['x']:.1f}, {item['y']:.1f}) size={item['size']:.1f}: '{item['text']}'")

    # Step 2: Find cell numbers
    print("\n" + "="*60)
    number_items = find_grid_numbers(text_items)

    if not number_items:
        print("No cell numbers found!")
        return

    # Show found numbers
    found_nums = sorted(set(n['num'] for n in number_items))
    missing_nums = sorted(set(range(1, 177)) - set(found_nums))
    print(f"\nFound numbers: {found_nums[:20]}...{found_nums[-10:]}")
    print(f"Missing from 1-176: {missing_nums[:30]}")

    # Step 3: Convert to grid
    # Try with the size that gives most coverage
    sizes = sorted(set(round(n['size'], 1) for n in number_items))

    for target_size in sizes:
        filtered = [n for n in number_items if round(n['size'], 1) == target_size]
        nums = set(n['num'] for n in filtered)
        if len(nums) > 100:  # Need substantial coverage
            print(f"\nTrying size {target_size} ({len(nums)} unique numbers)...")
            result = numbers_to_grid(filtered, target_size)
            if result:
                grid, positions, cw, ch = result
                print("\nGrid:")
                for r, row in enumerate(grid):
                    line = f"{r:2d} "
                    for cell in row:
                        line += "██" if cell == 1 else "░░"
                    print(line)

                black = sum(sum(row) for row in grid)
                print(f"Black: {black}, White: {SIZE*SIZE - black}")

    # Also try with ALL numbers regardless of size
    print(f"\nTrying with ALL numbers...")
    result = numbers_to_grid(number_items)
    if result:
        grid, positions, cw, ch = result
        print("\nGrid:")
        for r, row in enumerate(grid):
            line = f"{r:2d} "
            for cell in row:
                line += "██" if cell == 1 else "░░"
            print(line)

        black = sum(sum(row) for row in grid)
        print(f"Black: {black}, White: {SIZE*SIZE - black}")

        # Save number positions
        output = {
            'number_positions': {str(k): list(v) for k, v in positions.items()},
            'cell_width': cw,
            'cell_height': ch,
            'grid': grid,
        }
        with open('/home/user/MB/analysis/grid_numbers.json', 'w') as f:
            json.dump(output, f, indent=2)
        print("Saved to analysis/grid_numbers.json")


if __name__ == '__main__':
    main()
