#!/usr/bin/env python3
"""
Reconstruct the 21x21 crossword grid from the PDF image.
Uses the known ACROSS and DOWN entry numbers plus standard crossword rules.

Strategy: Use PyMuPDF (fitz) to extract the grid image, then analyze
black vs white cells by pixel color at cell centers.
"""

import sys
try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

import json

# Known entry lists from the puzzle
ACROSS = [1,8,14,22,23,24,25,28,29,30,31,32,34,35,36,38,41,42,43,45,47,48,50,54,57,58,59,61,63,64,66,68,70,72,73,77,79,80,81,82,83,85,88,90,91,92,94,97,99,100,102,103,105,106,107,109,111,113,114,117,119,120,121,123,124,127,129,132,134,136,138,141,143,145,147,148,149,153,155,156,158,159,161,164,165,167,171,172,173,174,175,176]
DOWN = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,26,27,33,37,39,40,43,44,46,49,51,52,53,55,56,60,62,65,67,69,71,72,74,75,76,77,78,80,83,84,86,87,89,93,95,96,98,101,104,108,110,112,115,116,117,118,122,124,125,126,128,130,131,133,135,137,139,140,141,142,144,150,151,152,153,154,157,160,162,163,166,168,169,170]

ACROSS_SET = set(ACROSS)
DOWN_SET = set(DOWN)
ALL_NUMBERS = sorted(ACROSS_SET | DOWN_SET)

def extract_grid_from_pdf(pdf_path):
    """Extract the crossword grid as a pixel array from the PDF."""
    if not HAS_FITZ:
        print("PyMuPDF not available, trying alternative...")
        return None

    doc = fitz.open(pdf_path)
    page = doc[0]

    # Render at high resolution
    mat = fitz.Matrix(4, 4)  # 4x zoom
    pix = page.get_pixmap(matrix=mat)

    # Save as PNG for analysis
    img_path = "/home/user/MB/analysis/crossword_grid.png"
    pix.save(img_path)
    print(f"Saved grid image to {img_path}")
    print(f"Image size: {pix.width} x {pix.height}")

    return img_path, pix

def analyze_grid_image(img_path):
    """Analyze the grid image to find black/white cells."""
    if not HAS_PIL:
        print("PIL not available")
        return None

    img = Image.open(img_path)
    pixels = img.load()
    w, h = img.size
    print(f"Image dimensions: {w} x {h}")

    # The grid is in the right portion of the image
    # From the PDF layout, the grid starts roughly at:
    # Looking at the image, the grid area is approximately:
    # The crossword grid occupies roughly the right 60% of the page
    # and the top 75% vertically

    # Let me sample colors across the image to find the grid bounds
    # First, find the grid by looking for the dense pattern of lines

    # At 4x zoom, the page is roughly 2448 x 3168 pixels
    # The grid in the original PDF is roughly:
    # Left edge: ~37% of page width
    # Right edge: ~87% of page width
    # Top edge: ~6% of page height
    # Bottom edge: ~72% of page height

    # These are approximate - let me scan for grid lines
    grid_left = int(w * 0.355)
    grid_right = int(w * 0.87)
    grid_top = int(h * 0.055)
    grid_bottom = int(h * 0.715)

    grid_w = grid_right - grid_left
    grid_h = grid_bottom - grid_top

    cell_w = grid_w / 21
    cell_h = grid_h / 21

    print(f"Grid bounds: ({grid_left}, {grid_top}) to ({grid_right}, {grid_bottom})")
    print(f"Grid size: {grid_w} x {grid_h}")
    print(f"Cell size: {cell_w:.1f} x {cell_h:.1f}")

    # Sample center of each cell to determine black/white
    grid = [[None]*21 for _ in range(21)]

    for row in range(21):
        for col in range(21):
            # Center of cell
            cx = int(grid_left + (col + 0.5) * cell_w)
            cy = int(grid_top + (row + 0.5) * cell_h)

            # Sample a small area around center (5x5 pixels)
            total_brightness = 0
            count = 0
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    px = cx + dx
                    py = cy + dy
                    if 0 <= px < w and 0 <= py < h:
                        r, g, b = pixels[px, py][:3]
                        brightness = (r + g + b) / 3
                        total_brightness += brightness
                        count += 1

            avg_brightness = total_brightness / count if count > 0 else 128

            # Black cells have low brightness, white cells have high
            # Threshold: below 100 = black, above = white
            grid[row][col] = 'W' if avg_brightness > 100 else 'B'

    return grid

def refine_grid_bounds(img_path):
    """More carefully find the grid boundaries by scanning for line patterns."""
    if not HAS_PIL:
        return None

    img = Image.open(img_path)
    pixels = img.load()
    w, h = img.size

    # Scan horizontally at various y positions to find vertical grid lines
    # Grid lines are thin dark lines at regular intervals

    # First, find approximate y position of grid (scan middle of expected area)
    test_y = int(h * 0.4)  # Middle of expected grid area

    # Scan for dark pixels (grid lines) across the row
    dark_cols = []
    for x in range(int(w*0.3), int(w*0.95)):
        r, g, b = pixels[x, test_y][:3]
        if (r + g + b) / 3 < 80:
            dark_cols.append(x)

    if not dark_cols:
        print("Could not find grid lines at test y position")
        return None

    # Find clusters of dark columns (grid lines)
    line_positions = []
    if dark_cols:
        cluster_start = dark_cols[0]
        prev = dark_cols[0]
        for x in dark_cols[1:]:
            if x - prev > 3:
                line_positions.append((cluster_start + prev) // 2)
                cluster_start = x
            prev = x
        line_positions.append((cluster_start + prev) // 2)

    print(f"Found {len(line_positions)} vertical line positions at y={test_y}")
    if len(line_positions) >= 22:
        # Should have 22 vertical lines for 21 columns
        grid_left = line_positions[0]
        grid_right = line_positions[21] if len(line_positions) > 21 else line_positions[-1]
        print(f"Grid x-range: {grid_left} to {grid_right}")

        # Now find horizontal lines
        test_x = (grid_left + grid_right) // 2
        dark_rows = []
        for y in range(int(h*0.02), int(h*0.80)):
            r, g, b = pixels[test_x, y][:3]
            if (r + g + b) / 3 < 80:
                dark_rows.append(y)

        hline_positions = []
        if dark_rows:
            cluster_start = dark_rows[0]
            prev = dark_rows[0]
            for y in dark_rows[1:]:
                if y - prev > 3:
                    hline_positions.append((cluster_start + prev) // 2)
                    cluster_start = y
                prev = y
            hline_positions.append((cluster_start + prev) // 2)

        print(f"Found {len(hline_positions)} horizontal line positions at x={test_x}")
        if len(hline_positions) >= 22:
            grid_top = hline_positions[0]
            grid_bottom = hline_positions[21] if len(hline_positions) > 21 else hline_positions[-1]
            print(f"Grid y-range: {grid_top} to {grid_bottom}")

            return {
                'vlines': line_positions[:22],
                'hlines': hline_positions[:22],
                'left': grid_left,
                'right': grid_right,
                'top': grid_top,
                'bottom': grid_bottom
            }

    return None

def analyze_grid_precise(img_path, bounds):
    """Analyze grid using precise line positions."""
    if not HAS_PIL:
        return None

    img = Image.open(img_path)
    pixels = img.load()
    w, h = img.size

    vlines = bounds['vlines']
    hlines = bounds['hlines']

    grid = [[None]*21 for _ in range(21)]

    for row in range(21):
        for col in range(21):
            # Cell bounds from line positions
            x1 = vlines[col]
            x2 = vlines[col+1] if col+1 < len(vlines) else vlines[col] + (vlines[1] - vlines[0])
            y1 = hlines[row]
            y2 = hlines[row+1] if row+1 < len(hlines) else hlines[row] + (hlines[1] - hlines[0])

            # Sample the center region (inner 50% of cell)
            cx1 = x1 + (x2 - x1) * 3 // 8
            cx2 = x1 + (x2 - x1) * 5 // 8
            cy1 = y1 + (y2 - y1) * 3 // 8
            cy2 = y1 + (y2 - y1) * 5 // 8

            total_brightness = 0
            count = 0
            for px in range(cx1, cx2+1):
                for py in range(cy1, cy2+1):
                    if 0 <= px < w and 0 <= py < h:
                        r, g, b = pixels[px, py][:3]
                        total_brightness += (r + g + b) / 3
                        count += 1

            avg = total_brightness / count if count > 0 else 128
            grid[row][col] = 'W' if avg > 100 else 'B'

    return grid

def number_grid(grid):
    """Apply standard crossword numbering to a grid.
    Returns dict mapping number -> (row, col, is_across, is_down)
    """
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

            # Check if starts an across word
            if (c == 0 or grid[r][c-1] == 'B'):
                # Must have at least one more white cell to the right
                if c + 1 < cols and grid[r][c+1] == 'W':
                    starts_across = True

            # Check if starts a down word
            if (r == 0 or grid[r-1][c] == 'B'):
                # Must have at least one more white cell below
                if r + 1 < rows and grid[r+1][c] == 'W':
                    starts_down = True

            if starts_across or starts_down:
                numbering[num] = (r, c, starts_across, starts_down)
                num += 1

    return numbering

def validate_numbering(numbering):
    """Check if the numbering matches our known across/down lists."""
    computed_across = set()
    computed_down = set()

    for num, (r, c, is_a, is_d) in numbering.items():
        if is_a:
            computed_across.add(num)
        if is_d:
            computed_down.add(num)

    across_match = computed_across == ACROSS_SET
    down_match = computed_down == DOWN_SET

    if not across_match:
        missing_across = ACROSS_SET - computed_across
        extra_across = computed_across - ACROSS_SET
        if missing_across:
            print(f"Missing ACROSS entries: {sorted(missing_across)}")
        if extra_across:
            print(f"Extra ACROSS entries: {sorted(extra_across)}")

    if not down_match:
        missing_down = DOWN_SET - computed_down
        extra_down = computed_down - DOWN_SET
        if missing_down:
            print(f"Missing DOWN entries: {sorted(missing_down)}")
        if extra_down:
            print(f"Extra DOWN entries: {sorted(extra_down)}")

    max_num = max(numbering.keys()) if numbering else 0
    print(f"Total numbered cells: {max_num}")
    print(f"Across entries: {len(computed_across)} (expected {len(ACROSS)})")
    print(f"Down entries: {len(computed_down)} (expected {len(DOWN)})")
    print(f"Across match: {across_match}")
    print(f"Down match: {down_match}")

    return across_match and down_match

def compute_lengths(grid, numbering):
    """Compute the length of each across and down entry."""
    rows = len(grid)
    cols = len(grid[0])

    across_lengths = {}
    down_lengths = {}

    for num, (r, c, is_a, is_d) in numbering.items():
        if is_a:
            # Count white cells to the right
            length = 0
            cc = c
            while cc < cols and grid[r][cc] == 'W':
                length += 1
                cc += 1
            across_lengths[num] = length

        if is_d:
            # Count white cells downward
            length = 0
            rr = r
            while rr < rows and grid[rr][c] == 'W':
                length += 1
                rr += 1
            down_lengths[num] = length

    return across_lengths, down_lengths

def print_grid(grid):
    """Print the grid in a readable format."""
    for row in grid:
        line = ""
        for cell in row:
            if cell == 'B':
                line += "██"
            else:
                line += "░░"
        print(line)

def main():
    pdf_path = "/home/user/MB/puzzles/Million-Dollar-Crossword.pdf"

    # Step 1: Extract image from PDF
    print("=" * 60)
    print("Step 1: Extracting grid image from PDF")
    print("=" * 60)

    result = extract_grid_from_pdf(pdf_path)
    if result is None:
        print("Failed to extract image from PDF")
        return

    img_path, pix = result

    # Step 2: Find precise grid bounds
    print("\n" + "=" * 60)
    print("Step 2: Finding grid boundaries")
    print("=" * 60)

    bounds = refine_grid_bounds(img_path)

    if bounds:
        print(f"\nVertical lines: {bounds['vlines'][:5]}...{bounds['vlines'][-2:]}")
        print(f"Horizontal lines: {bounds['hlines'][:5]}...{bounds['hlines'][-2:]}")

        # Step 3: Analyze cells
        print("\n" + "=" * 60)
        print("Step 3: Analyzing cells")
        print("=" * 60)

        grid = analyze_grid_precise(img_path, bounds)
    else:
        print("Using approximate bounds...")
        grid = analyze_grid_image(img_path)

    if grid is None:
        print("Failed to analyze grid")
        return

    # Print the detected grid
    print("\nDetected grid pattern:")
    print_grid(grid)

    # Count black cells
    black_count = sum(1 for r in grid for c in r if c == 'B')
    white_count = sum(1 for r in grid for c in r if c == 'W')
    print(f"\nBlack cells: {black_count}, White cells: {white_count}")

    # Step 4: Number the grid
    print("\n" + "=" * 60)
    print("Step 4: Numbering the grid")
    print("=" * 60)

    numbering = number_grid(grid)

    # Step 5: Validate
    print("\n" + "=" * 60)
    print("Step 5: Validating against known entry lists")
    print("=" * 60)

    valid = validate_numbering(numbering)

    # Step 6: Compute lengths
    print("\n" + "=" * 60)
    print("Step 6: Computing entry lengths")
    print("=" * 60)

    across_lengths, down_lengths = compute_lengths(grid, numbering)

    print("\nACROSS entries:")
    for num in sorted(across_lengths.keys()):
        r, c = numbering[num][0], numbering[num][1]
        print(f"  {num:3d}A: length {across_lengths[num]:2d}  (row {r+1}, col {c+1})")

    print("\nDOWN entries:")
    for num in sorted(down_lengths.keys()):
        r, c = numbering[num][0], numbering[num][1]
        print(f"  {num:3d}D: length {down_lengths[num]:2d}  (row {r+1}, col {c+1})")

    # Save results
    results = {
        'grid': grid,
        'numbering': {str(k): list(v) for k, v in numbering.items()},
        'across_lengths': across_lengths,
        'down_lengths': down_lengths,
        'valid': valid
    }

    with open('/home/user/MB/analysis/grid_data.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to /home/user/MB/analysis/grid_data.json")
    print(f"Validation: {'PASSED' if valid else 'FAILED'}")

    return grid, numbering, across_lengths, down_lengths, valid

if __name__ == '__main__':
    main()
