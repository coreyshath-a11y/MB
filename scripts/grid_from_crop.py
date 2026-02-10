#!/usr/bin/env python3
"""
Extract the 21x21 crossword grid from the MrBeast Million Dollar Crossword puzzle.

Strategy:
  1. Open the high-res render of the puzzle page (3672x4752).
  2. Crop to just the crossword grid area.
  3. Try grid-line detection (Hough lines or column/row dark-pixel profiles).
  4. If that fails, tile the crop into a 21x21 grid, sample brightness at each
     cell center, and use k-means to classify black vs white (and optionally gray).
  5. Apply standard crossword numbering rules.
  6. Validate against known ACROSS / DOWN entry lists.
  7. Check key constraints (167A = 16 letters, 149A = 9 letters).
  8. Also detect gray/shaded cells for the staircase region.
  9. Save results to grid_validated.json.
"""

import json
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# ---------------------------------------------------------------------------
# Known entry lists
# ---------------------------------------------------------------------------
ACROSS = [1,8,14,22,23,24,25,28,29,30,31,32,34,35,36,38,41,42,43,45,47,48,
          50,54,57,58,59,61,63,64,66,68,70,72,73,77,79,80,81,82,83,85,88,90,
          91,92,94,97,99,100,102,103,105,106,107,109,111,113,114,117,119,120,
          121,123,124,127,129,132,134,136,138,141,143,145,147,148,149,153,155,
          156,158,159,161,164,165,167,171,172,173,174,175,176]
DOWN = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,26,27,33,
        37,39,40,43,44,46,49,51,52,53,55,56,60,62,65,67,69,71,72,74,75,76,
        77,78,80,83,84,86,87,89,93,95,96,98,101,104,108,110,112,115,116,117,
        118,122,124,125,126,128,130,131,133,135,137,139,140,141,142,144,150,
        151,152,153,154,157,160,162,163,166,168,169,170]

ACROSS_SET = set(ACROSS)
DOWN_SET = set(DOWN)
ALL_NUMBERS = sorted(ACROSS_SET | DOWN_SET)
MAX_NUM = max(ALL_NUMBERS)  # 176
GRID_SIZE = 21

# ---------------------------------------------------------------------------
# Numbering and validation
# ---------------------------------------------------------------------------

def number_grid(grid):
    """Apply standard crossword numbering. grid: 0=white, 1=black.
    Returns dict: number -> {row, col, across, down}
    """
    n = len(grid)
    numbering = {}
    num = 1
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                continue
            starts_across = (c == 0 or grid[r][c-1] == 1) and (c + 1 < n and grid[r][c+1] == 0)
            starts_down   = (r == 0 or grid[r-1][c] == 1) and (r + 1 < n and grid[r+1][c] == 0)
            if starts_across or starts_down:
                numbering[num] = {'row': r, 'col': c,
                                  'across': starts_across, 'down': starts_down}
                num += 1
    return numbering


def compute_entry_lengths(grid, numbering):
    """Compute across and down word lengths for each entry."""
    n = len(grid)
    across_lengths = {}
    down_lengths = {}
    for num, info in numbering.items():
        r, c = info['row'], info['col']
        if info['across']:
            length = 0
            cc = c
            while cc < n and grid[r][cc] == 0:
                length += 1
                cc += 1
            across_lengths[num] = length
        if info['down']:
            length = 0
            rr = r
            while rr < n and grid[rr][c] == 0:
                length += 1
                rr += 1
            down_lengths[num] = length
    return across_lengths, down_lengths


def validate_grid(grid):
    """Validate grid against known ACROSS/DOWN lists.
    Returns (is_valid, numbering, details_string).
    """
    numbering = number_grid(grid)
    comp_across = {n for n, info in numbering.items() if info['across']}
    comp_down   = {n for n, info in numbering.items() if info['down']}

    a_match = comp_across == ACROSS_SET
    d_match = comp_down == DOWN_SET

    max_num = max(numbering.keys()) if numbering else 0
    details = []
    details.append(f"Computed: {len(comp_across)} across, {len(comp_down)} down")
    details.append(f"Expected: {len(ACROSS)} across, {len(DOWN)} down")
    details.append(f"Max number: {max_num} (expected {MAX_NUM})")
    details.append(f"Across match: {a_match}, Down match: {d_match}")

    if not a_match:
        missing_a = sorted(ACROSS_SET - comp_across)
        extra_a   = sorted(comp_across - ACROSS_SET)
        if missing_a:
            details.append(f"  Missing across: {missing_a}")
        if extra_a:
            details.append(f"  Extra across: {extra_a}")
    if not d_match:
        missing_d = sorted(DOWN_SET - comp_down)
        extra_d   = sorted(comp_down - DOWN_SET)
        if missing_d:
            details.append(f"  Missing down: {missing_d}")
        if extra_d:
            details.append(f"  Extra down: {extra_d}")

    # Check key constraints
    across_lens, down_lens = compute_entry_lengths(grid, numbering)
    len_167a = across_lens.get(167, None)
    len_149a = across_lens.get(149, None)
    details.append(f"167A length: {len_167a} (expected 16)")
    details.append(f"149A length: {len_149a} (expected 9)")
    length_ok = (len_167a == 16 and len_149a == 9)
    details.append(f"Key length constraints OK: {length_ok}")

    return (a_match and d_match and length_ok), numbering, "\n".join(details)


def print_grid_ascii(grid, numbering=None):
    """Print the grid in ASCII."""
    n = len(grid)
    num_map = {}
    if numbering:
        for num, info in numbering.items():
            num_map[(info['row'], info['col'])] = num
    for r in range(n):
        line = ""
        for c in range(n):
            if grid[r][c] == 1:
                line += " ## "
            else:
                num = num_map.get((r, c), "")
                if num:
                    line += f"{num:>3} "
                else:
                    line += "  . "
        print(line)


# ---------------------------------------------------------------------------
# Image-based extraction
# ---------------------------------------------------------------------------

def extract_grid_from_image(img_path, crop_bounds=None):
    """
    Extract the 21x21 black/white grid from the crossword image.

    crop_bounds: dict with keys left_frac, right_frac, top_frac, bottom_frac
                 defining the crop region as fractions of image dimensions.

    Returns: (grid, gray_cells) or (None, None)
    """
    print(f"Opening image: {img_path}")
    img = Image.open(img_path)
    W, H = img.size
    print(f"Image size: {W}x{H}")

    # Default crop bounds
    if crop_bounds is None:
        crop_bounds = {
            'left_frac': 0.37,
            'right_frac': 0.87,
            'top_frac': 0.055,
            'bottom_frac': 0.72,
        }

    x1 = int(W * crop_bounds['left_frac'])
    x2 = int(W * crop_bounds['right_frac'])
    y1 = int(H * crop_bounds['top_frac'])
    y2 = int(H * crop_bounds['bottom_frac'])
    print(f"Crop region: ({x1},{y1}) to ({x2},{y2})  [{x2-x1}x{y2-y1}]")

    crop = img.crop((x1, y1, x2, y2))
    crop.save("/home/user/MB/analysis/grid_crop_debug.png")
    print(f"Saved crop to grid_crop_debug.png")

    crop_arr = np.array(crop)
    # Convert to grayscale
    if len(crop_arr.shape) == 3:
        gray = np.mean(crop_arr[:, :, :3], axis=2)
    else:
        gray = crop_arr.astype(float)

    cH, cW = gray.shape
    print(f"Crop size: {cW}x{cH}")

    # ------------------------------------------------------------------
    # APPROACH 1: Grid-line detection via dark-pixel column/row profiles
    # ------------------------------------------------------------------
    print("\n--- Approach 1: Grid line detection ---")
    grid_result = try_gridline_detection(gray, cW, cH)

    if grid_result is not None:
        grid, gray_cells = classify_cells(gray, grid_result, crop_arr)
        is_valid, numbering, details = validate_grid(grid)
        print(f"\nGrid-line approach result:")
        print(details)
        if is_valid:
            print("*** GRID LINE DETECTION SUCCEEDED ***")
            return grid, gray_cells

    # ------------------------------------------------------------------
    # APPROACH 2: Tile-based k-means classification
    # ------------------------------------------------------------------
    print("\n--- Approach 2: Tile-based k-means ---")

    # Try multiple slight adjustments to the crop bounds
    offsets = [
        (0, 0, 0, 0),
        (-0.005, 0.005, -0.005, 0.005),
        (0.005, -0.005, 0.005, -0.005),
        (-0.01, 0.01, -0.01, 0.01),
        (0.01, -0.01, 0.01, -0.01),
        (-0.01, 0, -0.005, 0),
        (0, 0.01, 0, 0.005),
        (-0.015, 0.005, -0.005, 0.005),
        (0.005, -0.015, 0.005, -0.005),
    ]

    for dx1, dx2, dy1, dy2 in offsets:
        adj_bounds = {
            'left_frac': crop_bounds['left_frac'] + dx1,
            'right_frac': crop_bounds['right_frac'] + dx2,
            'top_frac': crop_bounds['top_frac'] + dy1,
            'bottom_frac': crop_bounds['bottom_frac'] + dy2,
        }
        ax1 = int(W * adj_bounds['left_frac'])
        ax2 = int(W * adj_bounds['right_frac'])
        ay1 = int(H * adj_bounds['top_frac'])
        ay2 = int(H * adj_bounds['bottom_frac'])
        adj_crop = img.crop((ax1, ay1, ax2, ay2))
        adj_arr = np.array(adj_crop)
        if len(adj_arr.shape) == 3:
            adj_gray = np.mean(adj_arr[:, :, :3], axis=2)
        else:
            adj_gray = adj_arr.astype(float)

        adj_cH, adj_cW = adj_gray.shape

        result = try_kmeans_tiling(adj_gray, adj_cW, adj_cH, adj_arr)
        if result is not None:
            grid, gray_cells = result
            is_valid, numbering, details = validate_grid(grid)
            offset_str = f"({dx1:+.3f},{dx2:+.3f},{dy1:+.3f},{dy2:+.3f})"
            print(f"\nk-means with offset {offset_str}:")
            print(details)
            if is_valid:
                print(f"*** K-MEANS SUCCEEDED with offset {offset_str} ***")
                return grid, gray_cells

    # ------------------------------------------------------------------
    # APPROACH 3: Use Hough line transform (OpenCV)
    # ------------------------------------------------------------------
    print("\n--- Approach 3: OpenCV Hough line detection ---")
    grid_result = try_hough_lines(gray, cW, cH)
    if grid_result is not None:
        grid, gray_cells = classify_cells(gray, grid_result, crop_arr)
        is_valid, numbering, details = validate_grid(grid)
        print(f"\nHough approach result:")
        print(details)
        if is_valid:
            print("*** HOUGH LINE DETECTION SUCCEEDED ***")
            return grid, gray_cells

    # ------------------------------------------------------------------
    # APPROACH 4: Brute-force search over grid bounds
    # ------------------------------------------------------------------
    print("\n--- Approach 4: Brute-force grid bounds search ---")
    result = try_bruteforce_bounds(img, W, H)
    if result is not None:
        return result

    print("\n*** ALL IMAGE-BASED APPROACHES FAILED ***")
    return None, None


def try_gridline_detection(gray, cW, cH):
    """Detect grid lines using dark-pixel column/row profiles.
    Returns (hlines, vlines) arrays of 22 lines each, or None.
    """
    from scipy.signal import find_peaks

    # Try multiple thresholds for dark pixel detection
    best_vlines = None
    best_vscore = 1e9
    best_hlines = None
    best_hscore = 1e9

    for thresh in [60, 80, 100, 120, 140, 160]:
        # Vertical lines: columns with many dark pixels
        col_dark = np.sum(gray < thresh, axis=0).astype(float)
        min_dist = cW // 28
        min_height = np.max(col_dark) * 0.08 if np.max(col_dark) > 0 else 1

        peaks_v, _ = find_peaks(col_dark, height=min_height, distance=min_dist)
        if len(peaks_v) < 15:
            continue

        # Greedy search for best set of ~22 evenly-spaced peaks
        diffs = np.diff(peaks_v)
        median_sp = np.median(diffs)

        for start_idx in range(min(len(peaks_v), 15)):
            lines = [peaks_v[start_idx]]
            for p in peaks_v[start_idx + 1:]:
                expected = lines[-1] + median_sp
                if abs(p - expected) < median_sp * 0.3:
                    lines.append(p)
            if len(lines) >= 19:
                spacings = np.diff(lines)
                score = np.std(spacings) + abs(len(lines) - 22) * 5
                if score < best_vscore:
                    best_vscore = score
                    best_vlines = list(lines)

        # Horizontal lines
        row_dark = np.sum(gray < thresh, axis=1).astype(float)
        min_dist_h = cH // 28
        min_height_h = np.max(row_dark) * 0.08 if np.max(row_dark) > 0 else 1

        peaks_h, _ = find_peaks(row_dark, height=min_height_h, distance=min_dist_h)
        if len(peaks_h) < 15:
            continue

        diffs_h = np.diff(peaks_h)
        median_sp_h = np.median(diffs_h)

        for start_idx in range(min(len(peaks_h), 15)):
            lines = [peaks_h[start_idx]]
            for p in peaks_h[start_idx + 1:]:
                expected = lines[-1] + median_sp_h
                if abs(p - expected) < median_sp_h * 0.3:
                    lines.append(p)
            if len(lines) >= 19:
                spacings = np.diff(lines)
                score = np.std(spacings) + abs(len(lines) - 22) * 5
                if score < best_hscore:
                    best_hscore = score
                    best_hlines = list(lines)

    if best_vlines is None or best_hlines is None:
        print("  Grid line detection failed: not enough lines found.")
        return None

    # Extend/trim to exactly 22 lines
    vlines = extend_to_22(best_vlines, cW)
    hlines = extend_to_22(best_hlines, cH)

    if vlines is None or hlines is None:
        print("  Grid line detection failed: could not get 22 lines.")
        return None

    v_spacing = np.mean(np.diff(vlines))
    h_spacing = np.mean(np.diff(hlines))
    print(f"  Found {len(vlines)} vertical lines (spacing ~{v_spacing:.1f}px)")
    print(f"  Found {len(hlines)} horizontal lines (spacing ~{h_spacing:.1f}px)")

    return (hlines, vlines)


def extend_to_22(lines, max_dim):
    """Extend a set of grid lines to exactly 22 by adding predicted positions."""
    lines = list(lines)
    if len(lines) < 2:
        return None
    spacing = np.median(np.diff(lines))

    # Extend at the start
    while len(lines) < 22:
        predicted = lines[0] - spacing
        if predicted >= -spacing * 0.5:
            lines.insert(0, int(round(predicted)))
        else:
            break

    # Extend at the end
    while len(lines) < 22:
        predicted = lines[-1] + spacing
        if predicted <= max_dim + spacing * 0.5:
            lines.append(int(round(predicted)))
        else:
            break

    # Trim if over 22
    while len(lines) > 22:
        spacings = np.diff(lines)
        median_sp = np.median(spacings)
        deviations = np.abs(spacings - median_sp)
        worst = np.argmax(deviations)
        if worst == 0:
            lines = lines[1:]
        elif worst == len(spacings) - 1:
            lines = lines[:-1]
        else:
            lines.pop(worst + 1)

    return lines if len(lines) == 22 else None


def classify_cells(gray, gridlines, color_arr=None):
    """Given grid lines (hlines, vlines), classify each cell as black/white/gray.
    Returns (grid, gray_cells) where grid[r][c] is 0 (white) or 1 (black),
    and gray_cells is a list of (r,c) tuples.
    """
    hlines, vlines = gridlines

    # Sample the center of each cell
    brightness = np.zeros((21, 21))
    for r in range(21):
        for c in range(21):
            y1, y2 = hlines[r], hlines[r+1]
            x1, x2 = vlines[c], vlines[c+1]
            # Sample inner 40% to avoid grid lines
            dy, dx = y2 - y1, x2 - x1
            cy1 = y1 + int(dy * 0.25)
            cy2 = y2 - int(dy * 0.25)
            cx1 = x1 + int(dx * 0.25)
            cx2 = x2 - int(dx * 0.25)
            # Clamp
            cy1 = max(0, cy1)
            cy2 = min(gray.shape[0]-1, cy2)
            cx1 = max(0, cx1)
            cx2 = min(gray.shape[1]-1, cx2)
            if cy2 <= cy1 or cx2 <= cx1:
                brightness[r][c] = 128
            else:
                brightness[r][c] = np.mean(gray[cy1:cy2, cx1:cx2])

    # k-means with k=2 first (black vs white)
    flat = brightness.flatten()
    grid, gray_cells = kmeans_classify(flat, brightness, color_arr, hlines, vlines)
    return grid, gray_cells


def kmeans_classify(flat, brightness, color_arr, hlines, vlines):
    """Use k-means to classify cells as black/white and detect gray cells."""
    from sklearn.cluster import KMeans

    # k=2: black vs white
    km2 = KMeans(n_clusters=2, random_state=42, n_init=10).fit(flat.reshape(-1, 1))
    centers2 = km2.cluster_centers_.flatten()
    labels2 = km2.labels_.reshape(21, 21)

    # Determine which cluster is black (lower brightness)
    black_cluster = np.argmin(centers2)
    white_cluster = np.argmax(centers2)

    grid = [[0]*21 for _ in range(21)]
    for r in range(21):
        for c in range(21):
            if labels2[r][c] == black_cluster:
                grid[r][c] = 1

    # Detect gray cells using k=3
    gray_cells = []
    if len(flat) > 0:
        km3 = KMeans(n_clusters=3, random_state=42, n_init=10).fit(flat.reshape(-1, 1))
        centers3 = sorted(km3.cluster_centers_.flatten())
        labels3 = km3.labels_.reshape(21, 21)

        # Find the cluster whose center is in between (gray)
        cluster_order = np.argsort(km3.cluster_centers_.flatten())
        # cluster_order[0] = darkest, [1] = middle, [2] = brightest
        gray_cluster_idx = cluster_order[1]

        # Only report gray cells if the middle cluster is truly distinct
        if centers3[1] - centers3[0] > 20 and centers3[2] - centers3[1] > 20:
            for r in range(21):
                for c in range(21):
                    if labels3[r][c] == gray_cluster_idx:
                        gray_cells.append((r, c))

    return grid, gray_cells


def try_kmeans_tiling(gray, cW, cH, color_arr=None):
    """Tile the crop into 21x21 cells, sample brightness, k-means classify."""
    from sklearn.cluster import KMeans

    cell_w = cW / 21.0
    cell_h = cH / 21.0

    # Sample brightness at each cell center (inner 50%)
    brightness = np.zeros((21, 21))
    for r in range(21):
        for c in range(21):
            y1 = int(r * cell_h)
            y2 = int((r + 1) * cell_h)
            x1 = int(c * cell_w)
            x2 = int((c + 1) * cell_w)
            dy, dx = y2 - y1, x2 - x1
            cy1 = y1 + int(dy * 0.25)
            cy2 = y2 - int(dy * 0.25)
            cx1 = x1 + int(dx * 0.25)
            cx2 = x2 - int(dx * 0.25)
            cy1 = max(0, cy1)
            cy2 = min(gray.shape[0]-1, cy2)
            cx1 = max(0, cx1)
            cx2 = min(gray.shape[1]-1, cx2)
            if cy2 <= cy1 or cx2 <= cx1:
                brightness[r][c] = 128
            else:
                brightness[r][c] = np.mean(gray[cy1:cy2, cx1:cx2])

    flat = brightness.flatten()

    # Print brightness stats
    print(f"  Brightness range: {flat.min():.1f} - {flat.max():.1f}, "
          f"mean={flat.mean():.1f}, std={flat.std():.1f}")

    # k-means with k=2
    km = KMeans(n_clusters=2, random_state=42, n_init=10).fit(flat.reshape(-1, 1))
    centers = km.cluster_centers_.flatten()
    labels = km.labels_.reshape(21, 21)

    black_cluster = np.argmin(centers)
    print(f"  k=2 centers: {sorted(centers)}")

    grid = [[0]*21 for _ in range(21)]
    for r in range(21):
        for c in range(21):
            if labels[r][c] == black_cluster:
                grid[r][c] = 1

    black_count = sum(sum(row) for row in grid)
    print(f"  Black cells: {black_count}")

    # Also try with k=3 for gray detection
    gray_cells = []
    if flat.std() > 10:
        km3 = KMeans(n_clusters=3, random_state=42, n_init=10).fit(flat.reshape(-1, 1))
        centers3 = sorted(km3.cluster_centers_.flatten())
        print(f"  k=3 centers: {centers3}")
        labels3 = km3.labels_.reshape(21, 21)
        cluster_order = np.argsort(km3.cluster_centers_.flatten())
        gray_cluster_idx = cluster_order[1]
        if centers3[1] - centers3[0] > 15 and centers3[2] - centers3[1] > 15:
            for r in range(21):
                for c in range(21):
                    if labels3[r][c] == gray_cluster_idx:
                        gray_cells.append((r, c))
            print(f"  Gray cells detected: {len(gray_cells)}")

    return grid, gray_cells


def try_hough_lines(gray, cW, cH):
    """Try OpenCV Hough transform to find grid lines."""
    try:
        import cv2
    except ImportError:
        print("  OpenCV not available, skipping Hough approach.")
        return None

    # Edge detection
    gray_uint8 = gray.astype(np.uint8)
    edges = cv2.Canny(gray_uint8, 50, 150, apertureSize=3)

    # Hough lines
    lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=int(min(cW, cH) * 0.3))
    if lines is None:
        print("  No Hough lines found.")
        return None

    # Separate horizontal and vertical lines
    h_lines = []
    v_lines = []
    for line in lines:
        rho, theta = line[0]
        if abs(theta) < 0.1 or abs(theta - np.pi) < 0.1:
            # Vertical
            v_lines.append(abs(rho))
        elif abs(theta - np.pi/2) < 0.1:
            # Horizontal
            h_lines.append(abs(rho))

    print(f"  Hough: {len(v_lines)} vertical, {len(h_lines)} horizontal")

    if len(v_lines) < 10 or len(h_lines) < 10:
        print("  Not enough Hough lines.")
        return None

    # Cluster nearby lines
    v_lines = cluster_lines(sorted(v_lines), min_dist=cW//30)
    h_lines = cluster_lines(sorted(h_lines), min_dist=cH//30)

    print(f"  After clustering: {len(v_lines)} vertical, {len(h_lines)} horizontal")

    # Try to pick 22 evenly-spaced lines from each set
    vlines = pick_best_22(v_lines, cW)
    hlines = pick_best_22(h_lines, cH)

    if vlines is None or hlines is None:
        print("  Could not select 22 evenly-spaced lines.")
        return None

    return (hlines, vlines)


def cluster_lines(lines, min_dist):
    """Cluster nearby line positions."""
    if not lines:
        return []
    clusters = [[lines[0]]]
    for l in lines[1:]:
        if l - clusters[-1][-1] < min_dist:
            clusters[-1].append(l)
        else:
            clusters.append([l])
    return [np.mean(c) for c in clusters]


def pick_best_22(lines, max_dim):
    """From a set of line positions, pick the best 22 evenly-spaced ones."""
    if len(lines) < 15:
        return None

    lines = sorted(lines)
    best = None
    best_score = 1e9

    # Estimate spacing
    for i in range(len(lines)):
        for j in range(i+1, min(i+5, len(lines))):
            spacing = (lines[j] - lines[i]) / (j - i)
            if spacing < max_dim / 30 or spacing > max_dim / 15:
                continue

            # Build set of 22 lines starting from lines[i] - k*spacing
            for k in range(5):
                start = lines[i] - k * spacing
                predicted = [start + m * spacing for m in range(22)]

                # Match predicted to actual
                matched = []
                for pred in predicted:
                    dists = [abs(l - pred) for l in lines]
                    best_match = min(dists)
                    if best_match < spacing * 0.2:
                        matched.append(lines[np.argmin(dists)])
                    else:
                        matched.append(pred)

                if len(matched) == 22:
                    score = np.std(np.diff(matched))
                    if score < best_score:
                        best_score = score
                        best = [int(round(m)) for m in matched]

    return best


def try_bruteforce_bounds(img, W, H):
    """Try many slight variations of crop bounds to find valid grid."""
    print("  Trying brute-force crop bound adjustments...")

    # Systematic search
    left_fracs = np.arange(0.35, 0.42, 0.005)
    right_fracs = np.arange(0.85, 0.90, 0.005)
    top_fracs = np.arange(0.04, 0.08, 0.005)
    bottom_fracs = np.arange(0.70, 0.74, 0.005)

    best_score = -1
    best_result = None
    trials = 0

    for lf in left_fracs:
        for rf in right_fracs:
            for tf in top_fracs:
                for bf in bottom_fracs:
                    trials += 1
                    x1 = int(W * lf)
                    x2 = int(W * rf)
                    y1 = int(H * tf)
                    y2 = int(H * bf)
                    crop = img.crop((x1, y1, x2, y2))
                    arr = np.array(crop)
                    if len(arr.shape) == 3:
                        g = np.mean(arr[:, :, :3], axis=2)
                    else:
                        g = arr.astype(float)
                    cH, cW = g.shape

                    # Quick k-means tiling
                    result = quick_kmeans(g, cW, cH)
                    if result is None:
                        continue
                    grid = result

                    numbering = number_grid(grid)
                    comp_across = {n for n, info in numbering.items() if info['across']}
                    comp_down   = {n for n, info in numbering.items() if info['down']}

                    # Score: number of matching entries
                    a_correct = len(comp_across & ACROSS_SET)
                    d_correct = len(comp_down & DOWN_SET)
                    a_extra = len(comp_across - ACROSS_SET)
                    d_extra = len(comp_down - DOWN_SET)
                    score = a_correct + d_correct - a_extra - d_extra

                    if score > best_score:
                        best_score = score
                        max_num = max(numbering.keys()) if numbering else 0
                        print(f"  Trial {trials}: score={score} "
                              f"(across={a_correct}/{len(ACROSS)}, down={d_correct}/{len(DOWN)}) "
                              f"max_num={max_num} bounds=({lf:.3f},{rf:.3f},{tf:.3f},{bf:.3f})")

                        if comp_across == ACROSS_SET and comp_down == DOWN_SET:
                            # Check key lengths
                            al, dl = compute_entry_lengths(grid, numbering)
                            len_167a = al.get(167, None)
                            len_149a = al.get(149, None)
                            if len_167a == 16 and len_149a == 9:
                                print(f"  *** BRUTE FORCE SUCCEEDED at trial {trials}! ***")
                                # Detect gray cells
                                gray_cells = detect_gray_cells(img, W, H, lf, rf, tf, bf)
                                return grid, gray_cells

    print(f"  Brute force: best score = {best_score} after {trials} trials")
    if best_result is not None:
        return best_result
    return None


def quick_kmeans(gray, cW, cH):
    """Quick k-means classification for brute-force search."""
    from sklearn.cluster import KMeans

    cell_w = cW / 21.0
    cell_h = cH / 21.0

    brightness = np.zeros((21, 21))
    for r in range(21):
        for c in range(21):
            y1 = int(r * cell_h)
            y2 = int((r + 1) * cell_h)
            x1 = int(c * cell_w)
            x2 = int((c + 1) * cell_w)
            dy, dx = y2 - y1, x2 - x1
            cy1 = y1 + int(dy * 0.3)
            cy2 = y2 - int(dy * 0.3)
            cx1 = x1 + int(dx * 0.3)
            cx2 = x2 - int(dx * 0.3)
            cy1 = max(0, cy1)
            cy2 = min(gray.shape[0]-1, cy2)
            cx1 = max(0, cx1)
            cx2 = min(gray.shape[1]-1, cx2)
            if cy2 <= cy1 or cx2 <= cx1:
                return None
            brightness[r][c] = np.mean(gray[cy1:cy2, cx1:cx2])

    flat = brightness.flatten()
    if flat.std() < 5:
        return None

    km = KMeans(n_clusters=2, random_state=42, n_init=5).fit(flat.reshape(-1, 1))
    centers = km.cluster_centers_.flatten()
    labels = km.labels_.reshape(21, 21)
    black_cluster = np.argmin(centers)

    grid = [[0]*21 for _ in range(21)]
    for r in range(21):
        for c in range(21):
            if labels[r][c] == black_cluster:
                grid[r][c] = 1

    return grid


def detect_gray_cells(img, W, H, lf, rf, tf, bf):
    """Detect gray/shaded cells in the grid area."""
    from sklearn.cluster import KMeans

    x1 = int(W * lf)
    x2 = int(W * rf)
    y1 = int(H * tf)
    y2 = int(H * bf)
    crop = img.crop((x1, y1, x2, y2))
    arr = np.array(crop)
    if len(arr.shape) == 3:
        gray = np.mean(arr[:, :, :3], axis=2)
    else:
        gray = arr.astype(float)
    cH, cW = gray.shape

    cell_w = cW / 21.0
    cell_h = cH / 21.0
    brightness = np.zeros((21, 21))
    for r in range(21):
        for c in range(21):
            y1i = int(r * cell_h)
            y2i = int((r + 1) * cell_h)
            x1i = int(c * cell_w)
            x2i = int((c + 1) * cell_w)
            dy, dx = y2i - y1i, x2i - x1i
            cy1 = y1i + int(dy * 0.3)
            cy2 = y2i - int(dy * 0.3)
            cx1 = x1i + int(dx * 0.3)
            cx2 = x2i - int(dx * 0.3)
            brightness[r][c] = np.mean(gray[max(0,cy1):max(1,cy2), max(0,cx1):max(1,cx2)])

    flat = brightness.flatten()
    km3 = KMeans(n_clusters=3, random_state=42, n_init=10).fit(flat.reshape(-1, 1))
    centers3 = sorted(km3.cluster_centers_.flatten())
    labels3 = km3.labels_.reshape(21, 21)
    cluster_order = np.argsort(km3.cluster_centers_.flatten())
    gray_cluster = cluster_order[1]

    gray_cells = []
    if centers3[1] - centers3[0] > 15 and centers3[2] - centers3[1] > 15:
        for r in range(21):
            for c in range(21):
                if labels3[r][c] == gray_cluster:
                    gray_cells.append([r, c])
    return gray_cells


# ---------------------------------------------------------------------------
# Constraint-based reconstruction (fallback if image fails)
# ---------------------------------------------------------------------------

def reconstruct_from_constraints():
    """
    Reconstruct the 21x21 grid purely from the ACROSS/DOWN entry number lists.

    Uses a row-by-row constraint propagation approach:
    - Scan cells in reading order (left-to-right, top-to-bottom)
    - For each cell, decide BLACK or WHITE
    - Track the next number to assign
    - A white cell gets a number if it starts an across or down word
    - The roles (across/down/both) must match the known lists

    Uses backtracking search with aggressive pruning.
    """
    print("\n" + "=" * 70)
    print("FALLBACK: Constraint-based reconstruction from entry lists")
    print("=" * 70)

    N = GRID_SIZE  # 21

    # Roles for each number
    num_roles = {}
    for num in ALL_NUMBERS:
        roles = set()
        if num in ACROSS_SET:
            roles.add('A')
        if num in DOWN_SET:
            roles.add('D')
        num_roles[num] = roles

    # We need to place numbers 1..176 in a 21x21 grid.
    # Number 1 must be at (0,0) since it's both across and down.
    # We'll use DFS with pruning.

    # State: for each cell in reading order, BLACK or WHITE
    # When we encounter a WHITE cell that starts an across or down word,
    # it gets the next number.

    # Optimization: process cells in reading order and maintain:
    # - current number counter
    # - the grid so far

    grid = [[-1] * N for _ in range(N)]  # -1 = undecided

    def cell_idx(r, c):
        return r * N + c

    def idx_to_rc(idx):
        return idx // N, idx % N

    def get_cell(r, c):
        if 0 <= r < N and 0 <= c < N:
            return grid[r][c]
        return -2  # out of bounds treated specially

    def would_start_across(r, c):
        """Would cell (r,c) start an across word if it's white?"""
        left = get_cell(r, c-1)
        right = get_cell(r, c+1)
        return (c == 0 or left == 1) and (c + 1 < N and right != 1)

    def would_start_down(r, c):
        """Would cell (r,c) start a down word if it's white?"""
        above = get_cell(r-1, c)
        below = get_cell(r+1, c)
        return (r == 0 or above == 1) and (r + 1 < N and below != 1)

    solutions = []

    def solve(idx, next_num):
        """Backtracking solver. idx = current cell index, next_num = next number to assign."""
        if next_num > MAX_NUM:
            # All numbers placed. Remaining cells must not create new numbers.
            for i in range(idx, N * N):
                r, c = idx_to_rc(i)
                grid[r][c] = 0  # white by default
                # But check if this creates a numbered cell
                sa = would_start_across(r, c)
                sd = would_start_down(r, c)
                if sa or sd:
                    # This cell would get a number, but we've run out
                    # Make it black instead
                    grid[r][c] = 1
            # Validate
            numbering = number_grid([[max(0, grid[r][c]) for c in range(N)] for r in range(N)])
            if max(numbering.keys(), default=0) == MAX_NUM:
                solutions.append([row[:] for row in grid])
            # Undo
            for i in range(idx, N * N):
                r, c = idx_to_rc(i)
                grid[r][c] = -1
            return

        if idx >= N * N:
            # Ran out of cells but still have numbers to place
            return

        r, c = idx_to_rc(idx)

        # Pruning: remaining cells must be enough for remaining numbers
        remaining_cells = N * N - idx
        remaining_nums = MAX_NUM - next_num + 1
        if remaining_cells < remaining_nums:
            return

        # Option 1: Make cell BLACK
        grid[r][c] = 1
        # Check: does this violate any constraint?
        # - If the cell above is white and started a down word, this black cell
        #   would make that down word length < 2 if it's immediately below
        valid = True
        # Check if making this black creates a 1-letter word above
        if r > 0 and grid[r-1][c] == 0:
            if r == 1 or grid[r-2][c] == 1:
                # (r-1,c) would be a single white cell between two blacks vertically
                # That's OK as long as it doesn't start a down word of length 1
                pass  # We allow length-1 words for now, validate at end

        if valid:
            solve(idx + 1, next_num)
            if solutions:
                grid[r][c] = -1
                return

        # Option 2: Make cell WHITE
        grid[r][c] = 0
        sa = would_start_across(r, c)
        sd = would_start_down(r, c)

        if sa or sd:
            # This cell gets number next_num
            expected_roles = num_roles.get(next_num, set())
            actual_roles = set()
            if sa:
                actual_roles.add('A')
            if sd:
                actual_roles.add('D')
            if actual_roles == expected_roles:
                solve(idx + 1, next_num + 1)
                if solutions:
                    grid[r][c] = -1
                    return
            # Roles don't match - this configuration is invalid
        else:
            # White cell, no number
            solve(idx + 1, next_num)
            if solutions:
                grid[r][c] = -1
                return

        grid[r][c] = -1

    # This is too slow for 441 cells. Let's use a smarter approach.
    # Instead, use the known length constraints to help.

    # Actually, let me try a completely different approach:
    # Use the fact that numbers are sequential in reading order.
    # For each pair of consecutive numbers, we know the gap (number of cells
    # between them). We need to determine which cells in that gap are black
    # and which are white.

    # But we don't know the positions yet. Let me try an iterative approach
    # where I fix rows one at a time.

    print("Direct backtracking is too slow for 21x21. Using iterative row approach...")

    # Alternative: use SAT solver or Z3 if available
    try:
        return reconstruct_with_z3()
    except ImportError:
        print("Z3 not available.")

    # Alternative: greedy forward approach with local search
    return reconstruct_greedy()


def reconstruct_greedy():
    """Greedy forward reconstruction with local fixes."""
    print("Attempting greedy reconstruction...")

    N = GRID_SIZE

    # Known facts:
    # - Number 1 is at (0,0), both across and down
    # - Numbers increase in reading order
    # - 167A has length 16 (starts at row ~18-19, column 0 or near 0, spans most of row)
    # - 149A has length 9

    # Let's try: assign positions to all 176 numbers greedily.
    # For each number, find the earliest valid position in reading order.

    grid = [[0] * N for _ in range(N)]  # Start all white
    number_positions = {}

    num_roles = {}
    for num in ALL_NUMBERS:
        roles = set()
        if num in ACROSS_SET:
            roles.add('A')
        if num in DOWN_SET:
            roles.add('D')
        num_roles[num] = roles

    # We'll process cells in reading order and try to assign numbers.
    # If a white cell would get a number, check if it matches the next expected number.
    # If not, make adjustments.

    # This is still complex. Let me try a different approach:
    # Start with all white, number it, see what's wrong, then flip cells.

    numbering = number_grid(grid)
    print(f"All-white grid: {len(numbering)} numbers (expected {MAX_NUM})")

    # With an all-white grid, every cell at the top edge or left edge starts a word.
    # Way too many numbers. We need to add black cells to reduce the count.

    # Instead of full reconstruction, let's report failure and rely on image.
    print("Greedy approach: complex, skipping in favor of image-based methods.")
    return None


def reconstruct_with_z3():
    """Use Z3 SMT solver for exact constraint-based reconstruction."""
    from z3 import Bool, And, Or, Not, If, Solver, sat, Sum, IntVal

    print("Using Z3 solver for constraint-based reconstruction...")
    N = GRID_SIZE

    # Variables: is_black[r][c] for each cell
    is_black = [[Bool(f"b_{r}_{c}") for c in range(N)] for r in range(N)]

    solver = Solver()

    # Number assignment: cells get numbered in reading order
    # A cell (r,c) is numbered if it's white AND starts across or down word

    # starts_across(r,c): white AND (left is black/edge) AND (right is white)
    def starts_across(r, c):
        left_blocked = is_black[r][c-1] if c > 0 else True
        right_white = Not(is_black[r][c+1]) if c + 1 < N else False
        return And(Not(is_black[r][c]), left_blocked, right_white)

    def starts_down(r, c):
        top_blocked = is_black[r-1][c] if r > 0 else True
        bottom_white = Not(is_black[r+1][c]) if r + 1 < N else False
        return And(Not(is_black[r][c]), top_blocked, bottom_white)

    def is_numbered(r, c):
        return Or(starts_across(r, c), starts_down(r, c))

    # Create boolean vars for "this cell is the position of number K"
    # This is expensive for 176 numbers * 441 cells. Let's use a different encoding.

    # Alternative: use integer variables for the position of each number
    # But Z3 integer reasoning can be slow too.

    # Actually, let's use the cumulative sum encoding:
    # count[i] = number of numbered cells in cells 0..i (in reading order)
    # count[-1] = 0
    # count[N*N-1] = 176

    # For cell i (reading order), let num_i = 1 if cell is numbered, 0 if not
    # Then count[i] = count[i-1] + num_i
    # The number assigned to cell i (if numbered) is count[i]

    # We need: for each K in 1..176:
    #   the cell with count = K has the right roles

    # This requires knowing which cell has count = K, which needs:
    # For each K, exists exactly one cell i where count[i] = K and cell i is numbered

    # This is getting complex. Let me try a simpler approach with Z3.

    # For each cell in reading order, create an integer variable num[i]:
    # num[i] = 0 if cell is black or white-non-numbered
    # num[i] = K if cell is the position of number K

    # Constraints:
    # 1. num values are non-decreasing in reading order (ignoring 0s)
    # 2. Non-zero num values form the sequence 1, 2, ..., 176
    # 3. If num[i] = K, then the cell has the right roles for K

    # This is still 441 integer variables. Z3 might handle it.

    print("Z3 encoding is complex. Trying simplified approach...")

    # Simplified: just encode the black cell pattern constraints
    # Key constraint: total numbered cells = 176

    # numbered[r][c] = is_numbered(r,c) as defined above

    # Count numbered cells
    numbered_bools = []
    for r in range(N):
        for c in range(N):
            numbered_bools.append(is_numbered(r, c))

    # Total must be 176
    solver.add(Sum([If(b, IntVal(1), IntVal(0)) for b in numbered_bools]) == MAX_NUM)

    # Cell (0,0) must be white (number 1)
    solver.add(Not(is_black[0][0]))

    # Number 1 is both across and down
    solver.add(starts_across(0, 0))
    solver.add(starts_down(0, 0))

    # 167A has length 16: there exists a row where an across entry spans 16 cells
    # near the bottom of the grid
    # 149A has length 9

    # These constraints are hard to encode directly without knowing positions.
    # Let's just solve for the count = 176 constraint and check.

    print("Solving Z3 model (this may take a while)...")
    result = solver.check()

    if result == sat:
        model = solver.model()
        grid = [[0]*N for _ in range(N)]
        for r in range(N):
            for c in range(N):
                if model.evaluate(is_black[r][c]):
                    grid[r][c] = 1
        return grid
    else:
        print(f"Z3 result: {result}")
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    img_path = "/home/user/MB/analysis/crossword_hires.png"
    out_path = "/home/user/MB/analysis/grid_validated.json"

    print("=" * 70)
    print("MrBeast Million Dollar Crossword - Grid Extraction")
    print("=" * 70)

    # Try image-based extraction with several crop bound configurations
    crop_configs = [
        # (name, {bounds})
        ("default", {
            'left_frac': 0.37, 'right_frac': 0.87,
            'top_frac': 0.055, 'bottom_frac': 0.72,
        }),
        ("wider", {
            'left_frac': 0.35, 'right_frac': 0.88,
            'top_frac': 0.05, 'bottom_frac': 0.73,
        }),
        ("tighter", {
            'left_frac': 0.38, 'right_frac': 0.86,
            'top_frac': 0.06, 'bottom_frac': 0.71,
        }),
        ("shifted-right", {
            'left_frac': 0.39, 'right_frac': 0.88,
            'top_frac': 0.055, 'bottom_frac': 0.715,
        }),
        ("shifted-left", {
            'left_frac': 0.36, 'right_frac': 0.86,
            'top_frac': 0.055, 'bottom_frac': 0.72,
        }),
    ]

    grid = None
    gray_cells = None

    for name, bounds in crop_configs:
        print(f"\n{'='*70}")
        print(f"Trying crop config: {name}")
        print(f"  Bounds: left={bounds['left_frac']}, right={bounds['right_frac']}, "
              f"top={bounds['top_frac']}, bottom={bounds['bottom_frac']}")
        print(f"{'='*70}")

        result = extract_grid_from_image(img_path, bounds)
        if result is not None and result[0] is not None:
            grid, gray_cells = result
            is_valid, numbering, details = validate_grid(grid)
            if is_valid:
                print(f"\n*** SUCCESS with config '{name}' ***")
                break

    # If image-based failed, try constraint-based reconstruction
    if grid is None:
        grid_result = reconstruct_from_constraints()
        if grid_result is not None:
            grid = grid_result
            gray_cells = []

    if grid is None:
        print("\n*** ALL APPROACHES FAILED ***")
        # Save what we have
        output = {
            "status": "FAILED",
            "message": "Could not extract valid grid from image or constraints"
        }
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"Saved failure report to {out_path}")
        return

    # Final validation
    is_valid, numbering, details = validate_grid(grid)
    across_lens, down_lens = compute_entry_lengths(grid, numbering)

    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    print(details)

    # Print grid
    print("\nGrid (# = black, . = white):")
    for r in range(21):
        print("".join("#" if grid[r][c] == 1 else "." for c in range(21)))

    # Print numbered grid
    print("\nNumbered grid:")
    print_grid_ascii(grid, numbering)

    # Print entry lengths
    print(f"\nAcross entry lengths:")
    for num in sorted(across_lens.keys()):
        if num in ACROSS_SET:
            print(f"  {num}A: {across_lens[num]}")

    print(f"\nDown entry lengths:")
    for num in sorted(down_lens.keys()):
        if num in DOWN_SET:
            print(f"  {num}D: {down_lens[num]}")

    # Black cell count
    black_count = sum(sum(row) for row in grid)
    white_count = 21*21 - black_count
    print(f"\nBlack cells: {black_count}, White cells: {white_count}")

    # Gray cells
    if gray_cells:
        print(f"\nGray/shaded cells ({len(gray_cells)}):")
        for gc in gray_cells:
            print(f"  ({gc[0]}, {gc[1]})")

    # Save results
    grid_str = [["B" if grid[r][c] == 1 else "W" for c in range(21)] for r in range(21)]

    numbering_json = {}
    for num, info in numbering.items():
        numbering_json[str(num)] = {
            'row': info['row'],
            'col': info['col'],
            'across': info['across'],
            'down': info['down'],
        }

    across_lens_json = {str(k): v for k, v in across_lens.items()}
    down_lens_json = {str(k): v for k, v in down_lens.items()}

    output = {
        "valid": is_valid,
        "grid": grid_str,
        "grid_binary": grid,
        "numbering": numbering_json,
        "across_lengths": across_lens_json,
        "down_lengths": down_lens_json,
        "black_cells": black_count,
        "white_cells": white_count,
        "gray_cells": gray_cells if gray_cells else [],
        "validation_details": details,
    }

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved results to {out_path}")

    # Save debug image
    save_debug_image(grid, numbering, gray_cells)


def save_debug_image(grid, numbering, gray_cells):
    """Save a debug visualization of the extracted grid."""
    scale = 30
    N = 21
    img = Image.new('RGB', (N * scale + 1, N * scale + 1), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    gray_set = set()
    if gray_cells:
        for gc in gray_cells:
            if isinstance(gc, (list, tuple)):
                gray_set.add((gc[0], gc[1]))

    num_map = {}
    if numbering:
        for num, info in numbering.items():
            num_map[(info['row'], info['col'])] = num

    for r in range(N):
        for c in range(N):
            x0, y0 = c * scale, r * scale
            x1, y1 = x0 + scale, y0 + scale
            if grid[r][c] == 1:
                draw.rectangle([x0, y0, x1, y1], fill=(0, 0, 0))
            elif (r, c) in gray_set:
                draw.rectangle([x0, y0, x1, y1], fill=(180, 180, 180), outline=(0, 0, 0))
            else:
                draw.rectangle([x0, y0, x1, y1], outline=(0, 0, 0))

            # Draw number
            num = num_map.get((r, c))
            if num:
                draw.text((x0 + 2, y0 + 1), str(num), fill=(0, 0, 0))

    path = "/home/user/MB/analysis/grid_extracted_debug.png"
    img.save(path)
    print(f"Saved debug image to {path}")


if __name__ == "__main__":
    main()
