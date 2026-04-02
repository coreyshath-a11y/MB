#!/usr/bin/env python3
"""
Digitize the 21x21 crossword grid - Phase 2: Better grid line detection.
Grid lines are LIGHT GRAY (~126-180), not black.
Black cells are truly black (~0-10).
"""

import numpy as np
from PIL import Image
import json

# Load the low-res image (clearer grid lines per user)
img = Image.open('/tmp/pdf_image_15.png')
pixels = np.array(img)
h, w = pixels.shape[:2]
gray = np.mean(pixels[:,:,:3], axis=2)
print(f"Low-res image: {w}x{h}")

# =============================================================================
# FIND GRID BOUNDARIES
# =============================================================================
# Strategy: The grid area is where we find the dense pattern of grid lines.
# Grid lines are gray (~126-180). Black cells are very dark (~0-10).
# White cells are very bright (~250-255).
# Let's look for regions that have pixels in the gray range (grid lines).

# First, let's look at what brightness values exist in the image
print("\nBrightness histogram (sampled):")
for threshold in [10, 50, 100, 130, 150, 180, 200, 230, 250]:
    count = np.sum(gray < threshold)
    pct = 100 * count / gray.size
    print(f"  Pixels < {threshold}: {count} ({pct:.1f}%)")

# Let's look at the brightness profile of a horizontal line through the grid area
# The grid should be in the upper-right quadrant of the image
# Let me sample at y=300 (middle of what should be grid)
y_test = 300
row_profile = gray[y_test, :]
print(f"\nBrightness at y={y_test} (selected x positions):")
for x in range(400, 1200, 20):
    b = row_profile[x]
    label = ""
    if b < 15: label = " <<< BLACK CELL"
    elif b < 190: label = " <<< GRAY (grid line?)"
    elif b > 240: label = ""
    if b < 190 or x % 100 == 0:
        print(f"  x={x:4d}: {b:.0f}{label}")

# Let's create a "grid line detector" - pixels that are in the gray range
# (not black/dark like black cells, and not white like cell interiors)
# Grid lines: ~126-200 range
gridline_mask = (gray > 100) & (gray < 210)

# Let's look at row sums of this mask across different x ranges
print("\n\nSearching for grid region...")
# Column sums within y range 50-650 (expected grid area)
col_sums = gridline_mask[50:650, :].sum(axis=0)
# The grid columns will have high sums (grid lines are consistently gray)
# Find the range with high column sums
print("Column sums of gray pixels (y=50-650):")
for x in range(0, w, 50):
    if x < w:
        s = col_sums[x]
        if s > 20:
            print(f"  x={x}: {s}")

# Now let's try to find the grid more precisely by looking at the actual image
# Let me scan for vertical lines of gray pixels
print("\n\nSearching for vertical grid lines (columns with many gray pixels)...")
# For each column, count gray pixels in the expected y range
vline_scores = []
for x in range(w):
    count = 0
    for y in range(70, 620):
        if 100 < gray[y, x] < 210:
            count += 1
    vline_scores.append(count)

vline_scores = np.array(vline_scores)
# Find peaks (columns with many gray pixels)
threshold = np.max(vline_scores) * 0.3
vline_candidates = np.where(vline_scores > threshold)[0]
print(f"Columns with gray score > {threshold:.0f}: {len(vline_candidates)}")
if len(vline_candidates) > 0:
    print(f"  Range: x={vline_candidates[0]} to x={vline_candidates[-1]}")
    # Cluster them
    clusters = []
    cluster = [vline_candidates[0]]
    for x in vline_candidates[1:]:
        if x - cluster[-1] <= 3:
            cluster.append(x)
        else:
            clusters.append(int(np.mean(cluster)))
            cluster = [x]
    clusters.append(int(np.mean(cluster)))
    print(f"  {len(clusters)} distinct vertical lines: {clusters}")

# Now let's do the same for horizontal lines
print("\n\nSearching for horizontal grid lines (rows with many gray pixels)...")
hline_scores = []
for y in range(h):
    count = 0
    for x in range(400, 1180):  # approximate grid x range
        if 100 < gray[y, x] < 210:
            count += 1
    hline_scores.append(count)

hline_scores = np.array(hline_scores)
threshold_h = np.max(hline_scores) * 0.3
hline_candidates = np.where(hline_scores > threshold_h)[0]
print(f"Rows with gray score > {threshold_h:.0f}: {len(hline_candidates)}")
if len(hline_candidates) > 0:
    print(f"  Range: y={hline_candidates[0]} to y={hline_candidates[-1]}")
    clusters_h = []
    cluster = [hline_candidates[0]]
    for y in hline_candidates[1:]:
        if y - cluster[-1] <= 3:
            cluster.append(y)
        else:
            clusters_h.append(int(np.mean(cluster)))
            cluster = [y]
    clusters_h.append(int(np.mean(cluster)))
    print(f"  {len(clusters_h)} distinct horizontal lines: {clusters_h}")

# Let's also just look at the raw brightness along a column to understand the grid
# Pick a column in the middle of the expected grid
test_col = 700
print(f"\n\nBrightness along column x={test_col}:")
for y in range(50, 650, 5):
    b = gray[y, test_col]
    label = ""
    if b < 15: label = " <<< BLACK"
    elif b < 200: label = " <<< GRAY"
    if b < 200:
        print(f"  y={y}: {b:.0f}{label}")

# Let's also look at what the ACTUAL grid lines look like at higher precision
# Zoom into a small area where we expect a grid line
print(f"\n\nDetailed brightness at y=75-85, x=700:")
for y in range(70, 90):
    b = gray[y, 700]
    print(f"  y={y}: {b:.0f}")
