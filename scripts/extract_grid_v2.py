#!/usr/bin/env python3
"""
Extract the 21x21 crossword grid from the Million-Dollar-Crossword PDF.

Strategy:
1. Render PDF at high zoom with PyMuPDF
2. Crop to approximate grid region
3. Systematically search for the correct grid alignment by varying the
   top-left corner position in small increments
4. For each alignment, extract the 21x21 grid and validate against
   known ACROSS/DOWN entry lists
5. If exact alignment found, save results; otherwise use hill climbing
   to fix remaining errors
"""

import json
import os
import numpy as np
from PIL import Image, ImageDraw

# ---------------------------------------------------------------------------
# Known entry lists from the puzzle
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
N = 21  # Grid size


def number_grid(grid):
    """Standard crossword numbering. Returns dict: num -> {row, col, across, down}"""
    n = len(grid)
    numbering = {}
    num = 1
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                continue
            sa = (c == 0 or grid[r][c-1] == 1) and (c + 1 < n and grid[r][c+1] == 0)
            sd = (r == 0 or grid[r-1][c] == 1) and (r + 1 < n and grid[r+1][c] == 0)
            if sa or sd:
                numbering[num] = {'row': r, 'col': c, 'across': sa, 'down': sd}
                num += 1
    return numbering


def score_grid(grid):
    """
    Score how well a grid matches the known ACROSS/DOWN lists.
    Returns (score, details_dict).
    Higher score = better match.
    """
    numbering = number_grid(grid)
    comp_across = {n for n, info in numbering.items() if info['across']}
    comp_down = {n for n, info in numbering.items() if info['down']}

    a_correct = len(comp_across & ACROSS_SET)
    d_correct = len(comp_down & DOWN_SET)
    a_extra = len(comp_across - ACROSS_SET)
    d_extra = len(comp_down - DOWN_SET)
    a_missing = len(ACROSS_SET - comp_across)
    d_missing = len(DOWN_SET - comp_down)

    max_num = max(numbering.keys()) if numbering else 0
    total_nums = len(numbering)

    # Score: correct matches minus penalties for extras and missing
    score = (a_correct + d_correct) - 2 * (a_extra + d_extra) - (a_missing + d_missing)

    details = {
        'total_nums': total_nums,
        'max_num': max_num,
        'a_correct': a_correct, 'a_extra': a_extra, 'a_missing': a_missing,
        'd_correct': d_correct, 'd_extra': d_extra, 'd_missing': d_missing,
        'score': score,
        'perfect': (a_extra == 0 and d_extra == 0 and a_missing == 0 and d_missing == 0
                    and max_num == MAX_NUM),
    }
    return score, details


def validate_grid(grid):
    """Check if grid exactly matches known entry lists."""
    numbering = number_grid(grid)
    comp_across = {n for n, info in numbering.items() if info['across']}
    comp_down = {n for n, info in numbering.items() if info['down']}

    # Note: number 146 is missing from both lists (likely an omission).
    # We accept the grid if all listed numbers match AND no wrong extras exist,
    # even if 146 appears as an extra.
    a_match = comp_across >= ACROSS_SET  # all expected across entries present
    d_match = comp_down >= DOWN_SET      # all expected down entries present
    a_no_wrong_extra = (comp_across - ACROSS_SET) <= {146}  # only 146 allowed as extra
    d_no_wrong_extra = (comp_down - DOWN_SET) <= {146}

    max_num = max(numbering.keys()) if numbering else 0

    valid = a_match and d_match and a_no_wrong_extra and d_no_wrong_extra and max_num == MAX_NUM
    return valid, numbering


def compute_entry_lengths(grid, numbering):
    """Compute entry lengths for all across and down entries."""
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


# ===================================================================
# IMAGE EXTRACTION
# ===================================================================

def load_grid_image():
    """Load and render the PDF page as a grayscale numpy array."""
    import fitz

    pdf_path = "/home/user/MB/puzzles/Million-Dollar-Crossword.pdf"
    doc = fitz.open(pdf_path)
    page = doc[0]

    zoom = 6
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
        pix.height, pix.width, pix.n)
    gray = np.mean(img_data[:, :, :3], axis=2)
    doc.close()

    return gray, pix.width, pix.height


def find_grid_bounds(gray, W, H):
    """
    Find the precise bounding box of the crossword grid.
    Returns (x0, y0, x1, y1) in pixel coordinates of the full image.
    These define the outer edges of the grid (from the outside of the
    first grid line to the outside of the last grid line).
    """
    # The grid is in the upper-right area of the page.
    # Approximate region: x: 30-90%, y: 3-55%
    crop_x1 = int(W * 0.30)
    crop_y1 = int(H * 0.03)
    crop_x2 = int(W * 0.92)
    crop_y2 = int(H * 0.55)
    region = gray[crop_y1:crop_y2, crop_x1:crop_x2]

    # Find grid lines by looking at column/row darkness profiles
    # A grid line appears as a dark column/row in the region.

    # Vertical profile (for finding vertical grid lines = x positions)
    # Average each column
    col_profile = np.mean(region, axis=0)

    # Horizontal profile (for finding horizontal grid lines = y positions)
    row_profile = np.mean(region, axis=1)

    # Find the grid extent by looking for the region with many dark lines.
    # The grid has 22 evenly-spaced lines in each direction.

    # Find dark columns (potential vertical grid lines)
    from scipy.signal import find_peaks
    dark_cols = np.max(col_profile) - col_profile  # invert: peaks = dark lines
    v_peaks, v_props = find_peaks(dark_cols, height=30, distance=30)

    dark_rows = np.max(row_profile) - row_profile
    h_peaks, h_props = find_peaks(dark_rows, height=30, distance=30)

    print(f"Found {len(v_peaks)} vertical line candidates, {len(h_peaks)} horizontal line candidates")

    # We need exactly 22 of each. If we have more, filter by regularity.
    # Find the best set of 22 evenly-spaced peaks.
    def find_best_22(peaks, label):
        """Find the best subset of 22 evenly-spaced peaks."""
        if len(peaks) < 22:
            print(f"  Warning: only {len(peaks)} {label} peaks found")
            return peaks

        if len(peaks) == 22:
            return peaks

        # Try each possible spacing and offset
        best_subset = None
        best_score = -1

        for i in range(len(peaks)):
            for j in range(i+1, min(i+5, len(peaks))):
                spacing = (peaks[j] - peaks[i]) / (j - i)
                if spacing < 50 or spacing > 100:
                    continue

                # Generate expected positions
                expected = [peaks[i] + k * spacing for k in range(22)]
                if expected[-1] > peaks[-1] + 20:
                    continue

                # Count matches
                matched = 0
                for exp in expected:
                    dists = np.abs(peaks - exp)
                    if np.min(dists) < 10:
                        matched += 1

                if matched > best_score:
                    best_score = matched
                    best_subset = expected

        if best_subset is not None:
            # Snap to nearest actual peaks
            result = []
            for exp in best_subset:
                dists = np.abs(peaks - exp)
                idx = np.argmin(dists)
                if dists[idx] < 15:
                    result.append(peaks[idx])
                else:
                    result.append(int(round(exp)))
            print(f"  Best {label} lines: matched {best_score}/22 peaks, spacing ~ {spacing:.1f}")
            return np.array(result)

        return peaks[:22]

    v_lines = find_best_22(v_peaks, "vertical")
    h_lines = find_best_22(h_peaks, "horizontal")

    # Convert to full image coordinates
    v_lines_abs = v_lines + crop_x1
    h_lines_abs = h_lines + crop_y1

    return v_lines_abs, h_lines_abs, gray


def extract_grid_at_alignment(gray, v_lines, h_lines, threshold=80):
    """
    Extract 21x21 grid using specified grid line positions.
    v_lines and h_lines are in absolute image coordinates.
    """
    grid = []
    for r in range(21):
        row = []
        for c in range(21):
            y1, y2 = int(h_lines[r]), int(h_lines[r+1])
            x1, x2 = int(v_lines[c]), int(v_lines[c+1])
            dy, dx = y2 - y1, x2 - x1

            # Sample inner region (avoiding grid lines)
            margin_y = max(2, int(dy * 0.25))
            margin_x = max(2, int(dx * 0.25))
            cy1 = y1 + margin_y
            cy2 = y2 - margin_y
            cx1 = x1 + margin_x
            cx2 = x2 - margin_x

            H_img, W_img = gray.shape
            cy1, cy2 = max(0, cy1), min(H_img, cy2)
            cx1, cx2 = max(0, cx1), min(W_img, cx2)

            cell = gray[cy1:cy2, cx1:cx2]
            if cell.size > 0:
                avg = np.median(cell)  # Use median for robustness
            else:
                avg = 255

            row.append(1 if avg < threshold else 0)
        grid.append(row)

    return grid


def search_grid_alignment(gray, W, H):
    """
    Systematically search for the correct grid alignment by varying
    the top-left corner and cell spacing.
    """
    print("\n" + "=" * 70)
    print("SYSTEMATIC GRID ALIGNMENT SEARCH")
    print("=" * 70)

    v_lines_abs, h_lines_abs, _ = find_grid_bounds(gray, W, H)

    # Compute average spacings
    v_spacing = np.mean(np.diff(v_lines_abs))
    h_spacing = np.mean(np.diff(h_lines_abs))
    print(f"\nDetected spacings: vertical={v_spacing:.2f}, horizontal={h_spacing:.2f}")
    print(f"V-lines range: {v_lines_abs[0]} to {v_lines_abs[-1]}")
    print(f"H-lines range: {h_lines_abs[0]} to {h_lines_abs[-1]}")

    # Try the directly detected lines first
    best_grid = None
    best_score = -999
    best_details = None
    best_alignment = None

    for threshold in [50, 80, 100, 128, 150]:
        grid = extract_grid_at_alignment(gray, v_lines_abs, h_lines_abs, threshold)
        sc, det = score_grid(grid)
        black_count = sum(sum(row) for row in grid)
        print(f"\nThreshold={threshold}: score={sc}, max_num={det['max_num']}, "
              f"blacks={black_count}, a_correct={det['a_correct']}/{len(ACROSS)}, "
              f"d_correct={det['d_correct']}/{len(DOWN)}")
        if sc > best_score:
            best_score = sc
            best_grid = [row[:] for row in grid]
            best_details = det
            best_alignment = ('detected', threshold)
        if det['perfect']:
            print("  PERFECT MATCH!")
            return grid, det

    print(f"\nBest detected-line result: score={best_score}")

    # Now try shifting the grid by small amounts
    # Use the best threshold
    best_thresh = best_alignment[1]

    print(f"\nSearching over grid offsets (threshold={best_thresh})...")

    # The grid might have a different starting position.
    # Try shifting both vertical and horizontal lines.
    # Use uniform spacing based on detected average.

    # Try different spacings too
    for spacing_delta in [-1.0, -0.5, 0, 0.5, 1.0]:
        spacing = (v_spacing + h_spacing) / 2 + spacing_delta

        for dy in range(-30, 31, 2):
            for dx in range(-15, 16, 2):
                # Generate uniform grid lines
                v0 = v_lines_abs[0] + dx
                h0 = h_lines_abs[0] + dy

                v_test = np.array([v0 + i * spacing for i in range(22)])
                h_test = np.array([h0 + i * spacing for i in range(22)])

                # Quick bounds check
                if v_test[-1] >= W or h_test[-1] >= H or v_test[0] < 0 or h_test[0] < 0:
                    continue

                grid = extract_grid_at_alignment(gray, v_test, h_test, best_thresh)
                sc, det = score_grid(grid)

                if sc > best_score:
                    best_score = sc
                    best_grid = [row[:] for row in grid]
                    best_details = det
                    best_alignment = (f'offset dy={dy} dx={dx} sp={spacing:.1f}', best_thresh)
                    print(f"  New best: {best_alignment[0]}, score={sc}, "
                          f"max_num={det['max_num']}, "
                          f"a={det['a_correct']}/{len(ACROSS)}, "
                          f"d={det['d_correct']}/{len(DOWN)}")

                if det['perfect']:
                    print("  PERFECT MATCH!")
                    return grid, det

    # Try with per-axis spacing (non-square cells)
    print(f"\nTrying non-square cell spacings...")
    for v_sp_delta in [-2, -1, 0, 1, 2]:
        for h_sp_delta in [-2, -1, 0, 1, 2]:
            v_sp = v_spacing + v_sp_delta * 0.3
            h_sp = h_spacing + h_sp_delta * 0.3

            for dy in range(-20, 21, 3):
                for dx in range(-10, 11, 3):
                    v0 = v_lines_abs[0] + dx
                    h0 = h_lines_abs[0] + dy

                    v_test = np.array([v0 + i * v_sp for i in range(22)])
                    h_test = np.array([h0 + i * h_sp for i in range(22)])

                    if v_test[-1] >= W or h_test[-1] >= H or v_test[0] < 0 or h_test[0] < 0:
                        continue

                    grid = extract_grid_at_alignment(gray, v_test, h_test, best_thresh)
                    sc, det = score_grid(grid)

                    if sc > best_score:
                        best_score = sc
                        best_grid = [row[:] for row in grid]
                        best_details = det
                        best_alignment = (f'offset dy={dy} dx={dx} v_sp={v_sp:.1f} h_sp={h_sp:.1f}', best_thresh)
                        print(f"  New best: {best_alignment[0]}, score={sc}, "
                              f"max_num={det['max_num']}")

                    if det['perfect']:
                        print("  PERFECT MATCH!")
                        return grid, det

    print(f"\nBest alignment search result: score={best_score}, alignment={best_alignment}")
    print(f"  Details: {best_details}")

    return best_grid, best_details


# ===================================================================
# HILL CLIMBING
# ===================================================================

def hill_climb(grid, max_rounds=100):
    """Fix grid using hill climbing on the validation score."""
    print("\n" + "=" * 70)
    print("HILL CLIMBING")
    print("=" * 70)

    best_grid = [row[:] for row in grid]
    best_sc, best_det = score_grid(best_grid)
    print(f"Initial: score={best_sc}, max_num={best_det['max_num']}, "
          f"a={best_det['a_correct']}/{len(ACROSS)}, d={best_det['d_correct']}/{len(DOWN)}")

    if best_det['perfect']:
        return best_grid

    # Phase 1: Single-cell flips
    for round_num in range(max_rounds):
        improved = False
        for r in range(N):
            for c in range(N):
                best_grid[r][c] = 1 - best_grid[r][c]
                sc, det = score_grid(best_grid)
                if sc > best_sc:
                    best_sc = sc
                    best_det = det
                    improved = True
                    if det['perfect']:
                        print(f"  Round {round_num}: PERFECT at ({r},{c})! score={sc}")
                        return best_grid
                else:
                    best_grid[r][c] = 1 - best_grid[r][c]

        if not improved:
            print(f"  Single-flip converged at round {round_num}, score={best_sc}")
            break
        print(f"  Round {round_num}: score={best_sc}, max_num={best_det['max_num']}, "
              f"a={best_det['a_correct']}/{len(ACROSS)}, d={best_det['d_correct']}/{len(DOWN)}")

    if best_det['perfect']:
        return best_grid

    # Phase 2: 2-cell flips
    print("  Trying 2-cell flips...")
    for round_num in range(20):
        improved = False
        for r1 in range(N):
            for c1 in range(N):
                best_grid[r1][c1] = 1 - best_grid[r1][c1]
                # Check single flip first
                sc1, det1 = score_grid(best_grid)
                if sc1 > best_sc:
                    best_sc = sc1
                    best_det = det1
                    improved = True
                    if det1['perfect']:
                        print(f"  2-flip round {round_num}: PERFECT!")
                        return best_grid
                    continue  # Keep this flip, continue

                for r2 in range(N):
                    start_c2 = 0
                    if r2 == r1:
                        start_c2 = c1 + 1
                    elif r2 < r1:
                        continue
                    for c2 in range(start_c2, N):
                        best_grid[r2][c2] = 1 - best_grid[r2][c2]
                        sc, det = score_grid(best_grid)
                        if sc > best_sc:
                            best_sc = sc
                            best_det = det
                            improved = True
                            if det['perfect']:
                                print(f"  2-flip round {round_num}: PERFECT!")
                                return best_grid
                            # Keep both flips, move on
                            break
                        else:
                            best_grid[r2][c2] = 1 - best_grid[r2][c2]
                    else:
                        continue
                    break  # Found improvement with (r1,c1)+(r2,c2)
                else:
                    # No 2nd flip improved. Undo first flip.
                    best_grid[r1][c1] = 1 - best_grid[r1][c1]

        if not improved:
            print(f"  2-flip converged at round {round_num}, score={best_sc}")
            break
        print(f"  2-flip round {round_num}: score={best_sc}, max_num={best_det['max_num']}")

    return best_grid


# ===================================================================
# TARGETED FIX: Analyze numbering errors and fix specific cells
# ===================================================================

def targeted_fix(grid):
    """
    Analyze which numbers have wrong roles and try to fix them
    by strategically flipping cells near the problem areas.
    """
    print("\n" + "=" * 70)
    print("TARGETED FIX")
    print("=" * 70)

    best_grid = [row[:] for row in grid]
    numbering = number_grid(best_grid)
    comp_across = {n for n, info in numbering.items() if info['across']}
    comp_down = {n for n, info in numbering.items() if info['down']}

    print(f"Current: {len(numbering)} numbers, max={max(numbering.keys()) if numbering else 0}")

    # Find problem numbers
    wrong_across = comp_across - ACROSS_SET - {146}
    missing_across = ACROSS_SET - comp_across
    wrong_down = comp_down - DOWN_SET - {146}
    missing_down = DOWN_SET - comp_down

    print(f"Wrong across (should not be across): {sorted(wrong_across)}")
    print(f"Missing across (should be across): {sorted(missing_across)}")
    print(f"Wrong down (should not be down): {sorted(wrong_down)}")
    print(f"Missing down (should be down): {sorted(missing_down)}")

    # For each wrong number, find its position and try local fixes
    all_problems = sorted(
        [(n, 'wrong_across') for n in wrong_across] +
        [(n, 'missing_across') for n in missing_across] +
        [(n, 'wrong_down') for n in wrong_down] +
        [(n, 'missing_down') for n in missing_down]
    )

    for num, problem in all_problems:
        if num not in numbering:
            continue  # Can't find position

        r, c = numbering[num]['row'], numbering[num]['col']

        # Try flipping cells around (r, c)
        neighbors = []
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    neighbors.append((nr, nc))

        best_local_sc, _ = score_grid(best_grid)

        for nr, nc in neighbors:
            best_grid[nr][nc] = 1 - best_grid[nr][nc]
            sc, det = score_grid(best_grid)
            if sc > best_local_sc:
                best_local_sc = sc
                if det['perfect']:
                    print(f"  PERFECT after fixing ({nr},{nc}) for num {num}!")
                    return best_grid
            else:
                best_grid[nr][nc] = 1 - best_grid[nr][nc]

    sc, det = score_grid(best_grid)
    print(f"After targeted fix: score={sc}, max_num={det['max_num']}")
    return best_grid


# ===================================================================
# SAVE RESULTS
# ===================================================================

def save_results(grid, output_path):
    """Save grid data to JSON."""
    valid, numbering = validate_grid(grid)
    across_lengths, down_lengths = compute_entry_lengths(grid, numbering)

    numbering_map = {}
    for num, info in numbering.items():
        entry = {
            'row': info['row'],
            'col': info['col'],
            'starts_across': info['across'],
            'starts_down': info['down'],
        }
        if info['across'] and num in across_lengths:
            entry['across_length'] = across_lengths[num]
        if info['down'] and num in down_lengths:
            entry['down_length'] = down_lengths[num]
        numbering_map[str(num)] = entry

    entry_catalog = {
        'across': {str(k): v for k, v in sorted(across_lengths.items())},
        'down': {str(k): v for k, v in sorted(down_lengths.items())}
    }

    black_count = sum(sum(row) for row in grid)
    max_num = max(numbering.keys()) if numbering else 0

    result = {
        'valid': valid,
        'grid_size': N,
        'grid': grid,
        'black_cells': black_count,
        'white_cells': N*N - black_count,
        'total_numbers': len(numbering),
        'max_number': max_num,
        'numbering_map': numbering_map,
        'entry_lengths': entry_catalog,
        'across_count': len([n for n in numbering.values() if n['across']]),
        'down_count': len([n for n in numbering.values() if n['down']]),
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\nSaved to {output_path}")
    print(f"  Valid: {valid}")
    print(f"  Black cells: {black_count}")
    print(f"  Numbers: {len(numbering)} (max={max_num})")
    return result


def save_grid_image(grid, path, numbering=None, scale=30):
    """Save grid as PNG with optional numbers."""
    n = len(grid)
    img = Image.new('RGB', (n*scale+1, n*scale+1), (255,255,255))
    draw = ImageDraw.Draw(img)

    for r in range(n):
        for c in range(n):
            x0, y0 = c*scale, r*scale
            x1, y1 = x0+scale, y0+scale
            if grid[r][c] == 1:
                draw.rectangle([x0,y0,x1,y1], fill=(0,0,0))
            else:
                draw.rectangle([x0,y0,x1,y1], outline=(180,180,180))

    # Draw thick outer border
    draw.rectangle([0, 0, n*scale, n*scale], outline=(0,0,0), width=2)

    # Draw numbers if provided
    if numbering:
        for num, info in numbering.items():
            r, c = info['row'], info['col']
            x = c * scale + 2
            y = r * scale + 1
            draw.text((x, y), str(num), fill=(100, 0, 0))

    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    print(f"Grid image saved to {path}")


def print_grid(grid, numbering=None):
    """Print ASCII grid."""
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


# ===================================================================
# MAIN
# ===================================================================

def main():
    print("=" * 70)
    print("MILLION-DOLLAR CROSSWORD GRID EXTRACTION v2")
    print("=" * 70)

    output_path = "/home/user/MB/analysis/grid_data_validated.json"
    image_path = "/home/user/MB/analysis/grid_validated.png"

    # Step 1: Load image
    print("\nLoading PDF image...")
    gray, W, H = load_grid_image()
    print(f"Image size: {W}x{H}")

    # Step 2: Search for correct alignment
    grid, details = search_grid_alignment(gray, W, H)

    if details.get('perfect'):
        print("\n*** FOUND PERFECT GRID ***")
        valid, numbering = validate_grid(grid)
        save_results(grid, output_path)
        save_grid_image(grid, image_path, numbering)
        print_grid(grid, numbering)
        return

    # Step 3: Hill climbing
    grid = hill_climb(grid)
    sc, det = score_grid(grid)

    if det['perfect']:
        print("\n*** HILL CLIMBING FOUND PERFECT GRID ***")
        valid, numbering = validate_grid(grid)
        save_results(grid, output_path)
        save_grid_image(grid, image_path, numbering)
        print_grid(grid, numbering)
        return

    # Step 4: Targeted fix
    grid = targeted_fix(grid)
    sc, det = score_grid(grid)

    if det['perfect']:
        print("\n*** TARGETED FIX FOUND PERFECT GRID ***")
        valid, numbering = validate_grid(grid)
        save_results(grid, output_path)
        save_grid_image(grid, image_path, numbering)
        print_grid(grid, numbering)
        return

    # Step 5: More hill climbing after targeted fix
    grid = hill_climb(grid, max_rounds=200)
    sc, det = score_grid(grid)

    # Save best attempt
    print(f"\nSaving best attempt (score={sc}, max_num={det['max_num']})")
    save_results(grid, output_path)
    save_grid_image(grid, image_path)
    print_grid(grid)

    if not det['perfect']:
        print("\nWARNING: Grid validation failed. Manual review needed.")
        print(f"  Score: {sc}")
        print(f"  Details: {det}")


if __name__ == '__main__':
    main()
