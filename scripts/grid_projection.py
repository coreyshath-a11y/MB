#!/usr/bin/env python3
"""
Extract the 21x21 grid using projection analysis.
Render at high res, crop to grid area, use row/col projections
to find grid line positions, then sample cells between lines.
"""

import json
import sys
import fitz
import numpy as np
from PIL import Image

ACROSS = [1,8,14,22,23,24,25,28,29,30,31,32,34,35,36,38,41,42,43,45,47,48,50,54,57,58,59,61,63,64,66,68,70,72,73,77,79,80,81,82,83,85,88,90,91,92,94,97,99,100,102,103,105,106,107,109,111,113,114,117,119,120,121,123,124,127,129,132,134,136,138,141,143,145,147,148,149,153,155,156,158,159,161,164,165,167,171,172,173,174,175,176]
DOWN = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,26,27,33,37,39,40,43,44,46,49,51,52,53,55,56,60,62,65,67,69,71,72,74,75,76,77,78,80,83,84,86,87,89,93,95,96,98,101,104,108,110,112,115,116,117,118,122,124,125,126,128,130,131,133,135,137,139,140,141,142,144,150,151,152,153,154,157,160,162,163,166,168,169,170]
ACROSS_SET = set(ACROSS)
DOWN_SET = set(DOWN)
SIZE = 21

def number_grid(grid):
    numbering = {}
    num = 1
    for r in range(SIZE):
        for c in range(SIZE):
            if grid[r][c] == 1:
                continue
            starts_a = (c == 0 or grid[r][c-1] == 1) and (c+1 < SIZE and grid[r][c+1] == 0)
            starts_d = (r == 0 or grid[r-1][c] == 1) and (r+1 < SIZE and grid[r+1][c] == 0)
            if starts_a or starts_d:
                numbering[num] = (r, c, starts_a, starts_d)
                num += 1
    return numbering, num - 1

def check_grid(grid):
    numbering, max_num = number_grid(grid)
    if max_num != 176:
        return False, max_num, 0
    correct = 0
    for n in range(1, 177):
        if n in numbering:
            _, _, is_a, is_d = numbering[n]
            if (is_a == (n in ACROSS_SET)) and (is_d == (n in DOWN_SET)):
                correct += 1
    return correct == 176, max_num, correct

def find_peaks(signal, min_distance=10, prominence=None):
    """Find peaks in a 1D signal with minimum distance constraint."""
    peaks = []
    n = len(signal)

    for i in range(1, n-1):
        if signal[i] > signal[i-1] and signal[i] >= signal[i+1]:
            if prominence is None or signal[i] > prominence:
                peaks.append(i)

    # Enforce minimum distance
    if min_distance > 1 and peaks:
        filtered = [peaks[0]]
        for p in peaks[1:]:
            if p - filtered[-1] >= min_distance:
                filtered.append(p)
        peaks = filtered

    return peaks

def main():
    pdf_path = "/home/user/MB/puzzles/Million-Dollar-Crossword.pdf"

    doc = fitz.open(pdf_path)
    page = doc[0]

    # Render at very high zoom
    zoom = 12
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    w, h = pix.width, pix.height
    print(f"Rendered at {zoom}x: {w} x {h}")

    # Convert to numpy
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(h, w, -1)
    gray = np.mean(arr[:,:,:3], axis=2)

    # Crop to approximate grid area
    # Try a range of crop areas
    crop_configs = [
        # (left_frac, right_frac, top_frac, bottom_frac)
        (0.360, 0.870, 0.055, 0.715),
        (0.358, 0.872, 0.054, 0.716),
        (0.362, 0.868, 0.056, 0.714),
    ]

    best_result = None
    best_correct = 0

    for lf, rf, tf, bf in crop_configs:
        l = int(w * lf)
        r = int(w * rf)
        t = int(h * tf)
        b = int(h * bf)

        crop = gray[t:b, l:r]
        ch, cw = crop.shape
        print(f"\nCrop ({lf},{rf},{tf},{bf}): {cw} x {ch}")

        # Create binary: dark pixels (grid lines, black cells, text)
        binary = (crop < 80).astype(float)

        # Vertical projection: sum along columns -> find vertical grid lines
        v_proj = np.sum(binary, axis=0)

        # Horizontal projection: sum along rows -> find horizontal grid lines
        h_proj = np.sum(binary, axis=1)

        # Grid lines are thin dark lines spanning most of the grid
        # They appear as peaks in the projections

        # Expected cell size
        expected_cell_w = cw / SIZE
        expected_cell_h = ch / SIZE
        min_peak_dist = int(expected_cell_w * 0.6)

        # Find vertical line positions (peaks in v_proj)
        v_threshold = ch * 0.3  # Grid lines span at least 30% of height
        v_peaks = find_peaks(v_proj, min_distance=min_peak_dist, prominence=v_threshold)

        # Find horizontal line positions
        h_threshold = cw * 0.3
        h_peaks = find_peaks(h_proj, min_distance=int(expected_cell_h * 0.6), prominence=h_threshold)

        print(f"  Expected cell size: {expected_cell_w:.1f} x {expected_cell_h:.1f}")
        print(f"  V peaks (thresh={v_threshold:.0f}): {len(v_peaks)}")
        print(f"  H peaks (thresh={h_threshold:.0f}): {len(h_peaks)}")

        # Try lower thresholds
        for v_thr_pct, h_thr_pct in [(0.2, 0.2), (0.15, 0.15), (0.1, 0.1), (0.25, 0.25)]:
            vt = ch * v_thr_pct
            ht = cw * h_thr_pct
            vp = find_peaks(v_proj, min_distance=min_peak_dist, prominence=vt)
            hp = find_peaks(h_proj, min_distance=int(expected_cell_h * 0.6), prominence=ht)

            if 20 <= len(vp) <= 25 and 20 <= len(hp) <= 25:
                print(f"  Found good peaks at thresh ({v_thr_pct},{h_thr_pct}): "
                      f"{len(vp)} v-lines, {len(hp)} h-lines")
                v_peaks = vp
                h_peaks = hp
                break

        # If we still don't have 22 lines, try uniform spacing
        if len(v_peaks) < 22 or len(h_peaks) < 22:
            print(f"  Not enough peaks ({len(v_peaks)} v, {len(h_peaks)} h). Trying uniform spacing...")

            # Use detected peaks to calibrate, or fall back to uniform
            if len(v_peaks) >= 5:
                # Use median spacing of detected peaks
                v_spacings = [v_peaks[i+1] - v_peaks[i] for i in range(len(v_peaks)-1)]
                v_cell = np.median(v_spacings)
                # Find the best starting position
                best_start = 0
                best_align = 0
                for start in range(int(v_cell)):
                    lines = [int(start + i * v_cell) for i in range(22)]
                    align = sum(1 for p in v_peaks for l in lines if abs(p - l) < v_cell * 0.15)
                    if align > best_align:
                        best_align = align
                        best_start = start
                v_peaks = [int(best_start + i * v_cell) for i in range(22)]
                print(f"  V: Using calibrated uniform with cell={v_cell:.1f}, start={best_start}")
            else:
                v_peaks = [int(i * cw / SIZE) for i in range(22)]
                print(f"  V: Using pure uniform")

            if len(h_peaks) >= 5:
                h_spacings = [h_peaks[i+1] - h_peaks[i] for i in range(len(h_peaks)-1)]
                h_cell = np.median(h_spacings)
                best_start = 0
                best_align = 0
                for start in range(int(h_cell)):
                    lines = [int(start + i * h_cell) for i in range(22)]
                    align = sum(1 for p in h_peaks for l in lines if abs(p - l) < h_cell * 0.15)
                    if align > best_align:
                        best_align = align
                        best_start = start
                h_peaks = [int(best_start + i * h_cell) for i in range(22)]
                print(f"  H: Using calibrated uniform with cell={h_cell:.1f}, start={best_start}")
            else:
                h_peaks = [int(i * ch / SIZE) for i in range(22)]
                print(f"  H: Using pure uniform")

        # Ensure exactly 22 lines
        v_peaks = v_peaks[:22]
        h_peaks = h_peaks[:22]

        if len(v_peaks) < 22:
            v_peaks = [int(i * cw / SIZE) for i in range(22)]
        if len(h_peaks) < 22:
            h_peaks = [int(i * ch / SIZE) for i in range(22)]

        # Now sample each cell
        # For each threshold, build a grid and test it
        for thresh in [60, 70, 80, 90, 100, 110, 120, 130, 140, 150]:
            grid = [[0]*SIZE for _ in range(SIZE)]

            for row in range(SIZE):
                y1 = h_peaks[row]
                y2 = h_peaks[row+1] if row+1 < len(h_peaks) else ch

                # Sample center region (avoid edges where grid lines are)
                margin_y = int((y2 - y1) * 0.25)
                cy1 = y1 + margin_y
                cy2 = y2 - margin_y

                for col in range(SIZE):
                    x1 = v_peaks[col]
                    x2 = v_peaks[col+1] if col+1 < len(v_peaks) else cw

                    margin_x = int((x2 - x1) * 0.25)
                    cx1 = x1 + margin_x
                    cx2 = x2 - margin_x

                    if cy1 < cy2 and cx1 < cx2:
                        cell = crop[cy1:cy2, cx1:cx2]
                        avg = np.mean(cell)
                        grid[row][col] = 1 if avg < thresh else 0
                    else:
                        grid[row][col] = 0

            valid, max_num, correct = check_grid(grid)
            black = sum(sum(row) for row in grid)

            if correct > best_correct or (correct == best_correct and valid):
                best_correct = correct
                best_result = {
                    'grid': [row[:] for row in grid],
                    'thresh': thresh,
                    'crop': (lf, rf, tf, bf),
                    'v_peaks': [int(p) for p in v_peaks],
                    'h_peaks': [int(p) for p in h_peaks],
                    'valid': valid,
                    'max_num': max_num,
                    'correct': correct,
                    'black': black,
                }
                print(f"  thresh={thresh}: max_num={max_num}, correct={correct}/176, "
                      f"black={black}, valid={valid}")

                if valid:
                    break

        if best_result and best_result['valid']:
            break

    if not best_result:
        print("\nNo good result found!")
        return

    print(f"\n{'='*60}")
    print(f"BEST RESULT: correct={best_result['correct']}/176, "
          f"valid={best_result['valid']}, thresh={best_result['thresh']}")
    print(f"{'='*60}")

    grid = best_result['grid']

    # Print grid
    for r, row in enumerate(grid):
        line = f"{r:2d} "
        for cell in row:
            line += "██" if cell == 1 else "░░"
        print(line)

    black = sum(sum(row) for row in grid)
    print(f"Black: {black}, White: {SIZE*SIZE - black}")

    # If not perfect, try hill-climbing repair
    if not best_result['valid']:
        print("\nAttempting hill-climbing repair...")

        def score(g):
            _, mx, corr = check_grid(g)
            return corr - abs(mx - 176) * 5

        current = score(grid)
        improved = True
        iteration = 0

        while improved and iteration < 100:
            improved = False
            iteration += 1

            for r in range(SIZE):
                for c in range(SIZE):
                    grid[r][c] = 1 - grid[r][c]
                    s = score(grid)
                    if s > current:
                        current = s
                        improved = True
                        valid, mx, corr = check_grid(grid)
                        if valid:
                            print(f"PERFECT GRID FOUND at iteration {iteration}!")
                            improved = False
                            break
                    else:
                        grid[r][c] = 1 - grid[r][c]
                if not improved or (check_grid(grid)[0]):
                    break

            if iteration % 5 == 0:
                _, mx, corr = check_grid(grid)
                print(f"  Iteration {iteration}: score={current}, correct={corr}/176, max_num={mx}")

    # Final check
    valid, max_num, correct = check_grid(grid)
    print(f"\nFinal: valid={valid}, max_num={max_num}, correct={correct}/176")

    # Save
    numbering, _ = number_grid(grid)

    entries = {}
    for num, (r, c, is_a, is_d) in numbering.items():
        if is_a:
            length = 0
            cc = c
            while cc < SIZE and grid[r][cc] == 0:
                length += 1
                cc += 1
            entries[f"{num}A"] = {'cells': [(r, c+i) for i in range(length)], 'length': length, 'start': [r,c]}
        if is_d:
            length = 0
            rr = r
            while rr < SIZE and grid[rr][c] == 0:
                length += 1
                rr += 1
            entries[f"{num}D"] = {'cells': [(r+i, c) for i in range(length)], 'length': length, 'start': [r,c]}

    results = {
        'grid': grid,
        'valid': valid,
        'max_num': max_num,
        'correct': correct,
        'black_cells': sum(sum(row) for row in grid),
        'entries': entries,
        'numbering': {str(k): {'row': v[0], 'col': v[1], 'across': v[2], 'down': v[3]}
                     for k, v in numbering.items()},
    }

    out_path = '/home/user/MB/analysis/grid_final.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)

    # Print key entries
    for key in ['167A', '149A', '1A', '1D', '174A']:
        if key in entries:
            print(f"  {key}: length {entries[key]['length']} at {entries[key]['start']}")

    print(f"\nSaved to {out_path}")

if __name__ == '__main__':
    main()
