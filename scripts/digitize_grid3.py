#!/usr/bin/env python3
"""
Digitize the 21x21 crossword grid - Phase 3: Full extraction.
Uses both low-res and hi-res images.
"""

import numpy as np
from PIL import Image
import json

# =============================================================================
# KNOWN ENTRY LISTS (from PDF)
# =============================================================================
ACROSS = [1,8,14,22,23,24,25,28,29,30,31,32,34,35,36,38,41,42,43,45,47,48,
          50,54,57,58,59,61,63,64,66,68,70,72,73,77,79,80,81,82,83,85,88,90,
          91,92,94,97,99,100,102,103,105,106,107,109,111,113,114,117,119,120,
          121,123,124,127,129,132,134,136,138,141,143,145,148,153,155,156,158,
          159,161,164,165,167,171,172,173,174,175,176]

DOWN = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,26,27,33,
        37,39,40,43,44,46,49,51,52,53,55,56,60,62,65,67,69,71,72,74,75,76,
        77,78,80,83,84,86,87,89,93,95,96,98,101,104,108,110,112,115,116,117,
        118,122,124,125,126,128,130,131,133,135,137,139,140,141,142,144,150,
        151,152,154,157,160,162,163,166,168,169,170]

ACROSS_SET = set(ACROSS)
DOWN_SET = set(DOWN)

# =============================================================================
# GRID LINE POSITIONS (from Phase 2 analysis)
# =============================================================================
# In the low-res (1200x1553) image:
# 22 horizontal lines with ~25.6px spacing
hlines_lr = [99, 125, 151, 176, 202, 227, 253, 279, 304, 330, 355, 381,
             406, 432, 458, 483, 509, 534, 560, 585, 611, 637]
# 22 vertical lines with ~25.6px spacing
vlines_lr = [521, 547, 572, 598, 623, 649, 675, 700, 726, 751, 777, 803,
             828, 854, 879, 905, 930, 956, 981, 1007, 1033, 1058]

print(f"Grid in low-res: x=[{vlines_lr[0]},{vlines_lr[-1]}] y=[{hlines_lr[0]},{hlines_lr[-1]}]")
print(f"Cell size: ~{(vlines_lr[-1]-vlines_lr[0])/21:.1f} x {(hlines_lr[-1]-hlines_lr[0])/21:.1f} pixels")

# Scale to hi-res (5100x6600 from 1200x1553)
scale_x = 5100 / 1200
scale_y = 6600 / 1553
print(f"Scale factors: x={scale_x:.3f} y={scale_y:.3f}")

hlines_hr = [int(y * scale_y) for y in hlines_lr]
vlines_hr = [int(x * scale_x) for x in vlines_lr]
print(f"Grid in hi-res: x=[{vlines_hr[0]},{vlines_hr[-1]}] y=[{hlines_hr[0]},{hlines_hr[-1]}]")
print(f"Cell size hi-res: ~{(vlines_hr[-1]-vlines_hr[0])/21:.1f} x {(hlines_hr[-1]-hlines_hr[0])/21:.1f} pixels")

# =============================================================================
# EXTRACT CELL DATA FROM HI-RES IMAGE
# =============================================================================
print("\nLoading hi-res image...")
img_hr = Image.open('/tmp/crossword_hires-1.png')
pix_hr = np.array(img_hr)
h_img, w_img = pix_hr.shape[:2]
gray_hr = np.mean(pix_hr[:,:,:3], axis=2)
print(f"Hi-res loaded: {w_img}x{h_img}")

# Also load low-res for comparison
img_lr = Image.open('/tmp/pdf_image_15.png')
pix_lr = np.array(img_lr)
gray_lr = np.mean(pix_lr[:,:,:3], axis=2)

# =============================================================================
# CLASSIFY EACH CELL
# =============================================================================
print("\n" + "="*70)
print("Classifying cells...")
print("="*70)

grid = [[None]*21 for _ in range(21)]
cell_brightness = [[0]*21 for _ in range(21)]
cell_dark_fraction = [[0]*21 for _ in range(21)]

for row in range(21):
    for col in range(21):
        # Cell boundaries in hi-res
        x1 = vlines_hr[col]
        x2 = vlines_hr[col + 1]
        y1 = hlines_hr[row]
        y2 = hlines_hr[row + 1]

        cell_w = x2 - x1
        cell_h = y2 - y1

        # Sample the INNER portion of the cell (avoid grid lines on edges)
        # Use inner 60% to avoid grid lines
        margin_x = int(cell_w * 0.20)
        margin_y = int(cell_h * 0.20)

        inner_x1 = x1 + margin_x
        inner_x2 = x2 - margin_x
        inner_y1 = y1 + margin_y
        inner_y2 = y2 - margin_y

        # Clamp
        inner_x1 = max(0, min(inner_x1, w_img-1))
        inner_x2 = max(0, min(inner_x2, w_img-1))
        inner_y1 = max(0, min(inner_y1, h_img-1))
        inner_y2 = max(0, min(inner_y2, h_img-1))

        # Extract inner cell region
        region = gray_hr[inner_y1:inner_y2, inner_x1:inner_x2]
        if region.size == 0:
            grid[row][col] = 'W'
            continue

        avg_brightness = np.mean(region)
        # Fraction of very dark pixels (< 30)
        dark_frac = np.mean(region < 30)

        cell_brightness[row][col] = avg_brightness
        cell_dark_fraction[row][col] = dark_frac

        # Classification:
        # - BLACK cells: mostly dark (dark_frac > 0.7 or avg_brightness < 50)
        # - WHITE cells: mostly bright (avg_brightness > 200)
        # - Cells with numbers or circles will still be mostly white

        if dark_frac > 0.6 or avg_brightness < 60:
            grid[row][col] = 'B'
        else:
            grid[row][col] = 'W'

# Print initial grid
print("\nInitial grid extraction:")
for row in range(21):
    line = ""
    for col in range(21):
        if grid[row][col] == 'B':
            line += "##"
        else:
            line += ".."
    print(f"  Row {row+1:2d}: {line}")

# Count
black_count = sum(1 for r in range(21) for c in range(21) if grid[r][c] == 'B')
white_count = 21*21 - black_count
print(f"\nBlack: {black_count}, White: {white_count}")

# =============================================================================
# ALSO EXTRACT FROM LOW-RES IMAGE FOR COMPARISON
# =============================================================================
print("\n" + "="*70)
print("Classifying cells from low-res image...")
print("="*70)

grid_lr = [[None]*21 for _ in range(21)]

for row in range(21):
    for col in range(21):
        x1 = vlines_lr[col]
        x2 = vlines_lr[col + 1]
        y1 = hlines_lr[row]
        y2 = hlines_lr[row + 1]

        cell_w = x2 - x1
        cell_h = y2 - y1

        # In low-res, cells are ~25 pixels. Use inner 50%
        margin_x = int(cell_w * 0.25)
        margin_y = int(cell_h * 0.25)

        inner_x1 = x1 + margin_x
        inner_x2 = x2 - margin_x
        inner_y1 = y1 + margin_y
        inner_y2 = y2 - margin_y

        h_lr_img, w_lr_img = gray_lr.shape
        inner_x1 = max(0, min(inner_x1, w_lr_img-1))
        inner_x2 = max(0, min(inner_x2, w_lr_img-1))
        inner_y1 = max(0, min(inner_y1, h_lr_img-1))
        inner_y2 = max(0, min(inner_y2, h_lr_img-1))

        region = gray_lr[inner_y1:inner_y2, inner_x1:inner_x2]
        if region.size == 0:
            grid_lr[row][col] = 'W'
            continue

        avg = np.mean(region)
        dark_frac = np.mean(region < 30)

        if dark_frac > 0.5 or avg < 80:
            grid_lr[row][col] = 'B'
        else:
            grid_lr[row][col] = 'W'

print("\nLow-res grid:")
for row in range(21):
    line = ""
    for col in range(21):
        if grid_lr[row][col] == 'B':
            line += "##"
        else:
            line += ".."
    print(f"  Row {row+1:2d}: {line}")

# Compare
mismatches = []
for r in range(21):
    for c in range(21):
        if grid[r][c] != grid_lr[r][c]:
            mismatches.append((r, c, grid[r][c], grid_lr[r][c]))

print(f"\nMismatches between hi-res and low-res: {len(mismatches)}")
for r, c, hr_val, lr_val in mismatches:
    print(f"  ({r+1},{c+1}): hi-res={hr_val}, low-res={lr_val}, "
          f"brightness={cell_brightness[r][c]:.0f}, dark_frac={cell_dark_fraction[r][c]:.2f}")

# =============================================================================
# NUMBER THE GRID AND VALIDATE
# =============================================================================
print("\n" + "="*70)
print("Numbering grid and validating...")
print("="*70)

def number_grid(g):
    """Apply standard crossword numbering."""
    numbering = {}
    num = 1
    for r in range(21):
        for c in range(21):
            if g[r][c] == 'B':
                continue
            starts_across = False
            starts_down = False

            # Starts across?
            if (c == 0 or g[r][c-1] == 'B'):
                if c + 1 < 21 and g[r][c+1] != 'B':
                    starts_across = True

            # Starts down?
            if (r == 0 or g[r-1][c] == 'B'):
                if r + 1 < 21 and g[r+1][c] != 'B':
                    starts_down = True

            if starts_across or starts_down:
                numbering[num] = (r, c, starts_across, starts_down)
                num += 1
    return numbering

def validate(numbering):
    """Check against known entry lists."""
    computed_across = set()
    computed_down = set()
    for num, (r, c, is_a, is_d) in numbering.items():
        if is_a: computed_across.add(num)
        if is_d: computed_down.add(num)

    missing_a = ACROSS_SET - computed_across
    extra_a = computed_across - ACROSS_SET
    missing_d = DOWN_SET - computed_down
    extra_d = computed_down - DOWN_SET

    max_num = max(numbering.keys()) if numbering else 0
    print(f"Total numbered cells: {max_num}")
    print(f"Across: {len(computed_across)} computed vs {len(ACROSS)} expected")
    print(f"Down: {len(computed_down)} computed vs {len(DOWN)} expected")

    if missing_a:
        print(f"MISSING from Across: {sorted(missing_a)}")
    if extra_a:
        print(f"EXTRA in Across: {sorted(extra_a)}")
    if missing_d:
        print(f"MISSING from Down: {sorted(missing_d)}")
    if extra_d:
        print(f"EXTRA in Down: {sorted(extra_d)}")

    match = (computed_across == ACROSS_SET and computed_down == DOWN_SET)
    print(f"MATCH: {match}")
    return match, computed_across, computed_down

# Validate hi-res grid
print("\n--- Hi-res grid validation ---")
numbering = number_grid(grid)
match, ca, cd = validate(numbering)

# Validate low-res grid
print("\n--- Low-res grid validation ---")
numbering_lr = number_grid(grid_lr)
match_lr, ca_lr, cd_lr = validate(numbering_lr)

# =============================================================================
# PRINT DETAILED CELL BRIGHTNESS FOR DEBUGGING
# =============================================================================
print("\n" + "="*70)
print("Cell brightness map (hi-res, avg brightness):")
print("="*70)
header = "     " + "".join(f"{c+1:5d}" for c in range(21))
print(header)
for row in range(21):
    line = f"R{row+1:2d}: "
    for col in range(21):
        b = cell_brightness[row][col]
        if grid[row][col] == 'B':
            line += f" [B] "
        else:
            line += f"{b:5.0f}"
    print(line)

print("\n" + "="*70)
print("Cell dark fraction map:")
print("="*70)
print(header)
for row in range(21):
    line = f"R{row+1:2d}: "
    for col in range(21):
        d = cell_dark_fraction[row][col]
        if grid[row][col] == 'B':
            line += f" [B] "
        else:
            line += f"{d:5.2f}"
    print(line)

# Print the grid with numbers
print("\n" + "="*70)
print("Grid with entry numbers:")
print("="*70)
num_grid = [['']*21 for _ in range(21)]
for num, (r, c, is_a, is_d) in numbering.items():
    num_grid[r][c] = str(num)

for row in range(21):
    line = ""
    for col in range(21):
        if grid[row][col] == 'B':
            line += " ### "
        elif num_grid[row][col]:
            line += f"{num_grid[row][col]:>4s} "
        else:
            line += "   . "
    print(f"  {line}")
