#!/usr/bin/env python3
"""
Digitize the 21x21 crossword grid from the high-resolution image.
Combines pixel-based extraction with constraint-based verification.
"""

import numpy as np
from PIL import Image
import json
import sys

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
ALL_NUMBERS = sorted(ACROSS_SET | DOWN_SET)

print(f"Known across entries: {len(ACROSS)}")
print(f"Known down entries: {len(DOWN)}")
print(f"Unique numbered cells in lists: {len(ALL_NUMBERS)}")
print(f"Max entry number: {max(ALL_NUMBERS)}")

# Check which numbers 1-176 are missing from both lists
missing = set(range(1, 177)) - ACROSS_SET - DOWN_SET
print(f"Numbers 1-176 NOT in either list: {sorted(missing)}")

# =============================================================================
# STEP 1: PIXEL-BASED GRID EXTRACTION
# =============================================================================
print("\n" + "="*70)
print("STEP 1: Pixel-based grid extraction from hi-res image")
print("="*70)

# Load the high-resolution image
img = Image.open('/tmp/crossword_hires-1.png')
pixels = np.array(img)
h, w = pixels.shape[:2]
print(f"Hi-res image size: {w} x {h}")

# Convert to grayscale for analysis
gray = np.mean(pixels[:,:,:3], axis=2)

# Strategy: Find the grid by detecting the regular pattern of grid lines
# Grid lines are thin dark lines. We scan for vertical lines in a horizontal strip
# and horizontal lines in a vertical strip.

# First, let's find the approximate grid area.
# From visual inspection, the grid is in the right portion of the image.
# Let's scan for dark vertical lines in the middle of the expected grid area.

# The image is 5100x6600. The grid appears to start at about x~2100 and
# extend to about x~4750, y from about y~350 to y~3800.

# Scan for vertical grid lines at a test y position (middle of grid)
test_y = h // 3  # approximately middle of grid area
print(f"Scanning for vertical grid lines at y={test_y}")

# Look at a horizontal strip
strip_h = gray[test_y-5:test_y+5, :].mean(axis=0)

# Find positions where brightness drops significantly (potential grid lines or black cells)
# Grid lines are thin (~2-4 pixels), black cells are wider (~100+ pixels)
# We need to distinguish between them

# Let's scan more carefully - find all runs of dark pixels
dark_threshold = 100  # pixels darker than this are "dark"
dark_mask = strip_h < dark_threshold

# Find transitions
transitions = []
in_dark = False
start = 0
for x in range(len(dark_mask)):
    if dark_mask[x] and not in_dark:
        start = x
        in_dark = True
    elif not dark_mask[x] and in_dark:
        transitions.append((start, x, x - start))
        in_dark = False
if in_dark:
    transitions.append((start, len(dark_mask), len(dark_mask) - start))

# Grid lines should be very thin (1-6 pixels in hi-res), black cells should be wide (~100+ pixels)
thin_lines = [(s, e, w_) for s, e, w_ in transitions if w_ <= 15]
wide_blocks = [(s, e, w_) for s, e, w_ in transitions if w_ > 15]

print(f"Found {len(thin_lines)} thin dark features and {len(wide_blocks)} wide dark features at y={test_y}")

# Let's try a different approach: scan multiple y positions and find consistent vertical lines
# Also, let's use the low-res image which the user says has clearer grid lines

print("\nSwitching to low-res image for clearer grid line detection...")
img_lr = Image.open('/tmp/pdf_image_15.png')
pixels_lr = np.array(img_lr)
h_lr, w_lr = pixels_lr.shape[:2]
gray_lr = np.mean(pixels_lr[:,:,:3], axis=2)
print(f"Low-res image size: {w_lr} x {h_lr}")

# User says: horizontal grid lines at approximately y = 75 + 25.5*n (in low-res)
# So vertical lines should be at similar spacing.
# Let's verify by looking at the image.

# The grid in the low-res occupies roughly the right 60% of the image
# Grid starts at about x=475 in the low-res
# Let's find the exact grid boundaries

# Scan for vertical lines at multiple y positions
y_positions = [int(75 + 25.5 * 10), int(75 + 25.5 * 15)]  # middle rows
all_vlines = []

for test_y_lr in y_positions:
    if test_y_lr >= h_lr:
        continue
    strip = gray_lr[test_y_lr, :]

    # Find dark pixels
    dark = strip < 140

    # Find dark run starts
    runs = []
    in_dark = False
    start = 0
    for x in range(len(dark)):
        if dark[x] and not in_dark:
            start = x
            in_dark = True
        elif not dark[x] and in_dark:
            runs.append((start, x))
            in_dark = False
    if in_dark:
        runs.append((start, len(dark)))

    # Thin runs are grid lines (width 1-3 in low-res)
    thin = [(s, e) for s, e in runs if e - s <= 5]
    all_vlines.append(thin)

print(f"Vertical line candidates at different y positions: {[len(v) for v in all_vlines]}")

# Let's use a more robust approach: look at the image column averages to find grid lines
# Grid lines are columns that are consistently dark across the grid height range

# Expected grid y range in low-res: y=75 to y=75+25.5*21 ≈ 610
y_start_lr = 70
y_end_lr = 620

# Average brightness of each column in the grid y range
col_avg = gray_lr[y_start_lr:y_end_lr, :].mean(axis=0)

# Find local minima (dark columns = potential grid lines)
# But black cells also create dark columns, so we need to be smarter

# Instead, let's look at row averages to find horizontal grid lines
row_avg = gray_lr[:, 470:850].mean(axis=1)  # approximate grid x range

# Find rows that are darker than neighbors (grid lines)
# Grid lines should be at regular intervals of ~25.5 pixels
dark_rows_lr = []
for y in range(50, 650):
    # A grid line row should be dark and its neighbors lighter
    if row_avg[y] < 200 and row_avg[y] < row_avg[max(0,y-3)] - 5 and row_avg[y] < row_avg[min(len(row_avg)-1,y+3)] - 5:
        dark_rows_lr.append(y)

# Cluster the dark rows
hline_clusters = []
if dark_rows_lr:
    cluster = [dark_rows_lr[0]]
    for y in dark_rows_lr[1:]:
        if y - cluster[-1] <= 3:
            cluster.append(y)
        else:
            hline_clusters.append(int(np.mean(cluster)))
            cluster = [y]
    hline_clusters.append(int(np.mean(cluster)))

print(f"\nFound {len(hline_clusters)} horizontal grid line candidates in low-res")
if len(hline_clusters) >= 10:
    print(f"First few: {hline_clusters[:5]}")
    print(f"Last few: {hline_clusters[-5:]}")
    # Compute spacing
    spacings = [hline_clusters[i+1] - hline_clusters[i] for i in range(len(hline_clusters)-1)]
    print(f"Spacings: {spacings[:10]}...")

# Let's try a cleaner approach using the known formula
# User says: y = 75 + 25.5*n for row boundaries in low-res
# That means 22 horizontal lines at n=0,1,...,21
# y values: 75, 100.5, 126, 151.5, 177, 202.5, 228, 253.5, 279, 304.5, 330, 355.5, 381, 406.5, 432, 457.5, 483, 508.5, 534, 559.5, 585, 610.5

hlines_lr = [75 + 25.5 * n for n in range(22)]
print(f"\nUsing formula y=75+25.5*n for horizontal lines:")
print(f"  Lines: {[f'{y:.1f}' for y in hlines_lr]}")

# Now we need to find the vertical grid lines similarly
# Let's check what x range the grid occupies
# Looking at column averages at a known grid line y position
y_test = int(hlines_lr[0])  # first grid line
strip_at_top = gray_lr[y_test-1:y_test+2, :].mean(axis=0)

# Find dark positions in this strip (should be grid lines and the top border)
dark_cols_at_top = np.where(strip_at_top < 180)[0]
print(f"\nDark columns at top grid line (y≈{y_test}): found {len(dark_cols_at_top)} dark pixels")
if len(dark_cols_at_top) > 0:
    print(f"  Range: x={dark_cols_at_top[0]} to x={dark_cols_at_top[-1]}")

# Let's look at column averages across all grid rows to find consistent vertical lines
# Average each column across all 22 grid line y positions
vline_signal = np.zeros(w_lr)
for yl in hlines_lr:
    yi = int(round(yl))
    if yi-1 >= 0 and yi+2 < h_lr:
        vline_signal += gray_lr[yi-1:yi+2, :].mean(axis=0)
vline_signal /= len(hlines_lr)

# The vertical grid lines should show as consistently dark columns
# Let's find minima
v_dark = np.where(vline_signal < 200)[0]
if len(v_dark) > 0:
    # Cluster
    vline_clusters = []
    cluster = [v_dark[0]]
    for x in v_dark[1:]:
        if x - cluster[-1] <= 3:
            cluster.append(x)
        else:
            vline_clusters.append(int(np.mean(cluster)))
            cluster = [x]
    vline_clusters.append(int(np.mean(cluster)))

    print(f"\nFound {len(vline_clusters)} vertical grid line candidates")
    print(f"  Positions: {vline_clusters}")

    if len(vline_clusters) >= 22:
        # Take the 22 that form the most regular spacing
        # Try to find 22 lines with spacing close to 25.5
        # Start from the first reasonable position
        vlines_lr = vline_clusters[:22]
        v_spacings = [vlines_lr[i+1] - vlines_lr[i] for i in range(len(vlines_lr)-1)]
        print(f"  Spacings: {v_spacings}")

# Let me try another approach - directly sample cell centers in the low-res image
# Using the known grid line formula
print("\n" + "="*70)
print("STEP 2: Sampling cell centers using grid line formula")
print("="*70)

# We need to find the x-positions of vertical grid lines
# From the image, the grid appears to start at about x=475 in low-res
# Let's try: x = x_start + 25.5*n
# We need to find x_start

# Look at several known rows and find where black cells create dark regions
# Row 1 should have black cells at specific positions

# Let me scan the first row (between hlines_lr[0] and hlines_lr[1])
y_row1_center = int((hlines_lr[0] + hlines_lr[1]) / 2)
row1_strip = gray_lr[y_row1_center, :]

# The first row has numbers 1-21 visible in the image, with 2 black cells
# From visual inspection, black cells appear to be at columns 8 and 12 (0-indexed 7 and 11)
# Let me find the grid x range by looking for the first and last cell content

# Actually let me just scan across and find the grid region
# The grid should have alternating white cells and some black cells
# The left border of the grid is a vertical line

# Look at the bottom of the grid too to find vertical lines more reliably
y_bottom = int(hlines_lr[21])
bottom_strip = gray_lr[y_bottom-1:y_bottom+2, :].mean(axis=0)
dark_at_bottom = np.where(bottom_strip < 180)[0]
if len(dark_at_bottom) > 0:
    print(f"Dark columns at bottom grid line: x={dark_at_bottom[0]} to x={dark_at_bottom[-1]}")

# Let's try finding x_start by looking at the middle of the grid where most cells are white
# At middle row, scan for the grid borders
y_mid = int(hlines_lr[10])  # middle row line
mid_strip = gray_lr[y_mid-1:y_mid+2, :].mean(axis=0)
dark_at_mid = np.where(mid_strip < 180)[0]

if len(dark_at_mid) > 0:
    # Cluster these
    mid_clusters = []
    cluster = [dark_at_mid[0]]
    for x in dark_at_mid[1:]:
        if x - cluster[-1] <= 3:
            cluster.append(x)
        else:
            mid_clusters.append(int(np.mean(cluster)))
            cluster = [x]
    mid_clusters.append(int(np.mean(cluster)))

    print(f"\nVertical lines at middle grid row: {len(mid_clusters)} found")
    print(f"  Positions: {mid_clusters}")

# I'll try to determine x_start empirically
# Let me sample brightness at y_row1_center for various x_start values
# and see which gives the best match for black cells at the right positions

# From the image, row 1 clearly has two black cells. Let me identify them by
# scanning the first row's brightness profile
print(f"\nRow 1 brightness profile (y={y_row1_center}):")
# Print brightness every ~25 pixels starting from x=470
for x in range(470, 850, 3):
    b = gray_lr[y_row1_center, x] if x < w_lr else 0
    if b < 50:
        marker = "BLACK"
    elif b < 150:
        marker = "gray"
    elif b > 230:
        marker = "WHITE"
    else:
        marker = "?"
    if b < 50 or (x % 25 < 3):
        print(f"  x={x}: brightness={b:.0f} {marker}")
