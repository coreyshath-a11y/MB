#!/usr/bin/env python3
"""
QR Code Overlay Test for MrBeast Million Dollar Crossword

Theory: The crossword grid's black/white cell pattern might form a QR code
when the left and right halves are overlaid (OR operation).

This script:
1. Extracts the crossword grid from the image (black=1, white=0)
2. Splits into left and right halves
3. Tests various overlay operations (OR, AND, XOR)
4. Tests mirroring, rotating, full grid as barcode
5. Checks for QR finder patterns
6. Attempts QR/DataMatrix decoding

By Mike Selinker / Lone Shark Games puzzle: "I WROTE A PUZZLE FOR JIMMY!"
"""

import sys
import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# Optional imports
try:
    from pyzbar.pyzbar import decode as pyzbar_decode
    HAS_PYZBAR = True
except ImportError:
    HAS_PYZBAR = False
    print("WARNING: pyzbar not available")

try:
    from pylibdmtx.pylibdmtx import decode as dmtx_decode
    HAS_DMTX = True
except ImportError:
    HAS_DMTX = False
    print("WARNING: pylibdmtx not available")


# ============================================================
# SECTION 1: Grid extraction from the crossword image
# ============================================================

def extract_grid_from_image(img_path):
    """Extract the 21xN black/white grid from the crossword image."""
    img = Image.open(img_path)
    arr = np.array(img)
    h, w = arr.shape[:2]
    gray = np.mean(arr, axis=2) if len(arr.shape) == 3 else arr.astype(float)
    
    print(f"  Image: {w}x{h}")
    
    # Find vertical grid lines using column darkness at threshold 200
    grid_y_start, grid_y_end = 70, 570
    
    # Compute dark pixel counts per column
    col_counts = []
    for x in range(400, 910):
        count = int(np.sum(gray[grid_y_start:grid_y_end, x] < 200))
        col_counts.append((x, count))
    
    # Find peaks (grid lines) - columns where count > 300
    v_peaks = []
    for x, count in col_counts:
        if count > 300:
            if not v_peaks or x - v_peaks[-1][0] > 10:
                v_peaks.append((x, count))
            elif count > v_peaks[-1][1]:
                v_peaks[-1] = (x, count)
    
    # Fill in missing grid lines (gaps of ~39px should have a line at the midpoint)
    v_lines = [p[0] for p in v_peaks]
    filled_v_lines = [v_lines[0]]
    for i in range(1, len(v_lines)):
        gap = v_lines[i] - v_lines[i-1]
        if gap > 30:  # Gap too large, insert midpoint
            filled_v_lines.append((v_lines[i-1] + v_lines[i]) // 2)
        filled_v_lines.append(v_lines[i])
    
    print(f"  Vertical grid lines ({len(filled_v_lines)}): {filled_v_lines[:5]}...{filled_v_lines[-3:]}")
    
    # Find horizontal grid lines similarly
    grid_x_start = filled_v_lines[0] + 5
    grid_x_end = filled_v_lines[-1] - 5
    
    row_counts = []
    for y in range(60, 580):
        count = int(np.sum(gray[y, grid_x_start:grid_x_end] < 200))
        row_counts.append((y, count))
    
    h_peaks = []
    for y, count in row_counts:
        if count > 200:
            if not h_peaks or y - h_peaks[-1][0] > 10:
                h_peaks.append((y, count))
            elif count > h_peaks[-1][1]:
                h_peaks[-1] = (y, count)
    
    h_lines = [p[0] for p in h_peaks]
    
    # Fill in missing horizontal lines
    filled_h_lines = [h_lines[0]]
    for i in range(1, len(h_lines)):
        gap = h_lines[i] - h_lines[i-1]
        if gap > 30:
            filled_h_lines.append((h_lines[i-1] + h_lines[i]) // 2)
        filled_h_lines.append(h_lines[i])
    
    print(f"  Horizontal grid lines ({len(filled_h_lines)}): {filled_h_lines[:5]}...{filled_h_lines[-3:]}")
    
    n_cols = len(filled_v_lines) - 1
    n_rows = len(filled_h_lines) - 1
    print(f"  Grid dimensions: {n_cols} columns x {n_rows} rows")
    
    # Sample center of each cell to determine black (1) or white (0)
    grid = np.zeros((n_rows, n_cols), dtype=int)
    
    for row in range(n_rows):
        for col in range(n_cols):
            # Cell boundaries
            x1 = filled_v_lines[col]
            x2 = filled_v_lines[col + 1]
            y1 = filled_h_lines[row]
            y2 = filled_h_lines[row + 1]
            
            # Sample center 50% of cell
            cx1 = x1 + (x2 - x1) * 3 // 8
            cx2 = x1 + (x2 - x1) * 5 // 8
            cy1 = y1 + (y2 - y1) * 3 // 8
            cy2 = y1 + (y2 - y1) * 5 // 8
            
            # Average brightness in center region
            region = gray[cy1:cy2+1, cx1:cx2+1]
            avg_brightness = np.mean(region)
            
            # Black cells have low brightness
            grid[row][col] = 1 if avg_brightness < 120 else 0
    
    return grid


def extract_grid_with_numbering(grid):
    """Apply standard crossword numbering and return number map."""
    n_rows, n_cols = grid.shape
    numbers = np.zeros_like(grid)
    num = 1
    
    across_nums = []
    down_nums = []
    
    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c] == 1:  # Black cell
                continue
            
            starts_across = False
            starts_down = False
            
            if (c == 0 or grid[r][c-1] == 1):
                if c + 1 < n_cols and grid[r][c+1] == 0:
                    starts_across = True
            
            if (r == 0 or grid[r-1][c] == 1):
                if r + 1 < n_rows and grid[r+1][c] == 0:
                    starts_down = True
            
            if starts_across or starts_down:
                numbers[r][c] = num
                if starts_across:
                    across_nums.append(num)
                if starts_down:
                    down_nums.append(num)
                num += 1
    
    return numbers, across_nums, down_nums


# ============================================================
# SECTION 2: Grid visualization
# ============================================================

def print_grid(grid, label="Grid"):
    """Print a grid pattern using block characters."""
    n_rows, n_cols = grid.shape
    print(f"\n{label} ({n_cols}x{n_rows}):")
    for row in range(n_rows):
        line = ""
        for col in range(n_cols):
            line += "##" if grid[row][col] == 1 else ".."
        print(f"  {line}")


def grid_to_image(grid, cell_size=10, label="grid"):
    """Convert a grid to a PIL Image."""
    n_rows, n_cols = grid.shape
    img = Image.new('L', (n_cols * cell_size, n_rows * cell_size), 255)
    draw = ImageDraw.Draw(img)
    
    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c] == 1:
                x1 = c * cell_size
                y1 = r * cell_size
                x2 = x1 + cell_size - 1
                y2 = y1 + cell_size - 1
                draw.rectangle([x1, y1, x2, y2], fill=0)
    
    return img


def save_grid_image(grid, path, cell_size=10):
    """Save grid as image file."""
    img = grid_to_image(grid, cell_size)
    img.save(path)
    print(f"  Saved: {path}")
    return img


# ============================================================
# SECTION 3: QR code detection
# ============================================================

def check_finder_pattern(grid, start_row, start_col):
    """Check if a 7x7 QR finder pattern exists at given position.
    
    Finder pattern is:
    1111111
    1000001
    1011101
    1011101
    1011101
    1000001
    1111111
    """
    pattern = np.array([
        [1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1]
    ])
    
    n_rows, n_cols = grid.shape
    if start_row + 7 > n_rows or start_col + 7 > n_cols:
        return False, 0
    
    region = grid[start_row:start_row+7, start_col:start_col+7]
    match = np.sum(region == pattern)
    total = 49
    
    return match == total, match / total


def find_all_finder_patterns(grid):
    """Search for QR finder patterns anywhere in the grid."""
    n_rows, n_cols = grid.shape
    results = []
    
    for r in range(n_rows - 6):
        for c in range(n_cols - 6):
            exact, similarity = check_finder_pattern(grid, r, c)
            if similarity >= 0.85:  # At least 85% match
                results.append((r, c, similarity, exact))
    
    return results


def check_qr_structure(grid):
    """Check if a grid has the overall structure of a QR code."""
    n_rows, n_cols = grid.shape
    
    results = {
        'has_top_left_finder': False,
        'has_top_right_finder': False,
        'has_bottom_left_finder': False,
        'finder_details': [],
        'size_valid': False,
        'timing_pattern': False,
    }
    
    # QR code sizes: 21, 25, 29, 33, ... (4n+1 for version n)
    valid_sizes = [4*v + 17 for v in range(1, 41)]
    if n_rows == n_cols and n_rows in valid_sizes:
        results['size_valid'] = True
        results['qr_version'] = (n_rows - 17) // 4
    
    # Check three corners for finder patterns
    # Top-left: (0,0)
    exact, sim = check_finder_pattern(grid, 0, 0)
    results['has_top_left_finder'] = exact
    results['finder_details'].append(('top-left', 0, 0, sim, exact))
    
    # Top-right: (0, n_cols-7)
    if n_cols >= 7:
        exact, sim = check_finder_pattern(grid, 0, n_cols - 7)
        results['has_top_right_finder'] = exact
        results['finder_details'].append(('top-right', 0, n_cols-7, sim, exact))
    
    # Bottom-left: (n_rows-7, 0)
    if n_rows >= 7:
        exact, sim = check_finder_pattern(grid, n_rows - 7, 0)
        results['has_bottom_left_finder'] = exact
        results['finder_details'].append(('bottom-left', n_rows-7, 0, sim, exact))
    
    # Check timing patterns (row 6 and column 6 should alternate 1,0,1,0...)
    if n_rows >= 9 and n_cols >= 9:
        # Horizontal timing pattern: row 6, columns 8 to n_cols-8
        h_timing = grid[6, 8:n_cols-8] if n_cols > 16 else np.array([])
        expected_h = np.array([1 if i % 2 == 0 else 0 for i in range(len(h_timing))])
        if len(h_timing) > 0:
            h_match = np.sum(h_timing == expected_h) / len(h_timing)
            results['h_timing_match'] = h_match
        
        # Vertical timing pattern: column 6, rows 8 to n_rows-8
        v_timing = grid[8:n_rows-8, 6] if n_rows > 16 else np.array([])
        expected_v = np.array([1 if i % 2 == 0 else 0 for i in range(len(v_timing))])
        if len(v_timing) > 0:
            v_match = np.sum(v_timing == expected_v) / len(v_timing)
            results['v_timing_match'] = v_match
        
        results['timing_pattern'] = (
            results.get('h_timing_match', 0) > 0.8 and 
            results.get('v_timing_match', 0) > 0.8
        )
    
    return results


def try_decode_as_barcode(grid, label="grid"):
    """Try to decode a grid as QR code or other barcode."""
    results = []
    
    # Create image from grid at multiple scales
    for cell_size in [10, 20, 5, 1]:
        img = grid_to_image(grid, cell_size)
        
        # Add quiet zone (white border)
        quiet = 4 * cell_size
        bordered = Image.new('L', (img.width + 2*quiet, img.height + 2*quiet), 255)
        bordered.paste(img, (quiet, quiet))
        
        # Try pyzbar
        if HAS_PYZBAR:
            try:
                decoded = pyzbar_decode(bordered)
                for d in decoded:
                    result = f"pyzbar ({label}, scale={cell_size}): {d.type} = {d.data.decode('utf-8', errors='replace')}"
                    results.append(result)
                    print(f"  FOUND: {result}")
            except Exception as e:
                pass
        
        # Try pylibdmtx
        if HAS_DMTX:
            try:
                decoded = dmtx_decode(bordered, timeout=2000)
                for d in decoded:
                    result = f"dmtx ({label}, scale={cell_size}): DataMatrix = {d.data.decode('utf-8', errors='replace')}"
                    results.append(result)
                    print(f"  FOUND: {result}")
            except Exception as e:
                pass
        
        # Also try inverted (white=black, black=white)
        inv_grid = 1 - grid
        inv_img = grid_to_image(inv_grid, cell_size)
        inv_bordered = Image.new('L', (inv_img.width + 2*quiet, inv_img.height + 2*quiet), 255)
        inv_bordered.paste(inv_img, (quiet, quiet))
        
        if HAS_PYZBAR:
            try:
                decoded = pyzbar_decode(inv_bordered)
                for d in decoded:
                    result = f"pyzbar INVERTED ({label}, scale={cell_size}): {d.type} = {d.data.decode('utf-8', errors='replace')}"
                    results.append(result)
                    print(f"  FOUND: {result}")
            except Exception as e:
                pass
        
        if HAS_DMTX:
            try:
                decoded = dmtx_decode(inv_bordered, timeout=2000)
                for d in decoded:
                    result = f"dmtx INVERTED ({label}, scale={cell_size}): DataMatrix = {d.data.decode('utf-8', errors='replace')}"
                    results.append(result)
                    print(f"  FOUND: {result}")
            except Exception as e:
                pass
    
    return results


# ============================================================
# SECTION 4: Overlay operations
# ============================================================

def split_left_right(grid, include_center='both'):
    """Split grid into left and right halves.
    
    For odd-width grids, center column can go to:
    - 'left': left half includes center
    - 'right': right half includes center
    - 'both': both halves include center
    - 'neither': center column excluded
    """
    n_rows, n_cols = grid.shape
    mid = n_cols // 2
    
    if n_cols % 2 == 1:  # Odd number of columns
        if include_center == 'left':
            left = grid[:, :mid+1]
            right = grid[:, mid+1:]
        elif include_center == 'right':
            left = grid[:, :mid]
            right = grid[:, mid:]
        elif include_center == 'both':
            left = grid[:, :mid+1]
            right = grid[:, mid:]
        else:  # neither
            left = grid[:, :mid]
            right = grid[:, mid+1:]
    else:
        left = grid[:, :mid]
        right = grid[:, mid:]
    
    return left, right


def overlay_or(a, b):
    """OR overlay: black if either is black."""
    return np.maximum(a, b)


def overlay_and(a, b):
    """AND overlay: black only if both are black."""
    return np.minimum(a, b)


def overlay_xor(a, b):
    """XOR overlay: black if exactly one is black."""
    return (a + b) % 2


def mirror_horizontal(grid):
    """Mirror grid left-to-right."""
    return np.fliplr(grid)


def mirror_vertical(grid):
    """Mirror grid top-to-bottom."""
    return np.flipud(grid)


def rotate_90(grid):
    """Rotate grid 90 degrees clockwise."""
    return np.rot90(grid, k=-1)


def rotate_180(grid):
    """Rotate grid 180 degrees."""
    return np.rot90(grid, k=2)


def rotate_270(grid):
    """Rotate grid 270 degrees clockwise."""
    return np.rot90(grid, k=1)


# ============================================================
# SECTION 5: Main test runner
# ============================================================

def run_all_tests(grid, output_dir):
    """Run all QR overlay tests on a grid."""
    n_rows, n_cols = grid.shape
    all_results = []
    
    print(f"\n{'='*60}")
    print(f"GRID: {n_cols}x{n_rows}")
    print(f"Black cells: {np.sum(grid)}, White cells: {np.sum(1-grid)}")
    print(f"{'='*60}")
    
    # --- Test 0: Full grid as-is ---
    print(f"\n--- Test 0: Full grid as barcode ---")
    qr_info = check_qr_structure(grid)
    print(f"  Size valid for QR: {qr_info['size_valid']}")
    if qr_info.get('qr_version'):
        print(f"  QR Version: {qr_info['qr_version']}")
    for fd in qr_info['finder_details']:
        print(f"  Finder {fd[0]}: similarity={fd[3]:.2f}, exact={fd[4]}")
    if qr_info.get('h_timing_match'):
        print(f"  H timing match: {qr_info['h_timing_match']:.2f}")
    if qr_info.get('v_timing_match'):
        print(f"  V timing match: {qr_info['v_timing_match']:.2f}")
    
    # Search for finder patterns anywhere
    finders = find_all_finder_patterns(grid)
    if finders:
        print(f"  Found {len(finders)} finder-like patterns:")
        for r, c, sim, exact in finders[:10]:
            print(f"    ({r},{c}): similarity={sim:.2f}, exact={exact}")
    
    # Try to decode
    results = try_decode_as_barcode(grid, "full_grid")
    all_results.extend(results)
    
    save_grid_image(grid, os.path.join(output_dir, "grid_full.png"), cell_size=10)
    
    # --- Test 0b: Full grid rotations ---
    for angle, rot_func in [(90, rotate_90), (180, rotate_180), (270, rotate_270)]:
        print(f"\n--- Test 0b: Full grid rotated {angle} degrees ---")
        rotated = rot_func(grid)
        qr_info = check_qr_structure(rotated)
        finders = find_all_finder_patterns(rotated)
        if finders:
            print(f"  Found {len(finders)} finder-like patterns")
            for r, c, sim, exact in finders[:5]:
                print(f"    ({r},{c}): similarity={sim:.2f}, exact={exact}")
        results = try_decode_as_barcode(rotated, f"full_grid_rot{angle}")
        all_results.extend(results)
    
    # --- Test 1: Left/Right OR overlay ---
    print(f"\n--- Test 1: Left/Right OR overlay ---")
    for center_mode in ['left', 'right', 'both', 'neither']:
        left, right = split_left_right(grid, include_center=center_mode)
        
        # Make same size by padding if needed
        max_cols = max(left.shape[1], right.shape[1])
        if left.shape[1] < max_cols:
            left = np.pad(left, ((0,0),(0,max_cols-left.shape[1])), constant_values=0)
        if right.shape[1] < max_cols:
            right = np.pad(right, ((0,0),(0,max_cols-right.shape[1])), constant_values=0)
        
        overlay = overlay_or(left, right)
        print(f"  Center={center_mode}: overlay shape={overlay.shape}, black={np.sum(overlay)}")
        
        finders = find_all_finder_patterns(overlay)
        if finders:
            print(f"  ** Found {len(finders)} finder-like patterns! **")
            for r, c, sim, exact in finders[:5]:
                print(f"    ({r},{c}): similarity={sim:.2f}, exact={exact}")
        
        results = try_decode_as_barcode(overlay, f"LR_OR_{center_mode}")
        all_results.extend(results)
        
        save_grid_image(overlay, os.path.join(output_dir, f"overlay_LR_OR_{center_mode}.png"), cell_size=10)
    
    # --- Test 2: Left/Right-mirrored OR overlay ---
    print(f"\n--- Test 2: Left/Right-mirrored OR overlay ---")
    for center_mode in ['left', 'right', 'neither']:
        left, right = split_left_right(grid, include_center=center_mode)
        right_mirrored = mirror_horizontal(right)
        
        max_cols = max(left.shape[1], right_mirrored.shape[1])
        if left.shape[1] < max_cols:
            left_p = np.pad(left, ((0,0),(0,max_cols-left.shape[1])), constant_values=0)
        else:
            left_p = left
        if right_mirrored.shape[1] < max_cols:
            right_p = np.pad(right_mirrored, ((0,0),(0,max_cols-right_mirrored.shape[1])), constant_values=0)
        else:
            right_p = right_mirrored
        
        overlay = overlay_or(left_p, right_p)
        print(f"  Center={center_mode}: overlay shape={overlay.shape}, black={np.sum(overlay)}")
        
        finders = find_all_finder_patterns(overlay)
        if finders:
            print(f"  ** Found {len(finders)} finder-like patterns! **")
            for r, c, sim, exact in finders[:5]:
                print(f"    ({r},{c}): similarity={sim:.2f}, exact={exact}")
        
        results = try_decode_as_barcode(overlay, f"LR_mirror_OR_{center_mode}")
        all_results.extend(results)
        
        save_grid_image(overlay, os.path.join(output_dir, f"overlay_LR_mirror_OR_{center_mode}.png"), cell_size=10)
    
    # --- Test 3: Left-mirrored / Right OR overlay ---
    print(f"\n--- Test 3: Left-mirrored / Right OR overlay ---")
    for center_mode in ['left', 'right', 'neither']:
        left, right = split_left_right(grid, include_center=center_mode)
        left_mirrored = mirror_horizontal(left)
        
        max_cols = max(left_mirrored.shape[1], right.shape[1])
        if left_mirrored.shape[1] < max_cols:
            left_p = np.pad(left_mirrored, ((0,0),(0,max_cols-left_mirrored.shape[1])), constant_values=0)
        else:
            left_p = left_mirrored
        if right.shape[1] < max_cols:
            right_p = np.pad(right, ((0,0),(0,max_cols-right.shape[1])), constant_values=0)
        else:
            right_p = right
        
        overlay = overlay_or(left_p, right_p)
        print(f"  Center={center_mode}: overlay shape={overlay.shape}, black={np.sum(overlay)}")
        
        finders = find_all_finder_patterns(overlay)
        if finders:
            print(f"  ** Found {len(finders)} finder-like patterns! **")
            for r, c, sim, exact in finders[:5]:
                print(f"    ({r},{c}): similarity={sim:.2f}, exact={exact}")
        
        results = try_decode_as_barcode(overlay, f"mirrorL_R_OR_{center_mode}")
        all_results.extend(results)
    
    # --- Test 4: AND and XOR overlays ---
    print(f"\n--- Test 4: AND and XOR overlays ---")
    for op_name, op_func in [("AND", overlay_and), ("XOR", overlay_xor)]:
        for center_mode in ['left', 'neither']:
            left, right = split_left_right(grid, include_center=center_mode)
            right_mirrored = mirror_horizontal(right)
            
            max_cols = max(left.shape[1], right_mirrored.shape[1])
            left_p = np.pad(left, ((0,0),(0,max(0, max_cols-left.shape[1]))), constant_values=0)[:,:max_cols]
            right_p = np.pad(right_mirrored, ((0,0),(0,max(0, max_cols-right_mirrored.shape[1]))), constant_values=0)[:,:max_cols]
            
            overlay = op_func(left_p, right_p)
            print(f"  {op_name} center={center_mode}: black={np.sum(overlay)}")
            
            finders = find_all_finder_patterns(overlay)
            if finders:
                print(f"  ** Found {len(finders)} finder-like patterns! **")
                for r, c, sim, exact in finders[:5]:
                    print(f"    ({r},{c}): similarity={sim:.2f}, exact={exact}")
            
            results = try_decode_as_barcode(overlay, f"LR_{op_name}_{center_mode}")
            all_results.extend(results)
            
            save_grid_image(overlay, os.path.join(output_dir, f"overlay_LR_{op_name}_{center_mode}.png"), cell_size=10)
    
    # --- Test 5: Top/Bottom overlay ---
    print(f"\n--- Test 5: Top/Bottom overlay ---")
    mid_row = n_rows // 2
    top = grid[:mid_row, :]
    bottom = grid[mid_row:, :] if n_rows % 2 == 0 else grid[mid_row+1:, :]
    bottom_flipped = mirror_vertical(bottom)
    
    min_rows = min(top.shape[0], bottom_flipped.shape[0])
    for op_name, op_func in [("OR", overlay_or), ("AND", overlay_and), ("XOR", overlay_xor)]:
        overlay = op_func(top[:min_rows, :], bottom_flipped[:min_rows, :])
        print(f"  TB {op_name}: shape={overlay.shape}, black={np.sum(overlay)}")
        
        finders = find_all_finder_patterns(overlay)
        if finders:
            print(f"  ** Found {len(finders)} finder-like patterns! **")
            for r, c, sim, exact in finders[:5]:
                print(f"    ({r},{c}): similarity={sim:.2f}, exact={exact}")
        
        results = try_decode_as_barcode(overlay, f"TB_{op_name}")
        all_results.extend(results)
    
    # --- Test 6: Quadrant overlays ---
    print(f"\n--- Test 6: Quadrant overlays ---")
    mid_row = n_rows // 2
    mid_col = n_cols // 2
    
    q1 = grid[:mid_row, :mid_col]  # top-left
    q2 = grid[:mid_row, mid_col+1:] if n_cols % 2 == 1 else grid[:mid_row, mid_col:]  # top-right
    q3 = grid[mid_row+1:, :mid_col] if n_rows % 2 == 1 else grid[mid_row:, :mid_col]  # bottom-left
    q4_r_start = mid_row+1 if n_rows % 2 == 1 else mid_row
    q4_c_start = mid_col+1 if n_cols % 2 == 1 else mid_col
    q4 = grid[q4_r_start:, q4_c_start:]  # bottom-right
    
    # Make all quadrants the same size
    min_r = min(q1.shape[0], q2.shape[0], q3.shape[0], q4.shape[0])
    min_c = min(q1.shape[1], q2.shape[1], q3.shape[1], q4.shape[1])
    q1 = q1[:min_r, :min_c]
    q2 = q2[:min_r, :min_c]
    q3 = q3[:min_r, :min_c]
    q4 = q4[:min_r, :min_c]
    
    # Try various quadrant combinations with mirroring
    combos = [
        ("q1 OR mirror(q2)", q1, mirror_horizontal(q2)),
        ("q1 OR flipV(q3)", q1, mirror_vertical(q3)),
        ("q1 OR mirror(flipV(q4))", q1, mirror_horizontal(mirror_vertical(q4))),
        ("all 4 OR", None, None),  # special case
    ]
    
    for combo_name, a, b in combos:
        if combo_name == "all 4 OR":
            overlay = overlay_or(overlay_or(q1, mirror_horizontal(q2)),
                               overlay_or(mirror_vertical(q3), mirror_horizontal(mirror_vertical(q4))))
        else:
            overlay = overlay_or(a, b)
        
        print(f"  {combo_name}: shape={overlay.shape}, black={np.sum(overlay)}")
        
        finders = find_all_finder_patterns(overlay)
        if finders:
            print(f"  ** Found {len(finders)} finder-like patterns! **")
            for r, c, sim, exact in finders[:5]:
                print(f"    ({r},{c}): similarity={sim:.2f}, exact={exact}")
        
        results = try_decode_as_barcode(overlay, combo_name)
        all_results.extend(results)
    
    # --- Test 7: Try making 21x21 from grid if not already ---
    if n_rows != 21 or n_cols != 21:
        print(f"\n--- Test 7: Resize/crop to 21x21 for QR Version 1 ---")
        # Try cropping to 21x21 from center
        r_start = max(0, (n_rows - 21) // 2)
        c_start = max(0, (n_cols - 21) // 2)
        if n_rows >= 21 and n_cols >= 21:
            cropped = grid[r_start:r_start+21, c_start:c_start+21]
            print(f"  Cropped from ({r_start},{c_start})")
            qr_info = check_qr_structure(cropped)
            for fd in qr_info['finder_details']:
                print(f"  Finder {fd[0]}: similarity={fd[3]:.2f}")
            results = try_decode_as_barcode(cropped, "cropped_21x21")
            all_results.extend(results)
            save_grid_image(cropped, os.path.join(output_dir, "grid_cropped_21x21.png"), cell_size=10)
    
    # --- Test 8: Try 25x25 (QR Version 2) ---
    if n_rows >= 25 and n_cols >= 25 and (n_rows != 25 or n_cols != 25):
        print(f"\n--- Test 8: Crop to 25x25 for QR Version 2 ---")
        r_start = max(0, (n_rows - 25) // 2)
        c_start = max(0, (n_cols - 25) // 2)
        cropped25 = grid[r_start:r_start+25, c_start:c_start+25]
        qr_info = check_qr_structure(cropped25)
        for fd in qr_info['finder_details']:
            print(f"  Finder {fd[0]}: similarity={fd[3]:.2f}")
        results = try_decode_as_barcode(cropped25, "cropped_25x25")
        all_results.extend(results)
    
    # --- Test 9: Try existing images directly ---
    print(f"\n--- Test 9: Direct barcode scan of crossword images ---")
    image_paths = [
        "/home/user/MB/screenshots/Crossword.png",
        "/home/user/MB/screenshots/Close up of crossword grey.png",
        "/home/user/MB/screenshots/Possible QR overlap from video.png",
    ]
    
    for img_path in image_paths:
        if os.path.exists(img_path):
            name = os.path.basename(img_path)
            print(f"  Scanning {name}...")
            img = Image.open(img_path)
            
            # Try direct
            if HAS_PYZBAR:
                try:
                    decoded = pyzbar_decode(img)
                    for d in decoded:
                        result = f"pyzbar ({name}): {d.type} = {d.data.decode('utf-8', errors='replace')}"
                        all_results.append(result)
                        print(f"  FOUND: {result}")
                except:
                    pass
            
            if HAS_DMTX:
                try:
                    decoded = dmtx_decode(img, timeout=3000)
                    for d in decoded:
                        result = f"dmtx ({name}): DataMatrix = {d.data.decode('utf-8', errors='replace')}"
                        all_results.append(result)
                        print(f"  FOUND: {result}")
                except:
                    pass
            
            # Try grayscale + thresholded versions
            gray_img = img.convert('L')
            for thresh in [128, 160, 200]:
                bw = gray_img.point(lambda p: 255 if p > thresh else 0)
                if HAS_PYZBAR:
                    try:
                        decoded = pyzbar_decode(bw)
                        for d in decoded:
                            result = f"pyzbar ({name}, thresh={thresh}): {d.type} = {d.data.decode('utf-8', errors='replace')}"
                            all_results.append(result)
                            print(f"  FOUND: {result}")
                    except:
                        pass
    
    return all_results


# ============================================================
# SECTION 6: Direct scan of the "Possible QR overlap" image
# ============================================================

def analyze_qr_overlap_image():
    """Special analysis of the 'Possible QR overlap from video.png' image."""
    img_path = "/home/user/MB/screenshots/Possible QR overlap from video.png"
    if not os.path.exists(img_path):
        print("QR overlap image not found")
        return []
    
    print(f"\n{'='*60}")
    print("SPECIAL: Analyzing 'Possible QR overlap from video.png'")
    print(f"{'='*60}")
    
    img = Image.open(img_path)
    arr = np.array(img)
    gray = np.mean(arr, axis=2) if len(arr.shape) == 3 else arr.astype(float)
    h, w = gray.shape
    
    print(f"  Image: {w}x{h}")
    
    results = []
    
    # Try various threshold levels
    for thresh in [80, 100, 120, 140, 160, 180, 200]:
        binary = (gray < thresh).astype(int)
        
        # Try to detect QR finder patterns in binary image
        finders = find_all_finder_patterns(binary)
        if finders:
            print(f"  Threshold {thresh}: Found {len(finders)} finder-like patterns!")
            for r, c, sim, exact in finders[:5]:
                print(f"    ({r},{c}): similarity={sim:.2f}, exact={exact}")
    
    # Try pyzbar and dmtx on various versions
    for thresh in [80, 100, 120, 140, 160, 180, 200]:
        bw = img.convert('L').point(lambda p: 255 if p > thresh else 0)
        
        if HAS_PYZBAR:
            try:
                decoded = pyzbar_decode(bw)
                for d in decoded:
                    result = f"QR_overlap thresh={thresh}: {d.type} = {d.data.decode('utf-8', errors='replace')}"
                    results.append(result)
                    print(f"  FOUND: {result}")
            except:
                pass
        
        if HAS_DMTX:
            try:
                decoded = dmtx_decode(bw, timeout=2000)
                for d in decoded:
                    result = f"QR_overlap dmtx thresh={thresh}: {d.data.decode('utf-8', errors='replace')}"
                    results.append(result)
                    print(f"  FOUND: {result}")
            except:
                pass
    
    # Also try inverted
    inv_img = Image.eval(img.convert('L'), lambda p: 255 - p)
    if HAS_PYZBAR:
        try:
            decoded = pyzbar_decode(inv_img)
            for d in decoded:
                result = f"QR_overlap INVERTED: {d.type} = {d.data.decode('utf-8', errors='replace')}"
                results.append(result)
                print(f"  FOUND: {result}")
        except:
            pass
    
    return results


# ============================================================
# MAIN
# ============================================================

def main():
    output_dir = "/home/user/MB/analysis/qr_overlay"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("QR CODE OVERLAY TEST")
    print("MrBeast Million Dollar Crossword")
    print("=" * 60)
    
    # Step 1: Extract grid from crossword image
    print(f"\n{'='*60}")
    print("STEP 1: Extract grid from crossword image")
    print(f"{'='*60}")
    
    img_path = "/home/user/MB/screenshots/Crossword.png"
    grid = extract_grid_from_image(img_path)
    
    n_rows, n_cols = grid.shape
    print(f"\nExtracted grid: {n_cols}x{n_rows}")
    print(f"Black cells: {np.sum(grid)}")
    print(f"White cells: {np.sum(1-grid)}")
    
    print_grid(grid, "Extracted Crossword Grid")
    
    # Validate against known ACROSS/DOWN
    print(f"\n{'='*60}")
    print("STEP 2: Validate grid numbering")
    print(f"{'='*60}")
    
    numbers, across_nums, down_nums = extract_grid_with_numbering(grid)
    
    # Known lists from map_grid.py
    ACROSS_EXPECTED = [1,8,14,22,23,24,25,28,29,30,31,32,34,35,36,38,41,42,43,45,47,48,50,54,57,58,59,61,63,64,66,68,70,72,73,77,79,80,81,82,83,85,88,90,91,92,94,97,99,100,102,103,105,106,107,109,111,113,114,117,119,120,121,123,124,127,129,132,134,136,138,141,143,145,147,148,149,153,155,156,158,159,161,164,165,167,171,172,173,174,175,176]
    DOWN_EXPECTED = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,26,27,33,37,39,40,43,44,46,49,51,52,53,55,56,60,62,65,67,69,71,72,74,75,76,77,78,80,83,84,86,87,89,93,95,96,98,101,104,108,110,112,115,116,117,118,122,124,125,126,128,130,131,133,135,137,139,140,141,142,144,150,151,152,153,154,157,160,162,163,166,168,169,170]
    
    print(f"Computed: {len(across_nums)} across, {len(down_nums)} down, max number={max(across_nums + down_nums) if across_nums or down_nums else 0}")
    print(f"Expected: {len(ACROSS_EXPECTED)} across, {len(DOWN_EXPECTED)} down, max=176")
    
    across_match = set(across_nums) == set(ACROSS_EXPECTED)
    down_match = set(down_nums) == set(DOWN_EXPECTED)
    print(f"Across match: {across_match}")
    print(f"Down match: {down_match}")
    
    if not across_match:
        missing = set(ACROSS_EXPECTED) - set(across_nums)
        extra = set(across_nums) - set(ACROSS_EXPECTED)
        if missing:
            print(f"  Missing across: {sorted(missing)[:20]}")
        if extra:
            print(f"  Extra across: {sorted(extra)[:20]}")
    
    if not down_match:
        missing = set(DOWN_EXPECTED) - set(down_nums)
        extra = set(down_nums) - set(DOWN_EXPECTED)
        if missing:
            print(f"  Missing down: {sorted(missing)[:20]}")
        if extra:
            print(f"  Extra down: {sorted(extra)[:20]}")
    
    # Step 3: Run all QR overlay tests
    print(f"\n{'='*60}")
    print("STEP 3: QR overlay tests")
    print(f"{'='*60}")
    
    all_results = run_all_tests(grid, output_dir)
    
    # Step 4: Analyze the "Possible QR overlap" image
    qr_results = analyze_qr_overlap_image()
    all_results.extend(qr_results)
    
    # Step 5: Summary
    print(f"\n{'='*60}")
    print("SUMMARY OF ALL FINDINGS")
    print(f"{'='*60}")
    
    if all_results:
        print(f"\nTotal barcode/QR detections: {len(all_results)}")
        for r in all_results:
            print(f"  - {r}")
    else:
        print("\nNo barcodes or QR codes were detected in any configuration.")
        print("\nPossible explanations:")
        print("  1. The grid extraction may be imprecise (image resolution)")
        print("  2. The overlay theory may require a different operation")
        print("  3. The QR code may need the FILLED crossword (not just black cells)")
        print("  4. The grid may need additional transformation")
        print("  5. The 'QR overlap' theory may not apply to this puzzle")
    
    # Save grid data for reference
    grid_file = os.path.join(output_dir, "extracted_grid.json")
    with open(grid_file, 'w') as f:
        json.dump({
            'grid': grid.tolist(),
            'dimensions': [n_rows, n_cols],
            'black_cells': int(np.sum(grid)),
            'white_cells': int(np.sum(1-grid)),
            'across_nums': across_nums,
            'down_nums': down_nums,
        }, f, indent=2)
    print(f"\nGrid data saved to {grid_file}")
    
    return all_results


if __name__ == '__main__':
    main()
