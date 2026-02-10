#!/usr/bin/env python3
"""
QR Code / Pattern Analysis for the MrBeast $1M Crossword Puzzle.

Tests whether the crossword grid (black=1, white=0) encodes a QR code,
DataMatrix, or other barcode pattern. Also tests various transformations.

The 25x25 grid is EXACTLY QR Version 2 size (25x25 modules).
"""
import json
import sys
from pathlib import Path

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    from pyzbar.pyzbar import decode as pyzbar_decode
    HAS_PYZBAR = True
except ImportError:
    HAS_PYZBAR = False

try:
    from pylibdmtx.pylibdmtx import decode as dmtx_decode
    HAS_DMTX = True
except ImportError:
    HAS_DMTX = False

PUZZLE_PATH = Path(__file__).parent / "puzzle.json"

def load_grid():
    with open(PUZZLE_PATH) as f:
        puzzle = json.load(f)
    return puzzle["grid"], puzzle["grid_size"]

def grid_to_binary(grid, invert=False):
    """Convert grid to binary matrix (1=black, 0=white).
    If invert, swap black/white."""
    size = len(grid)
    binary = []
    for r in range(size):
        row = []
        for c in range(size):
            val = 1 if grid[r][c] == 1 else 0
            if invert:
                val = 1 - val
            row.append(val)
        binary.append(row)
    return binary

def binary_to_image(binary, scale=10):
    """Convert binary grid to PIL image."""
    if not HAS_PIL:
        return None
    size = len(binary)
    img = Image.new("L", (size * scale, size * scale), 255)
    pixels = img.load()
    for r in range(size):
        for c in range(size):
            color = 0 if binary[r][c] == 1 else 255
            for dy in range(scale):
                for dx in range(scale):
                    pixels[c * scale + dx, r * scale + dy] = color
    return img

def try_decode_qr(img):
    """Try to decode as QR code."""
    results = []
    if HAS_PYZBAR:
        try:
            decoded = pyzbar_decode(img)
            for d in decoded:
                results.append({
                    "type": d.type,
                    "data": d.data.decode("utf-8", errors="replace"),
                    "rect": str(d.rect),
                })
        except Exception as e:
            results.append({"error": f"pyzbar: {e}"})
    return results

def try_decode_datamatrix(img):
    """Try to decode as DataMatrix."""
    results = []
    if HAS_DMTX:
        try:
            decoded = dmtx_decode(img)
            for d in decoded:
                results.append({
                    "type": "DataMatrix",
                    "data": d.data.decode("utf-8", errors="replace"),
                    "rect": str(d.rect),
                })
        except Exception as e:
            results.append({"error": f"dmtx: {e}"})
    return results

def check_qr_finder_patterns(binary):
    """Check if the grid has QR finder patterns in the correct positions.
    QR Version 2 (25x25) has 7x7 finder patterns at:
    - Top-left: (0,0) to (6,6)
    - Top-right: (0,18) to (6,24)
    - Bottom-left: (18,0) to (24,6)
    """
    size = len(binary)
    if size != 25:
        return {"match": False, "reason": f"Grid is {size}x{size}, not 25x25"}

    # Expected finder pattern (7x7)
    finder = [
        [1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1],
    ]

    positions = {
        "top_left": (0, 0),
        "top_right": (0, 18),
        "bottom_left": (18, 0),
    }

    results = {}
    for name, (sr, sc) in positions.items():
        match_count = 0
        total = 49  # 7x7
        for dr in range(7):
            for dc in range(7):
                r, c = sr + dr, sc + dc
                if 0 <= r < size and 0 <= c < size:
                    if binary[r][c] == finder[dr][dc]:
                        match_count += 1
        results[name] = {
            "match_pct": round(100 * match_count / total, 1),
            "matches": match_count,
            "total": total,
        }

    return results

def transform_grid(binary, transform):
    """Apply a transformation to the binary grid."""
    size = len(binary)
    if transform == "identity":
        return [row[:] for row in binary]
    elif transform == "rotate_90":
        return [[binary[size-1-c][r] for c in range(size)] for r in range(size)]
    elif transform == "rotate_180":
        return [[binary[size-1-r][size-1-c] for c in range(size)] for r in range(size)]
    elif transform == "rotate_270":
        return [[binary[c][size-1-r] for c in range(size)] for r in range(size)]
    elif transform == "flip_h":
        return [[binary[r][size-1-c] for c in range(size)] for r in range(size)]
    elif transform == "flip_v":
        return [[binary[size-1-r][c] for c in range(size)] for r in range(size)]
    elif transform == "transpose":
        return [[binary[c][r] for c in range(size)] for r in range(size)]
    elif transform == "fold_lr":
        # XOR left half with mirrored right half
        result = [[0]*size for _ in range(size)]
        for r in range(size):
            for c in range(size):
                left = binary[r][c]
                right = binary[r][size-1-c]
                result[r][c] = left ^ right
        return result
    elif transform == "fold_tb":
        # XOR top half with mirrored bottom half
        result = [[0]*size for _ in range(size)]
        for r in range(size):
            for c in range(size):
                top = binary[r][c]
                bottom = binary[size-1-r][c]
                result[r][c] = top ^ bottom
        return result
    return binary

def test_all_transforms(grid):
    """Test all grid transformations as QR/DataMatrix codes."""
    binary_normal = grid_to_binary(grid)
    binary_invert = grid_to_binary(grid, invert=True)

    transforms = [
        "identity", "rotate_90", "rotate_180", "rotate_270",
        "flip_h", "flip_v", "transpose",
        "fold_lr", "fold_tb",
    ]

    results = []
    for invert_name, binary in [("normal", binary_normal), ("inverted", binary_invert)]:
        for t in transforms:
            transformed = transform_grid(binary, t)
            img = binary_to_image(transformed, scale=10)
            if img is None:
                continue

            label = f"{invert_name}+{t}"

            # Try QR decode
            qr_results = try_decode_qr(img)
            dm_results = try_decode_datamatrix(img)

            # Check finder patterns
            finder_check = check_qr_finder_patterns(transformed)

            result = {
                "transform": label,
                "qr_decoded": qr_results,
                "datamatrix_decoded": dm_results,
                "finder_patterns": finder_check,
            }
            results.append(result)

            # Print progress
            finder_str = ""
            if isinstance(finder_check, dict) and "top_left" in finder_check:
                tl = finder_check["top_left"]["match_pct"]
                tr = finder_check["top_right"]["match_pct"]
                bl = finder_check["bottom_left"]["match_pct"]
                finder_str = f"  finders: TL={tl}% TR={tr}% BL={bl}%"

            decoded_str = ""
            if qr_results:
                for qr in qr_results:
                    if "data" in qr:
                        decoded_str += f"  QR: {qr['data']}"
            if dm_results:
                for dm in dm_results:
                    if "data" in dm:
                        decoded_str += f"  DM: {dm['data']}"

            status = "DECODED!" if decoded_str else "no decode"
            print(f"  {label:25s}: {status}{finder_str}{decoded_str}")

    return results

def analyze_grid_patterns(grid):
    """Analyze structural patterns in the grid."""
    size = len(grid)
    binary = grid_to_binary(grid)

    print("\nGrid Pattern Analysis:")
    print(f"  Size: {size}x{size}")

    # Count black cells
    black = sum(sum(row) for row in binary)
    total = size * size
    print(f"  Black cells: {black}/{total} ({100*black/total:.1f}%)")

    # Symmetry checks
    # 180-degree rotational symmetry (standard for crosswords)
    sym_180 = 0
    for r in range(size):
        for c in range(size):
            if binary[r][c] == binary[size-1-r][size-1-c]:
                sym_180 += 1
    print(f"  180° rotational symmetry: {sym_180}/{total} ({100*sym_180/total:.1f}%)")

    # Horizontal symmetry
    sym_h = 0
    for r in range(size):
        for c in range(size):
            if binary[r][c] == binary[r][size-1-c]:
                sym_h += 1
    print(f"  Horizontal symmetry: {sym_h}/{total} ({100*sym_h/total:.1f}%)")

    # Vertical symmetry
    sym_v = 0
    for r in range(size):
        for c in range(size):
            if binary[r][c] == binary[size-1-r][c]:
                sym_v += 1
    print(f"  Vertical symmetry: {sym_v}/{total} ({100*sym_v/total:.1f}%)")

    # Row/column black cell counts
    print("\n  Black cells per row:")
    for r in range(size):
        count = sum(binary[r])
        bar = "#" * count
        print(f"    Row {r+1:2d}: {count:2d} {bar}")

    print("\n  Black cells per column:")
    for c in range(size):
        count = sum(binary[r][c] for r in range(size))
        bar = "#" * count
        print(f"    Col {chr(65+c)}: {count:2d} {bar}")

def save_grid_images(grid):
    """Save grid as images in various transformations."""
    if not HAS_PIL:
        print("PIL not available, skipping image generation")
        return

    out_dir = Path(__file__).parent / "qr_tests"
    out_dir.mkdir(exist_ok=True)

    binary_normal = grid_to_binary(grid)
    binary_invert = grid_to_binary(grid, invert=True)

    transforms = ["identity", "rotate_90", "rotate_180", "rotate_270",
                   "flip_h", "flip_v", "fold_lr", "fold_tb"]

    for invert_name, binary in [("normal", binary_normal), ("inverted", binary_invert)]:
        for t in transforms:
            transformed = transform_grid(binary, t)
            img = binary_to_image(transformed, scale=10)
            if img:
                path = out_dir / f"grid_{invert_name}_{t}.png"
                img.save(str(path))

    print(f"\nSaved {len(transforms)*2} grid images to {out_dir}/")

def main():
    print("=" * 60)
    print("QR / Pattern Analysis for 25x25 Crossword Grid")
    print("=" * 60)

    print(f"\nLibrary status:")
    print(f"  numpy:    {'YES' if HAS_NUMPY else 'NO'}")
    print(f"  PIL:      {'YES' if HAS_PIL else 'NO'}")
    print(f"  pyzbar:   {'YES' if HAS_PYZBAR else 'NO'}")
    print(f"  pylibdmtx: {'YES' if HAS_DMTX else 'NO'}")

    grid, size = load_grid()
    print(f"\nGrid loaded: {size}x{size}")
    print(f"NOTE: 25x25 = QR Version 2 size!")

    # Analyze patterns
    analyze_grid_patterns(grid)

    # Test all transforms
    print("\nTesting all transformations as QR/DataMatrix:")
    results = test_all_transforms(grid)

    # Save images
    if "--save-images" in sys.argv or "-s" in sys.argv:
        save_grid_images(grid)

    # Summary
    any_decoded = False
    for r in results:
        if r["qr_decoded"] or r["datamatrix_decoded"]:
            for qr in r["qr_decoded"]:
                if "data" in qr:
                    any_decoded = True
            for dm in r["datamatrix_decoded"]:
                if "data" in dm:
                    any_decoded = True

    if any_decoded:
        print("\n*** DECODED DATA FOUND! ***")
    else:
        print("\nNo QR/DataMatrix data decoded from any transformation.")
        print("Possible next steps:")
        print("  1. Complete the grid (37 missing across entries)")
        print("  2. Try combining with braille/tank data")
        print("  3. Try partial grid regions as smaller codes")
        print("  4. Try filled crossword letters as code data")

if __name__ == "__main__":
    main()
