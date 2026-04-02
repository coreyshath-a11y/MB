#!/usr/bin/env python3
"""
Digitize grid - Phase 4: Find black cells by connected component analysis,
then refine grid boundaries.
"""

import numpy as np
from PIL import Image

# Load hi-res image
img = Image.open('/tmp/crossword_hires-1.png')
pixels = np.array(img)
h, w = pixels.shape[:2]
gray = np.mean(pixels[:,:,:3], axis=2).astype(np.float32)
print(f"Image: {w}x{h}")

# Create binary mask of very dark pixels (black cell interiors)
black_mask = gray < 20
print(f"Very dark pixels (<20): {np.sum(black_mask)} ({100*np.mean(black_mask):.1f}%)")

# Find bounding boxes of large dark regions (black cells)
# Use simple connected component analysis
from scipy import ndimage

labeled, num_features = ndimage.label(black_mask)
print(f"Connected components of dark pixels: {num_features}")

# Find large components (black cells should be ~108x108 = ~11664 pixels)
# Filter for components with area > 2000 pixels
component_stats = []
for i in range(1, num_features + 1):
    mask = labeled == i
    area = np.sum(mask)
    if area > 2000:
        ys, xs = np.where(mask)
        y_min, y_max = ys.min(), ys.max()
        x_min, x_max = xs.min(), xs.max()
        bbox_w = x_max - x_min
        bbox_h = y_max - y_min
        cx = (x_min + x_max) / 2
        cy = (y_min + y_max) / 2
        component_stats.append({
            'area': area, 'cx': cx, 'cy': cy,
            'x_min': x_min, 'x_max': x_max,
            'y_min': y_min, 'y_max': y_max,
            'bbox_w': bbox_w, 'bbox_h': bbox_h
        })

print(f"\nLarge dark components (area > 2000): {len(component_stats)}")

# Sort by area descending
component_stats.sort(key=lambda c: c['area'], reverse=True)

# Print details
print("\nTop components by area:")
for i, c in enumerate(component_stats[:80]):
    aspect = c['bbox_w'] / max(c['bbox_h'], 1)
    print(f"  #{i+1}: area={c['area']:6d} center=({c['cx']:.0f},{c['cy']:.0f}) "
          f"bbox={c['bbox_w']}x{c['bbox_h']} aspect={aspect:.2f}")

# Filter for roughly square components with size close to a cell (~100x100)
black_cell_candidates = []
for c in component_stats:
    # A black cell should be roughly square and about 80-130 pixels per side
    if (50 < c['bbox_w'] < 200 and 50 < c['bbox_h'] < 200):
        aspect = c['bbox_w'] / max(c['bbox_h'], 1)
        if 0.5 < aspect < 2.0:  # roughly square
            black_cell_candidates.append(c)

print(f"\nBlack cell candidates (roughly square, ~100px): {len(black_cell_candidates)}")
for i, c in enumerate(black_cell_candidates):
    print(f"  #{i+1}: center=({c['cx']:.0f},{c['cy']:.0f}) size={c['bbox_w']}x{c['bbox_h']} area={c['area']}")

# Find grid boundaries from black cell positions
if len(black_cell_candidates) > 5:
    all_cx = [c['cx'] for c in black_cell_candidates]
    all_cy = [c['cy'] for c in black_cell_candidates]

    x_min_cells = min(all_cx)
    x_max_cells = max(all_cx)
    y_min_cells = min(all_cy)
    y_max_cells = max(all_cy)

    print(f"\nBlack cell center range: x=[{x_min_cells:.0f},{x_max_cells:.0f}] y=[{y_min_cells:.0f},{y_max_cells:.0f}]")

    # If black cells span the grid, we can estimate cell size
    # Assuming cells are evenly spaced on a 21x21 grid
    # Cell centers are at: grid_left + (col+0.5)*cell_size, grid_top + (row+0.5)*cell_size

    # Let's cluster the x and y positions
    cx_sorted = sorted(all_cx)
    cy_sorted = sorted(all_cy)

    # Find distinct x positions (cluster within ~cell_size/2)
    def cluster_positions(positions, min_gap=50):
        if not positions:
            return []
        clusters = [[positions[0]]]
        for p in positions[1:]:
            if p - clusters[-1][-1] < min_gap:
                clusters[-1].append(p)
            else:
                clusters.append([p])
        return [np.mean(c) for c in clusters]

    distinct_x = cluster_positions(cx_sorted, 50)
    distinct_y = cluster_positions(cy_sorted, 50)

    print(f"\nDistinct black cell columns: {len(distinct_x)}")
    print(f"  X positions: {[f'{x:.0f}' for x in distinct_x]}")
    print(f"\nDistinct black cell rows: {len(distinct_y)}")
    print(f"  Y positions: {[f'{y:.0f}' for y in distinct_y]}")

    # From the distinct positions, estimate the cell size
    if len(distinct_x) > 1:
        x_diffs = [distinct_x[i+1] - distinct_x[i] for i in range(len(distinct_x)-1)]
        # The cell size should be the GCD of the differences
        # or the minimum difference
        min_x_diff = min(x_diffs)
        print(f"\n  Min x spacing between black cells: {min_x_diff:.1f}")

    if len(distinct_y) > 1:
        y_diffs = [distinct_y[i+1] - distinct_y[i] for i in range(len(distinct_y)-1)]
        min_y_diff = min(y_diffs)
        print(f"  Min y spacing between black cells: {min_y_diff:.1f}")

# Also look for very large dark components (which might be merged adjacent black cells)
print("\n\nLarge dark regions (possible merged black cells):")
merged_candidates = []
for c in component_stats:
    if c['bbox_w'] > 150 or c['bbox_h'] > 150:
        # This might be multiple adjacent black cells merged
        if c['bbox_w'] < 1000 and c['bbox_h'] < 1000:  # Not too large (like text blocks)
            merged_candidates.append(c)
            print(f"  center=({c['cx']:.0f},{c['cy']:.0f}) size={c['bbox_w']}x{c['bbox_h']} area={c['area']}")

# Let me also check a smaller dark pixel threshold
black_mask2 = gray < 10
labeled2, num2 = ndimage.label(black_mask2)
print(f"\nWith threshold <10: {num2} components")

component_stats2 = []
for i in range(1, num2 + 1):
    mask = labeled2 == i
    area = np.sum(mask)
    if area > 1000:
        ys, xs = np.where(mask)
        y_min, y_max = ys.min(), ys.max()
        x_min, x_max = xs.min(), xs.max()
        component_stats2.append({
            'area': area,
            'cx': (x_min+x_max)/2, 'cy': (y_min+y_max)/2,
            'x_min': x_min, 'x_max': x_max,
            'y_min': y_min, 'y_max': y_max,
            'bbox_w': x_max-x_min, 'bbox_h': y_max-y_min
        })

component_stats2.sort(key=lambda c: c['area'], reverse=True)
print(f"Components with area > 1000: {len(component_stats2)}")
for c in component_stats2[:60]:
    print(f"  area={c['area']:6d} center=({c['cx']:.0f},{c['cy']:.0f}) "
          f"bbox={c['bbox_w']}x{c['bbox_h']} bounds=[{c['x_min']},{c['y_min']}]-[{c['x_max']},{c['y_max']}]")
