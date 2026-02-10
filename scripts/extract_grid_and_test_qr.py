#!/usr/bin/env python3
"""
Extract the crossword grid properly and test QR code overlay theories.

Strategy:
1. Extract from the PDF at high resolution using PyMuPDF
2. Use adaptive thresholding to find grid lines
3. Sample cell centers for black/white
4. Validate against known ACROSS/DOWN entry lists
5. Test QR code theories with the validated grid
"""

import json
import numpy as np
from PIL import Image, ImageDraw
import sys
import os

# Known entry lists from the puzzle
ACROSS = [1,8,14,22,23,24,25,28,29,30,31,32,34,35,36,38,41,42,43,45,47,48,50,54,57,58,59,61,63,64,66,68,70,72,73,77,79,80,81,82,83,85,88,90,91,92,94,97,99,100,102,103,105,106,107,109,111,113,114,117,119,120,121,123,124,127,129,132,134,136,138,141,143,145,147,148,149,153,155,156,158,159,161,164,165,167,171,172,173,174,175,176]
DOWN = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,26,27,33,37,39,40,43,44,46,49,51,52,53,55,56,60,62,65,67,69,71,72,74,75,76,77,78,80,83,84,86,87,89,93,95,96,98,101,104,108,110,112,115,116,117,118,122,124,125,126,128,130,131,133,135,137,139,140,141,142,144,150,151,152,153,154,157,160,162,163,166,168,169,170]

ACROSS_SET = set(ACROSS)
DOWN_SET = set(DOWN)
ALL_NUMBERS = sorted(ACROSS_SET | DOWN_SET)
MAX_NUM = max(ALL_NUMBERS)  # 176

def extract_from_pdf():
    """Extract grid image from PDF at high resolution."""
    try:
        import fitz
    except ImportError:
        print("No PyMuPDF, trying PNG directly")
        return None

    pdf_path = "/home/user/MB/puzzles/Million-Dollar-Crossword.pdf"
    doc = fitz.open(pdf_path)
    page = doc[0]

    # Render at 6x zoom for high resolution
    mat = fitz.Matrix(6, 6)
    pix = page.get_pixmap(matrix=mat)
    img_path = "/home/user/MB/analysis/crossword_hires.png"
    pix.save(img_path)
    print(f"Saved hi-res image: {pix.width}x{pix.height}")
    return img_path

def find_grid_lines(img_path):
    """Find horizontal and vertical grid lines by scanning for dark pixels."""
    img = Image.open(img_path)
    arr = np.array(img)
    h, w = arr.shape[:2]
    gray = np.mean(arr[:,:,:3], axis=2) if len(arr.shape) == 3 else arr.astype(float)

    print(f"Image: {w}x{h}")

    # The crossword grid is in the right portion of the page
    # Scan multiple horizontal lines to find consistent vertical line positions

    # First, estimate grid area
    # Scan for columns with many dark pixels (vertical lines)
    col_darkness = np.sum(gray < 100, axis=0)  # Count dark pixels per column

    # Find the grid region - columns with high dark pixel counts
    threshold = h * 0.15
    grid_cols = np.where(col_darkness > threshold)[0]

    if len(grid_cols) == 0:
        print("No grid columns found, trying lower threshold")
        threshold = h * 0.05
        grid_cols = np.where(col_darkness > threshold)[0]

    if len(grid_cols) > 0:
        grid_x_start = grid_cols[0] - 10
        grid_x_end = grid_cols[-1] + 10
        print(f"Grid x range: {grid_x_start} to {grid_x_end}")
    else:
        print("FAILED to find grid columns")
        return None

    # Similarly for rows
    row_darkness = np.sum(gray[:, grid_x_start:grid_x_end] < 100, axis=1)
    row_threshold = (grid_x_end - grid_x_start) * 0.15
    grid_rows = np.where(row_darkness > row_threshold)[0]

    if len(grid_rows) > 0:
        grid_y_start = grid_rows[0] - 10
        grid_y_end = grid_rows[-1] + 10
        print(f"Grid y range: {grid_y_start} to {grid_y_end}")
    else:
        print("FAILED to find grid rows")
        return None

    # Now find actual grid line positions within the grid area
    # Vertical lines: columns where darkness spikes
    region = gray[grid_y_start:grid_y_end, grid_x_start:grid_x_end]

    # For vertical lines: compute column darkness in grid region
    v_darkness = np.sum(region < 100, axis=0)
    v_threshold = (grid_y_end - grid_y_start) * 0.3

    # Find peaks (grid lines)
    v_candidates = np.where(v_darkness > v_threshold)[0]

    # Cluster nearby candidates
    vlines = []
    if len(v_candidates) > 0:
        cluster = [v_candidates[0]]
        for i in range(1, len(v_candidates)):
            if v_candidates[i] - v_candidates[i-1] <= 3:
                cluster.append(v_candidates[i])
            else:
                vlines.append(int(np.mean(cluster)) + grid_x_start)
                cluster = [v_candidates[i]]
        vlines.append(int(np.mean(cluster)) + grid_x_start)

    # For horizontal lines
    h_darkness = np.sum(region < 100, axis=1)
    h_threshold = (grid_x_end - grid_x_start) * 0.3
    h_candidates = np.where(h_darkness > h_threshold)[0]

    hlines = []
    if len(h_candidates) > 0:
        cluster = [h_candidates[0]]
        for i in range(1, len(h_candidates)):
            if h_candidates[i] - h_candidates[i-1] <= 3:
                cluster.append(h_candidates[i])
            else:
                hlines.append(int(np.mean(cluster)) + grid_y_start)
                cluster = [h_candidates[i]]
        hlines.append(int(np.mean(cluster)) + grid_y_start)

    print(f"Found {len(vlines)} vertical lines, {len(hlines)} horizontal lines")

    if len(vlines) >= 2:
        avg_spacing = np.mean(np.diff(vlines))
        print(f"Average v-line spacing: {avg_spacing:.1f}px → {len(vlines)-1} columns")
    if len(hlines) >= 2:
        avg_spacing = np.mean(np.diff(hlines))
        print(f"Average h-line spacing: {avg_spacing:.1f}px → {len(hlines)-1} rows")

    return {
        'vlines': vlines,
        'hlines': hlines,
        'img_path': img_path,
        'gray': gray
    }

def extract_cells(grid_info):
    """Extract black/white status of each cell."""
    vlines = grid_info['vlines']
    hlines = grid_info['hlines']
    gray = grid_info['gray']

    n_cols = len(vlines) - 1
    n_rows = len(hlines) - 1

    print(f"\nExtracting {n_rows}x{n_cols} grid")

    grid = []
    for r in range(n_rows):
        row = []
        for c in range(n_cols):
            # Get cell bounds
            x1 = vlines[c]
            x2 = vlines[c+1]
            y1 = hlines[r]
            y2 = hlines[r+1]

            # Sample inner 40% of cell to avoid grid lines
            dx = x2 - x1
            dy = y2 - y1
            cx1 = x1 + int(dx * 0.3)
            cx2 = x2 - int(dx * 0.3)
            cy1 = y1 + int(dy * 0.3)
            cy2 = y2 - int(dy * 0.3)

            # Get average brightness
            cell_region = gray[cy1:cy2, cx1:cx2]
            avg = np.mean(cell_region)

            # Black cell if average brightness is low
            is_black = avg < 128
            row.append(1 if is_black else 0)
        grid.append(row)

    return np.array(grid), n_rows, n_cols

def number_grid(grid):
    """Standard crossword numbering."""
    n_rows, n_cols = grid.shape
    numbering = {}
    num = 1

    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c] == 1:  # Black cell
                continue

            starts_across = False
            starts_down = False

            # Starts across: left edge or black to left, and white to right
            if (c == 0 or grid[r][c-1] == 1):
                if c + 1 < n_cols and grid[r][c+1] == 0:
                    starts_across = True

            # Starts down: top edge or black above, and white below
            if (r == 0 or grid[r-1][c] == 1):
                if r + 1 < n_rows and grid[r+1][c] == 0:
                    starts_down = True

            if starts_across or starts_down:
                numbering[num] = {
                    'row': r, 'col': c,
                    'across': starts_across, 'down': starts_down
                }
                num += 1

    return numbering

def validate(numbering):
    """Validate against known entry lists."""
    comp_across = {n for n, info in numbering.items() if info['across']}
    comp_down = {n for n, info in numbering.items() if info['down']}

    a_match = comp_across == ACROSS_SET
    d_match = comp_down == DOWN_SET

    print(f"Computed: {len(comp_across)} across, {len(comp_down)} down")
    print(f"Expected: {len(ACROSS)} across, {len(DOWN)} down")
    print(f"Max number: {max(numbering.keys()) if numbering else 0} (expected {MAX_NUM})")
    print(f"Across match: {a_match}, Down match: {d_match}")

    if not a_match:
        missing = ACROSS_SET - comp_across
        extra = comp_across - ACROSS_SET
        if missing: print(f"  Missing across: {sorted(missing)[:20]}...")
        if extra: print(f"  Extra across: {sorted(extra)[:20]}...")
    if not d_match:
        missing = DOWN_SET - comp_down
        extra = comp_down - DOWN_SET
        if missing: print(f"  Missing down: {sorted(missing)[:20]}...")
        if extra: print(f"  Extra down: {sorted(extra)[:20]}...")

    return a_match and d_match

def print_grid_visual(grid):
    """Print ASCII visualization."""
    for r in range(grid.shape[0]):
        line = ""
        for c in range(grid.shape[1]):
            line += "##" if grid[r][c] == 1 else ".."
        print(line)

def test_qr_overlay(grid):
    """Test various QR code overlay theories."""
    n_rows, n_cols = grid.shape
    print(f"\n{'='*60}")
    print(f"QR CODE OVERLAY TESTS ({n_rows}x{n_cols} grid)")
    print(f"{'='*60}")

    results = []

    # Theory 1: Left-right fold (overlay left half onto right half)
    if n_cols >= 2:
        half = n_cols // 2

        for op_name, op_fn in [("OR", np.logical_or), ("AND", np.logical_and), ("XOR", np.logical_xor)]:
            # Left half and right half (same size)
            left = grid[:, :half]
            right_flipped = np.fliplr(grid[:, n_cols-half:])

            result = op_fn(left, right_flipped).astype(int)
            black_count = np.sum(result)

            # Check for QR finder patterns (7x7 squares with specific pattern)
            has_finder = check_qr_finder(result)

            results.append(f"LR fold {op_name}: {result.shape}, {black_count} black, finder={has_finder}")
            print(f"  LR fold {op_name}: {result.shape}, {black_count} black cells, QR finder pattern: {has_finder}")

            # Save image
            save_grid_image(result, f"/home/user/MB/analysis/qr_overlay/test_LR_{op_name}.png")

    # Theory 2: Top-bottom fold
    if n_rows >= 2:
        half = n_rows // 2

        for op_name, op_fn in [("OR", np.logical_or), ("AND", np.logical_and), ("XOR", np.logical_xor)]:
            top = grid[:half, :]
            bottom_flipped = np.flipud(grid[n_rows-half:, :])

            result = op_fn(top, bottom_flipped).astype(int)
            black_count = np.sum(result)
            has_finder = check_qr_finder(result)

            results.append(f"TB fold {op_name}: {result.shape}, {black_count} black, finder={has_finder}")
            print(f"  TB fold {op_name}: {result.shape}, {black_count} black cells, QR finder pattern: {has_finder}")

            save_grid_image(result, f"/home/user/MB/analysis/qr_overlay/test_TB_{op_name}.png")

    # Theory 3: Full grid rotations as QR
    for rot in [0, 90, 180, 270]:
        rotated = np.rot90(grid, k=rot//90)
        has_finder = check_qr_finder(rotated)
        if has_finder:
            print(f"  Full grid rotated {rot}°: QR FINDER FOUND!")
            save_grid_image(rotated, f"/home/user/MB/analysis/qr_overlay/test_full_rot{rot}.png")

    # Theory 4: Grid as Data Matrix (no finder patterns needed, but L-shaped border)
    has_dm = check_datamatrix_border(grid)
    print(f"  Full grid as Data Matrix: L-border = {has_dm}")

    for rot in [0, 90, 180, 270]:
        rotated = np.rot90(grid, k=rot//90)
        has_dm = check_datamatrix_border(rotated)
        if has_dm:
            print(f"  Rotated {rot}° as Data Matrix: L-BORDER FOUND!")

    # Theory 5: Inverted grid (swap black/white)
    inverted = 1 - grid
    for rot in [0, 90, 180, 270]:
        rotated = np.rot90(inverted, k=rot//90)
        has_finder = check_qr_finder(rotated)
        if has_finder:
            print(f"  INVERTED grid rotated {rot}°: QR FINDER FOUND!")
            save_grid_image(rotated, f"/home/user/MB/analysis/qr_overlay/test_inv_rot{rot}.png")

    # Theory 6: Make it square by padding
    if n_rows != n_cols:
        target = max(n_rows, n_cols)
        padded = np.zeros((target, target), dtype=int)
        padded[:n_rows, :n_cols] = grid
        has_finder = check_qr_finder(padded)
        print(f"  Zero-padded to {target}x{target}: QR finder = {has_finder}")
        save_grid_image(padded, f"/home/user/MB/analysis/qr_overlay/test_padded.png")

        # Also try centering
        centered = np.zeros((target, target), dtype=int)
        r_off = (target - n_rows) // 2
        c_off = (target - n_cols) // 2
        centered[r_off:r_off+n_rows, c_off:c_off+n_cols] = grid
        has_finder = check_qr_finder(centered)
        print(f"  Centered in {target}x{target}: QR finder = {has_finder}")

    # Theory 7: QR version 1 is 21x21 - if grid is 21x21, test directly
    if n_rows == 21 and n_cols == 21:
        print(f"\n  Grid IS 21x21 = QR Version 1!")
        # Check QR format info at specific positions
        check_qr_format_info(grid)

    # Theory 8: Split grid at column 13 (position of the gap in the image)
    if n_cols > 13:
        left_part = grid[:, :13]
        right_part = grid[:, 8:]  # Overlap region
        print(f"\n  Left 13 cols: {left_part.shape}, Right from col 8: {right_part.shape}")

    return results

def check_qr_finder(grid):
    """Check if grid contains QR finder patterns (7x7 with specific structure)."""
    n_rows, n_cols = grid.shape
    if n_rows < 7 or n_cols < 7:
        return False

    # QR finder pattern: 7x7 square with:
    # Row 0: 1111111
    # Row 1: 1000001
    # Row 2: 1011101
    # Row 3: 1011101
    # Row 4: 1011101
    # Row 5: 1000001
    # Row 6: 1111111
    finder = np.array([
        [1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1]
    ])

    # Also check inverted finder
    inv_finder = 1 - finder

    # Check all possible positions
    for r in range(n_rows - 6):
        for c in range(n_cols - 6):
            region = grid[r:r+7, c:c+7]
            if np.array_equal(region, finder) or np.array_equal(region, inv_finder):
                print(f"    FINDER at ({r},{c})!")
                return True

    return False

def check_datamatrix_border(grid):
    """Check for Data Matrix L-shaped solid border."""
    n_rows, n_cols = grid.shape

    # Data Matrix has solid black bottom and left borders
    # Check left column (all 1s)
    left_col = grid[:, 0]
    bottom_row = grid[-1, :]

    left_solid = np.all(left_col == 1)
    bottom_solid = np.all(bottom_row == 1)

    # Also check alternating top and right borders
    top_row = grid[0, :]
    right_col = grid[:, -1]

    # Alternating pattern: 1,0,1,0,...
    top_alt = all(top_row[i] == (i % 2 == 0) for i in range(len(top_row)))
    right_alt = all(right_col[i] == (i % 2 == 0) for i in range(len(right_col)))

    if left_solid and bottom_solid:
        return True
    if left_solid and top_alt:
        return True

    return False

def check_qr_format_info(grid):
    """For a 21x21 grid, check QR version 1 format info positions."""
    # QR Version 1 structure:
    # Finder patterns at corners: (0,0), (0,14), (14,0)
    # Format info along row 8 and column 8

    # Check three corners for finder patterns
    corners = [(0,0), (0,14), (14,0)]
    for r, c in corners:
        if r+7 <= 21 and c+7 <= 21:
            region = grid[r:r+7, c:c+7]
            finder = np.array([
                [1,1,1,1,1,1,1],
                [1,0,0,0,0,0,1],
                [1,0,1,1,1,0,1],
                [1,0,1,1,1,0,1],
                [1,0,1,1,1,0,1],
                [1,0,0,0,0,0,1],
                [1,1,1,1,1,1,1]
            ])
            match = np.sum(region == finder)
            total = 49
            print(f"    Corner ({r},{c}): {match}/{total} cells match finder pattern ({100*match//total}%)")

def save_grid_image(grid, path, scale=10):
    """Save a binary grid as a black/white PNG."""
    n_rows, n_cols = grid.shape
    img = Image.new('L', (n_cols * scale, n_rows * scale), 255)
    draw = ImageDraw.Draw(img)

    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c] == 1:
                draw.rectangle([c*scale, r*scale, (c+1)*scale-1, (r+1)*scale-1], fill=0)

    img.save(path)

def try_decode_as_qr(grid, label=""):
    """Try to decode a binary grid as QR/barcode."""
    try:
        from pyzbar.pyzbar import decode as pyzbar_decode
        # Create image from grid
        scale = 10
        n_rows, n_cols = grid.shape
        img = Image.new('L', (n_cols * scale, n_rows * scale), 255)
        draw = ImageDraw.Draw(img)
        for r in range(n_rows):
            for c in range(n_cols):
                if grid[r][c] == 1:
                    draw.rectangle([c*scale, r*scale, (c+1)*scale-1, (r+1)*scale-1], fill=0)

        results = pyzbar_decode(img)
        if results:
            print(f"  DECODED ({label}): {results}")
            return results
    except ImportError:
        pass

    return None

def main():
    print("=" * 60)
    print("CROSSWORD GRID EXTRACTION AND QR CODE ANALYSIS")
    print("=" * 60)

    # Step 1: Extract high-res image
    img_path = extract_from_pdf()
    if img_path is None:
        img_path = "/home/user/MB/screenshots/Crossword.png"

    # Step 2: Find grid lines
    print("\n--- Finding grid lines ---")
    grid_info = find_grid_lines(img_path)

    if grid_info is None:
        print("FAILED to find grid. Trying Crossword.png directly...")
        grid_info = find_grid_lines("/home/user/MB/screenshots/Crossword.png")

    if grid_info is None:
        print("FAILED on both sources")
        return

    # Step 3: Extract cells
    grid, n_rows, n_cols = extract_cells(grid_info)

    print(f"\n--- Grid: {n_rows} rows x {n_cols} cols ---")
    print(f"Black cells: {np.sum(grid)}, White cells: {np.sum(grid==0)}")
    print_grid_visual(grid)

    # Step 4: Number and validate
    print("\n--- Numbering grid ---")
    numbering = number_grid(grid)
    valid = validate(numbering)

    # Step 5: Compute entry lengths if valid
    if valid or True:  # Always show lengths for debugging
        print("\n--- Entry lengths ---")
        for num in sorted(numbering.keys())[:30]:
            info = numbering[num]
            parts = []
            if info['across']:
                # Count across length
                length = 0
                c = info['col']
                while c < n_cols and grid[info['row']][c] == 0:
                    length += 1
                    c += 1
                parts.append(f"A={length}")
            if info['down']:
                length = 0
                r = info['row']
                while r < n_rows and grid[r][info['col']] == 0:
                    length += 1
                    r += 1
                parts.append(f"D={length}")
            print(f"  {num}: ({info['row']},{info['col']}) {', '.join(parts)}")

    # Step 6: QR overlay tests
    test_qr_overlay(grid)

    # Step 7: Try decoding as-is with pyzbar
    print("\n--- Attempting barcode decode ---")
    for rot in [0, 90, 180, 270]:
        rotated = np.rot90(grid, k=rot//90)
        result = try_decode_as_qr(rotated, f"rot{rot}")
        if result:
            print(f"  SUCCESS at rotation {rot}!")

        # Also try inverted
        result = try_decode_as_qr(1 - rotated, f"inv_rot{rot}")
        if result:
            print(f"  SUCCESS (inverted) at rotation {rot}!")

    # Save grid data
    save_data = {
        'grid': grid.tolist(),
        'dimensions': [n_rows, n_cols],
        'black_cells': int(np.sum(grid)),
        'white_cells': int(np.sum(grid == 0)),
        'valid': valid,
        'numbering': {str(k): v for k, v in numbering.items()}
    }

    with open('/home/user/MB/analysis/qr_overlay/grid_extracted_v2.json', 'w') as f:
        json.dump(save_data, f, indent=2)

    print(f"\nSaved to grid_extracted_v2.json")
    print(f"Validation: {'PASSED' if valid else 'FAILED'}")

if __name__ == '__main__':
    main()
