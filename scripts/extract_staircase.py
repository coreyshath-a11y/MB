#!/usr/bin/env python3
"""
Extract the staircase grid structure from the Million Dollar Crossword PDF.

The staircase is a small grid in the bottom-right corner of the crossword puzzle page.
It contains gray/shaded cells forming a staircase pattern with 11 rows.
Each row represents a word entry; adjacent rows share overlapping cells vertically.

Uses numpy for fast pixel-level analysis.
Detects grid lines via projection profiles with peak detection.
"""

import fitz  # PyMuPDF
import numpy as np
import json
import os

# --- Configuration ---
PDF_PATH = "/home/user/MB/puzzles/Million-Dollar-Crossword.pdf"
OUTPUT_JSON = "/home/user/MB/analysis/staircase_structure.json"

ZOOM = 6

# Tighter crop around just the staircase grid area
# (avoids clue number text on the left)
CROP_X_MIN_FRAC = 0.60
CROP_Y_MIN_FRAC = 0.77
CROP_X_MAX_FRAC = 0.97
CROP_Y_MAX_FRAC = 0.99

# Brightness thresholds
GRAY_MIN = 160
GRAY_MAX = 220
BLACK_MAX = 60
WHITE_MIN = 235

# Minimum count for a strong grid line (line that spans multiple cells)
H_LINE_MIN_COUNT = 200  # horizontal line: many dark pixels across
V_LINE_MIN_COUNT = 70   # vertical line: many dark pixels down


def load_pdf_region():
    """Load PDF, render at high res, return numpy array of brightness."""
    doc = fitz.open(PDF_PATH)
    page = doc[0]
    pw, ph = page.rect.width, page.rect.height

    clip = fitz.Rect(
        pw * CROP_X_MIN_FRAC, ph * CROP_Y_MIN_FRAC,
        pw * CROP_X_MAX_FRAC, ph * CROP_Y_MAX_FRAC
    )

    mat = fitz.Matrix(ZOOM, ZOOM)
    pix = page.get_pixmap(matrix=mat, clip=clip)
    doc.close()

    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    brightness = img[:, :, :3].mean(axis=2).astype(np.float32)

    print(f"Region: {pix.width} x {pix.height} pixels")
    return brightness, pix.width, pix.height


def find_major_lines(brt):
    """
    Find major grid lines by projection profile peak detection.
    Returns horizontal line y-positions and vertical line x-positions.
    """
    h, w = brt.shape
    is_dark = brt <= BLACK_MAX

    # Horizontal profile: sum dark pixels per row
    h_profile = is_dark.sum(axis=1).astype(float)
    # Vertical profile: sum dark pixels per column
    v_profile = is_dark.sum(axis=0).astype(float)

    # Find peaks in h_profile (strong horizontal lines)
    h_lines = find_peaks_in_profile(h_profile, min_count=H_LINE_MIN_COUNT, label="H")
    v_lines = find_peaks_in_profile(v_profile, min_count=V_LINE_MIN_COUNT, label="V")

    return h_lines, v_lines


def find_peaks_in_profile(profile, min_count, label=""):
    """Find peak positions in a 1D profile."""
    peaks = []
    above = profile >= min_count

    in_peak = False
    peak_start = 0
    peak_max_val = 0
    peak_max_pos = 0

    for i in range(len(profile)):
        if above[i]:
            if not in_peak:
                peak_start = i
                peak_max_val = profile[i]
                peak_max_pos = i
                in_peak = True
            elif profile[i] > peak_max_val:
                peak_max_val = profile[i]
                peak_max_pos = i
        else:
            if in_peak:
                center = (peak_start + i - 1) // 2
                peaks.append({
                    'pos': center,
                    'max_pos': peak_max_pos,
                    'max_val': int(peak_max_val),
                    'width': i - peak_start
                })
                in_peak = False

    if in_peak:
        center = (peak_start + len(profile) - 1) // 2
        peaks.append({
            'pos': center,
            'max_pos': peak_max_pos,
            'max_val': int(peak_max_val),
            'width': len(profile) - peak_start
        })

    print(f"\n{label} peaks ({len(peaks)}):")
    for p in peaks:
        print(f"  pos={p['pos']:4d} (max at {p['max_pos']}, val={p['max_val']}, w={p['width']})")

    return peaks


def filter_grid_peaks(peaks, expected_spacing_range=(60, 90)):
    """
    From a set of peaks, select those that form a regular grid.

    Strategy:
    1. Find the largest subset of peaks with consistent spacing (~74px for this grid)
    2. Filter out noise peaks (text, artifacts)
    """
    if len(peaks) < 2:
        return [p['pos'] for p in peaks]

    positions = [p['pos'] for p in peaks]
    values = [p['max_val'] for p in peaks]

    best_lines = []

    # Try each pair of peaks as potential grid neighbors
    lo, hi = expected_spacing_range
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            spacing = positions[j] - positions[i]
            if lo <= spacing <= hi:
                # Found a pair with good spacing. Extend the grid in both directions
                grid = _extend_grid(positions, values, positions[i], spacing, lo, hi)
                if len(grid) > len(best_lines):
                    best_lines = grid

    if not best_lines:
        # Fallback: just use all peaks sorted
        print("  WARNING: Could not find regular grid, using all peaks")
        return sorted(positions)

    best_lines.sort()
    print(f"  Selected {len(best_lines)} grid lines with ~{best_lines[1]-best_lines[0]}px spacing")
    return best_lines


def _extend_grid(all_positions, all_values, start, spacing, lo, hi):
    """Extend a grid from a start position, finding peaks near expected positions."""
    grid = [start]

    # Extend right
    expected = start + spacing
    while expected < max(all_positions) + spacing:
        # Find closest peak to expected position
        best = None
        best_dist = hi  # max allowable deviation
        for pos in all_positions:
            dist = abs(pos - expected)
            if dist < best_dist:
                best_dist = dist
                best = pos
        if best is not None and best_dist < spacing * 0.3:
            grid.append(best)
            expected = best + spacing
        else:
            break

    # Extend left
    expected = start - spacing
    while expected > min(all_positions) - spacing:
        best = None
        best_dist = hi
        for pos in all_positions:
            dist = abs(pos - expected)
            if dist < best_dist:
                best_dist = dist
                best = pos
        if best is not None and best_dist < spacing * 0.3:
            grid.insert(0, best)
            expected = best - spacing
        else:
            break

    return grid


def refine_grid_lines(peaks, expected_spacing=None, expected_spacing_range=(60, 90)):
    """
    Given detected peaks, determine the regular grid line positions.
    First filter to find regular grid, then fill in missing lines.
    """
    if not peaks:
        return []

    # Filter peaks to find regular grid
    positions = filter_grid_peaks(peaks, expected_spacing_range)

    if len(positions) < 2:
        return positions

    # Calculate spacings
    spacings = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
    print(f"  Spacings: {spacings}")

    if expected_spacing is None:
        expected_spacing = int(np.median(spacings))
    print(f"  Expected spacing: {expected_spacing}")

    # Fill in missing lines
    refined = [positions[0]]
    for i in range(1, len(positions)):
        gap = positions[i] - refined[-1]
        if gap > expected_spacing * 1.5:
            n_missing = round(gap / expected_spacing) - 1
            for j in range(1, n_missing + 1):
                interp = refined[-1] + int(j * gap / (n_missing + 1))
                refined.append(interp)
                print(f"  Interpolated missing line at {interp}")
        refined.append(positions[i])

    return refined


def check_cell_gray(brt, y1, y2, x1, x2):
    """Check if a cell region contains gray fill."""
    margin = 6
    y1i = y1 + margin
    y2i = y2 - margin
    x1i = x1 + margin
    x2i = x2 - margin

    if y2i <= y1i or x2i <= x1i:
        return False, 0.0

    cell = brt[y1i:y2i, x1i:x2i]
    gray_mask = (cell >= GRAY_MIN) & (cell <= GRAY_MAX)
    fraction = float(gray_mask.sum()) / max(cell.size, 1)

    return fraction > 0.25, fraction


def main():
    print("=" * 70)
    print("STAIRCASE GRID EXTRACTOR - High Precision")
    print("=" * 70)

    # Load
    print("\n--- Loading PDF ---")
    brt, img_w, img_h = load_pdf_region()

    # Find major grid lines
    print("\n--- Finding major grid lines ---")
    h_peaks, v_peaks = find_major_lines(brt)

    # Refine grid lines (fill in missing ones)
    print("\n--- Refining horizontal lines ---")
    h_lines = refine_grid_lines(h_peaks)
    print(f"  Final H lines ({len(h_lines)}): {h_lines}")

    print("\n--- Refining vertical lines ---")
    v_lines = refine_grid_lines(v_peaks)
    print(f"  Final V lines ({len(v_lines)}): {v_lines}")

    # Validate spacing
    if len(h_lines) >= 2:
        h_gaps = [h_lines[i+1] - h_lines[i] for i in range(len(h_lines)-1)]
        print(f"\n  Row heights: {h_gaps}")
        print(f"  Mean: {np.mean(h_gaps):.1f}, Std: {np.std(h_gaps):.1f}")

    if len(v_lines) >= 2:
        v_gaps = [v_lines[i+1] - v_lines[i] for i in range(len(v_lines)-1)]
        print(f"  Col widths: {v_gaps}")
        print(f"  Mean: {np.mean(v_gaps):.1f}, Std: {np.std(v_gaps):.1f}")

    # Build grid
    print("\n--- Building cell grid ---")
    n_rows = len(h_lines) - 1
    n_cols = len(v_lines) - 1
    print(f"Grid: {n_rows} rows x {n_cols} cols")

    grid = []
    gray_fractions = []
    for r in range(n_rows):
        row = []
        row_fracs = []
        for c in range(n_cols):
            is_gray, frac = check_cell_gray(brt, h_lines[r], h_lines[r+1],
                                             v_lines[c], v_lines[c+1])
            row.append(1 if is_gray else 0)
            row_fracs.append(frac)
        grid.append(row)
        gray_fractions.append(row_fracs)

    # Print grid with gray fractions
    print("\n=== CELL GRAY FRACTIONS ===")
    print("     ", end="")
    for c in range(n_cols):
        print(f"  C{c} ", end="")
    print()
    for r in range(n_rows):
        print(f" R{r:02d}:", end="")
        for c in range(n_cols):
            f = gray_fractions[r][c]
            if f > 0.25:
                print(f" {f:.2f}"[0:5], end="")
            else:
                print("  .  ", end="")
        print()

    # Print binary grid
    print("\n=== CELL GRID (## = gray cell) ===")
    print("     ", end="")
    for c in range(n_cols):
        print(f" {c:2d}", end="")
    print()
    print("     ", end="")
    for c in range(n_cols):
        print("---", end="")
    print()

    for r in range(n_rows):
        print(f" {r:2d} |", end="")
        for c in range(n_cols):
            print(" ##" if grid[r][c] else "  .", end="")
        # Count cells in row
        count = sum(grid[r])
        print(f"  | {count} cells")

    # Extract row structure
    print("\n=== ROW STRUCTURE ===")
    row_groups = []
    for r in range(n_rows):
        groups = []
        in_group = False
        start = 0
        for c in range(n_cols):
            if grid[r][c]:
                if not in_group:
                    start = c
                    in_group = True
            else:
                if in_group:
                    groups.append((start, c - start))
                    in_group = False
        if in_group:
            groups.append((start, n_cols - start))
        row_groups.append(groups)

    for r, groups in enumerate(row_groups):
        if groups:
            desc = " + ".join(f"cols {s}-{s+n-1} ({n} cells)" for s, n in groups)
            print(f"  Row {r:2d}: {desc}")

    # Identify entries
    entries = []
    for r, groups in enumerate(row_groups):
        for start_col, n_cells in groups:
            entries.append({
                'row': r,
                'start_col': start_col,
                'n_cells': n_cells,
                'end_col': start_col + n_cells - 1
            })

    print(f"\nTotal entries: {len(entries)}")
    print(f"Cell counts: {[e['n_cells'] for e in entries]}")

    # Find overlaps between adjacent entries
    print("\n=== ADJACENT-ROW OVERLAPS ===")
    overlaps = []
    for i in range(len(entries) - 1):
        e1 = entries[i]
        e2 = entries[i + 1]

        # Check consecutive rows only
        if e2['row'] != e1['row'] + 1:
            continue

        shared = []
        for c in range(max(e1['start_col'], e2['start_col']),
                       min(e1['end_col'], e2['end_col']) + 1):
            if grid[e1['row']][c] and grid[e2['row']][c]:
                shared.append(c)

        overlap = {
            'entry_above': i,
            'entry_below': i + 1,
            'row_above': e1['row'],
            'row_below': e2['row'],
            'shared_columns': shared,
            'n_shared': len(shared),
            'positions_in_above': [c - e1['start_col'] for c in shared],
            'positions_in_below': [c - e2['start_col'] for c in shared]
        }
        overlaps.append(overlap)

        if shared:
            print(f"  Entry {i+1} ({e1['n_cells']} cells, row {e1['row']}) "
                  f"& Entry {i+2} ({e2['n_cells']} cells, row {e2['row']}):")
            print(f"    {len(shared)} shared cell(s) at col(s) {shared}")
            print(f"    Positions in Entry {i+1}: {overlap['positions_in_above']} "
                  f"(0-indexed within {e1['n_cells']}-cell word)")
            print(f"    Positions in Entry {i+2}: {overlap['positions_in_below']} "
                  f"(0-indexed within {e2['n_cells']}-cell word)")
        else:
            print(f"  Entry {i+1} & {i+2}: NO overlap (rows {e1['row']} & {e2['row']})")

    # ASCII visual
    print("\n\n" + "=" * 70)
    print("STAIRCASE ASCII VISUALIZATION")
    print("=" * 70)

    # Column headers
    print("\n     ", end="")
    for c in range(n_cols):
        print(f" C{c} ", end="")
    print()

    for r in range(n_rows):
        # Top border
        line = "     "
        for c in range(n_cols):
            if grid[r][c]:
                above = grid[r-1][c] if r > 0 else 0
                line += "+---"
            else:
                prev = grid[r][c-1] if c > 0 else 0
                if prev and grid[r][c-1]:
                    line += "+   "
                else:
                    line += "    "
        # Closing +
        last_in_row = -1
        for c in range(n_cols-1, -1, -1):
            if grid[r][c]:
                last_in_row = c
                break
        if last_in_row >= 0:
            line = line[:5 + (last_in_row+1)*4] + "+"
        print(line)

        # Cell content
        row_str = f" R{r:02d} "
        for c in range(n_cols):
            if grid[r][c]:
                row_str += "| _ "
            else:
                prev = grid[r][c-1] if c > 0 else 0
                if prev:
                    row_str += "|   "
                else:
                    row_str += "    "
        if last_in_row >= 0:
            row_str = row_str[:5 + (last_in_row+1)*4] + "|"
        print(row_str)

    # Bottom border
    if n_rows > 0:
        r = n_rows - 1
        line = "     "
        for c in range(n_cols):
            if grid[r][c]:
                line += "+---"
            else:
                prev = grid[r][c-1] if c > 0 else 0
                if prev:
                    line += "+   "
                else:
                    line += "    "
        last_in_row = -1
        for c in range(n_cols-1, -1, -1):
            if grid[r][c]:
                last_in_row = c
                break
        if last_in_row >= 0:
            line = line[:5 + (last_in_row+1)*4] + "+"
        print(line)

    # Simple compact view
    print("\n=== COMPACT VIEW ===")
    entry_idx = 0
    for r in range(n_rows):
        line = f"  Row {r:2d}: "
        for c in range(n_cols):
            if grid[r][c]:
                line += "[_]"
            else:
                line += " . "
        # Label entries
        for groups in [row_groups[r]]:
            if groups:
                for start, n in groups:
                    entry_idx += 1
                    line += f"  <- Entry {entry_idx} ({n} cells)"
        print(line)

    # Save JSON
    print("\n\n--- Saving JSON ---")
    result = {
        'grid': {
            'n_rows': n_rows,
            'n_cols': n_cols,
            'cells': grid
        },
        'entries': entries,
        'overlaps': overlaps,
        'row_structure': [
            {
                'row': r,
                'groups': [{'start_col': s, 'n_cells': n, 'end_col': s + n - 1} for s, n in groups]
            }
            for r, groups in enumerate(row_groups) if groups
        ],
        'grid_lines_px': {
            'horizontal': h_lines,
            'vertical': v_lines,
            'row_heights': [h_lines[i+1] - h_lines[i] for i in range(len(h_lines)-1)] if len(h_lines) >= 2 else [],
            'col_widths': [v_lines[i+1] - v_lines[i] for i in range(len(v_lines)-1)] if len(v_lines) >= 2 else []
        }
    }

    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {OUTPUT_JSON}")

    # Final summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Grid: {n_rows} rows x {n_cols} columns")
    print(f"Entries: {len(entries)}")
    print()
    print(f"{'#':>3} {'Row':>4} {'Start':>6} {'End':>4} {'Cells':>6}  Overlap w/ next")
    print("-" * 58)
    for i, e in enumerate(entries):
        overlap_desc = ""
        for o in overlaps:
            if o['entry_above'] == i:
                pa = o['positions_in_above']
                pb = o['positions_in_below']
                overlap_desc = (f"{o['n_shared']} shared: "
                                f"pos {pa} in this, pos {pb} in next")
        print(f"{i+1:3d} {e['row']:4d} {e['start_col']:6d} {e['end_col']:4d} {e['n_cells']:6d}  {overlap_desc}")

    # Validate against expected countries
    print("\n\n--- COUNTRY FIT VALIDATION ---")
    proposed = [
        ("OMAN", 4), ("GREECE", 6), ("ITALY", 5), ("JAPAN", 5),
        ("IRAN", 4), ("PERU", 4), ("SPAIN", 5), ("CIV", 3),
        ("GHANA", 5), ("KENYA", 5), ("LAOS", 4)
    ]

    if len(entries) == len(proposed):
        print(f"Entry count matches: {len(entries)} entries, {len(proposed)} countries")
        all_ok = True
        for i, (country, expected_len) in enumerate(proposed):
            actual = entries[i]['n_cells']
            match = actual == expected_len
            status = "OK" if match else "MISMATCH"
            if not match:
                all_ok = False
            print(f"  Entry {i+1}: {country:8s} needs {expected_len} cells, "
                  f"grid has {actual} -> {status}")

        if all_ok:
            print("\n  ALL COUNTRIES FIT!")

            # Check letter overlaps
            print("\n  Checking letter overlaps with proposed countries...")
            grid_letters = [['.' for _ in range(n_cols)] for _ in range(n_rows)]
            for i, (country, _) in enumerate(proposed):
                e = entries[i]
                for j, letter in enumerate(country):
                    col = e['start_col'] + j
                    grid_letters[e['row']][col] = letter

            print("\n  Filled grid:")
            for r in range(n_rows):
                row_str = "    "
                for c in range(n_cols):
                    if grid_letters[r][c] != '.':
                        row_str += f" {grid_letters[r][c]} "
                    elif grid[r][c]:
                        row_str += " _ "
                    else:
                        row_str += " . "
                print(row_str)

            # Check overlaps
            print("\n  Overlap letter consistency:")
            for o in overlaps:
                if o['n_shared'] == 0:
                    continue
                i = o['entry_above']
                j = o['entry_below']
                country_a = proposed[i][0]
                country_b = proposed[j][0]
                for col in o['shared_columns']:
                    letter_a = grid_letters[entries[i]['row']][col]
                    letter_b = grid_letters[entries[j]['row']][col]
                    match = letter_a == letter_b
                    status = "MATCH" if match else "CONFLICT"
                    print(f"    Col {col}: {country_a}[{col - entries[i]['start_col']}]={letter_a} "
                          f"vs {country_b}[{col - entries[j]['start_col']}]={letter_b} -> {status}")
    else:
        print(f"Entry count mismatch: {len(entries)} entries vs {len(proposed)} expected countries")
        print("Grid structure doesn't match expected 11 countries.")


if __name__ == '__main__':
    main()
