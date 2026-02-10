#!/usr/bin/env python3
"""
Reconstruct the 21x21 crossword grid using TWO approaches:
1. Extract vector graphics (filled rectangles) from the PDF
2. If that fails, use constraint-based reconstruction from entry numbers

Then test QR code overlay theories with the valid grid.
"""

import json
import sys

try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

try:
    from PIL import Image
    import numpy as np
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Known entry lists
ACROSS = [1,8,14,22,23,24,25,28,29,30,31,32,34,35,36,38,41,42,43,45,47,48,50,54,57,58,59,61,63,64,66,68,70,72,73,77,79,80,81,82,83,85,88,90,91,92,94,97,99,100,102,103,105,106,107,109,111,113,114,117,119,120,121,123,124,127,129,132,134,136,138,141,143,145,147,148,149,153,155,156,158,159,161,164,165,167,171,172,173,174,175,176]
DOWN = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,26,27,33,37,39,40,43,44,46,49,51,52,53,55,56,60,62,65,67,69,71,72,74,75,76,77,78,80,83,84,86,87,89,93,95,96,98,101,104,108,110,112,115,116,117,118,122,124,125,126,128,130,131,133,135,137,139,140,141,142,144,150,151,152,153,154,157,160,162,163,166,168,169,170]

ACROSS_SET = set(ACROSS)
DOWN_SET = set(DOWN)
BOTH_SET = ACROSS_SET & DOWN_SET
ACROSS_ONLY = ACROSS_SET - DOWN_SET
DOWN_ONLY = DOWN_SET - ACROSS_SET

ALL_NUMBERS = sorted(ACROSS_SET | DOWN_SET)
MAX_NUM = max(ALL_NUMBERS)  # 176

# Known entry lengths from confirmed answers
KNOWN_LENGTHS = {
    # 167A = SUPERBOWLSTADIUM (16 letters)
    '167A': 16,
    # 149A = BEASTLAND (9 letters)
    '149A': 9,
}

def extract_vector_grid(pdf_path):
    """Extract grid from PDF vector graphics (filled rectangles)."""
    if not HAS_FITZ:
        print("PyMuPDF not available")
        return None

    doc = fitz.open(pdf_path)
    page = doc[0]

    # Get all drawings on the page
    drawings = page.get_drawings()
    print(f"Found {len(drawings)} drawings on page 1")

    # Look for filled rectangles (black cells)
    filled_rects = []
    all_rects = []
    for d in drawings:
        # Each drawing has 'items' with path operations
        for item in d.get('items', []):
            if item[0] == 're':  # rectangle
                rect = item[1]  # fitz.Rect
                all_rects.append({
                    'rect': rect,
                    'fill': d.get('fill'),
                    'color': d.get('color'),
                    'width': d.get('width'),
                })
                if d.get('fill') is not None:
                    filled_rects.append({
                        'rect': rect,
                        'fill': d.get('fill'),
                        'color': d.get('color'),
                    })

    print(f"Found {len(all_rects)} rectangles total, {len(filled_rects)} filled")

    # Analyze filled rectangles to find black cells
    black_rects = []
    for fr in filled_rects:
        fill = fr['fill']
        # Black fill: RGB close to (0,0,0)
        if fill and len(fill) >= 3:
            r, g, b = fill[0], fill[1], fill[2]
            if r < 0.2 and g < 0.2 and b < 0.2:
                rect = fr['rect']
                w = rect.width
                h = rect.height
                # Filter for reasonable cell sizes (not lines, not full page)
                if 5 < w < 100 and 5 < h < 100:
                    black_rects.append(fr)
        elif fill == (0,):
            # Grayscale black
            rect = fr['rect']
            w = rect.width
            h = rect.height
            if 5 < w < 100 and 5 < h < 100:
                black_rects.append(fr)

    print(f"Found {len(black_rects)} black-filled rectangles (potential black cells)")

    if black_rects:
        # Determine grid cell size from the rectangles
        widths = [r['rect'].width for r in black_rects]
        heights = [r['rect'].height for r in black_rects]

        median_w = sorted(widths)[len(widths)//2]
        median_h = sorted(heights)[len(heights)//2]
        print(f"Median black cell size: {median_w:.1f} x {median_h:.1f}")

        # Get the bounding box of all black cells
        xs = [r['rect'].x0 for r in black_rects] + [r['rect'].x1 for r in black_rects]
        ys = [r['rect'].y0 for r in black_rects] + [r['rect'].y1 for r in black_rects]

        grid_left = min(r['rect'].x0 for r in black_rects)
        grid_right = max(r['rect'].x1 for r in black_rects)
        grid_top = min(r['rect'].y0 for r in black_rects)
        grid_bottom = max(r['rect'].y1 for r in black_rects)

        print(f"Grid bounds from black cells: ({grid_left:.1f}, {grid_top:.1f}) to ({grid_right:.1f}, {grid_bottom:.1f})")

        # Determine grid position for each black cell
        cell_w = median_w
        cell_h = median_h

        grid = [['W']*21 for _ in range(21)]
        placed = 0

        for br in black_rects:
            rect = br['rect']
            cx = (rect.x0 + rect.x1) / 2
            cy = (rect.y0 + rect.y1) / 2

            col = round((cx - grid_left) / cell_w)
            row = round((cy - grid_top) / cell_h)

            if 0 <= row < 21 and 0 <= col < 21:
                grid[row][col] = 'B'
                placed += 1

        print(f"Placed {placed} black cells in 21x21 grid")
        return grid

    # Also check for line drawings that form a grid pattern
    print("\nChecking for grid lines...")
    lines = []
    for d in drawings:
        for item in d.get('items', []):
            if item[0] == 'l':  # line
                p1, p2 = item[1], item[2]
                lines.append((p1, p2, d.get('color'), d.get('width')))

    print(f"Found {len(lines)} line segments")

    # Look for all rectangles that might be grid outlines
    print("\nAll rectangle sizes (first 30):")
    for i, r in enumerate(all_rects[:30]):
        rect = r['rect']
        print(f"  {i}: ({rect.x0:.1f}, {rect.y0:.1f}) - ({rect.x1:.1f}, {rect.y1:.1f}) "
              f"size={rect.width:.1f}x{rect.height:.1f} fill={r['fill']} color={r['color']}")

    return None


def extract_grid_pixel_precise(pdf_path):
    """Extract grid by rendering at very high resolution and careful pixel analysis."""
    if not HAS_FITZ or not HAS_PIL:
        return None

    doc = fitz.open(pdf_path)
    page = doc[0]

    # Render at 6x for high precision
    zoom = 6
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)

    # Save for reference
    img_path = "/home/user/MB/analysis/grid_6x.png"
    pix.save(img_path)

    # Convert to numpy array
    img = Image.open(img_path)
    arr = np.array(img)
    h, w = arr.shape[:2]
    print(f"Rendered at {zoom}x: {w} x {h}")

    # Convert to grayscale
    if len(arr.shape) == 3:
        gray = np.mean(arr[:,:,:3], axis=2)
    else:
        gray = arr.astype(float)

    # Find the grid by looking for the dense region of dark lines
    # The grid should be in the right portion of the page
    # Scan for vertical dark line density

    # Create binary image (dark < 80)
    binary = (gray < 80).astype(np.uint8)

    # Sum dark pixels along columns in the grid region
    # Expected grid area: x from 35% to 87% of page width, y from 5% to 72% of page height
    x_start = int(w * 0.30)
    x_end = int(w * 0.92)
    y_start = int(h * 0.03)
    y_end = int(h * 0.76)

    region = binary[y_start:y_end, x_start:x_end]
    rh, rw = region.shape

    # Find vertical line positions: columns with high dark pixel density
    col_sums = np.sum(region, axis=0)
    col_threshold = rh * 0.3  # At least 30% of column height should be dark

    # Find peaks in column sums (grid lines)
    vline_candidates = np.where(col_sums > col_threshold)[0]

    # Cluster adjacent dark columns
    vlines = []
    if len(vline_candidates) > 0:
        cluster = [vline_candidates[0]]
        for i in range(1, len(vline_candidates)):
            if vline_candidates[i] - vline_candidates[i-1] <= 3:
                cluster.append(vline_candidates[i])
            else:
                vlines.append(int(np.mean(cluster)) + x_start)
                cluster = [vline_candidates[i]]
        vlines.append(int(np.mean(cluster)) + x_start)

    print(f"Found {len(vlines)} vertical grid lines")

    # Find horizontal line positions
    row_sums = np.sum(region, axis=1)
    row_threshold = rw * 0.3

    hline_candidates = np.where(row_sums > row_threshold)[0]

    hlines = []
    if len(hline_candidates) > 0:
        cluster = [hline_candidates[0]]
        for i in range(1, len(hline_candidates)):
            if hline_candidates[i] - hline_candidates[i-1] <= 3:
                cluster.append(hline_candidates[i])
            else:
                hlines.append(int(np.mean(cluster)) + y_start)
                cluster = [hline_candidates[i]]
        hlines.append(int(np.mean(cluster)) + y_start)

    print(f"Found {len(hlines)} horizontal grid lines")

    if len(vlines) < 22 or len(hlines) < 22:
        print("Not enough grid lines found. Trying with lower threshold...")

        # Try lower thresholds
        for thresh_pct in [0.2, 0.15, 0.10]:
            col_threshold = rh * thresh_pct
            vline_candidates = np.where(col_sums > col_threshold)[0]
            vlines = []
            if len(vline_candidates) > 0:
                cluster = [vline_candidates[0]]
                for i in range(1, len(vline_candidates)):
                    if vline_candidates[i] - vline_candidates[i-1] <= 3:
                        cluster.append(vline_candidates[i])
                    else:
                        vlines.append(int(np.mean(cluster)) + x_start)
                        cluster = [vline_candidates[i]]
                vlines.append(int(np.mean(cluster)) + x_start)

            row_threshold = rw * thresh_pct
            hline_candidates = np.where(row_sums > row_threshold)[0]
            hlines = []
            if len(hline_candidates) > 0:
                cluster = [hline_candidates[0]]
                for i in range(1, len(hline_candidates)):
                    if hline_candidates[i] - hline_candidates[i-1] <= 3:
                        cluster.append(hline_candidates[i])
                    else:
                        hlines.append(int(np.mean(cluster)) + y_start)
                        cluster = [hline_candidates[i]]
                hlines.append(int(np.mean(cluster)) + y_start)

            print(f"  thresh={thresh_pct}: {len(vlines)} vlines, {len(hlines)} hlines")

            if len(vlines) >= 22 and len(hlines) >= 22:
                break

    if len(vlines) >= 22 and len(hlines) >= 22:
        # Use first 22 of each for the 21x21 grid
        vlines = vlines[:22]
        hlines = hlines[:22]

        print(f"\nGrid line positions:")
        print(f"  V: {vlines[:5]}...{vlines[-3:]}")
        print(f"  H: {hlines[:5]}...{hlines[-3:]}")

        # Sample each cell center
        grid = [['W']*21 for _ in range(21)]

        for row in range(21):
            for col in range(21):
                y1 = hlines[row]
                y2 = hlines[row+1]
                x1 = vlines[col]
                x2 = vlines[col+1]

                # Sample center 40% of cell
                cy1 = y1 + (y2-y1)*3//10
                cy2 = y1 + (y2-y1)*7//10
                cx1 = x1 + (x2-x1)*3//10
                cx2 = x1 + (x2-x1)*7//10

                cell_region = gray[cy1:cy2, cx1:cx2]
                avg_brightness = np.mean(cell_region)

                # Also check for gray cells (staircase)
                if avg_brightness < 90:
                    grid[row][col] = 'B'
                elif avg_brightness < 170:
                    grid[row][col] = 'G'  # Gray (staircase)
                else:
                    grid[row][col] = 'W'

        return grid, vlines, hlines

    return None


def number_grid(grid):
    """Apply standard crossword numbering."""
    rows = len(grid)
    cols = len(grid[0])
    numbering = {}
    num = 1

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'B':
                continue

            starts_across = False
            starts_down = False

            # Starts across if (leftmost or left is black) and right is white
            if (c == 0 or grid[r][c-1] == 'B'):
                if c + 1 < cols and grid[r][c+1] != 'B':
                    starts_across = True

            # Starts down if (topmost or above is black) and below is white
            if (r == 0 or grid[r-1][c] == 'B'):
                if r + 1 < rows and grid[r+1][c] != 'B':
                    starts_down = True

            if starts_across or starts_down:
                numbering[num] = {
                    'row': r, 'col': c,
                    'across': starts_across,
                    'down': starts_down
                }
                num += 1

    return numbering


def validate_numbering(numbering):
    """Validate against known entry lists."""
    computed_across = {n for n, info in numbering.items() if info['across']}
    computed_down = {n for n, info in numbering.items() if info['down']}

    across_ok = computed_across == ACROSS_SET
    down_ok = computed_down == DOWN_SET

    total = max(numbering.keys()) if numbering else 0

    print(f"Total numbered cells: {total} (expected {MAX_NUM})")
    print(f"Across: {len(computed_across)} entries (expected {len(ACROSS)}), match={across_ok}")
    print(f"Down: {len(computed_down)} entries (expected {len(DOWN)}), match={down_ok}")

    if not across_ok:
        missing = ACROSS_SET - computed_across
        extra = computed_across - ACROSS_SET
        if missing: print(f"  Missing ACROSS: {sorted(missing)[:20]}")
        if extra: print(f"  Extra ACROSS: {sorted(extra)[:20]}")

    if not down_ok:
        missing = DOWN_SET - computed_down
        extra = computed_down - DOWN_SET
        if missing: print(f"  Missing DOWN: {sorted(missing)[:20]}")
        if extra: print(f"  Extra DOWN: {sorted(extra)[:20]}")

    return across_ok and down_ok


def compute_entry_lengths(grid, numbering):
    """Compute length of each entry."""
    rows = len(grid)
    cols = len(grid[0])

    across_lengths = {}
    down_lengths = {}

    for num, info in numbering.items():
        r, c = info['row'], info['col']

        if info['across']:
            length = 0
            cc = c
            while cc < cols and grid[r][cc] != 'B':
                length += 1
                cc += 1
            across_lengths[num] = length

        if info['down']:
            length = 0
            rr = r
            while rr < rows and grid[rr][c] != 'B':
                length += 1
                rr += 1
            down_lengths[num] = length

    return across_lengths, down_lengths


def print_grid(grid):
    """Print grid visually."""
    for row in grid:
        line = ""
        for cell in row:
            if cell == 'B':
                line += "##"
            elif cell == 'G':
                line += "░░"
            else:
                line += ".."
        print(line)


def test_qr_overlay(grid):
    """Test various QR code overlay theories with the grid."""
    rows = len(grid)
    cols = len(grid[0])

    # Convert to binary: 1=black, 0=white
    binary = [[1 if grid[r][c] == 'B' else 0 for c in range(cols)] for r in range(rows)]

    print("\n" + "="*60)
    print("QR CODE OVERLAY TESTS")
    print("="*60)

    # Test 1: Left-Right fold (overlay left half onto right half)
    if cols % 2 == 1:
        mid = cols // 2

        # Left half: columns 0..mid-1 (flipped)
        # Right half: columns mid+1..cols-1
        half_size = mid

        print(f"\nTest 1: LR fold around center column {mid}")

        for op_name, op_func in [("OR", lambda a,b: a|b), ("AND", lambda a,b: a&b), ("XOR", lambda a,b: a^b)]:
            result = [[0]*half_size for _ in range(rows)]
            for r in range(rows):
                for c in range(half_size):
                    left_val = binary[r][mid - 1 - c]  # Mirror left
                    right_val = binary[r][mid + 1 + c]
                    result[r][c] = op_func(left_val, right_val)

            black_count = sum(sum(row) for row in result)
            print(f"  LR {op_name}: {half_size}x{rows} grid, {black_count} black cells")

    # Test 2: Top-Bottom fold (overlay top half onto bottom half)
    if rows % 2 == 1:
        mid = rows // 2
        half_size = mid

        print(f"\nTest 2: TB fold around center row {mid}")

        for op_name, op_func in [("OR", lambda a,b: a|b), ("AND", lambda a,b: a&b), ("XOR", lambda a,b: a^b)]:
            result = [[0]*cols for _ in range(half_size)]
            for r in range(half_size):
                for c in range(cols):
                    top_val = binary[mid - 1 - r][c]  # Mirror top
                    bot_val = binary[mid + 1 + r][c]
                    result[r][c] = op_func(top_val, bot_val)

            black_count = sum(sum(row) for row in result)
            print(f"  TB {op_name}: {cols}x{half_size} grid, {black_count} black cells")

    # Test 3: Full 21x21 as-is - check for QR finder patterns
    print(f"\nTest 3: Check for QR finder patterns in raw grid")
    check_qr_finder(binary)

    # Test 4: Fold from user's image theory
    # The user showed left and right halves of the grid overlaid
    # "Not doubling up" means XOR or they perfectly complement
    print(f"\nTest 4: Check left/right complementarity")
    if cols % 2 == 1:
        mid = cols // 2
        complement_count = 0
        total = 0
        for r in range(rows):
            for c in range(mid):
                left_val = binary[r][c]
                right_val = binary[r][cols - 1 - c]
                if left_val != right_val:
                    complement_count += 1
                total += 1
        print(f"  Left-right complement: {complement_count}/{total} cells are complementary ({100*complement_count/total:.1f}%)")

        # If high complementarity, the XOR/OR gives interesting pattern
        if complement_count > total * 0.8:
            print("  HIGH complementarity! XOR overlay would produce all-black or all-white grid")

    # Test 5: Rotate and overlay
    print(f"\nTest 5: 180-degree rotation overlay")
    for op_name, op_func in [("OR", lambda a,b: a|b), ("AND", lambda a,b: a&b), ("XOR", lambda a,b: a^b)]:
        result = [[0]*cols for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                orig = binary[r][c]
                rotated = binary[rows-1-r][cols-1-c]
                result[r][c] = op_func(orig, rotated)

        black_count = sum(sum(row) for row in result)
        print(f"  180° {op_name}: {black_count} black cells out of {rows*cols}")

    # Test 6: Check if grid is symmetric
    print(f"\nTest 6: Grid symmetry check")
    sym_180 = True
    sym_lr = True
    sym_tb = True
    for r in range(rows):
        for c in range(cols):
            if binary[r][c] != binary[rows-1-r][cols-1-c]:
                sym_180 = False
            if binary[r][c] != binary[r][cols-1-c]:
                sym_lr = False
            if binary[r][c] != binary[rows-1-r][c]:
                sym_tb = False

    print(f"  180° rotational symmetry: {sym_180}")
    print(f"  Left-right mirror symmetry: {sym_lr}")
    print(f"  Top-bottom mirror symmetry: {sym_tb}")


def check_qr_finder(binary):
    """Check for QR code finder patterns (7x7 pattern in corners)."""
    rows = len(binary)
    cols = len(binary[0])

    # QR finder pattern is 7x7:
    # 1111111
    # 1000001
    # 1011101
    # 1011101
    # 1011101
    # 1000001
    # 1111111
    finder = [
        [1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1],
    ]

    # Check all 4 corners
    corners = [
        ("top-left", 0, 0),
        ("top-right", 0, cols-7),
        ("bottom-left", rows-7, 0),
        ("bottom-right", rows-7, cols-7),
    ]

    for name, start_r, start_c in corners:
        if start_r < 0 or start_c < 0 or start_r+7 > rows or start_c+7 > cols:
            continue

        match = 0
        total = 49
        for dr in range(7):
            for dc in range(7):
                if binary[start_r+dr][start_c+dc] == finder[dr][dc]:
                    match += 1

        # Also check inverted
        inv_match = total - match

        print(f"  {name}: {match}/{total} match ({100*match/total:.0f}%), "
              f"inverted: {inv_match}/{total} ({100*inv_match/total:.0f}%)")


def main():
    pdf_path = "/home/user/MB/puzzles/Million-Dollar-Crossword.pdf"

    # Approach 1: Vector graphics extraction
    print("="*60)
    print("APPROACH 1: Vector graphics extraction from PDF")
    print("="*60)

    grid = extract_vector_grid(pdf_path)

    if grid:
        print("\nExtracted grid:")
        print_grid(grid)

        black_count = sum(1 for r in grid for c in r if c == 'B')
        print(f"Black cells: {black_count}")

        numbering = number_grid(grid)
        valid = validate_numbering(numbering)

        if valid:
            print("\nGRID VALIDATED! Entry numbers match perfectly.")
            across_lengths, down_lengths = compute_entry_lengths(grid, numbering)
            test_qr_overlay(grid)
            save_results(grid, numbering, across_lengths, down_lengths, valid)
            return
        else:
            print("\nVector grid doesn't match. Trying pixel approach...")

    # Approach 2: High-res pixel extraction
    print("\n" + "="*60)
    print("APPROACH 2: High-resolution pixel extraction")
    print("="*60)

    result = extract_grid_pixel_precise(pdf_path)

    if result:
        grid, vlines, hlines = result

        print("\nExtracted grid (W=white, B=black, G=gray):")
        print_grid(grid)

        # For numbering, treat gray as white (staircase cells are usable)
        grid_for_numbering = [['B' if c == 'B' else 'W' for c in row] for row in grid]

        black_count = sum(1 for r in grid for c in r if c == 'B')
        gray_count = sum(1 for r in grid for c in r if c == 'G')
        white_count = sum(1 for r in grid for c in r if c == 'W')
        print(f"Black: {black_count}, Gray: {gray_count}, White: {white_count}")

        numbering = number_grid(grid_for_numbering)
        valid = validate_numbering(numbering)

        if valid:
            print("\nGRID VALIDATED! Entry numbers match perfectly.")
            across_lengths, down_lengths = compute_entry_lengths(grid_for_numbering, numbering)
            test_qr_overlay(grid_for_numbering)
            save_results(grid_for_numbering, numbering, across_lengths, down_lengths, valid,
                        gray_cells=[(r,c) for r in range(21) for c in range(21) if grid[r][c] == 'G'])
            return
        else:
            print("\nPixel grid doesn't match either. Need to try constraint approach.")

            # Try adjusting brightness threshold
            print("\nTrying different brightness thresholds...")
            for threshold in [70, 80, 100, 110, 120]:
                # Re-threshold
                test_grid = [['W']*21 for _ in range(21)]

                if HAS_PIL:
                    img = Image.open("/home/user/MB/analysis/grid_6x.png")
                    arr = np.array(img)
                    gray_arr = np.mean(arr[:,:,:3], axis=2)

                    for row in range(21):
                        for col in range(21):
                            y1 = hlines[row]
                            y2 = hlines[row+1]
                            x1 = vlines[col]
                            x2 = vlines[col+1]

                            cy1 = y1 + (y2-y1)*3//10
                            cy2 = y1 + (y2-y1)*7//10
                            cx1 = x1 + (x2-x1)*3//10
                            cx2 = x1 + (x2-x1)*7//10

                            cell_region = gray_arr[cy1:cy2, cx1:cx2]
                            avg = np.mean(cell_region) if cell_region.size > 0 else 255

                            if avg < threshold:
                                test_grid[row][col] = 'B'

                    test_numbering = number_grid(test_grid)
                    test_valid = validate_numbering(test_numbering)

                    black_c = sum(1 for r in test_grid for c in r if c == 'B')
                    print(f"  Threshold {threshold}: {black_c} black cells, valid={test_valid}")

                    if test_valid:
                        print(f"\n  FOUND VALID GRID at threshold {threshold}!")
                        across_lengths, down_lengths = compute_entry_lengths(test_grid, test_numbering)
                        test_qr_overlay(test_grid)
                        save_results(test_grid, test_numbering, across_lengths, down_lengths, True)
                        return
    else:
        print("Pixel extraction failed too.")

    print("\n" + "="*60)
    print("All extraction approaches failed. Using known grid_data.json if available.")
    print("="*60)


def save_results(grid, numbering, across_lengths, down_lengths, valid, gray_cells=None):
    """Save validated grid results."""
    results = {
        'grid': grid,
        'valid': valid,
        'numbering': {str(k): v for k, v in numbering.items()},
        'across_lengths': {str(k): v for k, v in across_lengths.items()},
        'down_lengths': {str(k): v for k, v in down_lengths.items()},
    }

    if gray_cells:
        results['gray_cells'] = gray_cells

    # Also compute entry positions for crossword filling
    entries = {}
    for num, info in numbering.items():
        r, c = info['row'], info['col']
        if info['across']:
            length = across_lengths.get(num, 0)
            cells = [(r, c+i) for i in range(length)]
            entries[f"{num}A"] = {
                'cells': cells,
                'length': length,
                'start': [r, c],
                'direction': 'across'
            }
        if info['down']:
            length = down_lengths.get(num, 0)
            cells = [(r+i, c) for i in range(length)]
            entries[f"{num}D"] = {
                'cells': cells,
                'length': length,
                'start': [r, c],
                'direction': 'down'
            }

    results['entries'] = entries

    out_path = "/home/user/MB/analysis/grid_validated.json"
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {out_path}")

    # Print entry length summary
    print(f"\nEntry length summary:")
    print(f"  ACROSS ({len(across_lengths)} entries):")
    for num in sorted(across_lengths.keys()):
        info = numbering[num]
        print(f"    {num:3d}A: length {across_lengths[num]:2d} at ({info['row']},{info['col']})")

    print(f"\n  DOWN ({len(down_lengths)} entries):")
    for num in sorted(down_lengths.keys()):
        info = numbering[num]
        print(f"    {num:3d}D: length {down_lengths[num]:2d} at ({info['row']},{info['col']})")

    # Validate known answer lengths
    print(f"\nKnown answer length validation:")
    for key, expected_len in KNOWN_LENGTHS.items():
        if key in entries:
            actual_len = entries[key]['length']
            match = "OK" if actual_len == expected_len else "MISMATCH"
            print(f"  {key}: expected {expected_len}, got {actual_len} - {match}")
        else:
            print(f"  {key}: NOT FOUND in entries")


if __name__ == '__main__':
    main()
