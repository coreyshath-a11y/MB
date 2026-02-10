#!/usr/bin/env python3
"""
Digitize grid - Phase 5: Efficient black cell detection using find_objects.
"""

import numpy as np
from PIL import Image
from scipy import ndimage

# Load hi-res image
print("Loading hi-res image...")
img = Image.open('/tmp/crossword_hires-1.png')
pixels = np.array(img)
h, w = pixels.shape[:2]
gray = np.mean(pixels[:,:,:3], axis=2).astype(np.float32)
print(f"Image: {w}x{h}")

# Find large connected black regions
black_mask = gray < 15
labeled, num_features = ndimage.label(black_mask)
print(f"Dark pixel components: {num_features}")

# Use find_objects for efficient bbox extraction
slices = ndimage.find_objects(labeled)
print(f"Extracting component properties...")

components = []
for i, sl in enumerate(slices):
    if sl is None:
        continue
    y_slice, x_slice = sl
    bbox_h = y_slice.stop - y_slice.start
    bbox_w = x_slice.stop - x_slice.start
    area = np.sum(labeled[sl] == (i + 1))

    if area > 3000:  # Only large components (cells are ~108x108=11664)
        cx = (x_slice.start + x_slice.stop) / 2
        cy = (y_slice.start + y_slice.stop) / 2
        components.append({
            'area': area, 'cx': cx, 'cy': cy,
            'x_min': x_slice.start, 'x_max': x_slice.stop,
            'y_min': y_slice.start, 'y_max': y_slice.stop,
            'bbox_w': bbox_w, 'bbox_h': bbox_h
        })

components.sort(key=lambda c: c['area'], reverse=True)
print(f"\nLarge components (area > 3000): {len(components)}")

for i, c in enumerate(components):
    aspect = c['bbox_w'] / max(c['bbox_h'], 1)
    cells_w = c['bbox_w'] / 108  # approximate cells wide
    cells_h = c['bbox_h'] / 108  # approximate cells tall
    print(f"  #{i+1}: area={c['area']:7d} center=({c['cx']:7.1f},{c['cy']:7.1f}) "
          f"bbox={c['bbox_w']:4d}x{c['bbox_h']:4d} ~{cells_w:.1f}x{cells_h:.1f} cells")

# Now let's identify which grid cells are black
# We need to find the grid boundaries first
#
# A single black cell is ~108x108 pixels
# Multiple adjacent black cells merge into larger regions
#
# From the component data, we can estimate grid position

# Let's look at the position distribution
all_x_starts = [c['x_min'] for c in components]
all_y_starts = [c['y_min'] for c in components]

print(f"\nComponent x_min range: {min(all_x_starts)}-{max(all_x_starts)}")
print(f"Component y_min range: {min(all_y_starts)}-{max(all_y_starts)}")

# The grid area should contain most of the black cells
# Let's find grid boundaries from the outermost black cells

all_x_max = max(c['x_max'] for c in components)
all_y_max = max(c['y_max'] for c in components)
print(f"Component x_max range: up to {all_x_max}")
print(f"Component y_max range: up to {all_y_max}")

# Now let's try a different approach to find exact grid lines
# Scan the image for rows/columns that are consistently gray (grid lines)
# Grid lines are thin (~2-4 px in hi-res) and gray (~100-180)

# Focus on the region that likely contains the grid
# From Phase 2: grid is at roughly x=521-1058 in low-res = x=2214-4497 in hi-res
# y=99-637 in low-res = y=421-2707 in hi-res
# But these might be slightly off

# Let's use a more robust method: look for regularly-spaced thin features
# across the expected grid region

# Scan horizontal strips for grid line detection
print("\n" + "="*70)
print("Finding grid lines in hi-res image...")
print("="*70)

# For horizontal grid lines: scan a vertical strip through the grid
# Pick x position in middle of grid
grid_region_x_start = 2200
grid_region_x_end = 4500
grid_region_y_start = 300
grid_region_y_end = 2800

# Average brightness along each row in the grid x-region
x_mid = (grid_region_x_start + grid_region_x_end) // 2

# Look at a narrow vertical strip to find horizontal lines
strip_width = 20
col_strip = gray[grid_region_y_start:grid_region_y_end,
                 x_mid-strip_width:x_mid+strip_width].mean(axis=1)

# Find local minima (dark horizontal lines)
# Grid lines should be thin and regularly spaced
print(f"\nScanning for horizontal grid lines at x≈{x_mid}...")

# Look for dips in brightness
# A grid line is a few pixels where brightness drops
hlines = []
for y in range(2, len(col_strip) - 2):
    # Check if this is a local minimum and sufficiently dark
    if (col_strip[y] < col_strip[y-2] - 10 and
        col_strip[y] < col_strip[y+2] - 10 and
        col_strip[y] < 200):
        # Don't add if too close to previous
        actual_y = y + grid_region_y_start
        if not hlines or actual_y - hlines[-1] > 20:
            hlines.append(actual_y)

print(f"Candidate horizontal lines: {len(hlines)}")
for y in hlines:
    print(f"  y={y} brightness={col_strip[y-grid_region_y_start]:.0f}")

# Check spacings
if len(hlines) > 1:
    spacings = [hlines[i+1] - hlines[i] for i in range(len(hlines)-1)]
    print(f"\nHorizontal line spacings: {spacings}")

# Same for vertical lines
y_mid = (grid_region_y_start + grid_region_y_end) // 2
row_strip = gray[y_mid-strip_width:y_mid+strip_width,
                 grid_region_x_start:grid_region_x_end].mean(axis=0)

print(f"\nScanning for vertical grid lines at y≈{y_mid}...")
vlines = []
for x in range(2, len(row_strip) - 2):
    if (row_strip[x] < row_strip[x-2] - 10 and
        row_strip[x] < row_strip[x+2] - 10 and
        row_strip[x] < 200):
        actual_x = x + grid_region_x_start
        if not vlines or actual_x - vlines[-1] > 20:
            vlines.append(actual_x)

print(f"Candidate vertical lines: {len(vlines)}")
for x in vlines:
    print(f"  x={x} brightness={row_strip[x-grid_region_x_start]:.0f}")

if len(vlines) > 1:
    spacings = [vlines[i+1] - vlines[i] for i in range(len(vlines)-1)]
    print(f"\nVertical line spacings: {spacings}")

# Now, the problem is that grid lines pass through BOTH white cells and black cells.
# Through white cells they're visible as gray; through black cells they're invisible.
# So we might miss some grid lines.
#
# Solution: use multiple scan positions and combine results.
# Also, we can use the detected grid line spacing to infer missing lines.

print("\n" + "="*70)
print("Multi-position grid line detection...")
print("="*70)

# Scan at multiple x positions for horizontal lines
all_hline_candidates = []
for x_test in range(grid_region_x_start + 50, grid_region_x_end - 50, 200):
    strip = gray[grid_region_y_start:grid_region_y_end, x_test]
    for y in range(5, len(strip) - 5):
        # Brightness dip detection
        local_max = max(strip[max(0,y-10):y-2].max() if y > 2 else 255,
                       strip[y+3:min(len(strip),y+11)].max() if y+3 < len(strip) else 255)
        if strip[y] < local_max - 20 and strip[y] < 200:
            actual_y = y + grid_region_y_start
            all_hline_candidates.append(actual_y)

# Histogram of y positions
y_hist = np.zeros(grid_region_y_end + 100)
for y in all_hline_candidates:
    if y < len(y_hist):
        y_hist[y] += 1

# Find peaks in histogram
hline_peaks = []
for y in range(grid_region_y_start, grid_region_y_end):
    if y_hist[y] >= 3:  # detected at multiple x positions
        if not hline_peaks or y - hline_peaks[-1] > 20:
            # Find best position in local window
            window = y_hist[max(0,y-3):y+4]
            best_y = y - 3 + np.argmax(window) if len(window) > 0 else y
            best_y = max(grid_region_y_start, min(grid_region_y_end, best_y))
            if not hline_peaks or best_y - hline_peaks[-1] > 20:
                hline_peaks.append(best_y)

print(f"\nRobust horizontal line candidates: {len(hline_peaks)}")
for y in hline_peaks:
    print(f"  y={y} (histogram count={y_hist[y]:.0f})")

if len(hline_peaks) > 1:
    spacings = [hline_peaks[i+1] - hline_peaks[i] for i in range(len(hline_peaks)-1)]
    print(f"Spacings: {spacings}")
    median_spacing = np.median(spacings)
    print(f"Median spacing: {median_spacing:.1f}")

# Same for vertical
all_vline_candidates = []
for y_test in range(grid_region_y_start + 50, grid_region_y_end - 50, 200):
    strip = gray[y_test, grid_region_x_start:grid_region_x_end]
    for x in range(5, len(strip) - 5):
        local_max = max(strip[max(0,x-10):x-2].max() if x > 2 else 255,
                       strip[x+3:min(len(strip),x+11)].max() if x+3 < len(strip) else 255)
        if strip[x] < local_max - 20 and strip[x] < 200:
            actual_x = x + grid_region_x_start
            all_vline_candidates.append(actual_x)

x_hist = np.zeros(grid_region_x_end + 100)
for x in all_vline_candidates:
    if x < len(x_hist):
        x_hist[x] += 1

vline_peaks = []
for x in range(grid_region_x_start, grid_region_x_end):
    if x_hist[x] >= 3:
        if not vline_peaks or x - vline_peaks[-1] > 20:
            window = x_hist[max(0,x-3):x+4]
            best_x = x - 3 + np.argmax(window) if len(window) > 0 else x
            best_x = max(grid_region_x_start, min(grid_region_x_end, best_x))
            if not vline_peaks or best_x - vline_peaks[-1] > 20:
                vline_peaks.append(best_x)

print(f"\nRobust vertical line candidates: {len(vline_peaks)}")
for x in vline_peaks:
    print(f"  x={x} (histogram count={x_hist[x]:.0f})")

if len(vline_peaks) > 1:
    spacings = [vline_peaks[i+1] - vline_peaks[i] for i in range(len(vline_peaks)-1)]
    print(f"Spacings: {spacings}")
    median_spacing = np.median(spacings)
    print(f"Median spacing: {median_spacing:.1f}")
